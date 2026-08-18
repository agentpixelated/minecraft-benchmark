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


def shard_configs(configs: list[dict[str, Any]], index: int, count: int) -> list[dict[str, Any]]:
    if count <= 0:
        raise ValueError("shard count must be positive")
    if index < 0 or index >= count:
        raise ValueError(f"shard index must be in [0,{count - 1}]")
    return [c for i, c in enumerate(configs) if i % count == index]
