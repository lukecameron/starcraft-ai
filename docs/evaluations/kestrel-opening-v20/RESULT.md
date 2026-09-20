# Kestrel v20 four-Zealot reserve result

## Decision: REJECT

Reserving 100 minerals after ten Probes until four accepted Zealot trains did not repair the v19 production miss. The candidate reached four trains on Benzene but only three on Heartbreak and recorded no post-first-train structure on either map. The local-overlap metric was two in both candidate games, but the matched v20 controls also reached two on these seeds, so no strength improvement is established.

| Pair | Arm / run | accepted trains | max local overlap | first threat / first local loss | Probes / Gateways / Zealots | post-first-train structures |
|---|---|---:|---:|---|---|---:|
| Benzene 6211 | Control `20260920T090006-d0139a7c27da` | 4 | 2 | 3693 / 3937 | 11 / 2 / 3 | 1 |
| Benzene 6211 | Candidate `20260920T090008-7d8e1f9660cc` | 4 | 2 | 3691 / 3835 | 10 / 2 / 3 | **0 (fail)** |
| Heartbreak 6212 | Candidate `20260920T090010-558eb105f3b8` | **3 (fail)** | 2 | 3617 / 3798 | 10 / 2 / 3 | **0 (fail)** |
| Heartbreak 6212 | Control `20260920T090011-4f24663671b4` | 3 | 2 | 3543 / 3855 | 10 / 2 / 3 | 0 |

The mineral reserve did not materially change Probe counts or guarantee a fourth train. The v19 hold remains the clearest mechanism signal, but it is not a validated strength improvement and remains outside the canonical baseline.

All four games were valid infrastructure outcomes: reciprocal terminal callbacks, zero launcher exits, LF3, no `insync_hash_mismatch`, zero rejected commands, zero gas-worker construction attempts, zero build `Unit_Busy` errors, and no missing Zealot-loss positions. All eight replay copies passed SHA-256, frame, race and `screp` parsing checks. Durable throughput was 3,072.1, 3,133.2, 3,784.8 and 3,624.5 logical frames/s, all above the 384-frame/s floor.

## Identity and preservation

- Control source SHA-256: `8994f313e679125395c360657b41c8559659db260f47a854c0c4ac98dfb87230`; binary: `f02db8b97e01482f897a0f481c11a92f0cd5bc21f4629abea1f5a6d113b44b9a`.
- Candidate source SHA-256: `52fac23540e49f704f3899bb56361d56afc5c458aa596020aaa09dc69b675290`; binary: `1f00a92f537bfa3e8b0e468faff07d1f5114b0420417b55b097eccdcfa04a09d`.
- Candidate patch: `patches/kestrel-v20-four-zealot-reserve.patch`, SHA-256 `1e702ecc361f1f5011b0e600aa33e7396cf569c7c432fcdc81459219eeb61614`.
- Frozen schedule: `schedule.json`, SHA-256 `a2c61c76920ec4f704e5e2d2091cf4aaa6e01e93e02926c4caa15377b7751ada`.
- Paired ledger: `artifacts/experiments/kestrel-opening-v20/paired-ledger.json`.

V20 is not adopted and does not advance to held-out comparison. Canonical Kestrel remains the accepted v13 construction-correctness baseline. All run manifests and replay files remain under the local artifact store.
