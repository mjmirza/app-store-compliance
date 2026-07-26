#!/usr/bin/env bash
# Test suite for accessibility-audit.py
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
AUDIT="python3 $HERE/accessibility-audit.py"
PASS=0; FAIL=0
ok(){ PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad(){ FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

# 1. VoiceOver empty label detected (critical severity -> exit 2)
T=$(mktemp -d)
printf 'struct CustomButton: View {\n  var body: some View {\n    Button("Tap") {}\n      .accessibilityLabel("")\n  }\n}' > "$T/Button.swift"
OUT="$($AUDIT "$T" 2>&1)"
RC=$?
if [ "$RC" -eq 2 ] && echo "$OUT" | grep -q 'ACC-APPLE-VOICEOVER-EMPTY-LABEL'; then
  ok "flags empty accessibility label and returns exit code 2"
else
  bad "empty accessibility label failed to block (rc=$RC)"
fi
rm -rf "$T"

# 2. Hardcoded system font size detected (high severity -> exit 0 since not critical)
T=$(mktemp -d)
printf 'let font = UIFont.systemFont(ofSize: 14)' > "$T/Label.swift"
OUT="$($AUDIT "$T" 2>&1)"
RC=$?
if [ "$RC" -eq 0 ] && echo "$OUT" | grep -q 'ACC-APPLE-DYNAMIC-TYPE-SYSTEM-FONT'; then
  ok "flags hardcoded system font size and passes with exit code 0"
else
  bad "hardcoded system font size (rc=$RC)"
fi
rm -rf "$T"

# 3. Android empty contentDescription detected (critical severity -> exit 2)
T=$(mktemp -d)
printf '<ImageView\n  android:layout_width="wrap_content"\n  android:layout_height="wrap_content"\n  android:contentDescription="" />' > "$T/layout.xml"
OUT="$($AUDIT "$T" 2>&1)"
RC=$?
if [ "$RC" -eq 2 ] && echo "$OUT" | grep -q 'ACC-AND-TALKBACK-EMPTY-DESC'; then
  ok "flags empty android contentDescription and returns exit code 2"
else
  bad "empty android contentDescription failed to block (rc=$RC)"
fi
rm -rf "$T"

# 4. Android text size in dp detected (critical severity -> exit 2)
T=$(mktemp -d)
printf '<TextView\n  android:textSize="14dp" />' > "$T/layout.xml"
OUT="$($AUDIT "$T" 2>&1)"
RC=$?
if [ "$RC" -eq 2 ] && echo "$OUT" | grep -q 'ACC-AND-FONTSCALING-DP'; then
  ok "flags android textSize in dp and returns exit code 2"
else
  bad "android textSize in dp failed to block (rc=$RC)"
fi
rm -rf "$T"

# 5. Multiline layout formatting correctly parsed (critical severity -> exit 2)
T=$(mktemp -d)
printf '<ImageView\n    android:layout_width="match_parent"\n    android:layout_height="wrap_content"\n    android:contentDescription=""\n    android:src="@drawable/logo" />' > "$T/layout.xml"
OUT="$($AUDIT "$T" 2>&1)"
RC=$?
if [ "$RC" -eq 2 ] && echo "$OUT" | grep -q 'ACC-AND-TALKBACK-EMPTY-DESC'; then
  ok "handles and flags multiline XML attributes correctly"
else
  bad "multiline XML attribute handling failed (rc=$RC)"
fi
rm -rf "$T"

# 6. Clean directory passes (exit 0)
T=$(mktemp -d)
printf 'struct CleanButton: View {\n  var body: some View {\n    Button("Tap") {}\n      .accessibilityLabel("Submit form")\n  }\n}' > "$T/Button.swift"
OUT="$($AUDIT "$T" 2>&1)"
RC=$?
if [ "$RC" -eq 0 ] && echo "$OUT" | grep -q 'No regressions detected'; then
  ok "clean files pass with exit code 0"
else
  bad "clean files pass failed (rc=$RC)"
fi
rm -rf "$T"

echo ""
echo "accessibility-audit-test: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
