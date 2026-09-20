# Kestrel v35 construction bookkeeping and emergency-episode hill-climb

Registered and frozen 2026-09-21 before gameplay. This is a preregistered five-game exploratory screen from the exact frozen Kestrel v34 candidate in `kestrel-hillclimb-v13`. It tests exactly two changes selected from the v34 replay and diagnostic review: fix construction bookkeeping so accepted builds release their pending state when the owned count rises above the pre-command baseline, and cap cumulative emergency Probe assignments at two per continuous qualifying threat episode.

## Decision

- **Change under evaluation:** Kestrel v35, with only the construction bookkeeping fix and cumulative emergency-episode assignment cap below applied to the exact v34 source and binary lineage. The v34 150-mineral reserve remains unchanged.
- **Decision this evaluation controls:** Whether v35 may proceed to a separately registered held-out confirmation screen. It does not replace canonical Kestrel v13 and cannot update local Elo.
- **Adoption threshold:** Every integrity, short-terminal, mechanism, regression, public-information, runtime, owner-frame, provenance, and non-Zerg inactivity gate passes, and the five-game cohort contains at least one verified Kestrel win.

## Hypothesis

In v34, construction bookkeeping captured a pending-build baseline after issuing the build command. In the ZZZK diagnostic, the first Gateway was accepted at frame 1392 and became current at 1768, but the post-acceptance baseline left `constructionPending` latched; the second Gateway was not accepted until frame 2172. Capturing `pendingBuildBaseline` from `count(type)` before `issue()`, storing that pre-command count on the accepted build, and releasing the pending state when the count becomes greater than that baseline should make the second Gateway available as soon as the first construction is actually reflected in public self state. Apply this exact bookkeeping to both `build()` and `buildAssimilator()`, while retaining the 150-mineral reserve. Limiting emergency bridge assignments to two unique Probe identities over a continuous qualifying local-threat episode should stop the observed replacement chain from spending every available defender while the threat remains active. Together, these changes should improve early Zerg survival without changing v34's staged-offense latch, non-Zerg policy, commandability guards, or public-information boundary.

The hypothesis is falsified for this screen if a valid cohort has no verified win, if the pre-command baseline/release gate or episode-cap state machine fails, if a fresh ZZZK lane does not have the second Gateway current before its first qualifying home threat and two completed combat units at that threat, if a non-Zerg lane records v35 Zerg-only activity, if v34's retained reserve/staged-offense gates regress, or if the candidate violates public-information or command-validity controls. The v34 absolute frames 2172/2328/3299 are diagnostic references for interpretation, not universal cross-seed timing bars. A timeout, missing terminal result, or other infrastructure-invalid attempt is `INCONCLUSIVE`, not evidence that the gameplay hypothesis failed.

## Design

### Control

The control is the exact frozen Kestrel v34 candidate from `kestrel-hillclimb-v13`, including its two-Probe emergency bridge through completed combat army size two, v32 three-unit reserve, v34 surplus-six staged offense and release latch, 96-frame home-move retry bound, gas-worker guard, production/economy policy, and all other behavior. The v34 source and binary must not be rebuilt or silently substituted.

### Treatment: exactly two changes

1. **Construction pending bookkeeping.** Preserve v34's 150-mineral reserve and all production policy. In both `build()` and `buildAssimilator()`, capture `pendingBuildBaseline = count(type)` before calling `issue()`. On an accepted build, store that pre-command baseline with the pending construction record. Release the pending state only when the public self count for that type becomes strictly greater than the stored baseline; do not capture the baseline after acceptance. Record aligned accepted-build frame, BWAPI type ID, pre-command count and immediate post-acceptance count arrays, together with the existing Gateway accepted/current/completed and sixth-Pylon timing fields. The ordered arrays must have equal length, each post-acceptance count must be at least its pre-command count, and later accepted/current/completed orders must remain consistent with the sequence. Apply the same baseline semantics to assimilators and report their rows when exercised.
2. **Cumulative emergency-episode cap.** Preserve v34's public-observation threat predicate, eligible-Probe rules, two-simultaneous-defender cap, economy/build exclusions, bridge attack handling, release behavior, and v34 staged offense. Define a continuous threat episode as beginning when a qualifying visible, detected, non-worker, attack-capable Zerg threat is observed inside the existing home-threat radius after no qualifying threat was observed, and ending only when that predicate becomes false. Reset the episode assignment count only at the threat-clear transition. Assign at most **two unique Probe identities cumulatively per episode**. A defender death removes that identity from the current defenders but does not create assignment capacity; no replacement may be assigned while the same episode remains active. If the army reaches v34's release threshold, surviving defenders are released as before, but the episode cap remains in force until threat clear. Record episode start/reset frames, ordered assignment IDs and frames, cumulative count, cap blocks, releases, deaths, and the reason for every eligibility decision.

There are no planned ablations in this five-game screen. The two changes are one preregistered treatment so that a follow-up confirmation cannot select a favorable sub-result after inspection.

### Frozen five-game screen

Run exactly five fresh candidate attempts concurrently, with no retry, reseeding, replacement, or control rerun:

| Game | Opponent | Map | Kestrel slot | Engine seed |
| ---: | --- | --- | ---: | ---: |
| 1 | ZZZKBot | Benzene | P1 | 9941 |
| 2 | UAlbertaBot-Terran | Destination | P2 | 9942 |
| 3 | UAlbertaBot-Protoss | Heartbreak Ridge | P1 | 9943 |
| 4 | McRave-9Pool-treatment | Circuit Breaker | P2 | 9944 |
| 5 | Stardust-repaired | Benzene | P1 | 9945 |

Use a 300-second wall cap per game, a 900-second cohort cap, and concurrency five. Preserve every manifest, runner log, diagnostic, replay, hash, parse result, and failure record. Do not silently score an unfinished match. Stop after two consecutive infrastructure-invalid attempts or the cohort cap. A timeout or missing terminal result is `INCONCLUSIVE`; a valid, fully parsed, short terminal loss is `REJECT` evidence.

## Primary metric

- **Name:** verified candidate wins in the five-game cohort.
- **Direction and unit:** higher is better; integer wins per five valid, short terminal games.
- **Exact formula:** `verified_win_count = sum(1 for game in games if integrity_pass and short_terminal_pass and candidate_terminal_result == "win")`.
- **Source fields:** final manifest terminal result, lifecycle status, child return codes, wall-cap status, replay-copy hashes, replay header frame, owner callback frame, expected races, and complete `screp` parse result.
- **Threshold:** at least one verified win, in addition to every mechanism and regression gate. This exploratory screen does not convert the count into an Elo update.

Report terminal frame and durable logical FPS per game, callback p99/max and CPU time, peak RSS, command rejection rates, and complete v34/v35 telemetry. A shorter verified win is favorable; a faster loss is not a strength claim.

## Mechanism gates

### Construction bookkeeping and first qualifying ZZZK threat

For every Zerg lane, record the first accepted, current, completed, and first follow-on Zealot frames for the second Gateway sequence, along with the complete pre-command baseline and pending-release rows described above. The v34 ZZZK values 2172 accepted, 2328 current, and 3299 completed are diagnostic references only; v35 is not required to beat those absolute frames on every fresh seed. The fresh ZZZK mechanism gate requires the second Gateway to be current before the first qualifying ZZZK home-threat frame and requires at least two completed Kestrel combat units at that threat. The first qualifying threat is the first frame satisfying v34's public threat predicate, independent of replay-only knowledge. Report the exact threat frame, second-Gateway accepted/current/completed frames, first follow-on-Zealot frame, completed army count, reserve size, and local threat identity. If the first qualifying ZZZK threat is never observed, the mechanism is `UNTESTED` and the cohort cannot advance.

The bookkeeping and ZZZK timing gates are mechanism gates, not Elo claims: they must be evaluated from public callback telemetry, not from replay state or evaluator state. Source review must confirm every accepted build stores its pre-command baseline before `issue()` and `constructionPending()` releases only when `count(type) > baseline`. The aligned build arrays and later current/completed frames must agree with that sequence; a missing row, unequal array length, earlier accepted order with no corresponding construction, or any evidence of overlapping pending construction is a failure.

### Emergency assignment episode cap

Both Zerg lanes must report ordered episode starts, threat-clear resets, assignment batches, unique Probe IDs, defender deaths, cap-block events, releases, and episode summaries. For every continuous qualifying episode:

- the cumulative number of unique assigned Probe identities is at most two;
- no replacement assignment is accepted after either two identities have been assigned, even if a defender dies;
- simultaneous defenders never exceed two;
- every assigned Probe satisfies v34's eligible-Probe, builder, gas-worker, economy, and build exclusions;
- every release carries the existing `army_ge_3` or `threat_clear` cause and preserves v34 release semantics;
- the episode count resets only after the threat predicate becomes false, and a later threat starts a new episode;
- assignment batches partition the ordered assignment-ID list and scalar counters agree with rows.

At least one Zerg lane must observe a qualifying episode and at least one cap-block opportunity; otherwise this mechanism is `UNTESTED` and the cohort cannot advance. A lane with no replacement opportunity reports `UNTESTED` for that sub-observation rather than claiming a pass by inference. Non-Zerg lanes must keep every episode, bridge, and Zerg-only counter empty or at its documented sentinel.

### Retained v34 reserve and staged offense

Retain all v34 gates: stable three-unit reserve and local-defense behavior; reserve remote attacks remain zero; accepted home moves do not exceed attempts; repeated accepted reserve home moves have minimum interval at least 96 frames; any Zerg attempt reaching three completed combat units records reserve peak three; and when a first non-worker Zerg home threat observes `g >= 2`, reserve size and reserved-local count at that exact frame are each at least `min(3, g)`. Across Zerg lanes, require at least one reserve remote-target suppression, one accepted reserve local-defense attack, and one lane reaching the surplus-six staged-offense release with a later accepted nonreserve remote attack when an opportunity occurs. Preserve v34's release latch until nonreserve surplus is zero; no remote nonreserve offense is allowed during staging, and no restage is allowed while surplus remains positive. An unobserved retained mechanism is `UNTESTED`, not a pass by inference.

All v34 staged-offense and reserve counters, rows, IDs, and sentinel fields must remain empty or zero in the three non-Zerg lanes. No v35 change may alter v34 production/economy telemetry outside the two registered changes.

## Integrity, public-information, provenance, and runtime gates

Integrity passes only when all five attempts have complete manifests, both child return codes zero, reciprocal Boolean terminal results, expected races/maps/slots/seeds, no timeout/launcher/state-hash/wrong-race failure, exactly two archived replay copies per game, matching recorded and measured replay hashes, complete `screp` parsing without parse-error commands, and `replay_header_frames + 1 == owning_callback_frame` for each replay copy. Preserve every failure and never infer completion from broad process-name matching.

The candidate must compile natively against OpenBW and against official BWAPI 4.4 headers before launch. Its build sidecar must preserve the exact v34 base identity, v35 source and patch bytes, compiler, binary, engine, game-data, and runtime identities. Only public legal BWAPI observations may influence gameplay; evaluator and replay access remains outside the policy. Source inspection must show no replay, evaluator, hidden-state, or opponent-private data entering the policy.

The schedule freezes the opponent hashes and the `Ours`/`Original`/`Port`/`Fork` labels and source links from `config/bot-identities.json`. Upstream observations remain attached to upstream builds and are not transferred to Kestrel. The candidate must be labeled `Ours`/`Original`/Luke Cameron in all result and dashboard records.

No fixed 384-fps adoption gate applies to this exploratory screen, but report durable logical FPS, callback timing, CPU time, and peak RSS for every game. Require a short verified terminal result for a gameplay decision. Do not update Elo, merge these games into the local-rating pool, or call this evidence tournament validation.

Regression passes only with zero gas-worker build attempts, zero build `Unit_Busy` rejections, rejected commands below 5% in every attempt and across the cohort, no game above six Pylons, and ordered accepted/current/completed frames for every observed sixth Pylon. If a retained build-commandability guard blocks, a later construction must be accepted after the first block. Report all unexercised mechanisms explicitly.

## Decision and result contract

- **`ADOPT`:** all five attempts are valid short terminal games, every integrity, mechanism, reserve, staged-offense, regression, public-information, runtime, owner-frame, and provenance gate passes, and at least one candidate win is verified. Adoption means only eligible for a separately preregistered held-out confirmation.
- **`REJECT`:** the cohort is valid and short-terminal, but the win threshold or any gameplay/mechanism/regression gate fails.
- **`INCONCLUSIVE`:** any timeout, missing terminal result, infrastructure-invalid attempt, cohort-cap stop, or failure of the integrity data needed to make the registered decision prevents a five-game decision. Preserve the attempt and do not retry it in this evaluation.
- **Raw-data location:** `artifacts/experiments/kestrel-hillclimb-v14/`.
- **Result-report location:** `docs/evaluations/kestrel-hillclimb-v14/RESULT.md`, with `NEGATIVE_RESULT.md` when required by the evaluation workflow.

## Registered source identity

The exact v34 base is the candidate registered by `kestrel-hillclimb-v13`:

- v34 experiment: `kestrel-hillclimb-v13`.
- v34 source SHA-256: `947b64fb0c6510bfbf32024850e9e517842f22349d8ac27a59f61d63897cf8bd`.
- v34 combined source SHA-256: `9d182a0f6db463bb5a6cf9ee16cd4b157988edd1626ce3d48e5b1630efaa9815`.
- v34 binary SHA-256: `f71a1dc353a89c1770a05c59b21ae4907aebb7650d87cbb3af9239137a4b763a`.
- v34 binary path: `artifacts/builds/f71a1dc353a89c1770a05c59b21ae4907aebb7650d87cbb3af9239137a4b763a/kestrel-opening-v34-candidate/Kestrel.dylib`.
- v34 reconstruction patch: `patches/kestrel-v33-to-v34-two-probe-threshold-and-offense-latch.patch`, SHA-256 `0e0c21d9957c1e9d5d506355a5af357e0b887406de14399e91f8310ab941dca1`.

The v35 candidate was independently rebuilt byte-for-byte after source review and before launch:

- v35 source SHA-256 (`Kestrel.cpp`): `e81637c5fe1251786bebe9c63aa577aacf8bbd935766d320dbb16574059907af`.
- v35 combined source SHA-256 (`Kestrel.cpp`, `CMakeLists.txt`, `LICENSE` concatenated in that order): `05ac2402858f7765710e95f5c3414fd698857f76afe407c502faa2956a3e025e`.
- v35 binary SHA-256: `8e85a4389b18caf7f55d857d81889e1d7ecfa4d41333794a5797f69a10769270`.
- v35 binary path: `artifacts/builds/8e85a4389b18caf7f55d857d81889e1d7ecfa4d41333794a5797f69a10769270/kestrel-opening-v35-candidate/Kestrel.dylib`.
- v35 build sidecar: `artifacts/builds/8e85a4389b18caf7f55d857d81889e1d7ecfa4d41333794a5797f69a10769270/kestrel-opening-v35-candidate/Kestrel.dylib.build.json`.
- v35 reconstruction patch: `patches/kestrel-v34-to-v35-construction-bookkeeping-and-emergency-episode-cap.patch`, SHA-256 `46e441080a8d599427bbdf111591be2ae47faa77fb99d7d6a8fb4dfd605bb023`.
- The final schedule records this plan's SHA-256 and is independently hashed before launch.

## Frozen runtime identities

- Engine library SHA-256: `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`.
- Engine launcher: `artifacts/builds/eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b/openbw-terminal-drain/BWAPILauncher`.
- Game data: `third_party/game-data/runtime`.
- v34 build sidecar: `artifacts/builds/f71a1dc353a89c1770a05c59b21ae4907aebb7650d87cbb3af9239137a4b763a/kestrel-opening-v34-candidate/Kestrel.dylib.build.json`.
