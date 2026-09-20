# Kestrel v19 lone-Zealot hold result

## Decision: REJECT

The combat hold improved the registered local-overlap metric on both maps: the candidate reached two simultaneously completed local Zealots before first loss, while both matched controls reached one. The candidate therefore supports the diagnostic hypothesis that a lone first Zealot was being lost sequentially. However, the Heartbreak candidate accepted only three Zealot trains and no structure after the first train, missing two preregistered production gates. Both candidates still lost to ZZZK, so v19 is not adopted.

| Pair | Arm / run | first Zealot complete | accepted trains | max local overlap | first threat / first local loss | Probes / Gateways / Zealots | post-first-train structures |
|---|---|---:|---:|---:|---|---|---:|
| Benzene 6209 | Control `20260920T085433-cbff9e0a7b4f` | 3173 | 4 | 1 | 3815 / 3994 | 11 / 2 / 3 | 0 |
| Benzene 6209 | Candidate `20260920T085436-52a12a1434c3` | 3251 | 4 | **2 (pass)** | 3700 / 3925 | 10 / 2 / 3 | **1 (pass)** |
| Heartbreak 6210 | Candidate `20260920T085438-f221c4eb11cc` | 3119 | **3 (fail)** | **2 (pass)** | 3537 / 3842 | 10 / 2 / 3 | **0 (fail)** |
| Heartbreak 6210 | Control `20260920T085439-aaa7195953b6` | 3119 | 4 | 1 | 3724 / 3950 | 10 / 2 / 2 | 0 |

The candidate held the first Zealot at home until a second completed Zealot existed, without changing construction or target selection. The primary overlap gate passed on both maps and the candidate was no worse than its matched controls. The Heartbreak production miss is retained as a real outcome rather than waived. A follow-up may test whether reserving minerals until four accepted Zealot trains preserves the overlap gain; it must keep the same preregistered production bar.

All four games were valid infrastructure outcomes: reciprocal terminal callbacks, zero launcher exits, LF3, no `insync_hash_mismatch`, zero rejected commands, zero gas-worker construction attempts, zero build `Unit_Busy` errors, and no missing Zealot-loss positions. All eight replay copies passed SHA-256, frame, race and `screp` parsing checks. Durable throughput was 3,085.7, 3,006.4, 3,740.7 and 3,830.9 logical frames/s, all above the 384-frame/s floor.

## Identity and preservation

- Control source SHA-256: `e6965f441748a3d1cd9c181e0ef9ecfa128819c774390dadeae1e66ddc2362e0`; binary: `f44605e64582c1827f46c419cbd906e0ffec4500e9fb4c1da08d61b2624b6999`.
- Candidate source SHA-256: `8994f313e679125395c360657b41c8559659db260f47a854c0c4ac98dfb87230`; binary: `f02db8b97e01482f897a0f481c11a92f0cd5bc21f4629abea1f5a6d113b44b9a`.
- Candidate patch: `patches/kestrel-v19-lone-zealot-hold.patch`, SHA-256 `16ecf951bbcccb41786e72ae050f5c0c011cd53242c6804c4f0b2dac8ef85b83`.
- Frozen schedule: `schedule.json`, SHA-256 `baa141cdc76350ffc51cc25b0ee3910bd546a6810d3607f4fdf0e5917e12c941`.
- Paired ledger: `artifacts/experiments/kestrel-opening-v19/paired-ledger.json`.

V19 is not adopted and does not advance to held-out comparison because the Heartbreak production gates failed. Canonical Kestrel remains the accepted v13 construction-correctness baseline. All run manifests and replay files remain under the local artifact store.
