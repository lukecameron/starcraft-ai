# Kestrel Modular v1 latency-instrumented five-game screen

Registered 21 September 2026 at 05:20 UTC. This is a fresh, bounded native
OpenBW strength screen for the exact Kestrel Modular v1 gameplay build used by
the recent second-Gateway safety screen. The only candidate change is runtime
latency telemetry (`latency_frames`); gameplay code and policy are unchanged.
The screen is descriptive local evidence and does not by itself promote the
build or update the rating configuration.

## Hypothesis and decision scope

The hypothesis is: **the latency-instrumented Kestrel Modular v1 build can
produce complete, exact-build games with measured callback latency and retain
the prior opening behavior across a small mixed screen.** Adding telemetry
must not introduce command failures, replay-integrity failures, or a material
runtime-regime change.

The primary observations are verified wins and losses by exact opponent, map,
slot and scenario seed. Secondary observations are terminal callback frames,
durable logical frames per wall second, candidate command totals and rejected
commands, opening milestones, combat-unit counts, `latency_frames`, and
qualitative replay notes. These five rows are not enough for a precise absolute
rating and are not pooled into a heterogeneous Elo claim. Report per-opponent
outcomes and a nominal Wilson interval only as a coarse screen summary. A row
may enter the existing exact-build Bradley–Terry cohort only after the lead
reviews every final manifest and explicitly updates the rating configuration.

## Frozen identities and regime

- Candidate: **Kestrel Modular v1**, Protoss, **Ours / Original**, author Luke
  Cameron, source
  <https://github.com/lukecameron/starcraft-ai/tree/main/bots/kestrel-modular-v1>.
  Source commit is `9f02aaea07cfecbd23cbd53a6295fc1dc526e831`; module SHA-256 is
  `eab694b547a16d954708950f944005fa75a73995452130c6927c5effb8f602eb`;
  sorted source-manifest SHA-256 is
  `711f7bbc49466a0e1fe3fd2d389f57da0fffe9e446a15c12296ceb2b0087b627`; and
  build-sidecar SHA-256 is
  `927e7fa9e4b075298e7236be1ce665d854284ad21dc12767cafed2abc85273d9`.
- ZZZKBot: Zerg, **Ours / Port**, original author Chris Coxe, source
  <https://github.com/chriscoxe/ZZZKBot>, module
  `ce796a5d49d78121aaf42b57ba758423ee89f74a249b42180cbc0b0cb9df4748`, sidecar
  `41c03e2c266fc012a6df0e1ec1c8c9efd65e24973490ef3d1980c9cf6b36f4f1`.
- McRave memo fork: Zerg, **Ours / Fork**, original author Christian McCrave,
  source <https://github.com/Cmccrave/McRave>, reviewed local module
  `04521befa41bb3873783b215493abf3a071414d2a5315cdea68fc7a67f4415ec`, sidecar
  `86965dce3c68d42c72373afa505bd68502b36eb030ca58b579934bd6fbdb399f`.
- UAlbertaBot-Protoss: Protoss, **Ours / Port**, original author David
  Churchill, source <https://github.com/davechurchill/ualbertabot>, module
  `75ac4f6bb44ed6e48fbee883638c77df9557c9a88070ceca4de11183053238c9`, sidecar
  `2710a35e2dc0f05548a99822a235aee47a0aeadc95d2e8dbf75699da248aeb40`.
- Engine is the terminal-drain OpenBW build
  `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`, with
  launcher `af1682393f9fe43afe885b35a1637e9c464719ef93c83e799d614beed20316c1`
  and LF3 latency on macOS ARM64. Game data, maps, learning state, engine,
  launcher, runner and provenance registry are frozen in `schedule.json`.

The frozen generic scorer must report integer `latency_frames` and the current
scorecard gates. The current non-Zerg-aware replay auditor remains the authority
for replay ownership, order/frame matching, hashes, parse fidelity, races and
terminal evidence. Zerg policy checks apply only when diagnostic enemy-race
metadata says `known_zerg=true`; non-Zerg rows retain all integrity checks while
their Zerg-specific mechanism checks are not applicable.

## Fixed five-game schedule and stop rule

Run exactly these five rows concurrently, one attempt per row, with a
120-second wall cap per game and a 300-second cohort cap. Do not retry, reseed,
replace, substitute or rerun any row. Preserve every manifest, log,
diagnostic, result, replay copy, hash, full parse and audit, including failures.

| Game | Opponent | Map | Candidate slot | Scenario seed |
| ---: | --- | --- | ---: | ---: |
| 1 | ZZZKBot | Benzene | P1 | 12511 |
| 2 | McRave memo fork | Circuit Breaker | P2 | 12512 |
| 3 | UAlbertaBot-Protoss | Heartbreak Ridge | P1 | 12513 |
| 4 | ZZZKBot | Destination | P2 | 12514 |
| 5 | UAlbertaBot-Protoss | Benzene | P2 | 12515 |

The runner's registered infrastructure stop rule is preserved: launch the five
fixed rows concurrently, stop new launches at the cohort cap, and let already
running rows finish. No row is replaced when another row is invalid.

## Validity and rating eligibility

A row is valid only when both children exit zero; terminal callbacks identify one
winner and are reciprocal; source and archived replay copies have equal hashes
and sizes; `screp` parses the complete replay with the expected races; and
`replay_header_frames + 1` equals the owning callback frame. The candidate,
opponent, engine, launcher, map, game data, slot, seed and empty learning-state
regime must match the schedule. Transport failure, timeout, wrong race,
missing result, replay failure or identity drift is infrastructure-invalid and
excluded from wins, losses and Elo.

Potential Elo eligibility additionally requires both candidate and opponent
latency values to be integer `3`, exact latency/regime identity, pinned final
manifest hashes, complete replay hash/parse/header alignment, and reviewer
confirmation that each row is unique and not a diagnostic fixture. A valid loss
remains evidence. No automatic rating update or promotion is authorized by this
plan.

For the qualitative review, preserve first visible threat, first candidate
response, second-Zealot overlap/hold release when exercised, second-Gateway
safety when applicable, command rejections including `Unit_Busy`, terminal
cause, and any race or performance anomaly. Report latency and throughput per
row; do not claim that Apple Silicon results transfer to tournament hardware.

## Frozen artifact paths

Candidate binary and sidecar:
`artifacts/builds/eab694b547a16d954708950f944005fa75a73995452130c6927c5effb8f602eb/kestrel-modular-v1-latency-elo-screen/KestrelModular.dylib`
and its `.build.json` sidecar. Opponent, engine, launcher, game-data paths,
hashes and all row details are frozen in `schedule.json`.
