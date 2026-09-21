# Kestrel Modular v1 builder-commandability recovery — NOT RUN

Registered 21 September 2026 before gameplay. The gather-commandability
recovery eliminated all gather rejections in its fixed row, but one of four
build commands returned BWAPI `Unit_Busy`. This second recovery changes only
builder eligibility and its telemetry. After the exact build tile is known,
`WorkerAllocator` preserves cargo returns, checks public BWAPI
`canBuild(type, tile)` for every role-eligible Probe, and selects the nearest
eligible Probe with unit ID as a deterministic tie-breaker. Opening,
production, construction intent, scouting, combat policy, and canonical
Kestrel v13 remain unchanged.

## Frozen identities

- Kestrel Modular v1 builder recovery, **Ours / Original**, author Luke
  Cameron: module SHA-256
  `8f211a0f9bd1b548083af65a0da555d4f1212cf7a7ea289c7eff857a6f803937`;
  sorted source-manifest SHA-256
  `e68b98082ed55110eec26fa3cad3abbaf95dba7891156fcd50b342506e2727d1`;
  build sidecar SHA-256
  `9fef3213c942eadc7c9aad6ad0d60eb9cf01e06e1008bc0bd0bc753666b3e8bd`.
- ZZZKBot Zerg, **Ours / Port**, original author Chris Coxe: module SHA-256
  `ce796a5d49d78121aaf42b57ba758423ee89f74a249b42180cbc0b0cb9df4748`;
  source revision `7183e37b6b416ea53c1040c83e639a3a3c395eed`; source
  <https://github.com/chriscoxe/ZZZKBot>.
- Terminal-drain OpenBW engine SHA-256
  `eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b`;
  launcher SHA-256
  `af1682393f9fe43afe885b35a1637e9c464719ef93c83e799d614beed20316c1`;
  LF3, macOS ARM64, fresh empty isolated learning state, no adjudication.

## Fixed row and stop rule

Run exactly one game on Circuit Breaker, seed 12402, with the builder-recovery
candidate as player 1 and ZZZKBot as player 2. Use a 120-second wall cap and
concurrency one. Do not retry, reseed, replace, or rerun the row for any
result. Preserve the manifest, diagnostics, logs, and both replay copies when
produced. No build, profiler, replay playback, or other engine experiment may
overlap the row.

## Integrity and recovery gates

A valid engine row requires both child exits zero; reciprocal terminal
callbacks with one verified winner; both archived replay copies matching
their source hashes; full `screp` parsing with the expected races; and
`replay_header_frames + 1 == owning_callback_frame`. Only the registered
terminal-drain kill events are allowed. A timeout, crash, sync error, missing
or contradictory result, replay failure, or identity drift is
infrastructure-invalid.

The final candidate diagnostic must pass both
`scripts/score_kestrel_modular_v1.py` and
`scripts/score_kestrel_modular_recovery.py`. It must report zero actual
command rejections, positive accepted gather and build commands, exact gather
acceptance reconciliation, and one ordered construction event per accepted
build command. Gather and builder preflight skips and cargo deferrals may be
zero or positive because they record avoided invalid requests, not issued
commands. The four-Probe Pylon, reserve, second-Zealot completion,
construction lifecycle, and command-category gates remain required.

## Decision

- **PASS TO FIVE-GAME SCREEN** only if the engine row and every integrity,
  modular-semantic, gather-recovery, and builder-recovery gate pass. The
  outcome may be a win or loss.
- **REJECT** if the row is valid and exposes any actual rejected command,
  unreconciled worker/construction accounting, malformed trace,
  public-observation violation, or retained-system regression.
- **INCONCLUSIVE** if infrastructure prevents a valid row or a registered
  mechanism remains unexercised without contradicting the implementation.

No outcome changes canonical Kestrel v13 or enters local Elo. This experiment
tests commandability recovery only. A five-opponent strength screen requires
its own frozen plan and a passing result here.
