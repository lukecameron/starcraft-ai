#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
tools="$root/.tools/engine"
bwapi="$root/third_party/bwapi"
openbw="$root/third_party/openbw"
build="$bwapi/build-arm64"
logs="$root/artifacts/spikes/engine"

test -d "$bwapi/.git" || { echo "missing $bwapi; clone OpenBW/bwapi first" >&2; exit 1; }
test -d "$openbw/.git" || { echo "missing $openbw; clone OpenBW/openbw first" >&2; exit 1; }
test -x "$tools/bin/cmake" || { echo "missing project-local CMake at $tools/bin/cmake" >&2; exit 1; }
test -x "$tools/bin/ninja" || { echo "missing project-local Ninja at $tools/bin/ninja" >&2; exit 1; }
mkdir -p "$logs"

"$tools/bin/cmake" \
  -S "$bwapi" \
  -B "$build" \
  -G Ninja \
  -DCMAKE_MAKE_PROGRAM="$tools/bin/ninja" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
  -DOPENBW_DIR="$openbw" \
  -DOPENBW_ENABLE_UI=OFF \
  >"$logs/configure-policy.log" 2>&1

"$tools/bin/cmake" --build "$build" --parallel "${ENGINE_BUILD_JOBS:-18}" \
  >"$logs/build.log" 2>&1

file "$build/bin/BWAPILauncher" "$build/lib/ExampleAIModule.dylib"
nm -gU "$build/lib/ExampleAIModule.dylib" | grep -E '(_gameInit|_newAIModule)$'
