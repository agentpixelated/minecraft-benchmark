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


def _sr_profile_id(key: str, scale: float) -> str:
    """Keep useful old IDs while adding a systematic scale matrix."""
    pct = scale * 100.0
    if key == "fsr1":
        if abs(pct - 66.6667) < 0.2: return "sr_fsr1_quality"
        if abs(pct - 58.8235) < 0.2: return "sr_fsr1_balanced"
        if abs(pct - 50.0) < 0.2: return "sr_fsr1_performance"
    if abs(pct - 66.6667) < 0.2 and key in {"sgsr1", "sgsr2", "fsr2", "fsr_v2", "fsr_v3", "dlss"}:
        return f"sr_{key}_quality"
    if abs(pct - 58.8235) < 0.2 and key == "xess":
        return "sr_xess_quality"
    return f"sr_{key}_rs{_scale_id(scale)}"


def generate_super_resolution_configs(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    """Generate raw RenderScale baselines plus an OpenGL-only SR cross-product.

    RenderScale and Super Resolution are never installed in the same profile.
    Raw RenderScale profiles provide the control condition for a given internal
    resolution; SR profiles then use Super Resolution's own upscale_ratio at the
    same scale. This keeps the comparison interpretable and avoids two mods both
    trying to own the game's render target.
    """
    spec = dict(cfg.get("super_resolution_benchmark") or {})
    sr_mod = spec.get("mod", "superresolution")
    rs_mod = spec.get("render_scale_mod", "renderscale")
    scales = [float(x) for x in spec.get("render_scales", [1.0, 2 / 3, 0.5])]
    sharpness = float(spec.get("sharpness", 0.55))

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
            "mods": [sr_mod],
            "generated": True,
            "benchmark_family": "super_resolution",
            "super_resolution": {
                "installed": True,
                "enabled": False,
                "profile": "mod_disabled",
                "algorithm": "fsr1",
                "render_scale": 1.0,
                "upscale_ratio": 1.0,
                "sharpness": sharpness,
                "hardware_optional": False,
            },
        },
    ]

    # Raw render-scale controls. RenderScale's internal FSR switch remains off;
    # these are pure resolution scaling baselines, not another SR implementation.
    for scale in scales:
        if scale <= 0 or scale > 1:
            raise ValueError(f"render scale must be in (0,1], got {scale}")
        cid = f"renderscale_rs{_scale_id(scale)}"
        out.append({
            "id": cid,
            "label": f"Raw RenderScale @ {_scale_label(scale)}",
            "mods": [rs_mod],
            "generated": True,
            "benchmark_family": "super_resolution",
            "render_scale": {
                "installed": True,
                "profile": cid,
                "render_scale": scale,
                "render_scale_percent": round(scale * 100.0, 3),
                "force_linear": False,
                "fsr": False,
            },
        })

    algorithms = list(spec.get("algorithms") or [])
    if not algorithms:
        for profile in spec.get("profiles", []):
            p = dict(profile)
            if p.get("id") == "sr_mod_disabled" or p.get("legacy_alias"):
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
                "id": p["id"], "label": p.get("label", p["id"]), "mods": [sr_mod],
                "generated": True, "benchmark_family": "super_resolution", "super_resolution": sr,
            })
        return out

    for algo_spec in algorithms:
        a = dict(algo_spec)
        key = str(a["id"])
        algo = str(a.get("algorithm", key))
        for scale in scales:
            ratio = 1.0 / scale
            profile_id = _sr_profile_id(key, scale)
            sr = {
                "installed": True,
                "enabled": True,
                "profile": profile_id,
                "algorithm": algo,
                "algorithm_id": key,
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
                "mods": [sr_mod],
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
