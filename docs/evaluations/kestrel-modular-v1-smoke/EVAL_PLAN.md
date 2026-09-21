# Kestrel Modular v1 lifecycle smoke — NOT RUN

Registered 21 September 2026 before gameplay. This one-game smoke asks whether
the first tracked modular successor can execute its composed systems through a
real native OpenBW lifecycle and emit semantically coherent telemetry. It is a
commandability and observability gate, not an Elo, promotion, or comparative
strength experiment.

## Frozen identities

- Kestrel Modular v1 Protoss, **Ours / Original**, author Luke Cameron: module
  SHA-256 `8134235c5ce2c589e5b6c890008cc9a2a086df7a715ddcdacfeef4aa5bd36cca`;
  sorted source-manifest SHA-256
  `4f848a72d4086badc400ce1ec2be61d4663f2cf1823577c40de1b436fab94f67`;
  build sidecar SHA-256
  `37366a664cbc030fb776968b655cd3ee06c62de068d5ad5f94e66e18cb51ccb3`.
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

Run exactly one game on Benzene, seed 12400, with Kestrel Modular v1 as player
1 and ZZZKBot as player 2. Use a 120-second wall cap and concurrency one. Do
not retry, reseed, replace, or rerun the row for any result. Preserve the
manifest, diagnostic, logs, and both replay copies when produced. No build,
profiler, replay playback, or other engine experiment may overlap the row.

## Integrity and semantic gates

A valid engine row requires both child exits zero; reciprocal terminal
callbacks with one verified winner; both archived replay copies matching their
source hashes; full `screp` parsing with the expected races; and
`replay_header_frames + 1 == owning_callback_frame`. Only the registered
terminal-drain kill events are allowed. A timeout, crash, sync error, missing
or contradictory result, replay failure, or identity drift is
infrastructure-invalid.

The final candidate diagnostic must have schema `kestrel-modular-v1`, `ended`
true, positive callback and command counts, zero rejected commands, and pass
`scripts/score_kestrel_modular_v1.py`. The scorecard requires:

- the known-Zerg first Pylon command accepted with exactly four completed
  Probes, no accepted Probe train at or before that boundary, and ordered
  Pylon completion;
- reserve samples tied to an eligible idle Nexus, at least one genuine reserve
  block, and same-callback order-aware second-Zealot flags;
- ordered Probe and Zealot acceptance/completion frames;
- construction acceptance/current/completion events with valid ordering; and
- nonnegative command-category totals that reconcile with aggregate totals.

## Decision

- **PASS TO FIVE-GAME SCREEN** only if the engine row and every semantic gate
  pass. The outcome may be a win or loss.
- **REJECT** if the row is valid and exposes a command rejection, malformed or
  contradictory trace, public-observation violation, or implemented-system
  regression.
- **INCONCLUSIVE** if infrastructure prevents a valid row or a registered
  mechanism remains unexercised without contradicting the implementation.

No outcome changes canonical Kestrel v13 or enters local Elo. If this smoke
passes, register the five-opponent screen separately before launching it.
