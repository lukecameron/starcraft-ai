# Kestrel v32 stable three-unit Zerg reserve hill-climb

Registered 2026-09-20 before candidate compilation or gameplay. The v31 recovery completed five valid concurrent games but lost all five and failed its Zerg mechanism gate: its first-four-unit staging emitted repeated accepted home moves, and McRave's first visible non-worker home threat found only one of five completed Zerg combat units local. This screen tests one narrower repair: an explicit stable reserve of three combat units against Zerg. The v31 recovery remains descriptive motivation and is not pooled as strength evidence.

## Candidate and hypothesis

The candidate starts from exact v31 source SHA-256 `347414e122c0b59311588a50e4c003a03b6dd61fb4081b1e01b0a750cc0de928` and changes only the known-Zerg early-defense policy. Against a publicly identified Zerg opponent, up to three completed Zealots or Dragoons are assigned explicit reserve identities, choosing the nearest eligible units when slots first open and retaining those identities until death. A reserved unit may attack a visible, detected, ground enemy inside the existing 12-tile home radius, but it may not accept a remote target. A reserve unit outside the four-tile staging tolerance, or moving away from home while inside it, may receive a home move; attempts are limited to once per unit per 96 frames. A fourth and later combat unit follows the existing target policy while the three-unit reserve stays assigned and may defend local public threats. Non-Zerg behavior, economy, production, sixth-Pylon limit, build-commandability guards and all other target-selection behavior remain unchanged.

The hypothesis is that a three-unit explicit reserve preserves enough local defense to cover the first real Zerg pressure window while allowing surplus units to attack, and that per-unit assignment state removes v31's redundant home-command traffic. The policy uses only public BWAPI observations and the bot's own history. Evaluator, replay and post-game state remain outside gameplay.

Scalar telemetry records reserve recruit and death events, current and peak reserve size, the first three-unit-reserve frame, attempted and accepted home moves, cooldown suppressions, accepted repeat moves and their minimum interval, maximum accepted moves for any one unit, remote targets suppressed for reserve units, reserve and non-reserve remote attack orders, accepted local-defense attacks, the first visible non-worker Zerg home threat, global/local combat and reserve/local-reserve counts at that exact frame, the first accepted surplus release frame and army size, and maximum offensive surplus. It also records command rejections, gas-worker build attempts, `Unit_Busy` build rejections, Pylon counts and callback/performance measurements. Stable identity is reviewed from the frozen source; the gameplay gates use the scalar evidence emitted by the candidate.

## Frozen five-game screen

Run exactly five candidate attempts concurrently, with no retry or replacement:

| Game | Opponent | Map | Kestrel slot | Engine seed |
| ---: | --- | --- | ---: | ---: |
| 1 | ZZZKBot | Benzene | P1 | 9911 |
| 2 | UAlbertaBot-Terran | Destination | P2 | 9912 |
| 3 | UAlbertaBot-Protoss | Heartbreak Ridge | P1 | 9913 |
| 4 | McRave-9Pool-treatment | Circuit Breaker | P2 | 9914 |
| 5 | Stardust-repaired | Benzene | P1 | 9915 |

Use a 300-second wall cap for each game and a 900-second cohort cap. Omit unsupported `MATCH_BOT_SEED` flags. Preserve every manifest, runner log, diagnostic, replay, hash and parse result, including failures. Stop after two consecutive infrastructure-invalid attempts or the cohort cap. Do not replace an invalid attempt. The fresh seeds make timing and outcome differences descriptive; they do not create matched causal evidence against v31.

## Integrity, regression and mechanism gates

Integrity passes only if all five attempts have completed manifests, both child return codes zero, reciprocal Boolean terminal results, no timeout, launcher, state-hash or wrong-race failure, exactly two archived replay copies per game, matching recorded and measured replay hashes, full `screp` parsing without parse-error commands, and expected races. For each replay copy, require `replay_header_frames + 1 == owning_callback_frame`; the replay terminal frame is one below its owner's terminal callback frame. A nonempty normal OpenBW diagnostic stderr is not by itself a launcher failure; lifecycle records and child exit status control that gate.

Regression passes only with zero gas-worker build attempts, zero build `Unit_Busy` rejections, below 5% rejected commands in every attempt and across the cohort, no game above six Pylons, and ordered accepted/current/completed frames for every observed sixth Pylon. If a retained build-commandability guard blocks, a later construction must be accepted after its first block. Report unexercised retained mechanisms as untested rather than passing them by inference.

The stable-reserve mechanism passes only if both Zerg attempts are valid; reserve remote attack orders remain zero; accepted home moves do not exceed attempts; and, when accepted repeat moves exist, the minimum accepted repeat interval is at least 96 frames. Each Zerg attempt that reaches three completed combat units must record reserve peak three and a nonnegative first-three frame. If a first non-worker home threat observes `g >= 2` completed combat units globally, the reserve size and reserved-local count at that exact frame must each be at least `min(3, g)`. Across the two lanes, at least one must record a reserve remote-target suppression, at least one must record an accepted reserve local-defense attack, and at least one must record both a three-unit reserve and an accepted non-reserve remote attack with a nonnegative surplus-release frame and release army of at least four. These observations prove that the reserve exercised defense without freezing all offense. New reserve telemetry must remain zero or its documented `-1` sentinel in all three non-Zerg lanes. An unobserved three-unit reserve, suppression, local defense, surplus release or qualifying threat is reported as untested and does not satisfy the corresponding mechanism gate.

Report durable logical frames per second, callback p99/max time, callback CPU time and peak RSS for each game. The current rule has no fixed 384-fps gate: the 300-second game cap, 900-second cohort cap and lifecycle/integrity gates control execution validity. Shorter is favorable only for a verified win; a faster loss is not improvement.

## Decision and scope

Advance v32 to a separately registered held-out confirmation only if every integrity and regression gate passes, the stable-reserve mechanism gate passes, and the candidate records at least one verified win. A complete valid cohort missing any gameplay, mechanism, integrity or regression gate is `REJECT`; zero wins rejects advancement. An infrastructure-invalid attempt or cohort is `INCONCLUSIVE`, is preserved without retry, and does not count as a failed gameplay result. This exploratory screen cannot update Elo, replace canonical Kestrel v13, or establish tournament strength.

## Registered source identity

- Candidate source SHA-256: `7d5dd3a025b7d6728a9e4c50bd2471ca6d60286b1dcece9caabe4ecc4142d599`.
- Combined source SHA-256: `8497832a32a8e3e2b5a7badbf195c6d834907b3fc3024ba6ef052dd5e81a572f` over `Kestrel.cpp`, `CMakeLists.txt`, then `LICENSE` bytes.
- Candidate binary SHA-256: `3809371159c53fee4b761227d0d4d91d5b45bb5342ddda0be3ab73eba0a9899d`.
- Candidate binary path: `artifacts/builds/3809371159c53fee4b761227d0d4d91d5b45bb5342ddda0be3ab73eba0a9899d/kestrel-opening-v32-candidate/Kestrel.dylib`.
- Reconstruction patch: `patches/kestrel-v32-stable-zerg-reserve.patch`, SHA-256 `7ab53d2036addac5dcb6464c8ce24d318093dcc8c688d26de2dff8dac91c0e10`.

The frozen source compiled natively against OpenBW and against the official BWAPI 4.4 headers with Apple Clang 21.0.0 before registration was finalized. The archived binary has a build sidecar with the exact source, patch, compiler and base identities. The schedule records the final plan hash; the batch ledger will record the frozen schedule hash at launch.

## Frozen runtime identities

- Engine library SHA-256: `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`.
- Engine launcher: `artifacts/builds/eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b/openbw-terminal-drain/BWAPILauncher`.
- Game data: `third_party/game-data/runtime`.
- The opponent identities and hashes are frozen in `schedule.json`; preserve their Ours/Original/Port/Fork labels and source provenance in the build sidecars.
