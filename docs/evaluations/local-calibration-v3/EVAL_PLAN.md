# Fill missing edges in the current local league

Registered 2026-09-20T06:43:32.974452+00:00 before trials. V2 completed24 clean games but never paired Stardust directly with its ZZZK rating reference or McRave with either UAlberta variant. Priors and indirect graph paths dominate some estimates; these comparisons are more informative than repeating the existing one-sided edges.

## Fixed design and decision

No code treatment. Use the same five frozen module/race/AI-config nodes, adopted engineeee406,180s wall limit,LF3 and fresh empty learning state as v2. Four Stardust–ZZZK games and eight McRave–UAlberta games; each pairing uses Heartbreak Ridge and Circuit Breaker, paired protocol slots and fixed new seeds in the linked schedules. McRave bot seeds equal scenario seeds. Run sub-batches serially,concurrency2; normal source/build work may overlap, so timing is descriptive. Maximum18 worker-minutes under timeout caps; expected under10 minutes elapsed.

Exactly12 attempts, no retries/replacements or optional stopping. Existing two-consecutive-infrastructure-failure stop remains. ADOPT this extension as complete display evidence if12/12 have opposing results,both exits0,no state-hash mismatch,and two hash-matching screp-parsed replays with owner-frame/race checks. All three previously missing pairing types must have four valid outcomes. Any invalid attempt rejects completeness; preserve the reviewed subset. Interrupted collection is inconclusive. No bot promotion or required Elo direction.

## Rating interpretation

Pool reviewed games with v2 only when exact regime/node identities match; keep v1 historical engine separate. Use unchanged400 Elo Gaussian prior,95% Laplace contrast intervals and200/800 sensitivity. ZZZK1000 remains arbitrary. Report direct pairwise records, current cumulative ratings, prior sensitivity and interval widths. Narrower conditional intervals are useful but do not guarantee calibration; repeated map/slot pairs and style-specific outcomes can violate independence/transitivity. No BASIL transfer, causal engine effect or tournament claim.

If new edges strongly contradict indirect estimates, inspect matchup records before collecting more. Do not change the model or acceptance threshold to conceal contradictory results.

## Frozen schedules

- `config/local-calibration-v3-stardust.json` SHA256`a313bd585c8f0fea5a99c95311dbbaa45e3ec746d6a7aa1f8a2291ce482c7efb`
- `config/local-calibration-v3-mcrave.json` SHA256`c2a7e93155fc35360b02733e7b5c73358b66d86efe2cabeb7808b36aabca077c`
