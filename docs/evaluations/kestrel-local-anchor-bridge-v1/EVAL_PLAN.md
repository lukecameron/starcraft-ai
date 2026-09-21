# Kestrel v13 local-anchor bridge v1 plan — NOT RUN

Registered 2026-09-21 before gameplay. This fixed eight-game extension asks
whether a direct UAlbertaBot-Protoss bridge adds useful exact-regime evidence
to the canonical Kestrel v13 local rating component. It is descriptive Apple
Silicon OpenBW calibration, not BASIL, ladder, submission, or tournament
evidence.

## Question and existing evidence

The current 120-second component contains 28 reviewed Kestrel v13 games:
Kestrel scored 3-11 against UAlbertaBot-Terran and 0-14 against ZZZKBot. The
unchanged Gaussian-prior Bradley-Terry fit places Kestrel at 373.5 with an
approximate 95% conditional interval of [-115.6, 862.7] relative to the
arbitrary ZZZKBot coordinate of 1000. The interval remains 978.3 Elo wide and
is strongly prior-sensitive.

UAlbertaBot Protoss is not connected to that 120-second component. This
extension adds four UAlbertaBot-Protoss versus Kestrel games and four
UAlbertaBot-Protoss versus ZZZKBot games. The Kestrel edge connects the new
node; the ZZZK edge supplies direct reference evidence in the same regime.
Reviewed UAlbertaBot-Protoss reference games used a 180-second timeout and
therefore remain excluded. No previous result is imported across that
boundary.

## Frozen identities and regime

- UAlbertaBot Protoss, **Ours / Port**, original author David Churchill:
  module SHA-256
  `75ac4f6bb44ed6e48fbee883638c77df9557c9a88070ceca4de11183053238c9`;
  packaged `UAlbertaBot_Config.txt` SHA-256
  `e4b2a2f5e40f85c2fd3f43e094fdee4808062751f143d66c785ef0178ba91b39`;
  source <https://github.com/davechurchill/ualbertabot>.
- Kestrel v13 Protoss, **Ours / Original**, author Luke Cameron: module
  SHA-256
  `622bca47b47f78f3e9d1971d1e340f991b54ced7f3bfdfd932d3062e125cbd98`;
  source SHA-256
  `12cecdb5039569711c318bab5bb6781b4f1e86e22c87e453f9d85c295fa13df0`;
  reconstruction patch SHA-256
  `8fd24ff479bc5a8794f0ae092855082b1a44270123fe8cc1810ee1493996177b`.
- ZZZKBot Zerg, **Ours / Port**, original author Chris Coxe: module SHA-256
  `ce796a5d49d78121aaf42b57ba758423ee89f74a249b42180cbc0b0cb9df4748`;
  source revision `7183e37b6b416ea53c1040c83e639a3a3c395eed`;
  source patch SHA-256
  `aedeeef6cc664e9d49d181d8a0044e110008fdca720df386e02fadb95c784c2d`;
  source <https://github.com/chriscoxe/ZZZKBot>.
- Terminal-drain OpenBW engine SHA-256
  `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`;
  launcher SHA-256
  `af1682393f9fe43afe885b35a1637e9c464719ef93c83e799d614beed20316c1`;
  LF3, macOS ARM64, fresh empty isolated learning state, no adjudication, and
  a 120-second wall cap per game.

The committed schedule freezes module, sidecar, AI configuration, engine,
launcher, game-data, map, runner, provenance, source, and patch hashes. No
code, configuration, or learned state may change within the cohort.
`scripts/run_batch.py` verifies those optional frozen inputs before creating
the experiment directory and consumes the schedule's concurrency unless an
identical explicit value is supplied.

## Fixed schedule

Run the eight rows exactly once with concurrency four. Seeds 14001-14008 are
fresh and unique. Each edge covers all four established maps and has two games
with UAlbertaBot Protoss in each player slot. There is no reciprocal same-seed
pair.

| Game | Opponent | Map | Seed | UAlbertaBot Protoss slot |
| ---: | --- | --- | ---: | ---: |
| 1 | Kestrel v13 | Benzene | 14001 | P1 |
| 2 | ZZZKBot | Destination | 14002 | P2 |
| 3 | Kestrel v13 | Heartbreak Ridge | 14003 | P2 |
| 4 | ZZZKBot | Circuit Breaker | 14004 | P1 |
| 5 | Kestrel v13 | Destination | 14005 | P1 |
| 6 | ZZZKBot | Benzene | 14006 | P2 |
| 7 | Kestrel v13 | Circuit Breaker | 14007 | P2 |
| 8 | ZZZKBot | Heartbreak Ridge | 14008 | P1 |

No game, replay playback, build, profiler, or other engine experiment may
overlap this cohort. Preserve every attempt, manifest, diagnostic, log, and
replay. Do not retry, reseed, replace, or rerun a row. Stop after two
consecutive infrastructure-invalid completions or cohort completion; already
started rows remain part of the evidence ledger.

## Validity and rating decision

A valid row requires all frozen identities; the expected map, race, seed, and
slot; both child return codes zero; reciprocal terminal callbacks; one verified
winner; two archived replay copies whose source and archive hashes match; full
`screp` parsing; expected header races; and
`replay_header_frames + 1 == owning_callback_frame`. A timeout, crash,
state-hash error, unregistered kill event, missing or contradictory result,
missing replay, parse failure, or identity mismatch is infrastructure-invalid
and never becomes a rating outcome.

`ADOPT for local rating evidence only` requires at least seven valid rows, at
least three valid rows on each edge, at least one valid row in each
UAlbertaBot player slot on each edge, three distinct maps on each edge, and an
independent manifest/replay audit. Otherwise the fixed cohort is
`INCONCLUSIVE`. There is no strength threshold because this experiment
estimates frozen builds rather than selecting a policy.

If adopted, pin each exact final-manifest hash in `config/local-ratings.json`,
append a current 120-second bridge cohort, and recompute the unchanged
Gaussian-prior Bradley-Terry MAP with 400 Elo prior SD, approximate 95%
Laplace contrast intervals, and 200/800 sensitivity. Keep ZZZKBot at an
arbitrary displayed coordinate of 1000. Report direct records, maps, slots,
attrition, interval width, and prior sensitivity. Do not pool the existing
180-second UAlbertaBot-Protoss games. The scalar model still omits map, slot,
matchup, and repeated-game dependence; a narrower conditional interval does
not establish tournament calibration.
