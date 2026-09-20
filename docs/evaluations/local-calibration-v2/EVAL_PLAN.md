# Fresh local league on the repaired engine

Registered 2026-09-20T06:31:29.663619+00:00 before execution. The earlier cohort lost three of twelve games to a reproduced terminal disconnect race. Engine eee406 is now adopted after six clean registered regression/control games. Old results remain separate; this is fresh evidence, not repaired historical outcomes.

## Fixed design

Same five exact build/race/configuration nodes as v1: McRave04521 Zerg, Stardust103997 Protoss, ZZZKce796 Zerg, UAlberta75ac Terran and Protoss. Retain the same six matchup pairs and swapped protocol slots, but collect two map/seed blocks per pair: Heartbreak Ridge or Circuit Breaker with seeds7101/7102/7201/7202/7301/7302, then Destination or Benzene with seeds7201/7202/7301/7302/7401/7402. The linked schedules fully specify each assignment and explicit McRave seed. Slots within a pair share map and seeds. Four maps are covered in total. All other frozen module/config hashes remain fixed.

Exactly24 games across three eight-game schedules, concurrency2 per schedule,180s wall cap, LF3, empty isolated learning state. Serial sub-batches; two-consecutive-infrastructure-failure stop remains. No retries, replacements, seed changes or optional stopping based on outcomes. At most36 worker-minutes under timeout caps; expected under10 minutes elapsed. No overlapping game batches; light build/source/dashboard work may overlap, so timings are descriptive only. Preserve all attempts and both available replays.

## Decision and uncertainty

ADOPT this cohort as a complete local rating display only if24/24 games have opposing Boolean terminal results, both exits0, no hash mismatch, archived SHA-matching replays that parse and agree with owner race/frame, and all five nodes form one connected graph. Any invalid game rejects the complete-cohort hypothesis; preserve valid reviewed subset as partial. An interrupted collection is inconclusive. No candidate-strength promotion follows from this data collection.

Use the already tested Gaussian-prior Bradley–Terry model,400 Elo prior SD,95% Laplace contrast intervals and200/800 sensitivity. ZZZK1000 is an arbitrary reference. Do not pool old-engine games, upstream ratings, diagnostic fixtures or unreviewed runs. Report pairwise results and map/slot coverage alongside scalar estimates. Repeated map/slot pairs are correlated; priors and model assumptions affect sparse results. This cohort improves coverage, not an accuracy guarantee or tournament calibration.

The expected useful result is a clean current-engine graph and enough losses/wins to identify the next uncertain matchup. If all edges are one-sided, report wide intervals and seek closer-strength opponents rather than treating a sweep as precise Elo.

## Frozen schedules

- `config/local-calibration-v2-stardust.json` SHA256`33ca7a7e6a2a900d580c4176c2ee771e4950457b9bf4180deed0abec395c2b7f`
- `config/local-calibration-v2-uab-t.json` SHA256`fdd3817bf53129e36fd256947039d0aea3f1b8e04131fb8d5f4b9bbf8282c7a2`
- `config/local-calibration-v2-mcrave.json` SHA256`372f0af33ac22de29dca8f1b7a9e6e87e775465db6ea341e7ee6f8ba0090ee30`
