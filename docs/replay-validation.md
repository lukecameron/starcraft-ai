# Archived replay validation

**Checked:** 2026-09-20
**Replay:** `artifacts/replays/2026/09/20/20260920T015245-8d1cc76f5e12/game-0001-player-1-1.rep`
**Purpose:** independently validate that the OpenBW-produced `.rep` is parseable by a maintained external CLI and retain machine-readable metadata.

## Parser provenance

The parser is [icza/screp](https://github.com/icza/screp), release **v1.13.4**, source tag commit `bee3af1b23834cc09efbda5fa3c02b0544a38ed4`. The project is Apache License 2.0; the module declares `github.com/icza/screp v1.13.4` with Go module checksum `h1:J/paOW+VJpd6fhl+G2m9L5EHj1KyFPDFPLgjDTfk0Uw=`. The official release page did not provide a darwin-arm64 asset, so the source tag was built locally:

```sh
GOBIN="$PWD/.tools/screp" go install github.com/icza/screp/cmd/screp@v1.13.4
```

The resulting `.tools/screp/screp` is a Mach-O arm64 executable. `screp -version` reports:

```text
screp version: v1.13.4
Parser version: v1.13.4
EAPM algorithm version: v1.0.6
Platform: darwin arm64
Built with: go1.27.1
```

Binary SHA-256: `240ca422e6d0827b5b227e953cc5b737c7cfa0756f90ae956df1e12c439e4a04`.

## Reproduction commands

Run from the repository root:

```sh
REPLAY="$PWD/artifacts/replays/2026/09/20/20260920T015245-8d1cc76f5e12/game-0001-player-1-1.rep"
.tools/screp/screp -overview "$REPLAY"
.tools/screp/screp -computed -cmds "$REPLAY" > artifacts/spikes/replay-validation/replay.json
.tools/screp/screp -map -mapDataHash sha256 "$REPLAY" > artifacts/spikes/replay-validation/map.json
```

Saved outputs:

| Output | SHA-256 |
|---|---|
| [`overview.txt`](../../artifacts/spikes/replay-validation/overview.txt) | `b40bed055e03eb2aea389bbf8b74f9bd4ad4eb8be1884779eb5307e1b60d7349` |
| [`replay.json`](../../artifacts/spikes/replay-validation/replay.json) | `d3ec44979a8edc53b929492e71f8fb14d7e446e93c7b3327ecd96da206634020` |
| [`map.json`](../../artifacts/spikes/replay-validation/map.json) | `d765e1226937eb21733ba8f645811604b4c242c355f0a39a80d0ff38d168177a` |

## Parsed evidence

The parser completed with exit code 0 and emitted no `ParseErrCmds`. The replay header reports:

| Field | Value |
|---|---|
| Engine/version | Brood War `-1.16` |
| Header frame count | 5,613 logical frames |
| Match type/speed | Melee / Normal |
| Map dimensions | 128 × 112 tiles |
| Map | Embedded name bytes decode as `Benzene1.1`; the raw screp JSON retains control-byte prefixes in the legacy name field |
| Players | 2 humans, both Protoss, both named `bwapi` |
| Parser-inferred winner | Team 2; corroborated separately by the game callbacks |
| Commands | 76 total: 37 Select, 37 Targeted Order, 2 Leave Game |
| Last command frames | player 0: 5,585; player 1: 5,567 |
| Player command counts | player 0: 2; player 1: 74 |
| Effective command counts | player 0: 2; player 1: 74 |
| APM / EAPM | player 0: 1 / 1; player 1: 19 / 19 |
| Parse errors | 0 |

The maximum command frame (5,585) is close to, but below, the header terminal frame count (5,613), and player 0 has two decoded `Leave Game` records at frame 5,585 (an unknown reason and a dropped-client reason). This is independent terminal-frame evidence that the file contains a coherent command stream through the end of the short diagnostic game. It does not prove replay synchronization for longer or more varied matches.

The embedded map section also parses as version 205, tileset `Space Platform`, with two human open slots and two start locations. The map description is present in the output. `map.json` contains the parsed CHK-style map metadata.

The original replay SHA-256 is `a763989ca5f89703aa1a57718f7f96c3fbcfcdd07a4e3d743edf9aa022887e41` (51,487 bytes). Its first four bytes are `a7 7e 7e 2b`; the replay parser, rather than a file-extension or size check, is the validation authority here.

## Result and limitation

**Result: validated as a parseable Brood War replay with coherent header, embedded map metadata, command statistics, and terminal leave-game events.** This independently supports the engine-spike claim that OpenBW emitted a native `.rep` rather than an arbitrary command log.

The replay is a short WorkerRush-versus-Idle diagnostic match, so the evidence is narrow. The parser exposes the embedded map name with legacy control-byte prefixes, and the header date is synthetic (`2083-05-15`) as emitted by the OpenBW fixture. Before relying on replay analytics for competitive games, validate a longer match containing production, combat, and multiple command types, and compare parser frame/terminal evidence with the engine manifest.

## Full native playback sample

The later UAlbertaBot versus ZZZKBot replay (SHA-256 `4b5462b10a1f2a3613d6cd7d4f0e3976d899e174b6a77f94e9b5256aa9f72174`) was replayed to completion. `artifacts/spikes/replay-playback-c8f74ad2/manifest.json` records process exit 0, `is_replay: true`, replay frame count 9,581, terminal observer frame 9,583, and `ended: true`. The two-frame observer delay is distinct from multiplayer LF3. Playback completes without recorded error; no live-versus-replay final-state checksum assertion exists yet.
