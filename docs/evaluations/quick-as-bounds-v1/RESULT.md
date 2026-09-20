# McRave A* bounds throughput result

Decision: **REJECT**. All ten scheduled games completed with verified opposing results, zero process failures and no `insync_hash_mismatch`, but six games missed the registered 384 durable logical frames/s minimum. The aggregate also missed it: 177,133 frames / 473.703 durable seconds = **373.9 frames/s**. The preregistered gate requires every game and the aggregate to pass, so the production candidate is not accepted on this evidence and no game was rerun.

| Game | Opponent | Map | Candidate slot | Result | Frames | Durable seconds | Frames/s |
| --- | --- | --- | ---: | --- | ---: | ---: | ---: |
| 1 | ZZZKBot Zerg | Benzene | 1 | win | 13,829 | 22.516 | 614.2 |
| 2 | ZZZKBot Zerg | Benzene | 2 | win | 16,123 | 26.064 | 618.6 |
| 3 | ZZZKBot Zerg | Destination | 1 | win | 16,123 | 27.706 | 581.9 |
| 4 | ZZZKBot Zerg | Destination | 2 | win | 16,092 | 29.795 | 540.1 |
| 5 | UAlbertaBot Protoss | Benzene | 1 | win | 17,518 | 45.880 | **381.8** |
| 6 | UAlbertaBot Protoss | Destination | 2 | win | 17,394 | 48.733 | **356.9** |
| 7 | UAlbertaBot Protoss | Benzene | 2 | win | 17,921 | 52.769 | **339.6** |
| 8 | UAlbertaBot Terran | Destination | 1 | win | 24,586 | 104.504 | **235.3** |
| 9 | UAlbertaBot Terran | Benzene | 1 | win | 19,068 | 57.104 | **333.9** |
| 10 | UAlbertaBot Terran | Destination | 2 | win | 18,479 | 58.632 | **315.2** |

Batch collection took 265.101 seconds with concurrency two. That wall time is operational context; the registered aggregate uses summed durable game times so concurrency cannot inflate it. The measurement includes both launchers, bots, engines, initialization, logging, and archive completion.

## Integrity and artifacts

Both clients exited zero in every game and each pair reported exactly one winner and one loser. The diagnostic engine recorded the same ordinary terminal pattern in all ten games: the winning client removed the defeated peer through `controller_not_occupied_after_action` after action 87 (`Leave Game`), while the defeated client recorded `transport_callback`. There was no opposing-winner callback and no `insync_hash_mismatch` in any client stderr. These observations support the manifests' verified outcomes; they do not generalize engine correctness beyond this cohort.

All 20 replay files were copied successfully with SHA-256 hashes and sizes in their match manifests, totaling 13,610,191 bytes. The launcher did not perform replay playback validation, so emission and hashing establish durable archival rather than semantic replay validity. The authoritative aggregate ledger is `artifacts/experiments/quick-mcrave-as-bounds-v1/manifest.json`; its ten `match_manifest` entries point to the raw logs, metadata and replay records. It remains unchanged.

Candidate-plus-engine CPU was 437.927 seconds across the ten games (20.290–97.296 seconds per game; median 44.103). Opponent-plus-engine CPU totaled 63.001 seconds. Candidate-plus-engine peak RSS ranged from 484,278,272 to 492,290,048 bytes (median 487,522,304; peak 469.5 MiB). These process measurements include OpenBW and cannot be attributed to McRave alone. Ordinary desktop background activity was not controlled.

## Interpretation and next investigation

The 10–0 result is descriptive only. Against ZZZKBot the 4/4 Wilson 95% interval is 51.0–100%; against each UAlberta race the 3/3 interval is 43.9–100%. The opponent-relative Elo point estimates are infinite at an observed 100% and are not ratings. This fixed cohort is neither a held-out strength test nor evidence that the A* change caused the wins.

The next bounded performance investigation should target repeated per-search callback work in `generateAS`, beginning with the slowest valid scenario, game 8 (Destination, UAlbertaBot Terran, seed 3001). The earlier profile placed BWEB path generation on at least 22.08% of samples, while the equivalence shadow counted 569,614,483 heuristic and 1,125,903,804 walkability callbacks. The evaluated candidate only removed repeated dimension/index queries; it did not reduce those callback counts. A preregistered same-input shadow of per-search memoization for the current read-only heuristic and walkability callbacks, requiring identical reachability, distance and ordered tiles, is therefore the highest-value next check. No optimization or strength claim follows from this batch.
