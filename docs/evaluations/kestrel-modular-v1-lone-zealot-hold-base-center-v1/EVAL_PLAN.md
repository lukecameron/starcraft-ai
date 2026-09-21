# Kestrel Modular v1 base-center lone-Zealot hold — NOT RUN

Registered 21 September 2026 before gameplay. The preceding lone-Zealot hold
row exercised the intended suppression for 188 samples and accepted two home
moves, but both moves used the start tile's top-left pixel `(3744,1792)`.
Post-game replay inspection showed the Nexus/base center at `(3808,1840)`.
That valid row lost before a second Zealot completed and was rejected. This
candidate changes only the lone-hold retreat destination to the public start
tile-derived base center, `start * 32 + (64,48)`, and records every accepted
hold target. Threat detection, rally, targeting outside the hold, production,
workers, builders, reserves, scouting, and post-release behavior are unchanged.

## Frozen identities

- Kestrel Modular v1 base-center hold, **Ours / Original**, author Luke
  Cameron: module SHA-256
  `4f840d64291cec481fd2a8b8ce09ab9a5e9eb85ea70da159a84c92bba19fcf5a`;
  sorted source-manifest SHA-256
  `ba03c138618c3289d815f91ee84b2d1bde70836c012c06cf58614050b3f9ef52`;
  build sidecar SHA-256
  `47b2a1cd5780f048f4aabf5d467ec4153f50ef4fa76f94b62d99731e07eaf443`.
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

Run exactly one game on Heartbreak Ridge, seed 12404, with the candidate as
player 1 and ZZZKBot as player 2. This is the opposite candidate slot and a
fresh seed relative to the rejected row. Use a 120-second wall cap and
concurrency one. Do not retry, reseed, replace, or rerun the row for any
result. Preserve the manifest, diagnostics, logs, and both replay copies. No
build, profiler, replay playback, or other engine experiment may overlap it.

## Integrity and retained-system gates

A valid engine row requires both child exits zero; reciprocal terminal
callbacks with one verified winner; both archived replay copies matching
their source hashes; complete `screp` parsing with the expected races; and
`replay_header_frames + 1 == owning_callback_frame`. Only the registered
terminal-drain kill events are allowed. A timeout, crash, sync error, missing
or contradictory result, replay failure, or identity drift is
infrastructure-invalid. Candidate, opponent, engine, launcher, map, game data,
slot, seed, and empty learning-state identities must match the schedule.

The final candidate diagnostic must pass
`scripts/score_kestrel_modular_v1.py`,
`scripts/score_kestrel_modular_recovery.py`, and
`scripts/score_kestrel_modular_hold.py`. It must retain zero actual command
rejections and zero `Unit_Busy` errors; positive accepted gather, build, and
train activity; exact gather and construction reconciliation; the four-Probe
Pylon; both mineral reserves; ordered construction lifecycle; and the
second-Zealot train/completion telemetry. No wrong-race production or
public-information violation is allowed.

## Base-center hold gates

The known-Zerg hold must record positive active and suppression samples, at
least one unique held completed Zealot, and at least one accepted hold home
move. Accepted moves may never exceed attempts. The recorded anchor must equal
`(start_tile_x * 32 + 64, start_tile_y * 32 + 48)`. The accepted-target array
length must equal accepted hold moves, and every accepted target must equal
that anchor; none may equal the old start-tile top-left coordinate.

Public self-state must observe two completed Zealots simultaneously. The hold
release frame must equal the public self-state second-Zealot completion frame.
In the owner-filtered replay command stream there must be no candidate
`Attack1` or `AttackMove` order before replay frame `hold_release_frame + 2`.
Pre-release `Move` orders may target only the registered base-center anchor.
Replay checks are evaluator-only and never enter gameplay.

## Decision

- **PASS TO FIVE-GAME SCREEN** only if the row is valid and every integrity,
  retained-system, commandability, anchor, overlap, release, telemetry, and
  replay gate passes. The outcome may be a win or loss.
- **REJECT** if the row is valid but any gate fails, including an old-anchor
  target, rejected command, retained-policy regression, missing two-Zealot
  overlap, missing release equality, malformed telemetry, or pre-release
  attack.
- **INCONCLUSIVE** only if infrastructure prevents a valid row or the
  hold/anchor move opportunity never occurs. Preserve the row; do not replace
  it. A valid exercised loss is not inconclusive.

No outcome changes canonical Kestrel v13 or enters local Elo. This is one
diagnostic Apple Silicon OpenBW mechanism row. It does not claim BASIL or
tournament strength and does not verify official Win32 runtime behavior. A
five-opponent strength screen requires its own frozen plan and a passing
result here.
