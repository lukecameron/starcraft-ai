# Current-engine local league — ADOPT display cohort

All24 registered games completed with verified opposing results, both child exits0 and no state-hash mismatch. All48 archived replay copies match their recorded SHA256, parse with screp1.13.4, contain the expected race pair and end at the owning callback frame minus one. The five exact build/race/config nodes form one connected comparison graph over four maps. Adopt this complete cohort for local-estimator display; no bot strength promotion follows.

## Local estimates

ZZZK1000 is an arbitrary coordinate, not its upstream BASIL rating. Intervals are approximate95% Gaussian-prior Bradley–Terry contrasts, conditional on the model, with400 Elo prior SD. The reference has zero displayed interval by definition; uncertainty about it is included in every other contrast.

| Exact build/race | Games W–L | Local estimate | Conditional interval | Prior SD200 /800 estimates |
|---|---:|---:|---|---|
| Stardust Protoss `1039975842c6` | 12–0 | 1278.8 | 737.3 to 1820.3 | 1146.5 / 1458.7 |
| ZZZKBot Zerg `ce796a5d49d7` | 7–1 | 1000.0 | 1000.0 to 1000.0 | 1000.0 / 1000.0 |
| McRave Zerg `04521befa41b` | 1–11 | 747.8 | 368.0 to 1127.6 | 755.1 / 775.8 |
| UAlbertaBot Protoss `75ac4f6bb44e` | 2–6 | 640.4 | 136.6 to 1144.1 | 761.8 / 484.5 |
| UAlbertaBot Terran `75ac4f6bb44e` | 2–6 | 616.7 | 166.7 to 1066.7 | 740.3 / 470.4 |

Stardust beat McRave8–0 and UAlberta Protoss4–0. ZZZK beat UAlberta Terran4–0 and McRave3–1. UAlberta Terran and Protoss split2–2: Terran won both Heartbreak Ridge games and lost both Destination games. Map, seed and matchup effects are not fitted; a scalar ranking cannot explain all style dependence.

The all-attempt durable rate was296,742 frames /408.462 seconds =726.5fps, with a slowest game351.1fps. Build work could overlap and these are rating scenarios; this is descriptive timing, not an engineering performance pass. Repeated map/slot pairs reduce effective independent information.

## Interpretation and next comparison

The cohort is complete and broadens coverage from two maps to four. It does not prove accurate absolute Elo or tournament transfer. Current-engine ratings never inherit the older engine's nine valid games or its three invalid outcomes. Apparent changes between old and current estimates combine different seeds, maps, outcome coverage and engine binaries; they are not a measured strategic improvement.

Stardust has no direct game against the ZZZK reference, and McRave has no direct comparison with either UAlberta variant in this cohort. Those missing edges are the next useful information. A new registered comparison should fill them before spending on many repeated one-sided pairings.

Replay review: local `artifacts/experiments/local-calibration-v2/replay-review.json`, SHA256`43098c7a9338b67c55addda784effe0b6ce8b1b3685c58dbe4aca5b6ed140736`. Rating inclusion is pinned to each final manifest hash in `config/local-ratings.json`. All attempts remain archived.
