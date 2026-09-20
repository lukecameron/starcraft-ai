# Kestrel v27 home-rally override hill-climb

Registered 2026-09-20 after v26 verified its Zerg tech-order mechanism but produced no wins and no Dragoons in either Zerg lane. This candidate returns to the stronger exploratory v22 base, source SHA-256 `e82345ea48dbd32c4296e10c57f2ddd0804f4a8141a5ab417262f7a645758cb5` and binary SHA-256 `6e112c43d6dace13d1152c834658aa35647ceea29b761159187d44d3837fcf57`.

v27 changes one combat condition. When a publicly observed combat threat is inside the home radius and fewer than two completed local Zealots exist, an out-of-radius Zealot now receives a move-home command whenever its current target position differs from home. v22 only issued that command when the unit was not moving, so an outbound move or attack could prevent the home response. Each Zealot can receive at most one accepted home-rally order per game, preventing repeated commands while the persistent threat flag is active. Economy, construction, unit production, target selection, the two-local hold threshold and public-observation rules are unchanged. Added telemetry records the first accepted home-rally frame, accepted order count and unique rallied-unit count.

The hypothesis is that overriding an existing outbound order will return at least one completed Zealot to the threatened base before the first home loss and improve early-fight conversion. A successful mechanism requires at least one threatened Zerg lane to record an accepted home-rally order at or after the first home-threat frame and at least one local completed Zealot before the first recorded home Zealot loss or game end.

Run exactly five candidate attempts concurrently against the frozen opponent gradient, with no retries or replacements:

| Game | Opponent | Map | Kestrel slot | Engine seed |
| ---: | --- | --- | ---: | ---: |
| 1 | ZZZKBot | Benzene | P1 | 9861 |
| 2 | UAlbertaBot-Terran | Destination | P2 | 9862 |
| 3 | UAlbertaBot-Protoss | Heartbreak Ridge | P1 | 9863 |
| 4 | McRave-9Pool-treatment | Circuit Breaker | P2 | 9864 |
| 5 | Stardust-repaired | Benzene | P1 | 9865 |

Use a 300-second wall cap for each game and a 900-second cohort cap. Omit unsupported `MATCH_BOT_SEED` flags. Preserve every manifest, runner log, result file, replay, hash and full replay parse, including invalid attempts.

The screen is valid only if all five attempts have reciprocal terminal results, matching replay hashes and full parsing; no launcher, state-hash or wrong-race failure; zero gas-worker build attempts; zero build `Unit_Busy` rejections; total command rejection below 5%; and durable throughput of at least 384 frames per second. Home-rally telemetry must report equal accepted-order and unique-unit counts, and that count must not exceed maximum observed Zealots. Stop after two consecutive infrastructure-invalid attempts or the cohort cap. Do not replace an invalid attempt.

Advance v27 to a matched confirmation only if it records at least one verified win, passes every integrity gate and demonstrates the registered rally mechanism in a threatened Zerg lane. Zero wins or failure to observe the mechanism rejects the candidate for advancement. Fresh seeds make frame differences from v22 descriptive rather than a hard adoption gate. This five-game exploratory screen cannot update Elo, replace canonical Kestrel v13 or establish tournament strength.
