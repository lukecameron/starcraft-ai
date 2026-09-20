# McRave Support JPS per-search memoization shadow result

**PASS.** All 16,773 Support comparisons matched on reachability, bit-exact distance, and the complete ordered tile vector. Fresh per-search memoization reduced predicate evaluations from 211,081,633 to 72,506,005, a 65.65% reduction, with zero output mismatches.

The trial also resolves the earlier uncertainty about cheap failure rejection. Of 16,246 failed calls, 16,220 invoked the predicate; only 26 failures avoided predicate work through the frame-local unreachable cache. Failed calls alone made 210,629,643 raw predicate calls versus 72,339,197 memo evaluations. The observed Support hotspot is real graph-search work rather than primarily an endpoint or cached-pair rejection.

## Integrity and timing scope

Runner session `39543`, run `20260920T061222-aea159a208bb`, completed in 62.656 seconds at McRave frame 18,603. Both launchers returned 0, metadata was opposing, `outcome_verified` was true, both replays were archived, and neither stderr contains `insync_hash_mismatch` or a crash signature. The final summary has SHA-256 `256ffeac6f3ce482d1e4a3b46ee94881499e55545a4df90203b34c296f06441c`.

The instrumented timers recorded 4.409 seconds in authoritative raw searches and 2.011 seconds in memoized shadows. This is supporting evidence only: the shadow ran first, both paths ran in one process, and the module performed twice the searches. It is not a production throughput comparison.

The justified production candidate is narrow: add an opt-in per-search boolean predicate cache inside `BWEB::Path::generateJPS`, and enable it only for the measured Support call. Allocate cache state fresh for each search, retain the existing boundary behavior and source/target special cases, and preserve first predicate-evaluation order. Other JPS callers remain on the existing path. The candidate still requires official-header compilation and a separately preregistered production performance gate; this result does not establish speed, strength, or adoption.
