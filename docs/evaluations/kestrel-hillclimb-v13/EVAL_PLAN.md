# Kestrel v34 two-Probe threshold and staged-offense hill-climb

Drafted 2026-09-21 before v34 source changes, compilation, or gameplay. This is a preregistered five-game exploratory screen from the exact frozen Kestrel v33 candidate in `kestrel-hillclimb-v12`. It combines exactly two Zerg-only policy changes: extend the existing two-Probe emergency bridge through completed combat army size two, and stage nonreserve combat units at home until a six-unit surplus is observed before latching them into offense until that surplus reaches zero.

## Decision

- **Change under evaluation:** Kestrel v34, with only the two registered Zerg policy changes below applied to the exact v33 source and binary lineage.
- **Decision this evaluation controls:** Whether v34 may proceed to a separately registered held-out confirmation screen. It does not replace canonical Kestrel v13 and it cannot update local Elo.
- **Adoption threshold:** Every integrity, short-terminal, regression, provenance, v33 bridge, v32 reserve, and v34 staged-offense gate must pass, and the five-game cohort must contain at least one verified Kestrel win.

## Hypothesis

The existing v33 two-Probe bridge will cover the remaining early Zerg pressure window when the completed combat army is two, releasing only when the army reaches three or the threat clears. Holding nonreserve combat units at home until six units of surplus are available, then latching those units into offense until surplus reaches zero, will reduce premature split attacks and produce a more coherent completion attempt without changing Protoss, Terran-opponent, or non-Zerg policy behavior.

The hypothesis is falsified for this screen if a valid cohort has no verified win, if either registered mechanism violates its state machine, if a change leaks into a non-Zerg lane, or if the retained production, commandability, reserve, or provenance gates fail. A timeout, missing terminal result, or other infrastructure-invalid attempt is `INCONCLUSIVE`, not evidence that the gameplay hypothesis failed.

## Design

### Control

The control is the exact frozen Kestrel v33 candidate from `kestrel-hillclimb-v12`, including its two-Probe emergency bridge, v32 three-unit Zerg reserve, 96-frame home-move retry bound, production and economy policy, gas-worker guard, and all other behavior. The v33 binary/source identities are recorded below and in the v12 schedule; they must not be rebuilt or silently substituted.

### Treatment: exactly two Zerg-only changes

1. **Bridge threshold.** Preserve the v33 public-observation trigger, eligible-Probe rules, two-defender cap, economy/build exclusions, and attack handling. While a visible, detected, non-worker, attack-capable Zerg threat is inside the existing local home-threat radius, the bridge is active while completed Kestrel combat army size is **at most two**. Release every surviving bridge defender when the threat clears or completed combat army size reaches **three or more**. A defender death removes only that identity. No hidden state, evaluator/replay state, scout contact, or cross-frame enemy cache may trigger it.
2. **Staged nonreserve offense.** Preserve the v33 three-unit reserve and its local-defense behavior. Define `nonreserve_surplus` at each policy decision as the number of completed Kestrel combat units not in the stable reserve. Keep nonreserve units in the existing home/staging behavior while `nonreserve_surplus < 6`, suppressing their remote-offense orders during that state. At the first observed `nonreserve_surplus >= 6`, release eligible nonreserve units into the existing offense target handling. Once released, latch the released state until `nonreserve_surplus == 0`; do not restage or oscillate while surplus remains positive. The latch may end because units die, but it must not be cleared merely because surplus falls below six. This change must not alter the reserve's local-defense restrictions or any non-Zerg behavior.

There are no planned ablations in this five-game screen. The two changes are one preregistered treatment so that any follow-up confirmation can test the combined policy without selecting a favorable sub-result after inspection.

### Frozen five-game screen

Run exactly five fresh candidate attempts concurrently, with no retry, reseeding, replacement, or control rerun:

| Game | Opponent | Map | Kestrel slot | Engine seed |
| ---: | --- | --- | ---: | ---: |
| 1 | ZZZKBot | Benzene | P1 | 9931 |
| 2 | UAlbertaBot-Terran | Destination | P2 | 9932 |
| 3 | UAlbertaBot-Protoss | Heartbreak Ridge | P1 | 9933 |
| 4 | McRave-9Pool-treatment | Circuit Breaker | P2 | 9934 |
| 5 | Stardust-repaired | Benzene | P1 | 9935 |

Use a 300-second wall cap per game and a 900-second cohort cap with concurrency five. Preserve every manifest, runner log, diagnostic, replay, hash, parse result, and failure record. Do not silently score an unfinished match. Stop after two consecutive infrastructure-invalid attempts or the cohort cap. A timeout or missing terminal result is `INCONCLUSIVE`; a valid, fully parsed, short terminal loss is `REJECT` evidence. A short verified terminal game means the engine delivered a terminal callback and reciprocal terminal result before the 300-second wall cap, with both archived replay copies owned by that terminal callback and parsed without errors.

## Primary metric

- **Name:** verified candidate wins in the five-game cohort.
- **Direction and unit:** higher is better; integer wins per five valid, short terminal games.
- **Exact formula:** `verified_win_count = sum(1 for game in games if integrity_pass and short_terminal_pass and candidate_terminal_result == "win")`.
- **Source fields:** final manifest terminal result, lifecycle status, child return codes, wall-cap status, replay-copy hashes, replay header frame, owner callback frame, expected races, and complete `screp` parse result.
- **Threshold:** at least one verified win, in addition to every mechanism and regression gate. This exploratory screen does not convert the count into an Elo update.

Secondary reports must include terminal frame and durable logical FPS per game, callback p99/max and CPU time, peak RSS, command rejection rates, and the complete bridge, reserve, and staged-offense telemetry. A shorter verified win is favorable; a faster loss is not a strength claim.

## Exact telemetry and mechanism gates

### v33 bridge, with the v34 threshold

Record the first qualifying trigger and trigger-episode count; ordered assignment frames, batch sizes, assigned Probe IDs, current and peak defender counts; accepted bridge attack orders; ordered release frames, release sizes, and cause flags for `army_ge_3` and `threat_clear`; cause-specific release counts; defender deaths; economy and build selector exclusions; and accepted post-release gather/build orders. Assignment batches must partition the ordered ID list, including repeated IDs across separate threat episodes. Release rows and cause summaries must agree.

Both Zerg attempts must be valid for the bridge gate. Neither may exceed two simultaneous bridge defenders. Every assignment batch must contain one or two eligible Probes while the qualifying trigger is active. Every release must carry `army_ge_3` or `threat_clear`, and no surviving released identity may remain excluded after a later documented release opportunity. A qualifying ZZZK-like local threat must produce at least one bridge assignment and one accepted bridge attack order. Across the two Zerg lanes, report exclusions and any accepted post-release economy/build order when an opportunity occurs; an absent opportunity is `UNTESTED`, not a fabricated pass. Non-Zerg lanes must keep every bridge counter and trace empty or at its documented `-1` sentinel.

### v34 staged nonreserve offense

Record ordered state rows with frame, completed combat army, reserve count, `nonreserve_surplus`, state, and cause; first staging frame; first threshold-observation frame; release frame, release surplus, release army, and released unit IDs; maximum surplus; home-move attempts and accepts while staging; remote-offense attempts and accepts while staging and after release; restage events; latch-clear frame/cause; and the first frame at which surplus reaches zero after release. State code `0` means `home_staging` and `1` means `released_latched`; cause code `0` means an observed state row without a transition, `2` means release at surplus six, and `4` means latch clear at observed surplus zero. Record any local-defense actions separately so reserve and bridge defense are not misclassified as nonreserve offense.

For each valid Zerg lane, state telemetry must begin in `home_staging` when nonreserve units exist, transition to `released_latched` only at an observed `nonreserve_surplus >= 6`, and never issue a nonreserve remote-offense order during staging. Once released, the state must remain latched while `nonreserve_surplus > 0`; a latch clear must carry cause code `4`, occur at observed surplus zero, and agree with the latch-clear and first-zero scalar frames. No restage transition is allowed while surplus remains positive. Counters, ordered rows, unit-ID lists, and scalar summaries must agree. At least one of the two Zerg lanes must reach surplus six and exercise the transition; if neither reaches the threshold, the staged-offense mechanism is `UNTESTED` and the cohort cannot advance. A lane that reaches the threshold may finish with positive surplus, but the telemetry must still prove that it remained latched through its terminal callback.

All staged-offense counters, rows, IDs, and sentinel fields must remain empty or zero in the three non-Zerg lanes. The v34 treatment must not alter the v33 bridge's defender exclusions, the v32 reserve's local-defense rules, or any production/economy telemetry outside the two registered Zerg changes.

### Retained v32 reserve and regression gates

Retain all v33/v32 reserve gates: reserve remote attacks remain zero; accepted home moves do not exceed attempts; accepted repeat home moves have minimum interval at least 96 frames; any Zerg attempt reaching three completed combat units records reserve peak three and a nonnegative first-three frame; and when a first non-worker Zerg home threat observes `g >= 2`, reserve size and reserved-local count at that exact frame are each at least `min(3, g)`. Across the Zerg lanes, require at least one reserve remote-target suppression, one accepted reserve local-defense attack, and one lane that reaches a three-unit reserve and later records an accepted nonreserve remote attack after the v34 surplus-six release with release army at least four. An unobserved retained mechanism is `UNTESTED`, not a pass by inference. Non-Zerg reserve telemetry must remain zero or `-1`.

Regression passes only with zero gas-worker build attempts, zero build `Unit_Busy` rejections, rejected commands below 5% in every attempt and across the cohort, no game above six Pylons, and ordered accepted/current/completed frames for every observed sixth Pylon. If a retained build-commandability guard blocks, a later construction must be accepted after the first block. Report all unexercised mechanisms explicitly.

## Validity, provenance, and runtime controls

Integrity passes only when all five attempts have complete manifests, both child return codes zero, reciprocal Boolean terminal results, no timeout/launcher/state-hash/wrong-race failure, exactly two archived replay copies per game, matching recorded and measured replay hashes, complete `screp` parsing without parse-error commands, and expected races. For each replay copy, require `replay_header_frames + 1 == owning_callback_frame`. Preserve all failures and do not infer completion from process names.

The candidate must compile natively against OpenBW and against official BWAPI 4.4 headers before launch. The build sidecar must preserve the exact v33 base identity, v34 source and patch bytes, compiler, binary, engine, game-data, and runtime identities. The schedule freezes the opponent hashes and the `Ours`/`Original`/`Port`/`Fork` labels and source links, consistent with `config/bot-identities.json`. Upstream observations remain attached to upstream builds and are not transferred to this Kestrel candidate. Only public legal BWAPI observations may influence gameplay; evaluator and replay access remains outside the policy.

The v34 diagnostic schema intentionally replaces v33's `emergency_army_two_*` release fields with `emergency_army_three_*`, replaces the obsolete `early_zerg_stage_*` fields with `zerg_offense_stage_*`, and retains the remaining v33 bridge and v32 reserve fields. Scoring must be version-aware: it must evaluate the army-three release and staged-offense fields for v34 while preserving legacy extraction for archived candidates.

No fixed 384-fps adoption gate applies to this exploratory screen, but report durable logical FPS, callback timing, CPU time, and peak RSS for every game. A verified short terminal result is required for a gameplay decision. Do not update Elo, merge the exploratory games into the local-rating pool, or call this evidence tournament validation.

## Decision and result contract

- **`ADOPT`:** all five attempts are valid short terminal games, every integrity/regression/bridge/staged-offense/reserve/provenance gate passes, and at least one candidate win is verified. Adoption means only “eligible for a separately preregistered held-out confirmation.”
- **`REJECT`:** the cohort is valid and short-terminal, but the win threshold or any gameplay/mechanism/regression gate fails.
- **`INCONCLUSIVE`:** any timeout, missing terminal result, infrastructure-invalid attempt, cohort-cap stop, or other failure prevents the registered five-game decision. Preserve the attempt and do not retry it within this evaluation.
- **Raw-data location:** `artifacts/experiments/kestrel-hillclimb-v13/`.
- **Result-report location:** `docs/evaluations/kestrel-hillclimb-v13/RESULT.md`, with `NEGATIVE_RESULT.md` when the repository's evaluation workflow requires it.

## Registered source identity

The exact v33 base is the candidate registered by `kestrel-hillclimb-v12`:

- v33 experiment: `kestrel-hillclimb-v12`.
- v33 source SHA-256: `d3c09bc2cd94eaccabefffe0fe76ed542f0e063a2a400a1428fc4b51d79d887a`.
- v33 combined source SHA-256: `562dc539d1171c5958ce80cbaebef4e53b336c908dc51e7385e75cb0d656cb66`.
- v33 binary SHA-256: `1d77b4483ea0fa21db1df9d8b45e15364986b793a2745b2c570f0db2fb55b632`.
- v33 binary path: `artifacts/builds/1d77b4483ea0fa21db1df9d8b45e15364986b793a2745b2c570f0db2fb55b632/kestrel-opening-v33-candidate/Kestrel.dylib`.
- v33 reconstruction patch: `patches/kestrel-v32-to-v33-two-probe-emergency-zerg-bridge.patch`, SHA-256 `e1765155cff50b27e306b16f6b9c6d562ea9d1aae5746ed1d74854228b3d7276`.

The v34 candidate identity is intentionally incomplete until the source is implemented and independently compiled:

- v34 source SHA-256 (`Kestrel.cpp`): `947b64fb0c6510bfbf32024850e9e517842f22349d8ac27a59f61d63897cf8bd`.
- v34 combined source SHA-256 (`Kestrel.cpp`, `CMakeLists.txt`, `LICENSE` concatenated in that order): `9d182a0f6db463bb5a6cf9ee16cd4b157988edd1626ce3d48e5b1630efaa9815`.
- v34 binary SHA-256: `f71a1dc353a89c1770a05c59b21ae4907aebb7650d87cbb3af9239137a4b763a`.
- v34 binary path: `artifacts/builds/f71a1dc353a89c1770a05c59b21ae4907aebb7650d87cbb3af9239137a4b763a/kestrel-opening-v34-candidate/Kestrel.dylib`.
- v34 build sidecar: `artifacts/builds/f71a1dc353a89c1770a05c59b21ae4907aebb7650d87cbb3af9239137a4b763a/kestrel-opening-v34-candidate/Kestrel.dylib.build.json`.
- v34 reconstruction patch: `patches/kestrel-v33-to-v34-two-probe-threshold-and-offense-latch.patch`, SHA-256 `0e0c21d9957c1e9d5d506355a5af357e0b887406de14399e91f8310ab941dca1`.
- The final schedule records this reviewed evaluation plan's SHA-256 before launch.

## Frozen runtime identities

- Engine library SHA-256: `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`.
- Engine launcher: `artifacts/builds/eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b/openbw-terminal-drain/BWAPILauncher`.
- Game data: `third_party/game-data/runtime`.
- v33 base sidecar: `artifacts/builds/1d77b4483ea0fa21db1df9d8b45e15364986b793a2745b2c570f0db2fb55b632/kestrel-opening-v33-candidate/Kestrel.dylib.build.json`.
