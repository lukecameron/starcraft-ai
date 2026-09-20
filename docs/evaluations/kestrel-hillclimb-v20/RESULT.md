# Kestrel hill-climb v20 result

Date: 2026-09-21  
Decision: **REJECT**

This was the fresh preregistered ten-row screen of
`Kestrel-v40-nearest-gateway-probe`. The nearest-builder treatment was proved
correct in every observed selection and Kestrel won three of four games against
ZZZKBot. Two valid ZZZK lanes nevertheless reached their first qualifying home
threat with only one completed combat unit. The plan requires two units in
every qualifying lane and makes any observed miss an independent rejection, so
v40 does not advance. One separate UAlbertaBot-Terran row timed out and remains
invalid. Do not retry this cohort or update Elo from it.

## Frozen identity and evidence

The plan SHA-256 is
`619f1430f8d0b0c1f6b014e1085d045a38d08914cea098894a867bd5008e7a6a`.
The committed source schedule SHA-256 is
`b5d3217530ee43a64278c6b08f75d4bc118fa9076d44351702e4e4604bc46874`;
the runner-persisted canonical copy is
`f2dba1f53bf93dafa69bcd957ccf5093424f74aacc5b155c139503de8415e4d9`.
The experiment ledger SHA-256 is
`3ed14b60927b63b64752d1bbdc2253d326cdce07e4cae228dfd26d69a8af9c4a`,
and the independently regenerated scorecard SHA-256 is
`44093d3de31f1aa783482cdbf0ae4e2e8d633eef40722d73a1bb06fc4e234397`.

The candidate is Kestrel, **Ours**, **Original**, author Luke Cameron, source
[lukecameron/starcraft-ai/tree/main/bots/kestrel](https://github.com/lukecameron/starcraft-ai/tree/main/bots/kestrel).
Its binary SHA-256 is
`adac4ff4dc5aea71b94a5a12d13d62f964fe56a71ca3fd5141f24d0094401012`,
source SHA-256 `89dde1b4dd26f3ba890e7b0f08836c5b9caef36a9799d8b744e2b01ff2f7c112`,
combined source SHA-256
`37be433c0f3e081951b77a5448ed256151a0b97e043601cb21de6ef8d23c3fc4`,
and telemetry patch SHA-256
`9ade3388f07b3289f9f12cd0a468bd6b12d0a3c064d0e166a532111f8cb5c4bf`.
All candidate, parent, opponent, engine, launcher, sidecar, script, map, MPQ,
and provenance hashes matched the schedule.

The schedule identifies ZZZKBot as **Ours / Port**, author Chris Coxe;
UAlbertaBot as **Ours / Port**, author David Churchill; McRave as **Ours /
Fork**, author Christian McCrave; and Stardust as **Ours / Fork**, author Bruce
Mackenzie Nielsen. Their source links and immutable hashes remain in
`schedule.json` and `config/bot-identities.json`.

## Run-by-run result

| Game | Run ID | Opponent | Map | Seed | Kestrel slot | Result | Candidate frame |
|---:|---|---|---|---:|---:|---|---:|
| 1 | `20260920T200634-c60da2d08109` | ZZZKBot | `sscai/(2)Benzene.scx` | 10101 | P1 | Win | 11752 |
| 2 | `20260920T200634-d58af69191c9` | ZZZKBot | `sscai/(2)Destination.scx` | 10102 | P2 | Loss | 5614 |
| 3 | `20260920T200634-f734fb07c566` | UAlbertaBot-Terran | `sscai/(2)Destination.scx` | 10103 | P1 | Timeout / unknown | 78720 |
| 4 | `20260920T200634-92030938174c` | UAlbertaBot-Protoss | `sscai/(2)Heartbreak Ridge.scx` | 10104 | P2 | Loss | 51556 |
| 5 | `20260920T200634-6d5a07e3abff` | McRave-9Pool-treatment | `sscai/(4)Circuit Breaker.scx` | 10105 | P1 | Loss | 15782 |
| 6 | `20260920T200636-ee4312ffeba2` | ZZZKBot | `sscai/(4)Circuit Breaker.scx` | 10106 | P1 | Win | 12651 |
| 7 | `20260920T200638-6b510f61ad96` | ZZZKBot | `sscai/(2)Heartbreak Ridge.scx` | 10107 | P2 | Win | 10946 |
| 8 | `20260920T200640-996559ceb400` | UAlbertaBot-Terran | `sscai/(2)Destination.scx` | 10108 | P2 | Loss | 23222 |
| 9 | `20260920T200641-b20bf4a0a4c9` | UAlbertaBot-Protoss | `sscai/(2)Heartbreak Ridge.scx` | 10109 | P1 | Loss | 11411 |
| 10 | `20260920T200646-2d259497200f` | Stardust-repaired | `sscai/(2)Benzene.scx` | 10110 | P2 | Loss | 10636 |

The fixed denominator is ten attempts: three wins, six losses, and one invalid
timeout. The nine valid terminals are 3-6. The ZZZKBot subgroup is 3-1;
UAlbertaBot-Terran is 0-1 plus one timeout; UAlbertaBot-Protoss is 0-2;
McRave is 0-1; and Stardust is 0-1. These heterogeneous results are not an
Elo estimate.

## Integrity and replay evidence

The ten schedule rows produced ten unique run IDs and manifests with no retry,
reseed, replacement, or rerun. Nine games have reciprocal terminal metadata,
zero launcher return codes, and exactly two archived replay copies each. All
18 copies match their source and archive hashes and sizes, parse fully with
`screp`, have the scheduled race headers, and satisfy
`replay_header_frames + 1 == owning_callback_frame`.

Game 3 hit the registered 120-second wall cap. Its launchers were terminated
with return code -15; it has nonterminal metadata, no replay, and no verified
outcome. It remains in the denominator. Its 655.5 logical frames per second is
diagnostic throughput, not valid completed-game performance evidence.

## Treatment and retained gates

The v40 Gateway-Probe proof passed in all ten diagnostics: 20/20 first/second
Gateway rows had aligned and fully partitioned arrays, no truncation, legal
reason codes, accepted-build frame alignment, the selected builder at the
minimum eligible distance, and the lowest ID on distance ties. This establishes
that v40 implemented the registered nearest-eligible-Probe policy; it does not
establish that the policy caused the wins.

All four valid ZZZK games were qualifying lanes and covered both slots. Their
opening observations were:

| Lane | Second Gateway current / completed | First qualifying threat | Completed combat globally / locally | Result |
|---|---:|---:|---:|---|
| Benzene P1 | 2055 / 3026 | 3725 | 2 / 2 | Win |
| Destination P2 | 2084 / 3055 | 3560 | 1 / 1 | Loss |
| Circuit Breaker P1 | 2026 / 2997 | 4213 | 3 / 3 | Win |
| Heartbreak P2 | 2082 / 3053 | 3551 | 1 / 1 | Win |

Destination and Heartbreak are decisive observed misses. Replay commands show
the second Zealot was ordered around frames 3002-3062; in both early P2 lanes,
the threat arrived before that unit could complete. The nearest-builder change
removed the selected-worker ambiguity but did not make the opening robust to
the earlier threat timing.

Construction telemetry passed in 10/10 diagnostics. Shared targeting had
3,576/3,576 accepted commands, 626 coordinated accepted selections in eight
exercised games, and zero shared-target rejects or illegal selections. Nine
lanes were eligible for and accepted Singularity Charge; eight completed it.
Reserve, emergency, staged-offense, cap, commandability, public-information,
and non-Zerg telemetry had no review flags, with unobserved opportunities left
explicitly untested.

Valid games stayed below five-percent command rejection, with zero gas-worker
build attempts and zero build `Unit_Busy` rejects. The invalid timeout recorded
30 rejected gather commands among 252 commands, 11.90%, which also exceeds the
registered per-game threshold as observed diagnostic evidence. The cohort had
54 rejects among 10,911 commands, 0.49%.

## Interpretation and next work

The 3-1 ZZZK record is the strongest short-batch result yet from an experimental
Kestrel descendant, and the treatment proof is clean. It still cannot promote
v40 because two qualifying opening lanes missed the fixed safety gate and one
of ten rows was invalid. Canonical Kestrel remains v13 and its local rating is
unchanged.

The next bounded opening experiment should target the actual timing gap: both
failing lanes need a second completed Zealot roughly 100-170 frames earlier.
The most direct hypothesis is a Zerg-only two-Gateway mineral/timing policy that
starts the pair close enough together for the second Gateway to train before
the frame-3550 pressure window. A separate later experiment can test holding
the first Zealot home until the second completes. Midgame work should examine
the McRave loss, where nine global combat units but only three local units were
present at the observed home threat despite clean shared-target commands.

No Elo update, public submission, tournament claim, or general promotion
follows from this result.
