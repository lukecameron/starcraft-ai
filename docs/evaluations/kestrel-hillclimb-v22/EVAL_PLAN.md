# Kestrel hill-climb v22 five-Probe Pylon diagnostic

Registered 2026-09-21 before gameplay. This is a fixed five-game,
five-concurrent diagnostic of the unadopted
`Kestrel-v42-five-probe-pylon` candidate. It is a short hill-climb screen, not
Elo, BASIL, ladder, submission, or tournament evidence. No v22 game has been
launched in this preregistration.

## Hypothesis

The v21 screen rejected v41 because its new known-Zerg reserve became active
after Kestrel had already accepted its second pre-Pylon Probe. The treatment
therefore usually did not affect the decision it was meant to change. In the
four Zerg rows, v41 accepted Probe trains at frames 0 and 384-408, then accepted
its first Pylon only at frames 810-852.

V42 changes one opening policy. Against a known Zerg, after the first trained
Probe completes and five Probes are complete, it reserves 250 minerals and may
place the first Pylon immediately instead of accepting the second Probe first.
V41's Gateway, builder-selection, combat, economy, and non-Zerg policies remain
unchanged. The hypothesis is that the earlier Pylon shifts the existing
two-Gateway opening early enough for both failed P2 ZZZK lanes to have two
completed local defenders at first qualifying pressure, without breaking the
passing Benzene lane, the later McRave opening, or non-Zerg behavior.

The hypothesis is falsified if either primary P2 lane still has fewer than two
completed local defenders at first qualifying pressure, if the five-Probe
treatment does not execute as registered in any valid Zerg row, if the
non-Zerg sentinel observes the treatment, or if a retained safety or command
gate regresses.

## Fixed cohort and execution

Run exactly the five rows in `schedule.json` once, concurrently, with fresh
seeds 12101-12105 and a 120-second wall cap per game. Execution must be outside
the restricted sandbox so local OpenBW sockets work. Do not retry, reseed,
replace, or rerun any row. Preserve every started result, replay, diagnostic,
log, and manifest, including timeouts and failures. If unsandboxed execution is
unavailable, do not start the cohort. Stop after two consecutive
infrastructure-invalid completions or cohort completion.

| Game | Opponent | Map | Kestrel slot | Seed | Purpose |
| ---: | --- | --- | ---: | ---: | --- |
| 1 | ZZZKBot | `sscai/(2)Destination.scx` | P2 | 12101 | v21 failed lane |
| 2 | ZZZKBot | `sscai/(2)Heartbreak Ridge.scx` | P2 | 12102 | v21 failed lane |
| 3 | ZZZKBot | `sscai/(2)Benzene.scx` | P1 | 12103 | v21 passing sentinel |
| 4 | McRave-9Pool-treatment | `sscai/(4)Circuit Breaker.scx` | P1 | 12104 | second Zerg style |
| 5 | UAlbertaBot-Terran | `sscai/(2)Destination.scx` | P1 | 12105 | non-Zerg sentinel |

## Integrity and treatment gates

Every valid row requires reciprocal terminal results, the registered
race/map/slot/seed, both launcher return codes zero, exactly two archived replay
copies, matching source/archive hashes and sizes, full `screp` parsing, expected
race headers, and `replay_header_frames + 1 == owning_callback_frame`.
Candidate, opponents, engine, launcher, sidecars, scripts, maps, runtime game
data, and provenance must match `schedule.json`.

Each valid Zerg row must report a positive
`zerg_five_probe_policy_active_frames`, true
`zerg_five_probe_pylon_accepted`, a nonnegative
`zerg_five_probe_pylon_accepted_frame` equal to
`first_pylon_accepted_frame`, and exactly one accepted Probe train before the
first Pylon acceptance. Its first Pylon acceptance must be at least 180 frames
earlier than the same map/slot v21 comparator: at or before frame 642 on
Destination P2, 666 on Heartbreak P2, 630 on Benzene P1, and 672 on Circuit
Breaker P1. These are mechanism gates for the registered policy, not causal
estimates because seeds differ.

The valid non-Zerg sentinel must report zero five-Probe treatment frames, false
Pylon-treatment acceptance, acceptance frame -1, zero opening Probe reserve,
and no Zerg-only state. Each valid row must retain an ordered first/second
accepted Gateway trace and zero malformed or contradictory v38-v41 telemetry.
Any treatment-scope violation, illegal information use, malformed trace,
gas-worker build attempt, build `Unit_Busy` rejection, or command rejection
rate at or above five percent is `REJECT`.

## Decision gates

The first threat grade uses the existing public-information definition: a
non-worker, ground, attack-capable enemy within the established home radius.
The two P2 ZZZK rows are the primary repair lanes. `ADOPT` only to a separate
held-out confirmation requires all of the following:

- all five rows are integrity-valid short terminals;
- every Zerg row passes all five-Probe mechanism gates above;
- both P2 ZZZK rows qualify and each has the second Gateway current before its
  first qualifying threat plus at least two completed combat units globally
  and locally at that frame;
- every other qualifying Zerg row also has at least two completed global and
  local combat units at first pressure;
- the Benzene ZZZK sentinel remains a win and Kestrel records at least one win
  among the other four rows;
- every observed retained construction, nearest-Gateway-Probe, reserve,
  emergency, staging, shared-target, scaling, cap, commandability,
  public-information, and non-Zerg gate passes; and
- durable throughput is at least 384 logical frames per wall second for every
  valid terminal, reported descriptively even though exact 16x pacing is not
  an iteration requirement.

An observed gameplay, treatment, or retained-policy regression is `REJECT`
even if another row is invalid. If a required primary lane is invalid or never
qualifies and no independent regression is observed, the result is
`INCONCLUSIVE`. A timeout or infrastructure failure remains in the fixed
denominator and is never replaced. Five games cannot update Elo or promote the
canonical Kestrel v13 build; a passing result only authorizes a separately
preregistered held-out confirmation.

## Quantitative and qualitative analysis

For each valid game, retain outcome, terminal frames, wall duration, durable
fps, callback cost, command rejection, replay fidelity, first Pylon treatment
and acceptance frames, accepted Probe-train frames before the Pylon,
first/second Gateway accepted/current/completed frames, first/second Zealot
train/completion frames, first qualifying threat, global and local combat count
at that threat, first local engagement, first home combat loss, peak local
defenders, construction cadence, and production/economy counts.

Compare the four Zerg rows descriptively with their v21 same-map/slot runs,
including Pylon, second-Gateway, first/second-Zealot, pressure, and defender
timing. Review all replay summaries and candidate diagnostics for when pressure
was seen, where defenders were located, idle production, builder travel,
supply/resource stalls, premature offense, target selection, and the cause of
the first decisive combat loss. Use those grades to identify two to five next
changes. Do not choose or implement the next change until all five fixed rows
have stopped and the registered result is written.
