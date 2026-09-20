# Kestrel replay hill-climb baseline

Registered 2026-09-20 after the 9Pool confirmation checkpoint and before the first hill-climb batch. This is an exploratory improvement loop, not a replacement for the reviewed local Elo cohort.

## Objective

Measure the current Kestrel v19 experimental baseline against a small, varied set of frozen local bots, then use replay-derived signals to choose a short list of concrete improvements. A short, decisive game is useful evidence, but this screen does not convert game length into Elo and does not promote a bot.

## Frozen baseline and engine

- Candidate: Kestrel v19 experimental build `f02db8b97e01482f897a0f481c11a92f0cd5bc21f4629abea1f5a6d113b44b9`, Protoss, Ours/Original. Its source snapshot is `8994f313e679125395c360657b41c8559659db260f47a854c0c4ac98dfb87230`.
- Engine: adopted native headless OpenBW terminal-drain build `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`.
- Learning: empty isolated state per game, LF3, local transport.
- Wall limit: 300 seconds per game; cohort cap 900 seconds. The batch uses five concurrent game processes to exercise the available multicore machine. There is no 384-fps acceptance gate in this exploratory screen; durable throughput is reported with each manifest.

## Fixed five-game baseline matrix

| Game | Opponent | Race | Map | Seed | Kestrel slot |
|---:|---|---|---|---:|---:|
| 1 | ZZZKBot | Zerg | `sscai/(2)Benzene.scx` | 9801 | P1 |
| 2 | UAlbertaBot-Terran | Terran | `sscai/(2)Destination.scx` | 9802 | P2 |
| 3 | UAlbertaBot-Protoss | Protoss | `sscai/(2)Heartbreak Ridge.scx` | 9803 | P1 |
| 4 | McRave-9Pool-treatment | Zerg | `sscai/(4)Circuit Breaker.scx` | 9804 | P2 |
| 5 | Stardust-repaired | Protoss | `sscai/(2)Benzene.scx` | 9805 | P1 |

Each attempt is retained even if it fails to start or times out. The batch stops only after two consecutive infrastructure failures; there are no replacements or retries.

## Replay scorecard

`scripts/score_kestrel_hillclimb.py` scores the candidate-owned replay for each archived game. It records manifest and replay hashes, parser status, candidate result metadata, terminal frames and durable throughput, command/order counts, first build/production/attack/harvest frames, and four descriptive signals: economy, construction, production and combat. It adds a short-game flag at five minutes and a simple `strong`/`partial`/`weak` grade based on signal coverage. These are review aids only: replay commands do not prove command acceptance or hidden state.

After the batch, inspect every replay qualitatively and quantitatively. Select two to five changes that target recurring failures across opponents or maps. A change is eligible for the next loop only if its source diff is isolated, its build hash is recorded, and the next batch uses a new seed range. No candidate becomes canonical from one five-game screen.

## Hill-climb decision rule

Prefer a candidate for the next screen when it improves at least one predeclared recurring signal (earlier legal production, fewer rejected commands, earlier first attack, more surviving economy, or shorter completed game) without introducing an integrity failure, a missing replay, or a clear regression in another opponent lane. A positive screen schedules a held-out confirmation; it does not update `config/kestrel-baseline.json` or the local Elo anchors.
