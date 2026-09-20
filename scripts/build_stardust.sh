#!/bin/sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
source_dir="$repo_root/third_party/stardust"
patch_file="$repo_root/patches/stardust-native-arm64.patch"
build_dir="$repo_root/build/stardust"
cmake_bin=${CMAKE_BIN:-"$repo_root/.tools/engine/bin/cmake"}
PATH="$repo_root/.tools/engine/bin:$PATH"

expected_stardust_revision=22d93d7a55d0a0494384474a456fd7ee26baee97
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

assert_revision "$source_dir" "$expected_stardust_revision" Stardust
assert_revision "$repo_root/third_party/bwapi-official" "$expected_official_revision" "Official BWAPI"
assert_revision "$repo_root/third_party/bwapi" "$expected_openbw_revision" "OpenBW BWAPI"
test -f "$patch_file" || { echo "Missing Stardust port patch: $patch_file" >&2; exit 1; }

test -z "$(git -C "$repo_root/third_party/bwapi-official" status --porcelain --untracked-files=all)" || {
  echo "Official BWAPI checkout has uncommitted files" >&2
  exit 1
}
openbw_changes=$(git -C "$repo_root/third_party/bwapi" status --porcelain --untracked-files=all | sed '\#^?? build-arm64[^/]*/#d')
test -z "$openbw_changes" || {
  echo "OpenBW BWAPI checkout has uncommitted source files" >&2
  exit 1
}
test -z "$(git -C "$source_dir" ls-files --others -- src 3rdparty/BWEM 3rdparty/FAP 3rdparty/nlohmann 3rdparty/bitsery 3rdparty/cppcrc 3rdparty/zstd 3rdparty/zstdstream)" || {
  echo "Stardust contains untracked compiled source files" >&2
  exit 1
}

if git -C "$source_dir" diff HEAD --quiet; then
  git -C "$source_dir" apply --check "$patch_file"
  git -C "$source_dir" apply "$patch_file"
fi
actual_patch=$(mktemp "${TMPDIR:-/tmp}/stardust-patch.XXXXXX")
trap 'rm -f "$actual_patch"' EXIT HUP INT TERM
git -C "$source_dir" diff HEAD --binary > "$actual_patch"
cmp -s "$patch_file" "$actual_patch" || {
  echo "Stardust tracked source diff does not exactly match $patch_file" >&2
  exit 1
}

"$cmake_bin" -S "$repo_root/ports/stardust" -B "$build_dir" -G Ninja \
  -DCMAKE_CXX_COMPILER=/usr/bin/clang++ \
  -DCMAKE_BUILD_TYPE=Release \
  -DSTARDUST_SOURCE_ROOT="$source_dir" \
  -DBWAPI_ROOT="$repo_root/third_party/bwapi" \
  -DBWAPI_BUILD="$repo_root/third_party/bwapi/build-arm64" \
  -DBWAPI_OFFICIAL_ROOT="$repo_root/third_party/bwapi-official"
"$cmake_bin" --build "$build_dir" --target StardustOfficialHeaders --parallel 4
"$cmake_bin" --build "$build_dir" --target Stardust --parallel 4

python3 - "$build_dir/Stardust.dylib" "$patch_file" <<'PY'
import hashlib, json, pathlib, subprocess, sys
binary, patch = map(pathlib.Path, sys.argv[1:])
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
compiler = subprocess.check_output(['/usr/bin/clang++', '--version'], text=True).splitlines()[0]
data = {
    'schema_version': 1,
    'source_repository': 'https://github.com/bmnielsen/Stardust.git',
    'source_revision': '22d93d7a55d0a0494384474a456fd7ee26baee97',
    'source_patch': 'patches/stardust-native-arm64.patch',
    'source_patch_sha256': sha(patch),
    'binary': str(binary),
    'binary_sha256': sha(binary),
    'build_type': 'Release',
    'compiler': compiler,
    'language_standard': 'C++20',
    'bwapi_revision': '48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2',
    'api_mode': 'standard BWAPI path; Stardust bundled OpenBW ABI excluded',
    'official_header_check': {
        'bwapi_revision': '7687da8abc4726f8366401f11ab648d421385793',
        'bwapi_version': '4.4.0',
        'target': 'StardustOfficialHeaders',
        'result': 'passed'
    },
    'license_submission_condition': 'public StarCraft tournament submission requires written author permission'
}
binary.with_suffix(binary.suffix + '.build.json').write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')
PY
