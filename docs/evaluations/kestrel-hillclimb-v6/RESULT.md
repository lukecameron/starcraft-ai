# Kestrel v26 Zerg tech-first construction result

## Decision: REJECT CANDIDATE

All five preregistered attempts completed with reciprocal terminal results, candidate losses, hash-matched replays and full replay parses. Kestrel recorded zero rejected commands, zero gas-worker build attempts and zero build `Unit_Busy` rejections. Durable throughput ranged from 572.7 to 2,853.4 frames per second, above the 384 fps gate. The screen is valid.

The registered construction mechanism fired in both Zerg lanes. Against ZZZKBot, the Assimilator was accepted at frame 3,144 and the Core at 4,122; no second Gateway was accepted before the game ended at frame 5,397. Against McRave, the Core was accepted at 4,398 and became current at 4,802, before the second Gateway was accepted at 5,640. This verifies the intended tech-before-second-Gateway ordering where the second Gateway was reached.

The mechanism did not convert to a win or to Dragoon production in either Zerg lane. ZZZKBot ended the game before the Core became current, with two maximum Zealots and no Dragoon. McRave reached a completed Core at frame 5,773 and survived to frame 14,542 without a recorded home Zealot loss, but trained no Dragoon. The three non-Zerg lanes retained v22's existing construction path and are descriptive coverage rather than tests of the Zerg-specific change.

| Opponent / map | Outcome | Frames | First threat | First Zealot loss | Core accepted | Second Gateway accepted | First Dragoon train | Max Zealots / Dragoons | Rejected commands |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ZZZKBot / Benzene | loss | 5,397 | 3,968 | 5,359 | 4,122 | none | none | 2 / 0 | 0 |
| UAlbertaBot-Terran / Destination | loss | 11,163 | 2,821 | 8,489 | 4,086 | 2,262 | 5,796 | 5 / 3 | 0 |
| UAlbertaBot-Protoss / Heartbreak Ridge | loss | 16,526 | 3,882 | 9,779 | 4,674 | 3,114 | 6,462 | 8 / 6 | 0 |
| McRave 9Pool / Circuit Breaker | loss | 14,542 | 5,905 | none recorded | 4,398 | 5,640 | none | 10 / 0 | 0 |
| Stardust repaired / Benzene | loss | 15,627 | 3,076 | 15,463 | 4,482 | 2,928 | 6,378 | 7 / 10 | 0 |

The candidate fails the preregistered advancement bar because it recorded zero verified wins. It is not adopted, does not update Elo and does not replace canonical Kestrel v13. The positive ordering signal can inform a later candidate, but v22 remains the exploratory hill-climb base until a distinct change earns a verified win and matched confirmation.

## Identity and preservation

- Plan SHA-256: `47b7eeaf1e476971e67bfe98757b104e002053c6632b70ee63957480a501df31`.
- Schedule SHA-256: `941bbc54e3bab94e217e35313bd1d58a8dcfbc0878ecd25ccd752e3291d78d2f`.
- Manifest SHA-256: `fa187f7de9b7d5777c3428ddc909178f420a450d3360ee3e9b5da9f89612415c`.
- Scorecard SHA-256: `b9dcc7f1b35e3e01719df79fea907b16a21ef768ddf821134e613dd9691dc539`.
- Candidate binary SHA-256: `45726aff4461d5367efb6f3ac4b355c4f3dd03dc537dfe46dca49a36fae72070`.
- Candidate source SHA-256: `324af4c924161410b44b875578f60246c6200caff4f68c65ad55cef96252434e`.

All artifacts remain local and preserved. No v26 game enters the local Elo pool.
