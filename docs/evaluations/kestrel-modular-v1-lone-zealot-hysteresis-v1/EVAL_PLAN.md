# Kestrel Modular v1 lone-Zealot leash hysteresis — NOT RUN

Registered 21 September 2026 before gameplay. The valid close-threat row
recorded 15 accepted defensive attacks, but its first held Zealot moved 157
pixels from the public base-center anchor and disappeared 123 frames before
the second held unit appeared. The subsequent fixed 96-pixel leash row was
infrastructure-inconclusive before child launch and is not retried or
replaced. This materially distinct candidate adds persistent per-unit return
state: a held Zealot that exceeds 96 pixels from the base-center anchor must
keep returning, with threat selection suppressed, until it reaches a 48-pixel
release radius. Production, workers, builders, reserves, construction,
scouting, the 256-pixel close-threat radius, and post-hold behavior are
unchanged.

## Frozen identities

- Candidate source commit:
  `6babb1fa9cc36b3e2091efb68403c63443eec0fe`.
- Kestrel Modular v1 leash hysteresis, **Ours / Original**, author Luke
  Cameron: module SHA-256
  `c1b45a4d70bfb8d52c0fe981e849bbbad63b3fb1f9db649f25fb928f03d2a2fd`;
  sorted source-manifest SHA-256
  `f42c18ca88cd4b1ffac83b5977ceb0e8605c4f6030e1770aa96e094eb36e67da`;
  build sidecar SHA-256
  `1672f749ba1bbcd9b8ddcb2e010de563ad96e4f6555eab6563040daf1483249e`.
- ZZZKBot Zerg, **Ours / Port**, original author Chris Coxe: module SHA-256
  `ce796a5d49d78121aaf42b57ba758423ee89f74a249b42180cbc0b0cb9df4748`;
  source revision `7183e37b6b416ea53c1040c83e639a3a3c395eed`; source
  <https://github.com/chriscoxe/ZZZKBot>.
- Terminal-drain OpenBW engine SHA-256
  `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`;
  launcher SHA-256
  `af1682393f9fe43afe885b35a1637e9c464719ef93c83e799d614beed20316c1`;
  LF3, macOS ARM64, fresh empty isolated learning state, no adjudication.

The candidate build sidecar contains the complete sorted source-file list and
source-manifest hash. The frozen binary and sidecar are local immutable build
artifacts. The schedule must also freeze this plan, every evaluator, the bot
identity registry, engine, launcher, map, and game-data hash before gameplay.

## Fixed row and stop rule

Run exactly one game on Heartbreak Ridge, seed 12407, with ZZZKBot as player 1
and the candidate as player 2. This preserves the valid predecessor's slot for
mechanism comparison and uses a fresh scenario seed. Use a 120-second wall cap
and concurrency one. Do not retry, reseed, replace, or rerun the row for any
result. Preserve all manifests, diagnostics, logs, and replay copies. No build,
profiler, replay playback, audit, or other engine experiment may overlap it.
The runner must pass its exact AF_UNIX transport preflight in an execution
context that permits local sockets before either child starts.

## Integrity and retained-system gates

A valid engine row requires both child exits zero; reciprocal terminal
callbacks with one verified winner; both archived replay copies matching their
source hashes; complete `screp` parsing with expected races; and
`replay_header_frames + 1 == owning_callback_frame`. Only the registered
terminal-drain kill events are allowed. A timeout, crash, sync error, transport
preflight failure, missing or contradictory result, replay failure, or identity
drift is infrastructure-invalid. Candidate, opponent, engine, launcher, map,
game data, slot, seed, and learning-state identities must match the schedule.

The final candidate diagnostic must pass
`scripts/score_kestrel_modular_v1.py`,
`scripts/score_kestrel_modular_recovery.py`,
`scripts/score_kestrel_modular_hold.py`, and the candidate-specific
`scripts/score_kestrel_modular_leash_hysteresis.py`. It must retain zero actual
command rejections and zero `Unit_Busy` errors; positive accepted gather,
build, and train activity; exact gather and construction reconciliation; the
four-Probe Pylon; both mineral reserves; ordered construction lifecycle; and
the second-Zealot train/completion telemetry. No wrong-race production or
public-information violation is allowed.

## Hysteresis mechanism gates

The known-Zerg hold must record positive active and suppression samples and at
least one unique held Zealot. The entry and release radii must equal 96 and 48.
There must be at least one return-state entry, positive return-active samples,
at least one actually issued accepted return move, and at least one release
from return state. Return-state and leash samples, actual issue attempts,
accepted/rejected outcomes, coalesced requests, aggregate counters, and
per-held-unit lifecycle counters must reconcile. Coalesced requests are state
samples but are not actual command attempts.

There must also be at least one visible, detected, ground-compatible
close-threat sample and at least one actually issued accepted defensive
attack. The threat radius must equal 256. Every recorded attack origin must be
at or within 96 pixels of the base-center anchor. Samples, attempts, outcomes,
events, arrays, positions, unit IDs, target IDs, maximum anchor distance, and
per-unit lifecycles must reconcile. Public self-state must observe two
completed Zealots simultaneously, and the hold release frame must equal the
second completion frame.

## Durable replay audit

The decision also requires a machine-readable audit produced by
`scripts/audit_kestrel_modular_replay.py` from the frozen match manifest,
candidate diagnostic, and `screp`. The audit must verify terminal integrity,
both replay copies, expected races, header/callback frame equality, and allowed
kill events. In the candidate owner-filtered command stream, it must find no
pre-release `AttackMove`; every accepted close-threat event must have exactly
one `Attack1` at `event_frame + 2` with matching target coordinates where
exposed; and held-unit `Move` commands must target the registered anchor. If
`screp` cannot prove the BWAPI-unit-ID mapping, the identity subcheck is
recorded as unsupported, while frame, order, ownership, and coordinates remain
mandatory. The audit JSON and its SHA-256 are preserved with the result.

## Decision

- **PASS TO FIVE-GAME SCREEN** only if the row is valid and every integrity,
  retained-system, commandability, anchor, hysteresis, close-threat, overlap,
  release, telemetry, and replay gate passes. The outcome may be a win or loss.
- **REJECT** if the row is valid but any gate fails, including absent return
  activity, missing actual return move or defensive attack, off-leash attack,
  old-anchor target, rejected command, missing two-Zealot overlap, or malformed
  telemetry/replay evidence.
- **INCONCLUSIVE** only if infrastructure prevents a valid row. Preserve the
  row without replacement. A valid exercised loss is not inconclusive.

No outcome changes canonical Kestrel v13 or enters local Elo. This is one
diagnostic Apple Silicon OpenBW mechanism row. It does not claim BASIL or
tournament strength and does not verify official Win32 runtime behavior. A
five-opponent strength screen requires its own frozen plan and a passing
result here.
