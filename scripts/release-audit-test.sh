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

echo "release-audit-test: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
