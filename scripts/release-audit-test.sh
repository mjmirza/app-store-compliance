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
OUT="$(python3 scripts/release-audit.py "$FX" 2>&1)"; RUN_RC=$?
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

# The harmless app above has a high placeholder finding and no listing, so it is never cleared.
[ "$RUN_RC" -ne 0 ] && ! echo "$OUT" | grep -q "CLEAR TO SUBMIT" && ok "an app with a high finding is not cleared to submit" || bad "an app with a high finding is not cleared to submit (rc=$RUN_RC)"

# The installed layout. scripts sit in skills/app-store-compliance and the guard sits in hooks, with no agent-os folder.
W="$(mktemp -d)"
SK="$W/c/skills/app-store-compliance"
mkdir -p "$SK" "$W/c/hooks"
cp -R data docs references templates scripts VERSION "$SK/"
cp agent-os/hooks/app-store-compliance-guard.sh "$W/c/hooks/"
CL="$W/clean"; mkdir -p "$CL/en-US"
printf 'Lumina Studio' > "$CL/en-US/name.txt"
printf 'A focused editor with layers and presets.' > "$CL/en-US/description.txt"
printf '{"privacy_policy_url":"https://lumina.app/privacy","support_url":"https://lumina.app/support"}' > "$CL/m.json"
NOMETA="$W/nometa"; mkdir -p "$NOMETA"; printf 'let a = 1\n' > "$NOMETA/A.swift"
STUB_PASS="$W/pass.sh"; printf '#!/usr/bin/env bash\necho "app-store-compliance-guard. 0 critical risks"\nexit 0\n' > "$STUB_PASS"
STUB_NC="$W/nc.sh"; printf '#!/usr/bin/env bash\necho "NOT CHECKED. No iOS or Android project was found."\nexit 1\n' > "$STUB_NC"
STUB_HIGH="$W/high.sh"; printf '#!/usr/bin/env bash\necho "  [HIGH]     BOTH-PLACEHOLDER  Placeholder text found"\necho "      fix. Replace placeholder text"\nexit 0\n' > "$STUB_HIGH"
STUB_ERR="$W/err.sh"; printf '#!/usr/bin/env bash\necho "guard crashed" >&2\nexit 2\n' > "$STUB_ERR"

OUT="$(python3 "$SK/scripts/release-audit.py" "$CL" 2>&1)"
echo "$OUT" | grep -qF "Guard. $W/c/hooks/app-store-compliance-guard.sh" && echo "$OUT" | grep -q "Scanning your app" && ! echo "$OUT" | grep -q "guard tests failed" && ok "the installed layout finds the installed guard and never needs its test file" || bad "the installed layout finds the installed guard and never needs its test file"

OUT="$(APP_STORE_GUARD_PATH="$STUB_PASS" python3 "$SK/scripts/release-audit.py" "$CL" 2>&1)"; RC=$?
[ "$RC" -eq 0 ] && echo "$OUT" | grep -q "Overall Status: PASSED" && ok "a clean app with complete scans passes the gate" || bad "a clean app with complete scans passes the gate (rc=$RC)"

OUT="$(APP_STORE_GUARD_PATH="$STUB_HIGH" python3 "$SK/scripts/release-audit.py" "$CL" 2>&1)"; RC=$?
[ "$RC" -eq 2 ] && echo "$OUT" | grep -q "Overall Status: BLOCKED" && ! echo "$OUT" | grep -q "CLEAR TO SUBMIT" && ok "a single high finding blocks the release" || bad "a single high finding blocks the release (rc=$RC)"

OUT="$(APP_STORE_GUARD_PATH="$STUB_NC" python3 "$SK/scripts/release-audit.py" "$CL" 2>&1)"; RC=$?
[ "$RC" -ne 0 ] && ! echo "$OUT" | grep -q "Overall Status: PASSED" && ! echo "$OUT" | grep -q "CLEAR TO SUBMIT" && echo "$OUT" | grep -q "NOT CHECKED" && ok "a guard that did not check the app fails the gate" || bad "a guard that did not check the app fails the gate (rc=$RC)"

OUT="$(APP_STORE_GUARD_PATH="$STUB_ERR" python3 "$SK/scripts/release-audit.py" "$CL" 2>&1)"; RC=$?
[ "$RC" -ne 0 ] && ! echo "$OUT" | grep -q "Overall Status: PASSED" && echo "$OUT" | grep -q "guard crashed" && ok "a guard error fails the gate and keeps its diagnostics" || bad "a guard error fails the gate and keeps its diagnostics (rc=$RC)"

OUT="$(APP_STORE_GUARD_PATH="$STUB_PASS" python3 "$SK/scripts/release-audit.py" "$NOMETA" 2>&1)"; RC=$?
[ "$RC" -ne 0 ] && ! echo "$OUT" | grep -q "Overall Status: PASSED" && echo "$OUT" | grep -q "Nothing was audited" && ok "a listing that was not audited fails the gate" || bad "a listing that was not audited fails the gate (rc=$RC)"

OUT="$(APP_STORE_GUARD_PATH="$W/no-such-guard.sh" python3 scripts/release-audit.py "$CL" 2>&1)"; RC=$?
[ "$RC" -ne 0 ] && echo "$OUT" | grep -q "guard not found" && ! echo "$OUT" | grep -q "Starting Release Readiness" && ok "a missing guard is reported before any scan" || bad "a missing guard is reported before any scan (rc=$RC)"
# --metadata points the listing audit at a pulled metadata folder instead of the app folder.
MD="$W/pulled"; mkdir -p "$MD/en-US"
printf 'Lumina Studio' > "$MD/en-US/name.txt"
printf 'A focused editor with layers and presets.' > "$MD/en-US/description.txt"
printf '{"privacy_policy_url":"https://lumina.app/privacy","support_url":"https://lumina.app/support"}' > "$MD/m.json"
OUT="$(APP_STORE_GUARD_PATH="$STUB_PASS" python3 "$SK/scripts/release-audit.py" "$NOMETA" --metadata "$MD" 2>&1)"; RC=$?
[ "$RC" -eq 0 ] && echo "$OUT" | grep -q "Overall Status: PASSED" && echo "$OUT" | grep -q "CLEAR TO SUBMIT" && ok "a clean pulled listing passed with --metadata reaches CLEAR" || bad "a clean pulled listing passed with --metadata reaches CLEAR (rc=$RC)"

OUT="$(APP_STORE_GUARD_PATH="$STUB_PASS" python3 "$SK/scripts/release-audit.py" "$NOMETA" 2>&1)"; RC=$?
[ "$RC" -eq 3 ] && echo "$OUT" | grep -q "Overall Status: INCOMPLETE" && echo "$OUT" | grep -q "Store listing not audited. Pull it with scripts/pull-metadata.sh, then pass --metadata <dir>." && ok "no listing and no --metadata is INCOMPLETE with the command to run" || bad "no listing and no --metadata is INCOMPLETE with the command to run (rc=$RC)"

OUT="$(APP_STORE_GUARD_PATH="$STUB_PASS" python3 "$SK/scripts/release-audit.py" "$NOMETA" --metadata "$W/no-such-dir" 2>&1)"; RC=$?
[ "$RC" -eq 1 ] && echo "$OUT" | grep -q "not a directory" && ! echo "$OUT" | grep -q "Starting Release Readiness" && ok "a missing --metadata folder is rejected before any scan" || bad "a missing --metadata folder is rejected before any scan (rc=$RC)"

rm -rf "$W"

echo "release-audit-test: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
