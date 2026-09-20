# Kestrel hill-climb v20 nearest-Gateway-Probe screen

Registered 2026-09-21 before gameplay. This is a fresh fixed ten-game,
five-concurrent screen of the identical `Kestrel-v40-nearest-gateway-probe`
hypothesis registered in v19, using the same frozen candidate, engine,
opponents, maps, slots, telemetry, gates, and 120-second per-game cap. It may
advance v40 only as the current experimental Kestrel development candidate.
It is not Elo, BASIL, submission, ladder, or tournament evidence. No v20 game
has been launched in this preregistration.

## Execution requirement

The runner must execute outside the restricted filesystem/process sandbox in an
unsandboxed environment where the two local OpenBW launchers can create and
connect to their match socket. The operator must verify that unsandboxed
execution is active before starting any row. If unsandboxed execution is not
available, do not start the cohort and record v20 as not run.

After the first row starts, run the fixed cohort exactly once. Do not retry,
reseed, replace, or rerun any row, including after a socket, launcher,
metadata, timeout, replay, or parser failure. Preserve every started result,
replay, diagnostic, log, and manifest. An infrastructure-invalid row remains
in the ten-row denominator; a stop after two consecutive infrastructure-invalid
completions leaves later rows explicitly skipped.

## Evidence and treatment

The v18 held-out confirmation rejected v38 after its valid second ZZZKBot lane
reached the qualifying frame-3659 home threat with only one completed local
and global combat unit. The passing ZZZKBot lane had first Gateway
accepted/current frames 1470/1614; the failing lane had 1392/1733. Both lanes
had the second Gateway current at frame 2090. Source review found that v38
selected the lowest-ID eligible Probe before asking it to travel to the legal
Gateway build tile.

The v39 policy change asks BWAPI for the same legal tile, then chooses the
nearest eligible completed Probe by distance to the tile center, with Probe ID
as the deterministic tie-break. It retains the existing scout,
emergency-defender, gas-worker, and constructing-worker exclusions. v40
preserves that policy exactly and adds bounded public self-state telemetry for
only the first two accepted Gateway commands. No gameplay decision reads the
new telemetry.

The causal hypothesis is that choosing the nearest eligible builder removes the
slot-sensitive first-Gateway travel delay and lets the retained two-Gateway
opening produce two completed local defenders by early Zerg pressure, without
regressing v38 shared targeting, scaling, reserve, emergency, staging,
construction, commandability, or non-Zerg behavior.

## Fixed cohort

Run exactly the ten rows in `schedule.json` once with concurrency five, fresh
seeds 10101–10110, and a 120-second wall cap per game. The schedule keeps the
v19 maps, opponent identities, candidate slots, and two five-row waves. Stop
after two consecutive infrastructure-invalid completions or cohort completion.
Analysis begins only after the fixed cohort stops.

| Game | Opponent | Map | Kestrel slot | Seed |
| ---: | --- | --- | ---: | ---: |
| 1 | ZZZKBot | `sscai/(2)Benzene.scx` | P1 | 10101 |
| 2 | ZZZKBot | `sscai/(2)Destination.scx` | P2 | 10102 |
| 3 | UAlbertaBot-Terran | `sscai/(2)Destination.scx` | P1 | 10103 |
| 4 | UAlbertaBot-Protoss | `sscai/(2)Heartbreak Ridge.scx` | P2 | 10104 |
| 5 | McRave-9Pool-treatment | `sscai/(4)Circuit Breaker.scx` | P1 | 10105 |
| 6 | ZZZKBot | `sscai/(4)Circuit Breaker.scx` | P1 | 10106 |
| 7 | ZZZKBot | `sscai/(2)Heartbreak Ridge.scx` | P2 | 10107 |
| 8 | UAlbertaBot-Terran | `sscai/(2)Destination.scx` | P2 | 10108 |
| 9 | UAlbertaBot-Protoss | `sscai/(2)Heartbreak Ridge.scx` | P1 | 10109 |
| 10 | Stardust-repaired | `sscai/(2)Benzene.scx` | P2 | 10110 |

The four ZZZKBot rows span all four existing maps and both Kestrel slots. The
six other rows retain the established opponent gradient and cover both slots
for each UAlberta race.

## Gateway-selection proof

Each observed first/second accepted Gateway selection must have aligned arrays
for frame, ordinal, builder ID, tile x/y, builder distance, eligible count,
minimum eligible distance, candidate count, and truncation flag. Flat candidate
ID, distance, and reason-code arrays must be partitioned by candidate counts.
Allowed reason codes are 0 eligible, 1 incomplete, 2 scout, 3 emergency
defender, 4 gas worker, and 5 constructing.

For every complete selection row, require no truncation; positive eligible
count; the selected builder present exactly once with reason 0; selected
distance equal to the minimum eligible distance; and selected ID equal to the
lowest ID among eligible candidates at that distance. Ordinals must be 1 and
2, frames ordered, and accepted Gateway build evidence must align with each
selection. Any contradiction, malformed trace, truncation, illegal exclusion,
or nearest/tie-break failure is a treatment regression and `REJECT`. Fewer
than three ZZZK lanes with two complete selection rows is `INCONCLUSIVE`.

## Opening, strength, and retained gates

A qualifying ZZZK lane is an integrity-valid terminal with a publicly observed
non-worker, ground, attack-capable enemy inside the established home radius.
`ADOPT` requires at least three qualifying ZZZK lanes including both Kestrel
slots. Every qualifying lane must have the second Gateway current before its
first qualifying threat and at least two completed combat units both globally
and inside the home radius at that frame. Any observed miss is `REJECT`.

`ADOPT` also requires all ten rows to be integrity-valid short terminals, at
least two verified Kestrel wins overall, and at least one ZZZKBot win. Require
valid shared-target opportunity plus an accepted coordinated command in at
least eight games; zero shared-target rejects or illegal selections; at least
three Singularity-Charge-eligible lanes; and accepted and completed range in
at least two. Every observed v38 construction, reserve, emergency episode,
staged-offense, cap, public-information, commandability, and non-Zerg gate must
pass. Command rejection must remain below five percent per game and cohort,
with zero gas-worker build attempts and zero build `Unit_Busy` rejects.

`REJECT` applies when all ten rows are valid and a fixed ADOPT condition fails,
or whenever an observed gameplay, treatment, or retained-policy regression
occurs. `INCONCLUSIVE` applies when missing integrity, parser, provenance,
telemetry, or qualifying-mechanism evidence prevents a decision. A timeout or
infrastructure failure is invalid, remains in the fixed denominator, and is
never replaced. A decisive observed regression still requires `REJECT` even if
a separate row is invalid.

## Integrity and frozen identity

Every valid row requires reciprocal terminal results, expected race/map/slot/
seed, both launcher return codes zero, exactly two archived replay copies,
matching source/archive hashes and sizes, full `screp` parsing, expected race
headers, and `replay_header_frames + 1 == owning_callback_frame`. Candidate,
opponents, engine, launcher, sidecars, scripts, maps, runtime game data, and
provenance must match `schedule.json`. The canonical Kestrel v13 Elo anchor
stays unchanged regardless of this result.
