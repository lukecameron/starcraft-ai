# Kestrel hill-climb v21 pre-Pylon bank diagnostic

Registered 2026-09-21 before gameplay. This is a fixed five-game,
five-concurrent diagnostic of the unadopted
`Kestrel-v41-zerg-two-gateway-bank` candidate. It is a short hill-climb screen,
not Elo, BASIL, ladder, submission, or tournament evidence. No v21 game has
been launched in this preregistration.

## Hypothesis

v20's v40 candidate failed the two-defender opening gate on the P2 Destination
and Heartbreak Ridge ZZZK lanes. Their second Gateways became current at frames
2084 and 2082 and completed at frames 3055 and 3053; each had only one
completed global and local combat unit when Zerg pressure arrived at frames
3560 and 3551.

v41 changes one gameplay condition. Against a known Zerg, once six Probes are
complete and before the first Pylon becomes current, the Probe-training reserve
is 250 minerals instead of 100. Construction still sees the full mineral bank,
so the Pylon can be placed while a Probe that v40 could queue is deferred. The
saved 50 minerals then enters v40's existing reserve through the second
Gateway. The hypothesis is that this advances Gateway/Zealot timing enough for
both failed P2 lanes to have two completed local defenders at first qualifying
pressure without breaking the passing Benzene lane, the later McRave opening,
or non-Zerg behavior.

## Fixed cohort and execution

Run exactly the five rows in `schedule.json` once, concurrently, with fresh
seeds 11101-11105 and a 120-second wall cap per game. Execution must be outside
the restricted sandbox so local OpenBW sockets work. Do not retry, reseed,
replace, or rerun any row. Preserve every started result, replay, diagnostic,
log, and manifest, including timeouts and failures. If unsandboxed execution is
unavailable, do not start the cohort. Stop after two consecutive
infrastructure-invalid completions or cohort completion.

| Game | Opponent | Map | Kestrel slot | Seed | Purpose |
| ---: | --- | --- | ---: | ---: | --- |
| 1 | ZZZKBot | `sscai/(2)Destination.scx` | P2 | 11101 | v20 failed lane |
| 2 | ZZZKBot | `sscai/(2)Heartbreak Ridge.scx` | P2 | 11102 | v20 failed lane |
| 3 | ZZZKBot | `sscai/(2)Benzene.scx` | P1 | 11103 | v20 passing sentinel |
| 4 | McRave-9Pool-treatment | `sscai/(4)Circuit Breaker.scx` | P1 | 11104 | second Zerg style |
| 5 | UAlbertaBot-Terran | `sscai/(2)Destination.scx` | P1 | 11105 | non-Zerg sentinel |

## Integrity and treatment gates

Every valid row requires reciprocal terminal results, the registered
race/map/slot/seed, both launcher return codes zero, exactly two archived replay
copies, matching source/archive hashes and sizes, full `screp` parsing, expected
race headers, and `replay_header_frames + 1 == owning_callback_frame`.
Candidate, opponents, engine, launcher, sidecars, scripts, maps, runtime game
data, and provenance must match `schedule.json`.

Each valid Zerg row must report a positive
`zerg_pre_pylon_probe_reserve_frames`, a 250 maximum opening Probe
reserve, an ordered first/second accepted Gateway trace, and zero malformed or
contradictory v38-v40 telemetry. The valid non-Zerg sentinel must report zero
pre-Pylon treatment frames, zero opening Probe reserve, and no Zerg-only state.
Any observed treatment-scope violation, illegal information use, malformed
trace, gas-worker build attempt, build `Unit_Busy` rejection, or command
rejection rate at or above five percent is `REJECT`.

## Decision gates

The first threat grade uses the existing public-information definition: a
non-worker, ground, attack-capable enemy within the established home radius.
The two P2 ZZZK rows are the primary repair lanes. `ADOPT only to a separate
held-out confirmation` requires all of the following:

- all five rows are integrity-valid short terminals;
- both P2 ZZZK rows qualify and each has the second Gateway current before its
  first qualifying threat plus at least two completed combat units globally and
  locally at that frame;
- every other qualifying Zerg row also has at least two completed global and
  local combat units at first pressure;
- the Benzene ZZZK sentinel remains a win and Kestrel records at least one win
  among the other four rows;
- every observed retained construction, nearest-Gateway-Probe, reserve,
  emergency, staging, shared-target, scaling, cap, commandability,
  public-information, and non-Zerg gate passes; and
- durable throughput is at least 384 logical frames per wall second for every
  valid terminal, reported descriptively even though the user waived exact
  16x pacing as an iteration requirement.

An observed gameplay, treatment, or retained-policy regression is `REJECT`
even if another row is invalid. If a required primary lane is invalid or never
qualifies and no independent regression is observed, the result is
`INCONCLUSIVE`. A timeout or infrastructure failure remains in the fixed
denominator and is never replaced. Five games cannot update Elo or promote the
canonical Kestrel v13 build; a passing result only authorizes a separately
preregistered held-out confirmation.

## Quantitative and qualitative analysis

For each valid game, retain outcome, terminal frames, wall duration, durable
fps, callback cost, command rejection, replay fidelity, first/second Gateway
accepted/current/completed frames, first/second Zealot train/completion frames,
Probe-train frames, treatment-active frames, first qualifying threat, global
and local combat count at that threat, first local engagement, first home
combat loss, peak local defenders, construction cadence, and production/economy
counts. Compare the three matched map/slot ZZZK scenarios descriptively with
their v20 runs, without treating different seeds as paired independent trials.

Review all replay summaries and candidate diagnostics for when pressure was
seen, where defenders were located, idle production, builder travel,
supply/resource stalls, premature offense, target selection, and the cause of
the first decisive combat loss. Use those grades to identify two to five next
changes. Do not choose or implement the next change until all five fixed rows
have stopped and the registered result is written.
