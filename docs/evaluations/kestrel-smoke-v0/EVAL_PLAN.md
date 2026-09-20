# Kestrel v0 native smoke plan

- Registered: `2026-09-20T05:56:41Z`, before any Kestrel match was launched.
- Question: can the original Kestrel Protoss policy complete a native OpenBW game through the standard BWAPI surface while demonstrating its economy, production, scouting, and combat lifecycle?
- Candidate: frozen `Kestrel.dylib` SHA-256 `a1cb8aa85489fdf57e046447be5af57c5132fd8d39f3b802547430b3e4d1f974`.
- Scenario: Kestrel Protoss as player 1 versus the frozen WorkerRush Zerg diagnostic fixture as player 2, Benzene, engine seed `6101`, LF3, empty learning state, 120-second wall cap.
- Execution: one attempt only after the lead grants the exclusive game window. Preserve all process results, logs, telemetry, and replays. Do not retry or substitute a seed after observing the outcome.
- Compatibility gate: both launchers exit zero, callbacks report opposing terminal outcomes, no state-hash mismatch appears, and both replay files parse.
- Behavior gate: replay or bot telemetry must show continued probe economy, at least one completed pylon and gateway, production of at least one zealot or dragoon, a scouting or combat movement/attack command beyond the starting base, and no wrong-race production. Missing or ambiguous replay visibility makes the behavior gate inconclusive.
- Performance characterization: report complete-match frames per second and Kestrel callback timing, but do not infer representative late-game throughput from this smoke.
- Decision: passing both gates permits a small preregistered opponent probe. Any crash, invalid replay, production stall, or missing lifecycle evidence sends the bot back to source diagnosis. A win or loss in this one game is not a strength claim.
