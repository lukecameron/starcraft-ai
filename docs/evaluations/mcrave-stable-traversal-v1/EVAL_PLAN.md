# McRave stable-traversal evaluation plan

Use engine and McRave seed 4201 on Destination, McRave Zerg versus UAlbertaBot Terran at LF3, with a 120-second wall limit and engine library `f1a32e5a3dc64b8c62a17788488d36594dd95b13ef124637795b5aca4c846c42`.

Both evaluation variants sort the self-worker snapshot and mineral snapshot by public BWAPI unit ID. The baseline otherwise retains repeated ground-distance selection; the candidate adds invocation-local caching. These are isolated evaluation builds and do not replace canonical McRave artifacts.

The baseline binary is `879c0f1785bac559090a87cf77e8f2d905fc6227642b6b15154e9e131cd3078f` from evaluation patch `fc54ec62d43998642b23e098af827d8cdcc2e9750303436f17d9b5dc5834ca2e`. The candidate binary is `3e922a4aa2dd3a786061f43e63a5eb1612abab715c77afc5c51c44a681c11fbe` from evaluation patch `b0429b8a9e15a20ca592d0ef913efa0fbbb3bbd7cb35521499b087e2610f54b9`. Both passed the 114-translation-unit official-header build.

First run the baseline twice. Parse the replays and compare ordered commands through frame 1,000 after removing only `UnitTag` and `UnitTags`; retain frame, player, type, position, order, unit type, and queue state. If those commands and the opening match, run one candidate game and apply the same baseline/candidate gate. Stop at the first early mismatch, preserve it, and do not extend deterministic changes. Measure bounded throughput only if the gate passes. No result establishes strength or promotes a binary.

Before the second repeat finished, the gate was strengthened at `2026-09-20T03:32:47.639111Z` to compare raw tag-bearing commands as well. A normalized pass alone would be insufficient without a stable unit-identity bijection. This amendment can only reject an otherwise accepted result; it cannot relax the original criterion.
