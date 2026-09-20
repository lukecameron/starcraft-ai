# Kestrel v13 local-anchor v3 plan — NOT RUN

Registered 2026-09-20T19:28:00Z, before gameplay. This is a fixed 16-game
extension of the accepted Kestrel v13 local rating anchor. Its purpose is to
narrow uncertainty around the exact canonical build under the same 120-second
LF3 OpenBW regime as `kestrel-local-anchor-v1`. It is descriptive Apple Silicon
current-engine calibration, not BASIL, ladder, submission, or tournament
evidence.

## Prior evidence and question

The valid v1 anchor is 12 games: Kestrel v13 scored 2-4 against UAlbertaBot
Terran and 0-6 against ZZZKBot, yielding a prior-dependent Gaussian-prior
Bradley-Terry estimate of 497.9 with approximate 95% interval [-26.2, 1021.9]
relative to the arbitrary ZZZKBot 1000 coordinate. The v2 repeat is permanently
INCONCLUSIVE and excluded: its second row reached frame 100003, both launchers
reported `execute_action: unknown action 8`, and one transport was killed
without terminal results or replays.

The question is whether 16 fresh, uniquely seeded games improve the precision
of the exact-build estimate without repeating v2's immediate reciprocal
same-seed pattern. A preregistration-time simulation at the current fitted
probabilities reduced expected interval width from about 1048 to 830 Elo; the
actual estimate and interval remain outcome-dependent.

## Frozen identities and regime

- Kestrel v13, Protoss, **Ours / Original**, author Luke Cameron: binary
  `622bca47b47f78f3e9d1971d1e340f991b54ced7f3bfdfd932d3062e125cbd98`,
  source `12cecdb5039569711c318bab5bb6781b4f1e86e22c87e453f9d85c295fa13df0`,
  reconstruction patch
  `8fd24ff479bc5a8794f0ae092855082b1a44270123fe8cc1810ee1493996177b`.
- UAlbertaBot Terran, **Ours / Port**, original author David Churchill: binary
  `75ac4f6bb44ed6e48fbee883638c77df9557c9a88070ceca4de11183053238c9`,
  source <https://github.com/davechurchill/ualbertabot>.
- ZZZKBot, **Ours / Port**, original author Chris Coxe: binary
  `ce796a5d49d78121aaf42b57ba758423ee89f74a249b42180cbc0b0cb9df4748`,
  source <https://github.com/chriscoxe/ZZZKBot>.
- OpenBW terminal-drain engine package
  `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`,
  launcher `af1682393f9fe43afe885b35a1637e9c464719ef93c83e799d614beed20316c1`,
  LF3, empty isolated learning state, and 120-second wall cap per game.

The schedule freezes all module, source, patch, sidecar, launcher, game-data,
map, runner, and provenance hashes. No code or learned state may change within
the cohort.

## Fixed schedule

Run the 16 rows exactly once with concurrency five, unique scenario seeds
9801-9816, no retry, replacement, reseed, or outcome-adaptive row. Each
opponent receives eight games across Benzene, Destination, Heartbreak Ridge,
and Circuit Breaker. Kestrel uses each player slot four times per opponent.
The two blocks repeat the map/slot pattern with fresh seeds; no map reuses a
seed and no seed is used for a reciprocal slot flip.

| Game | Opponent | Map | Seed | Kestrel slot |
| ---: | --- | --- | ---: | ---: |
| 1 | UAlbertaBot-Terran | Benzene | 9801 | P1 |
| 2 | ZZZKBot | Destination | 9802 | P2 |
| 3 | UAlbertaBot-Terran | Heartbreak Ridge | 9803 | P2 |
| 4 | ZZZKBot | Circuit Breaker | 9804 | P1 |
| 5 | UAlbertaBot-Terran | Destination | 9805 | P1 |
| 6 | ZZZKBot | Benzene | 9806 | P2 |
| 7 | UAlbertaBot-Terran | Circuit Breaker | 9807 | P2 |
| 8 | ZZZKBot | Heartbreak Ridge | 9808 | P1 |
| 9 | UAlbertaBot-Terran | Benzene | 9809 | P1 |
| 10 | ZZZKBot | Destination | 9810 | P2 |
| 11 | UAlbertaBot-Terran | Heartbreak Ridge | 9811 | P2 |
| 12 | ZZZKBot | Circuit Breaker | 9812 | P1 |
| 13 | UAlbertaBot-Terran | Destination | 9813 | P1 |
| 14 | ZZZKBot | Benzene | 9814 | P2 |
| 15 | UAlbertaBot-Terran | Circuit Breaker | 9815 | P2 |
| 16 | ZZZKBot | Heartbreak Ridge | 9816 | P1 |

The runner stops after two infrastructure-invalid completions in succession
or cohort completion. Because five games may already be in flight, every
started row is preserved and assessed. Pending rows after a stop remain
explicitly skipped. The direct runner preserves every manifest and log
incrementally.

## Integrity and rating decision

A valid row requires the frozen identities; expected map, race, seed and slot;
both launcher return codes zero; reciprocal terminal callbacks; a verified
winner; exactly two archived replay copies with matching source/archive hashes;
complete `screp` parsing; expected header races; and
`replay_header_frames + 1 == owning_callback_frame`. Any timeout, crash,
state-hash error, unknown-action transport failure, missing result, missing
replay, parser error, or identity mismatch is infrastructure-invalid and is
never converted into a game result.

`ADOPT for local rating evidence only` requires at least 14 valid rows, at
least six valid rows against each opponent, at least three valid rows in each
Kestrel slot across the cohort, at least three distinct maps represented on
each opponent edge, and complete independent manifest/replay review. The
fixed 16-row denominator and all failures are reported. Valid rows enter the
rating likelihood only after their exact final-manifest hashes are allowlisted.
No invalid or skipped row enters the likelihood.

`INCONCLUSIVE` applies if any minimum or evidence requirement fails. There is
no strength-based rejection threshold because this experiment estimates the
frozen canonical build rather than selecting a new policy. No result from this
cohort promotes another Kestrel build.

If adopted, append a new current cohort to `config/local-ratings.json`, retain
the unchanged Gaussian-prior Bradley-Terry MAP with 400 Elo prior SD and 200/
800 sensitivity, and report Kestrel relative to ZZZKBot's arbitrary 1000
coordinate. Report the combined v1+v3 estimate, approximate 95% Laplace
interval, direct records, maps, slots, attrition, and prior sensitivity. The
model does not fit map, slot, matchup, or repeated-game correlation effects.
