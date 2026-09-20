# Kestrel v14 one-time opening priority result

## Decision: PASS for broader confirmation

V14 passed every registered timing, production, command-quality, lifecycle, replay, and throughput gate. The result advances this candidate to broader confirmation only. Canonical V13 remains unchanged, and the four losses do not establish strength.

| Pair | Arm / run | Gateway accepted | Zealot train | Candidate advance | Max Probe / Gate / Zealot | Rejection | FPS |
|---|---|---:|---:|---|---|---:|---:|
| Benzene 6103 | Control `20260920T075508-62f8e5d7a9a6` | 1,962 | 3,126 | — | 15 / 2 / 1 | 0/60 | 2,910.2 |
| Benzene 6103 | Candidate `20260920T075521-695cfdaf1ba3` | 1,614 | 2,694 | Gateway 348f; Zealot 432f | 14 / 1 / 2 | 0/64 | 3,025.4 |
| Heartbreak 6104 | Candidate `20260920T075538-ef6b94d73a4e` | 1,860 | 2,934 | Gateway 186f; Zealot 228f | 13 / 2 / 2 | 0/51 | 3,546.8 |
| Heartbreak 6104 | Control `20260920T075550-558aa41220f5` | 2,046 | 3,162 | — | 14 / 1 / 2 | 2/55 (3.64%) | 3,444.0 |

The registered mechanism required both candidate timings to advance by at least 120 frames in both matched pairs. All four comparisons passed. Candidate first Gateway completion and first Zealot completion were also earlier: 2,693/3,299 versus 3,123/3,731 on Benzene, and 2,933/3,539 versus 3,157/3,767 on Heartbreak.

Both candidates resumed Probe production after the one-time phase and continued later construction: they reached 14 and 13 Probes, two Pylons, at least one Gateway, and two Zealots. Each issued accepted attack commands, produced only Protoss units, recorded zero gas-worker build attempts, zero build `Unit_Busy`, and zero rejected commands. The persistent accepted-Zealot flag prevents the opening phase from reactivating after unit deaths.

All four games completed with reciprocal callbacks, both launchers returning zero, LF3, and no state-hash mismatch. All eight archived replay copies parsed fully. Durable throughput exceeded 384 frames/s in every row. All four games were losses; outcome and terminal duration were descriptive and did not enter the timing decision.

## Frozen evidence

- Control module SHA-256: `23a6ca0190d6cb088c64be990cc8fa6128abf63de1f99820213a5cd29c77d5dc`
- Corrected candidate module SHA-256: `d9e3445e4740cd1c7dd48d0d99a27760bb95d365e573684222d649b3ee470f25`
- Candidate source SHA-256: `67758a7787a2df97598b49fcc28a84d0ac2c5336fb8ab052ea5bd2ddbc5bd046`
- Candidate incremental patch SHA-256: `b5fd51e6e50ab8eda83b12bcd550fc58e61a875ba09790598d01a99795f47a5c`
- Schedule/result record: `config/kestrel-opening-v14.json`

The initially compiled candidate `415832a2…` never ran. Prelaunch review corrected its accepted-versus-current Gateway reservation gap; the four games used only `d9e3445e…`.
