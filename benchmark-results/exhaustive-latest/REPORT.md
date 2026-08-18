# Exhaustive MCBench powerset screening

- Shards merged: **44**
- Configs: **176 / 256**
- Raw runs: **352**
- Invalid runs: **0**

> Screening only: GitHub-hosted Ubuntu uses software graphics. Use this run to find interactions/candidates, then repeat finalists on physical hardware.

## Renderer / FPS

| # | Stack | OpenGL | Vulkan | Vulkan vs OpenGL |
|---:|---|---:|---:|---:|
| 1 | Sodium + EntityCulling + Lithium + FerriteCore + BadOptimizations | 57.01 | 48.25 | -15.36% |
| 2 | Sodium + EntityCulling + MoreCulling + Lithium + BadOptimizations + Better Block Entities | 53.06 | 48.47 | -8.64% |
| 3 | Sodium + ImmediatelyFast + Lithium | 52.92 | 45.87 | -13.33% |
| 4 | Sodium + MoreCulling + Lithium + BadOptimizations | 52.92 | 49.49 | -6.48% |
| 5 | Sodium + EntityCulling + MoreCulling + FerriteCore + Better Block Entities | 40.95 | 37.69 | -7.94% |
| 6 | Sodium + ImmediatelyFast + Lithium + Better Block Entities | 38.90 | 34.31 | -11.81% |
| 7 | Sodium + EntityCulling + MoreCulling | 35.18 | 33.00 | -6.19% |
| 8 | Sodium + EntityCulling + MoreCulling + Lithium + FerriteCore + C2ME | 33.30 | 31.74 | -4.66% |
| 9 | Sodium + MoreCulling + C2ME + BadOptimizations | 32.54 | 30.26 | -7.03% |
| 10 | Sodium + EntityCulling + Lithium + FerriteCore + C2ME + BadOptimizations | 31.93 | 31.04 | -2.78% |
| 11 | Sodium + EntityCulling + C2ME + BadOptimizations | 31.88 | 28.92 | -9.28% |
| 12 | Sodium + EntityCulling + FerriteCore + C2ME + BadOptimizations | 31.52 | 30.12 | -4.44% |
| 13 | Sodium + C2ME | 29.89 | 25.84 | -13.54% |
| 14 | Sodium + ImmediatelyFast + EntityCulling + FerriteCore + C2ME + BadOptimizations | 28.43 | 27.44 | -3.46% |
| 15 | Sodium + EntityCulling + MoreCulling + Lithium + C2ME + BadOptimizations + Better Block Entities | 28.41 | 27.41 | -3.53% |

## Particle

| # | Stack | OpenGL | Vulkan | Vulkan vs OpenGL |
|---:|---|---:|---:|---:|
| 1 | Sodium + EntityCulling + MoreCulling + Lithium + BadOptimizations + Better Block Entities | 90.18 | 74.29 | -17.61% |
| 2 | Sodium + EntityCulling + Lithium + FerriteCore + BadOptimizations | 82.60 | 73.34 | -11.21% |
| 3 | Sodium + ImmediatelyFast + Lithium | 79.02 | 70.08 | -11.32% |
| 4 | Sodium + MoreCulling + Lithium + BadOptimizations | 78.85 | 77.58 | -1.61% |
| 5 | Sodium + EntityCulling + MoreCulling + FerriteCore + Better Block Entities | 72.08 | 64.02 | -11.19% |
| 6 | Sodium + EntityCulling + MoreCulling | 70.05 | 54.43 | -22.29% |
| 7 | Sodium + EntityCulling + MoreCulling + Lithium + FerriteCore + C2ME | 69.93 | 60.57 | -13.38% |
| 8 | Sodium + EntityCulling + C2ME + BadOptimizations | 65.66 | 60.43 | -7.95% |
| 9 | Sodium + EntityCulling + FerriteCore + C2ME + BadOptimizations | 64.52 | 60.00 | -7.01% |
| 10 | Sodium + EntityCulling + Lithium + FerriteCore + C2ME + BadOptimizations | 63.94 | 51.15 | -20.00% |
| 11 | Sodium + C2ME | 63.00 | 53.68 | -14.78% |
| 12 | Sodium + ImmediatelyFast + Lithium + Better Block Entities | 62.96 | 58.86 | -6.51% |
| 13 | Sodium + MoreCulling + C2ME + BadOptimizations | 62.67 | 44.48 | -29.02% |
| 14 | Sodium + EntityCulling + MoreCulling + Lithium + C2ME + BadOptimizations + Better Block Entities | 62.10 | 56.51 | -9.01% |
| 15 | Sodium + EntityCulling + MoreCulling + BadOptimizations | 59.08 | 50.32 | -14.82% |

## Block Entity

| # | Stack | OpenGL | Vulkan | Vulkan vs OpenGL |
|---:|---|---:|---:|---:|
| 1 | Sodium + EntityCulling + Lithium + FerriteCore + BadOptimizations | 81.23 | 68.00 | -16.29% |
| 2 | Sodium + EntityCulling + MoreCulling + Lithium + BadOptimizations + Better Block Entities | 77.51 | 68.37 | -11.79% |
| 3 | Sodium + MoreCulling + Lithium + BadOptimizations | 77.23 | 62.98 | -18.45% |
| 4 | Sodium + ImmediatelyFast + Lithium | 74.40 | 62.13 | -16.49% |
| 5 | Sodium + EntityCulling + MoreCulling + FerriteCore + Better Block Entities | 67.31 | 58.24 | -13.47% |
| 6 | Sodium + ImmediatelyFast + Lithium + Better Block Entities | 57.22 | 49.74 | -13.07% |
| 7 | Sodium + EntityCulling + MoreCulling | 55.99 | 52.26 | -6.66% |
| 8 | Sodium + EntityCulling + MoreCulling + Lithium + FerriteCore + C2ME | 50.18 | 54.58 | +8.76% |
| 9 | Sodium + EntityCulling + Lithium + FerriteCore + C2ME + BadOptimizations | 51.16 | 41.85 | -18.19% |
| 10 | Sodium + MoreCulling + C2ME + BadOptimizations | 50.35 | 42.74 | -15.12% |
| 11 | Sodium + EntityCulling + MoreCulling + BadOptimizations | 47.50 | 35.07 | -26.18% |
| 12 | Sodium + C2ME | 46.33 | 36.32 | -21.62% |
| 13 | Sodium + EntityCulling + C2ME + BadOptimizations | 46.24 | 46.16 | -0.17% |
| 14 | Sodium + EntityCulling + FerriteCore + C2ME + BadOptimizations | 44.90 | 42.06 | -6.33% |
| 15 | Sodium only | 44.55 | 39.57 | -11.17% |

## Chunk Generation

| # | Stack | OpenGL | Vulkan | Vulkan vs OpenGL |
|---:|---|---:|---:|---:|
| 1 | Sodium + EntityCulling + Lithium + FerriteCore + BadOptimizations | 58.06 | 51.10 | -11.98% |
| 2 | Sodium + ImmediatelyFast + Lithium | 54.92 | 42.48 | -22.65% |
| 3 | Sodium + MoreCulling + Lithium + BadOptimizations | 51.84 | 47.46 | -8.45% |
| 4 | Sodium + EntityCulling + MoreCulling + Lithium + BadOptimizations + Better Block Entities | 51.74 | 42.68 | -17.51% |
| 5 | Sodium + EntityCulling + MoreCulling + FerriteCore + Better Block Entities | 46.68 | 43.78 | -6.20% |
| 6 | Sodium + ImmediatelyFast + MoreCulling + C2ME + BadOptimizations | 45.05 | 40.58 | -9.93% |
| 7 | Sodium + EntityCulling + Lithium + FerriteCore + C2ME + BadOptimizations | 43.34 | 40.95 | -5.53% |
| 8 | Sodium + EntityCulling + FerriteCore + C2ME + BadOptimizations | 41.73 | 39.87 | -4.47% |
| 9 | Sodium + MoreCulling + C2ME + BadOptimizations | 41.64 | 36.63 | -12.03% |
| 10 | Sodium + EntityCulling + MoreCulling | 41.19 | 36.58 | -11.18% |
| 11 | Sodium + ImmediatelyFast + MoreCulling + FerriteCore + C2ME + BadOptimizations | 41.08 | 32.03 | -22.01% |
| 12 | Sodium + EntityCulling + MoreCulling + Lithium + C2ME + BadOptimizations + Better Block Entities | 40.85 | 38.06 | -6.82% |
| 13 | Sodium + ImmediatelyFast + EntityCulling + FerriteCore + C2ME + BadOptimizations | 40.71 | 40.46 | -0.63% |
| 14 | Sodium + ImmediatelyFast + FerriteCore + C2ME + Better Block Entities | 40.56 | 31.33 | -22.77% |
| 15 | Sodium + ImmediatelyFast + Lithium + Better Block Entities | 38.90 | 39.91 | +2.61% |

## Lighting

| # | Stack | OpenGL | Vulkan | Vulkan vs OpenGL |
|---:|---|---:|---:|---:|
| 1 | Sodium + EntityCulling + Lithium + FerriteCore + BadOptimizations | 88.11 | 75.19 | -14.67% |
| 2 | Sodium + MoreCulling + Lithium + BadOptimizations | 86.85 | 75.28 | -13.32% |
| 3 | Sodium + EntityCulling + MoreCulling + Lithium + BadOptimizations + Better Block Entities | 82.93 | 74.50 | -10.17% |
| 4 | Sodium + ImmediatelyFast + Lithium | 76.87 | 64.10 | -16.62% |
| 5 | Sodium + EntityCulling + MoreCulling + FerriteCore + Better Block Entities | 69.70 | 56.69 | -18.66% |
| 6 | Sodium + EntityCulling + MoreCulling + Lithium + FerriteCore + C2ME | 69.25 | 66.16 | -4.45% |
| 7 | Sodium + EntityCulling + MoreCulling | 67.86 | 58.40 | -13.93% |
| 8 | Sodium + ImmediatelyFast + Lithium + Better Block Entities | 63.22 | 55.65 | -11.98% |
| 9 | Sodium + EntityCulling + Lithium + FerriteCore + C2ME + BadOptimizations | 62.15 | 59.04 | -5.00% |
| 10 | Sodium + EntityCulling + FerriteCore + C2ME + BadOptimizations | 61.65 | 54.59 | -11.45% |
| 11 | Sodium + C2ME | 61.28 | 56.42 | -7.93% |
| 12 | Sodium + EntityCulling + MoreCulling + Lithium + FerriteCore | 60.02 | 49.20 | -18.03% |
| 13 | Sodium + MoreCulling + C2ME + BadOptimizations | 59.39 | 45.78 | -22.92% |
| 14 | Sodium + EntityCulling + C2ME + BadOptimizations | 56.78 | 58.83 | +3.60% |
| 15 | Sodium + EntityCulling + MoreCulling + Lithium + C2ME + BadOptimizations + Better Block Entities | 56.68 | 52.39 | -7.56% |

## Memory

| # | Stack | OpenGL | Vulkan | Vulkan vs OpenGL |
|---:|---|---:|---:|---:|
| 1 | Sodium + ImmediatelyFast + EntityCulling + Lithium + FerriteCore + Better Block Entities | 1759.10 | 1893.04 | +7.61% |
| 2 | Sodium + Lithium + FerriteCore + BadOptimizations | 1761.96 | 1900.87 | +7.88% |
| 3 | Sodium + Lithium + FerriteCore + BadOptimizations + Better Block Entities | 1765.15 | 1855.23 | +5.10% |
| 4 | Sodium + ImmediatelyFast + EntityCulling + MoreCulling + Lithium | 1768.19 | 1911.04 | +8.08% |
| 5 | Sodium + MoreCulling | 1772.65 | 2159.83 | +21.84% |
| 6 | Sodium + ImmediatelyFast + Lithium + BadOptimizations + Better Block Entities | 1776.19 | 1865.71 | +5.04% |
| 7 | Sodium + MoreCulling + Lithium + FerriteCore + BadOptimizations + Better Block Entities | 1781.16 | 1932.59 | +8.50% |
| 8 | Sodium + Lithium | 1781.83 | 1809.03 | +1.53% |
| 9 | Sodium + ImmediatelyFast + EntityCulling + MoreCulling + Lithium + Better Block Entities | 1784.53 | 1901.60 | +6.56% |
| 10 | Sodium + EntityCulling + MoreCulling + Lithium + FerriteCore + Better Block Entities | 1854.88 | 1791.40 | -3.42% |
| 11 | Sodium + MoreCulling + Lithium + C2ME + BadOptimizations | 1794.41 | 1942.43 | +8.25% |
| 12 | Sodium + ImmediatelyFast + Lithium + FerriteCore + BadOptimizations | 1797.65 | 1835.04 | +2.08% |
| 13 | Sodium + ImmediatelyFast + EntityCulling + Lithium + Better Block Entities | 1800.98 | 1867.22 | +3.68% |
| 14 | Sodium + EntityCulling + MoreCulling + FerriteCore | 1805.38 | 1922.69 | +6.50% |
| 15 | Sodium + Lithium + FerriteCore + Better Block Entities | 1848.11 | 1805.44 | -2.31% |

## Network

| # | Stack | OpenGL | Vulkan | Vulkan vs OpenGL |
|---:|---|---:|---:|---:|
| 1 | Sodium + EntityCulling + Lithium + FerriteCore + BadOptimizations | 88.77 | 68.71 | -22.60% |
| 2 | Sodium + MoreCulling + Lithium + BadOptimizations | 87.45 | 69.92 | -20.04% |
| 3 | Sodium + ImmediatelyFast + Lithium | 82.09 | 70.53 | -14.08% |
| 4 | Sodium + EntityCulling + MoreCulling + Lithium + BadOptimizations + Better Block Entities | 81.11 | 74.82 | -7.75% |
| 5 | Sodium + EntityCulling + MoreCulling + FerriteCore + Better Block Entities | 76.02 | 66.52 | -12.49% |
| 6 | Sodium + C2ME | 70.78 | 58.74 | -17.01% |
| 7 | Sodium + EntityCulling + C2ME + BadOptimizations | 68.33 | 63.46 | -7.12% |
| 8 | Sodium + EntityCulling + MoreCulling + Lithium + FerriteCore + C2ME | 67.73 | 65.62 | -3.11% |
| 9 | Sodium + MoreCulling + C2ME + BadOptimizations | 66.50 | 50.72 | -23.72% |
| 10 | Sodium + EntityCulling + MoreCulling + Lithium + C2ME + BadOptimizations + Better Block Entities | 64.26 | 51.96 | -19.14% |
| 11 | Sodium + EntityCulling + FerriteCore + C2ME + BadOptimizations | 63.51 | 58.77 | -7.46% |
| 12 | Sodium + EntityCulling + Lithium + FerriteCore + C2ME + BadOptimizations | 63.34 | 55.78 | -11.93% |
| 13 | Sodium + ImmediatelyFast + Lithium + Better Block Entities | 62.78 | 54.81 | -12.70% |
| 14 | Sodium + ImmediatelyFast + MoreCulling + C2ME + BadOptimizations | 60.28 | 53.29 | -11.61% |
| 15 | Sodium + EntityCulling + MoreCulling | 59.62 | 56.92 | -4.53% |

## Save / Quit

Status: **planned**. Reserved in the result schema; true graceful save/quit timing will be added separately rather than using forced process cleanup.

