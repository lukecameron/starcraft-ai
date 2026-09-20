# McRave ZvZ 9Pool candidate matched evaluation

Registered 2026-09-20T06:44:40Z, before compiling the treatment or launching any trial. This evaluates a narrow strategy candidate; it cannot promote the change to the production baseline.

## Hypothesis

For empty-learning ZvZ games in which normal learning selects the `PoolLair / 1HatchMuta` family, replacing only its selected opener with 9Pool improves match outcomes against frozen ZZZKBot relative to the unmodified frozen `436cfa74fa34c267f7404777a3170be0202485bdc7224d15fb30b85f02c5644e` build. The result is falsified if the treatment wins no more matched cells than control or produces any treatment-loss/control-win regression in a cell where the opener actually changes.

## Arms and source control

- Control: frozen McRave `436cfa74fa34c267f7404777a3170be0202485bdc7224d15fb30b85f02c5644e`.
- Treatment: the same full source, plus one post-learning override. Normal learning and `getPermanentBuild()` run first, preserving RNG consumption. In ZvZ only, when the selected build is `PoolLair`, the code retains the selected build and transition and changes only the opener to `9Pool`. A log records the pre-override opener. It does not force an incompatible 9Pool opener into another build family.
- Opponent: frozen ZZZKBot `ce796a5d49d78121aaf42b57ba758423ee89f74a249b42180cbc0b0cb9df4748`, Zerg.
- Engine: adopted frozen OpenBW package `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`.

The full treatment patch and incremental strategy diff are frozen before compilation. Both arms use empty isolated learning state. McRave is always player 1 and ZZZKBot player 2.

## Fixed scenario matrix and order

Run exactly 16 serial games, one control and one treatment for each cell below, with a 120-second wall cap. Within a cell use the listed value for both engine seed and McRave bot seed. Run control then treatment, proceeding in table order.

| Cell | Seed | Map | Role |
|---|---:|---|---|
| 1 | 1001 | Benzene | observed 9Pool negative control |
| 2 | 1001 | Heartbreak Ridge | observed 9Pool negative control |
| 3 | 6301 | Benzene | observed Gaspool effective treatment |
| 4 | 6301 | Heartbreak Ridge | observed Gaspool effective treatment |
| 5 | 1002 | Benzene | held-out, source-predicted Overpool effective treatment |
| 6 | 1002 | Heartbreak Ridge | held-out, source-predicted Overpool effective treatment |
| 7 | 8202 | Benzene | held-out, source-predicted 9Pool negative control |
| 8 | 8202 | Heartbreak Ridge | held-out, source-predicted 9Pool negative control |

Source-level inspection of the empty-learning random draws predicts PoolLair for all four seeds, with 1001 and 8202 selecting 9Pool, 6301 selecting Gaspool, and 1002 selecting Overpool. The observed control log remains authoritative. A cell is effective exactly when its control log reports a non-9Pool PoolLair opener and its treatment log reports that opener changing to 9Pool; a normally selected 9Pool cell is a no-op. This classification follows the frozen logs rather than outcome data. Fewer than two effective cells makes the cohort inconclusive.

## Metrics and fixed decision rule

Primary outcome is matched win difference: treatment wins minus control wins across the eight cells, from opposing Boolean terminal results in each manifest. For each effective cell, a benefit means either treatment win/control loss, or both arms losing with the treatment surviving to a later McRave terminal frame. Both-arm wins are neutral regardless of terminal time. A treatment loss/control win is a regression. Report the median paired terminal-frame difference only among both-loss effective pairs; if there are none, that metric is unavailable and does not veto faster wins.

The treatment advances only to a separate independent confirmation if all of these hold:

1. all 16 games are valid;
2. treatment wins more of the eight matched cells than control;
3. at least two effective cells are observed, at least half of the effective cells are benefits, and none is a treatment-loss/control-win regression;
4. every treatment game reaches at least 384 durable logical frames per wall second; and
5. treatment aggregate player-1 CPU seconds per logical frame is no more than 10% above control.

If the complete cohort is valid but any bar fails, reject this candidate. Passing means only `ADOPT FOR INDEPENDENT CONFIRMATION`; production adoption requires a later preregistered comparison with independent seeds and broader opponents. Report Wilson 95% intervals for each arm's descriptive win proportion, but do not use interval overlap or relative Elo as the decision rule.

## Integrity, exclusions, and stopping

A game is valid only if both launcher processes exit zero, terminal callbacks are Boolean and opposing, no `insync_hash_mismatch` or engine kill-source failure is logged, both archived replay hashes still match their manifests, and both replays parse structurally with screp. Also require the control log to show `PoolLair / 1HatchMuta` and the treatment log to show the expected override behavior. An invalid game is preserved and not replaced; any invalid game makes the cohort `INCONCLUSIVE`. A timeout is invalid rather than a loss. Stop after 16 attempts, or stop immediately after two consecutive infrastructure-invalid attempts. Preserve all attempts and skipped cells.

The two maps and four seeds are a small local sample against one opponent. Fixed seeds correlate starts and bot decisions across arms, so conventional independent-trial uncertainty is only descriptive. No result supports a universal 9Pool policy, learning-policy removal, or a strength/rating claim.

## Frozen build record

Recorded 2026-09-20T06:46:57Z without changing the registered design or decision rule. The native module and all 114 translation units against official BWAPI 4.4 headers compiled successfully with at most four jobs.

- Treatment module SHA-256: `fd174fa451c5c79af53b84d882f983630536c31fe116d22b76495cd1610cacfa`
- Package: `artifacts/builds/fd174fa451c5c79af53b84d882f983630536c31fe116d22b76495cd1610cacfa/mcrave-zvz-9pool-candidate/`
- Full source patch SHA-256: `f4a4d92df63ecf5cea055bf9edaa8eee8076819b68dbb46866eb9efaffa90650`
- Incremental strategy diff SHA-256: `bf8f5cef78ff7dc4c431b7758e3555d2cf3e1a55ed7a70dbf618f7b48a6d18f7`
- Build sidecar SHA-256: `4bb5223ce11ccd97b474877d9ebb7510ec8515db3b0c79eea88483a1db896e73`

## Pre-execution amendment

At 2026-09-20T06:47:31Z, before any trial, lead review identified that the original survival rule could penalize a faster treatment win and assumed exactly four effective cells. The fixed rule above instead treats wins categorically, defines benefit for both-loss pairs using survival, prohibits treatment-loss/control-win regressions, and requires at least two objectively observed effective cells. This amendment changes no source, scenario, integrity rule, performance guard, or trial count.
