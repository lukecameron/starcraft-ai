# Kestrel hill-climb v24 sixth-Probe restoration diagnostic

Registered 2026-09-20T22:14:00Z before gameplay. This is a fixed five-game,
five-concurrent diagnostic of the unadopted
`Kestrel-v44-sixth-probe-restoration` candidate. It is a short hill-climb
screen, not Elo, BASIL, ladder, submission, or tournament evidence. No v24
game has been launched in this preregistration.

## Hypothesis

The v23 screen showed that v43 moved the second Zealot command earlier and
restored two defenders plus a win on Benzene, but Destination and Heartbreak
Ridge still began their first Gateway cycle too late to complete the second
defender before pressure. Both primary rows had only one completed local
defender. Their second Zealot commands occurred roughly 160-180 frames too
late to finish by the observed pressure.

V44 changes one Zerg-only economy rule from v43. After the retained five-Probe
Pylon is accepted, it permits exactly one sixth Probe, blocks every seventh
Probe until the second Gateway is current, and retains v43's 100-mineral
reserve until the second Zealot is accepted. Non-Zerg behavior is unchanged.
The hypothesis is that one extra miner advances the Gateway and Zealot cycles
enough to produce two completed local defenders at first pressure on both
primary rows without reintroducing the Probe-spending conflict.

The hypothesis is falsified if either primary lane still has fewer than two
completed local defenders at pressure; the sixth Probe is absent, duplicated,
or outside its registered interval; the retained v42/v43 policies fail; or any
retained safety, command, scope, or integrity gate regresses.

## Primary metric and control

The primary metric is
`M = min(L_destination, L_heartbreak)`, where each `L` is the integer count
of completed local combat units at the row's first qualifying home-army threat.
The unit is completed combat units, higher is better, and the adoption
threshold is `M >= 2`. The values come from the candidate's public-state
`local_combat_at_first_home_army_threat` diagnostic, with
`first_home_army_threat_frame` defining the measurement frame and
`global_combat_at_first_home_army_threat` retained as a consistency check.
An absent qualifying threat makes that primary row inconclusive rather than
passing it.

The frozen historical control is the v23 v43 row on the same map and slot:
`20260920T215006-dc13ce0caf72` for Destination P2 and
`20260920T215006-a8d0da4f9a13` for Heartbreak Ridge P2. Both controls had
`L = 1`, so their control metric was `M = 1`. V24 uses fresh seeds; the
historical comparison is descriptive and does not claim paired-seed inference.
Secondary metrics are first/second Gateway frames, first/second Zealot frames,
sixth-Probe acceptance, outcome, first combat loss, wall duration, and durable
logical frames per wall second. They explain the mechanism but cannot override
a failed primary metric or safety gate.

## Fixed cohort and execution

Run exactly the five rows in `schedule.json` once, concurrently, with fresh
seeds 12301-12305 and a 120-second wall cap. Execution must be outside the
restricted sandbox so local OpenBW sockets work. Do not retry, reseed, replace,
or rerun any row. Preserve every started result, replay, diagnostic, log, and
manifest, including timeouts and failures. If unsandboxed execution is
unavailable, do not start. Stop after two consecutive infrastructure-invalid
completions or cohort completion.

| Game | Opponent | Map | Kestrel slot | Seed | Purpose |
| ---: | --- | --- | ---: | ---: | --- |
| 1 | ZZZKBot | `sscai/(2)Destination.scx` | P2 | 12301 | failed primary lane |
| 2 | ZZZKBot | `sscai/(2)Heartbreak Ridge.scx` | P2 | 12302 | failed primary lane |
| 3 | ZZZKBot | `sscai/(2)Benzene.scx` | P1 | 12303 | retained winning sentinel |
| 4 | McRave-9Pool-treatment | `sscai/(4)Circuit Breaker.scx` | P1 | 12304 | second Zerg style |
| 5 | Stardust-repaired | `sscai/(2)Benzene.scx` | P2 | 12305 | short non-Zerg sentinel |

## Integrity and treatment gates

Every valid row requires reciprocal terminal results, registered
race/map/slot/seed, both launcher return codes zero, exactly two archived replay
copies, matching source/archive hashes and sizes, full `screp` parsing,
expected race headers, and
`replay_header_frames + 1 == owning_callback_frame`. Candidate, opponents,
engine, launcher, sidecars, scripts, maps, runtime game data, provenance, and
source hashes must match `schedule.json`.

Every valid Zerg row must pass the retained v42 checks: positive five-Probe
policy-active frames, true Pylon-treatment acceptance, aligned treatment and
first-Pylon frames, and exactly one accepted Probe before that Pylon. It must
then pass v44: positive restoration-active frames, exactly one accepted sixth
Probe, an acceptance frame at or after first-Pylon acceptance and before the
second Gateway is current, and exactly one accepted Probe in that inclusive
start/exclusive end interval. No seventh Probe may be accepted before the
second Gateway becomes current.

Every valid Zerg row must also retain v43: positive 100-mineral reserve-active
frames after the second Gateway is current, at least two accepted Zealots, and
aligned, ordered block-frame, mineral, and pre-acceptance traces. A block flag
of `1` must occur strictly before the second-Zealot frame. A flag of `0`
is permitted only on the exact callback that accepts the second Zealot and
marks a provisional same-callback sample regardless of Nexus/Gateway iteration
order. No accepted Probe train may occur strictly after second-Gateway current
and before second-Zealot acceptance. If a Probe and the second Zealot are
accepted on one callback, the Probe command must leave at least 100 minerals
for the Zealot and is reported separately.

The valid non-Zerg sentinel must report inactive v42, v43, and v44 Zerg-only
state: zero active frames, false treatment acceptance, acceptance frames -1,
empty block/ordering traces, block counts zero, zero sixth-Probe acceptances,
zero post-Pylon/pre-second-Gateway Zerg-window Probe acceptances, and zero
opening Probe reserve. Every row must retain ordered construction,
nearest-Gateway-Probe, emergency, staging, scaling, shared-target, and public
observation telemetry. Any treatment-scope violation, illegal information use,
malformed trace, gas-worker build attempt, build `Unit_Busy` rejection, or
command rejection rate at or above five percent is `REJECT`.

## Decision gates

The first threat grade uses the existing public-information definition: a
non-worker, ground, attack-capable enemy within the established home radius.
Destination and Heartbreak Ridge P2 against ZZZKBot are primary. `ADOPT`
only to a separately preregistered held-out confirmation requires all of:

- all five rows are integrity-valid short terminals;
- all four Zerg rows pass retained v42/v43 and new v44 mechanism gates;
- both primary rows have the second Gateway current before first qualifying
  pressure and at least two completed combat units globally and locally at
  that frame;
- every other qualifying Zerg row also has at least two completed global and
  local combat units at first pressure;
- Benzene remains a win and Kestrel records at least one win among the other
  rows;
- every retained construction, nearest-Gateway-Probe, emergency, staging,
  shared-target, scaling, cap, commandability, public-information, and non-Zerg
  gate passes.

Durable logical frames per wall second and wall duration are reported for each
row, but there is no fixed speed gate. The 120-second wall cap bounds the
screen; shorter terminal games are preferred because they supply a decision
with less machine time.

An observed gameplay, treatment, or retained-policy regression is `REJECT`
even if another row is invalid. If a required primary row is invalid or never
qualifies and no independent regression is observed, the result is
`INCONCLUSIVE`. A timeout or infrastructure failure remains in the fixed
denominator and is never replaced. Five games cannot update Elo or promote
canonical Kestrel v13; a pass only authorizes held-out confirmation.

## Quantitative and qualitative analysis

For every valid game retain outcome, terminal frames, wall duration, durable
fps, callback cost, command rejection, replay fidelity, accepted Probe frames,
v42/v43/v44 treatment traces, first/second Gateway timing, first/second Zealot
train and completion timing, first qualifying threat, global/local combat count
at threat, first engagement, first home combat loss, peak defenders,
construction cadence, and production/economy counts.

Compare the four Zerg rows descriptively with v23 on the same map and slot,
including the sixth Probe, first/second Gateway timing, second-Zealot timing,
pressure, and defenders. Review every replay and diagnostic for idle
production, builder travel, supply/resource stalls, premature offense, target
selection, and the first decisive combat loss. Use those grades to identify
two to five next changes. Do not choose or implement the next change until all
five fixed rows have stopped and the registered result is written.
