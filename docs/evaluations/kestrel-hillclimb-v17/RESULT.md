# Kestrel hill-climb v17 result

Date: 2026-09-21  
Decision: **ADOPT only to a separately preregistered held-out confirmation**

This was a preregistered five-game matched screen of `Kestrel-v38-shared-target` against the exact v16 rows. The candidate reproduced the v16 aggregate outcome of one verified win and four losses while adding the shared-target treatment. Integrity and retained mechanism gates passed, so the candidate is eligible for a separately preregistered held-out confirmation. This is not a promotion, Elo result, or tournament claim.

## Frozen identity and evidence

The plan hash is `9559d89008377c1323335b17962ddebc4bcf68b34745a430e96cf711016ddebf`. The schedule hash is `5f72d1f1f36e9708f806c8deaf4477fab729d3854477b6ee444d3851454ce6d2`; the raw ledger hash is `7ee523aab65afbb7e7837c44720b7738328e858946944dfb26d66d38853fe90c`; and the canonical and independently regenerated scorecard hashes are both `24d15faaa6c1345080eceec6a25e236bbc3555949705e18bcbb30d4dcecf9c16`.

The candidate is `Kestrel-v38-shared-target`, owned by **Ours**, origin **Original**, author Luke Cameron, with source [lukecameron/starcraft-ai/tree/main/bots/kestrel](https://github.com/lukecameron/starcraft-ai/tree/main/bots/kestrel). Its binary is `artifacts/builds/7fdc4f9ad61152e7758318e7d35d04fbda0746a4e2f85a48b3bc664577e0c160/kestrel-opening-v38-shared-target/Kestrel.dylib`, SHA-256 `7fdc4f9ad61152e7758318e7d35d04fbda0746a4e2f85a48b3bc664577e0c160`. The source SHA-256 is `f105ab5073ec3d586807478c74838900ed02fa2d812c3ac4d94081c36c3217ab`; the combined source SHA-256 is `ce744d7adcd3dc0a051c68a7162d975b40284c014a9b7e1eae785b59da9b8f7b`; and the reconstruction patch `patches/kestrel-v37-to-v38-shared-target.patch` has SHA-256 `2d84b98d3288d4ac922c22c71647f29492925138ee1ec757ee36512b9786b61a`. The build sidecar SHA-256 is `75f2f2fd236bdd71cb64102f8286c0358cd39a1c1a8ffbccf69fb7578a53a1b4`.

The frozen v37 base was binary `ad60fe9280c8e3c8e22785e90656df76a27b86e06b435346c0bc47142af6e228`, source `ffacb1de456936fa47058baa7735d0318cdb3e3d7a923740ec7a63ece5dd7c86`, and combined source `b22fd4257d47b96cc127f778e9bd3e81a3a4c4a2c17ae5e3b0023f44cbc0b2b6`. The native OpenBW engine library identity is `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`.

The schedule identifies ZZZKBot as a Port owned by Ours (author Chris Coxe), UAlbertaBot as a Port owned by Ours (author David Churchill), and McRave and Stardust as Forks owned by Ours (authors Christian McCrave and Bruce Mackenzie Nielsen). Their frozen binary hashes are respectively `ce796a5d49d78121aaf42b57ba758423ee89f74a249b42180cbc0b0cb9df4748`, `75ac4f6bb44ed6e48fbee883638c77df9557c9a88070ceca4de11183053238c9`, `436cfa74fa34c267f7404777a3170be0202485bdc7224d15fb30b85f02c5644e`, and `1039975842c6edea71043e0da091ff21ad5311fd3ddbeb568cf89b364f7d28aa`.

## Run-by-run result

| Game | Run ID | Opponent | Map | Seed | Kestrel slot | Result | Candidate terminal frame |
|---:|---|---|---|---:|---:|---|---:|
| 1 | `20260920T184731-21d81fdc506e` | ZZZKBot | `sscai/(2)Benzene.scx` | 9941 | P1 | Win | 11349 |
| 2 | `20260920T184731-0d0592b849ec` | UAlbertaBot-Terran | `sscai/(2)Destination.scx` | 9942 | P2 | Loss | 12558 |
| 3 | `20260920T184731-5a708d51551f` | UAlbertaBot-Protoss | `sscai/(2)Heartbreak Ridge.scx` | 9943 | P1 | Loss | 51525 |
| 4 | `20260920T184731-9f0835a34183` | McRave-9Pool-treatment | `sscai/(4)Circuit Breaker.scx` | 9944 | P2 | Loss | 16588 |
| 5 | `20260920T184731-69772d6f50e9` | Stardust-repaired | `sscai/(2)Benzene.scx` | 9945 | P1 | Loss | 17084 |

All five manifests completed with `children_exited`, both child return codes equal to zero, and reciprocal terminal result metadata. The registered cohort had exactly five rows and no retry.

## Replay and telemetry integrity

Each game has exactly two archived replay copies, for ten total. All ten copies exist, have `archival_status: copied`, and their recorded SHA-256 values match recomputation for both source and archive. Independent `screp -cmds=true -computed=true -map=false -indent=false` parsing exited zero for all ten copies, with no parse errors. Replay header races match the configured races in all ten copies, and every copy satisfies `replay_header_frames + 1 == owning_player_frame_count`.

Candidate diagnostic files match the manifest result metadata in all substantive fields. The generated `metadata_path` is the only expected path-field difference. Candidate and opponent modules hash to the frozen schedule identities. The plan, schedule, ledger, scorecard, candidate source, patch, sidecar, and engine hashes above were independently recomputed.

## Registered gates and shared-target telemetry

The cohort had five valid integrity grades, five complete replay parses, five replay-hash matches, five short terminal games, and one Kestrel win. It recorded 11 rejected commands among 5,051 attempts (0.22%); all 11 were gather `Unit_Busy` results in the long UAlberta Protoss game, whose per-game rate was 1.49%. Build and shared-target commands had zero rejections, so the registered below-five-percent per-game and cohort gates passed. Construction bookkeeping passed in all five games: 97 accepted builds, five observed Gateway sequences, and five passing construction grades. Probe-reserve telemetry recorded nine reserve blocks and five passing grades. The retained emergency episode gate passed its observed episode checks in all five games; it recorded 20 episodes, six assignments, and zero cap blocks. Zerg-offense telemetry passed in all five games, with 2,564 post-release remote accepts and 65 home-move accepts.

The v38 shared-target mechanism recorded 1,914 attempts and 1,914 accepts, 2,206 selections, 247 coordinated accepted selections, 329 correction opportunities, 124 target switches, 1,931 multi-participant selections, and zero illegal selections. All five shared-target grades passed.

Scaling recorded four eligible upgrade lanes, four accepted upgrades, three completions before terminal, five fifth-Gateway observations, and three seventh-Pylon observations. The one incomplete upgrade and one unobserved seventh-Pylon opportunity are terminal-censoring observations, not integrity failures; the registered scaling screen passed its defined gate. The matched ZZZK opening and retained construction, reserve, emergency, staged-offense, commandability, and non-Zerg gates passed.

## Matched v16 comparison and causal limits

Both screens used the same five maps, seeds, slots, opponents, engine identity, and wall caps. v16 recorded one win and four losses; v17 recorded the same one win and four losses. Both cohorts had five valid integrity grades and ten verified replay copies. v17 adds shared-target telemetry and records zero shared-target rejects or illegal selections. Its aggregate candidate frames were 11,349, 12,558, 51,525, 16,588, and 17,084; the v16 candidate frames were 11,721, 12,961, 10,884, 15,596, and 11,349.

This is matched descriptive evidence, not a causal estimate. The v38 change is a shared-target bundle layered onto the v37 candidate, and five games cannot establish general strength, isolate mechanism effects, or establish tournament transfer. The observed v17 outcome does not justify Elo movement or promotion. A separately preregistered held-out confirmation must use its own decision bar and preserve the current provenance and replay requirements.

The accidental infrastructure-only CLI-check batch under `artifacts/prelaunch-failures/kestrel-hillclimb-v17-accidental-cli-check` is preserved separately. Its five failed infrastructure runs are excluded from the registered v17 cohort and do not alter this result.

No Elo update, public submission, tournament claim, or general promotion follows from this result.
