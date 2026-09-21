# Kestrel Modular v1 latency-instrumented Elo screen result

The five preregistered rows ran once, concurrently, on 21 September 2026.
All five produced clean reciprocal terminal outcomes, and Kestrel lost all five.
The nominal Wilson 95% interval for its observed win rate is 0–43.4%. This is
a small exact-build screen, so the interval is wide and the result is not a
tournament-strength claim.

| Opponent | Map | Result | Candidate callback frames | Durable frames/s | Army peak | Commands / rejected |
| --- | --- | --- | ---: | ---: | --- | ---: |
| ZZZKBot | Benzene | Loss | 5,924 | 665.89 | 3 Zealots | 55 / 0 |
| McRave memo fork | Circuit Breaker | Loss | 18,417 | 247.75 | 13 Zealots | 586 / 0 |
| UAlbertaBot-Protoss | Heartbreak Ridge | Loss | 12,682 | 992.88 | 6 Zealots, 4 Dragoons | 361 / 0 |
| ZZZKBot | Destination | Loss | 5,273 | 647.78 | 3 Zealots | 40 / 0 |
| UAlbertaBot-Protoss | Benzene | Loss | 19,285 | 1,193.90 | 10 Zealots, 10 Dragoons | 1,439 / 0 |

Every row matched its frozen map, seed, slot, candidate and opponent module,
engine, launcher and empty learning-state identity. Both players reported
latency 3. All ten source and archive replay copies hash-match, parse completely
with `screp`, identify the expected races, and align their header and callback
frames. The McRave row ran at 247.75 durable logical frames/s, below the
project's 384 frames/s throughput convention; this is a runtime anomaly, not a
result exclusion.

The generic telemetry scorecard passed its schema and mechanism gates in every
row. The replay auditor passed all integrity evidence. Its Zerg policy check
reported unmatched later hold-epoch attacks in the two ZZZK rows: one
`AttackMove` and seven `Attack1` frames on Benzene, and eight `Attack1` frames
on Destination. The auditor cannot join replay-local unit tags to BWAPI unit
IDs, and the reported frames occur in later active hold intervals after the
first release. These are preserved as mechanism-review findings; they do not
alter the replay-integrity or match-validity decision.

## Decision

The latency instrumentation is accepted: it preserved exact gameplay identity,
reported LF3 in all five rows, and introduced no command or lifecycle failure.
All five valid losses are admitted to the reviewed exact-build local
Bradley–Terry graph. The rating remains explicitly local, prior-sensitive and
uncertain.

The composed architecture is retained. Its ten explicit systems now separate
world state, memory, strategy, workers, production, construction, scouting,
squads, command arbitration and telemetry across 27 source files. The result
also makes the next work concrete. The next bounded hill-climb should test:

1. earlier survival reactions to rushes before the third Zealot;
2. worker recovery and expansion after the Zerg four-worker opening;
3. production scaling that completes rather than merely accepts later Gateways;
4. army composition and engagement timing against Protoss; and
5. replay-grounded threat and combat telemetry for those decisions.

## Durable evidence

- Batch manifest SHA-256:
  `446151911bd148dcb3a273d0fa03ec049f85147d9892d0c320335cf8a9e04fb3`.
- Match-manifest SHA-256 values, in schedule order:
  `60e3ba35f20f95bcb8a5231e541418af555d27f1658b6277846b59fdd10e662b`,
  `ffd40cf222e87e35a1cb5039cf3e47f8c18a843f5825d34bd486e68e96b21647`,
  `abb6cf0bbf4f7c5491c4fd472182977e77db27ec60b06decf6e82e545c54c333`,
  `f5a03ed00a04c9613c9eeef12c1b83a0006063ec5c1df025a2d4b3c3f0651c9d`,
  and `8a620a4caaee9aad6b62a3ebe3afcae3dc8a45bbf4601607f366014f03b865c1`.
- Candidate module SHA-256:
  `eab694b547a16d954708950f944005fa75a73995452130c6927c5effb8f602eb`.
- Candidate source-manifest SHA-256:
  `711f7bbc49466a0e1fe3fd2d389f57da0fffe9e446a15c12296ceb2b0087b627`.
