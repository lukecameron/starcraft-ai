# Current-engine local anchor calibration v4

Registered 2026-09-20T07:51:19Z, before any v4 game or replay result.

## Evidence gap and decision

The current-engine v2 and v3 cohorts contain 36 reviewed games across five exact build/race/config nodes. Eight of the ten possible direct graph edges have evidence. The two missing edges are ZZZK–UAlberta Protoss and Stardust–UAlberta Terran. The latter is unlikely to be the best use of a small extension: Stardust is already 16–0 and more one-sided Stardust rows add little information. UAlberta Protoss and Terran have the closest displayed estimates (535 and 580), wide overlapping conditional intervals, and a 2–2 direct record that changes by map. ZZZK–UAlberta Protoss is the remaining informative missing edge connected to the arbitrary 1000 reference.

This 12-game extension therefore assigns six games to the missing ZZZK–UAlberta Protoss edge and six to the close, map-sensitive UAlberta Protoss–Terran edge. The primary decision is whether the complete reviewed cohort is eligible for inclusion in the existing local-rating display. There is no required Elo direction and no bot promotion decision.

## Frozen regime and schedule

Use the exact current rating regime: engine `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`, game-data package already used by v2/v3, macOS ARM64, LF3, fresh empty isolated learning state, no adjudication, and a 180-second per-game timeout. Run serially with no concurrent game, build, replay playback, or profiler. Use the frozen UAlbertaBot module `75ac4f6bb44ed6e48fbee883638c77df9557c9a88070ceca4de11183053238c9` as Protoss and Terran nodes with the same packaged AI configuration as v2/v3, and frozen ZZZKBot `ce796a5d49d78121aaf42b57ba758423ee89f74a249b42180cbc0b0cb9df4748` as Zerg.

The operational schedule is `config/local-anchor-calibration-v4.json`. It has exactly 12 attempts: three fresh map/seed cells per edge, each run once with UAlberta Protoss in player 1 and once in player 2. Seeds 9401–9403 cover UAlberta Protoss–Terran on Benzene, Heartbreak Ridge and Destination. Seeds 9404–9406 cover UAlberta Protoss–ZZZK on Destination, Circuit Breaker and Benzene. Seeds are fixed before outcomes and are not selected from prior simulations.

Run every attempt once, persist the ledger after each attempt, and never retry, replace a seed, or adapt to outcomes. Stop immediately after the first invalid integrity result and preserve the valid reviewed subset; a stopped or interrupted cohort is INCONCLUSIVE for complete v4 inclusion.

## Inclusion and reporting rules

`INCLUDE` requires all 12 attempts to complete within the cap with both child return codes zero, opposing boolean terminal metadata, `outcome_verified: true`, no state-hash mismatch or unrelated kill source, and two archived replay copies whose bytes match their manifest hashes. Parse every complete replay command stream with screp and require zero parser-error commands, expected races, and the recorded owner-frame relationship. The adopted terminal-drain pair (`transport_callback` on the loser and `controller_not_occupied_after_action` on the winner) is allowed. Any missing/malformed result, crash, timeout, contradictory winner metadata, replay failure, or unreviewed engine diagnostic makes the complete cohort INCONCLUSIVE; no result is silently excluded.

If eligible, pool the 12 reviewed games with v2/v3 only after verifying exact node and regime identities and pinning each final manifest hash. Recompute the unchanged Gaussian-prior Bradley–Terry MAP with 400 Elo prior SD, approximate 95% Laplace contrast intervals, and 200/800 sensitivity. ZZZK remains an arbitrary 1000 coordinate rather than a BASIL calibration. Report both new direct matchup records and cumulative estimates, with uncertainty and residual map/slot dependence. Durable FPS, CPU and RSS are descriptive because this is a rating cohort, not a performance gate.

All outcomes remain conditional on a small local map/seed sample and a scalar transitive model. Inclusion improves graph evidence; it does not prove absolute strength, tournament transfer, or independence of paired slot observations.
