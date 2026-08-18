# Minecraft Sodium OpenGL / Vulkan / Render Scale / Super Resolution Benchmark

A repeatable Minecraft Fabric benchmark for comparing **Sodium + optimization-mod stacks** on OpenGL versus Minecraft's native Vulkan backend, plus a dedicated **Render Scale + Super Resolution** benchmark family.

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

The exhaustive CI workflow shards the work and merges its result summaries. GitHub-hosted VM results are screening data because they use virtual/software graphics; close rankings should be rerun on the target physical GPU.

### 3. Render Scale + Super Resolution matrix

This family is deliberately separate from the 256 optimization-mod power set. The Minecraft 26.2 Super Resolution build supports its upscaling path on OpenGL and disables it on Minecraft's native Vulkan backend.

Run it with:

```text
run-windows.bat --super-resolution
```

```bash
./run-linux.sh --super-resolution
```

```bash
AI_AGENT_NAME="chatgpt" python3 run-agent.py --super-resolution --accept-eula
```

The benchmark uses five matched internal render scales:

- **100%**
- **75%**
- **66.7%**
- **58.8%**
- **50%**

At those scales it tests eight Super Resolution algorithm paths:

- FSR 1
- SGSR 1
- SGSR 2
- FSR 2 OpenGL
- FidelityFX FSR 2.3.3
- FidelityFX FSR 3.1.4
- XeSS
- DLSS

The family contains **47 profiles** in total:

- 1 native Sodium OpenGL 100% baseline
- 1 Super Resolution-mod-disabled 100% overhead control
- 5 **raw RenderScale** controls (one at every internal scale)
- 40 Super Resolution profiles = 5 scales × 8 algorithms

RenderScale and Super Resolution are **not installed together in the same profile**. Raw RenderScale is the control condition; each SR profile uses Super Resolution's own `upscale_ratio` at the matched internal scale. This avoids two mods trying to own the framebuffer at once.

The result therefore reports two different comparisons:

- `vs_native_pct` — profile versus native 100% rendering
- `vs_raw_scale_pct` — SR profile versus raw RenderScale at the **same internal resolution**

Example at 50%:

```text
Native 100%
   ↓
Raw RenderScale 50%  ←→  FSR1 50%
                     ←→  SGSR1 50%
                     ←→  SGSR2 50%
                     ←→  FSR2 50%
                     ...
```

This separates the FPS gain caused merely by rendering fewer pixels from the extra cost/benefit of the upscaling algorithm itself.

Raw RenderScale profiles write `config/renderscale.json5` with the upstream experimental FSR switch disabled. Super Resolution profiles write `config/super_resolution/config.toml`. The two config files are reset between launches.

Hardware-specific algorithms may report **invalid / unsupported** instead of silently falling back. Enabled Super Resolution profiles require algorithm-initialization proof from the log; raw RenderScale profiles require the RenderScale mod plus the expected scale configuration to be proven.

Useful smoke subset:

```bash
./run-linux.sh --quick --super-resolution \
  --configs sr_native,renderscale_rs75,sr_fsr1_rs75,renderscale_rs50,sr_fsr1_performance \
  --accept-eula
```

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
| Render Scale + Super Resolution | matched raw-scale and upscaler profiles | FPS, 1% low, P99, vs-native %, vs-raw-scale % |
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

## Selected stacks / diagnostics

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
- matched raw RenderScale + Super Resolution preparation/runtime smoke
- exhaustive 256-stack sharded screening
