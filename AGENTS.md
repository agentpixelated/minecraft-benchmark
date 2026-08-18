# AI Agent Benchmark Instructions

This repository has three supported execution paths:

1. Windows human/local: `run-windows.bat`
2. Linux human/local: `./run-linux.sh`
3. AI agent/headless: `python3 run-agent.py`

## Rules for AI agents

- Do not change `benchmark-config.json`, ObjectBench source, graphics settings, or mod JARs during a reported benchmark session.
- Use the same machine/VM for the OpenGL and Vulkan sides of a comparison.
- Never report a Vulkan result unless the run has `backend_proven: true`.
- Treat any `status: invalid` row as invalid, not as zero FPS and not as an OpenGL fallback.
- Do not compare absolute FPS from virtual/software GPUs with physical GPUs as if they were equivalent.
- C2ME, ScalableLux, Krypton, Dynamic FPS, FastQuit, NoisiumForked, VMP, and similar workload-specific optimizations need dedicated benchmarks; do not rank them solely by ObjectBench average FPS.
- `sodium_bbe` should be judged especially on the `mixed_block_entities` scene, which contains BBE-relevant block entities.

## Recommended commands

Functional smoke test of the agent contract plus the two newer optimization candidates:

```bash
AI_AGENT_NAME="your-agent-name" python3 run-agent.py --quick --configs sodium,sodium_badoptimizations,sodium_bbe,sodium_full --accept-eula
```

Full benchmark:

```bash
AI_AGENT_NAME="your-agent-name" python3 run-agent.py --accept-eula
```

One backend only:

```bash
python3 run-agent.py --backend opengl --configs sodium --accept-eula
python3 run-agent.py --backend vulkan --configs sodium --accept-eula
```

Offline/source self-test:

```bash
python3 run-agent.py --self-test
```

## Headless Linux

If there is no `DISPLAY`, `run-agent.py` uses Xvfb. On Debian-family systems it will attempt to install:

- `xvfb`
- `mesa-vulkan-drivers`
- `libvulkan1`

This only happens when the process has root or non-interactive sudo. Disable package installation with `--no-auto-system-deps`.

## EULA

Agent mode is intentionally non-interactive. It will not accept the Minecraft EULA on its own. The user must explicitly authorize acceptance by passing `--accept-eula` (or setting `MC_EULA_ACCEPTED=1`) after reviewing the EULA.

## Optional Modrinth token

If `MODRINTH_TOKEN` exists in the agent environment, authenticated requests to `api.modrinth.com` use it automatically. Do not print, return, or commit the token.

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

The detailed benchmark remains in the normal timestamped `results/<timestamp>/` directory. Permanent CI writes the latest three-platform status to `ci/integration-smoke.json`.
