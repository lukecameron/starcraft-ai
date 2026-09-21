# Kestrel Modular v1 builder-commandability recovery result

Date: 2026-09-21  
Decision: **REJECT**

The one registered Circuit Breaker row ran exactly once on fresh seed 12402.
The builder fix succeeded at its direct target: all three issued build commands
were accepted, every accepted build has one ordered construction event, and
the allocator preserved three cargo returns without issuing an invalid build.
Gather recovery also held with 18 accepted assignments and zero command
rejections. The candidate still never observed two completed Zealots at once,
so the frozen retained-system gate fails. The row is not retried and does not
advance to the five-game screen or local Elo.

## Frozen identity and run

- Candidate binary SHA-256:
  `8f211a0f9bd1b548083af65a0da555d4f1212cf7a7ea289c7eff857a6f803937`
- Candidate source-manifest SHA-256:
  `e68b98082ed55110eec26fa3cad3abbaf95dba7891156fcd50b342506e2727d1`
- Plan SHA-256:
  `ab0d9ddee8486e2dba13a47d18f09374deffecf0747f903f9ea5130c6d7731c1`
- Schedule SHA-256:
  `a32fe613697380106d31281c6415a7b30b1645a850febc540cb5e95e4a6ccc58`
- Run ID: `20260921T015644-43ac45297fb5`
- Run/final manifest SHA-256:
  `89d62ba715b669711b6dc69869a0e3deddf84462a29a21c8e9e2f6fe02fea408`
- Experiment manifest SHA-256:
  `1607e95d90c382ab4984c5b35e07e88d0f166bb024fc0a4f595822360f6126f1`
- Candidate diagnostic SHA-256:
  `81d0f979f21a9c65670fa4f1ea77e5b8be9b74c763a45ddd5805280442482782`

Kestrel Modular v1 is **Ours / Original**, author Luke Cameron. ZZZKBot is
**Ours / Port**, original author Chris Coxe, with source at
<https://github.com/chriscoxe/ZZZKBot>. Kestrel lost at callback frame 5,304;
ZZZKBot won at callback frame 5,335. Both children exited zero. The game
completed durably in 1.96 seconds at about 2,725 logical frames per wall
second. Candidate and opponent peak RSS were approximately 44.0 and 44.5 MB.

## Independent integrity review

The registered plan, schedule, candidate, opponent, launcher, engine, map,
game data, sidecars, source manifests, slot, race, and seed all match their
frozen hashes. The two source replay files and their archived copies are
byte-identical:

| Owner | Bytes | Replay SHA-256 | Header frame | Callback frame |
| --- | ---: | --- | ---: | ---: |
| Kestrel Modular v1 / P1 | 69,191 | `52d0dfb67cab7a706229b5f6fbdded86b7a56c968e3f0e0f808b85a1d4902eef` | 5,303 | 5,304 |
| ZZZKBot / P2 | 69,261 | `4b5961e097d1cff48849622fe3280fcc28cf2db6f9bcac84e651c91205b3623a` | 5,334 | 5,335 |

All four source/archive parses exit zero with `screp`, report the expected
races, contain no command parse errors, and satisfy
`header frame + 1 == owning callback frame`. The logs contain only the two
registered terminal-drain events, `transport_callback/-1` and
`controller_not_occupied_after_action/87`, with no sync mismatch. This is
full parser validation, not replay playback validation.

## Recovery and retained-system evidence

The candidate issued 32 commands: build 3/0 rejected, train 4/0, gather 18/0,
attack 7/0, and scout 0/0. `Unit_Busy` remained zero. Gather accounting
reconciles exactly at 18 accepted of 18 issued, with nine public
`canGather(target)` preflight skips. Builder selection recorded three cargo
deferrals and no preflight skip; each accepted build maps to one ordered
construction event.

The four-Probe Pylon was accepted at frame 450 and completed at 1,068 with
four completed Probes. The first Gateway was accepted at 1,260 and completed
at 2,306. The second Gateway was accepted at 2,133 and completed at 3,208.
The replay records Zealot train commands at frames 2,639 and 3,212; telemetry
accepted the second at frame 3,210. Two completed Zealots were never observed
simultaneously, so both registered scorers are structurally complete but
return `mechanisms_pass=false` for that sole reason.

The timing does not support a simple late-second-train explanation. This row's
second train was earlier than the original Benzene smoke that did observe two
completed Zealots. The replay records a home attack-move at frame 3,245 and
target attacks at 3,500 and 3,590 before the second completion was observed.
Replay commands alone do not establish the first Zealot's death frame, so the
exact loss mechanism remains unproven. The next separately registered
candidate should isolate the previously positive v19 hold signal: against a
known Zerg opponent, suppress a lone first Zealot's target attacks and move it
home until a second completed Zealot exists. Worker, builder, construction,
production, scouting, resource-reserve, and post-release combat logic remain
unchanged.

This is diagnostic Apple Silicon OpenBW evidence from one short loss. It does
not measure playing strength, establish local Elo, validate replay playback,
or verify the official Win32 BWAPI runtime.
