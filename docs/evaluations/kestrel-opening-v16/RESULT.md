# Kestrel v16 first-Pylon reservation result

## Decision: REJECT

The candidate requested and completed its first Pylon earlier on both maps, but the earlier reservation did not create the intended overlapping defense. The candidate reached only one simultaneously completed local Zealot before the first local loss in both games, while the matched controls reached two. The candidate also failed the registered production guards on Heartbreak Ridge: only three accepted Zealot trains and no accepted structure request after the first Zealot train.

| Pair | Arm / run | first Pylon accepted / current / complete | first Gateway complete | accepted trains | max local overlap | first threat / first local loss | Probes / Gateways / Zealots | post-first-train structures |
|---|---|---:|---:|---:|---:|---|---|---:|
| Benzene 6203 | Control `20260920T083339-02d992fff3d9` | 1056 / 1153 / 1674 | 2787 | 5 | **2** | 3805 / 4102 | 11 / 2 / 3 | 2 |
| Benzene 6203 | Candidate `20260920T083341-33df1273eb31` | **792 / 861 / 1382** | **2461** | 5 | **1 (fail)** | 3965 / 4159 | 10 / 2 / 3 | **0 (fail)** |
| Heartbreak 6204 | Candidate `20260920T083343-fde4d42b5ae3` | **804 / 852 / 1373** | **2434** | **3 (fail)** | **1 (fail)** | 3761 / 4346 | 10 / 2 / 2 | **0 (fail)** |
| Heartbreak 6204 | Control `20260920T083345-3668c7a9941b` | 996 / 1098 / 1619 | 2725 | 4 | **2** | 3646 / 4135 | 11 / 2 / 3 | 1 |

Both candidate games lost to ZZZK. The candidate’s first Pylon was accepted 264 frames earlier on Benzene and 192 frames earlier on Heartbreak, and its first Gateway completed 326 and 291 frames earlier respectively. That timing improvement did not survive the home-defense gate: the first candidate Zealot still died before a second local Zealot overlapped it. This is evidence against this reservation policy in the V15 opening stack; it does not prove that earlier Pylons are generally harmful.

All four games were valid infrastructure outcomes: reciprocal terminal callbacks, zero launcher exits, LF3, no `insync_hash_mismatch`, zero rejected commands, zero gas-worker construction attempts, zero build `Unit_Busy` errors, and no missing Zealot-loss positions. All eight replay copies passed SHA-256, frame, race and `screp` parsing checks. Durable throughput was 3,054.6, 3,190.7, 3,820.6 and 3,747.9 logical frames/s, all above the 384-frame/s floor.

## Identity and preservation

- Control source SHA-256: `0dd08d52e816e4a28fdb979b9cb35093301d54b54eacaa38279fa07e79bc5101`; binary: `42f3ea9c3218a2873803962d5437d4f5e313e4883eef6f89ca4a63d6a30713a2`.
- Candidate source SHA-256: `e6965f441748a3d1cd9c181e0ef9ecfa128819c774390dadeae1e66ddc2362e0`; binary: `f44605e64582c1827f46c419cbd906e0ffec4500e9fb4c1da08d61b2624b6999`.
- Candidate patch: `patches/kestrel-v16-first-pylon.patch`, SHA-256 `64a9059ad4a3445b1c301c005daf585423079e519fbcd5d688174b6633ed8f6d`.
- Frozen schedule: `schedule.json`, SHA-256 `aaa726cbbf45e57de9ff26a8575f909df7abce6af9dfe7bdc4358f29b4aac39d`.
- Paired ledger: `artifacts/experiments/kestrel-opening-v16/paired-ledger.json`.

V16 is not adopted and does not advance to held-out comparison. Canonical Kestrel remains the accepted v13 construction-correctness baseline. All run manifests and replay files remain under the local artifact store for later dashboard publication.
