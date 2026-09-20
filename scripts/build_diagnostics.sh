#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
ENGINE="$ROOT/third_party/bwapi/build-arm64"
mkdir -p "$ROOT/build/bots"
for variant in WorkerRush Idle; do
    idle=0
    if [ "$variant" = Idle ]; then idle=1; fi
    clang++ -std=c++14 -O2 -Wall -Wextra -Werror -dynamiclib \
        -isystem "$ROOT/third_party/bwapi/bwapi/include" \
        -DDIAGNOSTIC_IDLE="$idle" "$ROOT/src/diagnostic_module.cpp" \
        -L"$ENGINE/lib" -lBWAPILIB -Wl,-rpath,"$ENGINE/lib" \
        -o "$ROOT/build/bots/$variant.dylib"
done
if [ -d "$ROOT/third_party/bwapi-official/bwapi/include" ]; then
    clang++ -std=c++14 -Wall -Wextra -Werror \
        -isystem "$ROOT/third_party/bwapi-official/bwapi/include" \
        -c "$ROOT/src/diagnostic_module.cpp" \
        -o "$ROOT/build/bots/diagnostic-official-4.4.o"
fi
