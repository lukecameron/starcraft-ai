# Kestrel v33 two-Probe emergency Zerg bridge result

## Decision: INCONCLUSIVE

The registered five-game screen did not produce a valid five-game cohort. Four games completed as verified losses, while the ZZZKBot lane reached the 300-second wall cap at 964,800 logical frames with no terminal result or replay. The preregistered decision rule makes an infrastructure-invalid attempt or cohort `INCONCLUSIVE`, so v33 does not advance, does not replace canonical v13, and does not update local Elo.

| Opponent / map | Run | Result | Candidate frame | Durable FPS | Emergency-bridge evidence |
| --- | --- | --- | ---: | ---: | --- |
| ZZZKBot / Benzene | `20260920T161814-5e0caf25d8d7` | Timeout / unknown | 964,800 | 3,215.25 | Two batches of two Probes at 3,978 and 4,434; eight accepted attacks; four threat-clear releases; four post-release gathers |
| UAlbertaBot-Terran / Destination | `20260920T161814-cc76bd4a2ea8` | Loss | 15,875 | 2,224.26 | Non-Zerg telemetry inactive |
| UAlbertaBot-Protoss / Heartbreak Ridge | `20260920T161814-9cfceb031f25` | Loss | 14,542 | 2,597.82 | Non-Zerg telemetry inactive |
| McRave-9Pool-treatment / Circuit Breaker | `20260920T161814-47c190f36465` | Loss | 19,812 | 319.99 | Late trigger at 18,660 with no eligible assignment; recorded as an untested opportunity, not a trace inconsistency |
| Stardust-repaired / Benzene | `20260920T161814-c638126c9d7a` | Loss | 15,193 | 1,033.82 | Non-Zerg telemetry inactive |

## Registered gates

**Integrity: FAIL.** The four completed games had child return codes `0/0`, reciprocal Boolean outcomes, two archived replay copies each, matching recorded and measured hashes, full `screp` parsing, and candidate replay headers exactly one frame below the candidate callbacks. The ZZZK attempt timed out after 300 seconds; both children were terminated with return code `-15`, the outcome remained unknown, and no replay was available. Its diagnostics and logs are preserved. The all-five integrity gate therefore fails without retry or replacement.

**Regression: PASS on the preserved diagnostic evidence.** Gas-worker build attempts and build `Unit_Busy` rejections were zero in all five lanes. Candidate rejection was `5/754` in the timed-out ZZZK lane and zero in the other four, for `5/6674 = 0.075%` across the cohort; all five were gather rejections. Maximum Pylons stayed at six. The accepted/current/completed sixth-Pylon frames were `9342 < 9720 < 10241`, `7938 < 8118 < 8639`, `7812 < 8092 < 8613`, `8340 < 8421 < 8942`, and `9630 < 9738 < 10259`. No build-commandability block occurred, so recovery from that retained guard was untested.

**Emergency bridge: INCONCLUSIVE, with coherent observed behavior.** The registered mechanism gate requires both Zerg attempts to be valid, which the timeout prevents. In the ZZZK lane, the first non-worker home threat arrived at frame 3,738 with two completed combat units, so the bridge was initially ineligible. After a local Zealot died at frame 3,978, the completed army fell to one and two eligible Probes were assigned. A second two-Probe batch was assigned at frame 4,434. The batches emitted eight accepted local attacks, never exceeded the two-defender cap, recorded 56 economy exclusions, released at frames 4,134 and 4,458 when the threat cleared, and issued four accepted post-release gather orders. The ordered scalar and trace telemetry agrees. McRave's much later trigger found no eligible assignment under the leave-four and role exclusions; that path is untested rather than a consistency failure. All three non-Zerg lanes kept bridge counters, traces and sentinels inactive.

**Retained stable reserve: PASS on observed telemetry.** Both Zerg lanes kept reserve remote attack orders at zero and accepted repeat home moves at least 96 frames apart. ZZZK reached reserve three at frame 5,754, released surplus offense at frame 5,952 with army four, recorded 39 accepted reserve local attacks and 375 non-reserve remote attacks. McRave reached reserve three at 4,044, had three reserved and local units when the first non-worker home threat was recorded, released surplus offense at 5,286 with army four, recorded 19 local reserve attacks and 4,613 non-reserve remote attacks. The non-Zerg lanes kept reserve telemetry at zero or its `-1` sentinels.

**Performance reporting: COMPLETE.** Durable rates were 3,215.25, 2,224.26, 2,597.82, 319.99 and 1,033.82 logical frames per wall second. No fixed 384-fps gate applied. Candidate callback p99 ranged from 0.01725 to 0.03246 ms, callback max from 1.88304 to 2.91867 ms, and peak RSS from 44.2 MB to 318.6 MB. These are Apple Silicon native OpenBW measurements, not tournament validation.

**Verified-win adoption: FAIL.** The four terminal games were losses and the remaining game had no verified outcome. The candidate has zero verified wins.

## Replay and diagnostic interpretation

The two-Probe bridge behaved as designed when it became eligible, and the four released defenders resumed mining. It did not cover the initial ZZZK contact in this seed because two combat units were already complete at first pressure. After one Zealot died, the bridge reinforced the remaining defender through two short threat episodes. The match then continued for 964,800 logical frames without a winner. Kestrel reached 28 Probes, six Pylons, four Gateways, ten Zealots and 23 Dragoons; it also recorded 25 reserve deaths, a maximum offensive surplus of 20, and 375 accepted non-reserve remote attacks. This is strong survival evidence but poor completion evidence. Without a replay or terminal result, it is not a win, a draw suitable for Elo, or proof that the bridge caused the survival.

The four replay-backed lanes still lost. Their diagnostic maxima show adequate basic production, while McRave recorded 4,613 accepted non-reserve remote attacks and still lost after 19,812 frames. Combined with the ZZZK non-termination, the next screen should test a narrow attack-cohesion or target-completion policy rather than add more static defenders. Fresh seeds and the missing timeout replay prevent a causal v32-versus-v33 comparison of terminal frames.

## Frozen evidence

- Plan SHA-256: `ff74942ad7abde62e084138be272ec08e7ed724445f713ce8590345eecad1d32`.
- Tracked schedule SHA-256: `814afbf21469e8b20ffbf17a38e098b64db589179e09c5b9ef8d5170e13a3194`.
- Archived normalized schedule SHA-256: `991e6ce27278296122efafcbebb50575fc7f269f672bd36ae71a4cc61862391c`.
- Batch manifest SHA-256: `cdce69717f6f0febaf223b06a7f4f18c3e629bac5cb403c57999615696e99c3f`.
- Hill-climb scorecard SHA-256: `906f75a69a375dbbb931320c129b484c4c9cdee99b57b29d7fd5ac74512af403`.
- Candidate binary SHA-256: `1d77b4483ea0fa21db1df9d8b45e15364986b793a2745b2c570f0db2fb55b632`.
- Candidate source SHA-256: `d3c09bc2cd94eaccabefffe0fe76ed542f0e063a2a400a1428fc4b51d79d887a`.
- Combined source SHA-256: `562dc539d1171c5958ce80cbaebef4e53b336c908dc51e7385e75cb0d656cb66`.
- Reconstruction patch SHA-256: `e1765155cff50b27e306b16f6b9c6d562ea9d1aae5746ed1d74854228b3d7276`.
- Engine SHA-256: `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`.

The scorecard is descriptive replay and diagnostic evidence. This heterogeneous screen is not an Elo estimate and is excluded from `config/local-ratings.json`.
