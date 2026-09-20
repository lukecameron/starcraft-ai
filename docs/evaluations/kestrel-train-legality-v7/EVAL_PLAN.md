# Kestrel v7 train-legality probe plan

- Registered: `2026-09-20T06:32:20Z`, before any Kestrel v7 game was launched.
- Observed problem: v6b target persistence reduced attack rejection to one of 169 attempts, but train calls accounted for 636 of 637 total rejections. BWAPI attributed them to `Unit_Busy` and `Insufficient_Supply`. The policy checked minerals, gas, and `isTraining()` but omitted public commandability and supply legality.
- Change: call standard public `Unit::canTrain(type)` immediately before each Nexus or Gateway `train(type)` request. The policy still polls its normal six-frame-or-latency cadence, keeps the same worker cap and unit priorities, and issues training on the first eligible poll. No opening, target, construction, or combat decision changes.
- Candidate: frozen Kestrel v7 SHA-256 `2facbf970d4a4fd131564d3d02cd3966bcadc50e13e08256a1a92d3886013d3e`; combined source identity `34f43843f762ed32c7052eda64e324db8fe6b4204dd48f94692d84df5d2b18f1`.
- Engine: adopted terminal-drain package SHA-256 `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`. This differs from v6b's historical diagnostic engine, so trajectory and rate comparisons are not causal; public error attribution supplies an absolute correctness gate.
- Fixed serial schedule after the current calibration window: Kestrel Protoss player 1 versus ZZZK Zerg on Benzene seed `6103`, then UAlbertaBot Terran on Destination seed `6104`; LF3, empty learning state, 120 seconds, one attempt each, no retries.
- Infrastructure/lifecycle guard: zero launcher exits, opposing callbacks, no state-hash mismatch, two parsed replays, at least 384 durable frames/s, at least eight probes, a pylon, a gateway, a zealot or dragoon, scouting and post-production combat, and no wrong-race production in both games.
- Production-intent guard: every game contains accepted probe and combat-unit train commands and lifetime maxima consistent with continued economy and army production. Polling that suppresses production fails regardless of rejection count.
- Primary gate: zero rejected train commands attributed to `Unit_Busy` or `Insufficient_Supply`, and below 5% rejected commands overall in each game. Any other train error fails pending source review.
- Target-persistence guard: attack rejection remains below 5% with nonzero post-production attack attempts.
- Decision: passing makes v7 the initial command-clean baseline and ends command-cleanup work. The next experiment addresses early Zerg defense. Outcomes remain descriptive and do not estimate Elo.
