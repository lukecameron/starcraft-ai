# McRave A* bounds/index shadow v1

## Registration

- Experiment: `mcrave-as-bounds-shadow-v1`
- Registered: `2026-09-20T04:21:44.742588Z`
- Status: preregistered; no build or trial launched

## Question and hypothesis

Can `BWEB::Path::generateAS` snapshot immutable map dimensions once per invocation and use direct neighbor bounds/index arithmetic while returning exactly the production result? The hypothesis is that all shadow and production calls have identical reachability, bit-exact distance, full ordered tile sequence, and callback invocation counts, while the candidate replaces repeated BWAPI map-dimension queries and `TilePosition::isValid` neighbor checks with two additional map-dimension queries per admitted candidate search. Endpoint `isValid()` remains unchanged in both paths and is outside that two-query scope. Any mismatch falsifies equivalence.

This is a semantics and source-work diagnostic. It cannot support a strength claim, and the instrumented run's wall time/FPS cannot support a performance claim.

## Frozen trial

Run one 120-second match, with no retry, using the frozen McRave module source identity `98df26327cba498ac6ea1759d00b748f63870c655b34ecad6e24eb0e6851f1df` plus only diagnostic shadow instrumentation, the diagnostic-only engine package rooted at `artifacts/builds/27ea649cb3def9a724df077adaae3e62f16c9de8fbfbc9850ee485af5fbd88cb/openbw-kill-path-diagnostic`, UAlbertaBot Terran `75ac4f6bb44ed6e48fbee883638c77df9557c9a88070ceca4de11183053238c9`, Destination, engine seed 3001, McRave seed 3001, McRave player 1, and UAlbertaBot player 2. The engine differs from `f1a32e5a3dc64b8c62a17788488d36594dd95b13ef124637795b5aca4c846c42` only by kill-source logging and does not change game semantics. The production A* result alone continues into gameplay.

This engine substitution was registered before build or data collection at `2026-09-20T04:23:50.261448000Z`, after the diagnostic package became available. It preserves additional failure evidence if the historical outcome issue recurs.

## Shadow protocol

Immediately before each production `generateAS` call, run the candidate on identical source, target, unit type, reverse flag, callbacks, and the read-only pre-call `notReachable` decision. The candidate uses independent node storage and never mutates production `currentId`, `tileData`, `notReachable`, or the `Path`. Run production afterward without restoring or changing any of its normal post-call state. Compare reachability, IEEE-754 distance bits, every ordered tile, and heuristic/walkability callback counts. Current callbacks are read-only during synchronous path generation; a callback-count mismatch or any stateful callback makes the trial invalid.

Source review covers every current A* callback: `Block.cpp` uses only captured geometry and `Map::isWalkable`; `Transports.cpp` reads threat grids; `Scouts.cpp` reads the threat grid and `newPath.unitWalkable`; `Navigation.cpp` retreat/regroup read the air-threat grid, ground harass reads ground threat and `unitWalkable`, and flying harass reads captured scalar/vector state plus visibility; none mutates bot or engine state. `Grids::onFrame` finishes before Support, Scouts, Combat, Workers, and Transports invoke path generation, and no callback advances a frame.

At game start, issue two diagnostic-only invalid-endpoint calls through the same instrumented production API. Invalid calls return before production cache/node mutation and provide explicit invalid-source and invalid-target coverage. They do not feed a path to policy.

Record total calls; all and valid-endpoint flying and ground calls by unit type; reachable, failed, invalid, and cache-short-circuit calls; mismatches and first mismatch detail; production map-width query count and neighbor-validity calls; candidate map-width/map-height query counts and direct bounds checks. Flush an incremental summary at least every 100 calls and on end.

## Acceptance and stopping

Stop after the one registered game. The result is `PASS` only if the completed diagnostic contains at least 1,000 calls, at least one valid-endpoint flying policy call, at least one valid-endpoint ground policy call, both invalid probes, and zero mismatches. Reachable and failed/cache-short-circuit coverage are reported separately; absence of a naturally failed valid-endpoint call is a coverage limitation, not grounds for a retry. Missing required coverage, incomplete summary, evidence of a stateful callback, crash, timeout, or conflicting terminal metadata is `INCONCLUSIVE`. Callback-count divergence is an equivalence mismatch and therefore `FAIL`, as is any reachability, distance, or ordered-tile mismatch. A `FAIL` blocks the optimization.

If equivalence passes, source-work reduction is reported from counters only. Global trajectory, FPS, CPU, and outcome are descriptive because shadow execution adds work and exact seeded trajectories are not globally repeatable.
