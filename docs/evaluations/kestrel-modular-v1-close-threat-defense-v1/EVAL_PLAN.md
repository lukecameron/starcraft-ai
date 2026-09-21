# Kestrel Modular v1 close-threat defense — NOT RUN

Registered 21 September 2026 before gameplay. The valid passive-hold row
accepted two retreat moves and issued no attack orders, but its first held
Zealot disappeared before the second completed. A later isolated base-center
anchor row was infrastructure-inconclusive before frame zero and is not
retried or replaced. This materially distinct candidate retains the
base-center retreat and adds one rule: during the known-Zerg lone-Zealot hold,
attack the nearest visible, detected, ground-compatible enemy within 256
pixels of the public base-center anchor; otherwise retreat to that anchor.
Production, workers, builders, reserves, scouting, threat radius outside this
hold, and post-release behavior are unchanged.

## Frozen identities

- Kestrel Modular v1 close-threat defense, **Ours / Original**, author Luke
  Cameron: module SHA-256
  `dbd9b204cb65da112e4d1994f6b6bd15fbd12be97db2bb2b7b64a4a82ee11bdf`;
  sorted source-manifest SHA-256
  `1456d91bf1f3529a246a7dd0d87fdeacaaf2d72a49e2029c2396d778a96f29d3`;
  build sidecar SHA-256
  `b820ae777131b5ec4048c0bd414a1242ab2e04d9d676b3298e77e9d6d2d4cce6`.
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

Run exactly one game on Heartbreak Ridge, seed 12405, with ZZZKBot as player 1
and the candidate as player 2. This uses the valid predecessor's candidate
slot for mechanism comparison and a fresh scenario seed. Use a 120-second wall
cap and concurrency one. Do not retry, reseed, replace, or rerun the row for
any result. Preserve all manifests, diagnostics, logs, and replay copies. No
build, profiler, replay playback, or other engine experiment may overlap it.
The runner must pass its exact AF_UNIX transport preflight in an execution
context that permits local sockets before either child starts.

## Integrity and retained-system gates

A valid engine row requires both child exits zero; reciprocal terminal
callbacks with one verified winner; both archived replay copies matching
their source hashes; complete `screp` parsing with expected races; and
`replay_header_frames + 1 == owning_callback_frame`. Only the registered
terminal-drain kill events are allowed. A timeout, crash, sync error, transport
preflight failure, missing or contradictory result, replay failure, or
identity drift is infrastructure-invalid. Candidate, opponent, engine,
launcher, map, game data, slot, seed, and learning-state identities must match
the schedule.

The final candidate diagnostic must pass
`scripts/score_kestrel_modular_v1.py`,
`scripts/score_kestrel_modular_recovery.py`, and
`scripts/score_kestrel_modular_hold.py`. It must retain zero actual command
rejections and zero `Unit_Busy` errors; positive accepted gather, build, and
train activity; exact gather and construction reconciliation; the four-Probe
Pylon; both mineral reserves; ordered construction lifecycle; and the
second-Zealot train/completion telemetry. No wrong-race production or
public-information violation is allowed.

## Defensive mechanism gates

The known-Zerg hold must record positive active and suppression samples, at
least one unique held Zealot, at least one close-threat sample, and at least
one actually issued and accepted defensive attack. The recorded close-threat
radius must equal 256. Samples, actual issue attempts, accepted/rejected
outcomes, events, arrays, positions, unit IDs, target IDs, and per-held-unit
lifecycle counters must reconcile. Coalesced repeated requests count as
samples but not actual issue attempts. Because the aggregate attack category
may also contain post-release squad orders, close-threat issued attempts,
rejections, and acceptances must each be no greater than the corresponding
total issued, rejected, and accepted attack commands; equality is not
required.

Every accepted retreat target must equal the recorded base-center anchor and
none may equal the old start-tile top-left. Public self-state must observe two
completed Zealots simultaneously, and the hold release frame must equal the
second completion frame. Owner-filtered replay commands may contain no
pre-release `AttackMove`. At LF3, every pre-release held-Zealot `Attack1` must
match an actually issued accepted close-threat event at replay frame
`event_frame + 2`, with the same held-unit and target identity when those
fields are exposed by the public command stream. When identity is unavailable,
the frame-and-order match remains mandatory and the identity sub-gate is
recorded as unsupported. Any pre-release held-Zealot `Move` must target the
registered anchor. Unrelated scout moves are exempt. Replay checks remain
evaluator-only.

## Decision

- **PASS TO FIVE-GAME SCREEN** only if the row is valid and every integrity,
  retained-system, commandability, anchor, close-threat, overlap, release,
  telemetry, and replay gate passes. The outcome may be a win or loss.
- **REJECT** if the row is valid but any gate fails, including an old-anchor
  target, rejected command, missing actual defensive attack, unrelated
  pre-release attack, missing two-Zealot overlap, or malformed telemetry.
- **INCONCLUSIVE** only if infrastructure prevents a valid row or no
  close-threat opportunity occurs. Preserve the row without replacement. A
  valid exercised loss is not inconclusive.

No outcome changes canonical Kestrel v13 or enters local Elo. This is one
diagnostic Apple Silicon OpenBW mechanism row. It does not claim BASIL or
tournament strength and does not verify official Win32 runtime behavior. A
five-opponent strength screen requires its own frozen plan and a passing
result here.
