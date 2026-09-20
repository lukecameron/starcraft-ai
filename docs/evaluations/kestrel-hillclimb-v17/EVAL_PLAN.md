# Kestrel hill-climb v17 shared-target screen

Registered 2026-09-21 before gameplay. This is a five-game matched screen of
`Kestrel-v38-shared-target` against the exact v16 scenario rows. It tests a
single combat-cohesion treatment on top of the v37 opening and scaling bundle.
It is not Elo evidence and cannot promote a build directly to the local rating
pool.

## Decision

- **Treatment:** preserve the v37 opening, Singularity Charge scaling, Pylon
  cap, Gateway cap, emergency defense, reserve, staging, scout and leash
  behavior. For ordinary completed non-reserve combat units, issue attacks to
  one shared visible legal ground target selected from public BWAPI state each
  selection cadence. Prefer a local visible target; otherwise select the
  nearest visible legal target to the eligible army centroid, breaking ties by
  unit ID. Retain a still-valid target until it becomes invalid or a local
  target takes priority.
- **Control:** the exact frozen v37 candidate and the same five v16 scenario
  inputs. The control is represented by the prior v16 screen; no new control
  games are required for this matched change-effect screen.
- **ADOPT:** permits a separately registered held-out confirmation only. It
  does not replace the canonical Kestrel anchor, change local Elo, or declare
  tournament strength.
- **REJECT:** applies when all five games are valid and the candidate fails the
  win or shared-target mechanism bar, or an observed retained regression is
  present.
- **INCONCLUSIVE:** applies when required integrity or treatment telemetry is
  missing or inconsistent, or when infrastructure prevents a valid cohort
  decision. A coherent terminal trace with an unobserved opportunity is valid
  evidence but cannot satisfy the corresponding adoption gate.

The v16 result remains **REJECT** because its registered emergency-episode
cap-block opportunity was unobserved. This v17 plan does not silently change
that result or re-use its bar. For v17, an emergency cap-block opportunity that
is observed must obey the retained cap; an opportunity that is not observed is
recorded as **UNTESTED** and is not required for this candidate's screen.

## Hypothesis and falsification

The v37 candidate produced the first verified Kestrel win but ordinary combat
units selected targets independently. A shared visible target should improve
combat concentration and shorten successful fights while retaining the v37
opening and scaling behavior.

The hypothesis is falsified for this screen if the valid cohort has zero
verified wins, if a lane reaches a shared-target opportunity but records no
accepted coordinated attack command, or if the treatment causes an observed
illegal target, command rejection, reserve/emergency/staging violation, or
other retained regression. A single five-game batch is too small to establish
generalization; ADOPT therefore advances only to held-out confirmation.

## Registered treatment boundary

The candidate may change only ordinary combat target selection and its aligned
diagnostic telemetry. Shared-target participants exclude emergency defenders,
the Zerg reserve, non-Zerg leashed Zealots, and scouts. Before staged Zerg
offense is released, ordinary non-reserve combat units may share only a local
legal defense target; the retained staging path blocks every remote target.
Existing defense, reserve, staging, leash, build, research, scouting, cadence
and targetability rules remain unchanged.

All target decisions must use public legal BWAPI observations available to the
bot at that callback. A target is legal only when it is visible to the bot,
ground-targetable by the issuing unit, and present in the bot's public unit
observation. Evaluator and replay state may grade legality after the game but
may not enter the policy.

## Frozen matched cohort

Run exactly five attempts concurrently, with no retry, reseed, replacement or
rerun:

| Game | Opponent | Map | Kestrel slot | Seed |
| ---: | --- | --- | ---: | ---: |
| 1 | ZZZKBot | `sscai/(2)Benzene.scx` | P1 | 9941 |
| 2 | UAlbertaBot-Terran | `sscai/(2)Destination.scx` | P2 | 9942 |
| 3 | UAlbertaBot-Protoss | `sscai/(2)Heartbreak Ridge.scx` | P1 | 9943 |
| 4 | McRave-9Pool-treatment | `sscai/(4)Circuit Breaker.scx` | P2 | 9944 |
| 5 | Stardust-repaired | `sscai/(2)Benzene.scx` | P1 | 9945 |

Use a 300-second wall cap per game, a 900-second cohort cap, concurrency five,
and stop after two consecutive infrastructure-invalid attempts or cohort
completion. Preserve every manifest, runner log, diagnostic, replay, hash,
parse result and failure record. A valid terminal loss is gameplay evidence;
an infrastructure-invalid attempt makes the cohort INCONCLUSIVE under the
rules below.

## Primary metric and decision bar

The primary metric is verified candidate wins per five valid short-terminal
games:

`verified_win_count = sum(1 for game in games if integrity_pass and short_terminal_pass and candidate_terminal_result == "win")`.

The minimum strength bar is at least one verified win. This is a descriptive
matched screen, not an Elo update. ADOPT additionally requires at least one
lane with a shared-target selection involving two or more ordinary combat
participants and at least one accepted coordinated attack command. That lane
must have aligned legal-target telemetry, zero shared-target command rejects,
and no illegal selection. At least one lane must also retain the v37 scaling
observation and completion gates described below.

## Shared-target telemetry gates

Each candidate diagnostic must contain integer or aligned-array fields for:

- `shared_target_frames`, `shared_target_ids`,
  `shared_target_eligible_counts`, `shared_target_ordered_counts`,
  `shared_target_local_counts`, `shared_target_participant_counts`,
  `shared_target_attempt_counts`, and `shared_target_accepted_counts`;
- flat `shared_target_participant_ids`, partitionable by the participant-count
  rows, plus `shared_target_selections`, `shared_target_attempts`, `shared_target_accepted`,
  `shared_target_rejects`, `shared_target_switches`,
  `shared_target_non_zerg_selections`, and
  `shared_target_illegal_selections`;
- `shared_target_correction_opportunities`, which is descriptive pre-command
  evidence of eligible units whose previous non-null order target differed
  from the selected shared target.

All aligned arrays must have equal row counts; participant counts must be
non-negative and sum to the flat participant-ID count. The prelaunch source
audit must establish that selection admits only visible, detected, ground
enemy units from public BWAPI state; the postgame gate requires aligned target
IDs and a zero illegal-selection counter.
An opportunity must have at least two participants, and at least one accepted
attack command must be recorded for the opportunity. `shared_target_rejects`
must remain zero for the adoption bar. A coherent terminal trace may end
before an opportunity, after selection, or after an accepted command; those
states are valid partial gameplay evidence, but a cohort with no observed
shared-target opportunity is REJECT because the mechanism was not exercised.
Missing fields, wrong types, impossible frame ordering, unpartitionable
participant IDs, or inconsistent legal-target evidence is INCONCLUSIVE.

## Retained v37 and earlier gates

The candidate must retain the v37 scaling and opening gates:

- all five games valid, with the matched ZZZK opening gate: second Gateway
  current before the first qualifying public home threat and at least two
  completed Kestrel combat units at that threat;
- coherent Singularity Charge eligibility, bank, attempt, acceptance and
  completion telemetry, with at least one eligible lane accepting and
  completing the upgrade;
- Pylon cap 10 and post-Core Gateway cap 6, with accepted/current/completed
  milestone prefixes ordered and no observed cap violation;
- retained construction bookkeeping, probe reserve, emergency episode,
  reserve-local-defense, staged-offense, surplus-six latch and non-Zerg
  inactivity behavior wherever those mechanisms are observed.

Emergency cap-block opportunities are treated as described in the Decision
section: an observed violation fails; an unobserved opportunity is UNTESTED
and is reported without converting the result to a hidden pass. The v37
scaling gate still requires an observed eligible lane with one accepted and
completed upgrade. All required accepted/current/completed arrays must remain
ordered and coherent.

Regression passes require zero gas-worker build attempts, zero build
`Unit_Busy` rejections, command rejection below five percent per game and
across the cohort, no Pylon count above 10, no post-Core Gateway count above
6, no reserve remote attack, no pre-release staged remote attack, and no
non-Zerg emergency/reserve/staging activity. The accepted construction
commandability guard must still permit a later construction after its first
block.

## Integrity, provenance and runtime rules

Every attempt must have a complete manifest, reciprocal Boolean terminal
results, expected races/maps/slots/seeds, exactly two archived replay copies,
matching hashes, complete replay parsing, and
`replay_header_frames + 1 == owning_callback_frame` for each copy. The
candidate and opponents must match the frozen schedule hashes. Ours/Original,
Ours/Port and Ours/Fork labels and author/source links remain those in
`config/bot-identities.json` and `schedule.json`.

The candidate must compile against native OpenBW and official BWAPI 4.4
headers. The build sidecar must retain the v37 base, compiler, binary, engine,
game-data and runtime identities. Report durable logical FPS, callback p99 and
maximum, CPU time, peak RSS and command rejection rates descriptively; no fixed
384-fps adoption gate applies to this matched screen.

Invalid attempts are preserved and counted. A timeout, missing terminal result,
nonzero child return code, launcher/state-hash/race failure, missing replay
copy, hash mismatch, incomplete parser output, missing owner-frame evidence,
or malformed required telemetry is INCONCLUSIVE. Do not replace an invalid
attempt or silently remove a negative result.

## Registered identity and runtime

- Candidate: `Kestrel-v38-shared-target`.
- Binary: `artifacts/builds/7fdc4f9ad61152e7758318e7d35d04fbda0746a4e2f85a48b3bc664577e0c160/kestrel-opening-v38-shared-target/Kestrel.dylib`.
- Binary SHA-256: `7fdc4f9ad61152e7758318e7d35d04fbda0746a4e2f85a48b3bc664577e0c160`.
- `Kestrel.cpp` SHA-256: `f105ab5073ec3d586807478c74838900ed02fa2d812c3ac4d94081c36c3217ab`.
- Combined source SHA-256: `ce744d7adcd3dc0a051c68a7162d975b40284c014a9b7e1eae785b59da9b8f7b`.
- Reconstruction patch: `patches/kestrel-v37-to-v38-shared-target.patch`.
- Patch SHA-256: `2d84b98d3288d4ac922c22c71647f29492925138ee1ec757ee36512b9786b61a`.
- Build sidecar: `artifacts/builds/7fdc4f9ad61152e7758318e7d35d04fbda0746a4e2f85a48b3bc664577e0c160/kestrel-opening-v38-shared-target/Kestrel.dylib.build.json`.
- Build sidecar SHA-256: `75f2f2fd236bdd71cb64102f8286c0358cd39a1c1a8ffbccf69fb7578a53a1b4`.
- Engine SHA-256: `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`.
- Launcher: `artifacts/builds/eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b/openbw-terminal-drain/BWAPILauncher`.
- Game data: `third_party/game-data/runtime`.
- Provenance registry: `config/bot-identities.json`.

Raw data belongs under `artifacts/experiments/kestrel-hillclimb-v17/`. The
durable result belongs in the same evaluation directory; rejected or
inconclusive outcomes must retain their negative evidence.
