# Official-game compatibility debt

Reviewed 2026-09-20. Budget: roughly two to three focused engineering days, not a rewrite. The diagnostic fixture uses only public BWAPI observations and commands; game data, launch, evaluation and archival are separate from gameplay. Engine access is forbidden in candidate policy code.

| Component | Evidence | Restoration work | Estimate / state |
| --- | --- | --- | --- |
| Shared diagnostic source | `src/diagnostic_module.cpp` compiles warning-free against OpenBW 4.2 and official BWAPI 4.4.0 headers on ARM64 | Rebuild source and official BWAPILIB for Win32 Release | Half day, source compile verified; Windows linking unverified |
| Official module | Official `v4.4.0` source pinned at `7687da8abc4726f8366401f11ab648d421385793`; example project uses `v141_xp`, DynamicLibrary | VS2017 x86 toolchain, runtime libraries, exports `gameInit` and `newAIModule`; use official 4.4.0 BWAPI.dll | Half day, statically reviewed |
| Original game | No Windows game process or injector run here | Load package into BW 1.16.1 via supported BWAPI/Chaoslauncher; check observations, startup, callbacks, replay, file access | Half to one day when a Windows execution environment exists; runtime unverified |
| Resource compliance | Native diagnostic whole-process measurements only | Measure intended package on representative x86 with a single core and actual environment cap | Half day after gameplay baseline stabilizes |
| Reused competitive bot | McRave native port in progress | Recompile every substantive policy patch against official API; preserve upstream Windows semantics; reassess debt after port | Unknown until port checkpoint; do not treat as validated candidate |

No Windows compiler (`clang-cl`, `lld-link`, MinGW x86), Wine, original-game install or runtime has been found on PATH. The produced `diagnostic-official-4.4.o` is an **ARM64 Mach-O object compiled against official headers**, not a Windows DLL or a successful Windows deployment.

Reproduce the source check after cloning the official tag into `third_party/bwapi-official`:

```sh
scripts/build_diagnostics.sh
```

Packaging: build own module and BWAPILIB from official 4.4.0 sources, ship the Win32 Release module with the venue-approved BWAPI.dll and required runtime dependencies, plus source/build instructions and third-party notices. Preserve permitted `bwapi-data/AI`, `read`, and `write` layout. Do not ship OpenBW, MPQs or the local replay archive in the tournament package. Verify the release DLL against the venue-listed checksum and recheck rules before packaging.

No cross-platform inference library, GPU runtime, privileged observation feature or host service is involved. New dependencies or simulator-specific policy changes require an updated debt estimate before adoption.
