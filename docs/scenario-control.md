# Controlled OpenBW scenarios

The evaluator can opt into repeatable OpenBW scenario initialization with two environment variables:

- `OPENBW_SCENARIO_SEED` is a base-10 unsigned 32-bit integer. It becomes the final OpenBW linear-congruential-generator state immediately before random-race selection and starting-slot shuffling. It therefore controls those draws and subsequent simulation randomness.
- `OPENBW_SCENARIO_PLAYER_ID` is a base-10, nonzero unsigned 32-bit integer. It deterministically replaces that process's randomly generated protocol UID. Each client in a game must use a distinct ID.

Both variables must be present or absent together. Empty values, signs, trailing characters, overflow, and player ID zero are rejected. Duplicate IDs are rejected by OpenBW's existing duplicate-UID handling. With neither variable set, UID and game-seed generation follow upstream OpenBW without a changed branch in the normal path.

For a two-player comparison, launcher positions use IDs 1 and 2. A paired game keeps those IDs attached to launcher positions and exchanges the bot modules and races. This preserves the scenario's two starting positions while exchanging the policies assigned to them. The control changes protocol identity and initialization only; it does not add observations or alter BWAPI's three-frame command latency.

The implementation is an exact patch over OpenBW revision `4b046d5f65302b10cb0a745f0fecd37ec85b20a8`. BWAPI remains at `48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2`. Rebuild from the repository root with:

```sh
./scripts/engine-build.sh
```

The build script accepts only the full diff in `patches/openbw-scenarios.patch`, rejects a dirty or unexpected BWAPI checkout, pins `/usr/bin/clang++`, limits parallel compilation to four jobs by default, and writes `third_party/bwapi/build-arm64/bin/BWAPILauncher.build.json`. That sidecar records both source revisions, the patch hash, compiler and build options, and hashes for the launcher and every generated dynamic library.

The same map, races, seed, player IDs, and deterministic command stream should produce the same replay initial state, player names, starting locations, and commands. Replay container bytes are not the comparison contract because each client writes its own perspective and container-level differences are not part of scenario control. OpenBW stores its RNG seed in the replay `StartTime` field, which replay tools may render as a date. Validation should parse both replays and compare the relevant header/setup fields and ordered command records.

## Validation

Seed 424242 was exercised twice with WorkerRush in launcher position 1 and Idle in position 2 on Benzene. Both games completed at logical frame 4219 with matching winner callbacks and LF3. `screp` produced identical parsed headers, map data, and all 80 ordered command records; the player-1 replay files were also byte-identical with SHA-256 `102fceb81e063cc97c06cafb6bcdd2c8fa32952bd50d8e6aff14400c8282edd7`. The durable records are:

- `artifacts/runs/20260920T024239-ff5e99f89c1e/game-0001/manifest.json`
- `artifacts/runs/20260920T024247-b4cd47265e8f/game-0001/manifest.json`

A third game exchanged WorkerRush and Idle between launcher positions while retaining seed 424242 and player IDs 1 and 2. The parsed replay retained player ID 1 at slot 1 and player ID 2 at slot 0; the bot names exchanged those slots, demonstrating the intended balanced-start assignment. Its record is `artifacts/runs/20260920T024254-47e64439d46e/game-0001/manifest.json`.

A direct launcher probe with `OPENBW_SCENARIO_SEED=-1` and player ID 1 exited before starting a game with `OPENBW_SCENARIO_SEED must be a decimal uint32`. The captured error is `artifacts/spikes/engine/scenario-negative-env.log`.
