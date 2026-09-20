#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
source_dir="$root/third_party/zzzkbot"
patch_file="$root/patches/zzzkbot-native-arm64.patch"
build_dir="$root/build/zzzkbot"
output="$build_dir/lib/ZZZKBot.dylib"
expected_revision=7183e37b6b416ea53c1040c83e639a3a3c395eed
expected_bwapi_revision=48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2

test "$(git -C "$source_dir" rev-parse HEAD)" = "$expected_revision" || {
  echo "ZZZKBot checkout is not at $expected_revision" >&2
  exit 1
}

test "$(git -C "$root/third_party/bwapi" rev-parse HEAD)" = "$expected_bwapi_revision" || {
  echo "OpenBW BWAPI checkout is not at $expected_bwapi_revision" >&2
  exit 1
}

if git -C "$source_dir" diff HEAD --quiet && test -z "$(git -C "$source_dir" ls-files --others -- 'ZZZKBot/Source/*')"; then
  git -C "$source_dir" apply --ignore-space-change "$patch_file"
fi

untracked_sources=$(git -C "$source_dir" ls-files --others -- 'ZZZKBot/Source/*')
test -z "$untracked_sources" || {
  echo "ZZZKBot compiled source tree contains untracked files:" >&2
  echo "$untracked_sources" >&2
  exit 1
}

actual_patch=$(mktemp "${TMPDIR:-/tmp}/zzzkbot-actual.XXXXXX")
expected_patch=$(mktemp "${TMPDIR:-/tmp}/zzzkbot-expected.XXXXXX")
trap 'rm -f "$actual_patch" "$expected_patch"' EXIT HUP INT TERM
git -C "$source_dir" diff HEAD --ignore-space-at-eol --binary --no-ext-diff | sed -e 's/\r$//' -e '${/^$/d;}' > "$actual_patch"
sed -e 's/\r$//' -e '${/^$/d;}' "$patch_file" > "$expected_patch"
if ! cmp -s "$expected_patch" "$actual_patch"; then
  echo "ZZZKBot tracked changes do not exactly match $patch_file" >&2
  exit 1
fi

"$root/.tools/engine/bin/cmake" -S "$root/ports/zzzkbot" -B "$build_dir" -G Ninja \
  -DZZZKBOT_SOURCE_DIR="$source_dir" \
  -DOPENBW_BWAPI_DIR="$root/third_party/bwapi" \
  -DOPENBW_BWAPI_BUILD_DIR="$root/third_party/bwapi/build-arm64" \
  -DCMAKE_MAKE_PROGRAM="$root/.tools/engine/bin/ninja" \
  -DCMAKE_CXX_COMPILER=/usr/bin/clang++ \
  -DCMAKE_BUILD_TYPE=Release
"$root/.tools/engine/bin/cmake" --build "$build_dir" --parallel 4

patch_sha=$(shasum -a 256 "$patch_file" | awk '{print $1}')
binary_sha=$(shasum -a 256 "$output" | awk '{print $1}')
compiler=$(/usr/bin/clang++ --version | head -n 1)
cat > "$output.build.json" <<EOF
{
  "schema_version": 1,
  "source_repository": "https://github.com/chriscoxe/ZZZKBot.git",
  "source_revision": "$expected_revision",
  "source_patch": "patches/zzzkbot-native-arm64.patch",
  "source_patch_sha256": "$patch_sha",
  "bwapi_revision": "$expected_bwapi_revision",
  "compiler": "$compiler",
  "cmake_build_type": "Release",
  "cxx_standard": "C++14",
  "max_parallel_jobs": 4,
  "binary_sha256": "$binary_sha"
}
EOF

echo "$output"
