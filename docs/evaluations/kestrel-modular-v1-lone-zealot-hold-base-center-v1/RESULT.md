# Kestrel Modular v1 base-center lone-Zealot hold result

Date: 2026-09-21
Decision: **INCONCLUSIVE**

The one registered Heartbreak Ridge row ran exactly once on fresh seed 12404.
Both OpenBW children exited before frame zero because the restricted execution
context could not bind the local Unix transport. Neither bot loaded far enough
to emit metadata or a replay. The frozen infrastructure-invalid rule therefore
applies. The row is preserved without retry, replacement, or reinterpretation;
the base-center mechanism remains untested and does not advance to the
five-game screen or local Elo.

## Frozen identity and attempt

- Candidate binary SHA-256:
  `4f840d64291cec481fd2a8b8ce09ab9a5e9eb85ea70da159a84c92bba19fcf5a`
- Candidate source-manifest SHA-256:
  `ba03c138618c3289d815f91ee84b2d1bde70836c012c06cf58614050b3f9ef52`
- Candidate build-sidecar SHA-256:
  `47b2a1cd5780f048f4aabf5d467ec4153f50ef4fa76f94b62d99731e07eaf443`
- Plan SHA-256:
  `921699a2b849a35f08c30c55de32f95501c49741c33dae53a416d1ce54e27fee`
- Source and persisted schedule SHA-256:
  `dce3cac3351424262f8bf1864615fe75e79d64215e433dbfb529fcbff41892bf`
- Run ID: `20260921T024505-382cb4682f1f`
- Match manifest SHA-256:
  `81cdcf5e769d64583c367db30dd9a4d9e48512ade3e6884091e3e81210f93bb9`
- Experiment manifest SHA-256:
  `4c9c037f1b4b4f8a8bb67c5d0a0898e8d66366326acd6d78bb012d6bf5d3bef8`

Kestrel Modular v1 is **Ours / Original**, author Luke Cameron. ZZZKBot is
**Ours / Port**, original author Chris Coxe, with source at
<https://github.com/chriscoxe/ZZZKBot>. The attempt used the exact registered
candidate as player 1 and ZZZKBot as player 2, Heartbreak Ridge, seed 12404,
LF3, empty isolated learning state, and the registered engine, launcher, map,
game data, sidecars, and source identities.

## Failure evidence

The attempt lasted 0.21 seconds. Both children returned zero, but neither
reported a callback frame, terminal winner, bot diagnostic, or replay. Both
42-byte stdout logs contain exactly:

```text
Error: connect: No such file or directory
```

Each log has SHA-256
`1661e40660285eebbf8be536989727cb2f57b43c36a9aedc4dcbc7bf5b16d39d`;
both stderr logs are empty. The match manifest consequently records
`outcome_verified=false`, no logical frame count, no result, no replay, and
`replay_missing_reason` stating that the launcher produced no `.rep` file.
The batch classifies the row as `missing_or_inconsistent_metadata` and scores
zero games.

The real CLI failure was reproduced without launching another game. In the
same restricted execution context, a minimal Python `AF_UNIX` bind under an
otherwise writable `/tmp/scai-*` directory failed with `PermissionError:
[Errno 1] Operation not permitted`. The identical local bind probe succeeded
outside that restriction. OpenBW's `LOCAL` transport tries to bind or connect
the configured socket; when bind is denied and no peer can create the socket,
both launchers reach the preserved `connect` error. This diagnosis explains
the attempt without changing its registered classification.

The launcher should preflight the exact local socket capability before child
startup and report a clear launch error. Future engine runs must use an
execution context that permits local Unix sockets. This result does not permit
a retry of the frozen row. A future gameplay candidate must be separately
registered and materially distinct.

This is infrastructure evidence only. It provides no observation of the
base-center hold, no playing-strength evidence, no Elo update, no BASIL or
tournament claim, and no official Win32 BWAPI runtime validation.
