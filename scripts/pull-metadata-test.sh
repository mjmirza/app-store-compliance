#!/usr/bin/env bash
# Exercise pull failures without using Apple or Google credentials or clients.
set -euo pipefail
SCRIPT="$(cd "$(dirname "$0")" && pwd)/pull-metadata.sh"
T="$(mktemp -d)"
trap 'rm -rf -- "$T"' EXIT
mkdir "$T/bin" "$T/home"
cat > "$T/bin/asc" <<'ASC'
#!/bin/bash
exit "${ASC_STATUS:-0}"
ASC
cat > "$T/bin/curl" <<'CURL'
#!/bin/bash
case "$*" in
  *'-X POST '*) printf '{"id":"fixture-edit"}\n' ;;
  *'-X DELETE '*) printf 'delete\n' >> "$CALLS" ;;
  *'/listings')
    case "$LISTINGS_MODE" in
      transport) exit 22 ;;
      malformed) echo '{not json' ;;
      *) printf '{"listings":[{"language":"en-US","title":"Fixture listing"}]}\n' ;;
    esac ;;
  *) exit 99 ;;
esac
CURL
chmod +x "$T/bin/asc" "$T/bin/curl"
export PATH="$T/bin:$PATH" HOME="$T/home" DIR="$T/output" CALLS="$T/calls"
export APP_ID=fixture VERSION=fixture PACKAGE_NAME=com.example.fixture GOOGLE_ACCESS_TOKEN=fixture
if ASC_STATUS=9 bash "$SCRIPT" apple > "$T/out" 2>&1; then
  echo 'Apple pull hid a failed asc command'; exit 1
fi
! grep -q '^Done\.' "$T/out"
ASC_STATUS=0 bash "$SCRIPT" apple > "$T/out" 2>&1
grep -q '^Done\.' "$T/out"
for mode in transport malformed; do
  : > "$CALLS"
  if LISTINGS_MODE="$mode" bash "$SCRIPT" google > "$T/out" 2>&1; then
    echo "Play pull hid a $mode failure"; exit 1
  fi
  ! grep -q '^Done\.' "$T/out"
  test "$(cat "$CALLS")" = delete
done
: > "$CALLS"
LISTINGS_MODE=good bash "$SCRIPT" google > "$T/out" 2>&1
test "$(cat "$DIR/en-US/name.txt")" = 'Fixture listing'
test "$(cat "$CALLS")" = delete
grep -q '^Done\.' "$T/out"
echo 'pull-metadata-test: Apple and Play failures propagate; both successful paths still work; temporary Play edits are deleted.'
