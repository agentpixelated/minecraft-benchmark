# Exhaustive MCBench powerset screening

- Shards merged: **56**
- Configs: **224 / 256**
- Raw runs: **448**
- Invalid runs: **0**

> Screening only: GitHub-hosted Ubuntu uses software graphics. Use this run to find interactions/candidates, then repeat finalists on physical hardware.

## Renderer / FPS

| # | Stack | OpenGL | Vulkan | Vulkan vs OpenGL |
|---:|---|---:|---:|---:|
| 1 | Sodium + EntityCulling + MoreCulling + FerriteCore + BadOptimizations | 38.17 | 34.46 | -9.71% |
| 2 | Sodium + FerriteCore | 36.65 | 33.04 | -9.87% |
| 3 | Sodium + EntityCulling + FerriteCore + Better Block Entities | 35.83 | 35.29 | -1.50% |
| 4 | Sodium + FerriteCore + Better Block Entities | 33.56 | 29.46 | -12.21% |
| 5 | Sodium + ImmediatelyFast + EntityCulling + Lithium + FerriteCore | 30.76 | 25.63 | -16.66% |
| 6 | Sodium + ImmediatelyFast + EntityCulling + MoreCulling + Better Block Entities | 30.75 | 26.43 | -14.05% |
| 7 | Sodium + EntityCulling + Lithium + Better Block Entities | 30.62 | 28.96 | -5.43% |
| 8 | Sodium + Lithium + C2ME + BadOptimizations + Better Block Entities | 30.16 | 27.71 | -8.11% |
| 9 | Sodium + EntityCulling + Lithium | 29.76 | 25.86 | -13.08% |
| 10 | Sodium + EntityCulling + MoreCulling + Lithium + BadOptimizations | 28.94 | 27.64 | -4.49% |
| 11 | Sodium + ImmediatelyFast + FerriteCore + C2ME + BadOptimizations + Better Block Entities | 28.77 | 25.11 | -12.72% |
| 12 | Sodium + EntityCulling + Lithium + FerriteCore | 28.58 | 25.97 | -9.13% |
| 13 | Sodium + ImmediatelyFast + MoreCulling + FerriteCore + BadOptimizations + Better Block Entities | 26.20 | 27.15 | +3.61% |
| 14 | Sodium + EntityCulling | 26.52 | 26.88 | +1.36% |
| 15 | Sodium + ImmediatelyFast + Lithium + FerriteCore + C2ME + Better Block Entities | 23.94 | 20.83 | -12.96% |

## Particle

| # | Stack | OpenGL | Vulkan | Vulkan vs OpenGL |
|---:|---|---:|---:|---:|
| 1 | Sodium + EntityCulling + MoreCulling + FerriteCore + BadOptimizations | 67.47 | 50.21 | -25.59% |
| 2 | Sodium + FerriteCore + Better Block Entities | 64.26 | 51.50 | -19.86% |
| 3 | Sodium + EntityCulling + FerriteCore + Better Block Entities | 60.41 | 55.37 | -8.35% |
| 4 | Sodium + FerriteCore | 60.33 | 54.80 | -9.17% |
| 5 | Sodium + EntityCulling + MoreCulling + Lithium + BadOptimizations | 59.77 | 46.11 | -22.87% |
| 6 | Sodium + ImmediatelyFast + MoreCulling + FerriteCore + BadOptimizations + Better Block Entities | 58.25 | 46.66 | -19.90% |
| 7 | Sodium + EntityCulling + Lithium + Better Block Entities | 56.09 | 48.51 | -13.51% |
| 8 | Sodium + EntityCulling + Lithium | 55.16 | 40.60 | -26.40% |
| 9 | Sodium + Lithium + C2ME + BadOptimizations + Better Block Entities | 54.89 | 46.66 | -15.00% |
| 10 | Sodium + EntityCulling | 54.48 | 46.36 | -14.90% |
| 11 | Sodium + ImmediatelyFast + EntityCulling + Lithium + FerriteCore | 54.37 | 47.78 | -12.13% |
| 12 | Sodium + ImmediatelyFast + EntityCulling + MoreCulling + Better Block Entities | 53.66 | 51.34 | -4.32% |
| 13 | Sodium + ImmediatelyFast + FerriteCore + C2ME + BadOptimizations + Better Block Entities | 52.23 | 52.85 | +1.18% |
| 14 | Sodium + EntityCulling + Lithium + FerriteCore | 50.40 | 44.24 | -12.23% |
| 15 | Sodium + ImmediatelyFast + EntityCulling + MoreCulling + FerriteCore + C2ME + BadOptimizations | 49.30 | 46.85 | -4.97% |

## Block Entity

| # | Stack | OpenGL | Vulkan | Vulkan vs OpenGL |
|---:|---|---:|---:|---:|
| 1 | Sodium + EntityCulling + MoreCulling + FerriteCore + BadOptimizations | 57.09 | 50.22 | -12.04% |
| 2 | Sodium + EntityCulling + FerriteCore + Better Block Entities | 54.57 | 47.21 | -13.50% |
| 3 | Sodium + FerriteCore | 52.99 | 49.12 | -7.31% |
| 4 | Sodium + FerriteCore + Better Block Entities | 50.09 | 44.41 | -11.34% |
| 5 | Sodium + ImmediatelyFast + EntityCulling + Lithium + FerriteCore | 48.24 | 38.63 | -19.93% |
| 6 | Sodium + ImmediatelyFast + EntityCulling + MoreCulling + Better Block Entities | 47.34 | 45.71 | -3.44% |
| 7 | Sodium + ImmediatelyFast + MoreCulling + FerriteCore + BadOptimizations + Better Block Entities | 47.06 | 38.20 | -18.84% |
| 8 | Sodium + EntityCulling + MoreCulling + Lithium + BadOptimizations | 46.96 | 43.22 | -7.97% |
| 9 | Sodium + EntityCulling + Lithium | 46.75 | 41.67 | -10.86% |
| 10 | Sodium + EntityCulling + Lithium + FerriteCore | 46.65 | 38.94 | -16.52% |
| 11 | Sodium + EntityCulling + Lithium + Better Block Entities | 45.05 | 43.70 | -3.00% |
| 12 | Sodium + EntityCulling | 44.39 | 38.05 | -14.27% |
| 13 | Sodium + ImmediatelyFast + FerriteCore + C2ME + BadOptimizations + Better Block Entities | 42.99 | 31.53 | -26.66% |
| 14 | Sodium + Lithium + C2ME + BadOptimizations + Better Block Entities | 42.65 | 34.02 | -20.23% |
| 15 | Sodium + ImmediatelyFast + EntityCulling + MoreCulling + FerriteCore + C2ME + BadOptimizations | 36.20 | 33.97 | -6.16% |

## Chunk Generation

| # | Stack | OpenGL | Vulkan | Vulkan vs OpenGL |
|---:|---|---:|---:|---:|
| 1 | Sodium + FerriteCore | 44.85 | 36.37 | -18.90% |
| 2 | Sodium + EntityCulling + FerriteCore + Better Block Entities | 37.92 | 42.67 | +12.51% |
| 3 | Sodium + FerriteCore + Better Block Entities | 39.33 | 36.62 | -6.89% |
| 4 | Sodium + ImmediatelyFast + EntityCulling + MoreCulling + Better Block Entities | 38.88 | 35.58 | -8.48% |
| 5 | Sodium + ImmediatelyFast + EntityCulling + MoreCulling + FerriteCore + C2ME + BadOptimizations | 38.76 | 36.65 | -5.45% |
| 6 | Sodium + EntityCulling + MoreCulling + Lithium + BadOptimizations | 36.17 | 38.41 | +6.21% |
| 7 | Sodium + ImmediatelyFast + EntityCulling + Lithium + FerriteCore | 37.66 | 32.03 | -14.94% |
| 8 | Sodium + ImmediatelyFast + FerriteCore + C2ME + BadOptimizations + Better Block Entities | 37.58 | 35.33 | -5.98% |
| 9 | Sodium + EntityCulling + MoreCulling + FerriteCore + BadOptimizations | 37.53 | 37.48 | -0.14% |
| 10 | Sodium + EntityCulling + Lithium + FerriteCore | 36.63 | 29.05 | -20.69% |
| 11 | Sodium + Lithium + C2ME + BadOptimizations + Better Block Entities | 34.34 | 36.48 | +6.23% |
| 12 | Sodium + EntityCulling + Lithium | 36.43 | 34.86 | -4.31% |
| 13 | Sodium + ImmediatelyFast + MoreCulling + FerriteCore + BadOptimizations + Better Block Entities | 34.44 | 30.46 | -11.54% |
| 14 | Sodium + C2ME + BadOptimizations | 34.30 | 26.99 | -21.29% |
| 15 | Sodium + EntityCulling + Lithium + Better Block Entities | 33.21 | 29.34 | -11.66% |

## Lighting

| # | Stack | OpenGL | Vulkan | Vulkan vs OpenGL |
|---:|---|---:|---:|---:|
| 1 | Sodium + EntityCulling + MoreCulling + FerriteCore + BadOptimizations | 62.31 | 56.72 | -8.97% |
| 2 | Sodium + FerriteCore + Better Block Entities | 61.12 | 47.36 | -22.52% |
| 3 | Sodium + EntityCulling + FerriteCore + Better Block Entities | 61.08 | 52.70 | -13.72% |
| 4 | Sodium + EntityCulling + Lithium + FerriteCore | 59.05 | 44.43 | -24.75% |
| 5 | Sodium + ImmediatelyFast + MoreCulling + FerriteCore + BadOptimizations + Better Block Entities | 58.88 | 49.53 | -15.89% |
| 6 | Sodium + EntityCulling + MoreCulling + Lithium + BadOptimizations | 58.31 | 49.72 | -14.74% |
| 7 | Sodium + FerriteCore | 57.85 | 56.43 | -2.47% |
| 8 | Sodium + ImmediatelyFast + EntityCulling + Lithium + FerriteCore | 55.18 | 40.64 | -26.35% |
| 9 | Sodium + Lithium + C2ME + BadOptimizations + Better Block Entities | 53.53 | 54.74 | +2.25% |
| 10 | Sodium + EntityCulling | 54.30 | 42.82 | -21.15% |
| 11 | Sodium + EntityCulling + Lithium | 54.25 | 46.32 | -14.61% |
| 12 | Sodium + EntityCulling + Lithium + Better Block Entities | 53.81 | 45.62 | -15.21% |
| 13 | Sodium + ImmediatelyFast + EntityCulling + MoreCulling + Better Block Entities | 52.90 | 45.29 | -14.38% |
| 14 | Sodium + ImmediatelyFast + FerriteCore + C2ME + BadOptimizations + Better Block Entities | 52.12 | 46.83 | -10.16% |
| 15 | Sodium + ImmediatelyFast + EntityCulling + MoreCulling + FerriteCore + C2ME + BadOptimizations | 50.94 | 44.10 | -13.44% |

## Memory

| # | Stack | OpenGL | Vulkan | Vulkan vs OpenGL |
|---:|---|---:|---:|---:|
| 1 | Sodium + EntityCulling + MoreCulling + Lithium + BadOptimizations + Better Block Entities | 1743.94 | 1870.86 | +7.28% |
| 2 | Sodium + EntityCulling + Lithium + FerriteCore + BadOptimizations | 1748.97 | 1899.18 | +8.59% |
| 3 | Sodium + Lithium + BadOptimizations + Better Block Entities | 1753.56 | 1906.71 | +8.73% |
| 4 | Sodium + MoreCulling + Lithium + BadOptimizations | 1754.99 | 2075.13 | +18.24% |
| 5 | Sodium + EntityCulling + MoreCulling + Lithium + FerriteCore | 1760.86 | 2009.12 | +14.10% |
| 6 | Sodium + Lithium + FerriteCore + BadOptimizations + Better Block Entities | 1793.50 | 1762.32 | -1.74% |
| 7 | Sodium + Lithium + FerriteCore + BadOptimizations | 1765.76 | 1829.85 | +3.63% |
| 8 | Sodium + ImmediatelyFast + Lithium + FerriteCore + Better Block Entities | 1770.55 | 1916.39 | +8.24% |
| 9 | Sodium + EntityCulling + Lithium + FerriteCore + Better Block Entities | 1772.98 | 2054.94 | +15.90% |
| 10 | Sodium + ImmediatelyFast + MoreCulling + Lithium + FerriteCore | 1773.41 | 1888.19 | +6.47% |
| 11 | Sodium + EntityCulling + Lithium + BadOptimizations | 1837.00 | 1781.81 | -3.00% |
| 12 | Sodium + Lithium + FerriteCore | 1784.71 | 1894.13 | +6.13% |
| 13 | Sodium + EntityCulling + MoreCulling + Lithium + FerriteCore + Better Block Entities | 1787.84 | 1909.21 | +6.79% |
| 14 | Sodium + EntityCulling + FerriteCore + C2ME + BadOptimizations + Better Block Entities | 1787.99 | 1944.70 | +8.76% |
| 15 | Sodium + EntityCulling + MoreCulling + Lithium + FerriteCore + C2ME + BadOptimizations | 1788.29 | 1920.17 | +7.37% |

## Network

| # | Stack | OpenGL | Vulkan | Vulkan vs OpenGL |
|---:|---|---:|---:|---:|
| 1 | Sodium + EntityCulling + MoreCulling + FerriteCore + BadOptimizations | 68.74 | 48.06 | -30.09% |
| 2 | Sodium + FerriteCore | 61.98 | 51.99 | -16.12% |
| 3 | Sodium + Lithium + C2ME + BadOptimizations + Better Block Entities | 61.01 | 51.45 | -15.66% |
| 4 | Sodium + EntityCulling + MoreCulling + Lithium + BadOptimizations | 60.28 | 46.67 | -22.58% |
| 5 | Sodium + FerriteCore + Better Block Entities | 58.47 | 50.63 | -13.40% |
| 6 | Sodium + ImmediatelyFast + FerriteCore + C2ME + BadOptimizations + Better Block Entities | 57.32 | 46.45 | -18.96% |
| 7 | Sodium + ImmediatelyFast + EntityCulling + MoreCulling + Better Block Entities | 56.48 | 50.94 | -9.81% |
| 8 | Sodium + EntityCulling + FerriteCore + Better Block Entities | 55.51 | 55.33 | -0.31% |
| 9 | Sodium + ImmediatelyFast + MoreCulling + FerriteCore + BadOptimizations + Better Block Entities | 54.75 | 46.80 | -14.52% |
| 10 | Sodium + EntityCulling + Lithium | 54.71 | 46.45 | -15.10% |
| 11 | Sodium + ImmediatelyFast + EntityCulling + Lithium + FerriteCore | 53.09 | 46.34 | -12.72% |
| 12 | Sodium + ImmediatelyFast + EntityCulling + MoreCulling + FerriteCore + C2ME + BadOptimizations | 52.94 | 47.20 | -10.84% |
| 13 | Sodium + EntityCulling + Lithium + FerriteCore + C2ME + Better Block Entities | 52.55 | 43.11 | -17.96% |
| 14 | Sodium + EntityCulling | 52.52 | 44.60 | -15.07% |
| 15 | Sodium + ImmediatelyFast + EntityCulling + MoreCulling + Lithium + FerriteCore + C2ME + BadOptimizations + Better Block Entities | 51.48 | 39.83 | -22.64% |

## Render Scale + Super Resolution

Status: **special_super_resolution**. Dedicated OpenGL-only matrix with native, raw RenderScale controls, and Super Resolution algorithms at matched internal render scales. RenderScale and Super Resolution are not stacked in the same profile.

## Save / Quit

Status: **planned**. Reserved in the result schema; true graceful save/quit timing will be added separately rather than using forced process cleanup.

