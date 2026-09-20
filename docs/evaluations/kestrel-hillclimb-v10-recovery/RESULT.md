# Kestrel v31 early-Zerg squad-staging recovery result

## Decision: REJECT CANDIDATE; MECHANISM AND WIN GATES FAILED

All five recovery attempts completed with reciprocal terminal results, zero nonzero child exits and ten preserved replay copies. Every replay hash matches its manifest, all ten parse fully without command parse errors, and every replay terminal frame is exactly one below its owning callback frame. The manifests' broad `launcher_error_detected` flag is set by normal nonempty OpenBW diagnostic stderr, while exit codes and lifecycle records show no launcher failure. Kestrel lost all five games, so the advancement rule fails independently of mechanism behavior.

The staging rule exercised in both Zerg lanes. It issued no prohibited pre-four remote attack, reached two local combat units in both games and released at an army of four against McRave. It failed the registered actual-threat condition in that lane: when the first visible non-worker Zerg threat entered the 12-tile home radius at frame 5,479, Kestrel had five completed combat units globally but only one locally. Against ZZZK, the same measurement passed at frame 3,692 with two of two combat units local, but the game still ended in a loss before the army reached four.

The attempted target-position guard did not bound staging orders. ZZZK accepted 101 home moves for one uniquely suppressed unit; McRave accepted 776 for six uniquely suppressed units. There were no rejections, but this is redundant command traffic and shows that target-position equality is not a reliable one-command latch. The next candidate must use explicit per-unit state or a registered retry cadence and must retain defenders after the first offensive release if it intends to protect the first real pressure window.

| Opponent / map | Outcome | Candidate frames | Wall seconds | Durable fps | Rejected / attempted | Army max Z / D | Staging summary |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| ZZZKBot / Benzene | loss | 5,552 | 2.05 | 2,724.0 | 0 / 140 | 3 / 0 | 3 suppressions, 101/101 home moves, local 2/2 at army threat, no release |
| UAlbertaBot-Terran / Destination | loss | 13,209 | 5.05 | 2,622.0 | 0 / 223 | 6 / 7 | Zerg-only treatment inactive |
| UAlbertaBot-Protoss / Heartbreak Ridge | loss | 33,421 | 13.76 | 2,432.0 | 12 / 268 | 7 / 11 | Zerg-only treatment inactive |
| McRave 9Pool / Circuit Breaker | loss | 19,874 | 42.11 | 472.7 | 0 / 5,589 | 10 / 14 | 18 suppressions, 776/776 home moves, release at 4; local 1/5 at army threat |
| Stardust repaired / Benzene | loss | 15,348 | 14.12 | 1,089.2 | 0 / 452 | 8 / 12 | Zerg-only treatment inactive; build guard blocked once and later construction recovered |

Regression gates pass. Every lane has zero gas-worker build attempts and zero build `Unit_Busy` rejections. The only rejected commands were 12 gathers in UAlberta-Protoss, 4.48% for that lane and 0.18% across the 6,672-command cohort. No game exceeded six Pylons; all observed sixth-Pylon accepted/current/completed frames are ordered. Stardust exercised one build-commandability guard at frame 3,024 and accepted later construction at frame 9,882.

Fresh seeds prevent causal comparisons with earlier candidates. Descriptively, v31's UAlberta-Protoss loss lasted much longer than v29, while its ZZZK loss ended sooner and McRave/Stardust were similar. A shorter verified win would be favorable under the registered rule; a shorter loss is not improvement. The scorecard's replay and outcome grades are descriptive and do not override the zero-win gate.

v31 is not adopted, does not enter Elo and does not replace canonical Kestrel v13. No retry or replacement was run after the recovery.

## Identity and preservation

- Recovery runs: `20260920T152002-53fed6c05ff1`, `20260920T152002-df2280214a47`, `20260920T152002-902b0d03b47d`, `20260920T152002-f8ceb7826f10`, `20260920T152002-5331c7b2f0dc`.
- Recovery plan SHA-256: `511fc973ad0dd089850277f5de13d9054a4d74278576c1f1765ad40c5312942f`.
- Frozen recovery schedule SHA-256: `ab5ae49c27dde3a83f16409e6957fabf2944daaf4b60dda777bc9ab409458dba`.
- Batch manifest SHA-256: `add901d2296b7ee18a05b4bc52b10050ee09851666cd78538b8afc3c7f673b94`.
- Scorecard SHA-256: `1f47ea3dd2067296036635e610e7bb9222e9a4924aa3145103fc705f7bd0d053`.
- Candidate binary SHA-256: `5ff164dc9dfd5c555837f110002f3907838891c6fdc95a8960cc48f12e47e107`.
- Candidate source SHA-256: `347414e122c0b59311588a50e4c003a03b6dd61fb4081b1e01b0a750cc0de928`.
- Reconstruction patch SHA-256: `caf0739d9a63f6c4f9f78f9ef8d7fccf878aabc4d0b8d32885619f3c071fdaa6`.
