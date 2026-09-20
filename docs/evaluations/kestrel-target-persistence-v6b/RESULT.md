# Kestrel v6b target-persistence probe result

**Decision: reject v6b under the registered total-command gate. Attack-request rejection improved enough to retain target persistence as a candidate, but its registered responsiveness guard remains inconclusive. Public BWAPI error attribution found a separate production-command defect.**

Both games passed infrastructure and lifecycle guards: zero launcher exits, opposing callbacks, no state-hash mismatch, two `screp`-readable replays, plausible Protoss production and combat, and throughput above 384 frames per second. Kestrel lost both games; this is descriptive only.

| Opponent | Run | Frames | Durable frames/s | Unit maxima: probes / pylons / gateways / zealots / dragoons | Total rejected | Attack rejected | Train rejected |
| --- | --- | ---: | ---: | --- | ---: | ---: | ---: |
| ZZZKBot | `20260920T063024-a3ed1c2ff9ee` | 6,172 | 2,910.9 | 16 / 2 / 2 / 1 / 0 | 91 / 150 (60.7%) | 0 / 4 | 91 / 111 |
| UAlbertaBot Terran | `20260920T063038-89385dcfc1ed` | 12,651 | 3,178.5 | 28 / 5 / 4 / 8 / 6 | 546 / 831 (65.7%) | 1 / 165 | 545 / 598 |

The registered total rejected-command fraction below 20% failed in both games and regressed from v5. Error attribution makes the reason concrete: target persistence itself reduced attack rejection to 0% against ZZZK and 0.6% against UAlbertaBot, while training generated every ZZZK rejection and all but one Terran rejection. BWAPI reported 79 `Unit_Busy` and 12 `Insufficient_Supply` errors against ZZZK, and 545 `Insufficient_Supply` plus one `Unit_Busy` error against UAlbertaBot. Build and gather commands had zero rejection in both games.

Replay evidence is consistent with active combat rather than suppression by inactivity. Accepted `Attack1` commands fell from v5's 23 to three against ZZZK and from 349 to 162 against UAlbertaBot, while both games retained attack-move scouting and post-production combat. The replay does not expose enough visibility state to prove every registered target-transition deadline, so the responsiveness guard is inconclusive rather than silently passed.

The next bounded fix is independent of target persistence: call the standard public `Unit::canTrain(type)` legality predicate before issuing a train command. The current minerals/gas and `isTraining()` checks omit supply legality and do not reliably capture commandability in this OpenBW path. This should remove known busy/supply rejections without weakening the production policy; unit maxima and accepted replay training remain required in its evaluation.

Kestrel callback CPU/p99/max were 0.019095 seconds / 0.005 ms / 2.06983 ms against ZZZK and 0.052108 seconds / 0.006583 ms / 2.30133 ms against UAlbertaBot. Replay SHA-256 values are `e1ba9073bd54d490b3d316177f37fd9bd47a7a73d7fa2ec25457e80a555d2d31` and `c3108d1e5ad8dd4772776aed08cf7086b4f7f926dc5c95507de9daf41e89f18f` for ZZZK, and `83e03b469ef886ecb3dc95d5f2cbde2a3011ac2a6f5296f48f2492d25e48ddb7` and `724bb96e4aac25b72c5e660d346edc5a81f08f89567470f380cb7a4bb2821fd9` for UAlbertaBot.
