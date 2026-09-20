# Missing-edge extension — ADOPT display evidence

All 12 registered games completed cleanly. Both children exited 0, terminal outcomes opposed, and no state-hash mismatch occurred. All 24 replay copies match their archived SHA256, parse with screp 1.13.4 and pass owner-frame/race checks. Each of the three requested pairing types has four valid games. The extension pools with v2 into the same current-engine component: 36 games and five exact build/race/config nodes. The older engine remains a separate nine-game component.

Direct results: Stardust beat ZZZK 4–0; McRave beat UAlberta Protoss 4–0 and Terran 3–1. The Terran win occurred on Heartbreak Ridge with McRave in protocol slot 2. These are exact-build/map/seed observations, not a causal code improvement.

## Updated cumulative local estimates

| Build/race | Cumulative W–L | Estimate | Approximate 95% conditional interval |
|---|---:|---:|---|
| Stardust Protoss `1039975842c6` | 16–0 | 1426.8 | 994.8 to 1858.9 |
| ZZZKBot Zerg `ce796a5d49d7` | 7–5 | 1000.0 | 1000.0 to 1000.0 |
| McRave Zerg `04521befa41b` | 8–12 | 836.8 | 536.4 to 1137.1 |
| UAlbertaBot Terran `75ac4f6bb44e` | 3–9 | 579.6 | 220.3 to 938.9 |
| UAlbertaBot Protoss `75ac4f6bb44e` | 2–10 | 535.3 | 139.2 to 931.5 |

The same 400 Elo Gaussian-prior model now has direct evidence for the previously missing edges. ZZZK 1000 is arbitrary; its zero-width displayed reference is a coordinate choice, not perfect certainty. Approximate intervals remain wide, prior-sensitive, and conditional on independent/transitive outcomes without fitted map/style effects. Repeated map/slot pairs are correlated. No BASIL rating or tournament claim follows.

The extension ran 209,968 frames over 426.028 summed durable seconds (492.9 fps aggregate); slowest 313.4 fps. Build work could overlap, so this is descriptive and cannot pass a performance promotion gate.

Adopt the complete extension for rating display. Further strength work should compare an actual candidate with its frozen baseline and reserve new seeds for confirmation; repeatedly measuring the same strong-versus-weak edges is lower value. Keep the current registry and separate historical evidence.

Local review ledger SHA256 `a5ed15ee9ca951ab3e3f63abdf6672fe5af2a776d577a072cceb6487a0dcaa6b`. Inclusion pins all twelve final match-manifest hashes in config/local-ratings.json. All attempts and replay copies are preserved.
