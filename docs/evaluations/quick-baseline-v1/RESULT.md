# First controlled quick baseline: INCONCLUSIVE

Completed 2026-09-20. Seven of ten registered games met the completion criterion. The operational-reference adoption threshold was ten of ten, so this build is not adopted. No strategic improvement or absolute ladder rating is established.

The frozen McRave package produced six clean wins and one clean loss. One ZZZKBot process crashed inside the OpenBW socket teardown after both clients reported opposing final results; that game remains a failure. Two games against UAlbertaBot Terran reached the registered 120-second wall cap and were terminated. They produced no replay, and their manifests and logs remain archived. No trials were replaced.

| Game | Opponent | Map | Candidate position | Result | Frames | Durable seconds | Frames/s |
| --- | --- | --- | ---: | --- | ---: | ---: | ---: |
| 1 | ZZZKBot Zerg | Benzene | 1 | Win | 16,247 | 35.704 | 455.1 |
| 2 | ZZZKBot Zerg | Benzene | 2 | Win | 16,154 | 31.416 | 514.2 |
| 3 | ZZZKBot Zerg | Destination | 1 | Loss | 6,141 | 5.805 | 1,058.0 |
| 4 | ZZZKBot Zerg | Destination | 2 | Peer engine crash | 9,799 | 14.249 | 687.7 |
| 5 | UAlbertaBot Protoss | Benzene | 1 | Win | 18,975 | 61.532 | 308.4 |
| 6 | UAlbertaBot Protoss | Destination | 2 | Win | 15,875 | 44.117 | 359.8 |
| 7 | UAlbertaBot Protoss | Benzene | 2 | Win | 17,146 | 51.653 | 332.0 |
| 8 | UAlbertaBot Terran | Destination | 1 | Timeout | 22,800* | 120.072 | 189.9* |
| 9 | UAlbertaBot Terran | Benzene | 1 | Win | 18,727 | 56.941 | 328.9 |
| 10 | UAlbertaBot Terran | Destination | 2 | Timeout | 24,240* | 120.067 | 201.9* |

*Timeout frames come from the last periodic candidate diagnostic and may lag actual simulation progress. Other rows use the maximum terminal callback frame across clients. Each client includes its own engine and bot; the two games in flight may contend for local resources.

## Conditional matchup estimates

| Opponent | Clean wins / games | Nominal Wilson 95% win interval | Relative Elo estimate | Transformed interval |
| --- | ---: | --- | --- | --- |
| ZZZKBot Zerg | 2 / 3 | 20.8%–93.9% | +120 | −233 to +473 |
| UAlbertaBot Protoss | 3 / 3 | 43.9%–100% | +∞ | −43 to +∞ |
| UAlbertaBot Terran | 1 / 1 | 20.7%–100% | +∞ | −234 to +∞ |

These estimates condition on clean completion and a very small selected cohort. Two Terran timeouts make its clean-game rate especially unrepresentative. Related opponent race configurations and paired starts limit independence. Infinite point estimates at all-win endpoints indicate insufficient evidence, not unlimited strength. There is no pooled Elo and no conversion to BASIL Elo.

## Performance and next decision

Batch wall time was 323.2 seconds. Total frames divided by summed per-game durable time was **380.5 frames/s for clean games** (15.85×), and **306.7 frames/s across all attempts** (12.78×, subject to timeout frame sampling). The slowest completed game was 308.4 frames/s. This cohort fails the 384 frames/s target; earlier faster smoke games did not predict the cross-race cost.

The candidate-plus-engine process peaked below 467 MiB in this batch. During the two timeouts it consumed about 115 user CPU seconds, versus about 14 for the opposing UAlbertaBot process. That identifies the candidate/engine process as the profiling priority; it does not yet separate engine cost from policy cost. The last candidate snapshots contain 58–60 Drones and 29–95 Zerglings, substantially larger armies than the initial smoke games.

Repair and verify the engine shutdown lifetime first, then profile the slow scenarios using a separately identified instrumented build. Any new engine or policy comparison requires a new plan and experiment ID. The loss on Destination remains strategic evidence to inspect after reliability and runtime are understood.

## Audit trail

Raw evidence is under `artifacts/experiments/quick-mcrave-crashfix-baseline-v1/` with per-game manifests and all emitted replays referenced there. Source, patch, module, map, AI configuration, engine libraries and scenario identity were frozen in those manifests. The schedule SHA-256 is `e35ef47093d5a6a3c62b1d2c09356017843f2a6a1d5ab2f0471c9456c34e157a`.

The running batch loaded an earlier classifier that labeled every nonzero runner exit `launcher_failure`. After collection, `manifest.collected.json` preserves that original ledger byte-for-byte; `manifest.json` records an explicit analysis amendment deriving game 4 as `crash` and games 8 and 10 as `timeout` from unchanged raw manifests. Scores, attempted games and the infrastructure stop rule are unchanged. The classifier now checks the specific termination evidence first, with regression coverage.

The exact source patches for this collection are retained in Git as `patches/mcrave-baseline-v1.patch` and `patches/openbw-baseline-v1.patch`. The active build scripts use the newer canonical patches; do not substitute those when reconstructing this historical regime.
