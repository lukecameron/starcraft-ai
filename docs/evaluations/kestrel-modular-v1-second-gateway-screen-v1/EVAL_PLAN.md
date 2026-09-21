# Kestrel Modular v1 second-Gateway safety — five-game mixed screen

Registered 21 September 2026 at 04:58 UTC, after the exact mechanism row
`kestrel-modular-v1-second-gateway-safety-v1` passed all of its frozen gates.
This is a fresh, five-game native OpenBW strength screen for the same immutable
Kestrel Modular v1 build. It tests whether the modular opening can produce
credible short-game outcomes across the existing local opponent gradient after
the known-Zerg second-Gateway safety change. It is a quick local screen, not a
tournament claim or a replacement for held-out validation.

## Hypothesis and decision scope

The hypothesis is: **the second-Gateway safety candidate will retain the
validated opening mechanisms while producing at least one clean win across a
mixed five-opponent screen without introducing command or replay-integrity
failures.** The screen is intended to expose the next matchup-specific
weaknesses as well as record wins and losses.

The primary strength observations are verified candidate wins and losses by
exact opponent, map, slot and seed. Secondary quantitative observations are
terminal callback frames, durable logical frames per wall second, candidate
command totals and rejected-command rate, accepted construction and training
milestones, maximum observed combat-unit count, and candidate callback CPU and
memory measurements when the runner records them. Qualitative replay review
will record the first visible threat, first candidate combat response, whether
the second-Zealot overlap and hold release were exercised, whether the
second-Gateway safety gate was exercised or censored, and the terminal cause.
The replay auditor remains the authority for durable ownership, order, frame and
target-position evidence; diagnostic scorecards remain descriptive for this
mixed-opponent screen.

The five rows are independent observations for scheduling purposes but are too
few to support a precise absolute rating. Report a nominal overall Wilson 95%
win interval and per-opponent one-game outcomes; treat one-game infinite Elo
endpoints as insufficient evidence. Do not pool heterogeneous opponents into a
single claimed Elo. A row may enter the existing exact-build Bradley–Terry
local rating cohort only after review establishes every identity, regime,
scenario and replay-integrity requirement and the lead explicitly updates the
rating configuration. This plan alone does not update Elo or promote the
candidate.

## Frozen identities

- Candidate, **Ours / Original**, author Luke Cameron, source
  <https://github.com/lukecameron/starcraft-ai/tree/main/bots/kestrel-modular-v1>:
  source commit `f87ef1f93263712ce3121cb2ba6d71a5dcca121f`, module SHA-256
  `c81f65b17c047087abc3e8a019028d4a3fde3f3db8361d7d026f986d20c88c31`, sorted
  source manifest SHA-256
  `a8d14242e8af8964b0875eab3f3d216bf55f102a0a55be73453e6a88db972c86`, and
  build-sidecar SHA-256
  `28d983ad5583efa64db24fea1c60567430e208b71c4388c58cd3eedf6720d9e1`.
- ZZZKBot Zerg, **Ours / Port**, original author Chris Coxe, source
  <https://github.com/chriscoxe/ZZZKBot>, module SHA-256
  `ce796a5d49d78121aaf42b57ba758423ee89f74a249b42180cbc0b0cb9df4748` and
  build-sidecar SHA-256
  `41c03e2c266fc012a6df0e1ec1c8c9efd65e24973490ef3d1980c9cf6b36f4f1`.
- UAlbertaBot Terran or Protoss, **Ours / Port**, original author David
  Churchill, source <https://github.com/davechurchill/ualbertabot>, shared
  module SHA-256
  `75ac4f6bb44ed6e48fbee883638c77df9557c9a88070ceca4de11183053238c9` and
  build-sidecar SHA-256
  `2710a35e2dc0f05548a99822a235aee47a0aeadc95d2e8dbf75699da248aeb40`.
- McRave Zerg memo fork, **Ours / Fork**, original author Christian McCrave,
  source <https://github.com/Cmccrave/McRave>, module SHA-256
  `04521befa41bb3873783b215493abf3a071414d2a5315cdea68fc7a67f4415ec` and
  build-sidecar SHA-256
  `86965dce3c68d42c72373afa505bd68502b36eb030ca58b579934bd6fbdb399f`.
  The frozen local binary is the reviewed memo fork used by the current local
  rating regime; it is not treated as the upstream McRave ladder binary.
- Stardust repaired fork, **Ours / Fork**, original author Bruce Mackenzie
  Nielsen, source <https://github.com/bmnielsen/Stardust>, module SHA-256
  `1039975842c6edea71043e0da091ff21ad5311fd3ddbeb568cf89b364f7d28aa` and
  build-sidecar SHA-256
  `1f17ab58bb4d6a51d06e2943a92da4c32ca015b9a9008bcc755c55213b06a38b`.
  This remains local benchmark evidence; no tournament submission or contact
  is authorized.
- Terminal-drain OpenBW engine SHA-256
  `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`,
  launcher SHA-256
  `af1682393f9fe43afe885b35a1637e9c464719ef93c83e799d614beed20316c1`, and
  launcher-sidecar SHA-256
  `0beebdd3bb6221a5e6143c015763d14fa20330a8976ede3f997062660b3e7390`.
  Runtime is LF3 on macOS ARM64 with fresh empty isolated learning state and
  no adjudication.

The schedule freezes the candidate, opponent binaries and sidecars, engine,
launcher, game data, maps, provenance registry, runner, diagnostic tools and
this plan before gameplay. No build, preflight, replay playback or audit is
part of this preregistration. The runner's AF_UNIX transport preflight must be
performed outside the restricted execution context immediately before launch;
it is not a game result and cannot change the schedule.

## Fixed five-game schedule and stop rule

Run exactly the following five games concurrently, one attempt per row, with a
120-second wall cap per game and a 300-second cohort cap. Do not retry, reseed,
replace an opponent, substitute a map, or rerun any row after an outcome. Use
the registered candidate slot and fresh scenario seed in each row:

| Game | Opponent | Map | Candidate slot | Scenario seed |
| ---: | --- | --- | ---: | ---: |
| 1 | ZZZKBot (Zerg) | Benzene | P1 | 12501 |
| 2 | UAlbertaBot-Terran | Destination | P2 | 12502 |
| 3 | UAlbertaBot-Protoss | Heartbreak Ridge | P1 | 12503 |
| 4 | McRave memo fork (Zerg) | Circuit Breaker | P2 | 12504 |
| 5 | Stardust repaired fork (Protoss) | Benzene | P1 | 12505 |

Preserve every run manifest, child log, diagnostic, result, replay copy, replay
hash, full `screp` parse and audit, including infrastructure-invalid rows. A
failure in one row does not authorize replacement. Stop launching only if the
cohort cap is reached or the runner's registered infrastructure stop rule is
met; games already running may finish and must be archived.

## Validity and review gates

A row is **valid and potentially Elo-eligible** only when both children exit
zero; terminal callbacks are reciprocal and identify one winner; source and
archived replay copies have equal hashes and sizes; `screp` parses the complete
replay with the expected candidate and opponent races; and
`replay_header_frames + 1` equals the owning callback frame. Candidate,
opponent, engine, launcher, map, game data, slot, seed and learning state must
match this schedule. Launcher failure, state-hash mismatch, wrong race,
transport failure, timeout, missing result, replay failure or identity drift
is infrastructure-invalid and excluded from wins, losses and Elo.

For valid rows, preserve the candidate's public-observation diagnostics and
run the generic modular score where its required fields are present. Run the
durable replay auditor for every row. On known-Zerg rows, report whether the
second-Gateway safety, two-Zealot overlap, 96/48 hysteresis and 160-pixel
close-threat evidence were exercised; an unobserved mechanism is censored
diagnostic data, not a fabricated pass or failure. Every row must retain its
raw commands and replay evidence even when a qualitative mechanism is not
exercised. Report command rejection counts and categories, with `Unit_Busy`
errors called out separately.

The screen's outcome is descriptive. Record the number of valid wins, losses,
infrastructure-invalid attempts, per-opponent outcomes, nominal Wilson
intervals and the uncertainty limits above. A valid loss is still usable
evidence. No outcome from this five-game screen changes canonical Kestrel v13,
adopts the candidate, or enters the local rating file automatically. The lead
may update the exact-build cohort only after checking the final manifests and
reviewed hashes against the existing local-ratings rules; invalid rows and
diagnostic-only observations must remain excluded.

## Frozen artifact paths

The candidate path is
`artifacts/builds/c81f65b17c047087abc3e8a019028d4a3fde3f3db8361d7d026f986d20c88c31/kestrel-modular-v1-second-gateway-safety/KestrelModular.dylib`.
Opponent, launcher and game-data paths, hashes, and the five rows are frozen
in `schedule.json`. Provenance is read from `config/bot-identities.json`.
