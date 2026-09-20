# Initial performance evidence

Measured 2026-09-20 on the verified M5 Max. Reference convention: 24 logical frames/s; 16× target: 384 frames/s. All games used native headless OpenBW and runtime LF3. Frames below are the maximum terminal callback frame across the two clients; loser and winner exit frames can differ. Each client runs its own engine plus bot.

| Complete game / archived run | Frames | Wall seconds | Frames/s | Reference speed | Peak RSS, McRave + engine |
| --- | ---: | ---: | ---: | ---: | ---: |
| WorkerRush vs Idle, `20260920T015245-8d1cc76f5e12` | 5614 | 1.536 | 3656 | 152× | Not applicable |
| McRave vs WorkerRush, `20260920T020358-c05c1bb639cc` | 8900 | 12.090 | 736 | 30.7× | 463.3 MiB |
| ZZZKBot vs McRave, `20260920T020618-09905c5f8fef` | 9520 | 15.045 | 633 | 26.4× | 464.4 MiB |

The last two totals include initialization, both engines/bots, input hashing, replay archival and initial durable terminal-manifest writes. Two small writes recording the final timing occur after that measurement. The first fixture predates durable-completion instrumentation and excludes final manifest flushes. Do not pool its unusually cheap workload into a competitive throughput average.

McRave won both smoke games. ZZZKBot reached a pool and twelve simultaneous Zerglings in the cross-game; McRave ended with two Hatcheries, twelve Drones and seventeen Zerglings. Both cross-game replays parse with screp and have matching command streams. This supports plausible port behavior, not equality to ladder binaries.

The slowest measured game exceeds 384 frames/s, but this is **not** the required fixed representative suite: only Benzene, two Zerg policies, early armies, no difficult late-game battle, and no controlled seed/starting-position schedule. We have no x86 performance proof. McRave's observed RSS includes its engine and is not an isolated bot-memory estimate; late-game growth remains unknown.

Diagnostic WorkerRush callback work was inexpensive (p99 0.0047 ms in the initial fixture), with a 2.106 ms maximum. Its sampled callback timings exclude periodic JSON writes; whole-process measurements include them. McRave does not yet have isolated callback CPU/tail/startup instrumentation. Whole-process CPU must not be mislabeled as policy CPU.

## First cross-race batch

The [controlled quick batch](evaluations/quick-baseline-v1/RESULT.md) supersedes the smoke-game performance impression. At concurrency two, seven clean games averaged 380.5 frames/s by total frames divided by summed durable seconds (15.85×); all ten attempts averaged 306.7 frames/s (12.78×, with sampled last-progress frames for timeouts). The slowest completed game was 308.4 frames/s. Two Destination games against UAlbertaBot Terran reached 120-second caps at roughly 190–202 sampled frames/s, with much larger candidate armies.

The candidate-plus-engine process consumed roughly 115 user CPU seconds per timeout, versus roughly 14 for its opponent. Its peak RSS stayed below 467 MiB during this cohort. The process is the profiling priority; these figures do not isolate policy CPU or guarantee a deployment memory budget. The 16× requirement is not satisfied by this broader cohort.

Next measurement: callback/startup profiling and sampled stacks on those preserved scenarios, with a separately identified instrumentation build and the production module retained in `artifacts/builds/`. No throughput or memory promotion gate is satisfied yet.
