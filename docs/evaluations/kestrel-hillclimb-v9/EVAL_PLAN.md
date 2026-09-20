# Kestrel v29 build-commandability repair hill-climb

Registered 2026-09-20 after v28 verified a completed sixth Pylon in three lanes but recorded zero wins and failed its zero build-`Unit_Busy` gate. v29 retains the exact v28 sixth-Pylon policy, source SHA-256 `709ae8920a7724c7024e778dc83ceb6f2ec9bc5b4edf236f70f2a3129a3b0b5c` and binary SHA-256 `86e59d631f27c151b6bd893bf77cde3ab62073b7ece1b4dfde9084850e3b3c63`.

v29 adds one engineering guard to both generic and Assimilator construction paths: a worker must report `canBuild(type, tile)` through public BWAPI state before Kestrel issues the build command. A failed guard does not reserve the worker. Telemetry records guard-block counts, first and last block frames, and the last accepted construction frame. Opening, supply, economy, production, combat and targeting policy are otherwise identical to v28.

The hypothesis is that suppressing non-commandable build attempts will eliminate build `Unit_Busy` rejections without starving later construction. If a guard block occurs, the repair mechanism requires zero rejected build commands and `last_accepted_build_frame > first_build_commandability_guard_block_frame`. If no guard block occurs, the repair mechanism is untested rather than confirmed. The retained supply mechanism requires ordered sixth-Pylon accepted/current/completed frames and `max_pylons == 6` in at least one game; no game may exceed six Pylons.

Run exactly five candidate attempts concurrently against the frozen opponent gradient, with no retries or replacements:

| Game | Opponent | Map | Kestrel slot | Engine seed |
| ---: | --- | --- | ---: | ---: |
| 1 | ZZZKBot | Benzene | P1 | 9881 |
| 2 | UAlbertaBot-Terran | Destination | P2 | 9882 |
| 3 | UAlbertaBot-Protoss | Heartbreak Ridge | P1 | 9883 |
| 4 | McRave-9Pool-treatment | Circuit Breaker | P2 | 9884 |
| 5 | Stardust-repaired | Benzene | P1 | 9885 |

Use a 300-second wall cap for each game and a 900-second cohort cap. Omit unsupported `MATCH_BOT_SEED` flags. Preserve every manifest, runner log, result file, replay, hash and full replay parse, including invalid attempts.

The screen is valid only if all five attempts have reciprocal terminal results, matching replay hashes and full parsing; no launcher, state-hash or wrong-race failure; zero gas-worker build attempts; zero build `Unit_Busy` rejections; each attempt and the cohort aggregate below a 5% rejected-command rate; and each attempt at or above 384 durable frames per second. Rejection rate is rejected commands divided by total attempted commands. Stop after two consecutive infrastructure-invalid attempts or the cohort cap. Do not replace an invalid attempt.

Advance v29 to a matched confirmation only if it records at least one verified win, passes every integrity gate, exercises the build guard with later accepted construction, and demonstrates the retained sixth-Pylon mechanism in at least one game. Zero wins rejects advancement. If the build guard never blocks, classify its repair mechanism as untested and do not claim confirmation. This five-game exploratory screen cannot update Elo, replace canonical Kestrel v13 or establish tournament strength.
