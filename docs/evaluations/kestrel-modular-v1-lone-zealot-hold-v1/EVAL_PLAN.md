# Kestrel Modular v1 lone-Zealot hold — NOT RUN

Registered 21 September 2026 before gameplay. The valid builder recovery row
accepted every build, gather, train, and combat command, but the first
completed Zealot engaged visible home pressure before the second defender was
observed complete. Two completed Zealots never coexisted. The earlier matched
v19 experiment reached two local completed Zealots before first loss on both
tested maps when it suppressed the lone first Zealot's target attacks, though
that candidate failed separate production gates. This experiment ports only
that public-state hold into `SquadController` and adds explanatory telemetry.
Worker allocation, builder selection, construction, production, scouting,
resource reserves, and post-release targeting remain unchanged.

## Frozen identities

- Kestrel Modular v1 lone-Zealot hold, **Ours / Original**, author Luke
  Cameron: module SHA-256
  `b387872d7ec3e9cd5a96041992699699e5606c0c0f9be67ad85cfdfcb769e81a`;
  sorted source-manifest SHA-256
  `bf88a5ca1dd21f93635fd2258bc0ac02e54f7ca61099c0ad25b9b65d0b4edd9e`;
  build sidecar SHA-256
  `ec080508fbcb1d79d2729684879fc7e66fc8780f51bbbfdc2d61b55eb5b8c3b7`.
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

Run exactly one game on Heartbreak Ridge, seed 12403, with ZZZKBot as player 1
and the candidate as player 2. Use a 120-second wall cap and concurrency one.
Do not retry, reseed, replace, or rerun the row for any result. Preserve the
manifest, diagnostics, logs, and both replay copies. No build, profiler,
replay playback, or other engine experiment may overlap the row.

## Integrity and mechanism gates

A valid engine row requires both child exits zero; reciprocal terminal
callbacks with one verified winner; both archived replay copies matching
their source hashes; complete `screp` parsing with the expected races; and
`replay_header_frames + 1 == owning_callback_frame`. Only the registered
terminal-drain kill events are allowed. A timeout, crash, sync error, missing
or contradictory result, replay failure, or identity drift is
infrastructure-invalid.

The final candidate diagnostic must pass
`scripts/score_kestrel_modular_v1.py`,
`scripts/score_kestrel_modular_recovery.py`, and
`scripts/score_kestrel_modular_hold.py`. It must retain zero actual command
rejections, positive accepted gather and build commands, exact gather and
construction reconciliation, the four-Probe Pylon, both reserves, and ordered
construction lifecycle evidence.

The known-Zerg hold must record positive active and suppression samples and at
least one unique completed Zealot. Two completed Zealots must coexist, and the
hold release frame must equal the public self-state second-Zealot completion
frame. Accepted home moves may be zero when the held unit is already home, but
may never exceed attempts. In the owner-filtered replay command stream there
must be no candidate `Attack1` or `AttackMove` order before replay frame
`hold_release_frame + 2`; ordinary `Move` orders toward home are allowed. This
replay check is evaluator-only and never enters gameplay.

## Decision

- **PASS TO FIVE-GAME SCREEN** only if the engine row and every integrity,
  modular, commandability, retained-opening, and hold gate pass. The outcome
  may be a win or loss.
- **REJECT** if the row is valid and exposes any actual rejected command,
  retained-system regression, missing two-Zealot overlap, pre-release attack,
  malformed trace, or public-observation violation.
- **INCONCLUSIVE** if infrastructure prevents a valid row or the lone-Zealot
  hold is never exercised without contradicting the implementation.

No outcome changes canonical Kestrel v13 or enters local Elo. This is one
diagnostic Apple Silicon OpenBW mechanism row. A five-opponent strength screen
requires its own frozen plan and a passing result here.
