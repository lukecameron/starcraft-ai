# McRave ZvZ 9Pool candidate matched evaluation

Registered 2026-09-20T06:44:40Z, before compiling the treatment or launching any trial. This evaluates a narrow strategy candidate; it cannot promote the change to the production baseline.

## Hypothesis

For empty-learning ZvZ games in which normal learning selects the `PoolLair / 1HatchMuta` family, replacing only its selected opener with 9Pool improves survival and match outcomes against frozen ZZZKBot relative to the unmodified frozen `436cfa74fa34c267f7404777a3170be0202485bdc7224d15fb30b85f02c5644e` build. The result is falsified if the treatment wins no more matched cells than control or its median paired survival-frame difference in cells where the opener actually changes is not positive.

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
| 5 | 1002 | Benzene | held-out seed |
| 6 | 1002 | Heartbreak Ridge | held-out seed |
| 7 | 8202 | Benzene | held-out seed |
| 8 | 8202 | Heartbreak Ridge | held-out seed |

Source-level inspection of the empty-learning random draws predicts PoolLair for all four seeds, but the observed control log is authoritative. A cell counts as an effective treatment only when its control log reports a non-9Pool PoolLair opener and the treatment log records that opener changing to 9Pool. A normally selected 9Pool cell remains a no-op control and is not moved into the effective subset after results are seen.

## Metrics and fixed decision rule

Primary outcome is matched win difference: treatment wins minus control wins across the eight cells, from opposing Boolean terminal results in each manifest. The supporting survival metric is the paired difference `treatment McRave terminal frame - control McRave terminal frame`, evaluated over the predeclared effective-or-no-op classification above; later terminal frames mean longer survival for losses, while wins remain reported separately rather than being treated as censored losses.

The treatment advances only to a separate independent confirmation if all of these hold:

1. all 16 games are valid;
2. treatment wins more of the eight matched cells than control;
3. among effective-treatment cells, at least three of four paired survival differences are positive and their median is greater than zero;
4. every treatment game reaches at least 384 durable logical frames per wall second; and
5. treatment aggregate player-1 CPU seconds per logical frame is no more than 10% above control.

If the complete cohort is valid but any bar fails, reject this candidate. Passing means only `ADOPT FOR INDEPENDENT CONFIRMATION`; production adoption requires a later preregistered comparison with independent seeds and broader opponents. Report Wilson 95% intervals for each arm's descriptive win proportion, but do not use interval overlap or relative Elo as the decision rule.

## Integrity, exclusions, and stopping

A game is valid only if both launcher processes exit zero, terminal callbacks are Boolean and opposing, no `insync_hash_mismatch` or engine kill-source failure is logged, both archived replay hashes still match their manifests, and both replays parse structurally with screp. Also require the control log to show `PoolLair / 1HatchMuta` and the treatment log to show the expected override behavior. An invalid game is preserved and not replaced; any invalid game makes the cohort `INCONCLUSIVE`. A timeout is invalid rather than a loss. Stop after 16 attempts, or stop immediately after two consecutive infrastructure-invalid attempts. Preserve all attempts and skipped cells.

The two maps and four seeds are a small local sample against one opponent. Fixed seeds correlate starts and bot decisions across arms, so conventional independent-trial uncertainty is only descriptive. No result supports a universal 9Pool policy, learning-policy removal, or a strength/rating claim.
