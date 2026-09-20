# McRave same-state goal-cache shadow result

The corrected diagnostic run `20260920T034508-c3b3abeca73e` completed normally at frame 20,680 in 66.36 seconds. Both processes exited with code 0, terminal metadata agreed on the winner, and both replay files were archived. The validation module was binary `d2dccfc2b4ade19f9d72889d16e1401160f7fdb78ce18eab2962e6ac8a8d1be8`, built from isolated evaluation patch `b248db0d0078f635d964542603dc665ac2098069ccad85fb5fd655e9230a1e60` with the 114-translation-unit official-header check passing.

Across 5,780 real non-flyer goal-assignment calls and 2,124 actual selections, the original repeated-distance shadow, cached-distance shadow, and unchanged original gameplay path produced the same ordered unit sequence. There were zero divergences. This supports behavioral equivalence for the small states observed in this game.

The preregistered coverage condition failed. The largest invocation had three initially eligible units, and the largest requested count was two; the requirement was at least 20 eligible units with at least 10 requested. Both shadows therefore made 5,625 ground-distance calls. The game never exercised the repeated-distance large-army case found by profiling, so it supplies no direct bottleneck-reduction evidence and does not complete the intended equivalence validation.

Recorded nanosecond counters include shadow bookkeeping, linear selected-vector checks, and diagnostic overhead. The per-call summary was rewritten through a temporary file and rename, without an `fsync` durability claim. These timings are not production throughput and are not used for a speed conclusion.

Run `20260920T034342-41a758b6eb77` was launched just before pre-launch review feedback arrived and was immediately interrupted. It is preserved as an aborted attempt and excluded from the result. The corrected implementation adds the nonpositive-count return, retains only the first full divergence, and atomically replaces complete summary files.

The evidence condition is insufficient. No production source changed, and there is no strength or promotion conclusion.
