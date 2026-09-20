# McRave Grids direct-bounds performance screen

Registered 2026-09-20T07:37:09Z, before candidate build or gameplay.

Operational clarification registered 2026-09-20T07:38:38Z, before build or gameplay: cap the whole cohort at 20 minutes and configure the runner to stop after the first invalid attempt (`stop_after_consecutive_invalid: 1`), matching the immediate integrity-stop rule below. No metric or decision threshold changed.

## Decision and hypothesis

This screen decides only whether the one-line Grids bounds candidate advances to a larger independent performance validation. It cannot adopt the candidate for production or make a strategy-strength claim.

The hypothesis is that replacing the proven `Grids::addToGrids` `WalkPosition::isValid()` call with a direct comparison against the existing dimensions cached at `Grids::onStart` reduces McRave process CPU per simulated frame by at least 5%, without a material per-pair CPU regression, memory regression, outcome regression, or integrity failure. Aggregate CPU/frame above 95% of control falsifies the primary hypothesis. The earlier same-input shadow observed 1,757,500,992 gameplay checks and eight boundary sentinels with zero disagreements; the profile attributed 7.98% of main-thread samples to the nested validity calls. Neither result predicts that this change alone will clear the existing 384-fps budget.

## Frozen arms and environment

- Control: McRave 9Pool candidate `fd174fa451c5c79af53b84d882f983630536c31fe116d22b76495cd1610cacfa`.
- Treatment: an isolated build from that exact source with only the `addToGrids` walk-circle condition changed from `!walk.isValid()` to direct nonnegative and cached `mapWalkWidth`/`mapWalkHeight` bounds. All shadow counters, comparisons, sentinels, and I/O are absent. Freeze its binary, binary-matched sidecar, full patch, and incremental patch before generating the operational schedule.
- Opponent: frozen UAlbertaBot `75ac4f6bb44ed6e48fbee883638c77df9557c9a88070ceca4de11183053238c9`, configured Zerg.
- Engine: frozen `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`.
- Execution: serial, no concurrent game/build/replay playback/profiler, empty per-game learning state, 120-second wall cap, escalated local execution for OpenBW sockets.

Use four fixed paired scenarios and run both arms once in each, for eight attempts total. Engine seed and McRave bot seed are the listed seed; UAlbertaBot receives no bot seed. Candidate/control slot is fixed within each pair, and arm order alternates:

| Pair | Map | Seed | McRave slot | Run order |
|---|---|---:|---:|---|
| 1 | `sscai/(2)Benzene.scx` | 9201 | 1 | control, treatment |
| 2 | `sscai/(2)Destination.scx` | 9202 | 2 | treatment, control |
| 3 | `sscai/(2)Benzene.scx` | 9203 | 2 | control, treatment |
| 4 | `sscai/(2)Destination.scx` | 9204 | 1 | treatment, control |

Run exactly this schedule once, checkpoint after every attempt, preserve all failures, and do not retry or replace a game. The cohort has a hard 20-minute elapsed cap; do not launch an attempt whose 120-second child cap cannot fit within the remaining cohort time.

## Metrics

For each McRave process, define CPU/frame as `(user_cpu_seconds + system_cpu_seconds) / result_metadata.frame_count`, using that player's fields in the final game manifest. The primary aggregate ratio is:

`(sum treatment McRave CPU seconds / sum treatment McRave frames) / (sum control McRave CPU seconds / sum control McRave frames)`.

Also report each paired ratio `treatment CPU/frame / control CPU/frame`. Peak RSS is the manifest's McRave `resource_usage.peak_rss_raw`; the cohort RSS ratio is the maximum treatment peak RSS divided by the maximum control peak RSS. Count McRave losses from verified opposing terminal metadata.

Report every game's durable FPS separately as `max(player frame_count) / durable_completion_seconds`. State for each game and the cohort whether the existing 384-fps floor is met. Any complete valid game below 384 means the overall engineering budget remains unresolved, regardless of this screen's advance decision.

## Integrity and decision rule

Every attempt must complete within its cap with both return codes zero, opposing terminal metadata, `outcome_verified: true`, both replay copies present with matching manifest hashes, and both full replay command streams structurally parse without parser errors. The adopted engine's reviewed terminal-drain diagnostics (`transport_callback` on the loser and `controller_not_occupied_after_action` on the winner) are allowed. Hash mismatch, crash, timeout, missing/malformed result, contradictory winner metadata, unrelated kill source, or replay failure makes the cohort INCONCLUSIVE and stops execution after preserving evidence. No game is silently excluded.

Advance to independent performance validation only if all eight games pass integrity and all of these gates hold:

1. aggregate treatment CPU/frame is at most 95% of control;
2. no paired treatment CPU/frame exceeds 110% of its control;
3. maximum treatment peak RSS is at most 105% of maximum control peak RSS; and
4. treatment has no more McRave losses than control across the four scenarios.

Meeting every gate is `ADVANCE`, not adoption. A complete valid cohort that misses any gate is `REJECT`. An integrity failure or unavailable required metric is `INCONCLUSIVE`. Residual same-seed run variability and four-scenario sampling limit inference; report pair values and uncertainty rather than treating pairing as deterministic replay equivalence.
