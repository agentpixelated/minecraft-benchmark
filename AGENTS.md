# AI Agent Benchmark Instructions

This repository has three supported execution paths:

1. Windows human/local: `run-windows.bat`
2. Linux human/local: `./run-linux.sh`
3. AI agent/headless: `python run-agent.py`

## Rules for AI agents

- Do not change `benchmark-config.json`, ObjectBench source, graphics settings, or mod JARs during a reported benchmark session.
- Use the same machine/VM for the OpenGL and Vulkan sides of a comparison.
- Never report a Vulkan result unless the run has `backend_proven: true`.
- Treat any `status: invalid` row as invalid, not as zero FPS and not as an OpenGL fallback.
- Do not compare absolute FPS from virtual/software GPUs with physical GPUs as if they were equivalent.
- C2ME, ScalableLux, Krypton, Dynamic FPS, and similar non-steady-state optimizations need workload-specific benchmarks; do not rank them solely by ObjectBench average FPS.

## Recommended commands

Functional smoke test:

```bash
AI_AGENT_NAME="your-agent-name" python run-agent.py --quick --configs sodium,sodium_full --accept-eula
```

Full benchmark:

```bash
AI_AGENT_NAME="your-agent-name" python run-agent.py --accept-eula
```

One backend only:

```bash
python run-agent.py --backend opengl --configs sodium --accept-eula
python run-agent.py --backend vulkan --configs sodium --accept-eula
```

Offline/source self-test:

```bash
python run-agent.py --self-test
```

## Headless Linux

If there is no `DISPLAY`, `run-agent.py` uses Xvfb. On Debian-family systems it will attempt to install:

- `xvfb`
- `mesa-vulkan-drivers`
- `libvulkan1`

This only happens when the process has root or non-interactive sudo. Disable package installation with `--no-auto-system-deps`.

## EULA

Agent mode is intentionally non-interactive. It will not accept the Minecraft EULA on its own. The user must explicitly authorize acceptance by passing `--accept-eula` (or setting `MC_EULA_ACCEPTED=1`) after reviewing the EULA.

## Machine-readable output

`run-agent.py` always writes `agent-result.json` unless `--json-out` is supplied. Important fields:

- `status`
- `agent`
- `platform`
- `headless`
- `valid_runs`
- `invalid_runs`
- `invalid[]`
- `summary`
- `report`
- `aggregate`

A successful benchmark must have:

```json
{"status":"success","invalid_runs":0}
```

The detailed benchmark remains in the normal timestamped `results/<timestamp>/` directory.
