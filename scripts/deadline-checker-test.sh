#!/usr/bin/env bash
# Test gauntlet for deadline-checker.py absorbed-state behavior.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
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

# --brief is what the guard prints. one line per deadline, nothing for an absorbed one.
DEADLINES_FILE="$T/deadlines.json" python3 scripts/deadline-checker.py --brief > "$T/brief.txt" 2>&1
check "brief keeps the section header" "Regulatory Compliance Deadline Status" "$T/brief.txt"
check "brief shows the overdue entry on one line" "^\[CRITICAL\] OVERDUE [0-9]+ days\. EU\. Law B" "$T/brief.txt"
ncheck "brief does not list absorbed entries" "Law A" "$T/brief.txt"
check "brief counts what it left out" "1 passed deadline" "$T/brief.txt"
ncheck "brief has no multi-line blocks" "Affected repository sections" "$T/brief.txt"
[ "$(wc -l < "$T/brief.txt")" -le 8 ] && echo "PASS brief output stays short" || { echo "FAIL brief output stays short ($(wc -l < "$T/brief.txt") lines)"; fails=$((fails+1)); }

cat > "$T/stores.json" <<'JSON'
{"deadlines":[
 {"id":"A","jurisdiction":"Apple App Store (Global)","law":"Apple rule","requirement":"r","effective_date":"2024-01-01","grace_period":"none","mandatory_date":"2025-06-01","enforcement_date":"2025-06-01","affected_repository_sections":"docs/Y.md","priority":"high"},
 {"id":"G","jurisdiction":"Google Play (Global)","law":"Play rule","requirement":"r","effective_date":"2024-01-01","grace_period":"none","mandatory_date":"2025-06-01","enforcement_date":"2025-06-01","affected_repository_sections":"docs/Y.md","priority":"high"},
 {"id":"E","jurisdiction":"European Union","law":"EU law","requirement":"r","effective_date":"2024-01-01","grace_period":"none","mandatory_date":"2025-06-01","enforcement_date":"2025-06-01","affected_repository_sections":"docs/Y.md","priority":"high"}
]}
JSON
DEADLINES_FILE="$T/stores.json" python3 scripts/deadline-checker.py --brief --platforms android > "$T/and.txt" 2>&1
check "platforms android keeps the Play deadline" "Play rule" "$T/and.txt"
check "platforms android keeps a law that binds every app" "EU law" "$T/and.txt"
ncheck "platforms android drops the Apple store deadline" "Apple rule" "$T/and.txt"
check "the dropped deadline is counted" "^1 deadline\(s\) for a store this project does not ship to" "$T/and.txt"
DEADLINES_FILE="$T/stores.json" python3 scripts/deadline-checker.py --brief --platforms ios,android > "$T/both.txt" 2>&1
check "both platforms keep the Apple deadline" "Apple rule" "$T/both.txt"
ncheck "both platforms leave nothing out" "does not ship to" "$T/both.txt"
DEADLINES_FILE="$T/stores.json" python3 scripts/deadline-checker.py --brief > "$T/none.txt" 2>&1
check "no platforms flag lists every store" "Apple rule" "$T/none.txt"

echo "----"
if [ "$fails" -eq 0 ]; then echo "deadline-checker-test: ALL PASS"; else echo "deadline-checker-test: $fails FAIL"; exit 1; fi
