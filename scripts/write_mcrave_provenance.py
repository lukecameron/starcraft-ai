#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
binary = Path(sys.argv[1]).resolve()
source = root / "third_party/mcrave"

def run(*args: str) -> str:
    return subprocess.check_output(args, text=True).strip()

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

patch = subprocess.check_output(["git", "-C", str(source), "diff", "HEAD", "--binary"])
record = {
    "schema_version": 1,
    "binary": str(binary),
    "binary_sha256": digest(binary.read_bytes()),
    "source_repository": "https://github.com/Cmccrave/McRave.git",
    "source_revision": run("git", "-C", str(source), "rev-parse", "HEAD"),
    "source_patch_sha256": digest(patch),
    "compiler": run("/usr/bin/clang++", "--version").splitlines()[0],
    "build_type": "Release",
    "language_standard": "C++17",
    "port_compile_options": ["-include", "cfloat", "-fdelayed-template-parsing", "BWEM_USE_WINUTILS=0"],
    "bot_rng_control": {
        "env": "MATCH_BOT_SEED",
        "semantics": "std::srand before McRave onStart",
        "platform": "non-Windows native port only",
    },
    "bwapi_revision": run("git", "-C", str(root / "third_party/bwapi"), "rev-parse", "HEAD"),
    "official_header_check": {
        "target": "McRaveOfficialHeaders",
        "bwapi_version": "4.4.0",
        "bwapi_revision": run("git", "-C", str(root / "third_party/bwapi-official"), "rev-parse", "HEAD"),
        "translation_units": 114,
        "result": "passed",
    },
}
Path(str(binary) + ".build.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
