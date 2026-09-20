# Kestrel v31 early-Zerg squad-staging hill-climb

Registered 2026-09-20 before candidate compilation or gameplay. Kestrel v30 is an instrumentation-only, formally inconclusive diagnostic because its registered replay-frame relation was wrong and one lane failed before terminal evidence. Its traces are descriptive motivation, not causal evidence. Independently, the valid matched v19 screen showed that early home staging increased simultaneous local Zealots from one to two on both tested maps, although that candidate missed a production gate and recorded no win.

The shortlist for the next bounded policy test was: keep the opening squad home before its first coordinated move; classify workers separately from combat threats; or add a short post-threat rally window. This run selects only the first item so its effect remains attributable. v31 starts from exact v29 source SHA-256 `0dbb8404b62197e52020655d098c888abdb25aaeca79b60358d44b4a806b4fe3`, combined source SHA-256 `956c5882e2948d54fce8d5dbf4e8fa963121e2998a09a6179a136d3e6b4f924d`, and binary SHA-256 `c7196ea991f5755b6e34c9c9ebff87faf3884d221de9492a7952ce20cc57d56c`.

## Candidate and hypothesis

The single gameplay change applies only against a publicly identified Zerg opponent while fewer than four completed Zealots plus Dragoons exist. Completed combat units may attack a visible, detected, ground enemy inside the existing 12-tile home radius. Otherwise they ignore visible remote targets, clear retained attack requests, and move to the existing home center if they are outside four tiles or still moving elsewhere. At four completed combat units the staging rule ends and v29 targeting resumes. Non-Zerg behavior is unchanged. The v29 public `canBuild` guards, sixth-Pylon limit, opening, economy, production, target choice after release, and command cadence are retained.

The hypothesis is that holding the first squad together will prevent scout-provided remote targets from drawing the early Zerg defense away one unit at a time, while releasing a four-unit group early enough to preserve offensive conversion.

Scalar telemetry records distinct remote-target suppression events and unique affected units, attempted and accepted home moves, accepted local-defense attacks, any prohibited pre-four remote attacks, the maximum pre-four army and local-combat counts, the first two-local frame, and accepted post-release attacks with the first release frame and army size. It also records the first visible non-worker Zerg home combat threat and local/global completed combat counts at that frame. Telemetry observes only public BWAPI state and never feeds evaluator or replay state into gameplay.

Mechanism passes only if both Zerg attempts are valid; `early_zerg_stage_max_army <= 3`, `early_zerg_stage_remote_attack_orders == 0`, and accepted home moves do not exceed attempts in both; at least one Zerg attempt records a remote-target suppression; at least one reaches two local completed combat units during staging; and at least one records an accepted release attack with `early_zerg_stage_release_army >= 4`. If a valid Zerg attempt records a first non-worker home threat with at least two completed combat units globally, it must have at least two local completed combat units at that frame. An unobserved suppression, release, or qualifying threat is reported as untested rather than inferred.

## Frozen five-game screen

Run exactly five candidate attempts concurrently, with no retry or replacement:

| Game | Opponent | Map | Kestrel slot | Engine seed |
| ---: | --- | --- | ---: | ---: |
| 1 | ZZZKBot | Benzene | P1 | 9901 |
| 2 | UAlbertaBot-Terran | Destination | P2 | 9902 |
| 3 | UAlbertaBot-Protoss | Heartbreak Ridge | P1 | 9903 |
| 4 | McRave-9Pool-treatment | Circuit Breaker | P2 | 9904 |
| 5 | Stardust-repaired | Benzene | P1 | 9905 |

Use a 300-second wall cap for each game and a 900-second cohort cap. Omit unsupported `MATCH_BOT_SEED` flags. Preserve every manifest, runner log, diagnostic, replay, hash and parse result, including failures. Stop after two consecutive infrastructure-invalid attempts or the cohort cap. Do not replace an invalid attempt.

Integrity passes only if all five attempts have completed manifests, both child return codes zero, reciprocal Boolean terminal results, no timeout, launcher, state-hash or wrong-race failure, exactly two archived replay copies per game, matching recorded and measured replay hashes, full `screp` parsing without parse-error commands, and expected races. For each replay copy, require `replay_header_frames + 1 == owning_callback_frame`; the replay terminal frame is one below its owner's terminal callback frame.

Regression passes only with zero gas-worker build attempts, zero build `Unit_Busy` rejections, below 5% rejected commands in every attempt and across the cohort, no game above six Pylons, and ordered accepted/current/completed frames for every observed sixth Pylon. If a build-commandability guard blocks, a later construction must be accepted after its first block. Report unexercised retained mechanisms as untested.

The user's current speed rule replaces the earlier fixed 384-fps gate. Report durable frames per second, callback p99/max time, callback CPU time and peak RSS for each game, but judge execution by the 300-second game cap and 900-second cohort cap. Shorter is favorable only for a verified win; a faster loss is not improvement.

Advance v31 to a matched confirmation only if every integrity and regression gate passes, the staging mechanism passes, and the candidate records at least one verified win. Zero wins rejects advancement. This exploratory screen cannot update Elo, replace canonical Kestrel v13, or establish tournament strength.

## Registered source identity

- Candidate source SHA-256: `347414e122c0b59311588a50e4c003a03b6dd61fb4081b1e01b0a750cc0de928`.
- Combined source SHA-256: `df80ddacc14c414d2e65272493cf445a8b22b6277fe6e2d3e791773733be466b`.
- Reconstruction patch: `patches/kestrel-v31-early-zerg-staging.patch`, SHA-256 `caf0739d9a63f6c4f9f78f9ef8d7fccf878aabc4d0b8d32885619f3c071fdaa6`.

The binary identity, native and official-header compilation results, frozen path, plan hash and schedule hash will be appended before match launch.
