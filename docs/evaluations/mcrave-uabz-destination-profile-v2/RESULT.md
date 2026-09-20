# McRave versus UAlbertaBot Zerg late-game CPU profile v2 result

**PASS.** Grids is the qualifying cohesive subsystem: 1,611 of 8,032 sampled main-thread stacks (20.06%) enter the outer `Grids::onFrame` branch. The capture exceeded the 1,000-sample bar, ran for the full requested live interval after frame 15,000, and retained enough symbols for a narrow follow-up.

## Capture integrity

The runner exec session was `52647`, run `20260920T072421-86abc73ea7da`, and the live manifest identified player 2 McRave as PID `77665`. The polling command first displayed frame 15,120 before sampling, but that transient observation was not archived. The preserved `trigger-diagnostic.json` copied immediately before `/usr/bin/sample` reports frame 18,720, bot seed 9202, and `ended: false`; frame 18,720 is therefore the reproducible trigger evidence. The sole `/usr/bin/sample 77665 10 1` command returned 0. Command timestamps span `2026-09-20T07:25:04.936486Z` through `07:25:15.050939Z` (10.114 seconds); the sample header begins at `07:25:04.968Z`, and the target remained alive until match completion at `07:25:42.747Z`. This directly establishes a full ten seconds against the live target.

The raw 10-second report contains 8,032 main-thread samples and has SHA-256 `265fb4115b222a4682eb3f39af9105ee0bf4629face09528d2a6366dce9c1880`. Capture metadata is `artifacts/experiments/mcrave-uabz-destination-profile-v2/raw/capture.json` (SHA-256 `caf5c3ba00a7678517b16c69a1a90dbefd435ef29830e336ce2e08f14be5acec`), and derived counts are in `analysis.json` (SHA-256 `470e722c49a415e367f5da6e91dbdf05f1701a599bb44184ffa4c8745737cf2f`).

The match completed separately in 81.550 seconds at local frames 27,779/27,810. McRave won, both processes returned 0, terminal results were opposing, `outcome_verified` was true, and both replays were archived. Logs contain the reviewed terminal-drain pair (`transport_callback` on the loser and `controller_not_occupied_after_action` on the winner), with no hash mismatch, crash, timeout, or unrelated kill source. This sampled match is excluded from throughput and strength evidence as preregistered.

## Nonoverlapping main-thread partition

Primary rows are mutually exclusive outer `McRaveModule::onFrame` call-site branches. The remainder includes smaller McRave branches and work outside McRave's frame callback; descendants are not added to their parents.

| Primary branch | Samples | Main thread |
|---|---:|---:|
| Grids | 1,611 | 20.06% |
| Units | 1,200 | 14.94% |
| Combat | 1,118 | 13.92% |
| Targets | 757 | 9.42% |
| Support | 748 | 9.31% |
| Resources | 141 | 1.76% |
| Expansion | 117 | 1.46% |
| Other McRave frame branches | 261 | 3.25% |
| Outside McRave frame branches | 2,079 | 25.88% |

Within Grids, the `updateGrids`/walk-grid call-site branch accounts for 1,063 samples (13.23% of the main thread). Its nested `BWAPI::Point<int, 8>::isValid()` calls account for 641 samples (7.98% of the main thread and 60.30% of that branch), dominated by repeated `mapWidth()` and `mapHeight()` calls. The visibility-loop call sites account for another 404 samples (5.03%). These are inclusive drill-down figures and overlap the 1,611-sample Grids parent.

For comparison, Combat JPS generation accounts for 494 samples (6.15%), Combat A* generation for 99 (1.23%), and Support JPS generation for 711 (8.85%). Each is nested in its corresponding primary branch.

## Narrow follow-up

The narrowest evidence-backed candidate is the walk-position bounds check in `Grids::addToGrids`: its per-unit walk-circle loop calls `walk.isValid()` for every candidate tile even though Grids already initializes fixed `mapWalkWidth` and `mapWalkHeight`. A same-input shadow should compare the existing validity result with direct `0 <= x < mapWalkWidth` and `0 <= y < mapWalkHeight`, count calls and mismatches, and leave the existing result authoritative. Only zero mismatches over representative edge and interior positions would justify a production change. The separate fixed 256-by-256 visibility scan should remain a later candidate so the first test isolates the larger observed call site.

This profile describes one process, scenario, machine, and late-game interval. Sampling perturbs the target, and inclusive drill-down counts overlap their parent branch. It supports a bounds-check diagnostic, not implementation, throughput, or strategy claims.
