# McRave per-search memoization throughput result

Decision: **REJECT**. All ten registered games completed with verified opposing results, no crash, timeout, contradictory metadata, or `insync_hash_mismatch`. The aggregate passed at 178,094 frames / 431.098 durable seconds = **413.1 frames/s**, but games 6–9 measured 362.9, 353.9, 269.5, and 355.8 frames/s. The preregistered gate requires every game and the aggregate to reach 384 frames/s, so the four valid slow games reject the candidate as the engineering baseline. No game was retried or replaced.

| Game | Opponent | Map | Candidate slot | Result | Frames | Durable seconds | Frames/s |
| --- | --- | --- | ---: | --- | ---: | ---: | ---: |
| 1 | ZZZKBot Zerg | Benzene | 1 | win | 13,767 | 21.599 | 637.4 |
| 2 | ZZZKBot Zerg | Benzene | 2 | win | 16,433 | 28.739 | 571.8 |
| 3 | ZZZKBot Zerg | Destination | 1 | win | 16,092 | 29.959 | 537.1 |
| 4 | ZZZKBot Zerg | Destination | 2 | win | 16,154 | 27.920 | 578.6 |
| 5 | UAlbertaBot Protoss | Benzene | 1 | win | 16,867 | 37.500 | 449.8 |
| 6 | UAlbertaBot Protoss | Destination | 2 | win | 17,425 | 48.018 | **362.9** |
| 7 | UAlbertaBot Protoss | Benzene | 2 | win | 20,835 | 58.868 | **353.9** |
| 8 | UAlbertaBot Terran | Destination | 1 | win | 24,028 | 89.168 | **269.5** |
| 9 | UAlbertaBot Terran | Benzene | 1 | win | 18,882 | 53.067 | **355.8** |
| 10 | UAlbertaBot Terran | Destination | 2 | win | 17,611 | 36.259 | 485.7 |

Collection took 230.486 seconds with concurrency two, followed by a successful default publish hook. Batch wall time is operational context; the registered aggregate uses the sum of per-game durable completion times. Each duration includes both engines, both bots, startup, logging, and archival.

## Integrity and replay validation

Both processes exited zero in every game, and each client pair reported exactly one winner and one loser. All ten client pairs recorded the ordinary terminal diagnostic pattern: winner-side `controller_not_occupied_after_action` after action 87 (`Leave Game`) and loser-side `transport_callback`. No client stderr contained `insync_hash_mismatch`, and no opposing winner callback appeared.

All 20 replay files were copied and hashed, totaling 14,409,237 bytes. The existing `screp` parser successfully read all 20 with zero nonzero exits, and each replay's current SHA-256 matched its match manifest. The durable parser ledger is `artifacts/experiments/quick-mcrave-as-memo-v1/replay-validation/summary.json`, SHA-256 `5ce14dff3af6f58e7641a9addea34de398e908c77aa6cf92ef4c4e0dbafb3c7a`; individual overview and stderr files are stored alongside it. Parser success establishes structural readability, not deterministic playback or semantic equivalence.

## Resource and outcome scope

Candidate-plus-engine CPU totaled 400.780 seconds across the ten games. Per-game CPU ranged from 19.362 to 85.195 seconds, with a median of 34.604 seconds. Candidate-plus-engine peak RSS ranged from 484,311,040 to 491,470,848 bytes; median RSS was 487,653,376 bytes (465.1 MiB), and the maximum was 468.7 MiB. These measurements include OpenBW and cannot be attributed to McRave alone. Opponent-plus-engine CPU totaled 61.108 seconds. Ordinary desktop background activity was not controlled.

The candidate won all ten games. ZZZKBot's 4/4 opponent-specific Wilson 95% interval is 51.0–100%; each UAlberta race's 3/3 interval is 43.9–100%. The corresponding opponent-relative Elo point estimates are infinite at an observed 100% win rate, so they are not finite ratings or evidence of an absolute BASIL level. The reused scenarios are descriptive and do not establish a causal strength improvement.

The aggregate and several individual measurements are descriptively faster than the preceding bounds candidate, but trajectories and terminal frames differed despite fixed seeds. The preregistration expressly disallows treating this cohort as a paired causal speed comparison. The same-input shadow's output-equivalence result remains valid; this batch only rejects the candidate against the full-match slow-tail performance bar. The highest-value next measurement is a CPU profile of this production candidate on game 8's Destination/UAlbertaBot Terran seed-3001 scenario, which remained the slowest valid case at 269.5 frames/s.

## Schedule erratum

The frozen schedule's `title` says “McRave A* bounds throughput check,” and its `entry_condition` repeats the earlier bounds-shadow count of 13,439. Those are stale descriptive template fields. The registered plan, experiment ID, candidate hash `04521befa41bb3873783b215493abf3a071414d2a5315cdea68fc7a67f4415ec`, hypothesis, engine, ten scenario rows, seeds, and fixed decision bar identify the memoization gate correctly. The schedule was preserved unchanged, and the stale wording was not treated as an eligibility condition.

The authoritative aggregate ledger is `artifacts/experiments/quick-mcrave-as-memo-v1/manifest.json`, SHA-256 `26de09adf181e54bd78dcd296ae954cd8c7b3ce9b1af74d93e16d8d4a327b608`; its ten `match_manifest` entries retain every raw result, client log and replay record.
