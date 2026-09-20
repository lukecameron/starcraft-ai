# Kestrel v18 explicit-second-Pylon result

## Decision: REJECT

The explicit branch successfully produced two Pylons in both candidate games, but it delayed the second Gateway and reduced the opening army. The candidate reached only one simultaneously completed local Zealot before its first local loss on both maps, accepted only three Zealot trains, and missed the primary overlap and production gates.

| Pair | Arm / run | first Pylon accepted / complete | max Pylons | second Gateway current / complete | accepted trains | max local overlap | first threat / first local loss | Probes / Zealots | post-first-train structures |
|---|---|---:|---:|---|---:|---:|---|---|---:|
| Benzene 6207 | Control `20260920T084922-60bf4709edc0` | 810 / 1405 | 1 | 2168 / 3139 | 6 | 1 | 3865 / 4023 | 11 / 3 | 0 |
| Benzene 6207 | Candidate `20260920T084924-75fdc2cf10ea` | 828 / 1419 | **2** | **2928 / 3899** | **3 (fail)** | **1 (fail)** | 3660 / 3818 | **9 (fail)** / 2 | 1 |
| Heartbreak 6208 | Candidate `20260920T084926-a4a4fdb19a67` | 804 / 1411 | **2** | **2439 / 3410** | **3 (fail)** | **1 (fail)** | 3540 / 3655 | **9 (fail)** / 2 | **0 (fail)** |
| Heartbreak 6208 | Control `20260920T084927-08b14c1a56b2` | 804 / 1408 | 1 | 2146 / 3117 | 4 | 1 | 3688 / 3897 | 10 / 2 | 0 |

The explicit second-Pylon request worked as intended, but the new build occupied the construction path before the second Gateway and shifted its completion 271 frames later on Benzene and 293 frames later on Heartbreak relative to the controls. The extra supply did not produce a second local defender in time. Both candidate games lost to ZZZK.

All four games were valid infrastructure outcomes: reciprocal terminal callbacks, zero launcher exits, LF3, no `insync_hash_mismatch`, zero rejected commands, zero gas-worker construction attempts, zero build `Unit_Busy` errors, and no missing Zealot-loss positions. All eight replay copies passed SHA-256, frame, race and `screp` parsing checks. Durable throughput was 3,156.1, 3,215.5, 3,718.8 and 3,815.7 logical frames/s, all above the 384-frame/s floor.

## Identity and preservation

- Control source SHA-256: `7d0033408a9931a98b7130fd0fde086b57a0ac3b0060ace87663a1d33af8c769`; binary: `b7319c6e7f50958b831ca993262487b4eddbd18595da88c459c21ad11be35ce4`.
- Candidate source SHA-256: `4c9e71f2c3a62f1e1d5fc5a6676fa445e7744e133d89cb9029c1004ed54105e3`; binary: `7e1dab45d0c42eca1f352788c14f4c5de55d68e0dc704cfaf6d6534169a7e21f`.
- Candidate patch: `patches/kestrel-v18-explicit-second-pylon.patch`, SHA-256 `b3a19b3fd9eb8bd1868a3d08ba31e2ac82f2c9926a0b771bb454b8815d85cff7`.
- Frozen schedule: `schedule.json`, SHA-256 `056252448273581c4367c2526079477d8e5811e6aa49d66d85d27165c4eaf0c7`.
- Paired ledger: `artifacts/experiments/kestrel-opening-v18/paired-ledger.json`.

V18 is not adopted and does not advance to held-out comparison. Canonical Kestrel remains the accepted v13 construction-correctness baseline. All run manifests and replay files remain under the local artifact store.
