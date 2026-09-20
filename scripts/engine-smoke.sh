#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
build="$root/third_party/bwapi/build-arm64"
logs="$root/artifacts/spikes/engine"
mkdir -p "$logs"

test -x "$build/bin/BWAPILauncher" || { echo "run scripts/engine-build.sh first" >&2; exit 1; }

# This is a loader/data smoke test. With no user-supplied game data it should
# reach OpenBW and report the first missing MPQ, rather than fail to load Mach-O
# dependencies. BWAPILauncher currently reports startup errors but exits zero.
(
  cd "$root"
  DYLD_LIBRARY_PATH="$build/lib" "$build/bin/BWAPILauncher"
) >"$logs/launcher-no-assets.log" 2>&1

grep -F "failed to open ./Patch_rt.mpq" "$logs/launcher-no-assets.log"
