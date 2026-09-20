#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
tools="$root/.tools/engine"
bwapi="$root/third_party/bwapi"
openbw="$root/third_party/openbw"
build="$bwapi/build-arm64"
logs="$root/artifacts/spikes/engine"
scenario_patch="$root/patches/openbw-scenarios.patch"
bwapi_revision=48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2
openbw_revision=4b046d5f65302b10cb0a745f0fecd37ec85b20a8

test -d "$bwapi/.git" || { echo "missing $bwapi; clone OpenBW/bwapi first" >&2; exit 1; }
test -d "$openbw/.git" || { echo "missing $openbw; clone OpenBW/openbw first" >&2; exit 1; }
test -x "$tools/bin/cmake" || { echo "missing project-local CMake at $tools/bin/cmake" >&2; exit 1; }
test -x "$tools/bin/ninja" || { echo "missing project-local Ninja at $tools/bin/ninja" >&2; exit 1; }
test -f "$scenario_patch" || { echo "missing $scenario_patch" >&2; exit 1; }
mkdir -p "$logs"

test "$(git -C "$bwapi" rev-parse HEAD)" = "$bwapi_revision" || { echo "unexpected BWAPI revision" >&2; exit 1; }
test -z "$(git -C "$bwapi" diff --binary HEAD -- . ':!build-arm64')" || { echo "BWAPI tracked sources are dirty" >&2; exit 1; }
test -z "$(git -C "$bwapi" status --porcelain --untracked-files=normal | grep -v -e '^?? build-arm64/$' -e '^?? build-arm64-asan/$' || true)" || { echo "BWAPI contains unexpected untracked files" >&2; exit 1; }
test "$(git -C "$openbw" rev-parse HEAD)" = "$openbw_revision" || { echo "unexpected OpenBW revision" >&2; exit 1; }
test -z "$(git -C "$openbw" status --porcelain --untracked-files=all | grep '^??' || true)" || { echo "OpenBW contains untracked files" >&2; exit 1; }
if git -C "$openbw" diff --quiet HEAD --; then
  git -C "$openbw" apply --check "$scenario_patch"
  git -C "$openbw" apply "$scenario_patch"
fi
actual_patch="$logs/openbw-scenarios.actual.patch"
git -C "$openbw" diff HEAD --binary >"$actual_patch"
cmp "$scenario_patch" "$actual_patch" || { echo "OpenBW working tree does not exactly match $scenario_patch" >&2; exit 1; }

"$tools/bin/cmake" \
  -S "$bwapi" \
  -B "$build" \
  -G Ninja \
  -DCMAKE_MAKE_PROGRAM="$tools/bin/ninja" \
  -DCMAKE_CXX_COMPILER=/usr/bin/clang++ \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
  -DOPENBW_DIR="$openbw" \
  -DOPENBW_ENABLE_UI=OFF \
  >"$logs/configure-policy.log" 2>&1

"$tools/bin/cmake" --build "$build" --parallel "${ENGINE_BUILD_JOBS:-4}" \
  >"$logs/build.log" 2>&1

file "$build/bin/BWAPILauncher" "$build/lib/ExampleAIModule.dylib"
nm -gU "$build/lib/ExampleAIModule.dylib" | grep -E '(_gameInit|_newAIModule)$'

ROOT="$root" BUILD="$build" BWAPI_REVISION="$bwapi_revision" OPENBW_REVISION="$openbw_revision" \
  /usr/bin/python3 - <<'PY'
import glob
import hashlib
import json
import os
import pathlib
import subprocess

root = pathlib.Path(os.environ["ROOT"])
build = pathlib.Path(os.environ["BUILD"])

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

artifacts = []
for path in [build / "bin" / "BWAPILauncher", *map(pathlib.Path, glob.glob(str(build / "lib" / "*.dylib")))]:
    if path.is_file():
        artifacts.append({
            "path": str(path.relative_to(root)),
            "sha256": sha256(path),
            "size_bytes": path.stat().st_size,
        })

patch = root / "patches" / "openbw-scenarios.patch"
data = {
    "schema_version": 1,
    "binary_path": str((build / "bin" / "BWAPILauncher").relative_to(root)),
    "binary_sha256": sha256(build / "bin" / "BWAPILauncher"),
    "bwapi_repository": "https://github.com/OpenBW/bwapi.git",
    "bwapi_revision": os.environ["BWAPI_REVISION"],
    "openbw_repository": "https://github.com/OpenBW/openbw.git",
    "openbw_revision": os.environ["OPENBW_REVISION"],
    "openbw_patch": "patches/openbw-scenarios.patch",
    "openbw_patch_sha256": sha256(patch),
    "timer_lifetime_fix": {
        "source": "sync.h",
        "semantics": "async timeout handlers retain shared completion state beyond caller stack scope",
    },
    "teardown_lifetime_fix": {
        "source": "sync_server_asio_socket.h",
        "semantics": "async handles skip client access after server teardown begins; guard outlives io_service",
    },
    "scenario_control": {
        "seed_env": "OPENBW_SCENARIO_SEED",
        "player_id_env": "OPENBW_SCENARIO_PLAYER_ID",
        "seed_semantics": "final OpenBW LCG state before random-race and starting-slot draws",
    },
    "compiler": subprocess.check_output(["/usr/bin/clang++", "--version"], text=True).splitlines()[0],
    "cmake_build_type": "Release",
    "max_parallel_jobs": int(os.environ.get("ENGINE_BUILD_JOBS", "4")),
    "artifacts": artifacts,
}
out = build / "bin" / "BWAPILauncher.build.json"
out.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
PY
