# Kestrel Modular v1 close-threat defense result

Date: 2026-09-21
Decision: **REJECT**

The one registered Heartbreak Ridge row ran exactly once on fresh seed 12405.
It was infrastructure-valid and exercised the new defense: the hold observed
143 close-threat samples and issued 15 accepted direct attacks, all visible in
the replay at the expected LF3 offset. The first held Zealot still disappeared
123 frames before the second held Zealot was first observed. Two completed
Zealots never coexisted and the hold never released, so the frozen overlap and
release gates fail. The row does not advance to the five-game screen or local
Elo.

## Frozen identity and run

- Candidate binary SHA-256:
  `dbd9b204cb65da112e4d1994f6b6bd15fbd12be97db2bb2b7b64a4a82ee11bdf`
- Candidate source-manifest SHA-256:
  `1456d91bf1f3529a246a7dd0d87fdeacaaf2d72a49e2029c2396d778a96f29d3`
- Candidate build-sidecar SHA-256:
  `b820ae777131b5ec4048c0bd414a1242ab2e04d9d676b3298e77e9d6d2d4cce6`
- Plan SHA-256:
  `83bd6c578807c3ed35fd2b487142c668f713e033c624d921609c1a9920f1e45e`
- Source and persisted schedule SHA-256:
  `055d45cc1d7906fa9dd1b33e1f3859e0fc22122f4c8962d080c31472ed7c5e81`
- Run ID: `20260921T031906-e09a379a5cab`
- Run/final manifest SHA-256:
  `b3f39fc728d5d7af36b4135480c9505e239f4d8bf29d37ec11eb0f50bb8b19f2`
- Experiment manifest SHA-256:
  `5f4326dbbd8c21cde73aa5a041cecd8fb0c7e612cefce9ff3f02a03946731c5e`
- Candidate diagnostic SHA-256:
  `0f9ddb419be68057a2f5357c496dd7af70f43a6f18ae2da06efff0144dcf4708`

Kestrel Modular v1 is **Ours / Original**, author Luke Cameron. ZZZKBot is
**Ours / Port**, original author Chris Coxe, with source at
<https://github.com/chriscoxe/ZZZKBot>. ZZZKBot won at callback frame 5,366;
Kestrel lost at callback frame 5,335. Both children exited zero. The game ran
at about 2,224 logical frames per wall second; candidate peak RSS was
44,662,784 bytes and maximum callback time was 2.02 ms.

## Independent integrity review

The plan, schedule, candidate, opponent, launcher, engine, map, game data,
sidecars, source manifests, slot, race and seed match their frozen identities.
The only kill events are the registered terminal-drain events
`controller_not_occupied_after_action/87` and `transport_callback/-1`; no sync
hash mismatch occurred.

The source and archived replay copies are byte-identical and all four complete
`screp` parses exited zero with expected races and no parse-error commands:

| Owner | Bytes | Replay SHA-256 | Header frame | Callback frame |
| --- | ---: | --- | ---: | ---: |
| ZZZKBot / P1 | 65,764 | `4f43a83c08eda8f1c413ab7ea57babf38b5a57928f65492d6f6eeda688f4c673` | 5,365 | 5,366 |
| Kestrel Modular v1 / P2 | 65,463 | `3276a30c9d71a5f0d6591b96c10d8f317a07ae28e9270f4f4f9cdc65eaacdcd6` | 5,334 | 5,335 |

Each replay satisfies `header frame + 1 == owning callback frame`.

## Mechanism evidence

The candidate issued 41 commands with zero rejection and zero `Unit_Busy`:
build 3, train 4, gather 18, attack 15 and scout 1. The four-Probe Pylon and
both resource reserves passed. Construction events were ordered: Pylon
`387→477→998`, first Gateway `1260→1353→2324`, and second Gateway
`2073→2198→3169`. Gather and construction accounting reconciled.

The known-Zerg hold was active for 234 samples and affected two distinct
completed Zealots. Its 256-pixel close-threat rule recorded 143 samples and 15
actual attack attempts, all accepted. Every event, array, position, unit/target
ID and per-held-unit lifecycle counter reconciled. The one accepted retreat
move targeted the calculated base center `(3808,1840)`; none targeted the old
top-left coordinate.

The owner-filtered replay contains one candidate `Move` at frame 3,320 to the
base center, no `AttackMove`, and exactly 15 `Attack1` commands. Their replay
frames are every accepted telemetry event frame plus two:

```text
3593 3620 3632 3692 3845 3941 3950 3953
3962 3974 3983 4016 4049 4052 4106
```

Replay target coordinates match telemetry. Replay unit tags cannot be mapped
reliably to BWAPI telemetry IDs, so the registered identity sub-gate is
recorded as unsupported; the mandatory frame, order and position checks pass.

All three scorers are structurally complete. Their sole retained-system
failure is the missing second completed Zealot; the hold scorer also reports
the missing release. The first held unit's lifecycle spans frames 3,318–3,720
with 44 close-threat samples and four accepted attacks. The second spans
3,843–4,137 with 99 samples and 11 accepted attacks. The disjoint ranges prove
that the required overlap was absent. The second Zealot train was accepted at
frame 3,237, but completion was never observed; release remained `-1`.

This valid exercised loss shows that legal local engagement makes the held
defender active and auditable, but does not preserve it long enough to create
overlap against this pressure. It is one diagnostic Apple Silicon OpenBW row,
not playing-strength, BASIL, tournament, replay-playback, or official Win32
runtime evidence.
