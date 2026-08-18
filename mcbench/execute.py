from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import time
from pathlib import Path
from typing import Any

import psutil

from .common import GAME, MOD_CACHE, WORLD_TEMPLATE, log, pmc_base, safe_rmtree
from .prepare import java_env


def install_selected_mods(manifest: dict[str, Any], base_mods: list[str], selected: dict[str, Any], objectbench: Path) -> list[str]:
    mods_dir = GAME / "mods"; mods_dir.mkdir(parents=True, exist_ok=True)
    for p in mods_dir.glob("*.jar"): p.unlink()
    slugs = list(base_mods) + list(selected.get("mods", [])); ids: list[str] = []
    for slug in slugs:
        for pid in manifest["groups"][slug]:
            if pid not in ids: ids.append(pid)
    files = []
    for pid in ids:
        item = manifest["projects"][pid]; src = MOD_CACHE / item["file"]
        shutil.copy2(src, mods_dir / src.name); files.append(src.name)
    shutil.copy2(objectbench, mods_dir / "objectbench.jar"); files.append("objectbench.jar")
    return files


def find_fabric_json(mc: str) -> Path:
    matches = list((GAME / "versions").rglob(f"*fabric*{mc}*.json"))
    if not matches: raise RuntimeError("Fabric metadata not found after PortableMC dry install")
    return sorted(matches, key=lambda p: len(str(p)))[0]


def patch_version_json(path: Path, backend: str) -> None:
    data = json.loads(path.read_text(encoding="utf-8")); args = data.setdefault("arguments",{}).setdefault("game",[])
    out=[]; i=0
    while i < len(args):
        if isinstance(args[i],str) and args[i] in ("--graphicsBackend","--quickPlaySingleplayer"):
            i += 2; continue
        out.append(args[i]); i += 1
    out += ["--graphicsBackend",backend,"--quickPlaySingleplayer","benchworld"]
    data["arguments"]["game"] = out; path.write_text(json.dumps(data,indent=2),encoding="utf-8")


def write_options(cfg: dict[str, Any]) -> None:
    v=cfg["video"]
    opts={"fullscreen":"false","enableVsync":str(v["vsync"]).lower(),"maxFps":v["max_fps"],"renderDistance":v["render_distance"],
          "simulationDistance":v["simulation_distance"],"guiScale":2,"pauseOnLostFocus":"false","graphicsMode":v["graphics_mode"],
          "clouds":str(v["clouds"]).lower(),"entityDistanceScaling":v["entity_distance_scaling"],"mipmapLevels":v["mipmap_levels"],"narrator":0,"bobView":"false"}
    (GAME/"options.txt").write_text("\n".join(f"{k}:{val}" for k,val in opts.items())+"\n",encoding="utf-8")


def process_tree_rss_mb(pid: int) -> float:
    try:
        root = psutil.Process(pid)
        procs = [root, *root.children(recursive=True)]
        total = 0
        for p in procs:
            try: total += p.memory_info().rss
            except (psutil.NoSuchProcess, psutil.AccessDenied): pass
        return total / (1024 * 1024)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return 0.0


def kill_process_tree(proc: subprocess.Popen | None) -> None:
    if proc is None: return
    try:
        if os.name == "nt":
            subprocess.run(["taskkill","/PID",str(proc.pid),"/T","/F"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        else:
            try:
                os.killpg(os.getpgid(proc.pid),signal.SIGTERM); time.sleep(1); os.killpg(os.getpgid(proc.pid),signal.SIGKILL)
            except ProcessLookupError: pass
    except Exception:
        try: proc.kill()
        except Exception: pass


def launch_one(config_id: str, backend: str, rep: int, cfg: dict[str, Any], run_dir: Path,
               manifest: dict[str, Any], objectbench: Path, java: Path) -> dict[str, Any]:
    tag=f"{config_id}__{backend}__r{rep}"; log(f"\n=== {tag} ===")
    selected=next(c for c in cfg["configs"] if c["id"]==config_id)
    files=install_selected_mods(manifest,cfg["base_mods"],selected,objectbench); write_options(cfg)
    patch_version_json(find_fabric_json(cfg["minecraft_version"]),backend)
    save=GAME/"saves"/"benchworld"; safe_rmtree(save); save.parent.mkdir(parents=True,exist_ok=True); shutil.copytree(WORLD_TEMPLATE,save)
    result=GAME/"objectbench-result.json"; result.unlink(missing_ok=True)
    log_path=run_dir/"logs"/f"{tag}.log"; log_path.parent.mkdir(parents=True,exist_ok=True)
    env=java_env(java); b=cfg["benchmark"]
    env.update({"BENCH_RUN":tag,"BENCH_INITIAL_MS":str(int(b["initial_seconds"]*1000)),"BENCH_WARM_MS":str(int(b["warmup_seconds"]*1000)),"BENCH_MEASURE_MS":str(int(b["measure_seconds"]*1000))})
    wh=cfg["window"]; command=pmc_base()+["start","-u","BenchUser","--resolution",f"{wh['width']}x{wh['height']}",f"fabric:{cfg['minecraft_version']}"]
    out=log_path.open("w",encoding="utf-8",errors="replace"); flags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name=="nt" else 0
    proc=subprocess.Popen(command,env=env,stdout=out,stderr=subprocess.STDOUT,text=True,creationflags=flags,start_new_session=(os.name!="nt"))
    valid=False; reason="backend_not_proven"; deadline=time.time()+int(b["backend_proof_timeout_seconds"]); peak_rss_mb=0.0
    try:
        while time.time()<deadline:
            peak_rss_mb=max(peak_rss_mb,process_tree_rss_mb(proc.pid))
            txt=log_path.read_text(errors="ignore") if log_path.exists() else ""
            if backend=="vulkan":
                if "Failed to create backend Vulkan" in txt or "Using graphics backend OpenGL" in txt: reason="vulkan_failed_or_fell_back_to_opengl"; break
                if "Using graphics backend Vulkan" in txt: valid=True; break
            else:
                if "Using graphics backend Vulkan" in txt: reason="opengl_run_used_vulkan"; break
                if "Using graphics backend OpenGL" in txt: valid=True; break
            if proc.poll() is not None: reason=f"minecraft_exited_{proc.returncode}"; break
            time.sleep(.5)
        if valid:
            deadline=time.time()+int(b["result_timeout_seconds"])
            while time.time()<deadline and not result.exists():
                peak_rss_mb=max(peak_rss_mb,process_tree_rss_mb(proc.pid))
                if proc.poll() is not None: break
                time.sleep(.5)
        if valid and result.exists():
            peak_rss_mb=max(peak_rss_mb,process_tree_rss_mb(proc.pid))
            data=json.loads(result.read_text(encoding="utf-8")); data.update({"config":config_id,"label":selected["label"],"backend":backend,"rep":rep,"backend_proven":True,"mods":files,
                "process_metrics":{"peak_rss_mb":round(peak_rss_mb,3)}})
            raw=run_dir/"runs"/f"{tag}.json"; raw.parent.mkdir(parents=True,exist_ok=True); raw.write_text(json.dumps(data,indent=2),encoding="utf-8"); return data
        txt=log_path.read_text(errors="ignore") if log_path.exists() else ""
        return {"config":config_id,"label":selected["label"],"backend":backend,"rep":rep,"status":"invalid","reason":reason,"mods":files,"process_metrics":{"peak_rss_mb":round(peak_rss_mb,3)},"log_tail":txt[-4000:]}
    finally:
        kill_process_tree(proc); out.close(); time.sleep(float(b["cooldown_seconds"]))
