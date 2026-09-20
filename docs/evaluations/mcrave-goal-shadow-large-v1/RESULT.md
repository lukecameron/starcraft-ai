# McRave large-state goal-cache shadow result

The one registered attempt, run `20260920T035048-f48d925aaecb`, selected the forced `HatchPool11Hatch3HatchMuta` opening and reached 156 zerglings. It ran to the 180.07-second diagnostic wall limit at frame 27,360. Both processes were terminated by the harness, so there is no terminal winner or replay; the partial result and all write-state evidence were preserved.

The correctness and coverage gate passed. Across 53,828 real non-flyer goal-assignment calls and 352,160 actual selections, the original repeated-distance shadow, invocation-cache shadow, and unchanged original gameplay path produced identical ordered unit sequences. There were zero divergences. The first qualifying call occurred at frame 24,499 with 48 eligible units and 10 requested assignments. The maximum recorded call, at frame 27,351, had 154 eligible units and requested 22.

The first qualifying call made 435 ground-distance calls under repeated selection and 48 with invocation caching. Across the whole run, repeated selection made 15,122,188 distance calls and caching made 1,243,302: 91.78% fewer, or a 12.16-fold reduction. This directly confirms the profiled repeated-distance work in actual large-army states.

The module was `3b75098fa1b7460faad21d6f2a678c7d9fad09e2faaaddd87716a948606481ce`, built from combined isolated patch `a68ec51f93456d91ed20d5852abf3e0c83d599390f9ddf88fea7175dea5a3de4`. The only incremental selector patch was `b35865f0affcfa09135f1e93fec893d8325bae0459cc54e04e7f79ca08cfec50`; official-header compilation passed all 114 translation units.

The measured shadow nanoseconds include duplicate algorithms, linear selected-vector checks, serialization, and per-call summary replacement. The game's 151.94 logical frames per second is diagnostic overhead, not production throughput. Forcing an existing opening deliberately changed the trajectory. This result supports behavioral equivalence and distance-work reduction for observed live states; it makes no strategy, strength, production-speed, or promotion claim.
