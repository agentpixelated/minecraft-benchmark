#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("root"); ap.add_argument("--out",default="exhaustive-results"); args=ap.parse_args()
    root=Path(args.root); paths=sorted(root.rglob("latest-summary.json"))
    if not paths: raise SystemExit("no shard summaries found")
    summaries=[json.loads(p.read_text(encoding="utf-8")) for p in paths]
    merged={"schema":2,"kind":"exhaustive-powerset-screening","minecraft":summaries[0].get("minecraft"),
            "method":summaries[0].get("method"),"shards":len(summaries),"hardware_samples":[s.get("hardware") for s in summaries],
            "matrix":{"mode":"powerset","total_configs":max((s.get("matrix",{}).get("total_configs",0) for s in summaries),default=0),
                      "optional_mods":summaries[0].get("matrix",{}).get("optional_mods",[])},
            "aggregate":{"configs":{},"invalid_runs":[]},
            "suite_results":{"definitions":summaries[0].get("suite_results",{}).get("definitions",{}),"configs":{}},
            "raw_runs":[]}
    for s in summaries:
        merged["aggregate"]["configs"].update(s.get("aggregate",{}).get("configs",{}))
        merged["aggregate"]["invalid_runs"].extend(s.get("aggregate",{}).get("invalid_runs",[]))
        merged["suite_results"]["configs"].update(s.get("suite_results",{}).get("configs",{}))
        merged["raw_runs"].extend(s.get("raw_runs",[]))
    out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    (out/"summary.json").write_text(json.dumps(merged,indent=2),encoding="utf-8")

    rows=[]
    for cid,c in merged["suite_results"]["configs"].items():
        for sid,r in c.get("suites",{}).items():
            if r.get("status")!="measured": continue
            rows.append({"config":cid,"label":c.get("label",cid),"mods":" + ".join(c.get("mods",[])),"suite":sid,
                         "unit":r.get("unit"),"higher_is_better":r.get("higher_is_better"),"opengl":r.get("opengl"),"vulkan":r.get("vulkan"),"delta_pct":r.get("delta_pct")})
    with (out/"ranking.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["config","label","mods","suite","unit","higher_is_better","opengl","vulkan","delta_pct"]); w.writeheader(); w.writerows(rows)

    lines=["# Exhaustive MCBench powerset screening","",f"- Shards merged: **{len(summaries)}**",f"- Configs: **{len(merged['aggregate']['configs'])} / {merged['matrix']['total_configs']}**",f"- Raw runs: **{len(merged['raw_runs'])}**",f"- Invalid runs: **{len(merged['aggregate']['invalid_runs'])}**","",
           "> Screening only: GitHub-hosted Ubuntu uses software graphics. Use this run to find interactions/candidates, then repeat finalists on physical hardware.",""]
    defs=merged["suite_results"]["definitions"]
    for sid,sdef in defs.items():
        measured=[r for r in rows if r["suite"]==sid and r["opengl"] is not None and r["vulkan"] is not None]
        lines += [f"## {sdef.get('label',sid)}",""]
        if not measured:
            lines += [f"Status: **{sdef.get('kind','unmeasured')}**. {sdef.get('note','')}",""]; continue
        hib=bool(measured[0]["higher_is_better"])
        scored=sorted(measured,key=lambda r:max(r["opengl"],r["vulkan"]) if hib else min(r["opengl"],r["vulkan"]),reverse=hib)[:15]
        lines += ["| # | Stack | OpenGL | Vulkan | Vulkan vs OpenGL |","|---:|---|---:|---:|---:|"]
        for i,r in enumerate(scored,1):
            lines.append(f"| {i} | {r['label']} | {r['opengl']:.2f} | {r['vulkan']:.2f} | {r['delta_pct']:+.2f}% |")
        lines.append("")
    (out/"REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({"shards":len(summaries),"configs":len(merged['aggregate']['configs']),"runs":len(merged['raw_runs']),"invalid":len(merged['aggregate']['invalid_runs']),"out":str(out)},indent=2))
    return 0


if __name__=="__main__": raise SystemExit(main())
