# Kestrel hill-climb v21 result

Date: 2026-09-21  
Decision: **REJECT**

The fixed five-game screen of `Kestrel-v41-zerg-two-gateway-bank` completed
without retries, reseeds, replacements, or reruns. All five games are valid
short terminals, with two wins and three losses. The treatment remained
Zerg-only and all retained diagnostics passed, but both primary P2 ZZZK lanes
still had only one completed global and local defender at first qualifying
pressure. The registered gate requires two in both lanes, so v41 does not
advance and Elo remains unchanged.

## Frozen identity and evidence

The registered plan SHA-256 is
`00cb18186a8fbb52c159f7cbff4cfdefabae72a9b2b05d9d25ade59987cae849`.
The committed source schedule SHA-256 is
`c9e8a9b88a793b6ea0afef7e8eadfbffebb59bf65067e2e16403afbe48260d6d`;
the runner-persisted canonical schedule SHA-256 is
`891ac80754a12ad4c7a62fdeb4d69e2aa9e0ddfaf1a85917ac5a9ddca07b1c09`.
The experiment manifest SHA-256 is
`789dc4a1ff0c9227a2be97b53c1fcbad92a9452d344d4b906bb3a80b0c302367`,
and the independently generated scorecard SHA-256 is
`eebe508201f08d48694f4863c986cee67b7b4285f3ba1d3d0bb017566587d67c`.

The candidate binary SHA-256 is
`2e39f690e1ec598dd03d0bbfe35de75f282ab626d7b6b0c135a6fb9947ed984d`,
source SHA-256
`fec0f4f6c1a1a37924827be427fabe9ce695cad84ef17f5bde23e77d754218ad`,
combined source SHA-256
`a6d9a19debf32131aabb16b57f6726e09c9312917be83e25362e2aeafa340d3a`,
and patch SHA-256
`446a560f4aab5c4bb167118ee82bd2fe7bb41702ef7b7c415a853eb25466ae07`.
Kestrel is **Ours / Original**, author Luke Cameron, with source at
[lukecameron/starcraft-ai](https://github.com/lukecameron/starcraft-ai/tree/main/bots/kestrel).
The schedule identifies ZZZKBot as **Ours / Port**, author Chris Coxe;
McRave as **Ours / Fork**, author Christian McCrave; and UAlbertaBot as
**Ours / Port**, author David Churchill. It freezes their source links,
binaries, and build sidecars.

## Run-by-run result

| Game | Run ID | Opponent | Map | Slot | Result | Candidate frame | Durable fps |
| ---: | --- | --- | --- | ---: | --- | ---: | ---: |
| 1 | `20260920T205151-05ea8962d510` | ZZZKBot | Destination | P2 | Loss | 6,017 | 2,535.9 |
| 2 | `20260920T205151-125a9dd54ec6` | ZZZKBot | Heartbreak Ridge | P2 | Win | 12,000 | 3,027.0 |
| 3 | `20260920T205151-7bdec05a70ef` | ZZZKBot | Benzene | P1 | Win | 11,907 | 3,092.6 |
| 4 | `20260920T205151-edfea79dc797` | McRave-9Pool-treatment | Circuit Breaker | P1 | Loss | 16,371 | 466.5 |
| 5 | `20260920T205151-b040256742bf` | UAlbertaBot-Terran | Destination | P1 | Loss | 11,814 | 2,405.0 |

The descriptive record is 2-3 overall and 2-1 against ZZZKBot. This mixed
five-game diagnostic is not an Elo estimate.

## Integrity and retained gates

All five match manifests have reciprocal verified terminal results and zero
launcher exits. The ten archived replay copies match their recorded hashes and
sizes, parse fully with `screp`, contain the scheduled race pair, have no replay
command parse errors, and satisfy
`replay_header_frames + 1 == owning_callback_frame`. The only observed kill
events are the two reviewed clean terminal-drain paths. All candidate and
opponent binaries, build sidecars, launcher, engine, scripts, maps, MPQs, and
provenance matched the frozen schedule.

All five games exceeded 384 durable logical frames per wall second. All ten
first/second Gateway builder selections passed the v40 nearest-distance and
lowest-ID proof with no truncation. Construction traces passed in all five
games. All 1,300 shared-target attempts were accepted, including 222
coordinated selections, with zero shared-target rejects or illegal selections.
All observed reserve, emergency, staged-offense, scaling, cap,
public-information, and commandability checks passed. There were zero rejected
candidate commands, zero gas-worker build attempts, and zero build
`Unit_Busy` rejects.

The treatment counter was positive in all four Zerg games: 35, 48, 39, and 54
cadence passes. The Terran sentinel reported zero treatment frames, zero
opening reserve, and no Zerg-only state. This proves treatment scope, but not a
useful economic intervention.

## Opening analysis

| Scenario | Build | Pylon accepted | Gateway 1 current | Gateway 2 accepted/current/completed | Zealot 1 completed | Threat | Global/local defenders |
| --- | --- | ---: | ---: | --- | ---: | ---: | --- |
| Destination P2 | v40 | 864 | 1,509 | 2,004 / 2,084 / 3,055 | 3,089 | 3,560 | 1 / 1 |
| Destination P2 | v41 | 822 | 1,524 | 1,998 / 2,132 / 3,103 | 3,101 | 3,538 | 1 / 1 |
| Heartbreak P2 | v40 | 804 | 1,506 | 1,992 / 2,082 / 3,053 | 3,083 | 3,551 | 1 / 1 |
| Heartbreak P2 | v41 | 846 | 1,588 | 2,040 / 2,168 / 3,139 | 3,167 | 3,591 | 1 / 1 |
| Benzene P1 | v40 | 828 | 1,492 | 1,968 / 2,055 / 3,026 | 3,071 | 3,725 | 2 / 2 |
| Benzene P1 | v41 | 810 | 1,580 | 1,902 / 2,034 / 3,005 | 3,161 | 3,778 | 2 / 2 |

The seeds differ, so these are descriptive matched map/slot comparisons rather
than paired independent trials. They show no repair: Destination's second
Gateway became current 48 frames later than v40, Heartbreak's 86 frames later,
and only Benzene improved by 21 frames. Both primary lanes remained one
defender short.

The more direct mechanism result is stronger. Each Zerg run already queued two
Probes before the first Pylon, and three of four Zerg runs recorded zero
existing reserve-block opportunities. v41's new policy became active only
after the Probe queue decisions it was meant to change. Benzene's seven
reserve blocks occurred later in the retained post-Pylon reserve window. Thus
v41 usually changed a policy value without suppressing a Probe train; the
result is a null intervention rather than evidence that a 50-mineral saving is
insufficient.

Destination lost shortly after pressure: first threat at frame 3,538, one
local Zealot, first home Zealot loss at 4,158, and terminal frame 6,017.
Heartbreak also had one local Zealot at frame 3,591 and lost it at 3,830, but
later recovered and won. Benzene had two local defenders at frame 3,778 and
retained the passing win. McRave reached three local defenders by its later
frame-4,469 pressure and survived competitively to frame 16,371 before losing.
The Terran sentinel had no treatment leakage and ended as a later partial loss;
it supplies no evidence for the Zerg opening repair.

## Ranked next changes

1. Test a coherent five-Probe Pylon opening against known Zerg: activate the
   reserve after the first trained Probe completes and allow the first Pylon at
   five completed Probes. This is the simplest change that actually skips the
   second queued Probe and should move the complete two-Gateway chain earlier.
2. If that is too economically costly, optimize Gateway tile and builder as one
   choice. v21 still sent the second builder 424-552 pixels, leaving 104-132
   frames between build acceptance and current state on the Zerg lanes.
3. After production reaches two defenders on time, hold the first Zealot near
   home until the second is complete or a public local threat requires it; this
   addresses location without confusing it with the current unit-count miss.
4. For the longer McRave loss, separately analyze post-opening army composition
   and engagement control. Its three-defender opening passed, so changing the
   rush timing for that loss would target the wrong phase.

The next experiment should isolate item 1 first. v41 is rejected, the canonical
Kestrel v13 remains unchanged, and no v21 result enters local Elo.
