# Kestrel Modular v1 lone-Zealot leash — NOT RUN

Registered 21 September 2026 before gameplay. The valid close-threat row
issued 15 accepted defensive attacks but its first held Zealot disappeared
123 frames before the second held Zealot appeared. Its last recorded position
was 157 pixels from the public base-center anchor. This does not prove why the
unit disappeared, but it is the strongest public-state signal from that row.
This materially distinct candidate retains the close-threat rule and adds one
rule before threat selection: while the known-Zerg lone-Zealot hold is active,
a held Zealot more than 96 pixels from the base-center anchor must move back to
the anchor and may not attack in that callback. Production, workers, builders,
reserves, construction, scouting, the 256-pixel close-threat radius, and
post-release behavior are unchanged.

## Frozen identities

- Kestrel Modular v1 lone-Zealot leash, **Ours / Original**, author Luke
  Cameron: module SHA-256
  `1734fcfa4542eff24c7341f43b226cb6eb03d4fd68a120beb1a0f406160f7818`;
  sorted source-manifest SHA-256
  `112b0f545b3b8b871cb86d166ec33c12fcd0583820d6fd5ebbd956d191875ccf`;
  build sidecar SHA-256
  `7cab62ed82405a5bb413c28c85d5ab0b272b44cadc4fddc3353ef7f05e8bbd7a`.
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

Run exactly one game on Heartbreak Ridge, seed 12406, with ZZZKBot as player 1
and the candidate as player 2. This preserves the valid predecessor's slot for
mechanism comparison and uses a fresh scenario seed. Use a 120-second wall cap
and concurrency one. Do not retry, reseed, replace, or rerun the row for any
result. Preserve all manifests, diagnostics, logs, and replay copies. No build,
profiler, replay playback, or other engine experiment may overlap it. The
runner must pass its exact AF_UNIX transport preflight in an execution context
that permits local sockets before either child starts.

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
`scripts/score_kestrel_modular_recovery.py`, and
`scripts/score_kestrel_modular_hold.py`. It must retain zero actual command
rejections and zero `Unit_Busy` errors; positive accepted gather, build, and
train activity; exact gather and construction reconciliation; the four-Probe
Pylon; both mineral reserves; ordered construction lifecycle; and the
second-Zealot train/completion telemetry. No wrong-race production or
public-information violation is allowed.

## Leash and defensive mechanism gates

The known-Zerg hold must record positive active and suppression samples, at
least one unique held Zealot, a leash radius exactly equal to 96, at least one
leash-block sample, at least one actually issued and accepted leash move, at
least one close-threat sample, and at least one actually issued and accepted
defensive attack. The close-threat radius must equal 256. Samples, actual issue
attempts, accepted/rejected outcomes, coalesced requests, events, arrays,
positions, unit IDs, target IDs, maximum anchor distance, and per-held-unit
lifecycle counters must reconcile. Coalesced requests count as leash-block or
close-threat samples but not actual command attempts.

Every accepted leash move and retreat move attributable to the held Zealot
must target the recorded base-center anchor; none may target the old start-tile
top-left. Every actually issued close-threat attack must originate at or within
96 pixels of that anchor. Public self-state must observe two completed Zealots
simultaneously, and the hold release frame must equal the second completion
frame. Owner-filtered replay commands may contain no pre-release `AttackMove`.
At LF3, every pre-release held-Zealot `Attack1` must match an actually issued
accepted close-threat event at replay frame `event_frame + 2`, with the same
held-unit and target identity when those fields are exposed by the public
command stream. When identity is unavailable, the frame-and-order match remains
mandatory and the identity sub-gate is recorded as unsupported. Every
pre-release held-Zealot `Move` must target the registered anchor. Unrelated
scout moves are exempt. Replay checks remain evaluator-only.

## Decision

- **PASS TO FIVE-GAME SCREEN** only if the row is valid and every integrity,
  retained-system, commandability, anchor, leash, close-threat, overlap,
  release, telemetry, and replay gate passes. The outcome may be a win or loss.
- **REJECT** if the row is valid but any gate fails, including an old-anchor
  target, rejected command, missing actual leash move, missing actual defensive
  attack, off-leash pre-release attack, unrelated pre-release attack, missing
  two-Zealot overlap, or malformed telemetry.
- **INCONCLUSIVE** only if infrastructure prevents a valid row or neither a
  leash block nor close-threat opportunity occurs. Preserve the row without
  replacement. A valid exercised loss is not inconclusive.

No outcome changes canonical Kestrel v13 or enters local Elo. This is one
diagnostic Apple Silicon OpenBW mechanism row. It does not claim BASIL or
tournament strength and does not verify official Win32 runtime behavior. A
five-opponent strength screen requires its own frozen plan and a passing result
here.
