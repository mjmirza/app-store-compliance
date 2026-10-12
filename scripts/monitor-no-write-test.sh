#!/usr/bin/env bash
# Issue 843. Every monitor says whether its items are live or sample, and writes no file unless asked.
set -uo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad() { FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT

for m in regulatory android ai-policy privacy security standards; do
  W="$T/$m"; mkdir -p "$W/app"; cd "$W" || exit 1
  flag="--dir"; [ "$m" = "regulatory" ] && flag="--project"
  OUT="$(python3 "$REPO/scripts/monitor-$m.py" "$flag" app 2>&1)"; RC=$?
  N="$(printf '%s\n' "$OUT" | grep -cE '^Data\. (sample|live) ')"
  [ "$RC" -eq 0 ] && [ "$N" -eq 1 ] && ok "$m says once whether its items are live or sample" || bad "$m says once whether its items are live or sample (rc=$RC lines=$N)"
  printf '%s\n' "$OUT" | grep -qE '^Data\. sample ' && ok "$m run with no feed flag is labelled sample" || bad "$m run with no feed flag is labelled sample"
  FILES="$(find "$W" -type f | wc -l | tr -d ' ')"
  [ "$FILES" -eq 0 ] && ok "$m writes no file when no output flag is passed" || bad "$m writes no file when no output flag is passed (files=$FILES)"
  [ "$m" = "regulatory" ] && continue
  printf '%s\n' "$OUT" | grep -q '^No file written\. ' && ok "$m says how to save the report" || bad "$m says how to save the report"
  python3 "$REPO/scripts/monitor-$m.py" --dir app --output-docs "$W/out/report.md" >/dev/null 2>&1
  [ -s "$W/out/report.md" ] && ok "$m writes the report when the output flag is passed" || bad "$m writes the report when the output flag is passed"
done

cd "$T/regulatory" || exit 1
python3 "$REPO/scripts/monitor-regulatory.py" --project app --json 2>"$T/err.txt" | python3 -c 'import json,sys; json.load(sys.stdin)' \
  && grep -qE '^Data\. sample ' "$T/err.txt" && ok "regulatory json stays parseable and the data line goes to stderr" || bad "regulatory json stays parseable and the data line goes to stderr"
for m in privacy security standards; do
  cd "$T/$m" || exit 1
  python3 "$REPO/scripts/monitor-$m.py" --dir app --pr-output "$T/$m/pr/draft.md" >/dev/null 2>&1
  [ -s "$T/$m/pr/draft.md" ] && ok "$m writes the PR draft when its flag is passed" || bad "$m writes the PR draft when its flag is passed"
done

echo ""
echo "monitor-no-write-test: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
