# McRave A* bounds/index shadow v1 result

## Decision

`PASS`. The one registered trial met every required coverage condition and produced zero equivalence mismatches. The dimension-snapshot optimization is eligible for a separate production candidate and measured evaluation. This result establishes equivalence for the observed calls; it does not establish a speed or strength improvement.

## Trial

Run `20260920T042625-18adf20f4372` used the registered Destination matchup, engine and bot seed 3001, diagnostic McRave player 1, and UAlbertaBot Terran player 2. The instrumented module SHA-256 was `4aecd9688a1daf10d764cb86f330c8e26dcf44557a461b66c80f09de28983942`; the diagnostic patch SHA-256 was `dd5c68f6a871bb28b8cbf13fbea72bfb0a63086148170b71af08a8c04ca8f99c`; and the engine package identity was `27ea649cb3def9a724df077adaae3e62f16c9de8fbfbc9850ee485af5fbd88cb`.

The match completed after 19,843 player-1 frames and 73.075 seconds through durable archival. Both processes exited 0 and reported reciprocal results; McRave won. Both replays were archived. These outcome and timing values are descriptive only because shadow execution roughly doubles A* work.

## Equivalence and coverage

The shadow compared 13,439 calls:

- 8,509 valid-endpoint flying policy calls;
- 4,928 valid-endpoint ground policy calls;
- two explicit invalid-endpoint probes;
- 13,437 reachable calls;
- zero valid-endpoint failed paths and zero unreachable-cache short circuits;
- zero reachability, distance-bit, ordered-tile, or callback-count mismatches.

Candidate and production callback totals matched exactly: 569,614,483 heuristic calls and 1,125,903,804 walkability calls each. The production path remained authoritative and alone mutated gameplay path and unreachable-cache state.

## Source-work counters

Across admitted searches, production performed 666,261,375 width queries through `oneDim` and 576,525,040 neighbor `TilePosition::isValid` calls. The candidate performed the same 576,525,040 neighbor bounds decisions with direct comparisons and made 26,874 additional dimension queries, exactly two for each of the 13,437 admitted searches. Endpoint `isValid()` checks remain unchanged and are outside this comparison.

These counters demonstrate that the proposed implementation removes repeated virtual map-dimension lookup from indexing and neighbor validation while preserving the observed algorithm outputs. They do not measure runtime savings; the shadow trial's CPU and wall time include both implementations.

## Evidence and limitations

The authoritative manifest is `artifacts/runs/20260920T042625-18adf20f4372/game-0001/manifest.json`. Durable copies of the terminal manifest and shadow summary are under `artifacts/experiments/mcrave-as-bounds-shadow-v1/results`. The summary SHA-256 is `d53ff1e8616aafc4bad736c6f9cdeb3a1dec9c1d193e786c42a29a514cd11269`.

No naturally failed valid-endpoint search or unreachable-cache short circuit occurred, so those paths lack real-game coverage. The invalid early-return path was covered explicitly. This was one game trajectory and cannot prove equivalence for arbitrary callback implementations; the current six callback families were separately source-reviewed as synchronous and read-only. Production adoption should retain the endpoint checks and eight-direction iteration, callback invocation order, queue ordering, floating-point operations, and unreachable-cache behavior exactly.
