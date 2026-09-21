# Kestrel Modular v1 tight close-threat defense — NOT RUN

Registered 21 September 2026 before gameplay. The valid 96/48-pixel
hysteresis row reduced the disjoint held-unit gap from 123 to 63 frames and
made five accepted anchor moves with zero command rejections, but the first
held Zealot still disappeared before the second appeared. Four accepted
attacks originated within the leash. This fresh, materially distinct candidate
retains the working return-state hysteresis and changes one rule: during the
known-Zerg lone-Zealot hold, visible detected ground-compatible enemies must be
within 160 pixels of the public base-center anchor instead of 256 before the
held unit may attack. Production, workers, builders, reserves, construction,
scouting, leash radii, and post-hold behavior are unchanged.

## Frozen identities

- Candidate source commit:
  `a63a7d5f03e8ba3d922161fc66a3c3933fe4485e`.
- Kestrel Modular v1 tight close-threat defense, **Ours / Original**, author
  Luke Cameron: module SHA-256
  `396f6c66088fc1dadb3ecb1dee7850712bad49dbf683ce14d54c73e7b70bf33b`;
  sorted source-manifest SHA-256
  `428dce70e38365a390801bf30a3bc7a6594548509ee69bf00b091b56cbb3edce`;
  build sidecar SHA-256
  `a450cdc64ff071b91afa82d023ea604e893afd54141bb43fdef22b5d9db60fba`.
- ZZZKBot Zerg, **Ours / Port**, original author Chris Coxe: module SHA-256
  `ce796a5d49d78121aaf42b57ba758423ee89f74a249b42180cbc0b0cb9df4748`;
  source revision `7183e37b6b416ea53c1040c83e639a3a3c395eed`; source
  <https://github.com/chriscoxe/ZZZKBot>.
- Terminal-drain OpenBW engine SHA-256
  `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`;
  launcher SHA-256
  `af1682393f9fe43afe885b35a1637e9c464719ef93c83e799d614beed20316c1`;
  LF3, macOS ARM64, fresh empty isolated learning state, no adjudication.

The schedule must freeze this plan, candidate-specific scorer, replay auditor,
bot registry, engine, launcher, map, game data, binary, sidecar, and source
manifest before gameplay.

## Fixed row and stop rule

Run exactly one game on Heartbreak Ridge, seed 12408, with ZZZKBot as player 1
and the candidate as player 2. This preserves the valid predecessor's slot for
mechanism comparison and uses a fresh scenario seed. Use a 120-second wall cap
and concurrency one. Do not retry, reseed, replace, or rerun the row for any
result. Preserve all manifests, diagnostics, logs, scorecards, audits, and
replay copies. No build, profiler, replay playback, audit, or other engine
experiment may overlap it. The runner must pass its exact AF_UNIX transport
preflight outside the restricted execution context before child startup.

## Integrity and retained-system gates

A valid row requires both child exits zero; reciprocal terminal callbacks with
one winner; source/archive replay hash equality; full `screp` parsing with
expected races; and `replay_header_frames + 1 == owning_callback_frame`. Only
the registered terminal-drain kill events are allowed. A timeout, crash, sync
error, transport failure, missing/contradictory result, replay failure, or
identity drift is infrastructure-invalid. Candidate, opponent, engine,
launcher, map, game data, slot, seed, and learning state must match schedule.

The candidate diagnostic must pass
`scripts/score_kestrel_modular_v1.py`,
`scripts/score_kestrel_modular_recovery.py`,
`scripts/score_kestrel_modular_hold.py`, and
`scripts/score_kestrel_modular_leash_hysteresis.py`. It must retain zero
command rejections and `Unit_Busy` errors; positive accepted gather, build,
train, return-move, and defensive-attack activity; exact reconciliation; the
four-Probe Pylon; both mineral reserves; ordered construction; and the
second-Zealot train/completion telemetry. No wrong-race production or
public-information violation is allowed.

## Defensive mechanism gates

The known-Zerg hold must record positive active and suppression samples and at
least one held Zealot. Hysteresis entry/release radii must equal 96/48 pixels,
with positive return entries, active samples, one actually issued accepted
return move, and one return release. Return/leash samples, attempts, outcomes,
coalescing, aggregate counters, and per-unit lifecycles must reconcile.

The close-threat anchor radius must equal 160 pixels. There must be at least
one eligible threat sample and one actually issued accepted defensive attack.
Every attack origin must be within the 96-pixel leash. Threat samples,
attempts, outcomes, events, arrays, positions, unit IDs, target IDs, maximum
anchor distance, and lifecycles must reconcile. Public self-state must observe
two completed Zealots simultaneously, and hold release must equal second
completion.

## Durable replay audit

`scripts/audit_kestrel_modular_replay.py` must produce a passing durable JSON
audit from the frozen match manifest, candidate diagnostic, and `screp`. It
must verify terminal/replay integrity and expected races. In the candidate
owner stream, there may be no pre-release `AttackMove`; every accepted
close-threat event must have exactly one `Attack1` at `event_frame + 2` with
matching target coordinates; and held-unit `Move` commands must target the
base-center anchor. Replay unit identity may be marked unsupported only when
the stream exposes no reliable mapping; ownership, frame, order, and position
remain mandatory. Preserve the audit and hash with the result.

## Decision

- **PASS TO FIVE-GAME SCREEN** only if every integrity, retained-system,
  commandability, anchor, hysteresis, tight-threat, overlap, release,
  telemetry, and replay gate passes. The result may be a win or loss.
- **REJECT** if the row is valid but any gate fails, including absent
  mechanism activity, off-leash attack, old-anchor target, rejected command,
  missing two-Zealot overlap, or malformed telemetry/replay evidence.
- **INCONCLUSIVE** only if infrastructure prevents a valid row. Preserve it
  without replacement. A valid exercised loss is not inconclusive.

No outcome changes canonical Kestrel v13 or enters local Elo. This is one
diagnostic Apple Silicon OpenBW mechanism row, not BASIL or tournament proof.
A five-opponent strength screen requires its own frozen plan and a pass here.
