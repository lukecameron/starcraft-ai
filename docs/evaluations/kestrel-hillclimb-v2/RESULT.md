# Kestrel v22 three-change hill-climb result

## Decision: INCONCLUSIVE FOR STRENGTH; DO NOT ADOPT

The five-game exploratory screen completed with valid manifests and parsed candidate replays, but Kestrel lost all five games. The candidate introduced no command rejections and preserved the descriptive replay signals, so the batch is useful for selecting the next bounded change but cannot support an Elo update or production promotion.

| Opponent / map | Outcome | Frames | Durable fps | First threat | First Zealot loss | Accepted trains | Structures after first train | Local Zealots before loss | Max Dragoons |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ZZZKBot / Benzene | loss | 5,800 | 2,686.4 | 3,931 | 4,459 | 4 | 0 | 1 | 0 |
| UAlbertaBot-Terran / Destination | loss | 18,851 | 2,468.6 | 3,794 | 16,482 | 23 | 10 | 8 | 10 |
| UAlbertaBot-Protoss / Heartbreak Ridge | loss | 11,163 | 2,754.4 | 2,964 | 7,696 | 11 | 11 | 3 | 3 |
| McRave 9Pool / Circuit Breaker | loss | 15,255 | 542.0 | 7,671 | 10,901 | 14 | 15 | 3 | 5 |
| Stardust repaired / Benzene | loss | 15,224 | 1,066.6 | 3,034 | no local Zealot loss recorded | 6 | 10 | 3 | 9 |

All five candidate replays were present, hash-matched and `screp`-parseable. Every scorecard row received all four descriptive signals and the five games were under the five-minute wall cap. These are command-derived review aids; replay orders do not prove hidden state or command acceptance.

## Interpretation and next hill-climb

The race-general public-threat latch and local home count helped the Protoss-pressure lane reach three local Zealots and eleven accepted structures, compared with one local Zealot and six structures in the v19 screen. The Stardust lane recorded no local Zealot loss before the game ended. The early-tech change increased production in the Terran lane to 23 accepted Zealot trains and in the Protoss lane to 11, but did not convert either game into a win. ZZZK still defeated the candidate before tech, and McRave ended the candidate after a later threat despite the earlier tech policy.

The next registered refinement raises the local hold threshold from two to three completed home Zealots while retaining the race-general threat latch and two-train tech unlock. This directly targets the remaining early-loss pattern without changing the opponent set or adding hidden-state access.

## Identity and preservation

- Plan SHA-256: `da1e662e2e63f27f3355eeec344e55bd045ac78eb2b2ad6058734662f0d6512e`.
- Schedule SHA-256: `c185ba41dd4fb8d896d21e43940e4e8230be1158c6afd966a7dd319d0dfdb86f`.
- Manifest SHA-256: `6af006fbb3c359dcd861253c817766cc8566cf2f1c160a58488014a56d641d39`.
- Scorecard SHA-256: `27e50a45dc72853696d19f9188602c75c3cd476219188d1b3743a0377751091c`.
- Candidate binary SHA-256: `6e112c43d6dace13d1152c834658aa35647ceea29b761159187d44d3837fcf57`.
- Candidate source SHA-256: `e82345ea48dbd32c4296e10c57f2ddd0804f4a8141a5ab417262f7a645758cb5`.

The v22 candidate remains an unadopted exploratory build. Canonical Kestrel v13 and its reviewed local rating are unchanged.
