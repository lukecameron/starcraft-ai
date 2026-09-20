# McRave per-search A* memoization shadow

Registered 2026-09-20T04:45:19Z, before compilation or execution. This is one diagnostic trial, not a gameplay or throughput acceptance test.

## Frozen inputs and question

Start from frozen A* candidate `ddc0415a3312bcfbc94f1e0efebe28e3ea1f5a4db739a7ae666567bc89b36c7f`. Run McRave as player 1 against UAlbertaBot Terran on Destination with engine seed 3001 and McRave bot seed 3001, using frozen diagnostic engine `27ea649cb3def9a724df077adaae3e62f16c9de8fbfbc9850ee485af5fbd88cb` from `artifacts/builds/27ea649cb3def9a724df077adaae3e62f16c9de8fbfbc9850ee485af5fbd88cb/openbw-kill-path-diagnostic` and a 120-second wall cap. This is the slow game-8 scenario from the rejected quick gate. Run once with no retry.

Question: for the real `generateAS` calls reached by this scenario, can each heuristic and walkability callback be evaluated at most once per valid tile per search without changing reachability, the bit representation of `double` distance, or the full ordered tile sequence?

## Candidate and isolation

The production A* remains authoritative for gameplay and alone mutates the production path object and `notReachable` cache. Before it runs, the diagnostic candidate executes against separate tile state and separate local heuristic/value/ready and walkability/value/ready arrays sized to the current map. Those arrays are newly constructed for each `generateAS` call, so no cached value survives a search, frame, unit, callback closure, or map. Candidate tile visitation uses a separate generation and backing array. Memory is bounded by the map tile count plus the fixed 65,536-entry candidate tile array.

On the first request for a valid tile in a search, the candidate calls the supplied callback and stores its value. Later requests for that tile reuse the value. This preserves the relative order of first callback evaluations, the eight-direction neighbor order, priority-queue operations, endpoint checks, `currentId` behavior, floating-point expressions and unreachable-cache behavior. Callback counts are expected to decrease and therefore are not an equivalence field.

The seven call families were source-reviewed before registration. The heuristic callbacks read only current-frame grid arrays, captured positions/scalars, and captured simulation-position vectors: air threat in flying retreat/regroup, transport air threat, ground threat in scout and ground-harass paths, and the flyer-harass distance/visibility calculation. The walkability callbacks are constant true or read BWEB walkability/used grids through the current `Path`. BWEB `Map::isWalkable`, `Map::isUsed`, and Grids getters only read arrays during these synchronous calls. No callback advances the engine, issues commands, logs, draws, mutates a captured value, or lazily populates state. Any contrary runtime/source evidence makes the trial INCONCLUSIVE rather than validating memoization.

The shadow writes `bwapi-data/write/as-memo-shadow-summary.json` atomically every 100 calls, at the first mismatch, and on `onEnd`. Two explicit invalid-endpoint probes run at startup. They test early-return equivalence but do not count as valid ground/flying policy coverage.

## Fixed decision rule

PASS requires all of the following in the last durable summary available before normal completion or the wall cap:

- at least 1,000 valid real-policy calls in total;
- at least one valid real-policy flying call and one valid real-policy ground call;
- both explicit invalid-endpoint probes recorded;
- zero reachability, bit-exact distance, or ordered-tile mismatches;
- memoized heuristic calls no greater than production heuristic calls, memoized walkability calls no greater than production walkability calls, and a strict reduction in their combined total;
- no crash, sanitizer/lifetime symptom, corrupt summary, or evidence that a callback is stateful during a search.

If the match completes, it must also have verified opposing terminal metadata and no `insync_hash_mismatch`; contradictory terminal metadata or a hash mismatch makes the trial INCONCLUSIVE regardless of local path comparisons.

A comparison mismatch is FAIL. Insufficient coverage, missing durable output, stateful callbacks, or instrumentation failure is INCONCLUSIVE. A wall timeout alone does not erase already durable same-call comparisons, but this trial cannot establish full-match performance or gameplay equivalence unless the match also completes normally. Results must report completion separately. No outcome permits a speedup, strength, rating, or production-adoption claim; it only decides whether this memoization deserves a separate production candidate and performance gate.

Amended 2026-09-20T04:46:18Z, still before compilation or execution, to replace the unresolved engine reference with the frozen diagnostic engine identity and to state the completed-match terminal-integrity condition. The candidate, scenario, coverage thresholds, comparison fields, decision categories, wall cap and no-retry rule are unchanged.
