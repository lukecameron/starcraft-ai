# Kestrel hill-climb v16 result

Date: 2026-09-21
Decision: **REJECT**

This was a preregistered five-game matched screen of `Kestrel-v37-post-opening-scaling` against the exact v15 scenario rows. The candidate produced one verified win, but the registered retained emergency-episode cap-block opportunity gate was unobserved: `emergency_episode_cap_blocks` was zero across the cohort. The cohort is valid and the failure is a gameplay/mechanism gate, so the registered decision is REJECT. This result does not update Elo, promote the candidate, or replace the canonical anchor.

## Frozen identity and evidence

The plan hash is `5e20aba59d0b199bd6f420873490c339d2d5c420edcdb546e43ad606dd796ddb`. The tracked schedule hash is `158651407c6ea114a8c5385796a5bab6097eda046710f9412bfb979c1859699a`; the batch runner's canonicalized persisted schedule hash is `b0f776ab1c4a973b135790636b7981a6d96e1eebc87af63febceae3c8e9274c4`. The raw ledger hash is `6d0d9b874c70a40423f8a47ab4d9becd9c144e07b9ac937902410aa67cce0af6`, and the independently regenerated scorecard hash is `cb4713b34d43302f45b94263f61ba60dbe9d2e2eb26154eae7199fc9c7ba37f3`.

The candidate is `Kestrel-v37-post-opening-scaling`, owned by **Ours**, origin **Original**, author Luke Cameron, with source [lukecameron/starcraft-ai/tree/main/bots/kestrel](https://github.com/lukecameron/starcraft-ai/tree/main/bots/kestrel). Its binary is `artifacts/builds/ad60fe9280c8e3c8e22785e90656df76a27b86e06b435346c0bc47142af6e228/kestrel-opening-v37-post-opening-scaling/Kestrel.dylib`, SHA-256 `ad60fe9280c8e3c8e22785e90656df76a27b86e06b435346c0bc47142af6e228`. The source SHA-256 is `ffacb1de456936fa47058baa7735d0318cdb3e3d7a923740ec7a63ece5dd7c86`; the combined source SHA-256 is `b22fd4257d47b96cc127f778e9bd3e81a3a4c4a2c17ae5e3b0023f44cbc0b2b6`. The v36-to-v37 reconstruction patch is `patches/kestrel-v36-to-v37-post-opening-scaling.patch`, SHA-256 `262cb9254874f2155c9c58fc669da8e8f418ebbe90c502da8e717f5403d8863a`. The build sidecar SHA-256 is `ea2cd75443e1f057a3db108072a92e5b7a35eb1fbb592a0287560cb0b604864f`.

The frozen v36 base was binary `c2e95394fd5c8c6a6dcd4ae2d7a8f1460624d454a906c6dba3e3e32bfb960b85`, source `a8f884c4dea4d3dfd4a91708763b35457c330f1bf4b89a6c12bdcbd0092effc3`, and combined source `81b1d8ed7e0879dbd9b36716fa4922e9366bddcc4d64ca6b6e77e70adff6fdbb`. The native OpenBW engine identity is `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`.

## Run-by-run result

| Game | Run ID | Opponent | Map | Seed | Kestrel slot | Result | Candidate terminal frame |
|---:|---|---|---|---:|---:|---|---:|
| 1 | `20260920T182135-5a03c3c5cc8e` | ZZZKBot | `sscai/(2)Benzene.scx` | 9941 | P1 | Win | 11721 |
| 2 | `20260920T182135-3fc37445b91d` | UAlbertaBot-Terran | `sscai/(2)Destination.scx` | 9942 | P2 | Loss | 12961 |
| 3 | `20260920T182135-300d82e64e6e` | UAlbertaBot-Protoss | `sscai/(2)Heartbreak Ridge.scx` | 9943 | P1 | Loss | 10884 |
| 4 | `20260920T182135-ee62cab2d5f9` | McRave-9Pool-treatment | `sscai/(4)Circuit Breaker.scx` | 9944 | P2 | Loss | 15596 |
| 5 | `20260920T182135-e49b402e4239` | Stardust-repaired | `sscai/(2)Benzene.scx` | 9945 | P1 | Loss | 11349 |

Run manifests are under the preserved run directories named by these IDs. Every manifest completed with `children_exited`, reciprocal Boolean terminal results, and both child return codes equal to zero. Individual durable completion times were 3.829s, 5.372s, 4.719s, 32.689s, and 8.893s; the cohort elapsed time was 32.738s, below the 300s per-game and 900s cohort caps.

## Replay and telemetry integrity

Each game has exactly two archived replay copies, for ten total. All ten copies exist, have `archival_status: copied`, and their recorded SHA-256 values match recomputation. Independent `screp -cmds=true -computed=true -map=false -indent=false` parsing exited zero for all ten copies, produced valid JSON, and reported no parse-error commands. Every copy satisfies `replay_header_frames + 1 == owning_callback_frame`; replay header races match the configured races in all ten copies.

The candidate diagnostic file for each game matches the manifest result metadata in all substantive telemetry fields. The runner adds `metadata_path` to the manifest-side object, so that generated path field is the only expected difference. The scaling fields are present with integer values in all five games. Games 1, 2, 4, and 5 each reached eligibility, accepted exactly one Singularity Charge command, and recorded completion. Game 3 coherently had no eligibility opportunity and retained the registered `-1`/zero sentinels.

The candidate and opponent modules launched in every match hash to the frozen schedule identities. The schedule entries and `config/bot-identities.json` agree on Ours/Original/Port/Fork labels and source provenance. The candidate binary, source, combined source, patch, plan, engine, and sidecar hashes above were independently recomputed.

## Registered gate outcomes

The cohort had five valid short-terminal games, one verified Kestrel win, five valid integrity grades, five replay-hash matches, five complete replay parses, and zero command rejections. Construction bookkeeping passed in all five games. Probe reserve telemetry passed in all five games with seven reserve-block observations. The v37 scaling telemetry had four eligible lanes, four accepted upgrades, four completed upgrades, four accepted fifth-Gateway extensions, one fifth Gateway that became current, and one seventh Pylon that was accepted, became current and completed. No Pylon or post-Core Gateway cap violation occurred. The matched ZZZK opening gate passed: the second Gateway became current before the first qualifying threat, and two completed Kestrel combat units were present at that threat.

The retained emergency episode telemetry recorded five passing episode grades and four assignments, but `emergency_episode_cap_blocks` was zero across all Zerg lanes. The preregistered requirement called for at least one qualifying episode and one cap-block opportunity across the Zerg lanes. The episode mechanism therefore remains unvalidated, and the candidate cannot be adopted.

## Matched v15 comparison

Both screens used the same five maps, seeds, slots, opponents, engine identity, and wall caps. v15 recorded five losses and zero wins; v16 recorded four losses and one win. Both cohorts had five valid integrity grades and complete replay evidence. v15 had 77 accepted builds, zero Probe reserve blocks, and zero emergency cap blocks. v16 had 84 accepted builds, seven Probe reserve blocks, four completed range upgrades, four fifth-Gateway observations, and one seventh-Pylon observation, while emergency cap blocks remained zero.

The matched ZZZK row changed from a v15 loss at candidate frame 29360 to a v16 win at frame 11721. The first qualifying threat was frame 3765 with two local completed combat units in v15 and frame 3771 with two in v16; second Gateway current was frame 2098 versus 2108. These are matched descriptive outcomes, not an isolated causal estimate: the v37 bundle changes upgrade timing and production caps together, and five games cannot separate their effects.

## Uncertainty and next hypotheses

This is a small matched screen, not Elo evidence. The v16 win is encouraging but cannot establish a general strength gain or tournament transfer. The v37 treatment bundles Singularity Charge banking, a ten-Pylon cap, and a six-Gateway post-Core cap, so the result cannot identify which component produced the improvement. The unobserved emergency cap-block opportunity means the retained defense mechanism remains a decision gate rather than a measured success.

The next experimental lineage may preserve the v37 win signal while testing one isolated combat-cohesion change, but v37 itself did not advance and the new candidate must pass its own preregistered screen before any held-out confirmation. Later ablations can separate range research from the production caps. A targeted Zerg lane may exercise the cumulative two-Probe cap-block path, but it remains diagnostic and cannot replace a registered strength confirmation.

No Elo update, promotion, public submission, or tournament claim follows from this result.
