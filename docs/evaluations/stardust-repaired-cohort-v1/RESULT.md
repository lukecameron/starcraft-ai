# Stardust empty-timer repair cohort result

## Outcome: PASS

The frozen repair passed the registered compatibility gate. All four scheduled games completed with zero launcher return codes and verified opposing winner callbacks. No client reported `insync_hash_mismatch` or `consumer_fail_closed`.

| Game | Opponent and assignment | Run | Result | Durable frames/s | Recovery log lower bound |
| ---: | --- | --- | --- | ---: | ---: |
| 1 | ZZZKBot, Stardust P1 | `20260920T044554-bab0b9ef80f8` | Win | 2,081.8 | 8 |
| 2 | ZZZKBot, Stardust P2 | `20260920T044600-7f7a5db65bbc` | Win | 2,088.1 | 8 |
| 3 | UAlbertaBot Terran, Stardust P1 | `20260920T044607-4cf98f929260` | Win | 2,065.9 | 8 |
| 4 | UAlbertaBot Terran, Stardust P2 | `20260920T044615-b257db5fec1a` | Win | 1,999.4 | 8 |

Every game exceeded the 384 durable frames/s threshold. Aggregate throughput was 55,967 logical frames / 27.176 seconds = 2,059.4 frames/s. This measures the frozen logging-engine package and is not a causal comparison with the rejected cohort.

The recovery logger is intentionally capped at eight lines per process. Each Stardust process reached that cap, so the cohort establishes a lower bound of at least eight recoveries per game and at least 32 total. The exact total may be higher. The defensive consumer path was never used.

## Replay compatibility

Every Stardust replay contained all three required evidence categories:

| Game | Probe trains | Building commands | Combat trains | Combat types |
| ---: | ---: | ---: | ---: | --- |
| 1 | 32 | 28 | 37 | Zealot, Dragoon, Corsair |
| 2 | 43 | 31 | 34 | Zealot, Dragoon, Corsair |
| 3 | 52 | 37 | 48 | Zealot, Dragoon |
| 4 | 40 | 23 | 37 | Zealot, Dragoon |

Observed buildings included Pylons, Gateways, Assimilators, Nexuses, Cybernetics Cores, Forges, Photon Cannons, and matchup-dependent technology buildings. No idle or wrong-race anomaly was found.

The terminal kill diagnostics followed the expected completed-game pattern in all four games: `controller_not_occupied_after_action` on the survivor after the peer was already defeated, and transport closure on the already-ended loser.

## Scope and retained evidence

Stardust won all four games, but this small compatibility cohort provides no finite Elo estimate, calibrated BASIL rating, or strength-promotion result. Passing establishes that the frozen repair completed this bounded cross-race cohort while exercising the repaired branch.

The manifest, raw logs, replays, and normalized command evidence are retained under `artifacts/experiments/stardust-repaired-cohort-v1/`; publishing was disabled as registered. The rejected original cohort remains preserved separately.
