#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
OUTPUT="$ROOT/public"
rm -rf "$OUTPUT"
mkdir -p "$OUTPUT"
python3 "$ROOT/scripts/export_dashboard.py" --root "$ROOT" --output "$OUTPUT"
