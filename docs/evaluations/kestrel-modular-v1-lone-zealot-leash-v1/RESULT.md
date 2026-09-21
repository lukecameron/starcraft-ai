# Kestrel Modular v1 lone-Zealot leash result

Date: 2026-09-21
Decision: **INCONCLUSIVE**

The one registered Heartbreak Ridge row was invoked exactly once on fresh seed
12406 during preregistration audit. The match runner's AF_UNIX capability
preflight failed in the restricted execution context before either OpenBW child
started. No player process, callback, bot diagnostic, or replay was produced.
The frozen infrastructure-invalid rule therefore applies. This row is
preserved without retry, replacement, or reinterpretation; the 96-pixel leash
mechanism remains untested and does not advance to the five-game screen or
local Elo.

## Frozen identity and attempt

- Candidate binary SHA-256:
  `1734fcfa4542eff24c7341f43b226cb6eb03d4fd68a120beb1a0f406160f7818`
- Candidate source-manifest SHA-256:
  `112b0f545b3b8b871cb86d166ec33c12fcd0583820d6fd5ebbd956d191875ccf`
- Candidate build-sidecar SHA-256:
  `7cab62ed82405a5bb413c28c85d5ab0b272b44cadc4fddc3353ef7f05e8bbd7a`
- Registration commit: `daef4ea065c21da7f2c925e91d1184a4a027d499`
- Plan SHA-256:
  `e26ad61b9169ff0e68f19b17b87b85fd853c2f9f6c8164e83d051e92f6b7ec11`
- Source and persisted schedule SHA-256:
  `c97137e2b6270f8ec70d63c288486ff48ede9d4de9d98a2b22b250e2986cb1a8`
- Run ID: `20260921T034831-7eff42c20fee`
- Match/root manifest SHA-256:
  `bbec0fc9a46ed055dae3517fc6c780d570b7609ad5109c03cf09dee294c908c2`
- Experiment manifest SHA-256:
  `7f20b9b34df22633e359c9c9f3bdc46bc9fa322f3172aab202ae0b9368ce16cc`

Kestrel Modular v1 is **Ours / Original**, author Luke Cameron. ZZZKBot is
**Ours / Port**, original author Chris Coxe, with source at
<https://github.com/chriscoxe/ZZZKBot>. The attempt used the exact registered
candidate as player 2 and ZZZKBot as player 1, Heartbreak Ridge, seed 12406,
LF3, empty isolated learning state, and the registered engine, launcher, map,
game data, sidecars, and source identities.

## Failure evidence

The attempt lasted 0.11 seconds. `run_match.py` failed its exact socket
preflight with:

```text
OSError: OpenBW AF_UNIX socket preflight failed for /tmp/scai-t2r4xoqe/game.socket: [Errno 1] Operation not permitted
```

The match manifest records `termination_reason: launch_error`, an empty
`players` array, no callback frame, no result, and no replay. The batch
classifies the row as `launcher_failure` and scores zero games. The runner
stdout is only the durable match-manifest path (97 bytes, SHA-256
`1db22b445313e99fa837a9154e6276eff65e276b2ae66525b281476cfb292c9e`);
stderr is empty. This is the preflight's intended behavior: it prevents the
misleading dual-client connect failure seen in the earlier base-center row and
leaves an explicit durable cause without starting a child process.

The preregistration audit also found that the general telemetry scorers verify
structure and retained opening mechanisms but do not by themselves require
positive leash activity or validate replay commands. Any future materially
distinct candidate must register a candidate-specific mechanism scorer and a
durable replay-evaluation artifact before gameplay. That audit improvement does
not alter this attempt's frozen decision.

This is infrastructure evidence only. It provides no observation of the leash,
no playing-strength evidence, no Elo update, no BASIL or tournament claim, and
no official Win32 BWAPI runtime validation.
