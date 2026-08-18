from __future__ import annotations

import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.parse
import zipfile
from pathlib import Path
from typing import Any

from .common import (BUILD_CACHE, CACHE, GAME, MOD_CACHE, ROOT, WORLD_TEMPLATE, download,
                     log, pmc_base, request_json, run, safe_rmtree)


def java_version(java: Path) -> str:
    try:
        cp = run([str(java), "-version"], check=False, capture=True, timeout=15)
        return (cp.stderr or cp.stdout).splitlines()[0]
    except Exception:
        return "unknown"


def find_java25() -> Path:
    names = {"java.exe"} if os.name == "nt" else {"java"}
    candidates: list[Path] = []
    for base in [GAME / "jvm", GAME]:
        if base.exists():
            for name in names:
                candidates.extend(base.rglob(name))
    for p in candidates:
        if p.is_file() and '"25' in java_version(p):
            return p
    for p in candidates:
        if p.is_file():
            return p
    raise RuntimeError("PortableMC did not install a usable Java runtime")


def java_env(java: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["JAVA_HOME"] = str(java.parent.parent)
    env["PATH"] = str(java.parent) + os.pathsep + env.get("PATH", "")
    return env


def ensure_game_and_java(cfg: dict[str, Any]) -> Path:
    GAME.mkdir(parents=True, exist_ok=True)
    mc = cfg["minecraft_version"]
    log(f"[setup] Installing Minecraft {mc}, Fabric and runtime into {GAME}")
    run(pmc_base() + ["start", "--dry", "-u", "BenchUser", f"fabric:{mc}"])
    java = find_java25()
    log(f"[setup] Java: {java} ({java_version(java)})")
    return java


def resolve_modrinth_project(slug_or_id: str, mc: str):
    project = request_json("https://api.modrinth.com/v2/project/" + urllib.parse.quote(slug_or_id, safe=""))
    query = urllib.parse.urlencode({"loaders": json.dumps(["fabric"]), "game_versions": json.dumps([mc])})
    versions = request_json(f"https://api.modrinth.com/v2/project/{project['id']}/version?{query}")
    if not versions:
        raise RuntimeError(f"No Fabric {mc} build found for Modrinth project {slug_or_id}")
    version = next((v for v in versions if v.get("version_type") == "release"), versions[0])
    return project, version


def resolve_and_download_mods(cfg: dict[str, Any], force: bool = False) -> dict[str, Any]:
    mc = cfg["minecraft_version"]
    requested = list(cfg["base_mods"])
    for c in cfg["configs"]:
        requested.extend(c.get("mods", []))
    requested = list(dict.fromkeys(requested))
    MOD_CACHE.mkdir(parents=True, exist_ok=True)
    projects: dict[str, dict[str, Any]] = {}
    groups: dict[str, list[str]] = {}

    def add(slug_or_id: str, root_slug: str) -> None:
        project, version = resolve_modrinth_project(slug_or_id, mc)
        pid = project["id"]
        groups.setdefault(root_slug, [])
        if pid not in groups[root_slug]:
            groups[root_slug].append(pid)
        if pid in projects:
            return
        file = next((f for f in version["files"] if f.get("primary")), version["files"][0])
        dst = MOD_CACHE / file["filename"]
        if force or not dst.exists():
            log(f"[mods] {project['slug']} {version['version_number']}")
            download(file["url"], dst)
        projects[pid] = {"project_id": pid, "slug": project["slug"], "title": project.get("title", project["slug"]),
                         "version_id": version["id"], "version": version["version_number"], "file": file["filename"],
                         "sha512": file.get("hashes", {}).get("sha512")}
        for dep in version.get("dependencies", []):
            if dep.get("dependency_type") == "required" and dep.get("project_id"):
                dep_project = request_json("https://api.modrinth.com/v2/project/" + dep["project_id"])
                add(dep_project["slug"], root_slug)
                if dep_project["id"] not in groups[root_slug]:
                    groups[root_slug].append(dep_project["id"])

    for slug in requested:
        add(slug, slug)
    payload = {"minecraft": mc, "resolved_at": dt.datetime.now().astimezone().isoformat(),
               "projects": projects, "groups": groups}
    (MOD_CACHE / "resolved-mods.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def ensure_objectbench(java: Path, cfg: dict[str, Any], rebuild: bool = False) -> Path:
    jar = BUILD_CACHE / "objectbench.jar"
    src_java = ROOT / "objectbench" / "ObjectBenchClient.java"
    src_meta = ROOT / "objectbench" / "fabric.mod.json"
    signature = BUILD_CACHE / "source-signature.txt"
    sig = str(hash((src_java.read_text(encoding="utf-8"), src_meta.read_text(encoding="utf-8"), cfg["minecraft_version"])))
    if jar.exists() and signature.exists() and signature.read_text() == sig and not rebuild:
        return jar
    safe_rmtree(BUILD_CACHE); BUILD_CACHE.mkdir(parents=True, exist_ok=True)
    mc = cfg["minecraft_version"]
    archive = CACHE / f"fabric-example-mod-{mc}.zip"
    if rebuild or not archive.exists():
        download(f"https://github.com/FabricMC/fabric-example-mod/archive/refs/heads/{mc}.zip", archive)
    with zipfile.ZipFile(archive) as z:
        z.extractall(BUILD_CACHE)
    roots = [p for p in BUILD_CACHE.iterdir() if p.is_dir() and p.name.startswith("fabric-example-mod-")]
    if not roots:
        raise RuntimeError("Could not extract Fabric example mod")
    project = roots[0]
    for d in [project / "src/main/java", project / "src/client/java"]:
        safe_rmtree(d)
    for d in [project / "src/main/resources", project / "src/client/resources"]:
        if d.exists():
            for p in d.iterdir():
                safe_rmtree(p) if p.is_dir() else p.unlink()
    (project / "src/client/java/bench").mkdir(parents=True, exist_ok=True)
    (project / "src/main/resources").mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_java, project / "src/client/java/bench/ObjectBenchClient.java")
    shutil.copy2(src_meta, project / "src/main/resources/fabric.mod.json")
    gradle = project / "build.gradle"
    gradle.write_text(gradle.read_text(encoding="utf-8").replace('"modid"', '"objectbench"'), encoding="utf-8")
    wrapper = project / ("gradlew.bat" if os.name == "nt" else "gradlew")
    if os.name != "nt": wrapper.chmod(wrapper.stat().st_mode | 0o111)
    log("[build] Compiling ObjectBench...")
    run([str(wrapper), "build", "--no-daemon", "-q"], cwd=project, env=java_env(java), timeout=300)
    built = [p for p in (project / "build/libs").glob("*.jar") if "sources" not in p.name]
    if not built: raise RuntimeError("ObjectBench build produced no jar")
    shutil.copy2(built[0], jar); signature.write_text(sig)
    return jar


def mojang_server_url(mc: str) -> str:
    manifest = request_json("https://piston-meta.mojang.com/mc/game/version_manifest_v2.json")
    meta = request_json(next(x["url"] for x in manifest["versions"] if x["id"] == mc))
    return meta["downloads"]["server"]["url"]


def wait_for_text(path: Path, needle: str, timeout: int) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if path.exists() and needle in path.read_text(errors="ignore"):
            return True
        time.sleep(.5)
    return False


def build_world(java: Path, cfg: dict[str, Any], accept_eula: bool, rebuild: bool = False) -> None:
    marker = WORLD_TEMPLATE / ".objectbench-v3"
    if marker.exists() and not rebuild: return
    if not accept_eula:
        if not sys.stdin.isatty():
            raise RuntimeError("Minecraft EULA acceptance required; re-run with --accept-eula after reviewing https://aka.ms/MinecraftEULA")
        print("\nReview the Minecraft EULA: https://aka.ms/MinecraftEULA")
        if input("Type YES to accept and continue: ").strip() != "YES":
            raise SystemExit("EULA not accepted; benchmark cancelled.")
    worldgen = CACHE / "worldgen"; safe_rmtree(worldgen); worldgen.mkdir(parents=True)
    server_jar = CACHE / f"minecraft-server-{cfg['minecraft_version']}.jar"
    if rebuild or not server_jar.exists(): download(mojang_server_url(cfg["minecraft_version"]), server_jar)
    shutil.copy2(server_jar, worldgen / "server.jar")
    (worldgen / "eula.txt").write_text("eula=true\n")
    (worldgen / "server.properties").write_text("level-name=benchworld\nlevel-seed=7608123456789\nlevel-type=minecraft:flat\ngamemode=creative\ndifficulty=peaceful\nonline-mode=false\nview-distance=12\nsimulation-distance=8\nspawn-protection=0\n")
    server_log = worldgen / "server.log"; out = server_log.open("w", encoding="utf-8")
    p = subprocess.Popen([str(java), "-Xms1G", "-Xmx2G", "-jar", "server.jar", "nogui"], cwd=worldgen,
                         stdin=subprocess.PIPE, stdout=out, stderr=subprocess.STDOUT, text=True, env=java_env(java))
    if not wait_for_text(server_log, "Done (", 90):
        p.kill(); out.close(); raise RuntimeError("Minecraft server did not start; see .mcbench/cache/worldgen/server.log")
    def cmd(s: str, delay: float=.04):
        assert p.stdin is not None; p.stdin.write(s + "\n"); p.stdin.flush(); time.sleep(delay)
    commands = [
        "gamerule randomTickSpeed 0","gamerule doMobSpawning false","gamerule doWeatherCycle false","gamerule doDaylightCycle false","time set noon","weather clear",
        "fill -48 3 -48 48 3 48 minecraft:smooth_stone","fill -40 4 -5 40 15 -3 minecraft:oak_leaves","fill -40 4 2 40 15 4 minecraft:glass","fill -40 4 9 40 12 11 minecraft:oak_fence","fill -40 4 16 40 12 18 minecraft:iron_bars","fill -40 4 23 40 12 25 minecraft:cobblestone_wall","fill -40 4 30 40 10 32 minecraft:stone_stairs","fill -40 4 37 40 8 39 minecraft:oak_trapdoor",
        "fill 112 3 -48 208 3 48 minecraft:smooth_stone","fill 120 4 -5 200 20 -3 minecraft:stone","fill 136 8 -5 143 14 -3 minecraft:air","fill 160 8 -5 167 14 -3 minecraft:air","fill 184 8 -5 191 14 -3 minecraft:air","fill 132 4 22 188 9 24 minecraft:barrel",
        "fill 272 3 -48 368 3 48 minecraft:smooth_stone","fill 280 4 3 360 10 5 minecraft:glass","fill 280 4 10 360 12 12 minecraft:oak_leaves","fill 280 4 17 360 10 19 minecraft:iron_bars","fill 288 4 27 352 9 29 minecraft:barrel","fill 288 4 35 352 8 37 minecraft:oak_fence"]
    for c in commands: cmd(c)
    for x in range(126,199,6):
        for z in range(4,33,4): cmd(f"summon minecraft:cow {x} 4 {z} {{NoAI:1b,Silent:1b,Invulnerable:1b,PersistenceRequired:1b}}",.02)
    for x in range(286,359,8):
        for z in range(-2,24,5): cmd(f"summon minecraft:cow {x} 4 {z} {{NoAI:1b,Silent:1b,Invulnerable:1b,PersistenceRequired:1b}}",.02)
    for c in ["forceload add -64 -64 64 64","forceload add 96 -64 224 64","forceload add 256 -64 384 64","save-all flush"]: cmd(c)
    time.sleep(8); cmd("save-all flush"); time.sleep(2); cmd("stop")
    try: p.wait(timeout=30)
    except subprocess.TimeoutExpired: p.kill()
    out.close(); safe_rmtree(WORLD_TEMPLATE); shutil.copytree(worldgen / "benchworld", WORLD_TEMPLATE)
    (WORLD_TEMPLATE / ".objectbench-v3").write_text("controlled world v3\n")
    log(f"[world] Built {WORLD_TEMPLATE}")
