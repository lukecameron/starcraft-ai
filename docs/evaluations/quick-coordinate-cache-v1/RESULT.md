# Coordinate repair and goal-cache quick result

Decision: **INCONCLUSIVE**. Nine of ten games had verified opposing results: eight wins and one loss. All ten launcher pairs exited zero and emitted two replay files, but the last game reported two winners and remains unscored. No crash or wall timeout occurred. The registered ten-clean-game and per-match throughput requirements were not met; the frozen reference is unchanged.

The all-attempt throughput was 403.0 logical frames/s (16.79 times the 24-fps convention), and clean games averaged 410.2 frames/s. The slowest game was 322.5 frames/s; five games fell below 384. The aggregate passes its threshold but cannot hide the failed slow-tail bar. Candidate-plus-engine process RSS peaked at 489,062,400 bytes (466.4 MiB), excluding the opponent process and not representing isolated bot memory. Batch collection took 223.4 seconds before dashboard publication.

| Game | Opponent | Map | Candidate slot | Result | Frames | Durable seconds | Frames/s |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |
| 1 | ZZZKBot Zerg | (2)Benzene | 1 | win | 16,185 | 30.888 | 524.0 |
| 2 | ZZZKBot Zerg | (2)Benzene | 2 | win | 16,123 | 29.930 | 538.7 |
| 3 | ZZZKBot Zerg | (2)Destination | 1 | loss | 6,885 | 6.461 | 1065.6 |
| 4 | ZZZKBot Zerg | (2)Destination | 2 | win | 16,123 | 33.115 | 486.9 |
| 5 | UAlbertaBot Protoss | (2)Benzene | 1 | win | 16,867 | 45.681 | 369.2 |
| 6 | UAlbertaBot Protoss | (2)Destination | 2 | win | 16,247 | 44.925 | 361.6 |
| 7 | UAlbertaBot Protoss | (2)Benzene | 2 | win | 16,247 | 38.207 | 425.2 |
| 8 | UAlbertaBot Terran | (2)Destination | 1 | win | 19,812 | 61.425 | 322.5 |
| 9 | UAlbertaBot Terran | (2)Benzene | 1 | win | 21,827 | 66.028 | 330.6 |
| 10 | UAlbertaBot Terran | (2)Destination | 2 | Metadata conflict | 18,665 | 52.699 | 354.2 |

## Outcome integrity

Game 10, run `20260920T035743-5518317f90cd`, ended with UAlbertaBot reporting winner=true at frame 18,665 and McRave reporting winner=true at frame 18,634. Both processes exited zero with empty stderr. McRave's final diagnostics showed one drone and no hatcheries or zerglings, but those counts are diagnostic evidence, not an authorized substitute for the contradictory winner callbacks. The game remains unscored while the engine outcome path is investigated.

The collected batch manifest is retained verbatim as `manifest.collected.json`, SHA-256 `49d56f1005eac28a997f76ef4b450736b33d90d07ce979c1ffac05c3224a56c5`. Its original `launcher_failure` category hid the more specific reason for run_match's nonzero exit. An explicit analysis amendment changes only this failure subtype to `missing_or_inconsistent_metadata`; raw match manifests, scores, schedules and stopping behavior remain unchanged. The classifier regression was reproduced against the actual record and corrected with nine focused batch tests passing.

## Strength and performance interpretation

ZZZKBot: 3 wins/1 loss, 95% Wilson win interval 30.1–95.4%, uncalibrated relative Elo +190.8 with transformed interval −146.7 to +528.4. UAlbertaBot Protoss: 3/3, interval 43.9–100%; Terran: 2/2 verified plus one metadata failure, interval 34.2–100%. All-win samples have infinite point estimates and do not establish an absolute rating. These are descriptive opponent-specific results, conditional on verified completion. They are not a calibrated BASIL rating or a causal improvement over the first batch, which used a different engine and RNG regime.

The cache already passed same-state large-call selection validation, and the station repair already produced a legal build at its corrected coordinate. Those local findings remain valid, but they do not satisfy this broader acceptance gate. Temporary replay-verification browser tabs were closed during the batch after games 1–7 completed. This was an ordinary desktop workload, not a claim of an otherwise idle-machine benchmark; no speed difference is attributed to a particular change.

Next resolve the conflicting terminal outcome, then profile the slowest verified case (Destination vs UAlbertaBot Terran, game 8) and target its remaining cost. Retain candidate `98df26327cba498ac6ea1759d00b748f63870c655b34ecad6e24eb0e6851f1df` as an unadopted engineering build.
