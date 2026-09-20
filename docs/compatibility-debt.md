# Official-game compatibility debt

Reviewed 2026-09-20. Budget: roughly two to three focused engineering days, not a rewrite. The diagnostic fixture uses only public BWAPI observations and commands; game data, launch, evaluation and archival are separate from gameplay. Engine access is forbidden in candidate policy code.

| Component | Evidence | Restoration work | Estimate / state |
| --- | --- | --- | --- |
| Shared diagnostic source | `src/diagnostic_module.cpp` compiles warning-free against OpenBW 4.2 and official BWAPI 4.4.0 headers on ARM64 | Rebuild source and official BWAPILIB for Win32 Release | Half day, source compile verified; Windows linking unverified |
| Official module | Official `v4.4.0` source pinned at `7687da8abc4726f8366401f11ab648d421385793`; example project uses `v141_xp`, DynamicLibrary | VS2017 x86 toolchain, runtime libraries, exports `gameInit` and `newAIModule`; use official 4.4.0 BWAPI.dll | Half day, statically reviewed |
| Original game | No Windows game process or injector run here | Load package into BW 1.16.1 via supported BWAPI/Chaoslauncher; check observations, startup, callbacks, replay, file access | Half to one day when a Windows execution environment exists; runtime unverified |
| Resource compliance | Native diagnostic whole-process measurements only | Measure intended package on representative x86 with a single core and actual environment cap | Half day after gameplay baseline stabilizes |
| Reused competitive bot | Full patched McRave source: all 114 translation units compile as ARM64 objects against official BWAPI 4.4.0 headers at pinned revision `7687da8abc4726f8366401f11ab648d421385793`; native OpenBW smoke completed with runtime LF3 and durable replay/result evidence | Compile and link a Win32 Release DLL against official BWAPILIB, then run it in BW 1.16.1 and verify startup, gameplay callbacks, file paths and replay output; preserve upstream Windows semantics | One to two days, source compatibility verified; Windows linking and original-game runtime unverified |
| Original Kestrel bot | Accepted v13 source compiles against both native OpenBW and official 4.4.0 headers; two full validation games retained economy, construction and combat using public BWAPI observations. Exact module and source hashes are in `config/kestrel-baseline.json` | Build the existing exported `gameInit`/`newAIModule` implementation as a Win32 DLL against official BWAPILIB, then verify the same gameplay and file-output behavior in the original game | Shares the Win32 toolchain and runtime work above; source compatibility verified, Windows linking and runtime unverified |

No Windows compiler (`clang-cl`, `lld-link`, MinGW x86), Wine, original-game install or runtime has been found on PATH. The produced `diagnostic-official-4.4.o` is an **ARM64 Mach-O object compiled against official headers**, not a Windows DLL or a successful Windows deployment.

Reproduce the source check after cloning the official tag into `third_party/bwapi-official`:

```sh
scripts/build_diagnostics.sh
```

Packaging: build own module and BWAPILIB from official 4.4.0 sources, ship the Win32 Release module with the venue-approved BWAPI.dll and required runtime dependencies, plus source/build instructions and third-party notices. Preserve permitted `bwapi-data/AI`, `read`, and `write` layout. Do not ship OpenBW, MPQs or the local replay archive in the tournament package. Verify the release DLL against the venue-listed checksum and recheck rules before packaging.

No cross-platform inference library, GPU runtime, privileged observation feature or host service is involved. New dependencies or simulator-specific policy changes require an updated debt estimate before adoption.
