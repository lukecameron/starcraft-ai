# McRave post-cache profile v1 result

## Outcome

The single registered trial produced a valid 10-second sample. The hypothesis is supported for this sampled state: the prior goal-distance search was not dominant, and BWEB path generation was present in at least 1,732 of 7,843 main-thread samples (22.08%), above the registered 20% hotspot threshold. This diagnostic controls no adoption decision and provides no speed or strength claim.

The largest source path was flying-unit navigation. The conservative BWEB count combines mutually exclusive top-level caller branches visible in the sample: Combat Navigation 1,372, Scouts 310, Support 43, and Workers 7. It deliberately omits smaller or ambiguous BWEB frames. Combat as a whole accounted for 1,561 samples (19.90%), Combat Navigation for 1,384 (17.65%), Grids for 1,383 (17.63%), and Scouts for 863 (11.00%). These are inclusive categories and can overlap, so they must not be summed as exclusive shares.

The old goal subsystem appeared in 20 samples (0.26%); its `BWEB::Map::getGroundDistance` child appeared in 19 (0.24%). Visual work appeared in 10 inclusive `McRave::Visuals::onFrame` samples (0.13%); this is an upper bound for the registered visual-only definition because the parent can include bookkeeping around drawing. Five leaf samples were in `BWAPI::Game::drawTextScreen`. Visual work is well below the 20% materiality threshold.

## Registered execution

The trial was launched once as run `20260920T041522-64a197b0b35f`, matching the registered frozen configuration:

- McRave player 1 module SHA-256 `98df26327cba498ac6ea1759d00b748f63870c655b34ecad6e24eb0e6851f1df`, Zerg, bot seed 3001;
- UAlbertaBot player 2 module SHA-256 `75ac4f6bb44ed6e48fbee883638c77df9557c9a88070ceca4de11183053238c9`, Terran, no bot seed;
- engine identity `f1a32e5a3dc64b8c62a17788488d36594dd95b13ef124637795b5aca4c846c42`;
- Destination, scenario seed 3001, 120-second wall cap.

The exact player-1 launcher PID was 55089. Polling first observed the threshold crossed at frame 10,080. macOS `sample` then captured that PID for 10 seconds at a 1 ms interval and produced 7,843 main-thread samples. The sample SHA-256 is `1621d4ad359c7749bbb241bd8ab08b3680e095c6aa08c5abba88766fd2558611`.

The match completed with verified reciprocal results and return codes 0/0. McRave won at its local frame 20,060; UAlbertaBot reported loss at frame 20,029. Harness elapsed time was 66.800 seconds and durable completion time was 66.801 seconds. Player 1 consumed 62.403 user CPU seconds and 0.810 system CPU seconds, with peak RSS 487,243,776 bytes. The player-1 and player-2 replay SHA-256 values are respectively `f01a307af10c1feaee11530b446dbba3e47ea9fd26705293e26fd0ad0ed8e6e0` and `88abaad1e27765e34ea1c99fb4aa93461eb4205366c0246c26af13418b6b0286`.

## Evidence and limitations

The authoritative run manifest is `artifacts/runs/20260920T041522-64a197b0b35f/game-0001/manifest.json`. Raw profiling evidence is under `artifacts/experiments/mcrave-post-cache-profile-v1/raw/`: `player1.sample.txt`, the live manifests captured at PID discovery and immediately before sampling, PID/frame records, runner logs, the final manifest copy, and `analysis.json` with the arithmetic.

This is one sampled interval in one uncontrolled global trajectory. Sampling and 100 ms polling add overhead. Inclusive stacks identify where the main thread was observed, not causal speedup from a hypothetical change. The BWEB aggregate is a conservative source-subsystem grouping across disjoint callers, while other listed categories overlap it. The result motivates a narrowly measured investigation of repeated flying-navigation path generation; it does not establish that caching or reducing those paths is correct, safe, or beneficial.
