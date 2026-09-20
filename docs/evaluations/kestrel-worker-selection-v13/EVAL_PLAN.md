# Kestrel v13 gas-worker construction guard plan

- Registered: `2026-09-20T07:31:43.646449+00:00`, before compilation or execution.
- Evidence: the retained v12 worker diagnostic reproduced Pylon build failures at frames 3,738 and 3,744 from worker 137 while its public order was `HarvestGas`; both returned `Unit_Busy`. The failure was stale `builderId_` reuse after the pending timer, not a same-cadence gather command.
- Hypothesis: excluding Probes for which public `Unit::isGatheringGas()` is true from both stale-builder reuse and generic `availableProbe()` selection prevents construction attempts from gas workers and removes build `Unit_Busy` errors while preserving production. BWAPI documents `isGatheringGas()` as covering travel to, waiting for, harvesting inside, and returning from a refinery.
- Candidate: isolated v13 from canonical accepted v7. It does not include v12's rejected mineral reservation. For a generic building, a retained builder reporting `isGatheringGas()` is discarded and selection continues through `availableProbe()`; `availableProbe()` skips gas workers, so the same rule covers normal buildings and Assimilator construction. Supply, production order, pending/retry timing, economy, scouting, combat, and all other strategy remain v7.
- Verification telemetry: `gas_worker_guard_events` counts public gas workers excluded from construction selection; `gas_worker_build_attempts` counts attempted builds whose selected worker reports gas gathering. Each guard event records frame, worker ID, order ID, and whether it occurred during stale-builder reuse or general selection.
- Frozen source identity: combined source SHA-256 `12cecdb5039569711c318bab5bb6781b4f1e86e22c87e453f9d85c295fa13df0`; v7-to-v13 patch SHA-256 `8fd24ff479bc5a8794f0ae092855082b1a44270123fe8cc1810ee1493996177b`. Build identity will be appended before launch.

## Fixed execution

Exactly two serial games using the original v7 probe inputs: Kestrel v13 Protoss as player 1 versus frozen ZZZK Zerg on Benzene seed `6103`, then frozen UAlbertaBot Terran on Destination seed `6104`. Use the adopted current engine, LF3, empty isolated learning state, 120-second cap, one attempt per row, no retries or replacements. Preserve every outcome.

## Gates

- Exercised path: across the two games, at least one gas worker must be excluded by the new guard with frame and order evidence. If no guard event occurs, validation is `INCONCLUSIVE` even if no build error occurs.
- Primary correctness: `gas_worker_build_attempts == 0`, zero build requests rejected with `Unit_Busy`, and below 5% rejected commands overall in each game.
- Lifecycle: both games must have zero launcher exits, reciprocal callbacks, no state-hash mismatch, fully parsed replay pairs, and at least 384 durable logical frames/s.
- Production: each game must continue Probe and combat-unit training; reach at least eight Probes, a Pylon, a Gateway, and a Zealot or Dragoon; issue scouting and post-production combat commands; and show no wrong-race production.
- Decision: `PASS` means this narrow correctness fix is eligible for baseline-adoption review. Any failed correctness/production bar is `REJECT`; missing exercised-path evidence or infrastructure-invalid evidence is `INCONCLUSIVE`. Outcomes are descriptive and no result establishes strength.

- Prebuild telemetry amendment `2026-09-20T07:32:56.778079000Z`: `issue()` now records `build_unit_busy_rejections` only when the rejected category is build and the immediately captured BWAPI error is `Unit_Busy`. Policy and registered gates are unchanged.

- Build identity recorded before launch at `2026-09-20T07:35:46+00:00`: module SHA-256 `622bca47b47f78f3e9d1971d1e340f991b54ced7f3bfdfd932d3062e125cbd98`; native and official-header targets passed.
