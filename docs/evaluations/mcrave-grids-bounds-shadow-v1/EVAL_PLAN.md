# McRave Grids walk-bounds same-input shadow

Registered 2026-09-20T07:28:57Z, before build or gameplay.

## Change and frozen trial

Build an isolated diagnostic module from frozen McRave 9Pool candidate `fd174fa451c5c79af53b84d882f983630536c31fe116d22b76495cd1610cacfa`. At the existing `Grids::addToGrids` walk-circle check, evaluate the current `WalkPosition::isValid()` result and a shadow predicate using public map dimensions cached by `Grids::onStart`: `x >= 0 && y >= 0 && x < mapWidth * 4 && y < mapHeight * 4`. Record checks and disagreements, but retain the existing `isValid()` result as the sole gameplay decision. No other policy or path behavior changes.

At `onStart`, also compare the predicates on fixed non-gameplay sentinel positions: negative x, negative y, origin, the final valid map corner, one-past x, one-past y, one-past both, and BWAPI's invalid walk-position sentinel. These pure queries must not alter gameplay. Persist an atomic summary every 100,000 gameplay checks, on the first disagreement, and at `onEnd`.

Compile the native module and all official-header object translation units with at most four jobs. Freeze the exact full source patch, incremental instrumentation patch, module, build inputs, and hashes before launch.

Run exactly one match on `sscai/(2)Destination.scx`: frozen UAlbertaBot `75ac4f6bb44ed6e48fbee883638c77df9557c9a88070ceca4de11183053238c9` as player 1 Zerg and the shadow McRave as player 2 Zerg, with frozen engine `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`, engine seed 9202, McRave bot seed 9202, empty per-player learning state, and a 120-second wall cap. Use escalated local execution for the OpenBW socket. Run no concurrent game, build, replay playback, or profiler. Do not retry.

## Decision rule

PASS requires a clean complete match with opposing terminal metadata, both launcher return codes zero, both replay copies archived, no hash mismatch/crash/unreviewed kill source, at least 100,000 exact gameplay-input comparisons, zero gameplay disagreements, all eight sentinel comparisons recorded, and zero sentinel disagreements. Any disagreement is FAIL. Incomplete coverage, timeout, startup failure, missing terminal summary, or unrelated integrity failure is INCONCLUSIVE. Preserve every artifact.

This evaluates predicate equivalence only. A pass supports review of a production replacement at this single call site; it does not establish a speedup, clear the 384-fps engineering floor, or justify changing the separate visibility scan.
