# Minecraft Sodium OpenGL / Vulkan / Super Resolution Benchmark

A repeatable Minecraft Fabric benchmark for comparing **Sodium + optimization-mod stacks** on OpenGL versus Minecraft's native Vulkan backend, plus a dedicated **Super Resolution** benchmark family.

Target: **Minecraft 26.2**. Supported execution paths:

1. **Windows** local / physical hardware
2. **Linux** local / physical hardware
3. **AI agent / headless** environments, including coding agents and CI VMs

All modes use the same isolated `.mcbench/` game installation; the normal `.minecraft` directory is not modified.

## Run

### Windows — one click

```text
run-windows.bat
```

### Linux

```bash
./run-linux.sh
```

### AI agent / headless

```bash
AI_AGENT_NAME="chatgpt" python3 run-agent.py --accept-eula
```

Agent mode is non-interactive and writes `agent-result.json` in addition to the normal benchmark report. On headless Debian-family Linux it can provision Xvfb + Mesa Vulkan automatically when root/passwordless sudo is available.

## Benchmark families

### 1. Authored OpenGL vs Vulkan matrix

The default authored matrix contains 16 representative stacks built from:

- ImmediatelyFast
- EntityCulling
- MoreCulling
- Lithium
- FerriteCore
- C2ME
- BadOptimizations
- Better Block Entities

Every selected stack uses the exact same resolved JAR set on OpenGL and Vulkan.

### 2. Exhaustive optimization-mod power set

The eight optional optimization mods can be expanded into their complete power set:

```bash
./run-linux.sh --quick --all-combinations --accept-eula
```

Eight binary choices produce **2^8 = 256 unique stacks**. With one quick repetition on OpenGL and Vulkan this is **512 Minecraft launches**.

The GitHub Actions exhaustive workflow shards this into 64 jobs with four stacks per shard and merges the resulting summaries into `benchmark-results/exhaustive-latest/`.

This exhaustive CI run is a **screening benchmark** because GitHub-hosted VMs use virtual/software graphics. Close rankings should be rerun on the target physical GPU with multiple repetitions.

### 3. Super Resolution benchmark

Super Resolution is deliberately **not** included in the 256-stack power set. The Minecraft 26.2 Super Resolution build disables its upscaling features when Minecraft itself uses the native Vulkan backend, so duplicating every SR configuration into the Vulkan half would be redundant and misleading.

Run the dedicated OpenGL-only matrix instead:

Windows:

```text
run-windows.bat --super-resolution
```

Linux:

```bash
./run-linux.sh --super-resolution
```

AI agent:

```bash
AI_AGENT_NAME="chatgpt" python3 run-agent.py --super-resolution --accept-eula
```

Quick smoke subset:

```bash
./run-linux.sh --quick --super-resolution \
  --configs sr_native,sr_mod_disabled,sr_fsr1_quality,sr_fsr1_balanced \
  --accept-eula
```

Current SR profiles include:

- Native Sodium OpenGL baseline — no Super Resolution mod
- Super Resolution installed but upscaling disabled — measures mod overhead
- FSR 1 — Quality 66.7%, Balanced 58.8%, Performance 50% internal render scale
- SGSR 1 — Quality 66.7%
- SGSR 2 — Quality 66.7%
- FSR 2 OpenGL — Quality 66.7%
- FidelityFX FSR 2.3.3 — Quality 66.7%
- FidelityFX FSR 3.1.4 — Quality 66.7%
- XeSS — Quality 58.8%
- DLSS — Quality 66.7%

Hardware-specific algorithms are allowed to report **invalid / unsupported** rather than silently falling back. Every enabled SR result also requires an algorithm-initialization proof from the Super Resolution log.

Each profile writes the upstream config at `config/super_resolution/config.toml` before launch. `upscale_ratio` is converted to an internal render scale as `1 / upscale_ratio`.

## ObjectBench v5 multi-suite methodology

One Minecraft launch traverses multiple deterministic workloads so specialized mods are not judged only by generic steady-state FPS.

| Suite | Workload | Primary measurement |
|---|---|---|
| Renderer / FPS | geometry + transparency; occlusion + entities | FPS / frametime |
| Particle | sustained particle stress | FPS / frametime |
| Block Entity | BBE-relevant block entities + entities | FPS / frametime |
| Chunk Generation | traversal into virgin chunks | streaming frametime proxy |
| Lighting | repeated lighting/block-state updates | FPS / frametime |
| Memory | whole Minecraft process tree | peak RSS MB |
| Network | integrated-server loopback update stress | FPS / frametime |
| Super Resolution | native vs upscaled OpenGL profiles | FPS, 1% low, P99, vs-native % |
| Save / Quit | reserved for graceful shutdown timing | planned — no synthetic number |

The graphical scenes are:

- `geometry_transparency`
- `occlusion_entities`
- `mixed_block_entities`
- `particle_stress`
- `lighting_updates`
- `network_updates`
- `chunk_generation`

The client benchmark mod controls player position and camera directly. There is no mouse/keyboard automation. The pristine world template is restored before every launch.

## Standard OpenGL vs Vulkan methodology

Default authored mode uses **2 repetitions per backend**. Backend order is balanced ABBA/BAAB by stack to reduce order drift.

Each run includes:

- initial stabilization
- per-scene warmup
- per-scene measurement
- backend verification from Sodium's own log
- pristine world reset
- process-tree RSS sampling
- isolated Minecraft process tree and cleanup

Metrics include:

- average FPS
- median FPS
- 1% low FPS
- 0.1% low FPS
- p99 frame time
- per-scene / per-suite metrics
- peak process-tree RSS
- Vulkan vs OpenGL percentage

A Vulkan result is accepted only when Sodium explicitly reports Vulkan. Failed initialization or OpenGL fallback is recorded as **invalid**.

## Quick mode

```text
run-windows.bat --quick
```

```bash
./run-linux.sh --quick
```

```bash
python3 run-agent.py --quick --configs sodium,sodium_full --accept-eula
```

Quick mode uses one repetition and shorter measurements. It is intended for screening and functional validation, not final performance conclusions.

## Selected stacks / backend diagnostics

```bash
./run-linux.sh --configs sodium,sodium_badoptimizations,sodium_bbe,sodium_if_lithium
./run-linux.sh --backend opengl --configs sodium
./run-linux.sh --backend vulkan --configs sodium
```

The same benchmark arguments can be passed through `run-windows.bat` or `run-agent.py`.

## Output

Each run creates:

```text
results/<timestamp>/
├── REPORT.md
├── summary.json
├── summary.csv
├── effective-config.json
├── hardware.json
├── resolved-mods.json
├── runs/
└── logs/
```

Convenience copies:

```text
results/latest-report.md
results/latest-summary.json
results/latest-summary.csv
```

AI-agent mode additionally writes `agent-result.json`.

The result viewer under `site/` accepts `summary.json` and `agent-result.json` locally in the browser; uploaded benchmark contents are not sent to a backend.

## Mod resolution

Exact compatible Modrinth versions and required dependency closures are resolved per benchmark session. Both OpenGL and Vulkan sides of a normal comparison use identical mod JARs.

Public resolution works without authentication. Optional authenticated requests use `MODRINTH_TOKEN` only for `api.modrinth.com`; the token is not sent to download/CDN hosts or written to reports.

## Validation

CI contains separate validation paths for:

- Windows environment preparation
- Linux real OpenGL + Vulkan rendering
- AI-agent/headless execution
- ObjectBench v5 multi-suite schema
- dedicated Super Resolution preparation/runtime smoke
- exhaustive 256-stack sharded screening

CI/agent VMs may use software graphics. Their absolute FPS is functional/screening data; final conclusions should come from the target physical GPU.

## Requirements and notes

- Internet access is required on the first run.
- A Vulkan-capable driver is required for native Vulkan benchmarking.
- Super Resolution algorithms have different GPU/driver/extension requirements; unsupported profiles remain invalid rather than being silently substituted.
- Close games, overlays, recording software, and other heavy background tasks before physical-hardware measurements.
- Do not compare absolute FPS from unrelated machines as a controlled A/B test.
- The scripts use an offline benchmark username and local singleplayer worlds only.
