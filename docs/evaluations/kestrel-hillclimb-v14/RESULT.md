# Kestrel v35 construction bookkeeping and emergency-episode result

## Decision: REJECT

The registered five-game cohort completed as five valid, short terminal losses. All five integrity and replay-fidelity checks passed, the v35 construction telemetry was complete in every lane, and the cumulative emergency-episode cap behaved coherently where it was exercised. The required verified-win threshold was `0/5`, so v35 does not advance, does not replace canonical Kestrel v13, and does not update local Elo.

| Opponent / map | Run | Result | Candidate frame | Rejected / attempted | Durable FPS |
| --- | --- | --- | ---: | ---: | ---: |
| ZZZKBot / Benzene | `20260920T172834-a24ddd2354af` | Loss | 6,482 | 0 / 66 | 2,707.53 |
| UAlbertaBot-Terran / Destination | `20260920T172834-10b086b67de6` | Loss | 17,983 | 7 / 598 | 2,742.82 |
| UAlbertaBot-Protoss / Heartbreak Ridge | `20260920T172834-b37083f8e82c` | Loss | 46,193 | 11 / 267 | 2,465.76 |
| McRave-9Pool-treatment / Circuit Breaker | `20260920T172834-d3c44e82dd7b` | Loss | 16,743 | 0 / 3,710 | 437.47 |
| Stardust-repaired / Benzene | `20260920T172834-ddae2ddc1b2b` | Loss | 10,760 | 0 / 240 | 1,266.32 |

## Registered gates

**Integrity: PASS.** Every attempt completed with status `completed`, child return codes `0/0`, reciprocal terminal outcomes, expected map/race/slot/seed, and no timeout or launcher failure. Each game retained two replay copies. All ten recorded replay hashes and sizes matched the archived files, `screp` parsing completed without parse-error commands, and each replay satisfied the owner-frame check (`replay header frames + 1 == owning callback frame`). The concurrent batch took 38.44 seconds; all five games exceeded the descriptive 384 logical-frames-per-wall-second throughput threshold.

**Construction bookkeeping: PASS as a telemetry and source gate; the ZZZK gameplay gate failed.** All five lanes recorded complete v35 accepted-build arrays with aligned frames, type IDs, pre-command counts and post-command counts. The aggregate contained 74 accepted build rows and five complete Gateway sequences. In the fresh ZZZK lane, the first Gateway was accepted/current/completed at `1440/1589/2560`, the second at `2094/2271/3242`, and the first Zealot was trained/completed at `2592/3197`. The second Gateway was current before the first qualifying home threat at frame `3789`, but only one completed combat unit was present globally and locally at that threat. The registered gate required two, so the construction hypothesis did not produce the required opening state.

**Emergency episode cap: PASS where exercised, with recovery untested.** The ZZZK lane began one continuous episode at frame `3792`, assigned exactly two unique Probe identities in one batch, accepted ten local attack orders, recorded two defender deaths, and blocked further assignment while the episode remained active. The scorecard recorded 116 cap-block frames. No replacement was accepted after the two identities were consumed. McRave recorded twelve public threat episodes without an eligible assignment; both Zerg lanes retained complete episode telemetry. No threat-clear or army-three release occurred, so post-release recovery was untested. The three non-Zerg lanes kept v35 episode and bridge activity at their inactive sentinels.

**Retained reserve and staged offense: PASS where observed, with opportunities untested.** McRave reached the registered surplus-six release at frame 7,314 with army nine and reserve three, blocked 390 pre-release remote attempts, accepted 3,142 post-release remote attempts, and cleared the latch at surplus zero at frame 15,036. Its first qualifying home threat had three global and local combat units at frame 4,404. The other Zerg lane did not reach the staged-offense threshold. Non-Zerg staged-offense and reserve telemetry remained inactive.

**Regression: PASS.** Gas-worker build attempts and build `Unit_Busy` rejections were zero in every game. Candidate command rejection stayed below 5% in every lane: `0/66`, `7/598`, `11/267`, `0/3710`, and `0/240`, or `18/4,881 = 0.369%` pooled. Maximum Pylons were `1, 6, 6, 6, 5`. The observed sixth-Pylon timings were ordered: UAlberta-Terran `9090 < 9228 < 9749`, UAlberta-Protoss `7974 < 8220 < 8741`, and McRave `9168 < 9425 < 9946`. The retained commandability guard did not block in these games.

**Verified-win adoption: FAIL.** All five terminal outcomes were Kestrel losses. This fails the preregistered advancement threshold independently of the descriptive mechanism passes.

## Replay-grounded interpretation

The construction fix changed the public sequence enough to make the second ZZZK Gateway current well before the first threat, but that timing alone did not put a second combat unit on the field. The first Zealot completed at frame 3,197, the second Gateway completed at frame 3,242, and the first qualifying threat arrived at frame 3,789. The result leaves too little time for the second Gateway to produce and complete another Zealot. The bridge then held its cumulative cap exactly: the two assigned Probes both died, and no replacement chain was allowed. This is a useful mechanism result, not a strength result.

The McRave replay shows the retained reserve and surplus-six staging state working through a longer game: three units were local at the first real home threat, and the staged army was released and later exhausted. Kestrel still lost at frame 16,743. UAlberta-Terran and Stardust reached losses after Kestrel produced broader armies, while UAlberta-Protoss ran to frame 46,193 before a loss. These are descriptive replay signals only; they do not establish a causal change or a local Elo result.

The next bounded candidate should preserve the reviewed v35 telemetry and cap as diagnostic foundations, then target the remaining early-combat timing gap with one narrow change: get the second completed combat unit online before the first qualifying ZZZK pressure. A separate cohesion or attack-completion screen remains preferable for the McRave midgame loss. These heterogeneous five games are excluded from `config/local-ratings.json`.

## Frozen evidence

- Plan SHA-256: `1e5532403a508ffc7323c86331c43ec2f03ff0a066e374d70955057df09a1d18`.
- Tracked schedule SHA-256: `7f62f9166eb551ca2cd1277aa311c1614986118ebff42c36f67a632a63de1f07`.
- Archived normalized schedule SHA-256: `042012fe3e8a2b6ec4c6b5f6acd94d07f6746dcf140de2984812e4875c4d1289`.
- Batch manifest SHA-256: `07b6bd4639a88d4a7d1c4867d0e1932cf330c28f07c95cc6263bb270d0de5086`.
- Hill-climb scorecard SHA-256: `806fd608aac3b1129e8eb114f471b9f45e8401217eca89e447d589774ed94a1f`.
- Candidate binary SHA-256: `8e85a4389b18caf7f55d857d81889e1d7ecfa4d41333794a5797f69a10769270`.
- Candidate source SHA-256: `e81637c5fe1251786bebe9c63aa577aacf8bbd935766d320dbb16574059907af`.
- Combined source SHA-256: `05ac2402858f7765710e95f5c3414fd698857f76afe407c502faa2956a3e025e`.
- Reconstruction patch SHA-256: `46e441080a8d599427bbdf111591be2ae47faa77fb99d7d6a8fb4dfd605bb023`.
- Engine SHA-256: `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`.

The scorecard combines replay-derived diagnostic signals with public callback telemetry. It is not an Elo estimate, promotion evidence or tournament validation.
