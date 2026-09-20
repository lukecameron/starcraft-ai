# McRave ZvZ 9Pool independent confirmation plan

Registered 2026-09-20T07:09:09Z after lead review and before any confirmation trial. Seeds were assigned as a consecutive fresh range without simulating outcomes or inspecting their selected openers.

## Decision and hypothesis

The hypothesis is that the frozen 9Pool treatment `fd174fa451c5c79af53b84d882f983630536c31fe116d22b76495cd1610cacfa` increases paired wins against frozen ZZZKBot relative to frozen control `436cfa74fa34c267f7404777a3170be0202485bdc7224d15fb30b85f02c5644e`, across fresh starts, four maps, and both candidate player slots. A result with fewer than four net paired wins, insufficient exact discordant-pair evidence, or a material map/slot regression falsifies the adoption hypothesis for this opponent lane.

Passing this plan accepts the 9Pool hypothesis for the tested local ZZZKBot ZvZ lane. It does not justify a production policy that would affect every Zerg opponent. Production adoption still requires broader-opponent evidence; the UAlbertaBot compatibility recommendation below is a prerequisite to that next lane.

## Frozen inputs

- Engine: `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`.
- Control: McRave `436cfa74fa34c267f7404777a3170be0202485bdc7224d15fb30b85f02c5644e`.
- Treatment: McRave `fd174fa451c5c79af53b84d882f983630536c31fe116d22b76495cd1610cacfa`.
- Opponent: ZZZKBot `ce796a5d49d78121aaf42b57ba758423ee89f74a249b42180cbc0b0cb9df4748`, Zerg.
- Empty isolated learning state for every process; LF3; headless local transport; 120-second per-game wall cap.

For every pair, control and treatment use the same map, player slot, engine seed, McRave bot seed, and opponent. Normal learning remains enabled. Selected opener is logged and reported only as exploratory context; it is not an eligibility criterion or exclusion.

Pairing controls the configured map, slot, engine seed and bot RNG seed, but it does not guarantee identical simulation trajectories. The preceding evaluation produced a control win and treatment loss in one nominal no-op 9Pool pair. Address allocation, unit identifiers, iteration order, timing, or the treatment's extra logging/idempotent setter may still perturb play. The sign test assumes discordant pair directions are exchangeable under the null and that the 32 fresh scenario pairs are independent enough for its binomial model. Report this limitation alongside the exact result; do not describe fixed seeds as deterministic replay identity.

## Fixed 32-pair schedule

Run 64 games serially. Within odd-numbered pairs run control then treatment; within even-numbered pairs run treatment then control. Persist and fsync the pair definition before its first launch and checkpoint both attempts after every pair. Do not retry, replace, reseed, or reorder a failed attempt.

| Pairs | Map | Seeds in pair order | McRave slots in seed order |
|---|---|---|---|
| 1-8 | Benzene | 9101, 9102, 9103, 9104, 9105, 9106, 9107, 9108 | P1, P2, P1, P2, P1, P2, P1, P2 |
| 9-16 | Destination | 9109, 9110, 9111, 9112, 9113, 9114, 9115, 9116 | P1, P2, P1, P2, P1, P2, P1, P2 |
| 17-24 | Heartbreak Ridge | 9117, 9118, 9119, 9120, 9121, 9122, 9123, 9124 | P1, P2, P1, P2, P1, P2, P1, P2 |
| 25-32 | Circuit Breaker | 9125, 9126, 9127, 9128, 9129, 9130, 9131, 9132 | P1, P2, P1, P2, P1, P2, P1, P2 |

Use map paths `sscai/(2)Benzene.scx`, `sscai/(2)Destination.scx`, `sscai/(2)Heartbreak Ridge.scx`, and `sscai/(4)Circuit Breaker.scx`. McRave is Zerg and ZZZKBot is Zerg in every game. The listed seed is both `OPENBW_SCENARIO_SEED` and the McRave `MATCH_BOT_SEED`; deterministic player IDs remain attached to launcher positions.

## Primary metric and exact inference

For each valid pair classify the outcomes as concordant, treatment-only win, or control-only win. Let `b` be treatment-only wins and `c` control-only wins. Primary net paired win gain is `b - c`. Under the null that either arm is equally likely to win a discordant pair, the preregistered one-sided exact sign-test value is

`p = sum(comb(b + c, k) for k = b through b + c) / 2^(b + c)`.

Report `b`, `c`, net gain, the exact one-sided p-value, and a two-sided 95% Clopper-Pearson interval for `b / (b + c)`. If there are no discordant pairs, report the interval and p-value as unavailable and reject the hypothesis. Also report ordinary arm win proportions and Wilson intervals as descriptive context only.

## Adoption and engineering bars

Accept the tested ZZZKBot-specific hypothesis only if every condition holds:

1. all 64 games and all 32 pairs are valid;
2. `b - c >= 4`;
3. the one-sided exact sign-test `p <= 0.05`;
4. treatment-minus-control wins are at least -1 in every map stratum and at least -1 in each McRave-slot stratum, so no map or slot has a catastrophic regression of two or more net wins;
5. every game reaches at least 384 durable logical frames per wall second;
6. treatment aggregate candidate-process CPU seconds per logical frame are at most 110% of control;
7. each candidate process uses at most 125 CPU seconds and 768 MiB peak RSS; and
8. the completed cohort, including durable replay archival and pair checkpoints, takes at most 150 minutes wall time.

The candidate process measurement includes its BWAPILauncher, OpenBW engine, and loaded bot. Resource-limit failure rejects engineering acceptance even if the outcome test passes. Report per-map and per-slot `b`, `c`, net gain, throughput, CPU/frame, and peak RSS without inventing secondary adoption rules.

## Integrity, stopping, and preservation

A game is valid only if both launcher processes exit zero, callbacks contain exactly one winner and one loser, no `insync_hash_mismatch`, crash, timeout, or abnormal kill path occurs, both replay hashes match their manifests, and both replays parse structurally with screp and agree with owner race/frame headers. The adopted terminal-drain engine's known ordinary cleanup diagnostics are explicitly allowed: `kill_client` source `controller_not_occupied_after_action` with action ID 87 (`Leave Game`) and source `transport_callback` with action ID -1. These exact names and values occurred once per side in all 16 games of the preceding cohort. Any other `kill_client` source/action pair is marked review-required and cannot be silently accepted or rejected until its context and terminal results are inspected.

An invalid game is retained and never scored as a loss. One invalid attempt makes the outcome decision inconclusive. Stop immediately after two consecutive invalid attempts, after 64 attempts, or when the 150-minute cohort cap is reached. An interruption is inconclusive; resume only the unlaunched fixed schedule entries from the durable ledger. Report all attempts and skipped entries.

## UAlbertaBot Zerg compatibility prerequisite

The existing frozen UAlbertaBot binary `75ac4f6bb44ed6e48fbee883638c77df9557c9a88070ceca4de11183053238c9` is a credible cheap second-opponent lane, but native Zerg gameplay has not yet been demonstrated in retained project evidence. Its frozen config selects `Zerg_ZerglingRush`, whose opening explicitly requests a Drone, Spawning Pool, and Zerglings. `StrategyManager::getBuildOrderGoal()` dispatches on the actual self race and its Zerg branch continues requesting Zerglings. The package includes the exact hashed config under `AI/UAlbertaBot_Config.txt`, and its official-header check passed 115 translation units.

Run two separately preregistered compatibility games before committing the 64-game confirmation: treatment McRave versus UAlbertaBot Zerg once in each player slot, on Benzene and Destination with fresh seeds. Require clean opposing callbacks, ordinary terminal diagnostics, two parseable replays, at least one UAlberta Drone, Spawning Pool and Zergling command/observation, and at least 384 durable fps. These games test whether the lane is operational; they are not part of the ZZZKBot sign test and cannot support the 9Pool adoption decision. If either fails compatibility, diagnose that lane without altering this confirmation schedule.
