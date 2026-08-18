from __future__ import annotations

import csv
import datetime as dt
import platform
import shutil
import statistics
from pathlib import Path
from typing import Any

import psutil

from .common import RESULTS, SCENES
from .prepare import java_version


def hardware_info(java: Path) -> dict[str, Any]:
    vm=psutil.virtual_memory()
    return {"timestamp":dt.datetime.now().astimezone().isoformat(),"platform":platform.platform(),"system":platform.system(),
            "release":platform.release(),"machine":platform.machine(),"processor":platform.processor(),"logical_cpus":psutil.cpu_count(logical=True),
            "physical_cpus":psutil.cpu_count(logical=False),"ram_gib":round(vm.total/1024**3,2),"java":str(java),"java_version":java_version(java)}


def aggregate(rows: list[dict[str, Any]], cfg: dict[str, Any]) -> dict[str, Any]:
    good=[r for r in rows if "overall" in r and r.get("backend_proven")]
    result={"configs":{},"invalid_runs":[r for r in rows if r not in good]}
    for c in cfg["configs"]:
        cid=c["id"]; entry={"label":c["label"],"backends":{},"comparison":{}}
        for backend in ["opengl","vulkan"]:
            rs=[r for r in good if r["config"]==cid and r["backend"]==backend]; be={"valid_runs":len(rs),"scenes":{}}
            for scene in SCENES:
                vals=[r["overall"] if scene=="overall" else r["scenes"][scene] for r in rs]
                if vals:
                    be["scenes"][scene]={"mean_fps":statistics.fmean(x["mean_fps"] for x in vals),"median_fps":statistics.fmean(x["median_fps"] for x in vals),
                        "one_percent_low_fps":statistics.fmean(x["one_percent_low_fps"] for x in vals),"zero_point_one_percent_low_fps":statistics.fmean(x["zero_point_one_percent_low_fps"] for x in vals),
                        "p99_frame_ms":statistics.fmean(x["p99_frame_ms"] for x in vals),"fps_range":[min(x["mean_fps"] for x in vals),max(x["mean_fps"] for x in vals)]}
            entry["backends"][backend]=be
        for scene in SCENES:
            try:
                o=entry["backends"]["opengl"]["scenes"][scene]; v=entry["backends"]["vulkan"]["scenes"][scene]
                entry["comparison"][scene]={"opengl_fps":o["mean_fps"],"vulkan_fps":v["mean_fps"],"vulkan_vs_opengl_pct":(v["mean_fps"]/o["mean_fps"]-1)*100,
                    "opengl_1pct_low":o["one_percent_low_fps"],"vulkan_1pct_low":v["one_percent_low_fps"],"opengl_p99_ms":o["p99_frame_ms"],"vulkan_p99_ms":v["p99_frame_ms"]}
            except KeyError: pass
        result["configs"][cid]=entry
    return result


def write_report(run_dir: Path, summary: dict[str, Any], cfg: dict[str, Any]) -> None:
    csv_path=run_dir/"summary.csv"
    with csv_path.open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["config","label","scene","opengl_fps","vulkan_fps","vulkan_vs_opengl_pct","opengl_1pct_low","vulkan_1pct_low","opengl_p99_ms","vulkan_p99_ms"])
        for cid,e in summary["aggregate"]["configs"].items():
            for scene,c in e["comparison"].items(): w.writerow([cid,e["label"],scene,c["opengl_fps"],c["vulkan_fps"],c["vulkan_vs_opengl_pct"],c["opengl_1pct_low"],c["vulkan_1pct_low"],c["opengl_p99_ms"],c["vulkan_p99_ms"]])
    lines=["# Sodium OpenGL vs Vulkan benchmark","",f"- Minecraft: **{cfg['minecraft_version']}**",f"- Repetitions/backend: **{cfg['benchmark']['repeats_per_backend']}**",f"- Resolution: **{cfg['window']['width']}×{cfg['window']['height']}**",f"- Render distance: **{cfg['video']['render_distance']}**","","## Overall comparison","","| Stack | OpenGL FPS | Vulkan FPS | Vulkan vs OpenGL | OpenGL 1% low | Vulkan 1% low |","|---|---:|---:|---:|---:|---:|"]
    rows=[]
    for _,e in summary["aggregate"]["configs"].items():
        c=e["comparison"].get("overall")
        if c: rows.append((max(c["opengl_fps"],c["vulkan_fps"]),e["label"],c))
    for _,label,c in sorted(rows,reverse=True): lines.append(f"| {label} | {c['opengl_fps']:.2f} | {c['vulkan_fps']:.2f} | {c['vulkan_vs_opengl_pct']:+.2f}% | {c['opengl_1pct_low']:.2f} | {c['vulkan_1pct_low']:.2f} |")
    lines += ["","## Method","","- Same machine and same resolved mod JARs for both backends.","- Controlled three-scene ObjectBench world.","- Programmatic camera/player path.","- Pregenerated benchmark chunks.","- World reset and Minecraft process-tree cleanup between runs.","- Backend accepted only when Sodium explicitly logs it.","","See `summary.json` for per-scene metrics and diagnostics."]
    (run_dir/"REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8"); RESULTS.mkdir(exist_ok=True)
    shutil.copy2(run_dir/"REPORT.md",RESULTS/"latest-report.md"); shutil.copy2(run_dir/"summary.json",RESULTS/"latest-summary.json"); shutil.copy2(csv_path,RESULTS/"latest-summary.csv")
