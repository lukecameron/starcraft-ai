# Kestrel v37 post-opening scaling screen

Registered and frozen 2026-09-21 before gameplay. This is a preregistered five-game matched screen of `Kestrel-v37-post-opening-scaling` against the exact v15 rows. It tests one bundled post-opening treatment against the v36 lineage; it is not Elo evidence.

## Decision

- Treatment: Singularity Charge after second Gateway current, completed Cybernetics Core, and six completed combat units, with 150/150 banking and retry-until-one-accept; Pylon cap 10 and post-Core Gateway cap 6.
- Control: exact frozen v36 candidate and the same five v15 scenario inputs.
- Adoption permits only a separately registered held-out confirmation. It does not replace the canonical anchor or update Elo.
- ADOPT requires five valid short terminal games, at least one verified win, one eligible lane with exactly one accepted and completed range upgrade, one observed seventh-Pylon or fifth-Gateway accepted/current extension, no cap violations, the matched ZZZK opening gate, and every retained v36/v35/v34, regression, provenance, public-information, runtime, owner-frame, and non-Zerg gate.
- REJECT applies when the cohort is valid and short-terminal but the win threshold or any gameplay/mechanism/regression gate fails.
- INCONCLUSIVE applies only to timeout, missing terminal result, infrastructure-invalid attempt, cohort-wall-cap stop, or missing/inconsistent reserve, scaling, or integrity telemetry.

## Hypothesis and treatment

The v36 screen reached substantially larger armies but still lost late, while it had no upgrade path and capped production at four Gateways. A single public-state scaling bundle should add ranged-combat effectiveness and production capacity after the opening is established without changing the v36 opening, construction, emergency, reserve, staged-offense, or commandability policy.

The candidate may issue Singularity Charge only when the second Gateway is current, the Cybernetics Core is completed, and at least six Kestrel combat units are completed. It banks 150 minerals and 150 gas, records every eligibility and bank-block observation, and retries until one accepted research command. It must accept at most one research command and record completion when the upgrade completes. Pylon construction must never exceed the constant cap of 10; post-Core Gateway construction must never exceed the constant cap of 6.

The only registered gameplay treatment is this bundle. No attack, scouting, emergency assignment, reserve, staged-offense, construction bookkeeping, or non-Zerg policy change is permitted. All gameplay decisions use public legal BWAPI observations only.

## Frozen matched cohort

Run exactly five attempts concurrently, with no retry, reseed, replacement, or rerun:

| Game | Opponent | Map | Kestrel slot | Seed |
| ---: | --- | --- | ---: | ---: |
| 1 | ZZZKBot | sscai/(2)Benzene.scx | P1 | 9941 |
| 2 | UAlbertaBot-Terran | sscai/(2)Destination.scx | P2 | 9942 |
| 3 | UAlbertaBot-Protoss | sscai/(2)Heartbreak Ridge.scx | P1 | 9943 |
| 4 | McRave-9Pool-treatment | sscai/(4)Circuit Breaker.scx | P2 | 9944 |
| 5 | Stardust-repaired | sscai/(2)Benzene.scx | P1 | 9945 |

Use a 300-second wall cap per game, 900-second cohort cap, concurrency five, and stop after two consecutive infrastructure-invalid attempts or the cohort cap. Preserve every manifest, runner log, diagnostic, replay, hash, parse result, and failure record. A valid terminal loss is gameplay evidence; an infrastructure-invalid attempt is INCONCLUSIVE.

## Primary metric and invalid rules

The primary metric is verified candidate wins per five valid short-terminal games:

`verified_win_count = sum(1 for game in games if integrity_pass and short_terminal_pass and candidate_terminal_result == "win")`.

The threshold is at least one verified win. A timeout, missing terminal result, nonzero child return code, launcher/state-hash/wrong-race failure, missing replay copy, hash mismatch, incomplete `screp` parse, missing owner-frame evidence, or malformed/inconsistent required telemetry makes the decision INCONCLUSIVE. Coherent partial telemetry caused by a terminal game is valid evidence, but fails the completion mechanism if no lane completes it. An eligible lane with a valid but failed upgrade or a valid cohort with no eligible lane is REJECT, not INCONCLUSIVE.

## Required gates

The ZZZK lane must retain the v36 opening gate: second Gateway current before the first qualifying public home threat and at least two completed Kestrel combat units at that threat. The first Pylon and both Gateway accepted/current/completed frames, first follow-on Zealot, and threat/combat frames must be recorded.

The v37 scaling telemetry must contain integer fields `max_pylon_cap`, `max_post_core_gateway_cap`, `range_upgrade_eligibility_frame`, `range_upgrade_bank_start_frame`, `range_upgrade_bank_block_count`, `range_upgrade_attempt_frame`, `range_upgrade_accepted_frame`, `range_upgrade_completion_frame`, `range_upgrade_attempts`, `range_upgrade_accepted`, `range_upgrade_completions`, `range_upgrade_max_bank_minerals`, `range_upgrade_max_bank_gas`, plus accepted/current/completed frames for `seventh_pylon` and `fifth_gateway`. Arrays and observed milestone prefixes must be aligned and ordered. The cap constants must equal 10 and 6, observed maxima must not exceed them, and every observed prefix must respect accepted <= current <= completed. A terminal game may coherently end after acceptance but before current/completed, or after an upgrade is accepted but before completion; that is valid partial gameplay evidence and does not make replay integrity inconclusive.

If `range_upgrade_eligibility_frame < 0`, the upgrade opportunity is UNTESTED. ADOPT requires at least one eligible lane with exactly one accepted upgrade and one completion. Missing required fields, wrong types, contradictory counters, impossible frame order, or a later milestone without its required earlier milestone is INCONCLUSIVE. A coherent trace that ends while banking, after a rejected attempt, after acceptance but before completion, or during a structure milestone is valid partial evidence. A valid cohort with no completed upgrade is REJECT.

Retain every v36/v35/v34 gate: construction pre-command baselines and ordered current/completed milestones; cumulative two-unique-Probe emergency episodes, including at least one qualifying episode and cap-block opportunity across Zerg lanes; stable three-unit reserve and local-defense behavior; zero reserve remote attacks; 96-frame accepted home-move cadence; reserve suppression/local attack; staged-offense release and post-release accepted nonreserve remote attack; surplus-six latch, zero remote offense while staging, and no restage while surplus remains positive. Unobserved retained mechanisms are UNTESTED and therefore cannot satisfy ADOPT.

Regression passes only with zero gas-worker build attempts, zero build `Unit_Busy` rejections, command rejection below 5% per game and across the cohort, no observed Pylon count above 10, no observed Gateway count above 6 after the Core, and ordered accepted/current/completed frames for every observed seventh Pylon and fifth Gateway. The retained commandability guard must permit a later construction after its first block.

All five attempts must have complete manifests, reciprocal Boolean terminal results, expected races/maps/slots/seeds, exactly two archived replay copies, matching hashes, complete parsing, and `replay_header_frames + 1 == owning_callback_frame` for each copy. The candidate must compile against native OpenBW and official BWAPI 4.4 headers. The sidecar must preserve the v36 base, v37 source and patch bytes, compiler, binary, engine, game-data, and runtime identities. Opponent hashes and Ours/Original/Port/Fork provenance are frozen in `schedule.json` and `config/bot-identities.json`.

No fixed 384-fps adoption gate applies; report durable logical FPS, callback p99/max, CPU time, peak RSS, command rejection rates, and uncertainty descriptively. This matched screen does not update Elo.

## Registered identity and runtime

- Candidate: `Kestrel-v37-post-opening-scaling`.
- Binary: `artifacts/builds/ad60fe9280c8e3c8e22785e90656df76a27b86e06b435346c0bc47142af6e228/kestrel-opening-v37-post-opening-scaling/Kestrel.dylib`.
- Binary SHA-256: `ad60fe9280c8e3c8e22785e90656df76a27b86e06b435346c0bc47142af6e228`.
- Source SHA-256 (`Kestrel.cpp`): `ffacb1de456936fa47058baa7735d0318cdb3e3d7a923740ec7a63ece5dd7c86`.
- Combined source SHA-256: `b22fd4257d47b96cc127f778e9bd3e81a3a4c4a2c17ae5e3b0023f44cbc0b2b6`.
- Reconstruction patch: `patches/kestrel-v36-to-v37-post-opening-scaling.patch`; SHA-256 `262cb9254874f2155c9c58fc669da8e8f418ebbe90c502da8e717f5403d8863a`.
- Source files: `third_party/kestrel-opening-v37-candidate/Kestrel.cpp`, `CMakeLists.txt`, `LICENSE`.
- Engine SHA-256: `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`.
- Launcher: `artifacts/builds/eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b/openbw-terminal-drain/BWAPILauncher`.
- Game data: `third_party/game-data/runtime`.
- Provenance registry: `config/bot-identities.json`.

Raw data belongs under `artifacts/experiments/kestrel-hillclimb-v16/`; the result belongs in `docs/evaluations/kestrel-hillclimb-v16/RESULT.md`, with `NEGATIVE_RESULT.md` when required.
