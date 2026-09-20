# Kestrel v36 opening reserve hill-climb result

## Decision: REJECT

The registered five-game cohort completed as five valid, short terminal losses. All replay and manifest integrity checks passed, the v36 telemetry was complete and aligned, and the non-Zerg reserve fields stayed inactive. Neither Zerg lane observed a qualifying 200..299-mineral idle-Nexus reserve-block opportunity, so the reserve mechanism is `UNTESTED`; the emergency episode cap also observed zero cap-block opportunities. The required verified-win threshold was `0/5`, so v36 does not advance, replace canonical Kestrel v13, or update local Elo.

| Opponent / map | Run | Result | Candidate frame | Rejected / attempted | Durable FPS |
| --- | --- | --- | ---: | ---: | ---: |
| ZZZKBot / Benzene | `20260920T175750-68f4313b16ab` | Loss | 29,360 | 7 / 954 | 3,055.31 |
| UAlbertaBot-Terran / Destination | `20260920T175750-e16825ab884f` | Loss | 17,859 | 2 / 548 | 2,238.05 |
| UAlbertaBot-Protoss / Heartbreak Ridge | `20260920T175750-de8083382e65` | Loss | 12,186 | 0 / 197 | 2,067.90 |
| McRave-9Pool-treatment / Circuit Breaker | `20260920T175750-53f8cbbcb6bd` | Loss | 16,991 | 0 / 4,079 | 457.05 |
| Stardust-repaired / Benzene | `20260920T175750-9bbc4c6e562c` | Loss | 11,132 | 0 / 228 | 1,295.03 |

## Registered gates

**Integrity: PASS.** All five attempts completed with status `completed`, both child return codes zero, reciprocal terminal outcomes, expected maps, races, slots and seeds, and no timeout or launcher failure. Each game retained two replay copies. All ten recorded replay hashes and sizes matched the archived files, `screp` parsing completed without parse-error commands, and the replay owner-frame checks passed. The five-game batch completed in 37.33 seconds. Every game exceeded the descriptive 384 logical-frames-per-wall-second threshold.

**Construction bookkeeping: PASS.** The v35 pre-command baseline and pending-release telemetry remained complete in all five lanes. The cohort contained 77 accepted build rows and five ordered Gateway sequences. The source and aligned arrays passed their registered consistency checks.

**Probe reserve: UNTESTED in both Zerg lanes.** ZZZK recorded `opening_probe_reserve=0`, `max_opening_probe_reserve=250`, reserve window `816..2100`, and accepted Probe train frames beginning `0, 438, 2496, 2802, 3138, 3588, 4854, ...`. McRave recorded maximum reserve `250`, window `858..2112`, and accepted Probe train frames beginning `0, 384, 2544, 2850, 3216, 3522, ...`. Both lanes recorded zero reserve-block frames and zero reserve-block minerals, with the registered opportunity note `reserve_block_opportunity_unobserved`. The first post-window Probe acceptance was after second-Gateway current in each lane. The refreshed scorecard grades both Zerg reserve mechanisms `untested`; it does not treat the absence of an opportunity as evidence that the reserve suppressed a command.

The raw ZZZK reserve-window endpoint is frame `2100`, two frames after second-Gateway current at `2098`; the refreshed cadence-aware scorer accepts the ordered telemetry, but this sampling detail should remain visible in later reports.

**Matched ZZZK opening: PASS as an observed timing state, not as a causal reserve result.** v36 reached the second Gateway current at frame `2098`, first Zealot train/complete at `2538/3143`, and the first qualifying threat at `3765` with two global and two local completed combat units. The first home combat loss was frame `22537`, or 18,772 frames after the threat. The emergency episode assigned Probe IDs `[131, 136]` at frame `3768`; no cumulative cap-block opportunity was observed and neither defender died in the recorded episode.

The matched v35 row reached second-Gateway current/completed at `2271/3242`, first Zealot train/complete at `2592/3197`, and threat at `3789` with one global and one local completed combat unit. Its first home combat loss was frame `3884`, only 95 frames after threat. v35 assigned IDs `[136, 128]` at `3792`, recorded 116 cap-block frames and two defender deaths. The v36 row therefore shows earlier Gateway timing, two units at pressure and much longer survival in this matched scenario. It does not establish that the 250-mineral reserve caused the improvement because no reserve-block opportunity was observed.

**Emergency episode cap: UNTESTED for the cap-block gate.** The v36 scorecard contains coherent episode telemetry and exactly two assigned identities in the ZZZK episode, but both Zerg lanes recorded zero cumulative-cap block opportunities. No replacement suppression after a defender death can be validated from this cohort.

**Retained reserve and staged offense: PASS where exercised.** The two Zerg lanes retained the v34 reserve and v35 staged-offense telemetry. ZZZK reached reserve peak three, recorded 65 reserve local-defense attack orders, 250 reserve remote-order blocks, 140 staged pre-release blocks and 461 post-release remote accepts. McRave reached reserve peak three, recorded 33 local-defense attacks, 342 reserve remote-order blocks, 613 staged pre-release blocks and 3,628 post-release remote accepts. The three non-Zerg lanes kept all Zerg-only fields at inactive sentinels.

**Regression: PASS.** Gas-worker build attempts and build `Unit_Busy` rejections were zero in every lane. Candidate command rejection was below 5% in every attempt: `7/954`, `2/548`, `0/197`, `0/4079`, and `0/228`, or `9/6006 = 0.150%` pooled. No game exceeded six Pylons. The observed sixth-Pylon traces were ordered in ZZZK (`8934 < 9107 < 9628`) and McRave (`8490 < 8541 < 9062`); the other lanes did not observe a sixth Pylon.

**Verified-win adoption: FAIL.** Every terminal outcome was a Kestrel loss. This independently fails the registered advancement threshold.

## Replay-grounded interpretation

The clearest matched signal is the ZZZK opening. v36's second Gateway current frame was 173 frames earlier than v35's, and v36 had two completed combat units at the first qualifying threat where v35 had one. v36 survived the initial pressure and continued to frame 29,360, while v35 lost its first home combat unit at frame 3,884. This is matched descriptive evidence only; the reserve itself never blocked a qualifying Probe opportunity.

Across the five lanes, replay-filtered `screp` attack orders changed v35 to v36 as follows: ZZZK `26→577`, UAlberta-Terran `386→271`, UAlberta-Protoss `106→66`, McRave `3498→3849`, and Stardust `101→84`. Filtered harvest orders were `19→66`, `46→60`, `77→44`, `42→47`, and `43→42`. Callback production telemetry recorded accepted Zealot trains of `5→19`, `9→35`, `8→11`, `17→16`, and `6→8` respectively. These counts describe different command layers and should not be treated as accepted-command equivalence.

The non-Zerg rows changed materially despite inactive reserve fields: UAlberta-Terran's second Gateway current moved from `3262` to `4151` and first home combat loss appeared at `9957`; UAlberta-Protoss ended at frame `12186` rather than `46193`; Stardust's second Gateway current moved from `4294` to `3664`. The exact causal interpretation is unresolved in this matched screen and requires a determinism/input audit before attributing those changes to v36.

## Next bounded hypotheses

1. Add a targeted reserve-opportunity fixture or held-out lane that actually reaches an idle Nexus with 200..299 minerals, then rerun the reserve change with the same public telemetry and an explicit block-count gate.
2. Preserve the v36 ZZZK opening and test one narrow production change that creates additional margin between second-Gateway current and the first qualifying threat; require two completed combat units before threat on held-out seeds.
3. Audit non-Zerg matched determinism, including exact candidate binary, source, engine, bot seeds and runtime inputs, before interpreting the large UAlberta-Terran and UAlberta-Protoss timing shifts.
4. Test McRave combat cohesion and target persistence separately. v36 issued more attack activity and more post-release remote accepts, but reached loss with fewer local completed Zealots (`10` versus v35's `15`), so command volume did not translate into a stronger final engagement.

## Frozen evidence

- Evaluation plan SHA-256: `d832c7d7ddde924aaadc6167a86ff8d3730b1d55bdf01b0fa65456bd3d3d8836`.
- Tracked schedule SHA-256: `c23fbd7385cbe2a97ffbf871d3a6c0096aeae7bd5f0818231f5d462e86e1299d`.
- Persisted batch schedule SHA-256: `6bcf13f874138e6e7cf9611461b587f91cd8daf384117d2a6613af97309b724e` (canonicalized JSON written by the batch runner).
- Batch ledger / manifest SHA-256: `89fc9ebd1af811a1cae6a25ca901e5d545f45435481cbf33c663382c0c9c339c`.
- Regenerated hill-climb scorecard SHA-256: `512cdc6460efc3b7ee60e16dbce6e3bb25d245eb678de33aa6e686163ee8cae4`.
- Candidate binary SHA-256: `c2e95394fd5c8c6a6dcd4ae2d7a8f1460624d454a906c6dba3e3e32bfb960b85`.
- Candidate source SHA-256: `a8f884c4dea4d3dfd4a91708763b35457c330f1bf4b89a6c12bdcbd0092effc3`.
- Combined source SHA-256: `81b1d8ed7e0879dbd9b36716fa4922e9366bddcc4d64ca6b6e77e70adff6fdbb`.
- Reconstruction patch SHA-256: `02633bc1a78d1f5ffffd1b051c7e67d5672b485fef4f2d91cd94d4eaea9aa371`.
- Engine SHA-256: `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`.
- Candidate provenance: `Ours` / `Original` / Luke Cameron; source `https://github.com/lukecameron/starcraft-ai/tree/main/bots/kestrel`.

The scorecard and replay heuristics are descriptive. This heterogeneous matched screen is excluded from `config/local-ratings.json` and is not tournament validation.
