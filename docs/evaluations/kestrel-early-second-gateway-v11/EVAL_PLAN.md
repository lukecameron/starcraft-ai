# Kestrel v11 early second-Gateway screen

## Decision

- Registered: `2026-09-20T07:08:18.524259+00:00`, before compilation or any v11 game.
- Review refinement: `2026-09-20T07:09:15.607540+00:00`, before compilation or launch. The source now explicitly blocks gas while a known-Zerg game has fewer than two current Gateways, and the primary metric measures overlap before the first Zealot dies rather than requiring both Zealots to be complete at the instant the threat first crosses the radius. Tactical scope, schedule, and lifecycle bars are unchanged.
- Locality refinement: `2026-09-20T07:10:21.950959+00:00`, before launch. The primary counter now includes only completed Zealots within the same 12-tile home radius, while retaining the global completed count as context. The threat requires a visible, detected, nonflying enemy type capable of attacking. The overlap window ends at first Zealot loss or game end, so a game with no Zealot loss is valid. Schedule and threshold remain unchanged.
- Hypothesis: against a known Zerg opponent, making the second Gateway the next production structure after the first Gateway begins, before the Assimilator, will provide at least two simultaneously completed Zealots in the home fight before the first Zealot dies.
- Falsification: either valid game never reaches two simultaneously completed Zealots after the first home threat and before the first Zealot death, fails the production/lifecycle guard, or fails the clean-game guard.
- Decision: `ADOPT` means retain v11 only for a broader paired Zerg evaluation; it does not replace canonical v7 or establish strength. Otherwise `REJECT`. An infrastructure-invalid game with no permitted retry yields `INCONCLUSIVE`.

## Arms and change

- Control evidence: frozen canonical v7 and the diagnostic-only run `20260920T070255-f110c96947fd`. The diagnostic observed the first Gateway request at frame 2,058, second Gateway request at 3,672, and first five-unit home threat at checkpoint 3,720 with zero completed Zealots. The first Zealot then fought alone and died. This supports a production-bottleneck hypothesis; it is not an exhaustive causal proof or a deterministic control arm.
- Treatment: isolated v11 source based byte-for-byte on v7. When the known enemy race is Zerg and exactly one Gateway is current, request the second Gateway as soon as 150 minerals are available, before the existing supply-26 condition. Do not request the Assimilator until two Gateways are current. Other races and all Probe, Pylon, train, gas/Core after two Gateways, scouting, targeting, and combat behavior remain v7.
- Instrumentation: result telemetry adds first/second current and completed Gateway frames, the first four accepted Zealot-train frames, first visible/detected ground attacker within 12 tiles of home, completed Zealots and nearby attacker count at that instant, maximum simultaneous completed Zealots globally and within the home radius after home threat and before first Zealot loss or game end, first Zealot-loss frame, and first own Probe-loss frame. This adds public reads and counters only. Because cached v7 lacks these fields and the diagnostic had heavier JSONL logging, timing comparisons are descriptive matched-input evidence, not deterministic or performance comparisons.
- Source identity: combined source SHA-256 `e1cfd1c9b369a755044f4652cfbfad2d2cb4d444df0a33c2ad279375551a79b6`; v7-to-v11 patch SHA-256 `85d6fb714e9bdb7fe43e7c3d6bb6d03c6a9603a8264bad5ebba54ee940d995d0`. Native and official-header binary identity will be appended before launch without changing source or gates.
- Build identity amendment: `2026-09-20T07:10:53.254142+00:00`, before launch. Native and official BWAPI 4.4 header targets compiled successfully; frozen module SHA-256 is `e997841c5f173d5218f7599ab60b9dc391335f8a45788f69df3fea3bc740f49c`.

## Fixed execution

- Exactly two full games, serial: v11 Protoss as player 1 versus frozen ZZZK Zerg on Benzene seed `6103`, then Heartbreak Ridge seed `6104`.
- Adopted engine `eee406…`, LF3, empty isolated learning state, 120-second cap, no bot seeds, retries, replacements, or adaptive maps.
- Minimum sample size and stopping rule: both scheduled games once. Preserve every outcome. Stop after an infrastructure-invalid attempt because the schedule permits no retry.
- Invalid only for launcher nonzero exit, timeout, missing/inconsistent callbacks, state-hash mismatch, missing telemetry, or an unreadable replay. Gameplay losses and policy failures remain valid and cannot be excluded.

## Metrics and gates

- Primary metric: `min(max_home_zealots_before_first_loss)` across the two candidate result objects, in units, sourced directly from each bot's telemetry after the first home threat and before the first Zealot loss or game end. Direction is higher. Adoption threshold is at least `2` in both games. `first_home_threat_frame` and `nearby_enemies_at_first_home_threat` must be nonnegative/positive so the overlap window is observed. `first_zealot_loss_frame == -1` is valid when no Zealot dies before game end. Also report global overlap and `completed_zealots_at_first_home_threat` without using them as the adoption threshold.
- Mechanism guard: second Gateway becomes current by frame 3,000 and completes before `first_home_threat_frame` in both games. Report first/second Gateway current/completion frames and first two Zealot-train frames. The diagnostic's second request at 3,672 is context, not a deterministic improvement threshold.
- Clean-game guard: both launchers return zero, callbacks are reciprocal, no state-hash mismatch, two replays parse with no command error, and durable throughput is at least 384 logical frames/s. Throughput only validates the package; instrumentation and short games prohibit a performance claim.
- Production/lifecycle guard: each game reaches two Gateways, at least three current/completed Zealots or a win, scouting and combat commands, fewer than 5% rejected commands, and no wrong-race production.
- Outcome: wins, terminal frame, worker-loss timing, and survival after first home threat are descriptive. A longer loss or a single win cannot satisfy the primary metric by itself and cannot support a strength claim.
