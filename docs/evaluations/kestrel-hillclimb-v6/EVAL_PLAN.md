# Kestrel v26 Zerg tech-first construction hill-climb

Registered 2026-09-20 after the v23 hold-size and v24-v25 target-selection candidates produced no wins. The frozen behavioral base is Kestrel v22, source SHA-256 `e82345ea48dbd32c4296e10c57f2ddd0804f4a8141a5ab417262f7a645758cb5` and binary SHA-256 `6e112c43d6dace13d1152c834658aa35647ceea29b761159187d44d3837fcf57`.

v26 changes one construction policy for known Zerg opponents: after two accepted Zealot trains, it starts an Assimilator and Cybernetics Core before accepting the second Gateway. v22 accepted the second Gateway first and could spend the opening minerals before either tech structure. The two-local-Zealot home hold, economy, public-observation rules and combat targeting remain unchanged. Added telemetry records accepted, current and completed frames for the Assimilator and Core, the second Gateway accepted frame and the first accepted Dragoon train; this telemetry does not affect decisions.

The hypothesis is that reserving the second-Gateway slot until the Core has started will convert v22's recurring zero-tech Zerg openings into earlier Dragoon production while preserving the existing defense. A successful mechanism requires `first_core_accepted_frame < second_gateway_accepted_frame` whenever a second Gateway is accepted, plus at least one accepted Core or Dragoon in a Zerg lane that reaches two accepted Zealot trains.

Run exactly five candidate attempts concurrently against the existing frozen opponent gradient, with no retries or replacements:

| Game | Opponent | Map | Kestrel slot | Engine seed |
| ---: | --- | --- | ---: | ---: |
| 1 | ZZZKBot | Benzene | P1 | 9851 |
| 2 | UAlbertaBot-Terran | Destination | P2 | 9852 |
| 3 | UAlbertaBot-Protoss | Heartbreak Ridge | P1 | 9853 |
| 4 | McRave-9Pool-treatment | Circuit Breaker | P2 | 9854 |
| 5 | Stardust-repaired | Benzene | P1 | 9855 |

Use a 300-second wall cap for each game and a 900-second cohort cap. Omit unsupported `MATCH_BOT_SEED` flags. Preserve every manifest, runner log, result file, replay, hash and full replay parse, including invalid attempts.

The screen is valid only if all five attempts have reciprocal terminal results, matching replay hashes and full parsing; no launcher, state-hash or wrong-race failure; zero gas-worker build attempts; zero build `Unit_Busy` rejections; total command rejection below 5%; and durable throughput of at least 384 frames per second. Stop after two consecutive infrastructure-invalid attempts or the cohort cap. Do not replace an invalid attempt.

Advance v26 to a matched confirmation only if it records at least one verified win, passes every integrity gate and demonstrates the registered tech-before-second-Gateway ordering in at least one Zerg lane. Zero wins rejects the candidate for advancement even if the mechanism fires. Fresh seeds make per-lane frame differences from v22 descriptive rather than a hard adoption gate. This five-game exploratory screen cannot update Elo, replace canonical Kestrel v13 or establish tournament strength.
