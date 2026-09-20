# McRave seeded goal-cache result

Both seed pairs completed with clean process exits, valid terminal metadata, and two replay files each. `screp` parsed all four player-one replays. The explicit bot seed worked for opening selection: seed 4101 selected `PoolHatch12Pool2HatchMuta` in both variants, while seed 4102 selected `HatchPool12Hatch3HatchMuta` in both variants.

| Seed | Variant | Run | Frames | Durable seconds | Durable FPS | McRave user CPU | Result |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 4101 | seed-only baseline | `20260920T031834-6b2e6bccd324` | 22,261 | 84.197 | 264.390 | 78.333 s | win |
| 4101 | goal cache | `20260920T032008-0612bbfdc30b` | 23,191 | 81.384 | 284.958 | 76.511 s | win |
| 4102 | seed-only baseline | `20260920T032211-8dc43b1938ab` | 17,704 | 49.741 | 355.921 | 46.918 s | win |
| 4102 | goal cache | `20260920T032312-56ef416d36d2` | 17,363 | 43.951 | 395.050 | 41.231 s | win |

Candidate durable FPS was 7.78% higher for seed 4101 and 10.99% higher for seed 4102. McRave CPU per logical frame was 6.24% and 10.39% lower, respectively.

The preregistered command-compatibility condition did not pass. Although starts and openings matched, normalized replay commands diverged at frame 3: the first Zerg worker targeted a different mineral position. The games later ended at different frames and with different unit counts. This divergence occurs before the optimized late-game goal assignment is expected to matter and shows residual address, container-order, opponent, or other uncontrolled nondeterminism. The throughput numbers remain useful observations but are not an isolated causal estimate of the cache.

The earlier `mcrave-goal-distance-cache-v1` preregistration contained a manually entered `created_at` of `03:09:00Z`. APFS birth, modification, and change timestamps all recorded `03:07:48Z`, before its candidate launch at about `03:08:48Z`. The original timestamp was retained and an explicit amendment added; no claim relies on the erroneous manual value.

The cache remains an engineering candidate. This evaluation supports no strength claim and does not promote or replace a configured bot.
