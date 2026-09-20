# Kestrel v27 home-rally override result

## Decision: REJECT CANDIDATE; ENGINEERING GATE FAILED

All five attempts reached reciprocal terminal losses with hash-matched, fully parsed replays. The registered home-rally branch fired in four lanes, including both Zerg opponents, and its accepted-order count equaled its unique-unit count everywhere. Kestrel recorded zero build `Unit_Busy` rejections and zero gas-worker build attempts. The cohort-wide command rejection rate was 13/3,151, or 0.41%.

The candidate still recorded zero wins and failed two preregistered engineering checks. McRave completed at 366.8 durable frames per second, below the 384 fps floor. McRave recorded 15 unique rallied Zealots versus 13 maximum concurrent Zealots, and Stardust recorded 9 versus 7; the plan required the unique lifetime count not to exceed the maximum concurrent count. That comparison was a poor spam proxy because replacements can make lifetime unique units exceed a concurrent maximum, while the source's per-unit set still prevents duplicate accepted rallies. The preregistered gate remains failed and is not revised after seeing results.

| Opponent / map | Outcome | Frames | Durable fps | First threat | First rally | Rally orders / unique | Local Zealots before loss | First Zealot loss | Rejected commands |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ZZZKBot / Benzene | loss | 6,265 | 2,609.4 | 4,022 | 4,110 | 3 / 3 | 1 | 4,328 | 0 |
| UAlbertaBot-Terran / Destination | loss | 12,186 | 2,731.6 | 9,696 | 10,086 | 1 / 1 | 1 | 10,157 | 0 |
| UAlbertaBot-Protoss / Heartbreak Ridge | loss | 49,789 | 2,024.1 | 48,718 | none | 0 / 0 | 0 | none recorded | 13 gather |
| McRave 9Pool / Circuit Breaker | loss | 19,936 | **366.8** | 4,096 | 4,176 | 15 / 15 | 3 | 17,371 | 0 |
| Stardust repaired / Benzene | loss | 12,000 | 1,254.8 | 3,085 | 3,660 | 9 / 9 | 4 | none recorded | 0 |

The mechanism was exercised but did not produce a win. Against ZZZKBot, three different Zealots accepted a home rally and one completed Zealot was observed locally before the first loss, yet the first loss followed only 218 frames after the first rally and the game still ended before tech. Against McRave, fifteen distinct Zealots rallied over the game and Kestrel reached thirteen Dragoons, but still lost. Fresh seeds make frame differences from v22 descriptive rather than causal.

v27 is not adopted, does not enter Elo and does not replace canonical Kestrel v13. Future screens should retain the direct accepted-order/unique-unit equality check but must not compare lifetime unique units to maximum concurrent units.

## Identity and preservation

- Plan SHA-256: `c204cfe3f105046d5b06b2164c75b3f98ad62b5ab76c9ce9f6fa00944b311b6e`.
- Schedule SHA-256: `3486b1c6833a7d523d1cf193a953914a2c9250ddbadacb5fa4e4445d6f770bc1`.
- Manifest SHA-256: `2a89cc358b411166d6518e243438965bd3a879b78dcfd3b5ebc27aed2c5022d7`.
- Scorecard SHA-256: `27beb384b331ecea4d80e5d07ee1b7b4ee3d9c84e2dc83dcb518fe273975aa84`.
- Candidate binary SHA-256: `88ce994524e9215bb6dbcfad00a1086408df5fc665a3c3798367a132f89b32e5`.
- Candidate source SHA-256: `06f652bc56214a6a3bc778d84abe0440189f8d5d487f4d175deab0380535e8a2`.

All attempts, logs, metadata and replay copies remain preserved locally.
