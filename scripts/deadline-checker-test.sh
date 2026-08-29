#!/usr/bin/env bash
# Test gauntlet for deadline-checker.py absorbed-state behavior.
set -uo pipefail
cd "$(dirname "$0")/.."
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
fails=0
check() { # name, expected, haystack-file
  if grep -qE "$2" "$3"; then echo "PASS $1"; else echo "FAIL $1 (wanted /$2/)"; fails=$((fails+1)); fi
}
ncheck() {
  if grep -qE "$2" "$3"; then echo "FAIL $1 (must NOT match /$2/)"; fails=$((fails+1)); else echo "PASS $1"; fi
}

cat > "$T/deadlines.json" <<'JSON'
{"version":"test","updated":"2026-01-01","description":"fixture","deadlines":[
 {"id":"PAST-ABSORBED","jurisdiction":"EU","law":"Law A","requirement":"Req A",
  "effective_date":"2024-01-01","grace_period":"none","mandatory_date":"2025-01-01",
  "enforcement_date":"2025-01-01","affected_repository_sections":"docs/X.md",
  "priority":"high","absorbed_into":"docs/X.md section 2"},
 {"id":"PAST-OPEN","jurisdiction":"EU","law":"Law B","requirement":"Req B",
  "effective_date":"2024-01-01","grace_period":"none","mandatory_date":"2025-06-01",
  "enforcement_date":"2025-06-01","affected_repository_sections":"docs/Y.md",
  "priority":"critical"},
 {"id":"FUTURE-FAR","jurisdiction":"US","law":"Law C","requirement":"Req C",
  "effective_date":"2026-01-01","grace_period":"none","mandatory_date":"2030-01-01",
  "enforcement_date":"2030-01-01","affected_repository_sections":"docs/Z.md",
  "priority":"medium"}
]}
JSON

DEADLINES_FILE="$T/deadlines.json" python3 scripts/deadline-checker.py > "$T/out.txt" 2>&1

check "absorbed entry listed as absorbed one-liner" "ABSORBED" "$T/out.txt"
check "absorbed entry names its coverage" "docs/X.md section 2" "$T/out.txt"
ncheck "absorbed entry not in loud action block" "Law A" <(grep -A3 "Action Required" "$T/out.txt" | head -40)
check "unabsorbed past entry still loud" "Law B" "$T/out.txt"
check "unabsorbed past entry marked overdue" "days overdue" "$T/out.txt"
ncheck "far-future entry silent" "Law C" "$T/out.txt"

# malformed file fails open with error, exit 0
echo "{bad" > "$T/bad.json"
DEADLINES_FILE="$T/bad.json" python3 scripts/deadline-checker.py > "$T/out2.txt" 2>&1
check "malformed data fails open" "No deadlines loaded|Error loading" "$T/out2.txt"

echo "----"
if [ "$fails" -eq 0 ]; then echo "deadline-checker-test: ALL PASS"; else echo "deadline-checker-test: $fails FAIL"; exit 1; fi
