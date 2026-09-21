# Kestrel Modular v1 gather-commandability recovery result

Date: 2026-09-21  
Decision: **REJECT**

The one registered Benzene row ran exactly once on fresh seed 12401. The
worker fix succeeded at its direct target: all 14 issued gather commands were
accepted, while seven uncommandable assignments were stopped by public BWAPI
preflight and cargo returns were preserved. The candidate still issued one
build command that BWAPI rejected as `Unit_Busy`, and it never observed two
completed Zealots at once. Both conditions fail frozen semantic gates, so the
registered decision is **REJECT**. The row is not retried and does not enter
local Elo.

## Frozen identity and run

- Candidate binary SHA-256:
  `8758914724960797e48c30c5e73885571c08e8a96fd432e7ee8b0b62d7e70e36`
- Candidate source-manifest SHA-256:
  `16d857585753b2379800880e818d0a19c60f2230041db8c477da817afcf0013f`
- Plan SHA-256:
  `3022345cb37b10cc96112ba67725a0774e0995bf24eaca9c33caf74db503cdcf`
- Schedule SHA-256:
  `c83c06ba0562883a3eba38752026e60fe415b6503ffc1590f8102002839940d4`
- Run ID: `20260921T011400-20158638681c`
- Final manifest SHA-256:
  `98ae6a6a460bf3468e15d58f2b417174d269a54fb4bd203efb785d481c879ae4`
- Batch manifest SHA-256:
  `8760ae59f7f6c6a1af2f47306c8c4699d2e88a0b549805e1f62d7c6c0ebd53fe`
- Candidate diagnostic SHA-256:
  `f334496b6614d140fcd3d21a0835f4825db63b57bd51a3767ce95bbaa05e6148`

Kestrel Modular v1 is **Ours / Original**, author Luke Cameron. ZZZKBot is
**Ours / Port**, original author Chris Coxe, with source at
<https://github.com/chriscoxe/ZZZKBot>. The candidate lost at callback frame
5,366; ZZZKBot won at callback frame 5,397. Both children exited zero. The
game completed in 2.48 seconds at 2,176 logical frames per wall second, with
per-process peak RSS of approximately 43.9 and 44.2 MB.

## Independent integrity review

All 21 audited frozen hashes match the registered schedule. The candidate,
opponent, engine, launcher, sidecars, source manifest, required files, game
data, map, slot, and seed are exact. The two source replay files and their
archived copies match their recorded hashes and sizes:

| Owner | Bytes | Replay SHA-256 | Header frame | Callback frame |
| --- | ---: | --- | ---: | ---: |
| Kestrel Modular v1 / P1 | 67,938 | `eeb1da5e6dbdf5de29bbae09dc286980d5b319dc7189befbcb082f384dc6e571` | 5,365 | 5,366 |
| ZZZKBot / P2 | 68,161 | `42d8f1eed93b9e357b1cdcd31758bf73f21858701e099231f06bb33d17bc89d9` | 5,396 | 5,397 |

Both replay copies parse completely with `screp`, report the expected races,
have no command parse errors, and satisfy
`header frame + 1 == owning callback frame`. The logs contain exactly the two
registered terminal-drain events, `transport_callback/-1` and
`controller_not_occupied_after_action/87`, with no sync mismatch.

## Recovery and retained-system evidence

Gather accounting reconciles exactly: 14 attempts, zero rejections, and 14
accepted assignments. The allocator recorded seven `canGather(target)`
preflight skips and 853 cargo deferrals. These are avoided requests, not
issued commands. The direct failure from the first smoke is fixed in this
row.

The four-Probe Pylon was accepted at frame 414 and completed at 1,035 with
exactly four completed Probes. The first and second Gateways were accepted at
1,188 and 2,151 and completed at 2,249 and 3,209. Both Zealot trains were
accepted, the second at 3,447, but two completed Zealots were never observed
at the same time. Two later Probe trains were accepted at 3,750 and 4,059.
Reserve telemetry contains 674 active samples and 671 genuine blocks.

The candidate attempted 29 commands: build 4/1 rejected, train 4/0, gather
14/0, attack 7/0, and scout 0/0. The sole error was build-category
`Unit_Busy`. Three accepted build commands appear in the replay and match the
three ordered construction events. The preserved trace does not record the
rejected attempt's frame, worker ID, intended structure, or unit state; no
narrower causal claim is supported.

## Next experiment

The next isolated change should move exact builder eligibility into
`WorkerAllocator`: preserve cargo returns, evaluate `canBuild(type, tile)` for
each role-eligible Probe, and select the nearest eligible Probe with unit ID
as a deterministic tie-breaker. Telemetry should distinguish build preflight
skips and cargo deferrals from issued build commands. A new candidate then
requires its own frozen one-row Zerg smoke on a fresh seed and map. The base
modular and gather-recovery scorers remain required, including the
second-completed-Zealot gate.

This is diagnostic Apple Silicon OpenBW evidence from one short loss. It does
not measure playing strength, establish local Elo, validate replay playback,
or verify the official Win32 BWAPI runtime.
