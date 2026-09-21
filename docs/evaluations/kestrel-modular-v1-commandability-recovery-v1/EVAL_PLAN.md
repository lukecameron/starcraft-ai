# Kestrel Modular v1 gather-commandability recovery — NOT RUN

Registered 21 September 2026 before gameplay. The first modular lifecycle
smoke was an infrastructure-valid rejection because 10 of 32 gather commands
returned BWAPI `Unit_Busy`. This recovery changes only worker assignment
command hygiene and its telemetry: carrying workers finish returning cargo,
and every new resource assignment must pass public BWAPI
`canGather(target)` immediately before issue. The composed architecture,
opening policy, build order, combat policy, and canonical Kestrel v13 remain
unchanged.

## Frozen identities

- Kestrel Modular v1 gather recovery, **Ours / Original**, author Luke
  Cameron: module SHA-256
  `8758914724960797e48c30c5e73885571c08e8a96fd432e7ee8b0b62d7e70e36`;
  sorted source-manifest SHA-256
  `16d857585753b2379800880e818d0a19c60f2230041db8c477da817afcf0013f`;
  build sidecar SHA-256
  `58c3a81b957d222f63c2a566c8d88f4d489f687c58a2e05fa4967fb527a0709b`.
- ZZZKBot Zerg, **Ours / Port**, original author Chris Coxe: module SHA-256
  `ce796a5d49d78121aaf42b57ba758423ee89f74a249b42180cbc0b0cb9df4748`;
  source revision `7183e37b6b416ea53c1040c83e639a3a3c395eed`; source
  <https://github.com/chriscoxe/ZZZKBot>.
- Terminal-drain OpenBW engine SHA-256
  `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`;
  launcher SHA-256
  `af1682393f9fe43afe885b35a1637e9c464719ef93c83e799d614beed20316c1`;
  LF3, macOS ARM64, fresh empty isolated learning state, no adjudication.

## Fixed row and stop rule

Run exactly one game on Benzene, seed 12401, with the recovery candidate as
player 1 and ZZZKBot as player 2. Use a 120-second wall cap and concurrency
one. Do not retry, reseed, replace, or rerun the row for any result. Preserve
the manifest, diagnostics, logs, and both replay copies when produced. No
build, profiler, replay playback, or other engine experiment may overlap the
row.

## Integrity and recovery gates

A valid engine row requires both child exits zero; reciprocal terminal
callbacks with one verified winner; both archived replay copies matching
their source hashes; full `screp` parsing with the expected races; and
`replay_header_frames + 1 == owning_callback_frame`. Only the registered
terminal-drain kill events are allowed. A timeout, crash, sync error, missing
or contradictory result, replay failure, or identity drift is
infrastructure-invalid.

The final candidate diagnostic must pass both
`scripts/score_kestrel_modular_v1.py` and
`scripts/score_kestrel_modular_recovery.py`. It must report zero actual
command rejections, positive accepted gather assignments, and exact
reconciliation between accepted gather assignments and the gather command
category. Preflight skips and cargo deferrals are permitted and must be
nonnegative because they are avoided invalid attempts, not issued commands.
The four-Probe Pylon, reserve, second-Zealot, construction lifecycle, and
command-category semantic gates from the first smoke remain required.

## Decision

- **PASS TO FIVE-GAME SCREEN** only if the engine row and every integrity,
  modular-semantic, and recovery gate pass. The outcome may be a win or loss.
- **REJECT** if the row is valid and exposes any actual rejected command,
  unreconciled worker accounting, malformed trace, public-observation
  violation, or retained-system regression.
- **INCONCLUSIVE** if infrastructure prevents a valid row or a registered
  mechanism remains unexercised without contradicting the implementation.

No outcome changes canonical Kestrel v13 or enters local Elo. This experiment
tests commandability recovery only. A five-opponent strength screen requires
its own frozen plan and a passing result here.
