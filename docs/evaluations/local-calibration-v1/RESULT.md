# Initial local league calibration — REJECT clean-cohort gate

All 12 scheduled games were attempted. Nine have clean opposing outcomes; three report both players as winners and are excluded. The registered 12/12 clean-completion requirement failed. No bot is promoted. A partial, explicitly uncalibrated league is displayed with the nine reviewed games; all five exact build/race/config nodes are connected.

## Results

| Matchup | Map | Clean score | Invalid |
|---|---|---:|---:|
| Stardust vs McRave | Heartbreak Ridge | No score | 2 |
| Stardust vs UAlberta Protoss | Circuit Breaker | 2–0 | 0 |
| UAlberta Terran vs UAlberta Protoss | Heartbreak Ridge | 0–2 | 0 |
| UAlberta Terran vs ZZZK | Circuit Breaker | 0–2 | 0 |
| McRave vs ZZZK | Heartbreak Ridge | 0–2 | 0 |
| McRave vs Stardust | Circuit Breaker | 0–1 | 1 |

McRave's previous 10/10 quick result on Benzene/Destination did not transfer to these new maps/opponent matchups. This is useful evidence of weakness, not a measured regression caused by a new code change. Its three clean games here are losses. Stardust and ZZZK remain undefeated in this tiny accepted sample; their relative ordering is not established reliably.

## Initial estimates

These are Gaussian-prior Bradley–Terry MAP values with approximate 95% Laplace contrast intervals. The exact ZZZK reference is assigned 1000 by definition. No BASIL observations enter the fit.

| Exact build/race | Clean record | Estimate | Approximate95% interval |
|---|---:|---:|---:|
| Stardust103997 Protoss | 3–0 | 1083.3 | 312.4–1854.1 |
| ZZZKce796 Zerg | 4–0 | 1000 reference | Fixed display coordinate |
| UAlberta75ac Protoss | 2–2 | 769.1 | 34.1–1504.1 |
| McRave04521 Zerg | 0–3 | 578.6 | −75.8–1233.0 |
| UAlberta75ac Terran | 0–4 | 449.4 | −261.9–1160.7 |

The wide overlapping intervals and 200/800 Elo prior sensitivity shown on the dashboard are material. Two maps, correlated swapped-slot pairs, default opponent randomness and style effects prevent a precise ladder inference. A changed binary gets a new node. Histories show cumulative evidence for exact builds, not transfer of predecessor wins.

## Evidence and performance

All 24 replay files are hash-checked and screp 1.13.4 parsed; each header frame count+1 matches its owner terminal callback and reported races match the launch. Invalid games retain both replays too. Valid games have both exit codes 0, opposing results and no engine hash-mismatch event. `config/local-ratings.json` freezes accepted manifest hashes, so unreviewed or altered manifests cannot silently enter the fit.

All-attempt durable aggregate: 138,606 frames / 205.826s = 673.4fps. Range: 389.2–3173.3fps. Development compilation may overlap; these timings are observational and cannot pass a performance gate.

Raw batch ledgers: `artifacts/experiments/local-calibration-v1-{stardust,uab-t,mcrave}/manifest.json`. Parser ledger: `artifacts/experiments/local-calibration-v1/replay-review.json`, SHA256`7cd86598916c6776244141b1fff216d058ae1fe4b7e144cfe715d67d11a7b34f`. Numerical/evidence tests cover independent grid/curvature checks, symmetry, sweeps, prior sensitivity, disconnected graphs, exact identity, regime separation, deduplication and review gating.

## Next decision

Investigate the repeated invalid McRave–Stardust outcomes before using that matchup as a dependable anchor. Inspect McRave losses against the rush bot on Heartbreak Ridge for a concrete strategic or map-handling cause. A small direct Stardust–ZZZK cohort would resolve the unobserved top edge, but register it separately after reviewing these results. Do not rerun this cohort or silently replace failed games.
