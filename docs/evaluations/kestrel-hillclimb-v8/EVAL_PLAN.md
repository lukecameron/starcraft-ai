# Kestrel v28 sixth-Pylon hill-climb

Registered 2026-09-20 after v27 reached the hard five-Pylon ceiling in four of five games but produced no win. v27 also failed two engineering gates, so v28 returns to the frozen v22 exploratory base, source SHA-256 `e82345ea48dbd32c4296e10c57f2ddd0804f4a8141a5ab417262f7a645758cb5` and binary SHA-256 `6e112c43d6dace13d1152c834658aa35647ceea29b761159187d44d3837fcf57`.

v28 changes one construction threshold: the supply-aware Pylon branch may construct a sixth Pylon instead of stopping at five. All opening timing, economy, production, combat, targeting, home hold and public-observation rules remain identical to v22. Added telemetry records the sixth Pylon's accepted, current and completed frames.

The hypothesis is that one additional Pylon will remove the repeated late-game supply ceiling and permit more army production in a lane that survives long enough. A successful mechanism requires at least one game to record `0 <= sixth_pylon_accepted_frame <= sixth_pylon_current_frame <= sixth_pylon_completed_frame`, report `max_pylons == 6`, and show the sixth Pylon in replay/metadata evidence. No game may report more than six Pylons. A game ending before that condition is a mechanism non-observation rather than a source failure.

Run exactly five candidate attempts concurrently against the frozen opponent gradient, with no retries or replacements:

| Game | Opponent | Map | Kestrel slot | Engine seed |
| ---: | --- | --- | ---: | ---: |
| 1 | ZZZKBot | Benzene | P1 | 9871 |
| 2 | UAlbertaBot-Terran | Destination | P2 | 9872 |
| 3 | UAlbertaBot-Protoss | Heartbreak Ridge | P1 | 9873 |
| 4 | McRave-9Pool-treatment | Circuit Breaker | P2 | 9874 |
| 5 | Stardust-repaired | Benzene | P1 | 9875 |

Use a 300-second wall cap for each game and a 900-second cohort cap. Omit unsupported `MATCH_BOT_SEED` flags. Preserve every manifest, runner log, result file, replay, hash and full replay parse, including invalid attempts.

The screen is valid only if all five attempts have reciprocal terminal results, matching replay hashes and full parsing; no launcher, state-hash or wrong-race failure; zero gas-worker build attempts; zero build `Unit_Busy` rejections; each attempt's rejected-command rate below 5%; and each attempt at or above 384 durable frames per second. Rejection rate is rejected commands divided by total attempted commands, checked per game and for the cohort aggregate. Stop after two consecutive infrastructure-invalid attempts or the cohort cap. Do not replace an invalid attempt.

Advance v28 to a matched confirmation only if it records at least one verified win, passes every integrity gate and demonstrates a current sixth Pylon in at least one game. Zero wins rejects advancement. If no game reaches the sixth-Pylon condition, classify the mechanism as untested and do not advance it. Fresh seeds make frame differences from v22 descriptive rather than a hard adoption gate. This five-game exploratory screen cannot update Elo, replace canonical Kestrel v13 or establish tournament strength.
