# Kestrel hill-climb v18 held-out confirmation

Registered 2026-09-21 before gameplay. This is a ten-game held-out
confirmation of `Kestrel-v38-shared-target` after the v17 matched screen. It
uses two five-game analysis blocks, fresh seeds, and the same proven opponent binaries.
It can promote v38 only as the current experimental Kestrel development
candidate. It cannot replace the canonical Kestrel anchor, update Elo, or
establish tournament strength.

## Treatment and control

The treatment is the frozen v38 candidate: preserve the v37 opening,
Singularity Charge scaling, Pylon and Gateway caps, emergency defense, Zerg
reserve and staging, scout and non-Zerg leash behavior, and use one shared
visible legal ground target for ordinary completed non-reserve combat units.
The target prefers a local visible target, otherwise the nearest visible legal
target to the eligible army centroid with unit-ID tie-break, and retains a
valid target until invalidated or a local target takes priority.

The control is the frozen v37 base and the v17 result as the historical
matched reference. This confirmation does not launch fresh control games; the
registered question is whether the already screened v38 candidate remains
valid and competitive on fresh rows. No ablation is planned.

## Hypothesis and falsification

The v17 screen showed exercised shared-target coordination with one win and no
target-command rejects or illegal selections. The hypothesis is that v38 can
retain those legality and scaling properties while producing at least two wins
in ten fresh games, including at least one ZZZK win.

The hypothesis is falsified for this confirmation by fewer than two verified
wins, zero ZZZK wins, fewer than eight games with a valid shared-target
multi-participant opportunity and an accepted coordinated command, any
shared-target reject or illegal selection, failure of the scaling completion
requirement, or any observed retained reserve, emergency, staging, cap,
construction, public-information, integrity, or runtime regression.

## Fixed decision rule

`ADOPT` requires all ten games to be integrity-valid short terminals, at least
two verified candidate wins, at least one ZZZK win in its two-game subgroup,
and no observed retained or treatment regression. There is no positive win
floor for any other opponent subgroup; every subgroup result, including zero
wins, is reported rather than silently excluded.

ADOPT also requires shared-target telemetry in at least eight of ten games:
each such game must have a selection with at least two ordinary participants,
an accepted coordinated attack command, aligned legal-target evidence, zero
shared-target rejects, and zero illegal selections. Every game that observes a
shared-target opportunity must satisfy those per-game conditions. At least
three eligible lanes must record accepted Singularity Charge commands and at
least two eligible lanes must record accepted and completed upgrades. All
observed retained v37 gates and regression checks must pass.

`REJECT` applies when all ten games are valid and any fixed ADOPT condition
fails, or an observed gameplay or treatment regression occurs. `INCONCLUSIVE`
applies when required integrity, provenance, telemetry, or parser evidence is
missing or inconsistent, or infrastructure prevents a valid ten-game
decision. Invalid attempts remain evidence and are never replaced.

## Cohort and stopping rule

Run exactly ten attempts in the fixed listed order with concurrency five. The
wave field identifies two analysis blocks of five; it is not a synchronized
execution barrier, so the runner may start the next listed row when a slot is
free.
Use a 300-second wall cap per game and a 1200-second cohort cap. Stop after
two consecutive infrastructure-invalid attempts or cohort completion. Do not
retry, reseed, replace, or rerun any attempt.

| Wave | Game | Opponent | Map | Kestrel slot | Seed |
| ---: | ---: | --- | --- | ---: | ---: |
| 1 | 1 | ZZZKBot | `sscai/(2)Benzene.scx` | P1 | 10041 |
| 1 | 2 | UAlbertaBot-Terran | `sscai/(2)Destination.scx` | P2 | 10042 |
| 1 | 3 | UAlbertaBot-Protoss | `sscai/(2)Heartbreak Ridge.scx` | P1 | 10043 |
| 1 | 4 | McRave-9Pool-treatment | `sscai/(4)Circuit Breaker.scx` | P2 | 10044 |
| 1 | 5 | Stardust-repaired | `sscai/(2)Benzene.scx` | P1 | 10045 |
| 2 | 6 | ZZZKBot | `sscai/(2)Benzene.scx` | P2 | 10046 |
| 2 | 7 | UAlbertaBot-Terran | `sscai/(2)Destination.scx` | P1 | 10047 |
| 2 | 8 | UAlbertaBot-Protoss | `sscai/(2)Heartbreak Ridge.scx` | P2 | 10048 |
| 2 | 9 | McRave-9Pool-treatment | `sscai/(4)Circuit Breaker.scx` | P1 | 10049 |
| 2 | 10 | Stardust-repaired | `sscai/(2)Benzene.scx` | P2 | 10050 |

The maps are the opponent-specific maps already completed in v17; slots are
flipped in wave 2. This avoids introducing unverified map/opponent pairs while
still testing both candidate slots. Preserve every manifest, runner log,
diagnostic, replay copy, hash, parser result, and failure record.

## Primary metric and mechanism gates

The primary metric is

`verified_win_count = sum(1 for game in games if integrity_pass and short_terminal_pass and candidate_terminal_result == "win")`.

The unit is one valid game; the denominator is ten scheduled games, and no
invalid attempt is silently removed. Report the pooled rate and each opponent
subgroup descriptively; do not convert them to Elo.

Each diagnostic must contain aligned integer arrays
`shared_target_frames`, `shared_target_ids`,
`shared_target_eligible_counts`, `shared_target_ordered_counts`,
`shared_target_local_counts`, `shared_target_participant_counts`,
`shared_target_attempt_counts`, `shared_target_accepted_counts`, and flat
`shared_target_participant_ids`. It must also contain
`shared_target_selections`, `shared_target_attempts`,
`shared_target_accepted`, `shared_target_rejects`,
`shared_target_switches`, `shared_target_non_zerg_selections`,
`shared_target_illegal_selections`, and
`shared_target_correction_opportunities`.

Aligned arrays must have equal row counts. Participant counts must be
non-negative and partition the flat participant IDs. Selection must use only
public visible, detected, ground enemy units. A shared-target opportunity has
at least two ordinary participants and at least one accepted attack command.
The pre-command correction counter is descriptive and is not treated as a
reject. Any malformed or contradictory telemetry is INCONCLUSIVE.

## Retained gates and invalid trials

The v37 opening and scaling gates remain in force: each ZZZK lane must have the
second Gateway current before its qualifying home threat with at least two
completed combat units; accepted/current/completed milestone prefixes
must be ordered; Pylon and post-Core Gateway maxima must remain 10 and 6; and
at least three lanes must be eligible for Singularity Charge, with at least
two accepted and completed upgrades.

Retained construction bookkeeping, Probe reserve, emergency episodes and
release, reserve-local-defense, staged offense and surplus-six latch must be
coherent wherever observed. There must be zero gas-worker build attempts,
zero build `Unit_Busy` rejections, command rejection below five percent in
each game and across the cohort, zero reserve remote attacks, zero pre-release
staged remote attacks, and no non-Zerg emergency/reserve/staging activity.
Observed emergency cap-block opportunities must obey the cap; an unobserved
opportunity is reported UNTESTED and does not fail the v18 decision.

Every attempt must have reciprocal terminal results, expected race/map/slot/
seed, exactly two archived replay copies, matching hashes, complete `screp`
parsing, and `replay_header_frames + 1 == owning_callback_frame` for each
copy. Candidate, opponent, engine, game-data, launcher, and provenance hashes
must match the schedule. Native OpenBW and official BWAPI 4.4 header build
identity is inherited from the frozen v38 sidecar.

## Frozen identities

- Candidate: `Kestrel-v38-shared-target`.
- Binary SHA-256: `7fdc4f9ad61152e7758318e7d35d04fbda0746a4e2f85a48b3bc664577e0c160`.
- Source SHA-256: `f105ab5073ec3d586807478c74838900ed02fa2d812c3ac4d94081c36c3217ab`.
- Combined source SHA-256: `ce744d7adcd3dc0a051c68a7162d975b40284c014a9b7e1eae785b59da9b8f7b`.
- Patch SHA-256: `2d84b98d3288d4ac922c22c71647f29492925138ee1ec757ee36512b9786b61a`.
- Build sidecar SHA-256: `75f2f2fd236bdd71cb64102f8286c0358cd39a1c1a8ffbccf69fb7578a53a1b4`.
- Engine SHA-256: `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`.
- Launcher SHA-256: `af1682393f9fe43afe885b35a1637e9c464719ef93c83e799d614beed20316c1`.
- Launcher sidecar SHA-256: `0beebdd3bb6221a5e6143c015763d14fa20330a8976ede3f997062660b3e7390`.
- Game data: `third_party/game-data/runtime`.
- The schedule freezes SHA-256 values for all three runtime MPQs and all four
  scheduled map files.
- Provenance registry: `config/bot-identities.json`, SHA-256
  `7336555a6cfaa992bc6d912c61c1d0c421953e084ab10af0e202a5a632801b7d`.

The v17 ADOPT decision remains unchanged. This v18 confirmation is the only
decision covered by this plan.
