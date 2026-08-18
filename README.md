# Minecraft Sodium OpenGL vs Vulkan Benchmark

A repeatable Minecraft Fabric benchmark for comparing the **same Sodium + mod configuration** on:

- Sodium **OpenGL**
- Sodium **native Vulkan**

The benchmark targets Minecraft **26.2** and supports three execution paths:

1. **Windows** local/physical hardware
2. **Linux** local/physical hardware
3. **AI agent / headless** environments, including coding agents and CI VMs

All modes use the same benchmark core, ObjectBench world, mod resolver, graphics settings, backend proof, metrics, and report format. The isolated game installation lives under `.mcbench/`; the normal `.minecraft` installation is not modified.

## Run

### Windows — one click

Clone/download the repository, then double-click:

```text
run-windows.bat
```

### Linux — one command

```bash
./run-linux.sh
```

`run-linux.sh` is committed executable.

### AI agent / headless

```bash
AI_AGENT_NAME="chatgpt" python3 run-agent.py --accept-eula
```

Quick functional benchmark:

```bash
AI_AGENT_NAME="chatgpt" python3 run-agent.py --quick --configs sodium,sodium_full --accept-eula
```

Agent mode is non-interactive and writes `agent-result.json` in addition to the normal benchmark report. On headless Debian-family Linux it can provision Xvfb + Mesa Vulkan automatically when root/passwordless sudo is available. See [`AGENTS.md`](AGENTS.md) for the machine contract.

The Windows/Linux launchers bootstrap `uv`, Python, PortableMC, and Java 25 when required. Agent mode delegates to those same launchers rather than implementing a separate benchmark path.

## Default mod matrix

Every selected stack is tested on both OpenGL and Vulkan. The current default matrix contains **16 stacks**:

- Sodium only
- + ImmediatelyFast
- + EntityCulling
- + MoreCulling
- + Lithium
- + FerriteCore
- + BadOptimizations
- + Better Block Entities
- + C2ME
- ImmediatelyFast + MoreCulling
- ImmediatelyFast + Lithium
- MoreCulling + Lithium
- ImmediatelyFast + MoreCulling + Lithium
- EntityCulling + MoreCulling + Lithium
- Full stack without C2ME
- Full stack

Exact compatible Modrinth versions and required dependency closures are resolved once per benchmark session and written to `resolved-mods.json`, so the OpenGL and Vulkan sides use identical JAR sets.

> C2ME is included for completeness, but steady-state FPS is not the correct primary metric for C2ME. Chunk generation/loading should be benchmarked separately.

## ObjectBench scenes

ObjectBench currently uses three deterministic steady-state scenes:

1. **Geometry + transparency** — leaves, glass, fences, bars, walls, stairs, trapdoors.
2. **Occlusion + entities** — opaque occluders, hidden no-AI entities, and block entities.
3. **Mixed block entities** — visible transparent/non-cubic geometry, no-AI entities, plus a dense BBE-relevant set of chests, shulker boxes, decorated pots, signs, and bells.

The client benchmark mod controls player position and camera directly. There is no mouse/keyboard automation. Benchmark chunks are generated before FPS measurement, time/weather/random ticks are frozen, and the pristine world template is restored before every run.

## Standard methodology

Default mode uses **2 repetitions per backend**. With the current 16-stack matrix this is **64 Minecraft launches**. Backend order is balanced ABBA/BAAB by stack to reduce order drift.

Each run has:

- initial stabilization
- per-scene warmup
- per-scene measurement
- backend verification from Sodium's own log
- pristine world reset
- isolated Minecraft process tree and hard cleanup

Metrics include:

- average FPS
- median FPS
- 1% low FPS
- 0.1% low FPS
- p99 frame time
- per-scene metrics
- Vulkan vs OpenGL percentage

A Vulkan result is accepted only when Sodium explicitly reports the Vulkan backend. Failed Vulkan initialization or OpenGL fallback is recorded as **invalid**, never silently counted as Vulkan.

## Quick mode

Windows:

```text
run-windows.bat --quick
```

Linux:

```bash
./run-linux.sh --quick
```

AI agent:

```bash
python3 run-agent.py --quick --configs sodium,sodium_full --accept-eula
```

Quick mode uses one repetition per backend and shorter sampling. Use standard mode for performance conclusions.

## Selected stacks / backend diagnostics

```bash
./run-linux.sh --configs sodium,sodium_badoptimizations,sodium_bbe,sodium_if_lithium
./run-linux.sh --backend opengl --configs sodium
./run-linux.sh --backend vulkan --configs sodium
```

The same benchmark arguments can be passed through `run-windows.bat` or `run-agent.py`.

## Output

Each benchmark creates:

```text
results/20260818-210000/
├── REPORT.md
├── summary.json
├── summary.csv
├── effective-config.json
├── hardware.json
├── resolved-mods.json
├── runs/
└── logs/
```

Convenience copies are also written to `results/latest-report.md`, `results/latest-summary.json`, and `results/latest-summary.csv`.

AI-agent mode additionally writes:

```text
agent-result.json
```

A fully successful agent run must contain:

```json
{"status":"success","invalid_runs":0}
```

## Configuration

Edit `benchmark-config.json` to change resolution, render distance, sample duration, repetitions, or the mod matrix. Both graphics backends inherit the same settings for a session.

## Optional Modrinth token

Public Modrinth resolution works without authentication. To use authenticated Modrinth API requests, set `MODRINTH_TOKEN` in the environment before launching.

Windows PowerShell:

```powershell
$env:MODRINTH_TOKEN = "mrp_your_token_here"
.\run-windows.ps1
```

Linux:

```bash
export MODRINTH_TOKEN='mrp_your_token_here'
./run-linux.sh
```

AI agent:

```bash
export MODRINTH_TOKEN='mrp_your_token_here'
python3 run-agent.py --accept-eula
```

The token is attached only to requests sent to `api.modrinth.com`, is not sent to download/CDN hosts, and is not written to benchmark reports. Do not commit it to the repository.

## Validation

Permanent integration CI covers all three supported paths:

- **Windows:** full benchmark environment preparation through the Windows launcher, including resolution of the complete mod matrix.
- **Linux:** real quick OpenGL + Vulkan benchmark through the Linux launcher.
- **AI agent:** real headless OpenGL + Vulkan benchmark through `run-agent.py`, including Sodium baseline, BadOptimizations, Better Block Entities, and full stack, plus validation of `agent-result.json`.

The latest machine-readable three-platform CI status is written to `ci/integration-smoke.json`.

CI/agent VMs may use virtual/software graphics; their FPS is functional validation only. Performance conclusions should come from the target physical GPU.

## Requirements and notes

- Internet access is required on the first run.
- A Vulkan-capable driver is required for physical Vulkan benchmarking.
- Close other games, renderers, recording software, and heavy background tasks before benchmarking.
- Do not compare absolute FPS from different machines as a controlled A/B test.
- The primary comparison is **OpenGL vs Vulkan and mod-stack differences on the same hardware**.
- The scripts use an offline benchmark username and local singleplayer worlds only.
