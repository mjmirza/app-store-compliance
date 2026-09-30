#!/usr/bin/env bash
# Pins release-audit.py against counting deadline-checker lines as findings.
# A tiny app with one placeholder and no privacy policy must not report criticals.

set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

PASS=0
FAIL=0
ok()  { PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad() { FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

FX="$(mktemp -d)"
trap 'rm -rf "$FX"' EXIT
mkdir -p "$FX/App"
printf '<plist><dict><key>NSCameraUsageDescription</key><string>camera</string></dict></plist>\n' > "$FX/App/Info.plist"
printf 'let s = "lorem ipsum"\n' > "$FX/App/A.swift"

BEFORE="$(git status --porcelain)"
OUT="$(python3 scripts/release-audit.py "$FX" 2>&1)"
AFTER="$(git status --porcelain)"
REPORT="$FX/RELEASE-READINESS-REPORT.md"

[ -f "$REPORT" ] && ok "report is written into the audited project" || bad "report missing from the audited project"
[ "$BEFORE" = "$AFTER" ] && ok "the playbook repository is left untouched" || bad "the audit changed files in this repository"

SUMMARY="$(printf '%s\n' "$OUT" | grep -E '^Summary: ' | tail -1)"
echo "$SUMMARY" | grep -q 'critical=0 ' && ok "no critical findings on a harmless app ($SUMMARY)" || bad "unexpected criticals ($SUMMARY)"

grep -q 'BOTH-PLACEHOLDER' "$REPORT" 2>/dev/null && ok "the real placeholder finding is still reported" || bad "placeholder finding lost"

TOTAL="$(echo "$SUMMARY" | grep -oE '[0-9]+' | awk '{t+=$1} END {print t+0}')"
IDS="$(grep -oE '\b[A-Z]+(-[A-Z0-9.]+)+\b' "$REPORT" 2>/dev/null | sort -u | wc -l | tr -d ' ')"
[ "${TOTAL:-x}" = "$IDS" ] && ok "every counted finding has a real hyphenated id ($TOTAL)" || bad "finding count $TOTAL does not match $IDS real ids"

# A target path that does not exist is an error, never a silent audit of this playbook.
OUT="$(python3 scripts/release-audit.py "$FX/no-such-app" 2>&1)"; RC=$?
[ "$RC" -eq 1 ] && echo "$OUT" | grep -q "not a directory" && ! echo "$OUT" | grep -q "Starting Release Readiness" && ok "a missing target path is rejected before any scan" || bad "a missing target path is rejected before any scan (rc=$RC)"

# The audit runs the playbook's own tests first, which is slow. The reader is told how long before the wait.
FIRST="$(python3 scripts/release-audit.py "$FX/no-such-app" 2>&1; sed -n '/Starting Release Readiness/,/Scanning your app/p' scripts/release-audit.py)"
echo "$FIRST" | grep -q "about two minutes" && ok "the slow self-check step says how long it takes" || bad "the slow self-check step says how long it takes"

# A finding whose title contains "(mandatory " is a finding. Only deadline lines, which carry a date there, are skipped.
python3 - <<'PYT' && ok "only deadline lines are dropped from the finding list" || bad "only deadline lines are dropped from the finding list"
import importlib.util, sys
spec = importlib.util.spec_from_file_location("ra", "scripts/release-audit.py")
ra = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ra)
keep = "  [HIGH]     BOTH-PLACEHOLDER  Placeholder text (mandatory disclosure) found"
keep2 = "  [HIGH]     BOTH-SOME-RULE  A title that quotes a date (mandatory 2026-10-15)"
drop = [
    "[CRITICAL] OVERDUE 12 days. EU. Some Act (mandatory 2026-09-18)",
    "[HIGH] in 3 days. Apple. Thing (mandatory 2026-10-03)",
    "[HIGH] EU AI Act (mandatory 2025-02-02) absorbed into docs/EU.md",
]
fn = getattr(ra, "is_deadline_line", None)
sys.exit(0 if fn and not fn(keep) and not fn(keep2) and all(fn(d) for d in drop) else 1)
PYT

echo "release-audit-test: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
