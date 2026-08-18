from __future__ import annotations

import argparse
import datetime as dt
import json
from typing import Any

from .common import CACHE, RESULTS, ROOT, STATE, load_config, log
from .execute import launch_one
from .prepare import build_world, ensure_game_and_java, ensure_objectbench, resolve_and_download_mods
from .report import aggregate, hardware_info, write_report


def select_configs(cfg: dict[str, Any], selection: str | None):
    if not selection: return cfg["configs"]
    wanted=[x.strip() for x in selection.split(",") if x.strip()]; by_id={c["id"]:c for c in cfg["configs"]}
    unknown=[x for x in wanted if x not in by_id]
    if unknown: raise RuntimeError(f"Unknown config ids: {unknown}. Available: {', '.join(by_id)}")
    return [by_id[x] for x in wanted]


def self_test(cfg: dict[str, Any]) -> None:
    src=(ROOT/"objectbench"/"ObjectBenchClient.java").read_text(encoding="utf-8")
    assert "OBJECTBENCH DONE" in src and "LevelRenderEvents.END_MAIN" in src
    assert {"sodium","sodium_full"}.issubset({c["id"] for c in cfg["configs"]})
    log("SELF-TEST OK")


def main() -> int:
    ap=argparse.ArgumentParser(description="Benchmark Sodium OpenGL vs native Vulkan with identical Fabric mod stacks.")
    ap.add_argument("--quick",action="store_true"); ap.add_argument("--configs"); ap.add_argument("--backend",choices=["both","opengl","vulkan"],default="both")
    ap.add_argument("--accept-eula",action="store_true"); ap.add_argument("--rebuild",action="store_true"); ap.add_argument("--prepare-only",action="store_true"); ap.add_argument("--self-test",action="store_true")
    args=ap.parse_args(); cfg=load_config()
    if args.quick: cfg["benchmark"].update({"initial_seconds":5,"warmup_seconds":2,"measure_seconds":4,"repeats_per_backend":1})
    cfg["configs"]=select_configs(cfg,args.configs)
    if args.self_test: self_test(cfg); return 0
    STATE.mkdir(exist_ok=True); CACHE.mkdir(parents=True,exist_ok=True); RESULTS.mkdir(exist_ok=True)
    java=ensure_game_and_java(cfg); mods=resolve_and_download_mods(cfg,force=args.rebuild); objectbench=ensure_objectbench(java,cfg,rebuild=args.rebuild); build_world(java,cfg,args.accept_eula,rebuild=args.rebuild)
    if args.prepare_only: log("PREPARE COMPLETE"); return 0
    run_dir=RESULTS/dt.datetime.now().strftime("%Y%m%d-%H%M%S"); (run_dir/"logs").mkdir(parents=True); (run_dir/"runs").mkdir(parents=True)
    (run_dir/"hardware.json").write_text(json.dumps(hardware_info(java),indent=2),encoding="utf-8"); (run_dir/"resolved-mods.json").write_text(json.dumps(mods,indent=2),encoding="utf-8"); (run_dir/"effective-config.json").write_text(json.dumps(cfg,indent=2),encoding="utf-8")
    backends=["opengl","vulkan"] if args.backend=="both" else [args.backend]; repeats=int(cfg["benchmark"]["repeats_per_backend"]); rows=[]
    for ci,c in enumerate(cfg["configs"]):
        if len(backends)==2 and repeats==2: order=[("opengl",1),("vulkan",1),("vulkan",2),("opengl",2)] if ci%2==0 else [("vulkan",1),("opengl",1),("opengl",2),("vulkan",2)]
        else: order=[(b,r) for r in range(1,repeats+1) for b in backends]
        for backend,rep in order:
            rows.append(launch_one(c["id"],backend,rep,cfg,run_dir,mods,objectbench,java)); (run_dir/"raw-progress.json").write_text(json.dumps(rows,indent=2),encoding="utf-8")
    summary={"minecraft":cfg["minecraft_version"],"method":"ObjectBench v3; controlled 3 scenes; programmatic camera; pregenerated chunks; isolated game dir; balanced backend order; process-tree cleanup","hardware":json.loads((run_dir/"hardware.json").read_text()),"aggregate":aggregate(rows,cfg),"raw_runs":rows}
    (run_dir/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8"); write_report(run_dir,summary,cfg); log(f"\nDONE: {run_dir/'REPORT.md'}"); return 0
