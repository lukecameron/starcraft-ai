#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
LOCK="$ROOT/dashboard/.publish.lock"
STATUS="$ROOT/dashboard/deploy-status.json"
LOG_DIR="$ROOT/artifacts/deployments"
mkdir -p "$LOG_DIR"

if ! mkdir "$LOCK" 2>/dev/null; then
  old_pid=$(cat "$LOCK/pid" 2>/dev/null || true)
  if [ -n "$old_pid" ] && kill -0 "$old_pid" 2>/dev/null; then
    echo "dashboard publish already running as pid $old_pid" >&2
    exit 3
  fi
  rm -f "$LOCK/pid"
  rmdir "$LOCK" 2>/dev/null || { echo "dashboard publish lock is stale but not empty: $LOCK" >&2; exit 3; }
  mkdir "$LOCK"
fi
printf '%s\n' "$$" >"$LOCK/pid"
cleanup() { rm -f "$LOCK/pid"; rmdir "$LOCK" 2>/dev/null || true; }
started=$(date -u +%Y-%m-%dT%H:%M:%SZ)
phase=build
interrupted() {
  printf '{"started_at":"%s","finished_at":"%s","phase":"%s","status":130}\n' "$started" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$phase" >"$STATUS.tmp"
  mv "$STATUS.tmp" "$STATUS"
  exit 130
}
trap cleanup EXIT
trap interrupted HUP INT TERM

stamp=$(date -u +%Y%m%dT%H%M%SZ)
log="$LOG_DIR/pages-$stamp.log"
if ! "$ROOT/scripts/build-pages.sh" >"$log" 2>&1; then
  printf '{"finished_at":"%s","phase":"build","status":1,"log":"%s"}\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$log" >"$STATUS.tmp"
  mv "$STATUS.tmp" "$STATUS"
  cat "$log"
  exit 1
fi

cd "$ROOT"
phase=deploy
set +e
npx wrangler pages deploy "$ROOT/public" --project-name starcraft-ai --branch main "$@" >>"$log" 2>&1
deploy_status=$?
set -e
cat "$log"
if [ "$deploy_status" -ne 0 ]; then
  printf '{"started_at":"%s","finished_at":"%s","phase":"deploy","status":%s,"log":"%s"}\n' "$started" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$deploy_status" "$log" >"$STATUS.tmp"
  mv "$STATUS.tmp" "$STATUS"
  exit "$deploy_status"
fi

deployment_url=$(grep -Eo 'https://[^[:space:]]+\.pages\.dev' "$log" | tail -1)
if [ -z "$deployment_url" ]; then
  printf '{"started_at":"%s","finished_at":"%s","phase":"capture_url","status":1,"log":"%s"}\n' "$started" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$log" >"$STATUS.tmp"
  mv "$STATUS.tmp" "$STATUS"
  echo "wrangler succeeded but no immutable deployment URL was found" >&2
  exit 1
fi
phase=rewrite_snapshot
if ! python3 "$ROOT/scripts/export_dashboard.py" --root "$ROOT" --rewrite-replay-base "$deployment_url" >>"$log" 2>&1; then
  printf '{"started_at":"%s","finished_at":"%s","phase":"rewrite_snapshot","status":1,"deployment_url":"%s","log":"%s"}\n' "$started" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$deployment_url" "$log" >"$STATUS.tmp"
  mv "$STATUS.tmp" "$STATUS"
  exit 1
fi
printf '{"started_at":"%s","finished_at":"%s","phase":"complete","status":0,"deployment_url":"%s","log":"%s"}\n' "$started" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$deployment_url" "$log" >"$STATUS.tmp"
mv "$STATUS.tmp" "$STATUS"
printf '%s\n' "$deployment_url"
