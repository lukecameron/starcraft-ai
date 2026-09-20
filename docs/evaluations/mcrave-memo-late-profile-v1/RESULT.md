# McRave memoized A* late-game CPU profile result

**INCONCLUSIVE.** The retained timestamps cannot prove the requested ten seconds of live sampling. The sample report header is `2026-09-20T05:02:31.475Z`, while the target's match manifest records completion at `2026-09-20T05:02:40.585Z`, only 9.110 seconds later. The preregistration makes an incomplete requested duration inconclusive, so the useful branch counts below are partial diagnostic evidence and do not pass the evaluation.

## Capture integrity

The runner session was `75876`, run `20260920T050142-3662b2986e1a`, and the exact player-1 PID was `95545`. Durable McRave telemetry reported frame 15,120 before the one permitted command, `/usr/bin/sample 95545 10 1`. The command returned and emitted a full call graph, top-of-stack table, binary list, and 7,165 main-thread observations. Its header and the manifest completion time do not establish a complete ten-second live interval; the later `capture.json` timestamp was recorded after the command and is not evidence of its start time. The raw 845,271-byte report has SHA-256 `849538f82dbccb9ea295d48bc6bd2d912e010e2765381469a4ca7a17462ea657`.

The match result is separate from sample completeness. It completed in 57.718 seconds rather than timing out: McRave won at frame 19,998, both launchers returned 0, terminal metadata was opposing and `outcome_verified` was true, and both replays were archived. No `insync_hash_mismatch` or crash signature appears in the preserved logs.

## Main-thread accounting

The denominator is all 7,165 sampled main-thread stacks. The primary figures use mutually exclusive outermost `McRaveModule::onFrame()` call-site branches; descendants are not added to parents.

| Branch | Samples | Main thread |
|---|---:|---:|
| All McRave `onFrame` branches | 5,891 | 82.22% |
| Combat | 1,706 | 23.81% |
| Grids update | 1,351 | 18.86% |
| Support | 842 | 11.75% |

Within Combat, outer `BWEB::Path::generateAS_h` contexts account for 378 samples (5.28% of the main thread), leaving 1,328 samples (18.53%) as other Combat work. Another 20 `generateAS` samples occur under Scouts, making all observed `generateAS` contexts 398 samples (5.55%). These counts use only outer call contexts, so instruction-offset descendants are not counted repeatedly.

Combat Navigation accounts for 955 samples (13.33%). Ground march and retreat path call contexts account for 566 samples (7.90%) and resolve into `BWEB::Path::generateJPS`; Support is another 842-sample outer branch whose path update also enters `generateJPS`. Grids is reported as its direct 1,351-sample primary branch. Nested Grids calls from predicates belong to their enclosing Combat or Support primary branch and are intentionally not added to the Grids total.

The partial sample suggests a future source diagnostic should count why Combat ground march/retreat and Support paths are regenerated, including destination changes and path-validity failures, then test reuse only where the same inputs and map state make the existing path valid. It does not justify an implementation or strategy change.

This is one late-game, one-process sample on Destination. Sampling perturbs the process, inclusive nested hotspots overlap their parent branches, and the result does not measure full-match production throughput or strength.
