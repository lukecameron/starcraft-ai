#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
source_dir="$root/bots/kestrel"
build_dir="$root/build/kestrel"
output="$build_dir/Kestrel.dylib"
expected_bwapi_revision=48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2

test "$(git -C "$root/third_party/bwapi" rev-parse HEAD)" = "$expected_bwapi_revision" || {
  echo "OpenBW BWAPI checkout is not at $expected_bwapi_revision" >&2
  exit 1
}
test -z "$(git -C "$root/third_party/bwapi" status --short --untracked-files=no)" || {
  echo "OpenBW BWAPI tracked source must be clean" >&2
  exit 1
}

"$root/.tools/engine/bin/cmake" -S "$source_dir" -B "$build_dir" -G Ninja \
  -DBWAPI_ROOT="$root/third_party/bwapi" \
  -DBWAPI_BUILD="$root/third_party/bwapi/build-arm64" \
  -DBWAPI_OFFICIAL_ROOT="$root/third_party/bwapi-official" \
  -DCMAKE_MAKE_PROGRAM="$root/.tools/engine/bin/ninja" \
  -DCMAKE_CXX_COMPILER=/usr/bin/clang++ \
  -DCMAKE_BUILD_TYPE=Release
"$root/.tools/engine/bin/cmake" --build "$build_dir" --target KestrelOfficialHeaders --parallel 4
"$root/.tools/engine/bin/cmake" --build "$build_dir" --target Kestrel --parallel 4

source_sha=$(cat "$source_dir/Kestrel.cpp" "$source_dir/CMakeLists.txt" "$source_dir/LICENSE" | shasum -a 256 | awk '{print $1}')
binary_sha=$(shasum -a 256 "$output" | awk '{print $1}')
compiler=$(/usr/bin/clang++ --version | head -n 1)
cat > "$output.build.json" <<EOF
{
  "schema_version": 1,
  "name": "Kestrel",
  "ownership": "project",
  "origin": "original",
  "source_files": ["bots/kestrel/Kestrel.cpp", "bots/kestrel/CMakeLists.txt", "bots/kestrel/LICENSE"],
  "source_sha256": "$source_sha",
  "bwapi_revision": "$expected_bwapi_revision",
  "compiler": "$compiler",
  "cmake_build_type": "Release",
  "cxx_standard": "C++14",
  "max_parallel_jobs": 4,
  "official_bwapi_headers": "compiled",
  "binary_sha256": "$binary_sha"
}
EOF

echo "$output"
