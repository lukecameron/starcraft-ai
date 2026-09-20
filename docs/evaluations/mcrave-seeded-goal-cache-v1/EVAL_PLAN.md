# McRave seeded goal-cache evaluation plan

This evaluation asks whether caching ground distances within one `assignNumberToGoal` call improves bounded McRave throughput when both OpenBW's initial state and McRave's process-global random generator are controlled.

The seed-only baseline is binary `7b089ca77fa9b2a057320b88d8fd4cf3d6b984bca0715e2fe3aca517b7a1f998`, built from patch `2ab7cf14886558baf032079231ddd16d4e0d62e687317d46722b93048b7913df`. The candidate is binary `3c81f2ebd1c54a612345a0156909f7bebf001a03d363a9f344a54b25d5c1baf5`, built from patch `4222551473a11860e99bbdd956e94ad8976bc9af4870e6546ec11c462146b6b9`. Both use `MATCH_BOT_SEED`, applied with `std::srand` before any McRave subsystem starts. Both passed the 114-translation-unit official BWAPI header build.

Run baseline and candidate on Destination as McRave Zerg versus UAlbertaBot Terran at LF3, with matching engine and bot seeds 4101 and 4102. Use the corrected engine library `f1a32e5a3dc64b8c62a17788488d36594dd95b13ef124637795b5aca4c846c42` and a 120-second wall limit. Preserve every result, failure, and replay.

Interpret throughput only if each pair records the same opening and a compatible early command sequence, with no candidate-only failure. Report each seed separately and together. This bounded evaluation cannot establish strength and will not promote or replace the configured baseline.
