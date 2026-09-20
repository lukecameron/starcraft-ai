#!/bin/sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
source_dir="$repo_root/third_party/mcrave"
patch_file="$repo_root/patches/mcrave.patch"
build_dir="$repo_root/build/mcrave"
cmake_bin=${CMAKE_BIN:-"$repo_root/.tools/engine/bin/cmake"}
PATH="$repo_root/.tools/engine/bin:$PATH"

expected_mcrave_revision=7d1719a22d8b896f957abae50e2ea5efff974fe2
expected_official_revision=7687da8abc4726f8366401f11ab648d421385793
expected_openbw_revision=48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2

assert_revision() {
  checkout=$1
  expected=$2
  label=$3
  actual=$(git -C "$checkout" rev-parse HEAD)
  if [ "$actual" != "$expected" ]; then
    echo "$label checkout is at $actual, expected $expected" >&2
    exit 1
  fi
}

assert_revision "$source_dir" "$expected_mcrave_revision" McRave
assert_revision "$repo_root/third_party/bwapi-official" "$expected_official_revision" "Official BWAPI"
assert_revision "$repo_root/third_party/bwapi" "$expected_openbw_revision" "OpenBW BWAPI"

test -f "$patch_file" || { echo "Missing McRave port patch: $patch_file" >&2; exit 1; }

# The official checkout is an input to the 4.4 source-compatibility claim.
test -z "$(git -C "$repo_root/third_party/bwapi-official" status --porcelain --untracked-files=all)" || {
  echo "Official BWAPI checkout has uncommitted files" >&2
  exit 1
}

# build-arm64 is the expected local output; every other OpenBW checkout change
# could alter headers or the library linked into this module.
openbw_changes=$(git -C "$repo_root/third_party/bwapi" status --porcelain --untracked-files=all | sed '\#^?? build-arm64[^/]*/#d')
test -z "$openbw_changes" || {
  echo "OpenBW BWAPI checkout has uncommitted source files" >&2
  exit 1
}

test -z "$(git -C "$source_dir" ls-files --others -- Source)" || {
  echo "McRave Source contains untracked files that CMake would compile" >&2
  exit 1
}

if git -C "$source_dir" diff HEAD --quiet; then
  git -C "$source_dir" apply --check "$patch_file"
  git -C "$source_dir" apply "$patch_file"
fi

actual_patch=$(mktemp "${TMPDIR:-/tmp}/mcrave-patch.XXXXXX")
trap 'rm -f "$actual_patch"' EXIT HUP INT TERM
git -C "$source_dir" diff HEAD --binary > "$actual_patch"
cmp -s "$patch_file" "$actual_patch" || {
  echo "McRave tracked source diff does not exactly match $patch_file" >&2
  exit 1
}

"$cmake_bin" -S "$repo_root/ports/mcrave" -B "$build_dir" -G Ninja \
  -DCMAKE_CXX_COMPILER=/usr/bin/clang++ \
  -DCMAKE_BUILD_TYPE=Release \
  -DBWAPI_ROOT="$repo_root/third_party/bwapi" \
  -DBWAPI_BUILD="$repo_root/third_party/bwapi/build-arm64" \
  -DBWAPI_OFFICIAL_ROOT="$repo_root/third_party/bwapi-official"
"$cmake_bin" --build "$build_dir" --target McRaveOfficialHeaders --parallel 4
"$cmake_bin" --build "$build_dir" --parallel 4
python3 "$repo_root/scripts/write_mcrave_provenance.py" "$build_dir/McRave.dylib"
