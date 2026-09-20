# McRave Support JPS per-search memoization shadow

Registered 2026-09-20T06:08:40Z, before compilation or execution.

## Evidence and question

The preceding registered diagnosis observed 24,676 Support `generateJPS` calls, 23,795 of which returned unreachable. Source review shows that `Path::generateJPS` forces source and target walkable, then may reject a pair through its frame-local `notReachable` set before invoking JPS. The aggregate did not distinguish those cheap rejections from full graph searches.

Question: among actual Support JPS searches, can the pure walkability predicate be evaluated once per coordinate per search while preserving the exact path result, and does this remove enough repeated predicate work to justify a production candidate?

## Frozen trial and shadow

Start from frozen memo candidate `04521befa41bb3873783b215493abf3a071414d2a5315cdea68fc7a67f4415ec`. Run exactly one diagnostic as player 1 Zerg against UAlbertaBot Terran on Destination, engine seed and McRave bot seed 3001, frozen engine `27ea649cb3def9a724df077adaae3e62f16c9de8fbfbc9850ee485af5fbd88cb`, and a 120-second cap. Do not retry.

For each Support call that currently reaches `generateJPS`, run a separate memoized shadow immediately before the unmodified production search. Both see the same pre-call frame-local unreachable cache; the shadow does not mutate it. The shadow preserves the JPS algorithm, bounds behavior, source/target special cases, first predicate-call order, path construction, and floating-point distance operations. It stores only the boolean result of the supplied predicate by coordinate for that search, then discards the storage. Production alone sets the unit path and mutates the unreachable cache.

The Support predicate is source-reviewed as read-only during a synchronous call: it reads enemy territory, tile validity, fixed map dimensions and center, and a captured `centerDist`. It issues no command and mutates no captured or global state. Compare reachability, bit-exact distance, and the full ordered tile vector. Record raw predicate calls, memo predicate requests/evaluations, failed calls with and without predicate work, and separate failed-search callback totals. Nanosecond totals are diagnostic only: shadow-first execution warms caches and the instrumented binary is not a production throughput measurement.

## Decision rule

PASS requires at least 1,000 compared Support calls, at least 100 failed calls that actually invoke the predicate, zero output mismatches, memo evaluations no greater than raw predicate calls, and at least a 20% aggregate reduction in predicate evaluations among actual searches. A completed match must also have opposing terminal metadata, zero crashes, and no `insync_hash_mismatch`.

An output mismatch is FAIL. Insufficient coverage, evidence that the callback is stateful, corrupt output, or terminal-integrity failure is INCONCLUSIVE. Report frame-local early rejections separately so they are not presented as expensive searches. A PASS only permits an isolated production candidate followed by official-header compilation and a separate fair performance gate; it does not establish speed, strength, or adoption.

Amended 2026-09-20T06:11:06Z, before compilation or execution, because the preceding instrumented match took 103.8 seconds and this shadow performs an additional JPS search. Reaching the 120-second cap does not erase already durable same-call comparisons if all numerical coverage and equivalence bars above are met, but it makes full-match integrity and performance INCONCLUSIVE and must be reported separately. The one-attempt rule, cap, scenario, comparison fields, zero-mismatch bar, callback-reduction bar, and all coverage thresholds are unchanged.
