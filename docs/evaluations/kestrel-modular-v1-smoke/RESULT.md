# Kestrel Modular v1 lifecycle smoke result

Date: 2026-09-21  
Decision: **REJECT**

The one registered Benzene row ran exactly once, with Kestrel Modular v1 as
player 1 and ZZZKBot as player 2. The engine lifecycle, replay integrity, and
registered opening semantics all passed. The candidate issued 32 gather
commands and BWAPI rejected 10 of them with `Unit_Busy`, so the registered
zero-rejection gate failed. This valid row therefore forces **REJECT**. It is
not retried and does not enter local Elo.

## Frozen identity and run

- Candidate binary SHA-256:
  `8134235c5ce2c589e5b6c890008cc9a2a086df7a715ddcdacfeef4aa5bd36cca`
- Candidate source-manifest SHA-256:
  `4f848a72d4086badc400ce1ec2be61d4663f2cf1823577c40de1b436fab94f67`
- Plan SHA-256:
  `e3cf963d355a6c787a5c78362efd9859353e727fc7b9243f9a45152263b0be68`
- Schedule SHA-256:
  `2d6837ab5bdba94fb4cbbead8e150d8c1d1dd0980bd05d4701c9ec2965e83add`
- Run ID: `20260921T005435-f2ca7d9e0921`
- Final manifest SHA-256:
  `038f092a6581d7de802f9ce02ad76d2e3daf06002f5d6e8e13fd193e067f40e4`
- Candidate diagnostic SHA-256:
  `f7ee31659e3bde74b99e683961143fb251589359029ae703191ff3507fc0835e`

Kestrel Modular v1 is **Ours / Original**, author Luke Cameron. ZZZKBot is
**Ours / Port**, original author Chris Coxe, with source at
<https://github.com/chriscoxe/ZZZKBot>. The candidate lost at callback frame
5,366; ZZZKBot won at callback frame 5,397. Both children exited zero. The
game completed in 2.35 seconds at 2,298 logical frames per wall second, with
per-process peak RSS of approximately 43.8 and 44.1 MB.

## Independent integrity review

The candidate, opponent, engine, launcher, sidecars, source manifest,
required files, game data, map, slot, and seed all match the frozen schedule.
The two source replay files and their archived copies are byte-identical to
their recorded hashes and sizes:

| Owner | Bytes | Replay SHA-256 | Header frame | Callback frame |
| --- | ---: | --- | ---: | ---: |
| Kestrel Modular v1 / P1 | 68,476 | `0fdef870ffc3c2e25a0747fbb735d1885dcdfe1ba6de5c88faf8ec6d7a830e05` | 5,365 | 5,366 |
| ZZZKBot / P2 | 68,758 | `2cd4357bf62c03a030ade39f8877317ab08d91e7e2ab612da025de926666f4e6` | 5,396 | 5,397 |

All four source/archive copies parse completely with `screp`, report the
registered Protoss/Zerg races, have no command parse errors, and satisfy
`header frame + 1 == owning callback frame`. The logs contain exactly the two
registered terminal-drain events, `transport_callback/-1` and
`controller_not_occupied_after_action/87`, with no sync mismatch.

## System evidence

The composed systems executed through the real engine lifecycle. Telemetry
ended cleanly with 1,789 sampled callbacks, 47 attempted commands, and a
2.223 ms maximum sampled callback. The opening and construction trace showed:

- the first Pylon accepted at frame 423 with exactly four completed Probes,
  observed current at 513, and completed at 1,033;
- the first Gateway accepted at 1,251 and completed at 2,364;
- the second Gateway accepted at 2,094 and completed at 3,190;
- two accepted Zealot trains, four later Probe trains, a maximum of seven
  Probes, two Gateways, and two Zealots; and
- 611 reserve-active samples and 609 genuine reserve blocks, including the
  order-aware second-Zealot boundary.

The registered scorer reports `complete=true` with no structural issues, but
`mechanisms_pass=false` because commands were rejected. Command accounting is
internally consistent: build 3/0 rejected, train 6/0, gather 32/10, attack
6/0, and scout 0/0.

## Diagnosis and next experiment

`WorkerAllocator` attempts a new gather command whenever a Probe is not
reported as gathering the target resource. That includes short states in
which the worker is not interruptible, such as a just-completed construction
transition, so BWAPI rejects the command as `Unit_Busy`. A recovery candidate
should preserve carrying workers' return trips and use BWAPI's public
`canGather(target)` commandability check immediately before issuing a new
assignment. It must receive a new binary hash and a separately preregistered
one-row recovery smoke; this rejected row remains closed.

This is diagnostic Apple Silicon OpenBW evidence from one short loss. It does
not measure playing strength, establish local Elo, validate replay playback,
or verify the official Win32 BWAPI runtime.
