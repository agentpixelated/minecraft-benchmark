# Minecraft Sodium OpenGL vs Vulkan Benchmark

A local, repeatable Minecraft Fabric benchmark for comparing the **same Sodium + mod configuration** on:

- Sodium **OpenGL**
- Sodium **native Vulkan**

The benchmark targets Minecraft **26.2** and runs on the user's real Windows or Linux hardware. It uses an isolated benchmark installation under `.mcbench/`; it does **not** modify the normal `.minecraft` installation.

## One-click run

### Windows

Clone/download the repository, then double-click:

```text
run-windows.bat
```

### Linux

After cloning the repository:

```bash
./run-linux.sh
```

`run-linux.sh` is committed as executable. The launchers bootstrap `uv`, Python, PortableMC, and Java 25 when required. On the first run they ask you to accept the Minecraft EULA before creating the local benchmark world.

## What is benchmarked

Every selected mod stack is run on both backends. The default matrix contains 14 stacks:

- Sodium only
- + ImmediatelyFast
- + EntityCulling
- + MoreCulling
- + Lithium
- + FerriteCore
- + C2ME
- ImmediatelyFast + MoreCulling
- ImmediatelyFast + Lithium
- MoreCulling + Lithium
- ImmediatelyFast + MoreCulling + Lithium
- EntityCulling + MoreCulling + Lithium
- Full stack without C2ME
- Full stack

The exact compatible Modrinth versions and their required dependency closure are resolved once per benchmark session and written to `resolved-mods.json`, so OpenGL and Vulkan use the exact same JAR set inside each comparison.

> C2ME is included for completeness, but steady-state FPS is not the correct primary metric for C2ME. Chunk generation/loading should be benchmarked separately.

## Benchmark scenes

ObjectBench uses three deterministic scenes:

1. **Geometry + transparency** — leaves, glass, fences, bars, walls, stairs, trapdoors.
2. **Occlusion + entities** — opaque occluders, hidden no-AI entities, and block entities.
3. **Mixed block entities** — visible transparent/non-cubic geometry, barrels, and no-AI entities.

The benchmark client mod controls player position and camera directly. There is no mouse/keyboard automation. Benchmark chunks are generated before FPS measurement, time/weather/random ticks are frozen, and the world is reset before every run.

## Standard methodology

Default mode uses **2 repetitions per backend**. With the default 14-stack matrix this is 56 Minecraft launches. For each mod stack the backend order is balanced (ABBA or BAAB depending on stack index) to reduce time/order drift.

Each run has:

- initial stabilization period
- per-scene warmup
- per-scene measurement window
- backend verification from Sodium's own log
- pristine world reset between runs
- isolated Minecraft process tree and hard cleanup between runs

Metrics:

- average FPS
- median FPS
- 1% low FPS
- 0.1% low FPS
- p99 frame time
- per-scene metrics
- Vulkan vs OpenGL percentage

A Vulkan run is accepted only if Sodium explicitly reports the Vulkan backend. A failed Vulkan initialization or OpenGL fallback is recorded as invalid rather than counted as a Vulkan result.

## Quick mode

For a faster smoke test:

Windows:

```text
run-windows.bat --quick
```

Linux:

```bash
./run-linux.sh --quick
```

Quick mode uses one repetition per backend and shorter sampling. Use standard mode for performance conclusions.

## Run only selected stacks

```bash
./run-linux.sh --configs sodium,sodium_immediatelyfast,sodium_if_lithium
```

On Windows the same arguments can be passed to `run-windows.bat`.

Backend-only diagnostics are also available:

```bash
./run-linux.sh --backend opengl --configs sodium
./run-linux.sh --backend vulkan --configs sodium
```

## Output

Each benchmark creates a timestamped directory:

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

## Configuration

Edit `benchmark-config.json` to change resolution, render distance, sample duration, repetitions, or the mod matrix. Both backends inherit the same settings for a given benchmark session.

## Validation

The repository includes permanent cross-platform CI checks. During development the complete user-facing launch path was also exercised in virtual machines:

- **Windows:** the PowerShell launcher successfully installed/prepared Minecraft 26.2, Fabric, Java, the complete mod matrix, ObjectBench, and the controlled benchmark world.
- **Linux:** the executable shell launcher successfully ran real Minecraft quick benchmarks for both Sodium OpenGL and Sodium Vulkan, including Sodium-only and the full mod stack. All four renderer runs produced benchmark JSON with backend verification and no invalid run.

These CI machines use virtual/software graphics, so their FPS values are only functional validation. Performance conclusions should come from running the benchmark on the target physical GPU.

## Requirements and notes

- Internet access is required on the first run.
- A Vulkan-capable driver is required for Sodium Vulkan.
- Close other games, renderers, recording software, and heavy background tasks before running.
- Do not compare results from different machines as if they were controlled A/B tests. The primary purpose is **OpenGL vs Vulkan and mod-stack comparisons on the same hardware**.
- The scripts use an offline benchmark username and only local singleplayer worlds.
