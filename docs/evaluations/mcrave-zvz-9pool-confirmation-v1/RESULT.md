# McRave ZvZ 9Pool independent confirmation result

## Decision: ADOPT FOR THE TESTED ZZZKBot LANE ONLY

The frozen 9Pool treatment met every preregistered outcome, integrity, throughput, CPU, memory and wall-time gate against frozen ZZZKBot. This accepts the hypothesis for this local ZZZKBot ZvZ lane. It does not make the treatment the production baseline or establish BASIL or tournament strength; broader-opponent confirmation remains required.

The preregistered evaluation plan SHA-256 is `cb5b9883cf86bc2be047e30527dd5a0e1dd1da9be3bc67b17df4e59587c1f155`. The executed schedule SHA-256 is `0376b74e77964b6aeee53f1524650c06eb601c12316f28ece68eb3174b0e385b`; its frozen copy SHA-256 is `6a05fea4d7bab108c1d5b4ec8c5d7e0cd6c8c6ea0572e0728559fe40eed3aeaf`.

## Paired outcome

All 64 games in all 32 fixed pairs were valid. The treatment had 29 wins and the control 24 wins; 11 pairs were concordant wins for both arms, 16 were concordant losses for both arms, 5 were treatment-only wins, and 0 were control-only wins. Therefore `b = 5`, `c = 0`, and the paired net gain is **+5**. The preregistered one-sided exact sign-test value is `1 / 2^5 = 0.03125`, below `0.05`. The two-sided 95% Clopper-Pearson interval for the treatment share of discordant pairs is approximately `[0.478, 1.000]`.

Descriptive arm win proportions are treatment `29/64 = 45.3%` with Wilson 95% interval `[33.7%, 57.4%]`, and control `24/64 = 37.5%` with Wilson 95% interval `[26.7%, 49.7%]`. These intervals are descriptive and were not used as the decision rule.

| Stratum | Pairs | Control wins | Treatment wins | Treatment-only `b` | Control-only `c` | Net |
|---|---:|---:|---:|---:|---:|---:|
| Benzene | 8 | 8 | 8 | 0 | 0 | 0 |
| Destination | 8 | 4 | 6 | 2 | 0 | +2 |
| Heartbreak Ridge | 8 | 6 | 8 | 2 | 0 | +2 |
| Circuit Breaker | 8 | 6 | 7 | 1 | 0 | +1 |
| McRave slot P1 | 16 | 15 | 16 | 1 | 0 | +1 |
| McRave slot P2 | 16 | 9 | 13 | 4 | 0 | +4 |

Every map and slot stratum met the preregistered treatment-minus-control lower bound of `-1`; no stratum had a control-only win.

## Engineering gates

The durable ledger `artifacts/experiments/mcrave-zvz-9pool-confirmation-v1/paired-ledger.json` reports status `completed`, 64 valid attempts, 32 checkpointed pairs, and 1,180.311 active seconds (19.672 minutes), below the 150-minute cap. Its SHA-256 is `28c4d839375508e35ea4bea6a92056c8e0f7ea3d4af683c65453825e206e91f8`.

All 128 replay copies matched their manifest hashes, parsed fully with `screp`, had no command-parse errors, matched owner callback frames, and contained the expected Zerg/Zerg headers. Every attempt had zero invalid reasons, opposing terminal callbacks, zero launcher exits, no state-hash mismatch, no timeout, no crash, and only the two registered terminal-drain cleanup events. No retries, replacements, reseeding, or reordered attempts occurred.

The slowest durable game was treatment pair 18 on Heartbreak Ridge at **514.33 logical frames/s**, above the 384-fps floor. Treatment candidate-process CPU was 555.2771759999999 seconds over 414,256 callback frames, or **0.0013404204 CPU s/frame**. Control CPU was 481.839481 seconds over 371,073 frames, or **0.0012985032 CPU s/frame**. The treatment/control ratio was **1.03228 (103.23%)**, below the 110% limit.

The maximum treatment candidate-process CPU time was 26.746689 seconds, below the 125-second limit. Maximum treatment peak RSS was 489,832,448 bytes (467.14 MiB), below 768 MiB and below the control maximum of 491,880,448 bytes (469.09 MiB); the treatment/control RSS ratio was 99.58%.

The frozen control module was `436cfa74fa34c267f7404777a3170be0202485bdc7224d15fb30b85f02c5644e`; the treatment module was `fd174fa451c5c79af53b84d882f983630536c31fe116d22b76495cd1610cacfa`; the opponent was ZZZKBot `ce796a5d49d78121aaf42b57ba758423ee89f74a249b42180cbc0b0cb9df4748`; and the adopted engine was `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`.

## Limits

The result is based on one frozen ZZZKBot build, four maps, 32 paired seeds, and the Apple Silicon OpenBW regime. Fixed seeds align scenario inputs but do not guarantee identical trajectories; address allocation, timing and iteration effects can remain. The result is therefore a local opponent-lane result. It does not justify changing the canonical production build, claiming a BASIL rating, or pooling these games with another engine, platform or opponent regime.
