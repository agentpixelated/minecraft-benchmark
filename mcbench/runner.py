from __future__ import annotations

import argparse
import datetime as dt
import json
from typing import Any

from .common import CACHE, RESULTS, ROOT, STATE, load_config, log
from .execute import launch_one
from .matrix import generate_powerset_configs, generate_super_resolution_configs, shard_configs
from .prepare import build_world, ensure_game_and_java, ensure_objectbench, resolve_and_download_mods
from .report import aggregate, build_suite_results, hardware_info, write_report
from .suite_world import enhance_suite_world


def select_configs(cfg: dict[str, Any], selection: str | None):
    if not selection: return cfg["configs"]
    wanted=[x.strip() for x in selection.split(",") if x.strip()]; by_id={c["id"]:c for c in cfg["configs"]}
    unknown=[x for x in wanted if x not in by_id]
    if unknown: raise RuntimeError(f"Unknown config ids: {unknown}. Available: {', '.join(by_id)}")
    return [by_id[x] for x in wanted]


def self_test(cfg: dict[str, Any]) -> None:
    src=(ROOT/"objectbench"/"ObjectBenchClient.java").read_text(encoding="utf-8")
    assert "OBJECTBENCH DONE" in src and "LevelRenderEvents.END_MAIN" in src
    assert "particle_stress" in src and "chunk_generation" in src
    assert {"sodium","sodium_full"}.issubset({c["id"] for c in cfg["configs"]})
    generated=generate_powerset_configs(cfg)
    assert len(generated)==2**len(cfg.get("optional_mods",[]))
    assert len({c["id"] for c in generated})==len(generated)
    sr=generate_super_resolution_configs(cfg)
    assert sr[0]["id"]=="sr_native" and any(c["id"]=="sr_fsr1_quality" for c in sr)
    assert all(c.get("benchmark_family")=="super_resolution" for c in sr)
    log(f"SELF-TEST OK ({len(generated)} exhaustive combinations; {len(sr)} SR profiles)")


def main() -> int:
    ap=argparse.ArgumentParser(description="Multi-suite benchmark: Sodium OpenGL vs native Vulkan plus dedicated Super Resolution profiles.")
    ap.add_argument("--quick",action="store_true"); ap.add_argument("--configs"); ap.add_argument("--backend",choices=["both","opengl","vulkan"],default="both")
    ap.add_argument("--all-combinations",action="store_true",help="Generate the full power set of optional_mods")
    ap.add_argument("--super-resolution",action="store_true",help="Run the dedicated OpenGL-only Super Resolution profile matrix")
    ap.add_argument("--shard-index",type=int,default=0); ap.add_argument("--shard-count",type=int,default=1)
    ap.add_argument("--accept-eula",action="store_true"); ap.add_argument("--rebuild",action="store_true"); ap.add_argument("--prepare-only",action="store_true"); ap.add_argument("--self-test",action="store_true")
    args=ap.parse_args(); cfg=load_config()
    if args.quick: cfg["benchmark"].update({"initial_seconds":3,"warmup_seconds":1,"measure_seconds":2,"repeats_per_backend":1,"cooldown_seconds":1,"result_timeout_seconds":120})
    if args.self_test: self_test(load_config()); return 0
    if args.super_resolution and args.all_combinations: raise RuntimeError("Use either --super-resolution or --all-combinations, not both")
    if args.super_resolution and args.backend=="vulkan": raise RuntimeError("Minecraft 26.2 Super Resolution is OpenGL-only; Vulkan disables SR features")

    if args.super_resolution:
        cfg["configs"]=generate_super_resolution_configs(cfg)
        if args.configs: cfg["configs"]=select_configs(cfg,args.configs)
        if args.shard_count != 1 or args.shard_index != 0: cfg["configs"]=shard_configs(cfg["configs"],args.shard_index,args.shard_count)
        matrix_meta={"mode":"super_resolution","total_configs":len(generate_super_resolution_configs(load_config())),"backend":"opengl",
                     "shard_index":args.shard_index,"shard_count":args.shard_count,"shard_configs":len(cfg["configs"]),
                     "note":"Dedicated SR profiles are kept outside the OpenGL/Vulkan optimization-mod powerset because the MC 26.2 SR build disables upscaling on Vulkan."}
    elif args.all_combinations:
        if args.configs: raise RuntimeError("Use either --configs or --all-combinations, not both")
        all_generated=generate_powerset_configs(cfg)
        cfg["configs"]=shard_configs(all_generated,args.shard_index,args.shard_count)
        matrix_meta={"mode":"powerset","total_configs":len(all_generated),"optional_mods":cfg.get("optional_mods",[]),"shard_index":args.shard_index,"shard_count":args.shard_count,"shard_configs":len(cfg["configs"])}
    else:
        if args.shard_count != 1 or args.shard_index != 0: raise RuntimeError("--shard-* requires --all-combinations or --super-resolution")
        cfg["configs"]=select_configs(cfg,args.configs)
        matrix_meta={"mode":"authored","total_configs":len(cfg["configs"]),"shard_index":0,"shard_count":1,"shard_configs":len(cfg["configs"])}
    if not cfg["configs"]: raise RuntimeError("This shard contains no configs")

    STATE.mkdir(exist_ok=True); CACHE.mkdir(parents=True,exist_ok=True); RESULTS.mkdir(exist_ok=True)
    java=ensure_game_and_java(cfg); mods=resolve_and_download_mods(cfg,force=args.rebuild); objectbench=ensure_objectbench(java,cfg,rebuild=args.rebuild); build_world(java,cfg,args.accept_eula,rebuild=args.rebuild); enhance_suite_world(java,cfg,rebuild=args.rebuild)
    if args.prepare_only: log("PREPARE COMPLETE"); return 0
    run_dir=RESULTS/dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f"); (run_dir/"logs").mkdir(parents=True); (run_dir/"runs").mkdir(parents=True)
    (run_dir/"hardware.json").write_text(json.dumps(hardware_info(java),indent=2),encoding="utf-8"); (run_dir/"resolved-mods.json").write_text(json.dumps(mods,indent=2),encoding="utf-8"); (run_dir/"effective-config.json").write_text(json.dumps(cfg,indent=2),encoding="utf-8")
    backends=["opengl"] if args.super_resolution else (["opengl","vulkan"] if args.backend=="both" else [args.backend]); repeats=int(cfg["benchmark"]["repeats_per_backend"]); rows=[]
    for ci,c in enumerate(cfg["configs"]):
        if len(backends)==2 and repeats==2: order=[("opengl",1),("vulkan",1),("vulkan",2),("opengl",2)] if ci%2==0 else [("vulkan",1),("opengl",1),("opengl",2),("vulkan",2)]
        elif len(backends)==2 and repeats==1: order=[("opengl",1),("vulkan",1)] if ci%2==0 else [("vulkan",1),("opengl",1)]
        else: order=[(b,r) for r in range(1,repeats+1) for b in backends]
        for backend,rep in order:
            rows.append(launch_one(c["id"],backend,rep,cfg,run_dir,mods,objectbench,java)); (run_dir/"raw-progress.json").write_text(json.dumps(rows,indent=2),encoding="utf-8")
    agg=aggregate(rows,cfg)
    method="ObjectBench v5 multi-suite; controlled and stress scenes; programmatic camera; isolated game dir; process-tree cleanup"
    if args.super_resolution: method += "; dedicated OpenGL Super Resolution profile matrix with per-run upstream config and algorithm proof"
    else: method += "; balanced OpenGL/Vulkan backend order"
    summary={"schema":2,"minecraft":cfg["minecraft_version"],"method":method,"hardware":json.loads((run_dir/"hardware.json").read_text()),"matrix":matrix_meta,"suite_results":build_suite_results(agg,cfg),"aggregate":agg,"raw_runs":rows}
    (run_dir/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8"); write_report(run_dir,summary,cfg); log(f"\nDONE: {run_dir/'REPORT.md'}"); return 0
