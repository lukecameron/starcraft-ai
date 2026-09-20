# McRave ground-path regeneration diagnosis result

**PASS for diagnostic adequacy and next-shadow selection.** The single registered trial recorded 1,884,058 path checks and 94,425 actual generations. Support generated 24,676 JPS paths, of which 23,795 (96.43%) were unreachable. This observed category exceeds the preregistered 20% and 100-generation threshold. It selects a narrow Support unreachable-result shadow; it does not validate a production cache.

## Trial integrity

Runner session `17454`, run `20260920T060444-344951b48e0f`, completed normally in 103.791 seconds at McRave frame 25,733. Both launchers returned 0, metadata was opposing, `outcome_verified` was true, both replays were archived, and neither stderr contains `insync_hash_mismatch` or a crash signature. The final atomic summary has SHA-256 `5507d0e9956b16bdce16929de7d8a41c6dda8186c3ad86ca9311aaf23ea7396a`.

| Family | Attempts | Generated | Unreachable | Unreachable/generated |
|---|---:|---:|---:|---:|
| Combat march | 813,822 | 36,180 | 8,301 | 22.94% |
| Combat retreat | 813,822 | 33,569 | 256 | 0.76% |
| Support | 256,414 | 24,676 | 23,795 | 96.43% |

Combat already reuses exact endpoint paths on 777,642 march checks and 780,253 retreat checks. Its generated work is largely associated with endpoint changes: the aggregate recorded 4,325 march and 1,713 retreat target-only changes, plus about 31,856 both-endpoint changes in each family. The aggregate cannot attribute every generation to a single endpoint-change bucket because those buckets include all attempts, so no stronger causal count is claimed.

Support's source explains the repeated-work candidate. `Support::updatePath` reuses a prior path only when its tile vector is nonempty and its target equals the requested target. `BWEB::Path::generateJPS` leaves the vector empty when it cannot find a route. An eligible Support unit therefore retries after an unreachable result even when its endpoints may be unchanged. The trial observed 25 Support units, 23,795 failed generations, 121,082 checks with an empty prior path, and 158,319 exact-endpoint reuse checks. The current aggregate does not cross-tabulate exact endpoints with generation outcomes, so it establishes the scale of failed Support generation but not the exact count of identical consecutive failures.

The next bounded shadow should cover Support only. It should record per-unit consecutive unreachable calls and compare current JPS output against reusing an unreachable result only when source, target, and the complete Support walkability predicate output are unchanged. The predicate includes enemy territory, edge/center constraints, and the unit-dependent center distance; checking only endpoints or using a time-to-live would change behavior when map state changes. Production must remain authoritative, with equality on reachability, distance, and ordered tiles. This is the smallest route to a semantics-preserving decision from the observed hotspot.

The diagnostic adds map queries and file writes and is not a throughput measurement. The result does not establish strength, speed, or adoption.
