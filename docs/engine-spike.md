# Native OpenBW ARM64 spike

Verified 2026-09-20 on an Apple M5 Max running macOS 26.6.2 with Apple Clang 21.0.0.

## Result

The native, headless OpenBW launcher and a representative BWAPI AI module compile as ARM64 Mach-O binaries. The build completed successfully in 11.3 seconds at 18-way parallelism. Runtime reached OpenBW's data loader and stopped at the expected unavailable user asset:

```text
Error: file_reader: failed to open ./Patch_rt.mpq for reading
```

This establishes **compiled**, **loader smoke-tested**, and **complete multiplayer match and independently parsed replay verified**. After the engineer explicitly authorized following OpenBW's recommended data route, the required data was sourced into ignored local storage from Blizzard's public StarEdit package and the map from SSCAIT's published tournament pack.

Pinned upstream inputs:

| Component | Revision | Commit date | License observed |
| --- | --- | --- | --- |
| `OpenBW/bwapi` | `48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2` | 2020-06-11 | LGPL-3.0 license files |
| `OpenBW/openbw` | `4b046d5f65302b10cb0a745f0fecd37ec85b20a8` | 2026-08-13 | No license file found at this revision; redistribution status needs clarification |

The BWAPI repository describes itself as an OpenBW-specific fork of BWAPI 4.2.0 and explicitly says it no longer works with original StarCraft. OpenBW is incorporated through `OPENBW_DIR` during the BWAPI build.

## Reproduce the build

The project-local tools are CMake 4.4.3 and Ninja 1.13.2 under `.tools/engine`. A clean bootstrap is:

```sh
mkdir -p third_party artifacts/spikes/engine
git clone https://github.com/OpenBW/bwapi.git third_party/bwapi
git -C third_party/bwapi checkout 48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2
git clone https://github.com/OpenBW/openbw.git third_party/openbw
git -C third_party/openbw checkout 4b046d5f65302b10cb0a745f0fecd37ec85b20a8
python3 -m venv .tools/engine
.tools/engine/bin/pip install 'cmake==4.4.3' 'ninja==1.13.2'
scripts/engine-build.sh
scripts/engine-smoke.sh
```

CMake 4 removed compatibility with policy versions below 3.5. The upstream project declares CMake 3.1, so configuration needs `-DCMAKE_POLICY_VERSION_MINIMUM=3.5`. This is a command-line compatibility setting; no upstream patch was needed.

Outputs:

- `third_party/bwapi/build-arm64/bin/BWAPILauncher`: ARM64 executable.
- `third_party/bwapi/build-arm64/lib/{libBWAPI,libBWAPILIB,libOpenBWData}.dylib`: ARM64 libraries.
- `third_party/bwapi/build-arm64/lib/ExampleAIModule.dylib`: ARM64 module exporting `gameInit` and `newAIModule`.
- `artifacts/spikes/engine/configure.log`: the initial expected CMake 4 policy failure.
- `artifacts/spikes/engine/configure-policy.log`, `build.log`, and `launcher-no-assets.log`: successful configuration/build and runtime smoke evidence.

The upstream build emits warnings including undefined variable-template declarations, deprecated `sprintf`/`OSMemoryBarrier`, and non-trivial object-copy operations. Complete games now exercise this code, but these warnings remain upstream debt; passing games do not establish their safety.

## Local game data and maps

OpenBW's three required files are available under `third_party/game-data/mpq/` with exact capitalization:

- `Patch_rt.mpq`
- `StarDat.mpq`
- `BrooDat.mpq`

Source and immutable hashes:

| Artifact | Source | SHA-256 |
| --- | --- | --- |
| `StarEdit.zip` | `http://download.blizzard.com/pub/starcraft/StarEdit/StarEdit.zip` | `2306b3a82a1c2be7afc2ab2f917d44398ba50462bc47b4af25bc4952b2e17bfa` |
| `BrooDat.mpq` | extracted from `StarEdit.zip` | `c6d810981e24b947b36d531ab047e143fec0284a581fdaad6fc431e1e75e21df` |
| `Patch_rt.mpq` | extracted as `patch_rt.mpq`, capitalization normalized | `a063f069f1abe202b142b08a9dab878eba8ba033bf13a818024a72631c4452be` |
| `StarDat.mpq` | extracted from `StarEdit.zip` | `8845fd871b4f8f242cc5c2b6f6b8b319d86bbbd02bc836356b51f81b5ba8203f` |
| `sscai_map_pack.zip` | `https://sscaitournament.com/files/sscai_map_pack.zip` | `efc9070e5ff2fdd1066a414bb989748ac49bec776db1fac16eebd39d6e284aa7` |

Blizzard's public StarEdit announcement links the ZIP directly. The package is no longer supported, but it contains the trimmed 1.16-compatible archives OpenBW needs. SSCAIT publishes its 15-map pack as the tournament map selection. These assets remain local and must not be committed or redistributed.

To reproduce the local data layout from those public sources:

```sh
mkdir -p third_party/game-data/downloads third_party/game-data/runtime/sscai
curl --fail --location http://download.blizzard.com/pub/starcraft/StarEdit/StarEdit.zip -o third_party/game-data/downloads/StarEdit.zip
curl --fail --location https://sscaitournament.com/files/sscai_map_pack.zip -o third_party/game-data/downloads/sscai_map_pack.zip
python3 - <<'PY'
from pathlib import Path
import hashlib
import zipfile
base = Path('third_party/game-data')
expected = {
    'StarEdit.zip': '2306b3a82a1c2be7afc2ab2f917d44398ba50462bc47b4af25bc4952b2e17bfa',
    'sscai_map_pack.zip': 'efc9070e5ff2fdd1066a414bb989748ac49bec776db1fac16eebd39d6e284aa7',
}
for name, digest in expected.items():
    assert hashlib.sha256((base / 'downloads' / name).read_bytes()).hexdigest() == digest, name
with zipfile.ZipFile(base / 'downloads/StarEdit.zip') as archive:
    for source, target in [('BrooDat.mpq', 'BrooDat.mpq'), ('StarDat.mpq', 'StarDat.mpq'), ('patch_rt.mpq', 'Patch_rt.mpq')]:
        (base / 'runtime' / target).write_bytes(archive.read('StarEdit/' + source))
with zipfile.ZipFile(base / 'downloads/sscai_map_pack.zip') as archive:
    for name in archive.namelist():
        path = Path(name)
        if path.parent == Path('sscai') and path.suffix.lower() in ('.scm', '.scx'):
            (base / 'runtime/sscai' / path.name).write_bytes(archive.read(name))
PY
```

An upstream archive checksum change should be investigated before using it, since game data and maps affect reproducibility. Only data files are extracted; no downloaded installer or executable is run.

The launcher probes `Patch_rt.mpq` first. With all three MPQs and SSCAIT's `(2)Benzene.scx`, a headless single-player launch successfully loaded `ExampleAIModule.dylib`, reported BWAPI 4.2.0 Release live, identified `Benzene1.1`, and entered `Zerg vs Unknown`. The example bot then flooded `Unit_Does_Not_Exist` errors because OpenBW has no built-in opponent; the process was interrupted after the startup proof.

OpenBW has no built-in computer opponent. A real bot-versus-bot match needs two launcher processes and two native modules. The smallest initial module is the built `ExampleAIModule.dylib`; it only orders idle workers to mine and is suitable as a plumbing check, not a competitive baseline. Configure both processes through `BWAPI_CONFIG_*` environment variables or separate INI files, set `auto_menu=LAN`, and use `OPENBW_LAN_MODE=LOCAL` with the same short `OPENBW_LOCAL_PATH` for both clients. The automatic discovery mode stalled before callbacks on Destination, whereas direct local sockets started that game and two concurrent diagnostic pairs. Both clients must select the same map. UI is disabled at compile time and can also be forced with `OPENBW_ENABLE_UI=0`.

## Replay support

This OpenBW revision contains both a Brood War replay reader (`replay.h`) and saver (`replay_saver.h`). BWAPI's end-of-game path calls `bwgame.saveReplay(...)`; `auto_menu.save_replay` supplies its path. The saver writes the native Brood War replay structure, including the `0x53526572` identifier, compressed sections, CRC32 values, embedded scenario data, and command stream. Therefore output is intended to be a true `.rep`, not a custom command log.

Generation is runtime verified, and the archived player-1 replay independently parses with screp v1.13.4: 5,613 header frames and 76 decoded commands, without parser errors. See [replay validation](replay-validation.md). A BWAPILauncher replay-load smoke run reached module initialization; its retained log has no terminal-frame summary or persisted exit record, so full playback completion remains unverified. Parsing alone does not prove simulation synchronization.

Completed match evidence is in `artifacts/runs/20260920T015245-8d1cc76f5e12/game-0001/manifest.json`. WorkerRush Protoss defeated Idle Protoss on Benzene in 5,614 logical frames. End-to-end harness time was 1.536 seconds, or 3,656 logical frames/second (152x the project's 24-fps reference speed and 9.5x the required 16x target). Each launcher peaked around 44 MB RSS, though this short diagnostic match does not establish a representative full-game memory bound.

Both bots reported runtime latency of exactly 3 frames. WorkerRush issued 37 accepted commands, with zero rejected commands, callback p99 0.0047 ms and maximum 2.106 ms. Idle issued no commands and lost. The archived replay identities are:

- player 1: 51,487 bytes, SHA-256 `a763989ca5f89703aa1a57718f7f96c3fbcfcdd07a4e3d743edf9aa022887e41`
- player 2: 51,477 bytes, SHA-256 `9ca74ff8bccfb1955908cde684d540e1d097e58fd6e3756ca6be2432281cc8c9`

Two integration failures and one sandbox limitation were also preserved before success:

- runs `20260920T015054-18fd4974d193` and `20260920T015129-85962e13b704`: `File name too long`, first from an absolute replay path and then from a Unix socket path longer than macOS `sockaddr_un` permits.
- run `20260920T015225-d4f6cbd53aa6`: `bind: Operation not permitted` inside the command sandbox. The successful match used a short `/tmp/scai-*` socket directory and the authorized sandbox escalation.

## Latency and headless timing

OpenBW sets `sync_funcs.sync_st.latency = 3` when creating a multiplayer game. Single-player replay playback uses the default two-frame observer latency; that does not change the recorded multiplayer commands. `Game::getLatencyFrames()` returns this value directly. No environment/configuration override exists in the inspected source, so this backend implements the project's LF3 command-latency requirement by construction. Both diagnostic modules also reported 3 at runtime.

In the no-UI branch, `next_frame()` advances without sleeping. `OPENBW_GAME_SPEED` controls sleeping only when a UI object exists. Therefore headless throughput is not throttled by the normal 42 ms fastest-game frame duration. The first McRave/ZZZKBot cross-game measured 633 frames/s, or 26.4× reference speed, including durable replay archival. A representative late-game suite remains unmeasured; see [performance evidence](performance.md).

## Current bot route

McRave is the provisional development reference; ZZZKBot supplies an independent rush opponent. Both ports have completed native games and emitted independently parsed replays. Full McRave gameplay also compiles against official 4.4.0 headers, without a Windows link or runtime claim. See [McRave](mcrave-port.md), [ZZZKBot](zzzkbot-port.md), and the versioned [reference record](../config/baseline.json).

The cohort now includes ZZZKBot Zerg and full UAlbertaBot Protoss/Terran policies. It remains uncalibrated; the first controlled quick batch is registered. McRave's recent source update means author permission is needed before a derivative submission; local development and benchmarking can proceed. UAlbertaBot is also a runnable permissive fallback. Stardust carries a competition-fork consent condition and is a benchmark lead only.

## Official Windows/BWAPI path

The official-game target should be a separate Windows build of the same gameplay source, using official BWAPI 4.4.0 and Visual Studio 2017-compatible 32-bit Release settings. The official release notes require building `BWAPILIB` locally as a dependency of the bot rather than relying on a prebuilt `.lib`. Deliver a 32-bit AI module DLL exporting the same `gameInit(BWAPI::Game*)` and `newAIModule()` entry points; load it into StarCraft: Brood War 1.16.1 through the official BWAPI 4.4.0 injector/Chaoslauncher route.

Keep engine-specific startup and build definitions outside gameplay code. Compile gameplay against the common BWAPI 4.x subset and maintain two thin targets:

1. ARM64 macOS `.dylib` against OpenBW's BWAPI 4.2 fork for local simulation.
2. Win32 `.dll` against official BWAPI 4.4.0 for competition.

Avoid OpenBW internals in the policy. Differences between 4.2 and 4.4 must be isolated behind compatibility helpers and tested on both targets. The diagnostic and all 114 McRave translation units compile as ARM64 objects against official BWAPI 4.4.0 headers. No Windows compiler or original-game runtime was available: Win32 linking and injection remain unverified. The next portability check must produce and load the real Win32 DLL.

## Concrete remaining blockers

1. The runnable cohort has three codebases across three races. Calibrated strength, stronger diverse anchors and representative late-game performance remain unverified.
2. OpenBW's repository has no explicit license file at the pinned revision; clarify redistribution before shipping it or derived binaries.
3. Official BWAPI 4.4.0 is a different code line from the OpenBW 4.2 fork. Windows compilation and injection remain unverified.
4. Replay validation needs expansion to representative games and an explicit terminal-frame/desync assertion; the retained playback smoke log reaches module initialization without a recorded error; process completion and synchronization remain unverified.

## Controlled scenarios and expanded playback check

The evaluator now supports `--seed` with a pinned opt-in OpenBW patch; two repeated fixtures produced byte-identical replays, and swapping bot assignments preserved starting slots. See [scenario control](scenario-control.md). Bot-internal nondeterminism is still possible.

The same pinned patch now repairs an OpenBW asynchronous socket-handler lifetime fault during ordinary launcher shutdown. The exact release reproduction and an AddressSanitizer teardown check pass with both launcher processes exiting zero; see [OpenBW socket teardown lifetime repair](openbw-teardown.md).

`artifacts/spikes/replay-playback-c8f74ad2/manifest.json` records full native playback of UAlbertaBot versus ZZZKBot: replay length 9,581 frames, observer terminal callback at 9,583, zero exit, and no replay error. This verifies reaching the end of this replay; no final-state checksum comparison to the live match has been implemented.
