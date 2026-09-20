# Kestrel v34 bridge-threshold and staged-offense result

## Decision: REJECT

The registered cohort produced five valid, short terminal losses. Every integrity gate passed, the staged-offense mechanism exercised coherently against McRave, and the three non-Zerg lanes kept the Zerg-only telemetry inactive. The adoption rule also required at least one verified Kestrel win. The observed result was `0/5`, so v34 does not advance, does not replace canonical Kestrel v13, and does not update local Elo.

| Opponent / map | Run | Result | Candidate frame | Rejected / attempted | Durable FPS |
| --- | --- | --- | ---: | ---: | ---: |
| ZZZKBot / Benzene | `20260920T165258-965c2455153f` | Loss | 5,862 | 0 / 82 | 2,615.34 |
| UAlbertaBot-Terran / Destination | `20260920T165258-50963d417a62` | Loss | 25,392 | 17 / 1,049 | 1,322.51 |
| UAlbertaBot-Protoss / Heartbreak Ridge | `20260920T165258-ed9ffbd12dac` | Loss | 13,705 | 0 / 296 | 2,402.33 |
| McRave-9Pool-treatment / Circuit Breaker | `20260920T165258-69e69e4b3977` | Loss | 15,937 | 0 / 2,698 | 487.50 |
| Stardust-repaired / Benzene | `20260920T165258-e803a260d474` | Loss | 10,605 | 0 / 204 | 1,338.59 |

## Registered gates

**Integrity: PASS.** All five manifests completed with two zero child return codes, reciprocal Boolean outcomes, the expected races, maps, slots and seeds, and no timeout. The cohort finished in 32.85 seconds. All ten archived replay copies matched their recorded size and SHA-256, matched the run-local source copies, parsed through `screp` with no parse-error commands, and satisfied `replay_header_frames + 1 == owning_callback_frame`. The runner's archived normalized schedule SHA-256 is `eb99031b344f37887a0e497ad1ca3173d43fbbf463e7df12b17cb40dd4fad85f`.

**Emergency bridge: PASS where exercised, with recovery untested.** ZZZK triggered at frame 3,696 with one completed local combat unit. The bridge assigned six Probe identities in batches `[2, 1, 1, 1, 1]`, never exceeded two simultaneous defenders, accepted 37 local attacks and recorded 163 economy exclusions. All six assigned Probes died, so no threat-clear or army-three release occurred and post-release economy recovery was untested. McRave recorded later qualifying triggers with no eligible Probe assignment; this is an opportunity note rather than a trace inconsistency. The non-Zerg lanes kept every bridge counter and sentinel inactive.

**Staged nonreserve offense: PASS where exercised.** McRave reached surplus seven and army ten at frame 8,346. The state trace released seven IDs at that frame, blocked all 582 recorded pre-release remote attempts, accepted all 2,267 recorded post-release remote attempts, stayed latched while surplus was positive, and cleared at frame 13,836 with observed surplus zero and cause `surplus_zero`. Home staging accepted 18 of 18 move attempts with a minimum repeated interval of 96 frames. ZZZK never reached a nonreserve surplus and its threshold transition was untested. This satisfies the registered cohort gate because one Zerg lane exercised the transition. The non-Zerg lanes kept all staged-offense fields inactive.

**Retained reserve: PASS.** McRave reached a stable reserve of three at frame 4,206 and had all three local at the first qualifying home threat. It recorded 263 remote-order suppressions, 26 accepted local-defense attacks, zero reserve remote attacks, and later accepted nonreserve offense after the v34 release. ZZZK recorded two remote suppressions, eight local-defense attacks and zero reserve remote attacks. Accepted repeated reserve home moves were at least 96 frames apart.

**Regression: PASS.** Gas-worker build attempts and build `Unit_Busy` rejections were zero. The 17 rejected commands were UAlberta-Terran gather attempts; the per-game rate was 1.621% and the cohort rate was `17/4329 = 0.393%`, both below 5%. No game exceeded six Pylons. The three observed sixth-Pylon accepted/current/completed traces were ordered: `11844 < 11955 < 12476`, `8220 < 8378 < 8899`, and `9252 < 9458 < 9979`. UAlberta-Terran exercised the retained build-commandability guard at frame 7,680 and later accepted construction at frame 11,844.

**Verified-win adoption: FAIL.** Every terminal outcome was a Kestrel loss. The coherent mechanism traces are diagnostic evidence and do not override the registered win threshold.

## Replay interpretation

The clearest failure is the ZZZK opening. The first Zealot completed at frame 3,347, pressure arrived at 3,692, and the first local Zealot died at 3,889 before the second completed combat unit was available. Replacing dead bridge defenders caused six Probe deaths while Kestrel peaked at ten Probes, three Zealots and no Dragoons. The simultaneous two-Probe cap worked, but it did not bound cumulative worker loss through one continuous threat episode.

The McRave screen proves that v34 can hold a surplus at home and release it as one larger group. That group still traded down from a peak surplus of 16 to zero. McRave's replay records a substantially broader Zerg economy and production mix, including Mutalisks, Zerglings, five Hatcheries and five Sunken Colonies. The result supports keeping the staging mechanism as a measured foundation while testing how Kestrel concentrates and completes attacks; it does not prove that a different release threshold alone would win.

The non-Zerg losses expose scaling and cohesion limits outside the registered Zerg changes. UAlberta-Terran survived to frame 25,392 and outproduced Kestrel heavily. Against UAlberta-Protoss and Stardust, player-filtered replay commands show Kestrel repeatedly issuing attacks through a small number of unit tags, while the opponents produced larger combat totals. Stardust began Dragoon production thousands of frames before Kestrel. Command traces do not prove unit arrival or battlefield causality, so these are candidate hypotheses rather than promotion evidence.

## Ranked next changes

1. Advance the second Zerg Gateway or second Zealot enough to put two completed combat units at home before the observed frame-3,692 ZZZK pressure window.
2. Cap emergency assignments at two cumulative Probe identities per continuous threat episode so deaths cannot consume a replacement chain; allow a fresh pair only after a documented threat-clear transition.
3. Preserve the measured v34 reserve and surplus-six stage while testing a shared combat-group target with bounded retargeting, rather than per-unit serial target selection.
4. Add a separately measured midgame Protoss production screen for singleton tech rebuilding and earlier continuous Dragoon production.
5. Treat the UAlberta-Terran gather `Unit_Busy` path as robustness cleanup; it is isolated and not the main strength failure.

The next hill-climb should make only the first two Zerg-opening changes. The cohesion and Protoss-production hypotheses need their own telemetry and bounded screens rather than being selected together from this five-game result.

## Frozen evidence

- Plan SHA-256: `16c62d893a1e84232bda0d2f647d1862165063434d4680c5e36cc695fb60aac1`.
- Tracked schedule SHA-256: `74f56daec176788b1d15a00e99d8a027382b06c5582af37fc38ef1fcb626d788`.
- Archived normalized schedule SHA-256: `eb99031b344f37887a0e497ad1ca3173d43fbbf463e7df12b17cb40dd4fad85f`.
- Batch manifest SHA-256: `354165e6660ad6eb53858a00de28408e8b9d08a53c301c226aa1de57827b488c`.
- Hill-climb scorecard SHA-256: `10d3a5b124e8120e4635015c47a1c8acb06a27f51800737284686de476fe7cba`.
- Candidate binary SHA-256: `f71a1dc353a89c1770a05c59b21ae4907aebb7650d87cbb3af9239137a4b763a`.
- Candidate source SHA-256: `947b64fb0c6510bfbf32024850e9e517842f22349d8ac27a59f61d63897cf8bd`.
- Combined source SHA-256: `9d182a0f6db463bb5a6cf9ee16cd4b157988edd1626ce3d48e5b1630efaa9815`.
- Reconstruction patch SHA-256: `0e0c21d9957c1e9d5d506355a5af357e0b887406de14399e91f8310ab941dca1`.
- Engine SHA-256: `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`.

The scorecard and replay heuristics are descriptive. This heterogeneous screen is excluded from `config/local-ratings.json` and is not tournament validation.
