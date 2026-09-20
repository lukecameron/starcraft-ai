# Kestrel v17 supply-buffer result

## Decision: REJECT

Widening the ordinary supply-Pylon trigger from a four-supply margin to six did not change the relevant construction path. The candidate still built only one Pylon in both games, accepted no structure after its first Zealot train, and reached only one simultaneously completed local Zealot before its first local loss. The candidate did not meet the primary overlap gate or the post-first-train structure gate.

| Pair | Arm / run | first Pylon accepted / current / complete | first Gateway complete | accepted trains | max local overlap | first threat / first local loss | Probes / Gateways / Zealots | post-first-train structures |
|---|---|---:|---:|---:|---:|---|---|---:|
| Benzene 6205 | Control `20260920T084337-eb5d53849d66` | 828 / 865 / 1386 | 2710 | 4 | **1** | 3852 / 4037 | 11 / 2 / 3 | **0 (fail)** |
| Benzene 6205 | Candidate `20260920T084339-c8fc4ee37fde` | 810 / 880 / 1401 | 2473 | 4 | **1 (fail)** | 3868 / 4428 | 11 / 2 / 3 | **0 (fail)** |
| Heartbreak 6206 | Candidate `20260920T084341-e7d34e7bcb6b` | 864 / 933 / 1454 | 2505 | 4 | **1 (fail)** | 3815 / 4284 | **9 (fail)** / 2 / 3 | **0 (fail)** |
| Heartbreak 6206 | Control `20260920T084342-429930b76944` | 864 / 961 / 1482 | 2557 | 3 | **1** | 3691 / 3790 | 10 / 2 / 2 | **0** |

The candidate’s first Pylon timing was effectively unchanged from its v16 control and no second Pylon appeared. The supply-buffer threshold therefore did not reach the intended state before the opening fight. Both candidate games lost to ZZZK.

All four games were valid infrastructure outcomes: reciprocal terminal callbacks, zero launcher exits, LF3, no `insync_hash_mismatch`, zero rejected commands, zero gas-worker construction attempts, zero build `Unit_Busy` errors, and no missing Zealot-loss positions. All eight replay copies passed SHA-256, frame, race and `screp` parsing checks. Durable throughput was 3,110.9, 3,125.2, 3,847.0 and 3,869.7 logical frames/s, all above the 384-frame/s floor.

## Identity and preservation

- Control source SHA-256: `e6965f441748a3d1cd9c181e0ef9ecfa128819c774390dadeae1e66ddc2362e0`; binary: `f44605e64582c1827f46c419cbd906e0ffec4500e9fb4c1da08d61b2624b6999`.
- Candidate source SHA-256: `7d0033408a9931a98b7130fd0fde086b57a0ac3b0060ace87663a1d33af8c769`; binary: `b7319c6e7f50958b831ca993262487b4eddbd18595da88c459c21ad11be35ce4`.
- Candidate patch: `patches/kestrel-v17-supply-buffer.patch`, SHA-256 `03510ab3c5525b1e37bedc4fe764ebf237089af69717a73ac7ce6caabd43a091`.
- Frozen schedule: `schedule.json`, SHA-256 `86d37c987dff25e19ad707bba99ca263c8f01a866a11fddd2c11a93ef0121b5d`.
- Paired ledger: `artifacts/experiments/kestrel-opening-v17/paired-ledger.json`.

V17 is not adopted and does not advance to held-out comparison. Canonical Kestrel remains the accepted v13 construction-correctness baseline. All run manifests and replay files remain under the local artifact store.
