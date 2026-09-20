# Current native engine

New development experiments use the frozen engine in `config/engine.json`. The six-game validation and limits are recorded in [the result](evaluations/openbw-terminal-drain-v1/RESULT.md). Historical schedules keep their old engines and remain reproducible; `scripts/engine-build.sh` still builds the older foundation described in `engine-spike.md`.

Use the selected launcher and library directory as explicit `run_match.py` arguments. Do not substitute the new engine into an already registered old-engine experiment. Bot policy still sees only public BWAPI state; synchronization diagnostics are evaluator evidence.

The direct rebuild uses pristine pinned checkouts and the complete patches. Do not apply `openbw-scenarios.patch` first; its changes are included in the terminal-drain patch. From the repository root, using new output directory names if these already exist:

```sh
git clone --shared third_party/openbw third_party/openbw-terminal-drain
git -C third_party/openbw-terminal-drain checkout --detach 4b046d5f65302b10cb0a745f0fecd37ec85b20a8
git -C third_party/openbw-terminal-drain apply "$PWD/patches/openbw-terminal-drain.patch"
git clone --shared third_party/bwapi third_party/bwapi-terminal-drain
git -C third_party/bwapi-terminal-drain checkout --detach 48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2
git -C third_party/bwapi-terminal-drain apply "$PWD/patches/bwapi-terminal-diagnostics.patch"
.tools/engine/bin/cmake -S third_party/bwapi-terminal-drain \
  -B third_party/bwapi-terminal-drain/build-arm64 -G Ninja \
  -DCMAKE_MAKE_PROGRAM="$PWD/.tools/engine/bin/ninja" \
  -DCMAKE_CXX_COMPILER=/usr/bin/clang++ -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
  -DOPENBW_DIR="$PWD/third_party/openbw-terminal-drain" -DOPENBW_ENABLE_UI=OFF
.tools/engine/bin/cmake --build third_party/bwapi-terminal-drain/build-arm64 --parallel 4
```

The tested build is frozen under `artifacts/builds/eee406fca0aed7ebda45d229a930452bfe33c763f52ecc83c7c996327ea7114b/openbw-terminal-drain/`, including the verified launcher `.build.json` sidecar. Use that package for exact-input trials on this machine. A fresh compilation must receive its own recorded hashes and matching build sidecar before controlled-seed use; do not copy a sidecar onto a different launcher hash. The local experiment's `build.json` contains the complete compiler/revision/patch/artifact record.
