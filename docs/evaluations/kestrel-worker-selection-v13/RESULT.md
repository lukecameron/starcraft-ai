# Kestrel v13 gas-worker construction guard result

## Decision: PASS for baseline-adoption review

V13 passed every registered correctness, exercised-path, lifecycle, and production gate. This result supports review of the narrow worker-selection fix for the Kestrel baseline. It does not automatically replace canonical v7 and does not establish playing-strength improvement.

Batch session `12179` ran exactly the two fixed games once:

| Run | Opponent / map / seed | Outcome | Gas guards | Gas-worker build attempts | Build `Unit_Busy` | Total rejection | FPS |
|---|---|---:|---:|---:|---:|---:|---:|
| `20260920T073627-856dcb721664` | ZZZK Zerg / Benzene / 6103 | loss | 1 | 0 | 0 | 2/56 (3.57%) | 2,953.2 |
| `20260920T073629-a6ad5ae88993` | UAlbertaBot Terran / Destination / 6104 | loss | 7 | 0 | 0 | 36/1,055 (3.41%) | 1,633.1 |

The exercised-path requirement passed. On Benzene, the guard excluded worker 61 at frame 3,612 with public order 83 (`HarvestGas`) during general `availableProbe` selection. On Destination it excluded worker 131 seven times during construction selection, with gas-cycle orders 81–84 (`MoveToGas`, `WaitForGas`, `HarvestGas`, and `ReturnGas`) at frames 3,810, 4,632, 5,190, 5,862, 6,834, 7,632, and 8,754. This directly exercises BWAPI's documented `isGatheringGas()` range, including travel, waiting, harvesting, and return.

No build command in either game selected a worker reporting gas gathering, and the build-specific counter recorded zero `Unit_Busy` errors. The two rejected Benzene build requests had another error category and remain within the registered total-rejection ceiling. Destination's 36 rejected commands were gather requests; none were build requests. Both games remained below 5% total rejection.

## Lifecycle and production

Both games completed with reciprocal callbacks, zero launcher exits, LF3, no state-hash mismatch, and both player replay copies parsed fully. The archived player-1 replay SHA-256 values are `db4a8455c6f5df2c02e8391b24da2fc66533e6b40527e563fc5d88a10ed2967f` and `08a20076c179ab500340e56692537f2543de2174436a78a6774715297d93d756`.

- ZZZK game: maxima 16 Probes, 2 Pylons, 1 Gateway, 1 Zealot; 16 accepted train and 6 accepted attack commands.
- UAlberta game: maxima 28 Probes, 5 Pylons, 4 Gateways, 5 Zealots, 10 Dragoons; 109 accepted train and 769 accepted attack commands.

Both games therefore continued economy and army production, produced the required Protoss structures and combat units, issued scouting/combat actions, and showed no wrong-race production. Both throughput measurements exceeded 384 logical frames/s. The two losses are descriptive and do not alter the correctness decision.

## Frozen identity

- Registered: `2026-09-20T07:31:43.646449+00:00`
- Module SHA-256: `622bca47b47f78f3e9d1971d1e340f991b54ced7f3bfdfd932d3062e125cbd98`
- Combined source SHA-256: `12cecdb5039569711c318bab5bb6781b4f1e86e22c87e453f9d85c295fa13df0`
- V7-to-V13 patch SHA-256: `8fd24ff479bc5a8794f0ae092855082b1a44270123fe8cc1810ee1493996177b`
- Batch manifest: `artifacts/experiments/kestrel-worker-selection-v13/manifest.json`
- Frozen package: `artifacts/builds/622bca47b47f78f3e9d1971d1e340f991b54ced7f3bfdfd932d3062e125cbd98/kestrel-v13-gas-worker-guard/`

Lead decision, 20 September 2026: ADOPT as the development baseline. Source review confirmed the exclusion covers cached and fresh construction-worker selection; the lead independently recomputed guard/error counts from both final manifests. Canonical source now matches the frozen v13 package byte-for-byte. The two losses remain descriptive and no playing-strength promotion is claimed.
