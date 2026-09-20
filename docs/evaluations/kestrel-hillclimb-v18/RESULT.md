# Kestrel hill-climb v18 result

Date: 2026-09-21  
Decision: **REJECT**

This was the preregistered ten-attempt held-out confirmation of `Kestrel-v38-shared-target`. Kestrel recorded two verified wins, including one win over ZZZKBot, seven verified losses, and one preserved ZZZKBot timeout. The treatment telemetry remained legal and exercised, but the second valid ZZZKBot lane reached its qualifying home threat with only one completed combat unit. That is an observed failure of the retained two-unit opening gate, so the plan's independent observed-regression clause requires `REJECT` despite the separate timeout. Do not retry, promote v38, or update Elo from this cohort.

## Frozen identity and evidence

The plan SHA-256 is `6a450005eb3c40e0b2ba623a70927beef66bb02abeabede1f8ae092a17873c13`. The committed source schedule SHA-256 is `bc754c4d6defbee209bcad81f5c43f972d4b09d86859e9e80ad6d7b87e65500d`; its runner-persisted canonical copy is `6b01686ddc30405ab0fb796209c6cf9f382379f7201810fe17658a4e7b4a4a08`. The raw ledger SHA-256 is `4792f3674734e86a056bcfe7dc0090b036c4857255e755f8ed372f5416c247ba`, and the canonical and independently regenerated scorecard SHA-256 is `ffe471f42cf107e7444e795770a4b4aec5ab986de60de29a33795b9e850976ac`.

The candidate is Kestrel, **Ours**, **Original**, author Luke Cameron, with source [lukecameron/starcraft-ai/tree/main/bots/kestrel](https://github.com/lukecameron/starcraft-ai/tree/main/bots/kestrel). The frozen binary SHA-256 is `7fdc4f9ad61152e7758318e7d35d04fbda0746a4e2f85a48b3bc664577e0c160`; source SHA-256 `f105ab5073ec3d586807478c74838900ed02fa2d812c3ac4d94081c36c3217ab`; combined source SHA-256 `ce744d7adcd3dc0a051c68a7162d975b40284c014a9b7e1eae785b59da9b8f7b`; reconstruction patch SHA-256 `2d84b98d3288d4ac922c22c71647f29492925138ee1ec757ee36512b9786b61a`; and build-sidecar SHA-256 `75f2f2fd236bdd71cb64102f8286c0358cd39a1c1a8ffbccf69fb7578a53a1b4`.

The schedule identifies ZZZKBot as **Ours / Port**, original author Chris Coxe; UAlbertaBot as **Ours / Port**, original author David Churchill; McRave as **Ours / Fork**, original author Christian McCrave; and Stardust as **Ours / Fork**, original author Bruce Mackenzie Nielsen. The source links and frozen binary hashes remain in the schedule and provenance registry.

## Run-by-run result

| Game | Run ID | Opponent | Map | Seed | Kestrel slot | Result | Candidate frame |
|---:|---|---|---|---:|---:|---|---:|
| 1 | `20260920T190743-0b7a42f81163` | ZZZKBot | `sscai/(2)Benzene.scx` | 10041 | P1 | Timeout / unknown | 2438400 |
| 2 | `20260920T190743-eaeb4a294d8c` | UAlbertaBot-Terran | `sscai/(2)Destination.scx` | 10042 | P2 | Loss | 20587 |
| 3 | `20260920T190743-2d59beaee0a4` | UAlbertaBot-Protoss | `sscai/(2)Heartbreak Ridge.scx` | 10043 | P1 | Loss | 12403 |
| 4 | `20260920T190743-ec974d7985a3` | McRave-9Pool-treatment | `sscai/(4)Circuit Breaker.scx` | 10044 | P2 | Loss | 15565 |
| 5 | `20260920T190743-df0f84e78179` | Stardust-repaired | `sscai/(2)Benzene.scx` | 10045 | P1 | Loss | 11938 |
| 6 | `20260920T190747-00cbb042f206` | ZZZKBot | `sscai/(2)Benzene.scx` | 10046 | P2 | Win | 12124 |
| 7 | `20260920T190751-79d02c147453` | UAlbertaBot-Terran | `sscai/(2)Destination.scx` | 10047 | P1 | Win | 15410 |
| 8 | `20260920T190754-018398c237bc` | UAlbertaBot-Protoss | `sscai/(2)Heartbreak Ridge.scx` | 10048 | P2 | Loss | 49169 |
| 9 | `20260920T190756-ae9596c94ab4` | McRave-9Pool-treatment | `sscai/(4)Circuit Breaker.scx` | 10049 | P1 | Loss | 17022 |
| 10 | `20260920T190756-39c146c880fe` | Stardust-repaired | `sscai/(2)Benzene.scx` | 10050 | P2 | Loss | 10357 |

The registered primary denominator is ten scheduled attempts: two wins, seven losses, and one unknown, or 20% verified wins descriptively. Among only the nine valid terminals the record is 2-7. Opponent subgroups are ZZZKBot 1 win and 1 timeout, UAlbertaBot-Terran 1-1, UAlbertaBot-Protoss 0-2, McRave 0-2, and Stardust 0-2. These heterogeneous subgroups are not an Elo estimate.

## Integrity and timeout

Rows, maps, slots, seeds, candidate, opponents, engine, launcher, launcher sidecar, game data, and provenance hashes match the committed schedule. There are exactly ten attempts with no retry, reseed, or replacement.

Games 2 through 10 ended with `children_exited`, zero child return codes, reciprocal results, and two archived replay copies apiece. All 18 replay copies match their source and archive hashes, parse completely with `screp`, report the scheduled races, and satisfy `replay_header_frames + 1 == owning_callback_frame`.

Game 1 hit the 300-second wall cap at 2,438,400 logical frames. Both launcher processes were terminated with return code -15; there is no terminal result or replay, and Kestrel peak RSS was 1,170,817,024 bytes. The attempt remains part of the denominator and must not be retried. Its diagnostic telemetry is useful for a separately preregistered runtime and memory investigation, but its reported logical-frame throughput is not playing-strength evidence.

## Registered gates

Shared-target diagnostics were structurally valid in all ten attempts: 6,288 selections, 5,142 multi-participant selections, 734 coordinated accepted selections, 5,673 attempts and 5,673 accepts, 342 target switches, 637 correction opportunities, maximum 30 participants, zero shared-target rejects, and zero illegal selections. Every attempt observed an accepted coordinated multi-participant selection, exceeding the registered eight-game exercise threshold as telemetry evidence.

All ten lanes were eligible for Singularity Charge and recorded accepted and completed upgrades. The cohort observed six fifth-Gateway and seven seventh-Pylon milestones with ordered prefixes and no cap violation. Construction bookkeeping passed in all ten diagnostics. Retained reserve, emergency, staged-offense, public-information, and non-Zerg checks passed wherever observed; unobserved emergency or reserve opportunities remain explicitly untested as permitted by the plan.

The candidate recorded 40 rejected commands among 12,868 attempts, or 0.31%. Each lane remained below five percent; game 1 was highest at 26/819, or 3.17%. All rejections were gather `Unit_Busy`; build commands and shared-target commands had zero rejections, and gas-worker build attempts remained zero.

The decisive retained opening gate failed in valid game 6. Its second Gateway was current at frame 2,090 before the qualifying home threat at frame 3,659, but only one completed combat unit was present locally and globally; the registered requirement was at least two. Game 1 observed two units at its frame-3,754 threat, but later timed out. The fixed rule states that an observed gameplay or treatment regression independently produces `REJECT`, so the valid game-6 opening failure decides the cohort even though game 1 separately prevents a complete ten-terminal confirmation.

## Interpretation and next work

The two fresh wins and clean shared-target telemetry are encouraging descriptive evidence. They do not outweigh the fixed opening gate or establish a causal strength improvement. v17 remains an eligibility screen; v18 rejects promotion of v38. Canonical Kestrel v13 and its existing local rating remain unchanged.

The next work should first diagnose the ZZZKBot runaway and 1.09 GiB RSS, then address the repeatable one-defender ZZZK opening miss. Separate bounded candidates can later target the 0-4 Protoss subgroup and the 0-2 McRave subgroup. The recurring gather `Unit_Busy` traffic is a lower-risk correctness cleanup. No new policy candidate is selected from this rejected cohort.

No Elo update, public submission, tournament claim, or general promotion follows from this result.
