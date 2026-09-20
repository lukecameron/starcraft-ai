# Competition requirements and verification

Checked **2026-09-20**. [BASIL rules](https://www.basil-ladder.net/rules.html) govern the intended ladder. [SSCAIT status](https://sscaitournament.com/) says it accepts submissions for BASIL but no longer runs games. Its [submission rules](https://sscaitournament.com/index.php?action=rules) retain legacy tournament/platform requirements. Recheck before packaging; do not equate legacy SSCAIT timing with BASIL timing.

Every row below has that verification date. Source abbreviations link to the pages above; local status is **pending** unless specified.

| Requirement | Source | Local enforcement / status and remaining work |
| --- | --- | --- |
| BW 1.16.1, 1v1 | BASIL | Separate official runtime validation from OpenBW evidence. |
| LF3 Normal latency | BASIL | Inspect engine command delay; acceleration must preserve it. |
| 30-minute wall limit: no win/loss | BASIL | Record timeout separately; do not count it as defeat. |
| 60-minute game limit: kills + razings decide | BASIL | Verify exact frame conversion; tied score falls back to wall-limit semantics. Project reference seconds are separate. |
| Crashes lose unless both crash | BASIL | Preserve both process outcomes and failed-game metadata. |
| No enforced per-frame timeout | BASIL | Still measure callback tails and maximum stalls. |
| One Ryzen 7 1700X core; 1 GB less OS | BASIL | Single-thread bot, initial 512 MiB target; x86 whole-environment check pending. |
| 100 MB combined ai/read/write | BASIL | Package accounting pending; local replay archive lives elsewhere. |
| Network generally forbidden | BASIL | No policy network calls. |
| write copied to read; retained across updates | BASIL | Version learning snapshots; reset evaluation state explicitly. |
| Complete vision/cheats forbidden | SSCAIT | Policy uses legal BWAPI observations; evaluator/replay inspection separate. |
| Supported release DLL; 4.4.0 listed | SSCAIT | Target official 4.4.0; listed DLL MD5 `cf7a19fe79fad87f88177c6e327eaedc`. Verify downloaded binary before packaging. |
| Source plus executable and compatible BWAPI.dll | SSCAIT | Plan x86 Windows C++ DLL; compile and runtime evidence tracked separately. |
| Legacy 32-bit Windows 7 | SSCAIT | Build a conservative x86 target; actual current BASIL OS remains uncertain. |
| Slow-frame loss thresholds | SSCAIT | Legacy: >1 frame at >10 s; >10 at >1 s; >320 at >85 ms. Report separately from BASIL. |
| Read/write restricted; CWD fixed | SSCAIT | Bot persistence only in permitted folders; harness owns other I/O. |
| No deliberate crash, pause, console spam | SSCAIT | Source audit and runtime validation pending. |
| Exploits restricted to enumerated exceptions | SSCAIT | No exploit-dependent opening planned; check new tactics against source list. |
| Licenses, derivative originality, source/build instructions | SSCAIT | Select base only after license review. Updated-within-year derivatives require author permission before upload. No contact or submission authorized. |

The old SSCAIT 90-minute/86400-frame adjudication and dynamic speed rules are not our BASIL evaluation rules. BASIL's own game-clock wording needs engine/runtime verification before it becomes a frame constant. No tournament readiness is claimed.
