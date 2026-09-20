# Kestrel v32 stable three-unit Zerg reserve result

## Decision: REJECT for advancement

The five-game screen completed validly and the registered reserve mechanism passed, but Kestrel lost all five games. The registered adoption rule requires at least one verified win, so v32 does not advance, does not replace canonical v13, and does not update local Elo.

| Opponent / map | Run | Result | Candidate frame | Durable FPS | Reserve evidence |
| --- | --- | --- | ---: | ---: | --- |
| ZZZKBot / Benzene | `20260920T155249-f10d4c5796a5` | Loss | 5,490 | 2,595.18 | Peak 2; threat at 3,695 with 1/1 global/local combat; first loss 3,821; no surplus release |
| UAlbertaBot-Terran / Destination | `20260920T155249-6b174c7d4dcb` | Loss | 15,999 | 2,470.65 | Non-Zerg telemetry inactive |
| UAlbertaBot-Protoss / Heartbreak Ridge | `20260920T155249-1df24b730444` | Loss | 33,483 | 1,365.24 | Non-Zerg telemetry inactive |
| McRave-9Pool-treatment / Circuit Breaker | `20260920T155249-561366d52347` | Loss | 16,433 | 477.88 | Reserve 3 at 4,296; threat 4,307 with 3/3 reserved and local; surplus release 5,352 at army 4 |
| Stardust-repaired / Benzene | `20260920T155249-8e9baecf77fe` | Loss | 15,038 | 1,072.78 | Non-Zerg telemetry inactive |

## Registered gates

**Integrity: PASS.** All five manifests completed with both child return codes zero, reciprocal Boolean outcomes, no timeout, `launch_error: null`, and expected races. All ten archived replay copies match their manifest hashes, parse with `screp` without parse-error commands, and satisfy `replay_header_frames + 1 == owning_callback_frame`.

**Regression: PASS.** Gas-worker build attempts and build `Unit_Busy` rejections were zero in every game. Command rejection was `0/37`, `0/386`, `10/282`, `0/1679`, and `0/502`; the cohort rate was `10/2886 = 0.3465%`, and every lane remained below 5%. Maximum Pylons were `1, 6, 6, 6, 6`. Every observed sixth Pylon had ordered accepted/current/completed frames: UAlberta-Terran `8634 < 8744 < 9265`, UAlberta-Protoss `8178 < 8336 < 8857`, McRave `8760 < 8993 < 9514`, and Stardust `9624 < 9870 < 10391`. No build-commandability block occurred, so recovery from that guard was untested.

**Stable-reserve mechanism: PASS.** Both Zerg games were valid. Reserve remote attack orders remained zero, and accepted home moves did not exceed attempts. ZZZK accepted one of one home move; it never had three simultaneous completed reserve units, so the three-unit milestone was untested there. McRave reached reserve peak three at frame 4,296. At the first qualifying threat on frame 4,307 it had three global combat units, three reserve units and all three reserve units local. It recorded 373 remote-target suppressions, 57 accepted local-defense attacks, zero reserve remote attacks, and 1,286 non-reserve remote attacks. Its first surplus release was frame 5,352 at army size four. Accepted repeat home moves were at least 96 frames apart. The three non-Zerg lanes kept all new counters at zero and milestones at their `-1` sentinels.

**Performance reporting: PASS.** Every game completed below the 300-second cap and the concurrent cohort completed in 34.54 seconds, below 900 seconds. Durable FPS ranged from 477.88 to 2,595.18. Candidate callback p99 was at most 0.02475 ms, callback max at most 4.66221 ms, callback CPU at most 0.177395 seconds, and candidate peak RSS ranged from 42.41 to 46.36 MiB. These are Apple Silicon native OpenBW measurements, not tournament validation.

**Verified-win adoption: FAIL.** The candidate scored 0–5. No mechanism or engineering result can substitute for the frozen win requirement.

## Replay-grounded interpretation

The explicit reserve fixed the v31 defects it targeted. In the McRave lane, v31 emitted 776 accepted home moves and had only one of five combat units local at the first real pressure. V32 emitted 57 accepted home moves across a much longer defensive sequence, enforced a 96-frame minimum repeat interval, and had all three completed combat units reserved and local at first pressure. Three distinct combat actors issued local attacks together after the threat. The surplus army still attacked, so the reserve did not freeze offense.

The ZZZK lane exposes the next constraint. Only one combat unit was complete when pressure arrived at frame 3,695, and the first local loss followed 126 frames later. The second local defender arrived before that loss, but the three-unit reserve never formed. V32 reduced accepted home moves from v31's 101 to one, but command-state repair cannot create the missing early body. A future candidate should bridge this short one-defender window without reintroducing v9's costly six-Probe pull. Fresh seeds prevent causal comparison of terminal frames across v31 and v32.

## Frozen evidence

- Plan SHA-256: `a32332efdd83212df2714e603d62597dc91c28e4b2607cfc3135749c2f0d0849`.
- Tracked schedule SHA-256: `a813a9c4e37692c8a9e2d7f701cc45c066ff7c4e606a3ae1671d02190e7e932d`.
- Canonically persisted schedule SHA-256: `69ecf351da147640d1ad3031239a264df2865dfd88cf4b2b35fd5709d6050f73`.
- Batch manifest SHA-256: `e8ce72b0da01a663423397190193dc6b2953fded44fb8ba4869d0f27ac5dc58a`.
- Hill-climb scorecard SHA-256: `16d54438f8b50e5bc99affb0d55d8d49f7ba303c61b498e1fe9392a1376cf822`.
- Candidate binary SHA-256: `3809371159c53fee4b761227d0d4d91d5b45bb5342ddda0be3ab73eba0a9899d`.
- Candidate source SHA-256: `7d5dd3a025b7d6728a9e4c50bd2471ca6d60286b1dcece9caabe4ecc4142d599`.
- Reconstruction patch SHA-256: `7ab53d2036addac5dcb6464c8ce24d318093dcc8c688d26de2dff8dac91c0e10`.
- Engine SHA-256: `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`.

The scorecard is descriptive replay and diagnostic evidence. This five-game heterogeneous cohort is not an Elo estimate and is excluded from `config/local-ratings.json`.
