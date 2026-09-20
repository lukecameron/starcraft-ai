# Kestrel v29 build-commandability repair result

## Decision: REJECT CANDIDATE; THROUGHPUT GATE FAILED

All five registered attempts reached reciprocal terminal losses with hash-matched, fully parsed replays. The candidate recorded zero gas-worker build attempts, zero rejected build commands and a 0.48% cohort rejection rate: 17 rejected gather commands from 3,569 attempted commands. Four games exceeded 384 durable frames per second. McRave reached only 340.17 fps, below the preregistered floor, so the engineering screen failed. The candidate also recorded zero wins.

The build-commandability repair was exercised once in the UAlberta-Terran lane. The guard suppressed a build attempt at frame 2,604, no build command was rejected, and a later build was accepted at frame 20,868. This passes the registered mechanism check without claiming that the guard caused the outcome. The retained sixth-Pylon mechanism also fired in UAlberta-Terran, McRave and Stardust, with accepted, current and completed frames in order and no game exceeding six Pylons.

| Opponent / map | Outcome | Frames | Durable fps | Guard blocks / first | Last accepted build | Max Pylons | Sixth accepted / current / complete | Max Zealots / Dragoons | Rejected commands |
| --- | --- | ---: | ---: | --- | ---: | ---: | --- | ---: | ---: |
| ZZZKBot / Benzene | loss | 6,327 | 2,638.15 | 0 / not reached | 2,046 | 1 | not reached | 3 / 0 | 0 |
| UAlbertaBot-Terran / Destination | loss | 23,005 | 1,826.01 | 1 / 2,604 | 20,868 | 6 | 10,962 / 11,120 / 11,641 | 3 / 13 | 17 gather, 2.17% |
| UAlbertaBot-Protoss / Heartbreak Ridge | loss | 9,024 | 2,236.55 | 0 / not reached | 5,892 | 3 | not reached | 4 / 0 | 0 |
| McRave 9Pool / Circuit Breaker | loss | 20,308 | 340.17 | 0 / not reached | 10,254 | 6 | 8,772 / 8,931 / 9,452 | 13 / 10 | 0 |
| Stardust repaired / Benzene | loss | 15,317 | 1,093.04 | 0 / not reached | 9,606 | 6 | 9,606 / 9,756 / 10,277 | 8 / 13 | 0 |

The guard repairs the specific build-`Unit_Busy` failure observed in v28 and does not starve later construction in the one lane where it blocks. It does not supply evidence of improved strength: every game was a loss, ZZZK ended with three Zealots and no Dragoons, and UAlberta-Protoss ended with four Zealots and no Dragoons. McRave and Stardust reached mixed armies and the sixth-Pylon path but still lost. Fresh seeds make comparisons with earlier candidates descriptive rather than causal.

v29 is not adopted, does not enter Elo and does not replace canonical Kestrel v13. No retry or replacement was run. All attempts, logs, metadata and replay copies remain preserved locally.

## Identity and preservation

- Plan SHA-256: `ca6bfbeea5f0d78f20f653a2673eebd4affb400ad4a95eb11a664eaa638b3b34`.
- Schedule SHA-256: `26adb1612972811d9931eaf00b45775eb39e4f3c4e6989404f1daf930a98514a`.
- Manifest SHA-256: `62d3bf06bc267e366b540c322f44dff03bdac51baab7d47145ceed35459bf43d`.
- Scorecard SHA-256: `a8089652835a4bbdddbcb08a1efddf91ddd8f7a7e87babc80ce500a6369e8c52`.
- Candidate binary SHA-256: `c7196ea991f5755b6e34c9c9ebff87faf3884d221de9492a7952ce20cc57d56c`.
- Candidate source SHA-256: `0dbb8404b62197e52020655d098c888abdb25aaeca79b60358d44b4a806b4fe3`.
- Patch SHA-256: `3886344ea225b3481ecf9905a5e9a99f1ee6e44c51715ba7d07cc085dc5464b7`.
