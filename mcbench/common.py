from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "benchmark-config.json"
STATE = ROOT / ".mcbench"
GAME = STATE / "game"
CACHE = STATE / "cache"
MOD_CACHE = CACHE / "mods"
BUILD_CACHE = CACHE / "objectbench"
WORLD_TEMPLATE = CACHE / "world-template"
RESULTS = ROOT / "results"
USER_AGENT = "agentpixelated/minecraft-benchmark/1.1"
SCENES = ["overall", "geometry_transparency", "occlusion_entities", "mixed_block_entities"]


def log(msg: str) -> None:
    print(msg, flush=True)


def request_headers(url: str) -> dict[str, str]:
    headers = {"User-Agent": USER_AGENT}
    token = os.environ.get("MODRINTH_TOKEN", "").strip()
    host = (urllib.parse.urlparse(url).hostname or "").lower()
    # Never leak credentials to download/CDN or unrelated hosts. Authentication is
    # attached only to Modrinth's API host and the token itself is never logged.
    if token and host == "api.modrinth.com":
        headers["Authorization"] = token
    return headers


def request_json(url: str) -> Any:
    req = urllib.request.Request(url, headers=request_headers(url))
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.load(r)


def download(url: str, dst: Path) -> Path:
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_suffix(dst.suffix + ".part")
    req = urllib.request.Request(url, headers=request_headers(url))
    with urllib.request.urlopen(req, timeout=90) as r, tmp.open("wb") as f:
        shutil.copyfileobj(r, f)
    tmp.replace(dst)
    return dst


def run(cmd: list[str], *, env: dict[str, str] | None = None, cwd: Path | None = None,
        check: bool = True, capture: bool = False, timeout: int | None = None) -> subprocess.CompletedProcess:
    log("$ " + " ".join(str(x) for x in cmd))
    return subprocess.run([str(x) for x in cmd], cwd=str(cwd) if cwd else None, env=env,
                          check=check, text=True, capture_output=capture, timeout=timeout)


def portablemc_cmd() -> list[str]:
    exe = shutil.which("portablemc")
    return [exe] if exe else [sys.executable, "-m", "portablemc"]


def pmc_base() -> list[str]:
    return portablemc_cmd() + ["--main-dir", str(GAME), "--work-dir", str(GAME), "--timeout", "45"]


def load_config() -> dict[str, Any]:
    cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    required = {"minecraft_version", "base_mods", "window", "video", "benchmark", "configs"}
    missing = required - set(cfg)
    if missing:
        raise RuntimeError(f"benchmark-config.json missing keys: {sorted(missing)}")
    ids = [c["id"] for c in cfg["configs"]]
    if len(ids) != len(set(ids)):
        raise RuntimeError("benchmark-config.json contains duplicate config ids")
    return cfg


def safe_rmtree(path: Path) -> None:
    if not path.exists():
        return
    for _ in range(5):
        try:
            shutil.rmtree(path)
            return
        except PermissionError:
            time.sleep(1)
    shutil.rmtree(path)
