# Kestrel v28 sixth-Pylon result

## Decision: REJECT CANDIDATE; ENGINEERING GATE FAILED

All five attempts reached reciprocal terminal losses with hash-matched, fully parsed replays. Three lanes accepted, started and completed a sixth Pylon in the registered frame order, and no game exceeded the six-Pylon cap. The candidate recorded zero gas-worker build attempts, every game exceeded 384 durable frames per second, every per-game rejection rate remained below 5%, and the cohort rejected 35 of 2,910 attempted commands, or 1.20%.

The candidate recorded zero wins and failed the preregistered zero build-`Unit_Busy` gate. Stardust had one rejected build command with `Unit_Busy`. The failure is retained; no retry or replacement was run.

| Opponent / map | Outcome | Frames | Durable fps | Max Pylons | Sixth accepted / current / complete | Max Zealots / Dragoons | Rejected commands |
| --- | --- | ---: | ---: | ---: | --- | ---: | ---: |
| ZZZKBot / Benzene | loss | 6,296 | 2,712.3 | 1 | not reached | 3 / 0 | 0 |
| UAlbertaBot-Terran / Destination | loss | 29,019 | 1,432.7 | 6 | 8,604 / 8,707 / 9,228 | 5 / 12 | 34, 2.44% |
| UAlbertaBot-Protoss / Heartbreak Ridge | loss | 9,830 | 2,455.3 | 4 | not reached | 5 / 1 | 0 |
| McRave 9Pool / Circuit Breaker | loss | 17,425 | 444.7 | 6 | 8,952 / 9,056 / 9,577 | 12 / 6 | 0 |
| Stardust repaired / Benzene | loss | 11,132 | 1,301.3 | 6 | 7,938 / 8,086 / 8,607 | 5 / 6 | 1 build `Unit_Busy`, 0.46% |

The sixth-Pylon mechanism is verified in UAlberta-Terran, McRave and Stardust, but it did not convert to a win. UAlberta-Terran survived to frame 29,019 and produced twelve Dragoons, while McRave reached twelve Zealots and six Dragoons; both still lost. ZZZKBot and UAlberta-Protoss ended before the sixth-Pylon condition, so this candidate did not address their earlier opening failures. Fresh seeds make comparisons with v22 descriptive rather than causal.

v28 is not adopted, does not enter Elo and does not replace canonical Kestrel v13. The repeated five-Pylon ceiling is confirmed as reachable and removable, but a matched confirmation would only be justified after a candidate also records a verified win and passes all engineering gates.

## Identity and preservation

- Plan SHA-256: `2d9cf328b8705cf8ca66f05a88d1b7c36c7d3f6806e2fc5e09837d10dae67149`.
- Schedule SHA-256: `113f17bf718a724a003a7759389a6a3963f57ff9c9e00966aa90e08532f983d2`.
- Manifest SHA-256: `ef52fbd08054c07a2f4ab7981ede5f1931cad4ad67cfe9c9af292b9346a76a07`.
- Scorecard SHA-256: `e45befc7a0528bf8ef73140f0bb436d321218eabbd0c271b98507ce7ca68fa23`.
- Candidate binary SHA-256: `86e59d631f27c151b6bd893bf77cde3ab62073b7ece1b4dfde9084850e3b3c63`.
- Candidate source SHA-256: `709ae8920a7724c7024e778dc83ceb6f2ec9bc5b4edf236f70f2a3129a3b0b5c`.

All attempts, logs, metadata and replay copies remain preserved locally.
