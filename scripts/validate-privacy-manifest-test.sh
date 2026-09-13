#!/usr/bin/env bash
# Test suite for validate-privacy-manifest.py
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
V="python3 $HERE/validate-privacy-manifest.py"
PASS=0; FAIL=0
ok(){ PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad(){ FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT

write_manifest() {  # file tracking domains_xml types_xml
  cat > "$1" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>NSPrivacyTracking</key><$2/>
<key>NSPrivacyTrackingDomains</key>$3
<key>NSPrivacyCollectedDataTypes</key>$4
</dict></plist>
PLIST
}

TYPE_OK='<array><dict>
<key>NSPrivacyCollectedDataType</key><string>NSPrivacyCollectedDataTypeDeviceID</string>
<key>NSPrivacyCollectedDataTypeLinked</key><false/>
<key>NSPrivacyCollectedDataTypeTracking</key><true/>
<key>NSPrivacyCollectedDataTypePurposes</key><array><string>NSPrivacyCollectedDataTypePurposeDeveloperAdvertising</string></array>
</dict></array>'
DOMAINS='<array><string>att.attr.appsflyersdk.com</string></array>'

# 1 tracking true with no domains is the ITMS-91064 rejection
write_manifest "$T/a.xcprivacy" true '<array/>' "$TYPE_OK"
OUT="$($V "$T/a.xcprivacy" 2>&1)"
echo "$OUT" | grep -q 'APPLE-ITMS-91064-TRACKING-NO-DOMAINS' && ok "flags tracking true with empty domains" || bad "tracking/no-domains"

# 2 domains without tracking true is the converse
write_manifest "$T/b.xcprivacy" false "$DOMAINS" '<array/>'
OUT="$($V "$T/b.xcprivacy" 2>&1)"
echo "$OUT" | grep -q 'APPLE-ITMS-91064-DOMAINS-NO-TRACKING' && ok "flags domains with tracking false" || bad "domains/no-tracking"

# 3 a consistent manifest passes
write_manifest "$T/c.xcprivacy" true "$DOMAINS" "$TYPE_OK"
$V "$T/c.xcprivacy" >/dev/null 2>&1
[ $? -eq 0 ] && ok "consistent manifest passes" || bad "consistent manifest"

# 4 tracking false with no domains is valid, not a finding
write_manifest "$T/d.xcprivacy" false '<array/>' '<array/>'
$V "$T/d.xcprivacy" >/dev/null 2>&1
[ $? -eq 0 ] && ok "no tracking, no domains passes" || bad "no-tracking baseline"

# 5 a type used for tracking while the manifest says otherwise
write_manifest "$T/e.xcprivacy" false '<array/>' "$TYPE_OK"
OUT="$($V "$T/e.xcprivacy" 2>&1)"
echo "$OUT" | grep -q 'APPLE-MANIFEST-TRACKING-CONTRADICTION' && ok "flags per-type tracking contradiction" || bad "type contradiction"

# 6 unknown purpose constant
write_manifest "$T/f.xcprivacy" true "$DOMAINS" "${TYPE_OK/NSPrivacyCollectedDataTypePurposeDeveloperAdvertising/NSPrivacyCollectedDataTypePurposeMarketing}"
OUT="$($V "$T/f.xcprivacy" 2>&1)"
echo "$OUT" | grep -q 'APPLE-MANIFEST-BAD-PURPOSE' && ok "flags unknown purpose" || bad "bad purpose"

# 7 unreadable manifest exits 2 rather than passing silently
printf 'not a plist' > "$T/g.xcprivacy"
$V "$T/g.xcprivacy" >/dev/null 2>&1
[ $? -eq 2 ] && ok "unreadable manifest exits 2" || bad "unreadable exit code"

# 8 a plist whose root is an array is not a manifest, and must be a finding rather than a crash into a silent pass
printf '<?xml version="1.0" encoding="UTF-8"?><plist version="1.0"><array><string>x</string></array></plist>' > "$T/h.xcprivacy"
OUT="$($V "$T/h.xcprivacy" 2>&1)"; RC=$?
echo "$OUT" | grep -q 'APPLE-MANIFEST-UNREADABLE' && [ $RC -eq 2 ] && ok "root array is unreadable, exit 2" || bad "root array (rc=$RC)"

# 9 an empty NSPrivacyAccessedAPITypes array is invalid per TN3181
printf '<?xml version="1.0" encoding="UTF-8"?><plist version="1.0"><dict><key>NSPrivacyAccessedAPITypes</key><array/></dict></plist>' > "$T/i.xcprivacy"
OUT="$($V "$T/i.xcprivacy" 2>&1)"
echo "$OUT" | grep -q 'critical.APPLE-MANIFEST-API-TYPES-EMPTY' && ok "empty accessed API array is critical" || bad "empty accessed API array"

# 10 an accessed API with an empty reasons array is invalid per TN3181, and blocks
printf '<?xml version="1.0" encoding="UTF-8"?><plist version="1.0"><dict><key>NSPrivacyAccessedAPITypes</key><array><dict><key>NSPrivacyAccessedAPIType</key><string>NSPrivacyAccessedAPICategoryUserDefaults</string><key>NSPrivacyAccessedAPITypeReasons</key><array/></dict></array></dict></plist>' > "$T/j.xcprivacy"
OUT="$($V "$T/j.xcprivacy" 2>&1)"
echo "$OUT" | grep -q 'critical.APPLE-MANIFEST-API-NO-REASON' && ok "empty reason array is critical" || bad "empty reason array"

# 11 a collected type with the wrong value type is reported, never a crash
printf '<?xml version="1.0" encoding="UTF-8"?><plist version="1.0"><dict><key>NSPrivacyCollectedDataTypes</key><string>oops</string></dict></plist>' > "$T/k.xcprivacy"
OUT="$($V "$T/k.xcprivacy" 2>&1)"; RC=$?
echo "$OUT" | grep -q 'APPLE-MANIFEST-BAD-VALUE' && [ $RC -eq 1 ] && ok "wrong value type is a finding" || bad "wrong value type (rc=$RC)"

# 12 a NSPrivacyTracking that is not a Boolean is invalid per TN3181
printf '<?xml version="1.0" encoding="UTF-8"?><plist version="1.0"><dict><key>NSPrivacyTracking</key><string>yes</string></dict></plist>' > "$T/l.xcprivacy"
OUT="$($V "$T/l.xcprivacy" 2>&1)"
echo "$OUT" | grep -q 'critical.APPLE-MANIFEST-BAD-VALUE' && ok "non-boolean tracking is critical" || bad "non-boolean tracking"

echo ""
echo "validate-privacy-manifest-test: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
