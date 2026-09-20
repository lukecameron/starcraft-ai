# McRave ZvZ opening-selection and execution probe

Registered 2026-09-20T06:30:55Z, before compilation or execution. This is an observational diagnostic, not a strategy change or strength test.

## Question and design

The retained Heartbreak Ridge losses with seed 6301 reached the first Pool and Zerglings about 600 frames later than a Benzene win with seed 1001, but map and bot seed changed together and the replay does not identify McRave's opener. Does the delay follow the selected build tuple, or does it appear after the same tuple is selected on different maps?

Build an isolated diagnostic from frozen experimental candidate `436cfa74fa34c267f7404777a3170be0202485bdc7224d15fb30b85f02c5644e`; this base is retained and not adopted. Use adopted engine `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b` and frozen ZZZKBot `ce796a5d49d78121aaf42b57ba758423ee89f74a249b42180cbc0b0cb9df4748`. Run four serial games, always McRave player 1 Zerg and ZZZKBot player 2 Zerg, with empty isolated learning state and a 120-second cap:

1. seed/bot seed 1001 on Benzene;
2. seed/bot seed 1001 on Heartbreak Ridge;
3. seed/bot seed 6301 on Heartbreak Ridge;
4. seed/bot seed 6301 on Benzene.

The diagnostic records the initial and current build/opener/transition strings; first request frames for Pool, Extractor, additional Hatchery, additional Overlord, and Zergling pumping; and first observed frames for Pool, Extractor, additional Hatchery, additional Overlord, Zergling, Creep Colony, Sunken, Lair, and Spire. Starting Hatchery and Overlord counts are captured after initialization so they are not reported as new production. Existing gameplay alone controls every queue and command.

## Interpretation fixed before data

Adequate evidence requires all four games to complete without crash, hash mismatch, or contradictory terminal metadata; matching initial tuples for both maps within each seed; nonempty tuple labels; and durable opening timestamps through at least first Pool and Zergling. A mismatch between maps for the same seed, contaminated learning state, or missing telemetry is INCONCLUSIVE.

If tuples differ between seeds and each seed is stable across maps, classify opener selection as a seed-associated source of timing variation. Within each tuple, compare request frames, request-to-start gaps, and start-to-first-Zergling gaps across maps. If a later actual unit appears while its request frame remains similar, classify the difference as execution delay; if the request itself moves, classify it as build-state/queue timing. Report exact frames without claiming a general map effect from one observation per cell. If tuples are identical across both seeds, the selected opener does not explain this four-game timing difference and execution telemetry becomes the primary evidence.

No result permits forcing an opener, updating learning policy, or promoting strategy. The next change, if any, requires a separate shadow or strategy evaluation.
