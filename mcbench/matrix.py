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


def generate_super_resolution_configs(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    """Generate an OpenGL-only upscaling matrix.

    Super Resolution's Minecraft 26.2 release disables its upscaling path on the
    native Vulkan backend, so this deliberately stays outside the OpenGL/Vulkan
    optimization-mod power set. The native baseline contains no SR mod; the
    remaining profiles install the same SR build and vary only its config.toml.
    """
    spec = dict(cfg.get("super_resolution_benchmark") or {})
    mod = spec.get("mod", "superresolution")
    out: list[dict[str, Any]] = [
        {
            "id": "sr_native",
            "label": "Native OpenGL (Sodium only)",
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
        }
    ]
    sharpness = float(spec.get("sharpness", 0.55))
    for profile in spec.get("profiles", []):
        p = dict(profile)
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
            "id": p["id"],
            "label": p.get("label", p["id"]),
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
