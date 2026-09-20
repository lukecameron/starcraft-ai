# Kestrel v15 two-Gateway overlap result

## Decision: REJECT

V15 created two Gateways and four accepted Zealot trains in both candidate games, but never produced two simultaneously completed local Zealots before the first local Zealot died. The registered primary gate failed on both maps. Canonical V13 remains unchanged.

| Pair | Arm / run | second Gate current / complete | accepted trains | max local overlap | first threat / first local loss | Probe / Gate / Zealot maxima | post-first-train structures |
|---|---|---|---:|---:|---|---|---:|
| Benzene 6201 | Control `20260920T080538-e35c25c645dc` | absent | 3 | 1 | 3,703 / 3,864 | 13 / 1 / 2 | 2 |
| Benzene 6201 | Candidate `20260920T080551-1efd13ce87a9` | 2,462 / 3,433 | 4 | **1 (fail)** | 3,689 / 3,859 | 12 / 2 / 3 | 1 |
| Heartbreak 6202 | Candidate `20260920T080605-421e6f8cfebe` | 2,535 / 3,506 | 4 | **1 (fail)** | 3,615 / 3,987 | 11 / 2 / 3 | **0 (fail)** |
| Heartbreak 6202 | Control `20260920T080618-93e99ecac705` | 3,065 / 4,036 | 3 | 1 | 3,596 / 4,003 | 13 / 2 / 2 | 2 |

Candidate overlap equaled the controls but missed the absolute requirement of two on both maps. The second Gateway completed before the first local Zealot loss, yet the production timelines still yielded only one completed defender inside the home radius before that loss. Global maxima of three Zealots do not override the registered simultaneous local metric.

Both candidates reached two Gateways current, four accepted trains, at least two completed/current Zealots, and at least ten Probes. Benzene recorded one accepted structure after the first Zealot train; Heartbreak recorded none and independently failed that concrete production guard. Gas resumption was not established before terminal defeat and is not claimed.

All four games were clean losses: reciprocal callbacks, zero launcher exits, LF3, no state-hash mismatch, zero rejected commands, zero gas-worker build attempts, zero build `Unit_Busy`, and zero missing last-observed loss positions. All eight replay copies parsed fully. Durable throughput was 2,935.4, 3,099.3, 3,493.2, and 3,557.5 logical frames/s.

## Identity

- Corrected control module: `67413847356807ce6c9a8c69dd02d888ead1284a71ed94237c98c81d1c819dd5`
- Corrected candidate module: `42f3ea9c3218a2873803962d5437d4f5e313e4883eef6f89ca4a63d6a30713a2`
- Candidate source: `15c4963a13ff6c89b55d021e8b76b44761ba2c3f40275457ceba1788c6b64284`
- Candidate patch: `adfcdb7440028b39a38e4b7b8154b59c1411db895063e7841970f12ec955cafa`

The unrun pre-review modules remain preserved. This result rejects V15's narrow overlap hypothesis and does not select a replacement policy.
