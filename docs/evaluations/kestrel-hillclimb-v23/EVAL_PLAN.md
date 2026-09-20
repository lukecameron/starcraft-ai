# Kestrel hill-climb v23 second-Zealot reserve diagnostic

Registered 2026-09-20T21:44:00Z before gameplay. This is a fixed five-game,
five-concurrent diagnostic of the unadopted
`Kestrel-v43-second-zealot-reserve` candidate. It is a short hill-climb screen,
not Elo, BASIL, ladder, submission, or tournament evidence. No v23 game has
been launched in this preregistration.

## Hypothesis

The v22 screen showed a specific early production conflict. In all three ZZZK
terminals, Kestrel accepted two Probe trains after the second Gateway became
current and before accepting its second Zealot. The second Zealot replay
commands were delayed to frames 3,218 on Destination, 3,206 on Heartbreak
Ridge, and 3,140 on Benzene. Both primary P2 lanes therefore had only one
completed local defender at first pressure, and Benzene regressed from two
defenders and a win in v21 to one defender and a loss in v22.

V43 changes one Zerg-only production rule from v42. After the second Gateway
is current, Probe training keeps a 100-mineral reserve until the second Zealot
train command is accepted. The five-Probe Pylon policy, Gateway construction,
combat, later economy, and non-Zerg behavior are unchanged. The hypothesis is
that the reserve prevents the observed post-Gateway Probe spend, moves the
second Zealot command to the first legal production opportunity, and restores
two completed local defenders at first pressure on the failed ZZZK lanes.

The hypothesis is falsified if either primary lane still has fewer than two
completed local defenders at first pressure, the reserve or retained
five-Probe treatment does not execute coherently, a Probe is accepted inside
the protected interval, or a retained safety/command gate regresses.

## Fixed cohort and execution

Run exactly the five rows in `schedule.json` once, concurrently, with fresh
seeds 12201-12205 and a 120-second wall cap. Execution must be outside the
restricted sandbox so local OpenBW sockets work. Do not retry, reseed, replace,
or rerun any row. Preserve every started result, replay, diagnostic, log, and
manifest, including timeouts and failures. If unsandboxed execution is
unavailable, do not start. Stop after two consecutive infrastructure-invalid
completions or cohort completion.

| Game | Opponent | Map | Kestrel slot | Seed | Purpose |
| ---: | --- | --- | ---: | ---: | --- |
| 1 | ZZZKBot | `sscai/(2)Destination.scx` | P2 | 12201 | failed primary lane |
| 2 | ZZZKBot | `sscai/(2)Heartbreak Ridge.scx` | P2 | 12202 | failed primary lane |
| 3 | ZZZKBot | `sscai/(2)Benzene.scx` | P1 | 12203 | regressed sentinel |
| 4 | McRave-9Pool-treatment | `sscai/(4)Circuit Breaker.scx` | P1 | 12204 | second Zerg style |
| 5 | Stardust-repaired | `sscai/(2)Benzene.scx` | P2 | 12205 | short non-Zerg sentinel |

Stardust replaces the v22 UAlbertaBot-Terran sentinel because that v22 row
reached the fixed wall cap without a terminal result or replay. The replacement
is preregistered, has a reviewed frozen identity, and tests only that the new
Zerg-only state stays inactive; it is not a same-row performance comparison.

## Integrity and treatment gates

Every valid row requires reciprocal terminal results, registered
race/map/slot/seed, both launcher return codes zero, exactly two archived replay
copies, matching source/archive hashes and sizes, full `screp` parsing, expected
race headers, and `replay_header_frames + 1 == owning_callback_frame`.
Candidate, opponents, engine, launcher, sidecars, scripts, maps, runtime game
data, and provenance must match `schedule.json`.

Every valid Zerg row must pass the retained v42 five-Probe checks: positive
policy-active frames, true Pylon-treatment acceptance, aligned treatment and
first-Pylon frames, and exactly one accepted Probe train before the Pylon. It
must also report positive v43 reserve-active frames, a nonnegative second
Zealot train frame at or after the second Gateway current frame, at least two
accepted Zealot trains, a 100-mineral reserve, aligned and ordered reserve-block
arrays with minerals in `[50, 150)`, and no reserve block at or after the second
Zealot command. No accepted Probe train may occur from the second Gateway
current frame through the second Zealot command. Record separately whether a
fresh row contained a block opportunity; an absent opportunity makes the block
effect untested but does not invalidate otherwise coherent active telemetry.

The valid non-Zerg sentinel must report inactive v42 and v43 Zerg-only state:
zero treatment/reserve-active frames, false five-Probe Pylon acceptance,
acceptance frame -1, empty v43 block traces, block count zero, and zero opening
Probe reserve. Every valid row must retain ordered Gateway construction,
commandability, emergency, staging, scaling, and shared-target telemetry. Any
treatment-scope violation, illegal information use, malformed trace, gas-worker
build attempt, build `Unit_Busy` rejection, or command rejection rate at or
above five percent is `REJECT`.

## Decision gates

The first threat grade uses the existing public-information definition: a
non-worker, ground, attack-capable enemy within the established home radius.
The Destination and Heartbreak Ridge P2 ZZZK rows are primary. `ADOPT` only to
a separately preregistered held-out confirmation requires all of the following:

- all five rows are integrity-valid short terminals;
- all four Zerg rows pass the retained v42 and new v43 mechanism gates;
- both primary rows have the second Gateway current before first qualifying
  pressure and at least two completed combat units globally and locally at
  that frame;
- every other qualifying Zerg row also has at least two completed global and
  local combat units at first pressure;
- Benzene is a win and Kestrel records at least one win among the other rows;
- every retained construction, nearest-Gateway-Probe, emergency, staging,
  shared-target, scaling, cap, commandability, public-information, and non-Zerg
  gate passes; and
- every valid terminal reaches at least 384 durable logical frames per wall
  second, reported descriptively rather than as a pacing requirement.

An observed gameplay, treatment, or retained-policy regression is `REJECT`
even if another row is invalid. If a required primary row is invalid or never
qualifies and no independent regression is observed, the result is
`INCONCLUSIVE`. A timeout or infrastructure failure remains in the fixed
denominator and is never replaced. Five games cannot update Elo or promote
canonical Kestrel v13; a pass only authorizes held-out confirmation.

## Quantitative and qualitative analysis

For every valid game retain outcome, terminal frames, wall duration, durable
fps, callback cost, command rejection, replay fidelity, Pylon treatment,
accepted Probe frames, first/second Gateway accepted/current/completed frames,
first/second Zealot train/completion timing, v43 reserve activity and block
traces, first qualifying threat, global/local combat count at threat, first
engagement, first home combat loss, peak defenders, construction cadence, and
production/economy counts.

Compare the four Zerg rows descriptively with v22 on the same map and slot,
including the protected Probe interval, second-Zealot timing, pressure, and
defenders. Review all replays and diagnostics for idle production, builder
travel, supply/resource stalls, premature offense, target selection, and the
first decisive combat loss. Use those grades to identify two to five next
changes. Do not choose or implement the next change until all five fixed rows
have stopped and the registered result is written.
