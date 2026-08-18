from __future__ import annotations

import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

from .common import CACHE, WORLD_TEMPLATE, log, safe_rmtree
from .prepare import java_env, wait_for_text

MARKER = ".objectbench-v5-suites"


def enhance_suite_world(java: Path, cfg: dict[str, Any], rebuild: bool = False) -> None:
    """Add suite-specific stress zones without pre-generating the chunk-generation path.

    The base world builder remains responsible for renderer/entity/block-entity scenes.
    This pass adds command-driven particle, lighting, and update/packet stress zones.
    Command blocks are deliberately *not* forceloaded, so they only execute while the
    benchmark player is close enough for that suite and do not contaminate other scenes.
    """
    marker = WORLD_TEMPLATE / MARKER
    if marker.exists() and not rebuild:
        return
    if not WORLD_TEMPLATE.exists():
        raise RuntimeError("base benchmark world is missing")

    work = CACHE / "suite-worldgen"
    safe_rmtree(work)
    work.mkdir(parents=True)
    shutil.copytree(WORLD_TEMPLATE, work / "benchworld")

    server_jar = CACHE / f"minecraft-server-{cfg['minecraft_version']}.jar"
    if not server_jar.exists():
        raise RuntimeError("Minecraft server jar missing after base world generation")
    shutil.copy2(server_jar, work / "server.jar")
    (work / "eula.txt").write_text("eula=true\n", encoding="utf-8")
    (work / "server.properties").write_text(
        "level-name=benchworld\n"
        "level-seed=7608123456789\n"
        "level-type=minecraft:flat\n"
        "gamemode=creative\n"
        "difficulty=peaceful\n"
        "online-mode=false\n"
        "view-distance=12\n"
        "simulation-distance=8\n"
        "spawn-protection=0\n"
        "enable-command-block=true\n",
        encoding="utf-8",
    )

    server_log = work / "server.log"
    out = server_log.open("w", encoding="utf-8")
    p = subprocess.Popen(
        [str(java), "-Xms1G", "-Xmx2G", "-jar", "server.jar", "nogui"],
        cwd=work,
        stdin=subprocess.PIPE,
        stdout=out,
        stderr=subprocess.STDOUT,
        text=True,
        env=java_env(java),
    )
    if not wait_for_text(server_log, "Done (", 90):
        p.kill(); out.close()
        raise RuntimeError("suite world server did not start; see .mcbench/cache/suite-worldgen/server.log")

    def cmd(s: str, delay: float = .05) -> None:
        assert p.stdin is not None
        p.stdin.write(s + "\n"); p.stdin.flush(); time.sleep(delay)

    # Particle suite around x=480. Three emitters create mixed translucent particles.
    cmd("fill 432 3 -48 528 3 48 minecraft:smooth_stone")
    particle_commands = [
        (472, "particle minecraft:flame ~ ~8 ~ 18 8 18 0.03 420 force"),
        (480, "particle minecraft:smoke ~ ~8 ~ 18 8 18 0.02 420 force"),
        (488, "particle minecraft:poof ~ ~8 ~ 18 8 18 0.04 420 force"),
    ]
    for x, command in particle_commands:
        cmd(f'setblock {x} 4 0 minecraft:repeating_command_block{{auto:1b,Command:"{command}"}}')

    # Lighting suite around x=640. Alternating fills cause repeated light-engine updates.
    cmd("fill 592 3 -48 688 3 48 minecraft:smooth_stone")
    cmd("fill 620 4 4 660 10 6 minecraft:stone")
    light_on = "fill 622 5 8 658 9 16 minecraft:light[level=15] replace minecraft:air"
    light_off = "fill 622 5 8 658 9 16 minecraft:air replace minecraft:light[level=15]"
    cmd(f'setblock 636 4 0 minecraft:repeating_command_block{{auto:1b,Command:"{light_on}"}}')
    cmd(f'setblock 644 4 0 minecraft:repeating_command_block{{auto:1b,Command:"{light_off}"}}')

    # Network/update suite around x=800. Large state flips force integrated-server
    # block-update packets through the client connection each tick.
    cmd("fill 752 3 -48 848 3 48 minecraft:smooth_stone")
    net_a = "fill 784 4 6 816 8 14 minecraft:white_concrete replace minecraft:black_concrete"
    net_b = "fill 784 4 6 816 8 14 minecraft:black_concrete replace minecraft:white_concrete"
    cmd("fill 784 4 6 816 8 14 minecraft:black_concrete")
    cmd(f'setblock 796 4 0 minecraft:repeating_command_block{{auto:1b,Command:"{net_a}"}}')
    cmd(f'setblock 804 4 0 minecraft:repeating_command_block{{auto:1b,Command:"{net_b}"}}')

    # Do NOT touch x≈1984..2624. That virgin region is the chunk-generation suite.
    cmd("save-all flush", .5)
    time.sleep(2)
    cmd("stop")
    try:
        p.wait(timeout=30)
    except subprocess.TimeoutExpired:
        p.kill()
    out.close()

    safe_rmtree(WORLD_TEMPLATE)
    shutil.copytree(work / "benchworld", WORLD_TEMPLATE)
    (WORLD_TEMPLATE / MARKER).write_text(
        "ObjectBench v5 suites: particle, lighting, loopback update stress; chunk path intentionally virgin\n",
        encoding="utf-8",
    )
    log(f"[world] Added multi-suite stress zones to {WORLD_TEMPLATE}")
