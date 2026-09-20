# Kestrel v36 opening reserve hill-climb

Registered and frozen 2026-09-21 before gameplay. This is a preregistered five-game matched change-effect screen of the exact Kestrel v36 build. It tests one gameplay change against the exact v35 candidate lineage: reserve 250 minerals for the second Gateway by suppressing Probe production from the first Pylon being accepted until the second Gateway is current.

## Decision

- **Change under evaluation:** Kestrel v36, with only the 250-mineral opening Probe-production reserve described below. All v35 construction bookkeeping and cumulative emergency-episode Probe-cap mechanisms remain unchanged.
- **Control:** the exact frozen Kestrel v35 construction-bookkeeping and emergency-episode-cap candidate from the prior registered v35 screen, with its source, binary, engine, game data, maps, opponent builds and runtime lineage preserved.
- **Decision this evaluation controls:** whether v36 may proceed to a separately registered held-out confirmation screen. It cannot replace the canonical v13 local anchor or update local Elo.
- **Adoption threshold:** every integrity, short-terminal, mechanism, regression, public-information, runtime, owner-frame, provenance and non-Zerg inactivity gate passes, and the five-game cohort contains at least one verified Kestrel win.

## Hypothesis

The v35 opening can spend a Probe during the interval after the first Pylon is accepted and before the second Gateway becomes current. In the v35 ZZZK diagnostic this includes the Probe observed around frame 1580, and the second Gateway was not current early enough to support two completed combat units at the first qualifying threat. Holding 250 minerals for Probe production from first-Pylon acceptance through second-Gateway current should suppress that early Probe train, make the Gateway and follow-on combat production available sooner, and improve the chance of reaching two completed combat units before the first qualifying ZZZK pressure in the matched scenario, without changing the v35 construction bookkeeping, emergency episode cap, reserve, staged offense, command guards, or non-Zerg policy.

The hypothesis is falsified for this screen if the cohort is valid but has no verified win, if v36 does not suppress the registered early Probe-production opportunity in the matched ZZZK lane, if the second Gateway is not current before the first qualifying ZZZK home threat, if fewer than two combat units are complete at that threat, if Probe production is not resumed after the second Gateway becomes current, or if any retained v35, regression, public-information, provenance or non-Zerg gate fails. The v35 frame 1580 observation is a diagnostic motivation, not a universal timing bar.

## Design

### Treatment: exactly one gameplay change

In `trainUnits()`, retain all v35 logic and set `openingReserve` to 250 minerals when the candidate has identified Zerg, the first Pylon has been accepted, and the second Gateway is not yet current. The Probe command remains legal only when `minerals >= 50 + openingReserve`, so the reserve applies from first-Pylon acceptance through second-Gateway current. Preserve the existing 100-mineral early Pylon reserve and the post-second-Gateway first-Zealot reserve. No build order, combat, scouting, emergency assignment, construction bookkeeping, staged-offense, or commandability policy may change.

Source review must verify that the only policy diff from v35 is this reserve threshold and that v35 telemetry and public-information boundaries are intact. The candidate also emits public diagnostic-only telemetry for accepted Probe train frames, aligned reserve-block frames/minerals for idle Nexus opportunities, `opening_probe_reserve`, `max_opening_probe_reserve`, the reserve-window start/end frames, and the reserve-block count. The registered expectation is `max_opening_probe_reserve == 250` on every active Zerg lane and `== 0` on every non-Zerg lane. For each Zerg lane, verify first-Pylon accepted frame, second-Gateway current frame, every reserve-block frame with the observed mineral value in the registered 200..299 range, the suppressed early opportunity corresponding to the v35 frame-1580 Probe, the accepted Probe train frame sequence, and the first resumed accepted Probe train at or after second-Gateway current. An accepted Probe train is forbidden only in the half-open interval `[first_pylon_accepted_frame, second_gateway_current_frame)`; an accepted train exactly at `second_gateway_current_frame` is allowed. Owner-filtered replay parsing must corroborate the accepted Probe train sequence; diagnostic-only arrays must be aligned and may not be used as hidden gameplay state. Missing, unaligned or contradictory reserve telemetry is `INCONCLUSIVE`; do not infer the mechanism from a replay-only evaluator view.

### Frozen matched five-game screen

Run exactly five candidate attempts concurrently against the same five frozen opponent builds and the exact prior v35 screen maps, engine seeds and candidate slots below. This is a matched change-effect screen: the prior v35 results are the incumbent reference in the identical scenario regime, while the v36 games are new candidate attempts. Reusing the scenario inputs is intentional; the result must not be described as independent Elo evidence. Do not retry, reseed, replace or rerun a row.

| Game | Opponent | Map | Kestrel slot | Engine seed |
| ---: | --- | --- | ---: | ---: |
| 1 | ZZZKBot | Benzene | P1 | 9941 |
| 2 | UAlbertaBot-Terran | Destination | P2 | 9942 |
| 3 | UAlbertaBot-Protoss | Heartbreak Ridge | P1 | 9943 |
| 4 | McRave-9Pool-treatment | Circuit Breaker | P2 | 9944 |
| 5 | Stardust-repaired | Benzene | P1 | 9945 |

Minimum sample size is five attempts. Use a 300-second wall cap per game, a 900-second cohort cap and concurrency five. Stop after two consecutive infrastructure-invalid attempts or the cohort cap. Preserve every manifest, runner log, diagnostic, replay, hash, parse result and failure record. A valid terminal loss is retained as gameplay evidence; a timeout, missing terminal result or infrastructure-invalid attempt is `INCONCLUSIVE`.

There are no planned ablations. The 250-mineral reserve is one treatment so a later confirmation cannot select a favorable sub-result after inspection. The matched v35/v36 rows support a bounded change-effect comparison only; they do not create independent Elo evidence, update Elo, or merge these games into the local-rating pool.

## Primary metric

- **Name:** verified candidate wins in the five-game cohort.
- **Direction and unit:** higher is better; integer wins per five valid, short-terminal games.
- **Exact formula:** `verified_win_count = sum(1 for game in games if integrity_pass and short_terminal_pass and candidate_terminal_result == "win")`.
- **Source fields:** final manifest terminal result, lifecycle status, child return codes, wall-cap status, replay-copy hashes, replay header frame, owning callback frame, expected races/maps/slots/seeds and complete `screp` parse result.
- **Threshold:** at least one verified win, in addition to every registered mechanism and regression gate.

Report terminal frame and durable logical FPS per game, callback p99/max and CPU time, peak RSS, command rejection rates, Probe train observations, construction timing and complete v35 telemetry. A shorter verified win is favorable; a faster loss is not a strength claim.

## Mechanism and retained gates

### Matched ZZZK timing and Probe reserve

The matched ZZZK lane must observe the first qualifying public home threat. Record `opening_probe_reserve`, `max_opening_probe_reserve`, first-Pylon accepted/current/completed frames, first and second Gateway accepted/current/completed frames, the aligned Probe reserve-block frames/minerals, the reserve-window start/end frames and block count, accepted Probe train frames around the reserve window, the v35-motivated early Probe opportunity, the first resumed Probe acceptance at or after second-Gateway current, the first follow-on Zealot train/completion and completed Kestrel combat count. The second Gateway must be current before the first qualifying threat, and at least two Kestrel combat units must be complete at that threat. If the threat is absent, report `UNTESTED`; do not claim a pass by inference.

### Construction and emergency episode mechanisms

Retain v35's source-reviewed construction rule: accepted builds store the pre-command count before `issue()`, pending construction releases only when public self count exceeds that baseline, aligned arrays agree, no accepted row is missing, and no overlapping pending construction occurs. Retain v35's emergency episode rule: at most two unique Probe identities cumulatively per continuous qualifying threat, no replacement after two identities even after death, simultaneous defenders at most two, eligibility/build/economy/gas-worker exclusions intact, releases carry `army_ge_3` or `threat_clear`, episode counters reset only after threat clear, assignment batches partition the ordered IDs, and at least one qualifying episode and cap-block opportunity are observed across the Zerg lanes. Non-Zerg lanes must have empty/zero/sentinel emergency fields.

### v34 reserve and staged offense

Retain every v34 gate: stable three-unit reserve and local-defense behavior; zero reserve remote attacks; accepted home moves no greater than attempts; repeated accepted reserve moves at least 96 frames apart; a Zerg lane reaching three completed combat units records reserve peak three; at first non-worker Zerg home threat with `g >= 2`, reserve and reserved-local counts are each at least `min(3, g)`; at least one reserve remote-target suppression, one accepted reserve local-defense attack, and one staged-offense release followed by an accepted nonreserve remote attack when an opportunity occurs. Preserve the surplus-six release latch, zero remote offense during staging, and no restage while surplus remains positive. An unobserved retained mechanism is `UNTESTED`, not a pass. All reserve/staged-offense fields remain empty or zero in the three non-Zerg lanes.

### Regression, integrity, provenance and runtime

Regression passes only with zero gas-worker build attempts, zero build `Unit_Busy` rejections, rejected commands below 5% in every attempt and across the cohort, no game above six Pylons, and ordered accepted/current/completed frames for every observed sixth Pylon. A retained commandability guard must permit a later construction after its first block.

Integrity passes only when all five attempts have complete manifests, both child return codes zero, reciprocal Boolean terminal results, expected races/maps/slots/seeds, no timeout/launcher/state-hash/wrong-race failure, exactly two archived replay copies per game, matching recorded and measured replay hashes, complete `screp` parsing without parse-error commands, and `replay_header_frames + 1 == owning_callback_frame` for each replay copy. Preserve every failed record.

The candidate must compile natively against OpenBW and official BWAPI 4.4 headers before launch. Its sidecar must preserve the exact v35 base, v36 source and patch bytes, compiler, binary, engine, game-data and runtime identities. Gameplay may use only public legal BWAPI observations; evaluator/replay access remains outside the policy. The schedule freezes each opponent's hash and `Ours`/`Original`/`Port`/`Fork` provenance from `config/bot-identities.json`; the candidate is `Ours`/`Original`/Luke Cameron with its source link. No fixed 384-fps adoption gate applies to this exploratory screen, but durable logical FPS and callback performance are reported descriptively.

## Decision and result contract

- **`ADOPT`:** all five attempts are valid short terminal games, every integrity, mechanism, reserve, staged-offense, regression, public-information, runtime, owner-frame, provenance, Probe-reserve and non-Zerg gate passes, and at least one candidate win is verified. Adoption only permits a separately preregistered held-out confirmation.
- **`REJECT`:** the cohort is valid and short-terminal, but the win threshold or any gameplay/mechanism/regression gate fails.
- **`INCONCLUSIVE`:** any timeout, missing terminal result, infrastructure-invalid attempt, cohort-wall-cap stop or missing reserve/integrity evidence prevents the registered decision. Preserve the attempt and do not retry it in this evaluation.
- **Raw-data location:** `artifacts/experiments/kestrel-hillclimb-v15/`.
- **Result-report location:** `docs/evaluations/kestrel-hillclimb-v15/RESULT.md`, with `NEGATIVE_RESULT.md` when required by the evaluation workflow.

## Registered source identity

- Candidate name: `Kestrel-v36-opening-250-mineral-reserve`.
- Binary: `artifacts/builds/c2e95394fd5c8c6a6dcd4ae2d7a8f1460624d454a906c6dba3e3e32bfb960b85/kestrel-opening-v36-candidate/Kestrel.dylib`.
- Binary SHA-256: `c2e95394fd5c8c6a6dcd4ae2d7a8f1460624d454a906c6dba3e3e32bfb960b85`.
- Source SHA-256 (`Kestrel.cpp`): `a8f884c4dea4d3dfd4a91708763b35457c330f1bf4b89a6c12bdcbd0092effc3`.
- Combined source SHA-256 (`Kestrel.cpp`, `CMakeLists.txt`, `LICENSE` in that order): `81b1d8ed7e0879dbd9b36716fa4922e9366bddcc4d64ca6b6e77e70adff6fdbb`.
- Reconstruction patch: `patches/kestrel-v35-to-v36-opening-reserve.patch`, SHA-256 `02633bc1a78d1f5ffffd1b051c7e67d5672b485fef4f2d91cd94d4eaea9aa371`.
- Source files: `third_party/kestrel-opening-v36-candidate/Kestrel.cpp`, `CMakeLists.txt`, `LICENSE`.

The exact v35 base is the candidate registered by the prior v35 screen: binary SHA-256 `8e85a4389b18caf7f55d857d81889e1d7ecfa4d41333794a5797f69a10769270`, source SHA-256 `e81637c5fe1251786bebe9c63aa577aacf8bbd935766d320dbb16574059907af`, combined source SHA-256 `05ac2402858f7765710e95f5c3414fd698857f76afe407c502faa2956a3e025e`, and v35 patch SHA-256 `46e441080a8d599427bbdf111591be2ae47faa77fb99d7d6a8fb4dfd605bb023`.

## Frozen runtime and provenance

- Engine library SHA-256: `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`.
- Engine launcher: `artifacts/builds/eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b/openbw-terminal-drain/BWAPILauncher`.
- Game data: `third_party/game-data/runtime`.
- Provenance registry: `config/bot-identities.json`.
- Opponent identities, immutable paths, hashes, origin labels and source links are frozen in `schedule.json`.
