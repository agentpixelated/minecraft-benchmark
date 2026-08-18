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
        cid=c["id"]; entry={"label":c["label"],"mods":list(c.get("mods",[])),"benchmark_family":c.get("benchmark_family"),
                             "super_resolution":c.get("super_resolution"),"render_scale":c.get("render_scale"),"backends":{},"comparison":{}}
        for backend in ["opengl","vulkan"]:
            rs=[r for r in good if r["config"]==cid and r["backend"]==backend]; be={"valid_runs":len(rs),"scenes":{}}
            for scene in SCENES:
                vals=[]
                for r in rs:
                    if scene=="overall" and "overall" in r: vals.append(r["overall"])
                    elif scene in r.get("scenes",{}): vals.append(r["scenes"][scene])
                vals=[x for x in vals if x.get("samples",0)>0]
                if vals:
                    be["scenes"][scene]={"mean_fps":statistics.fmean(x["mean_fps"] for x in vals),"median_fps":statistics.fmean(x["median_fps"] for x in vals),
                        "one_percent_low_fps":statistics.fmean(x["one_percent_low_fps"] for x in vals),"zero_point_one_percent_low_fps":statistics.fmean(x["zero_point_one_percent_low_fps"] for x in vals),
                        "p99_frame_ms":statistics.fmean(x["p99_frame_ms"] for x in vals),"fps_range":[min(x["mean_fps"] for x in vals),max(x["mean_fps"] for x in vals)]}
            rss=[r.get("process_metrics",{}).get("peak_rss_mb") for r in rs]
            rss=[float(x) for x in rss if isinstance(x,(int,float)) and x>0]
            if rss: be["process_metrics"]={"peak_rss_mb":statistics.fmean(rss),"rss_range_mb":[min(rss),max(rss)]}
            sr_runs=[r.get("super_resolution") for r in rs if r.get("super_resolution")]
            if sr_runs: be["super_resolution_proof"]=sr_runs
            scale_runs=[r.get("render_scale") for r in rs if r.get("render_scale")]
            if scale_runs: be["render_scale_proof"]=scale_runs
            entry["backends"][backend]=be
        for scene in SCENES:
            try:
                o=entry["backends"]["opengl"]["scenes"][scene]; v=entry["backends"]["vulkan"]["scenes"][scene]
                entry["comparison"][scene]={"opengl_fps":o["mean_fps"],"vulkan_fps":v["mean_fps"],"vulkan_vs_opengl_pct":(v["mean_fps"]/o["mean_fps"]-1)*100,
                    "opengl_1pct_low":o["one_percent_low_fps"],"vulkan_1pct_low":v["one_percent_low_fps"],"opengl_p99_ms":o["p99_frame_ms"],"vulkan_p99_ms":v["p99_frame_ms"]}
            except KeyError: pass
        try:
            o=entry["backends"]["opengl"]["process_metrics"]["peak_rss_mb"]
            v=entry["backends"]["vulkan"]["process_metrics"]["peak_rss_mb"]
            entry["comparison"]["memory"]={"opengl_peak_rss_mb":o,"vulkan_peak_rss_mb":v,"vulkan_vs_opengl_pct":(v/o-1)*100}
        except KeyError: pass
        result["configs"][cid]=entry
    return result


def _mean_scene_metric(entry: dict[str,Any], backend: str, scenes: list[str], key: str) -> float | None:
    vals=[]
    for scene in scenes:
        try: vals.append(float(entry["backends"][backend]["scenes"][scene][key]))
        except (KeyError,TypeError,ValueError): pass
    return statistics.fmean(vals) if vals else None


def build_suite_results(agg: dict[str,Any], cfg: dict[str,Any]) -> dict[str,Any]:
    definitions=cfg.get("suites",{})
    out={"definitions":definitions,"configs":{}}
    for cid,entry in agg.get("configs",{}).items():
        suites={}
        for sid,sdef in definitions.items():
            kind=sdef.get("kind")
            if kind=="planned":
                suites[sid]={"status":"planned","opengl":None,"vulkan":None,"delta_pct":None}
                continue
            if kind=="special_super_resolution":
                sr=entry.get("super_resolution")
                raw_scale=entry.get("render_scale")
                profile=sr or raw_scale
                if entry.get("benchmark_family")!="super_resolution" or not profile:
                    suites[sid]={"status":"not_applicable","opengl":None,"vulkan":None,"delta_pct":None}
                    continue
                scenes=list(sdef.get("scenes",[])); primary=sdef.get("primary_metric","mean_fps")
                o=_mean_scene_metric(entry,"opengl",scenes,primary)
                suites[sid]={"status":"measured" if o is not None else "missing","unit":"FPS","higher_is_better":True,
                    "primary_metric":primary,"opengl":o,"vulkan":None,"delta_pct":None,"scenes":scenes,
                    "profile":profile,"profile_kind":"super_resolution" if sr else "raw_render_scale",
                    "supporting":{
                        "opengl_1pct_low":_mean_scene_metric(entry,"opengl",scenes,"one_percent_low_fps"),
                        "opengl_p99_ms":_mean_scene_metric(entry,"opengl",scenes,"p99_frame_ms")}}
                continue
            if kind=="process_rss":
                def rss(backend: str):
                    try: return float(entry["backends"][backend]["process_metrics"]["peak_rss_mb"])
                    except (KeyError,TypeError,ValueError): return None
                o,v=rss("opengl"),rss("vulkan")
                suites[sid]={"status":"measured" if o is not None or v is not None else "missing","unit":"MB","higher_is_better":False,
                    "primary_metric":"peak_rss_mb","opengl":o,"vulkan":v,"delta_pct":((v/o-1)*100 if o and v is not None else None)}
                continue
            scenes=list(sdef.get("scenes",[])); primary=sdef.get("primary_metric","mean_fps")
            o=_mean_scene_metric(entry,"opengl",scenes,primary); v=_mean_scene_metric(entry,"vulkan",scenes,primary)
            suites[sid]={"status":"measured" if o is not None or v is not None else "missing","unit":"ms" if primary.endswith("_ms") else "FPS",
                "higher_is_better":not primary.endswith("_ms"),"primary_metric":primary,"opengl":o,"vulkan":v,
                "delta_pct":((v/o-1)*100 if o and v is not None else None),"scenes":scenes,
                "supporting":{
                    "opengl_1pct_low":_mean_scene_metric(entry,"opengl",scenes,"one_percent_low_fps"),
                    "vulkan_1pct_low":_mean_scene_metric(entry,"vulkan",scenes,"one_percent_low_fps"),
                    "opengl_p99_ms":_mean_scene_metric(entry,"opengl",scenes,"p99_frame_ms"),
                    "vulkan_p99_ms":_mean_scene_metric(entry,"vulkan",scenes,"p99_frame_ms")}}
        out["configs"][cid]={"label":entry.get("label",cid),"mods":entry.get("mods",[]),"suites":suites}

    # SR family uses two controls: native 100% and a raw RenderScale control at
    # the same internal scale. This separates resolution gain from upscaler cost.
    try: native=out["configs"]["sr_native"]["suites"]["super_resolution"]["opengl"]
    except (KeyError,TypeError): native=None
    raw_by_scale: dict[float, tuple[str,float]] = {}
    for cid,item in out["configs"].items():
        sr=item["suites"].get("super_resolution")
        if not sr or sr.get("status")!="measured" or sr.get("profile_kind")!="raw_render_scale": continue
        profile=sr.get("profile") or {}; scale=profile.get("render_scale"); value=sr.get("opengl")
        if isinstance(scale,(int,float)) and isinstance(value,(int,float)):
            raw_by_scale[round(float(scale),5)]=(cid,float(value))
    for cid,item in out["configs"].items():
        sr=item["suites"].get("super_resolution")
        if not sr or sr.get("status")!="measured" or sr.get("opengl") is None: continue
        value=float(sr["opengl"])
        if native: sr["vs_native_pct"]=(value/float(native)-1)*100
        profile=sr.get("profile") or {}; scale=profile.get("render_scale")
        if isinstance(scale,(int,float)):
            matched=raw_by_scale.get(round(float(scale),5))
            if matched:
                raw_cid,raw_value=matched
                sr["raw_scale_baseline_config"]=raw_cid
                sr["vs_raw_scale_pct"]=(value/raw_value-1)*100
    return out


def write_report(run_dir: Path, summary: dict[str, Any], cfg: dict[str, Any]) -> None:
    csv_path=run_dir/"summary.csv"
    with csv_path.open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["config","label","scene","opengl_fps","vulkan_fps","vulkan_vs_opengl_pct","opengl_1pct_low","vulkan_1pct_low","opengl_p99_ms","vulkan_p99_ms"])
        for cid,e in summary["aggregate"]["configs"].items():
            for scene,c in e["comparison"].items():
                if "opengl_fps" not in c: continue
                w.writerow([cid,e["label"],scene,c["opengl_fps"],c["vulkan_fps"],c["vulkan_vs_opengl_pct"],c["opengl_1pct_low"],c["vulkan_1pct_low"],c["opengl_p99_ms"],c["vulkan_p99_ms"]])

    if summary.get("matrix",{}).get("mode")=="super_resolution":
        lines=["# Sodium OpenGL Render Scale + Super Resolution benchmark","",f"- Minecraft: **{cfg['minecraft_version']}**",f"- Repetitions/profile: **{cfg['benchmark']['repeats_per_backend']}**",f"- Output resolution: **{cfg['window']['width']}×{cfg['window']['height']}**","",
               "## Render Scale / Super Resolution profiles","","| Profile | Type | Render scale | Mean FPS | vs native | vs raw scale | 1% low | P99 ms |","|---|---|---:|---:|---:|---:|---:|---:|"]
        sr_cfg=summary.get("suite_results",{}).get("configs",{})
        for cid,item in sr_cfg.items():
            sr=item.get("suites",{}).get("super_resolution",{}); profile=sr.get("profile") or {}
            if sr.get("status")!="measured":
                lines.append(f"| {item.get('label',cid)} | — | — | INVALID / unsupported | — | — | — | — |")
                continue
            scale=profile.get("render_scale"); scale_txt=f"{float(scale)*100:.1f}%" if isinstance(scale,(int,float)) else "—"
            one=sr.get("supporting",{}).get("opengl_1pct_low"); p99=sr.get("supporting",{}).get("opengl_p99_ms"); delta=sr.get("vs_native_pct"); raw_delta=sr.get("vs_raw_scale_pct")
            kind={"raw_render_scale":"Raw scale","super_resolution":"Super Resolution"}.get(sr.get("profile_kind"),"Native")
            delta_txt=f"{delta:+.2f}%" if delta is not None else "—"; raw_txt=f"{raw_delta:+.2f}%" if raw_delta is not None else "—"
            one_txt=f"{one:.2f}" if one is not None else "—"; p99_txt=f"{p99:.2f}" if p99 is not None else "—"
            lines.append(f"| {item.get('label',cid)} | {kind} | {scale_txt} | {sr.get('opengl',0):.2f} | {delta_txt} | {raw_txt} | {one_txt} | {p99_txt} |")
        lines += ["","## Method","","- OpenGL only for the Super Resolution branch: the Minecraft 26.2 Super Resolution build disables its features on Minecraft's native Vulkan backend.","- `sr_native` is Sodium OpenGL at 100% without either scaling mod.","- `renderscale_rs*` profiles are raw-resolution controls using RenderScale with its own experimental FSR disabled.","- `sr_*` profiles use Super Resolution only; RenderScale is not installed simultaneously.","- `vs_raw_scale_pct` compares an SR algorithm against raw scaling at the same internal render scale.","- Each enabled SR profile requires algorithm-initialization proof; each raw RenderScale profile requires the mod plus matching `renderscale.json5` configuration proof.","- Hardware-specific profiles may be marked invalid/unsupported rather than silently falling back.","","See `summary.json` for per-scene frametime metrics, profile metadata, and proof fields."]
    else:
        lines=["# Sodium OpenGL vs Vulkan multi-suite benchmark","",f"- Minecraft: **{cfg['minecraft_version']}**",f"- Repetitions/backend: **{cfg['benchmark']['repeats_per_backend']}**",f"- Resolution: **{cfg['window']['width']}×{cfg['window']['height']}**",f"- Render distance: **{cfg['video']['render_distance']}**","","## Overall frametime comparison","","| Stack | OpenGL FPS | Vulkan FPS | Vulkan vs OpenGL | OpenGL 1% low | Vulkan 1% low |","|---|---:|---:|---:|---:|---:|"]
        rows=[]
        for _,e in summary["aggregate"]["configs"].items():
            c=e["comparison"].get("overall")
            if c: rows.append((max(c["opengl_fps"],c["vulkan_fps"]),e["label"],c))
        for _,label,c in sorted(rows,reverse=True): lines.append(f"| {label} | {c['opengl_fps']:.2f} | {c['vulkan_fps']:.2f} | {c['vulkan_vs_opengl_pct']:+.2f}% | {c['opengl_1pct_low']:.2f} | {c['vulkan_1pct_low']:.2f} |")
        lines += ["","## Suites","","Renderer/FPS, Particle, Block Entity, Chunk Generation (streaming proxy), Lighting, Memory, Network (loopback update stress), Render Scale + Super Resolution (dedicated OpenGL mode), and a reserved Save/Quit schema slot are stored in `suite_results`.","","## Method","","- Same machine and same resolved mod JARs for both backends.","- Programmatic camera/player path and isolated game directory.","- World reset and Minecraft process-tree cleanup between runs.","- Backend accepted only when Sodium explicitly logs it.","- Peak process-tree RSS sampled by the Python harness.","- Save/Quit is intentionally not fabricated from forced cleanup; it remains marked `planned` until graceful timing is implemented.","","See `summary.json` for per-suite/per-scene metrics and diagnostics."]
    (run_dir/"REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8"); RESULTS.mkdir(exist_ok=True)
    shutil.copy2(run_dir/"REPORT.md",RESULTS/"latest-report.md"); shutil.copy2(run_dir/"summary.json",RESULTS/"latest-summary.json"); shutil.copy2(csv_path,RESULTS/"latest-summary.csv")
