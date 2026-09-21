# Kestrel Modular v1 second-Gateway safety — NOT RUN

Registered 21 September 2026 before gameplay. This is a one-row native
OpenBW mechanism experiment for commit `f87ef1f`. The candidate keeps the
working modular opening, 96/48-pixel return hysteresis, and 160-pixel
close-threat anchor, and adds one public-self-state gate: against known Zerg,
the second Gateway request is unavailable until the bot has observed two
completed Zealots. The completion observation is latched; a later unit loss
does not retroactively permit an earlier request.

The registered hypothesis is: **deferring the known-Zerg second Gateway until
the second completed Zealot prevents premature Gateway spending while keeping
the two-Zealot overlap and close-threat defense exercised.** The mechanism
prediction is a second-Gateway acceptance frame at or after
`second_zealot_completed_frame`, or no second-Gateway acceptance before the
120-second row ends. The latter is a censored observation and is acceptable;
it is not evidence that a later Gateway would never be requested.

## Frozen identities

- Candidate source commit: `f87ef1f93263712ce3121cb2ba6d71a5dcca121f`.
- Candidate, **Ours / Original**, author Luke Cameron: module SHA-256
  `c81f65b17c047087abc3e8a019028d4a3fde3f3db8361d7d026f986d20c88c31`;
  sorted source-manifest SHA-256
  `a8d14242e8af8964b0875eab3f3d216bf55f102a0a55be73453e6a88db972c86`;
  build-sidecar SHA-256
  `28d983ad5583efa64db24fea1c60567430e208b71c4388c58cd3eedf6720d9e1`.
- ZZZKBot Zerg, **Ours / Port**, original author Chris Coxe: module SHA-256
  `ce796a5d49d78121aaf42b57ba758423ee89f74a249b42180cbc0b0cb9df4748`;
  source revision `7183e37b6b416ea53c1040c83e639a3a3c395eed`; source
  <https://github.com/chriscoxe/ZZZKBot>.
- Terminal-drain OpenBW engine SHA-256
  `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`;
  launcher SHA-256
  `af1682393f9fe43afe885b35a1637e9c464719ef93c83e799d614beed20316c1`;
  launcher sidecar SHA-256
  `0beebdd3bb6221a5e6143c015763d14fa20330a8976ede3f997062660b3e7390`.
  Runtime is LF3, macOS ARM64, fresh empty isolated learning state, with no
  adjudication.

The schedule freezes the candidate-specific scorer, replay auditor, bot
registry, engine, launcher, map, game data, binary, sidecar and source
manifest before gameplay. No engine match or preflight is part of
preregistration.

## Fixed row and stop rule

Run exactly one game on Heartbreak Ridge, seed `12409`, with ZZZKBot as player
1 and Kestrel Modular v1 as player 2. This keeps the predecessor's map and
slot while using a fresh scenario seed. Use a 120-second wall cap and
concurrency one. Do not retry, reseed, replace or rerun the row for any
outcome. Preserve every manifest, diagnostic, log, scorecard, audit and
replay copy. No build, profiler, replay playback, audit or other engine
experiment may overlap it. The runner must pass its exact AF_UNIX transport
preflight outside the restricted execution context before child startup.

## Required mechanism gates

A valid row requires both child exits zero; reciprocal terminal callbacks with
one winner; source/archive replay hash equality; full `screp` parsing with the
expected races; and `replay_header_frames + 1 == owning_callback_frame`.
Only the registered terminal-drain kill events are allowed. A timeout, crash,
sync error, transport failure, missing or contradictory result, replay failure
or identity drift is infrastructure-invalid. Candidate, opponent, engine,
launcher, map, game data, slot, seed and learning state must match the
schedule.

The candidate diagnostic must pass the generic modular score, recovery score,
hold score and leash-hysteresis score, plus
`scripts/score_kestrel_modular_second_gateway_safety.py`. It must retain zero
command rejections and `Unit_Busy` errors; positive accepted gather, build,
train, return-move and defensive-attack activity; exact telemetry
reconciliation; the four-Probe Pylon; both mineral reserves; ordered opening
construction; and second-Zealot train/completion telemetry. No wrong-race
production or public-information violation is allowed.

The second-Gateway scorer requires known-Zerg evidence, a nonnegative
`second_zealot_completed_frame`, and two accepted Zealot trains. If
`second_gateway_accepted_frame >= 0`, it must be greater than or equal to
`second_zealot_completed_frame`; an absent second-Gateway acceptance is a
passing censored observation through the fixed row's end. The scorer also
requires a two-Zealot overlap (`max_zealots >= 2`) and a hold release exactly
at second completion.

The close-threat mechanism must use radius 160, have positive eligible
samples and accepted attacks, and keep every attack origin within the 96-pixel
leash. Durable replay evidence must match every accepted close-threat event to
exactly one `Attack1` at event frame + 2, with matching target coordinates;
held-unit movement must target the base-center anchor. The replay audit may
mark unit identity unsupported only when the stream provides no reliable
mapping; ownership, frame, order and position remain mandatory.

## Decision and scope

- **PASS TO FIVE-GAME SCREEN** only if every integrity, retained-system,
  commandability, 160-pixel close-threat, hysteresis, two-Zealot overlap,
  release, second-Gateway safety and replay gate passes. The result may be a
  win or loss.
- **REJECT** if the row is valid but any gate fails, including an accepted
  second Gateway before second completion, absent required mechanism activity,
  off-leash attack, rejected command or malformed telemetry/replay evidence.
- **INCONCLUSIVE** only if infrastructure prevents a valid row. Preserve it
  without replacement. A valid exercised loss is not inconclusive.

This row is Elo-ineligible and does not change canonical Kestrel v13. A
five-opponent strength screen requires its own preregistered schedule and is
allowed only after this row passes.
