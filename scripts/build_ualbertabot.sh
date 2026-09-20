#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
source_dir="$root/third_party/ualbertabot"
patch_file="$root/patches/ualbertabot-native-arm64.patch"
build_dir="$root/build/ualbertabot"
output="$build_dir/UAlbertaBot.dylib"
expected_source=558899d8793456f4a6ec4196efbb5235552e24db
expected_bwapi=48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2
expected_official=7687da8abc4726f8366401f11ab648d421385793

test "$(git -C "$source_dir" rev-parse HEAD)" = "$expected_source" || { echo "unexpected UAlbertaBot revision" >&2; exit 1; }
test "$(git -C "$root/third_party/bwapi" rev-parse HEAD)" = "$expected_bwapi" || { echo "unexpected OpenBW BWAPI revision" >&2; exit 1; }
test "$(git -C "$root/third_party/bwapi-official" rev-parse HEAD)" = "$expected_official" || { echo "unexpected official BWAPI revision" >&2; exit 1; }

check_clean_headers() {
  checkout=$1
  if ! git -C "$checkout" diff HEAD --quiet -- bwapi/include ||
     test -n "$(git -C "$checkout" ls-files --others --exclude-standard -- bwapi/include)" ||
     test -n "$(git -C "$checkout" ls-files --others --ignored --exclude-standard -- bwapi/include)"; then
    echo "dirty or untracked BWAPI headers in $checkout" >&2
    exit 1
  fi
}
check_clean_headers "$root/third_party/bwapi"
check_clean_headers "$root/third_party/bwapi-official"

source_paths='UAlbertaBot/Source BOSS/source SparCraft/source'
untracked=$(git -C "$source_dir" ls-files --others --exclude-standard -- $source_paths)
ignored=$(git -C "$source_dir" ls-files --others --ignored --exclude-standard -- $source_paths)
test -z "$untracked$ignored" || { echo "untracked or ignored files exist in compiled source roots" >&2; printf '%s\n%s\n' "$untracked" "$ignored" >&2; exit 1; }

if git -C "$source_dir" diff HEAD --quiet; then
  git -C "$source_dir" apply "$patch_file"
fi

actual=$(mktemp "${TMPDIR:-/tmp}/ualberta-actual.XXXXXX")
expected=$(mktemp "${TMPDIR:-/tmp}/ualberta-expected.XXXXXX")
trap 'rm -f "$actual" "$expected"' EXIT HUP INT TERM
git -C "$source_dir" diff HEAD --binary --no-ext-diff | sed -e 's/\r$//' -e '${/^$/d;}' > "$actual"
sed -e 's/\r$//' -e '${/^$/d;}' "$patch_file" > "$expected"
cmp -s "$expected" "$actual" || { echo "UAlbertaBot tracked changes do not exactly match the native patch" >&2; exit 1; }

"$root/.tools/engine/bin/cmake" -S "$root/ports/ualbertabot" -B "$build_dir" -G Ninja \
  -DCMAKE_MAKE_PROGRAM="$root/.tools/engine/bin/ninja" -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_CXX_COMPILER=/usr/bin/clang++ \
  -DUALBERTA_SOURCE="$source_dir" -DBWAPI_ROOT="$root/third_party/bwapi" \
  -DBWAPI_BUILD="$root/third_party/bwapi/build-arm64" \
  -DBWAPI_OFFICIAL_ROOT="$root/third_party/bwapi-official"
"$root/.tools/engine/bin/cmake" --build "$build_dir" --target UAlbertaBotOfficialHeaders --parallel 4
"$root/.tools/engine/bin/cmake" --build "$build_dir" --parallel 4

mkdir -p "$build_dir/AI"
cp "$root/ports/ualbertabot/UAlbertaBot_Config.txt" "$build_dir/AI/UAlbertaBot_Config.txt"

patch_sha=$(shasum -a 256 "$patch_file" | awk '{print $1}')
config_sha=$(shasum -a 256 "$root/ports/ualbertabot/UAlbertaBot_Config.txt" | awk '{print $1}')
binary_sha=$(shasum -a 256 "$output" | awk '{print $1}')
compiler=$(/usr/bin/clang++ --version | head -n 1)
cat > "$output.build.json" <<EOF
{
  "schema_version": 1,
  "source_repository": "https://github.com/davechurchill/ualbertabot.git",
  "source_revision": "$expected_source",
  "source_patch": "patches/ualbertabot-native-arm64.patch",
  "source_patch_sha256": "$patch_sha",
  "config_sha256": "$config_sha",
  "bwapi_revision": "$expected_bwapi",
  "official_bwapi_revision": "$expected_official",
  "official_header_check": "passed",
  "official_header_translation_units": 115,
  "ai_files": [
    {
      "path": "UAlbertaBot_Config.txt",
      "sha256": "$config_sha"
    }
  ],
  "compiler": "$compiler",
  "cxx_standard": "C++14",
  "cmake_build_type": "Release",
  "max_parallel_jobs": 4,
  "binary_sha256": "$binary_sha"
}
EOF
echo "$output"
