# McRave visibility-grid bounds evaluation

Registered 2026-09-20T08:04:16Z, before build or gameplay.

## Candidate and hypothesis

Control is frozen McRave `fd174fa451c5c79af53b84d882f983630536c31fe116d22b76495cd1610cacfa`. The production candidate changes only `Grids::updateVisibility()`: read `min(256, mapWidth)` and `min(256, mapHeight)` once per invocation, retain the existing x-outer/y-inner order, iterate only that rectangle, and remove the now-redundant `TilePosition::isValid()` call. It does not contain the rejected `addToGrids` direct-bounds change, diagnostics, or any policy change.

The hypothesis is that this source-equivalent loop narrowing reduces aggregate McRave process CPU/frame by at least 5% while meeting integrity, per-pair CPU, memory and outcome guards. Profile v2 attributed about 5% of all sampled main-thread stacks to the visibility call sites, so this is a bounded hypothesis rather than a claim that the change will clear the existing 384-fps floor.

## Phase 1: same-input correctness

First build a diagnostic shadow from the same frozen control. For every coordinate in the original 256×256 x-major loop, compare the authoritative `TilePosition::isValid()` result with the proposed rectangular-domain predicate using dimensions read once for that invocation. Retain the authoritative result for the only `isVisible()` call and write. Compare eight non-gameplay boundary sentinels at `onStart`: negative x/y, origin, final included corner, first excluded x/y, `(255,255)` and `(256,256)`. Persist an atomic terminal summary; write early only on the first disagreement.

Compile natively and compile all 114 translation units against official BWAPI headers with at most four jobs. Run exactly one shadow match: UAlbertaBot Zerg player 1 versus shadow McRave Zerg player 2 on Destination, engine and McRave bot seed 9500, adopted engine `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`, fresh empty learning state, and 120-second cap. No concurrent game/build/replay playback/profiler; no retry.

Correctness PASS requires a clean complete game, both replays passing full structural parsing, at least 1,000,000 real-loop comparisons, all eight sentinels, zero disagreements in both sets, opposing terminal metadata, zero child failures, and no hash mismatch or unrelated kill source. Any disagreement is FAIL. Missing coverage or integrity is INCONCLUSIVE. Only PASS permits the production build and performance phase.

## Phase 2: four-pair performance screen

After correctness PASS and source review, build and freeze the diagnostic-free production candidate with binary-matched provenance and native/official-header checks. Run these four fixed scenario pairs against frozen UAlbertaBot Zerg `75ac4f6bb44ed6e48fbee883638c77df9557c9a88070ceca4de11183053238c9`; run control and candidate once in each cell, serially, alternating arm order. Engine seed and McRave bot seed are identical within a pair.

| Pair | Map | Seed | McRave slot | Arm order |
|---|---|---:|---:|---|
| 1 | Benzene | 9601 | 1 | control, candidate |
| 2 | Destination | 9602 | 2 | candidate, control |
| 3 | Heartbreak Ridge | 9603 | 2 | control, candidate |
| 4 | Circuit Breaker | 9604 | 1 | candidate, control |

Each game has a 120-second cap and fresh empty learning state. Run all eight once with no retry or replacement; stop on the first integrity-invalid result. The whole cohort cap is 20 minutes. Preserve every attempt and parse both full replay command streams before proceeding.

For the McRave process, CPU/frame is `(user_cpu_seconds + system_cpu_seconds) / result_metadata.frame_count`. The aggregate ratio is `(sum candidate CPU / sum candidate frames) / (sum control CPU / sum control frames)`. Report each pair's corresponding ratio. Peak RSS is `resource_usage.peak_rss_raw`; compare the maximum candidate value with the maximum control value. Report every game's durable FPS as `max(player frame_count) / durable_completion_seconds`.

`ADVANCE` to independent performance validation requires all eight integrity-valid games, aggregate candidate CPU/frame ≤95% of control, every paired ratio ≤110%, maximum candidate RSS ≤105% of maximum control RSS, and no more candidate losses than control. A complete cohort missing any gate is `REJECT`; integrity or required-metric failure is `INCONCLUSIVE`. Any complete valid game below 384 FPS leaves the absolute engineering budget unresolved and is reported separately without changing the advancement decision.

This screen can advance an engineering candidate only. It cannot adopt it, alter the earlier direct-walk-bounds rejection, establish strength, or change the rating graph.
