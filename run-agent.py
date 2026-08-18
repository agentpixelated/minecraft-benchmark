#!/usr/bin/env python3
"""Machine-readable benchmark entrypoint for AI coding/automation agents."""
from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_RESULT = ROOT / "agent-result.json"


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def agent_name() -> str:
    return os.environ.get("AI_AGENT_NAME") or os.environ.get("AGENT_NAME") or "unknown-agent"


def base_payload() -> dict:
    return {"schema": 2, "mode": "ai-agent", "agent": agent_name(), "platform": platform.platform(),
            "python": sys.version.split()[0], "headless": (os.name != "nt" and not bool(os.environ.get("DISPLAY")))}


def run_stream(command: list[str], env: dict[str, str] | None = None) -> int:
    print("[agent] exec:", " ".join(command), flush=True)
    proc = subprocess.Popen(command, cwd=ROOT, env=env)
    try: return proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        try: proc.wait(timeout=5)
        except subprocess.TimeoutExpired: proc.kill()
        return 130


def can_sudo_noninteractive() -> bool:
    if os.geteuid() == 0: return True
    sudo = shutil.which("sudo")
    if not sudo: return False
    return subprocess.run([sudo,"-n","true"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode == 0


def ensure_headless_linux_deps(auto_install: bool) -> tuple[bool, str | None]:
    if os.name == "nt" or os.environ.get("DISPLAY"): return True, None
    missing = [x for x in ["xvfb-run"] if not shutil.which(x)]
    if not missing and Path("/usr/share/vulkan/icd.d").exists(): return True, None
    if not auto_install: return False, "headless Linux requires Xvfb and a Vulkan ICD; install xvfb mesa-vulkan-drivers libvulkan1"
    apt = shutil.which("apt-get")
    if not apt or not can_sudo_noninteractive(): return False, "cannot auto-install Xvfb/Vulkan system packages"
    prefix = [] if os.geteuid() == 0 else [shutil.which("sudo"),"-n"]
    if subprocess.run([*prefix,apt,"update","-qq"]).returncode != 0: return False, "apt-get update failed"
    if subprocess.run([*prefix,apt,"install","-y","-qq","xvfb","mesa-vulkan-drivers","libvulkan1"]).returncode != 0:
        return False, "failed to install xvfb/mesa-vulkan-drivers/libvulkan1"
    return (bool(shutil.which("xvfb-run")), None if shutil.which("xvfb-run") else "xvfb-run unavailable after install")


def latest_summary_after(start: float) -> Path | None:
    candidates=[]; results=ROOT/"results"
    if results.exists():
        for p in results.glob("*/summary.json"):
            try:
                if p.stat().st_mtime >= start-2: candidates.append(p)
            except OSError: pass
    return max(candidates,key=lambda p:p.stat().st_mtime) if candidates else None


def summarize_result(summary_path: Path) -> dict:
    summary=json.loads(summary_path.read_text(encoding="utf-8")); raw=summary.get("raw_runs",[])
    valid=[r for r in raw if r.get("backend_proven") is True and r.get("status")!="invalid"]
    invalid=[r for r in raw if r.get("status")=="invalid" or r.get("backend_proven") is not True]
    return {"summary":str(summary_path.relative_to(ROOT)),"report":str((summary_path.parent/"REPORT.md").relative_to(ROOT)),
            "valid_runs":len(valid),"invalid_runs":len(invalid),
            "invalid":[{"config":r.get("config"),"backend":r.get("backend"),"rep":r.get("rep"),"reason":r.get("reason")} for r in invalid],
            "minecraft":summary.get("minecraft"),"matrix":summary.get("matrix"),"suite_results":summary.get("suite_results"),"aggregate":summary.get("aggregate")}


def self_test(out: Path) -> int:
    payload=base_payload()
    try:
        cfg=json.loads((ROOT/"benchmark-config.json").read_text(encoding="utf-8")); ids={c["id"] for c in cfg["configs"]}
        assert {"sodium","sodium_full"}.issubset(ids)
        assert len(cfg.get("suites",{}))==9 and len(cfg.get("optional_mods",[]))==8
        assert "super_resolution" in cfg["suites"] and len(cfg.get("super_resolution_benchmark",{}).get("profiles",[]))>=3
        assert (ROOT/"run-linux.sh").exists() and (ROOT/"run-windows.ps1").exists()
        compile((ROOT/"run-agent.py").read_text(encoding="utf-8"),"run-agent.py","exec")
        payload.update({"status":"self-test-ok","configs":len(cfg["configs"]),"suites":len(cfg["suites"]),"exhaustive_combinations":2**len(cfg["optional_mods"]),
                        "super_resolution_profiles":1+len(cfg["super_resolution_benchmark"]["profiles"])})
        write_json(out,payload); print("AGENT SELF-TEST OK"); return 0
    except Exception as exc:
        payload.update({"status":"self-test-failed","error":repr(exc)}); write_json(out,payload); print("AGENT SELF-TEST FAILED:",exc,file=sys.stderr); return 1


def main() -> int:
    ap=argparse.ArgumentParser(description="AI-agent/headless entrypoint for MCBench multi-suite OpenGL/Vulkan and Super Resolution benchmarks")
    ap.add_argument("--quick",action="store_true"); ap.add_argument("--configs"); ap.add_argument("--backend",choices=["both","opengl","vulkan"],default="both")
    ap.add_argument("--all-combinations",action="store_true"); ap.add_argument("--super-resolution",action="store_true")
    ap.add_argument("--shard-index",type=int,default=0); ap.add_argument("--shard-count",type=int,default=1)
    ap.add_argument("--accept-eula",action="store_true"); ap.add_argument("--rebuild",action="store_true"); ap.add_argument("--prepare-only",action="store_true"); ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--no-auto-system-deps",action="store_true"); ap.add_argument("--json-out",default=str(DEFAULT_RESULT)); args=ap.parse_args(); out=Path(args.json_out).resolve()
    if args.self_test: return self_test(out)
    payload=base_payload()
    if not args.accept_eula and os.environ.get("MC_EULA_ACCEPTED") not in {"1","true","TRUE","yes","YES"}:
        payload.update({"status":"requires-eula","error":"AI-agent mode is non-interactive; pass --accept-eula after the user has accepted the Minecraft EULA"}); write_json(out,payload); return 2
    ok,error=ensure_headless_linux_deps(not args.no_auto_system_deps)
    if not ok: payload.update({"status":"missing-system-dependency","error":error}); write_json(out,payload); return 2
    bench_args=[]
    if args.quick: bench_args.append("--quick")
    if args.configs: bench_args += ["--configs",args.configs]
    if args.backend!="both": bench_args += ["--backend",args.backend]
    if args.all_combinations: bench_args.append("--all-combinations")
    if args.super_resolution: bench_args.append("--super-resolution")
    if args.shard_count!=1 or args.shard_index!=0: bench_args += ["--shard-index",str(args.shard_index),"--shard-count",str(args.shard_count)]
    if args.accept_eula or os.environ.get("MC_EULA_ACCEPTED") in {"1","true","TRUE","yes","YES"}: bench_args.append("--accept-eula")
    if args.rebuild: bench_args.append("--rebuild")
    if args.prepare_only: bench_args.append("--prepare-only")
    if os.name=="nt": command=["powershell","-NoProfile","-ExecutionPolicy","Bypass","-File",str(ROOT/"run-windows.ps1"),*bench_args]
    else:
        command=[str(ROOT/"run-linux.sh"),*bench_args]
        if not os.environ.get("DISPLAY"): command=[shutil.which("xvfb-run") or "xvfb-run","-a",*command]
    env=os.environ.copy(); env.setdefault("AI_AGENT_NAME",agent_name()); started=time.time(); rc=run_stream(command,env)
    payload.update({"command":command,"returncode":rc,"started_unix":started,"finished_unix":time.time()})
    if args.prepare_only: payload["status"]="prepared" if rc==0 else "failed"; write_json(out,payload); return 0 if rc==0 else rc
    summary_path=latest_summary_after(started)
    if summary_path:
        payload.update(summarize_result(summary_path)); payload["status"]="success" if rc==0 and payload["invalid_runs"]==0 else "invalid-or-partial"
    else: payload.update({"status":"failed","error":"benchmark produced no new summary.json"})
    write_json(out,payload); print("[agent] machine result:",out); return 0 if payload["status"]=="success" else (rc if rc else 3)


if __name__=="__main__": raise SystemExit(main())
