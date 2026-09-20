# Kestrel v24 shared-target focus result

## Decision: REJECT FOR ADOPTION

The five-game screen completed with valid preserved replays and no launcher failures, but Kestrel lost all five games. Shared visible-target focus did not produce a win. The UAlberta-Terran lane survived to 19,905 frames without a recorded local Zealot loss, but the UAlberta-Protoss lane recorded 15 gather `Unit_Busy` rejections; the candidate remains exploratory and does not change Elo.

| Opponent / map | Outcome | Frames | Durable fps | First threat | First Zealot loss | Accepted trains | Structures after first train | Local Zealots before loss | Max Dragoons | Rejected commands |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ZZZKBot / Benzene | loss | 5,459 | 2,759.1 | 3,773 | 3,958 | 4 | 0 | 1 | 0 | 0 |
| UAlbertaBot-Terran / Destination | loss | 19,905 | 2,125.3 | 5,092 | none recorded | 9 | 10 | 9 | 8 | 0 |
| UAlbertaBot-Protoss / Heartbreak Ridge | loss | 32,088 | 1,798.4 | 29,837 | 30,850 | 8 | 11 | 8 | 8 | 15 gather `Unit_Busy` |
| McRave 9Pool / Circuit Breaker | loss | 16,030 | 465.1 | 7,375 | 15,137 | 15 | 12 | 14 | 9 | 0 |
| Stardust repaired / Benzene | loss | 16,030 | 1,005.6 | 3,031 | 15,330 | 20 | 9 | 2 | 11 | 0 |

All five candidate replays were present, hash-matched and `screp`-parseable. The v24 focus branch uses only currently visible, detected, non-flying enemy units; no evaluator-only state entered the policy. The result is an exploratory mechanism screen and cannot support a rating update or production promotion.

The next useful step is to keep v22's two-local hold and two-train tech base, retain shared-target focus only if a future run isolates its order-level effect, and address the remaining economy/combat conversion rather than increasing the hold threshold again. Canonical Kestrel v13 remains unchanged.

## Identity and preservation

- Plan SHA-256: `eb12214fb82494e6f7a3f9e170631ddbecc61921db4ea68437ac0f125847f255`.
- Schedule SHA-256: `e2b78155c9107b1273f3ba09ac4dcec394cf100d2ca9be90daef19ea7f01b822`.
- Manifest SHA-256: `e87f680a2caaab5675420a51ef84f8032f48a6f4e0609800fd5a6d5778211f70`.
- Scorecard SHA-256: `72224fa2cd86dfc07e8e60b7f07c2bdb2e9f0ad4d55fbcacf73c680c1a47795a`.
- Candidate binary SHA-256: `32dca20dd6f6e5a12b626f1321f44405124856fa8832a23a21e33cc1a4108512`.
- Candidate source SHA-256: `aa5bbefd8ce87ea8924e0e0d94e427e9f4830d32aaf3653762eae8489657a6a0`.

Canonical Kestrel v13 and the reviewed local rating remain unchanged.
