# Kestrel v30 first-engagement diagnostic result

## Decision: INCONCLUSIVE; PREREGISTERED INTEGRITY GATES FAILED

The exact five-attempt diagnostic completed without retries or replacements. Four attempts produced reciprocal terminal losses, two hash-matched replay copies apiece, full `screp` parses and terminal diagnostic events. The UAlberta-Terran attempt is invalid: at engine frame 100,003 its launcher emitted `execute_action: unknown action 8`, neither side produced a terminal callback, and no replay was emitted. Its partial telemetry is preserved but excluded from classification.

The other four attempts also miss the literal preregistered replay-frame relation. Each parsed replay reports one frame less than its corresponding callback, while the plan registered replay frame equal to callback frame plus one. The observed relation is consistent across all eight replay copies, but the bar cannot be reversed after seeing results. The diagnostic therefore has no formally valid lane and cannot authorize a v31 policy change under its registered rule.

| Opponent / map | Attempt | Outcome | Callback frames | First registered threat | Second completion | Local / global completed at threat | First engagement | First home combat loss | Registered descriptive label |
| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | --- |
| ZZZKBot / Benzene | `20260920T145146-da87c3e53cd1` | verified loss | 5,459 | 3,796, Zergling | 3,677 | 1 / 1 | 3,798 | 3,947 | positional dispersion |
| UAlbertaBot-Terran / Destination | `20260920T145146-9fb0be7279a8` | invalid | 99,840 partial | 3,832, SCV | 5,069 | 0 / 0 | 4,181 | not observed | excluded |
| UAlbertaBot-Protoss / Heartbreak Ridge | `20260920T145146-557385fb25f2` | verified loss | 9,861 | 2,791, Probe | 4,361 | 0 / 0 | 3,949 | 6,809 | production timing, worker-scout confounded |
| McRave 9Pool / Circuit Breaker | `20260920T145146-f81dae62f736` | verified loss | 16,247 | 5,448, Zergling | 3,749 | 0 / 5 | 5,464 | 11,906 | positional dispersion; late conversion secondary |
| Stardust repaired / Benzene | `20260920T145146-16677ccebd1b` | verified loss | 10,419 | 2,988, Probe | 4,865 | 0 / 0 | 3,913 | 8,322 | production timing, worker-scout confounded |

## Descriptive observations

The trace demonstrates a measurement flaw in the registered first-threat heuristic: BWAPI reports worker types as attack-capable, so the first UAlberta-Protoss, UAlberta-Terran and Stardust threats are scouting workers rather than an attacking army. Their literal production-timing labels must not drive a gameplay change.

The two Zerg lanes show a repeated grouping signal, but it remains diagnostic. Against ZZZK, the first two Zealots completed at frames 3,125 and 3,677. Both accepted attacks on visible Zerglings before the 12-tile home trigger; the first Zealot died at frame 3,773 just outside the home radius, leaving one local defender when the trigger fired. Against McRave, five combat units were complete when the first Zergling crossed the home radius, but none was local; several were already following the same visible target from 620 to 1,909 pixels away. McRave also meets the descriptive late-conversion rule: no local combat loss for 6,458 frames after threat, maximum simultaneous completed army 15, then a loss.

A supplemental non-worker read of the 120-frame snapshots found at most one local defender at the first observed enemy-army entry in each completed lane: ZZZK 1/1 local/global at frame 3,796, UAlberta-Protoss 1/2 at frame 6,720, McRave 0/5 at frame 5,448, and Stardust 1/1 at frame 8,160. This supports further measurement of early squad staging, but the result does not satisfy the registered gate for selecting or advancing a policy candidate.

v30 is instrumentation-only. It is not adopted, does not enter Elo and does not replace canonical Kestrel v13. The invalid UAlberta attempt and the unexpected replay-frame relation remain preserved; no attempt was rerun.

## Identity and preservation

- Plan SHA-256: `3e5593cd9db2e560a5511ca62a5043efc2cc6fd4b261c32953d9711fe43793e8`.
- Schedule SHA-256: `8e1455510e4ef027867602436d43995d442e434922680dcb0715aeff73334a68`.
- Manifest SHA-256: `eb5ad4e4788986f2ec1906bc3243ea0913a6f2df5e0c663633791f818d2d24fd`.
- Scorecard SHA-256: `53894ae0febd6ad92bc80463d6b8018fe3ee1b5ab0fa31885dfe7a70c162b18a`.
- Candidate binary SHA-256: `2fe8d4868a8957a634d0d33629632c590cf2198d1a7985f0b1966a2c9b812476`.
- Candidate source SHA-256: `c90ab2992e3f8017edb6b52a84e5fa99d9d146f5851d71eb6390a11f43944645`.
- Patch SHA-256: `afba2070e1b423fac6f354cfc233215ebd9b7babb9e42f7bc03935fde8da9504`.
- Diagnostic trace SHA-256 values in schedule order: `26e79cb52b3687a7bb7dd70900aa48656f9be6f0d3cb97133e9b1d3a15144e31`, `efbf5cf967751af018643ff7cd635d4fc5f96acb51708a77bdc24e658f230bc6`, `1e54f80f59f8a396e375a902037d643cbbeb3dd451869fe3036cdddafb3f563a`, `645fe8c923196ff5cb2b46330035221255b6ca43ebd9e508fbdb4d5a785f3bf6`, `fa549154d787fca0041d0e7956ab45dffed3688f5a7b8d430d98f19f1174a89a`.

All manifests, logs, partial write state, diagnostic JSONL files and available replay copies remain preserved locally.
