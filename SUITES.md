# MCBench multi-suite methodology

MCBench v5 separates optimization workloads instead of scoring every mod from one steady-state FPS number.

## Suites

| Suite | Current workload | Primary metric | Direction | Notes |
|---|---|---:|---|---|
| Renderer / FPS | geometry/transparency + occlusion/entities | FPS / frametime | higher FPS, lower p99 | Core Sodium/culling/render path. |
| Particle | command-driven mixed particle stress | FPS / frametime | higher FPS | Workload exists even without a dedicated particle optimization mod. |
| Block Entity | BBE-relevant chests, shulkers, pots, signs, bells | FPS / frametime | higher FPS | Designed to expose Better Block Entities effects. |
| Chunk Generation | rapid traversal through intentionally virgin chunks | streaming FPS / frametime proxy | higher FPS | Useful screening for C2ME interactions; not yet a direct chunks/sec measurement. |
| Lighting | repeated large light-block state changes | FPS / frametime | higher FPS | Exercises repeated lighting updates while the player is nearby. |
| Memory | sampled process-tree RSS during the run | peak RSS MB | lower | Useful for FerriteCore and stack interaction screening. |
| Network | integrated-server block-update packet stress | FPS / frametime | higher FPS | Loopback client/server update pressure; **not** WAN latency or throughput. |
| Save / Quit | reserved schema slot | save/quit ms | lower | `planned`; forced process cleanup is deliberately not reported as save/quit performance. |

## One launch, multiple workloads

One Minecraft launch walks all implemented graphical/stress workloads in sequence. This keeps the matrix practical and ensures a stack uses the same resolved JARs and process instance across suites.

Every raw run records:

- backend proof (`Using graphics backend OpenGL` / `Vulkan`)
- per-scene mean FPS, median FPS, 1% low, 0.1% low and p99 frametime
- process-tree peak RSS
- exact installed mod JARs
- config, backend and repetition

`summary.json` schema 2 adds `suite_results`, which maps those raw measurements into suite-specific primary values.

## Exhaustive power set

The optional mod set is currently:

1. ImmediatelyFast
2. EntityCulling
3. MoreCulling
4. Lithium
5. FerriteCore
6. C2ME
7. BadOptimizations
8. Better Block Entities

That produces `2^8 = 256` unique stacks including Sodium-only.

Generate/run all combinations locally:

```bash
./run-linux.sh --quick --all-combinations --accept-eula
```

or Windows:

```powershell
.\run-windows.ps1 --quick --all-combinations --accept-eula
```

AI-agent/headless:

```bash
AI_AGENT_NAME=chatgpt python3 run-agent.py --quick --all-combinations --accept-eula
```

For distributed execution:

```bash
./run-linux.sh --quick --all-combinations --shard-index 0 --shard-count 64 --accept-eula
```

The repository workflow `.github/workflows/exhaustive-powerset.yml` screens the 256-stack matrix on GitHub-hosted Ubuntu in 64 shards, comparing OpenGL and Vulkan once per stack, then merges all available results into:

- `benchmark-results/exhaustive-latest/summary.json`
- `benchmark-results/exhaustive-latest/ranking.csv`
- `benchmark-results/exhaustive-latest/REPORT.md`

## Interpretation

The exhaustive GitHub run is a **screening experiment**, not a physical-GPU verdict. GitHub-hosted Linux graphics are software-rendered. Use it to discover compatibility failures, large interactions and promising stacks. Re-run finalists with 2–5+ repetitions on physical Windows/Linux hardware before drawing real-GPU conclusions.
