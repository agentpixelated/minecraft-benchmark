from __future__ import annotations

from itertools import combinations
from typing import Any


def _slug_token(slug: str) -> str:
    aliases = {
        "immediatelyfast": "if",
        "entityculling": "ec",
        "moreculling": "mc",
        "lithium": "li",
        "ferrite-core": "fc",
        "c2me-fabric": "c2me",
        "badoptimizations": "bo",
        "better-block-entities": "bbe",
    }
    return aliases.get(slug, slug.replace("-", "_"))


def generate_powerset_configs(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    mods = list(cfg.get("optional_mods") or [])
    if not mods:
        # Backward-compatible fallback: infer all optional mods from authored configs.
        seen: list[str] = []
        for c in cfg.get("configs", []):
            for slug in c.get("mods", []):
                if slug not in seen:
                    seen.append(slug)
        mods = seen

    label_map = dict(cfg.get("mod_labels") or {})
    out: list[dict[str, Any]] = []
    for n in range(len(mods) + 1):
        for combo in combinations(mods, n):
            if not combo:
                cid = "sodium"
                label = "Sodium only"
            else:
                token = "_".join(_slug_token(x) for x in combo)
                cid = f"sodium__{token}"
                label = "Sodium + " + " + ".join(label_map.get(x, x) for x in combo)
            out.append({"id": cid, "label": label, "mods": list(combo), "generated": True})
    return out


def _scale_id(scale: float) -> str:
    pct = scale * 100.0
    rounded = round(pct)
    if abs(pct - rounded) < 0.05:
        return str(int(rounded))
    return (f"{pct:.1f}").replace(".", "p")


def _scale_label(scale: float) -> str:
    pct = scale * 100.0
    rounded = round(pct)
    if abs(pct - rounded) < 0.05:
        return f"{int(rounded)}%"
    return f"{pct:.1f}%"


def generate_super_resolution_configs(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    """Generate an OpenGL-only Render Scale x Super Resolution matrix.

    Super Resolution's Minecraft 26.2 release disables its upscaling path on the
    native Vulkan backend, so this deliberately stays outside the OpenGL/Vulkan
    optimization-mod power set. The native baseline contains no SR mod. A second
    baseline installs the SR mod but keeps it disabled. Every algorithm template
    is then crossed with every configured internal render scale.
    """
    spec = dict(cfg.get("super_resolution_benchmark") or {})
    mod = spec.get("mod", "superresolution")
    out: list[dict[str, Any]] = [
        {
            "id": "sr_native",
            "label": "Native OpenGL 100% (Sodium only)",
            "mods": [],
            "generated": True,
            "benchmark_family": "super_resolution",
            "super_resolution": {
                "installed": False,
                "enabled": False,
                "profile": "native",
                "render_scale": 1.0,
                "upscale_ratio": 1.0,
            },
        },
        {
            "id": "sr_mod_disabled",
            "label": "SR mod installed, disabled (100%)",
            "mods": [mod],
            "generated": True,
            "benchmark_family": "super_resolution",
            "super_resolution": {
                "installed": True,
                "enabled": False,
                "profile": "mod_disabled",
                "algorithm": "fsr1",
                "render_scale": 1.0,
                "upscale_ratio": 1.0,
                "sharpness": float(spec.get("sharpness", 0.55)),
                "hardware_optional": False,
            },
        },
    ]

    sharpness = float(spec.get("sharpness", 0.55))
    scales = [float(x) for x in spec.get("render_scales", [1.0, 2 / 3, 0.5])]
    algorithms = list(spec.get("algorithms") or [])

    # Backward compatibility with the original authored profile list.
    if not algorithms:
        for profile in spec.get("profiles", []):
            p = dict(profile)
            if p.get("id") == "sr_mod_disabled":
                continue
            ratio = float(p.get("upscale_ratio", 1.0))
            sr = {
                "installed": True,
                "enabled": bool(p.get("enabled", True)),
                "profile": p["id"],
                "algorithm": p.get("algorithm", "none"),
                "upscale_ratio": ratio,
                "render_scale": 1.0 / ratio if ratio else None,
                "sharpness": sharpness,
                "fsr_version": p.get("fsr_version"),
                "hardware_optional": bool(p.get("hardware_optional", False)),
            }
            out.append({
                "id": p["id"], "label": p.get("label", p["id"]), "mods": [mod],
                "generated": True, "benchmark_family": "super_resolution", "super_resolution": sr,
            })
        return out

    for algo_spec in algorithms:
        a = dict(algo_spec)
        key = str(a["id"])
        algo = str(a.get("algorithm", key))
        for scale in scales:
            if scale <= 0 or scale > 1:
                raise ValueError(f"render scale must be in (0,1], got {scale}")
            ratio = 1.0 / scale
            sid = _scale_id(scale)
            profile_id = f"sr_{key}_rs{sid}"
            sr = {
                "installed": True,
                "enabled": True,
                "profile": profile_id,
                "algorithm": algo,
                "upscale_ratio": ratio,
                "render_scale": scale,
                "render_scale_percent": round(scale * 100.0, 3),
                "sharpness": sharpness,
                "fsr_version": a.get("fsr_version"),
                "hardware_optional": bool(a.get("hardware_optional", False)),
            }
            out.append({
                "id": profile_id,
                "label": f"{a.get('label', key)} @ {_scale_label(scale)} render scale",
                "mods": [mod],
                "generated": True,
                "benchmark_family": "super_resolution",
                "super_resolution": sr,
            })
    return out


def shard_configs(configs: list[dict[str, Any]], index: int, count: int) -> list[dict[str, Any]]:
    if count <= 0:
        raise ValueError("shard count must be positive")
    if index < 0 or index >= count:
        raise ValueError(f"shard index must be in [0,{count - 1}]")
    return [c for i, c in enumerate(configs) if i % count == index]
