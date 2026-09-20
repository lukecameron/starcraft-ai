# McRave versus UAlbertaBot Zerg compatibility preflight

Registered 2026-09-20T07:09:09Z before either trial. This is a two-game compatibility check for a broader-opponent lane, not a strength comparison or evidence in the ZZZKBot confirmation.

## Frozen design

Use adopted engine `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`, treatment McRave `fd174fa451c5c79af53b84d882f983630536c31fe116d22b76495cd1610cacfa`, and frozen UAlbertaBot `75ac4f6bb44ed6e48fbee883638c77df9557c9a88070ceca4de11183053238c9`. Configure both bots as Zerg and use the exact packaged UAlbertaBot config SHA-256 `e4b2a2f5e40f85c2fd3f43e094fdee4808062751f143d66c785ef0178ba91b39`.

Run exactly two serial games with no retry:

1. seed and McRave bot seed 9201, Benzene, McRave player 1;
2. seed and McRave bot seed 9202, Destination, McRave player 2.

Each game has a 120-second wall cap. The cohort cap is 10 minutes including replay archival. Persist and fsync the schedule before launch and checkpoint after each game.

## Acceptance and integrity

Compatibility passes only if both games have zero child exits, exactly one winner and one loser, no timeout, crash or `insync_hash_mismatch`, two SHA-matching screp-readable replays with Zerg/Zerg headers, and at least 384 durable logical frames per wall second. UAlbertaBot must issue or observably realize all of a Drone, Spawning Pool and Zergling; absence of any makes compatibility inconclusive even if the game ends cleanly.

The adopted engine's allowed ordinary cleanup diagnostics are exactly `controller_not_occupied_after_action` with action ID 87 and `transport_callback` with action ID -1. Any other `kill_client` source/action pair is review-required rather than silently accepted. Preserve both attempts. One invalid or behavior-incomplete game makes the preflight inconclusive; two consecutive invalid games trigger the standard stop but add no retry.

Passing means only that frozen UAlbertaBot can exercise its configured `Zerg_ZerglingRush` lane against this candidate. Outcomes are descriptive and cannot be pooled with the ZZZKBot sign test. A later broader-opponent comparison needs its own control/treatment pairs and decision rule.
