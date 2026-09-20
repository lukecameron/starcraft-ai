# Evaluation plan: first controlled quick baseline

Registered 2026-09-20 before any game in `quick-mcrave-crashfix-baseline-v1`.

## Decision

- Change under evaluation: the frozen native McRave Zerg package with the queue lifetime and block-grid bounds repairs, binary SHA-256 `c49ee3c4b20a2772f1bfca03249c182d32a7238f9453a7a568990a188a1c4c65`.
- Decision controlled: accept this package as the operational reference for the next strategic experiment. This evaluation cannot establish a strength gain over upstream or an absolute BASIL rating.
- Adoption threshold: all ten scheduled games complete with two zero process exits, opposing terminal callbacks, archived replays, and no observed candidate crash. Report every failure; do not replace an inconvenient trial.

## Hypothesis

- Hypothesis: the repaired McRave package can complete the ten controlled cross-race scenarios in the frozen schedule, providing an initial descriptive matchup baseline.
- Falsified if: a candidate process crashes, or candidate behavior is shown to be incomplete/crippled in a replay. Other engine/result failures make the operational-reference decision inconclusive.

## Design

- Control: no strategic-change control arm. Prior failing runs establish the reproduced reliability problem and remain archived; their different seeds do not constitute paired strength comparisons.
- Treatment: frozen repaired McRave package; opponents are frozen ZZZKBot Zerg, UAlbertaBot Protoss, and UAlbertaBot Terran. These are two opponent codebases and three race/policy configurations.
- Ablations: none. The two undefined-behavior fixes address separately observed problems; this batch does not attribute a strategic gain to either.
- Minimum sample: ten completed games required for operational adoption. All attempted games enter the failure report.
- Stop: exactly ten preregistered attempts, unless interrupted or two consecutive completed attempts are infrastructure failures (crash, timeout, missing/inconsistent result, launcher failure). Already-running games may finish; skipped games stay explicit. Each game has a 120-second wall cap; concurrency is two. No retry within this evaluation.
- Schedule: `config/quick-schedule.json`, copied and hashed before launch; five Benzene and five Destination games, candidate in each launcher position five times. Seeds are registered there; paired ZZZK games swap policies across the same starts.

## Primary metric

- Name: verified completion fraction.
- Direction/unit: higher is better, fraction of ten scheduled games.
- Formula: count(games with status completed, outcome_verified true, both return_code 0, and nonempty replay archive) / 10.
- Source fields: each run's manifest.status, outcome_verified, players[].return_code, replays[].sha256/path and its referenced experiment ledger.
- Secondary: candidate clean-game win/loss counts by exact opponent/race; nominal Wilson 95% intervals; relative Elo advantage `400 * log10(p / (1-p))` per opponent only, with infinite observed endpoints and transformed intervals. No pooled Elo across different opponents. Failures are separate and cannot increase the clean-game denominator.
- Performance: durable end-to-end frames/s for each game, pooled frames divided by summed per-game durable seconds, slowest game, batch wall time, and whole-process peak RSS. This small opening-heavy cohort is not a representative late-game performance suite.

## Validity

- Invalid trials: engine startup/crash, inconsistent terminal results, missing replay or provenance mismatch. Retain all raw records and reason; no automatic exclusion from the reliability fraction.
- Exclusions: failed/unfinished trials are excluded only from descriptive completed-game win rate. They remain visible failures. Repeated identical deterministic games do not count as new evidence; this schedule uses distinct assignments/scenarios.
- Environment: pinned native ARM64 OpenBW and BWAPI, headless, multiplayer LF3, engine scenario patch recorded in every manifest. Bot internal time/search scheduling may still be nondeterministic.
- Controls: frozen module hashes and packaged AI configuration hashes; fresh per-player read/write; same map bytes and game data; source/patch provenance retained. Bot policy uses public BWAPI observations. Engine, ports or schedule changes during collection invalidate this evaluation and require a new plan.
- Uncertainty: Wilson intervals are descriptive conditional intervals for this small selected cohort; paired starts and related UAlberta race configurations limit independence. Ladder binary/version match and cross-engine transfer remain unknown.

## Result contract

- ADOPT: ten of ten verified completions, no candidate crash, and replay inspection supports active normal gameplay. Adoption means operational reference only.
- REJECT: a reproduced candidate crash or crippled policy falsifies the reliability hypothesis.
- INCONCLUSIVE: interruption, unresolved engine/result failure, insufficient valid coverage, or changed inputs prevents the registered acceptance check.
- Raw data: `artifacts/experiments/quick-mcrave-crashfix-baseline-v1/`, referenced `artifacts/runs/`, and all replay archives.
- Report: `docs/evaluations/quick-baseline-v1/RESULT.md`; negative and inconclusive results remain there.
- Publication: publish every outcome and its limitations to the user-requested dashboard. Publication is not strength promotion or tournament submission.
