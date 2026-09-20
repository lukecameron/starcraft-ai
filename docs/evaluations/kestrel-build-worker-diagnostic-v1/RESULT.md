# Kestrel build-worker diagnostic v1 result

## Result: confirmed stale-builder role conflict

The registered same-cadence `assignEconomy()` hypothesis was falsified. The two reproduced `Unit_Busy` build failures used worker `137`, and neither had a successful gather command in the same cadence. Instead, the bot reused its existing `builderId_` while that Probe was actively harvesting gas.

The single registered attempt ran in batch session `58056`, run `20260920T072826-04f5da60f197`, on Heartbreak Ridge seed 6104. It completed normally as a Kestrel loss with reciprocal callbacks, both launchers returning zero, LF3, no `insync_hash_mismatch`, and both replay copies archived. The player-1 replay parsed through 5,489 frames and has SHA-256 `c133b71612809753840270d34cbc6dac7c4b360389b397c46c681df1dcf7b0e9`.

## Reproduced failure

The complete JSONL trace contains 265 records, nine build attempts, and two rejected attempts:

| Frame | Type | Worker | Position | Pre/post order | Target | Distance | Same-cadence gather | Result |
|---:|---|---:|---|---|---|---:|---|---|
| 3,738 | Pylon (`156`) | 137 | `(3864,1700)` | `83` / `83` (`HarvestGas`) | `(111,51)` | 300 | false | `Unit_Busy` (`3`) |
| 3,744 | Pylon (`156`) | 137 | `(3864,1700)` | `83` / `83` (`HarvestGas`) | `(111,51)` | 300 | false | `Unit_Busy` (`3`) |
| 3,750 | Pylon (`156`) | 137 | `(3864,1700)` | `84` / `30` (`ReturnGas` → `PlaceBuilding`) | `(111,60)` | 358 | false | accepted |

The source explains the sequence. `build()` first calls `constructionPending()`, then prefers `unitById(builderId_)`. It replaces that worker only when absent, constructing, or the scout. It does not reject a worker that is gathering gas or otherwise busy. The earlier accepted Pylon request at frame 3,426 used the same worker. After the existing 240-frame pending interval expired, the worker was no longer `PlaceBuilding`, so `constructionPending()` stopped protecting the request; `build()` retained worker 137 and attempted another Pylon while its order was `HarvestGas`. Both calls failed immediately with `Unit_Busy`. Once the worker entered `ReturnGas`, BWAPI accepted the build at frame 3,750.

This is a proven stale-builder ownership conflict in the existing pending/retry lifecycle. It is not the proposed same-cadence gather/build conflict, and no policy repair was made in this diagnostic.

## First-Pylon description

The first Pylon was accepted at bot frame 1,224 using worker 110 at `(3988,1876)`, order `MiningMinerals`, target tile `(111,58)`, and recorded target distance 424 pixels. It became current at frame 1,341, 117 frames later. This successful path is descriptive and does not explain Benzene's earlier 289-frame travel interval.

## Identity and limits

- Preregistered: `2026-09-20T07:26:55+00:00`
- Module SHA-256: `a91296e864dc712e51440127280f07cf944ae28f23b28906f8949eb01933e78a`
- Combined source SHA-256: `b54d1cb5632ad86bc48b8c19102224f2f8be24052b697757fcd0aaaeb7b99665`
- Incremental diagnostic patch SHA-256: `331b19cf48b5a53a3e74516abcdabfa4b273a4e1867bad12a5908e9f71a62e0c`
- Raw trace: `artifacts/runs/20260920T072826-04f5da60f197/game-0001/player-1/bwapi-data/write/build-attempts.jsonl`
- Frozen package: `artifacts/builds/a91296e864dc712e51440127280f07cf944ae28f23b28906f8949eb01933e78a/kestrel-build-worker-diagnostic-v1/`

The trace proves this reproduced failure's worker state. It does not establish how often the conflict occurs across maps or seeds, justify strength promotion, or diagnose the Benzene first-Pylon path.
