#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
source_dir="$root/bots/kestrel-modular-v1"
build_dir="$root/build/kestrel-modular-v1"
output="$build_dir/KestrelModular.dylib"
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
"$root/.tools/engine/bin/cmake" --build "$build_dir" --target KestrelModularOfficialHeaders --parallel 4
"$root/.tools/engine/bin/cmake" --build "$build_dir" --target KestrelModular KestrelModularUnitTests --parallel 4
"$root/.tools/engine/bin/ctest" --test-dir "$build_dir" --output-on-failure

python3 - "$root" "$output" "$expected_bwapi_revision" <<'PY'
import hashlib
import json
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
output = Path(sys.argv[2])
revision = sys.argv[3]
source_root = root / "bots/kestrel-modular-v1"
source_files = sorted(
    path for path in source_root.rglob("*")
    if path.is_file() and path.name not in {".DS_Store"}
)
source_digest = hashlib.sha256()
relative_files = []
for path in source_files:
    relative = path.relative_to(root).as_posix()
    relative_files.append(relative)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    source_digest.update(f"{digest}  {relative}\n".encode())

binary_sha = hashlib.sha256(output.read_bytes()).hexdigest()
compiler = subprocess.run(
    ["/usr/bin/clang++", "--version"], check=True, capture_output=True, text=True
).stdout.splitlines()[0]
record = {
    "schema_version": 1,
    "name": "Kestrel Modular v1",
    "ownership": "project",
    "origin": "original",
    "source_files": relative_files,
    "source_manifest_sha256": source_digest.hexdigest(),
    "bwapi_revision": revision,
    "compiler": compiler,
    "cmake_build_type": "Release",
    "cxx_standard": "C++14",
    "max_parallel_jobs": 4,
    "official_bwapi_headers": "compiled",
    "unit_tests": "passed",
    "binary_sha256": binary_sha,
}
Path(str(output) + ".build.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
PY

echo "$output"
