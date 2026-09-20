# Kestrel v1 lifecycle probe plan

**Canceled before execution at `2026-09-20T06:04:40Z`.** Source review found that v1 still allowed `assignEconomy` to give the reserved builder a gather order while it was walking to place the building. No v1 match was launched. The preserved plan and binary identity remain the record of that untested candidate; v2 supersedes it without rewriting this gate.

- Registered: `2026-09-20T06:03:23Z`, before any Kestrel v1 match was launched.
- Observed problem: v0 repeatedly reissued accepted construction orders while its builder was traveling or placing, and the WorkerRush smoke ended before any combat unit was produced.
- Change: retain at most one pending building order for 240 frames or until the corresponding owned-unit count increases. Add lifetime maximum unit/building telemetry. No opening, targeting, or opponent-specific behavior changed.
- Question: does Kestrel v1 execute its intended economy, construction, production, scouting, and combat lifecycle in a complete standard-BWAPI game?
- Candidate: frozen `Kestrel.dylib` SHA-256 `dfbae9d3bbe7b6b1ab93911eee4c1bfa1a56887c0d3960ce3f2cd1c2e8b44fa4`; combined source identity `53dd044aca0a372582e0ceb8151f0729ca9b13a23b0284e406fa588532aa38eb`.
- Scenario: Kestrel Protoss as player 1 versus frozen UAlbertaBot Terran SHA-256 `75ac4f6bb44ed6e48fbee883638c77df9557c9a88070ceca4de11183053238c9` as player 2, Destination, engine seed `6102`, LF3, empty learning state, and a 120-second wall cap.
- Execution: one attempt after the lead grants a game window. Preserve every output; do not retry or substitute another seed after observing the result.
- Compatibility gate: both launchers exit zero, terminal callbacks are opposing, no state-hash mismatch occurs, and both replay files parse with `screp`.
- Behavior gate: telemetry or replay commands show at least eight probes, one pylon, one gateway, one zealot or dragoon, a scouting command outside the starting base, and a combat command after combat-unit production. There must be no wrong-race production. Repeated build commands must fall from v0's 55 total pylon/gateway attempts to at most 12. Missing or ambiguous evidence is inconclusive.
- Performance characterization: report whole-match durable throughput and Kestrel callback CPU/p99/max, without treating one trajectory as a representative suite.
- Decision: passing permits a short, separately preregistered matchup probe. A failed lifecycle condition returns to source diagnosis. The game result alone is not a strength or promotion claim.
