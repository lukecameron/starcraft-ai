# Stardust native-port cohort compatibility result

## Outcome: REJECT

The registered engineering gate failed. Three of four games completed cleanly, while game 1 crashed the Stardust launcher with `SIGSEGV` at frame 7,920. The requirement was four clean completions, so the port is not yet a reliable cohort benchmark. No game was retried.

The completed games all exceeded the 384 durable frames/s threshold. Their rates were 2,099.2, 2,066.3, and 1,743.1 frames/s. Across all attempts, including the crash, the descriptive aggregate was 51,162 frames / 25.636 seconds = 1,995.7 frames/s; across clean games it was 43,192 / 22.147 = 1,950.2 frames/s. These characterize the frozen logging-engine package and do not override the clean-completion failure.

## Compatibility evidence

All four available replay views contained Stardust worker production, building production, and combat-unit production commands:

| Game | Result | Probe trains | Build commands | Combat trains | Observed combat types |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | Crash | 20 | 16 | 8 | Zealot, Dragoon |
| 2 | Win | 41 | 30 | 34 | Zealot, Dragoon, Corsair |
| 3 | Win | 52 | 29 | 37 | Zealot, Dragoon |
| 4 | Win | 54 | 37 | 51 | Zealot, Dragoon, Shuttle |

Building commands included normal Protoss structures such as Pylons, Gateways, Assimilators, Nexuses, Cybernetics Cores, and production/technology buildings. No idle or wrong-race anomaly was observed. Game 1's only archived replay came from its ZZZK peer because Stardust crashed, but that synchronized replay still contains Stardust's commands through the failure.

Games 2–4 had zero launcher return codes, verified opposing winner callbacks, and no `insync_hash_mismatch`. Their first diagnostic kill paths followed the expected terminal pattern: `transport_callback` on the already-ended loser and `controller_not_occupied_after_action` on the survivor. Game 1 had no in-sync mismatch in the surviving peer; Stardust exited with code -11, and ZZZK then observed `transport_callback` and won by disconnect.

## Crash evidence

The macOS crash report records `EXC_BAD_ACCESS`/`SIGSEGV` on Stardust's main thread. The symbolized stack begins in `MiningOptimization::PatchOccupiedForecast::PatchOccupiedForecast`, called by `MiningOptimization::optimizeStartOfMining`, `Workers::issueOrders`, and `StardustAIModule::onFrame`. Stardust's own log shows normal play through frame 7,920, including worker/building/combat production; its diagnostic result remained `ended: false` and `winner: null`.

The crash report is preserved as `artifacts/experiments/quick-stardust-cohort-v1/game-0001-BWAPILauncher-crash.ips` with SHA-256 `27772235d3fa0ec161f811c294c347581937e8eb96f18abf56a98c474ae8fcc0`. Normalized replay and diagnostic evidence is in `compatibility-analysis.json`. The batch manifest, every runner log, all available replays, and the failed attempt remain preserved.

## Scope

The three scored games were all Stardust wins, which is descriptive coarse ordering only. This sample provides no finite Elo estimate, absolute BASIL rating, or strength-promotion evidence. The next engineering step is to reproduce and diagnose the `PatchOccupiedForecast` invalid-access path in an isolated Stardust build before another fixed compatibility schedule.

The configured publisher completed successfully at [deployment `79c24d22`](https://79c24d22.starcraft-ai.pages.dev).
