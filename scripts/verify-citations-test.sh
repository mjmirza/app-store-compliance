#!/usr/bin/env bash
# Gauntlet for verify-citations.py. Proves it catches the real fabricated
# citations found in the Jules PR flood, and stays quiet on genuine ones.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERIFY="$SCRIPT_DIR/verify-citations.py"
PASS=0
FAIL=0

ok() { echo "PASS  $1"; PASS=$((PASS + 1)); }
bad() { echo "FAIL  $1"; FAIL=$((FAIL + 1)); }

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

net_up() { curl -sS -o /dev/null --max-time 10 https://developer.apple.com >/dev/null 2>&1; }

# 1. offline parse finds URLs and never touches the network
cat > "$WORK/a.md" <<'EOF'
https://eur-lex.europa.eu/eli/reg/2016/679/oj
https://support.google.com/googleplay/android-developer/answer/10787469
EOF
out="$(python3 "$VERIFY" --dir "$WORK" --offline 2>&1)"
echo "$out" | grep -q "2 distinct URL" && ok "offline mode finds both URLs" || bad "offline mode URL count"
echo "$out" | grep -q "P1 https://eur-lex" && ok "trust hierarchy classifies EUR-Lex as P1" || bad "trust classification"

# 2. empty tree is clean, not a crash
mkdir -p "$WORK/empty"
python3 "$VERIFY" --dir "$WORK/empty" --offline >/dev/null 2>&1 && ok "empty tree exits 0" || bad "empty tree"

# 3. malformed and huge input do not crash the parser
printf 'http://\nhttps://x\n%s\n' "$(head -c 20000 /dev/zero | tr '\0' 'x')" > "$WORK/empty/junk.md"
python3 "$VERIFY" --dir "$WORK/empty" --offline >/dev/null 2>&1 && ok "malformed input survives" || bad "malformed input"

if ! net_up; then
  echo "SKIP  network tests (offline)"
else
  # 4. THE RED TEST. A known-fabricated Apple slug must be caught, even though
  #    it returns HTTP 200, because it serves the same body as a bogus control.
  mkdir -p "$WORK/fab"
  echo "Source: https://developer.apple.com/news/?id=required-reason-apis" > "$WORK/fab/bad.md"
  out="$(python3 "$VERIFY" --dir "$WORK/fab" 2>&1)"
  rc=$?
  echo "$out" | grep -q "FABRICATED" && ok "catches soft-404 Apple citation that returns HTTP 200" \
    || bad "MISSED soft-404 Apple citation"
  [ "$rc" -ne 0 ] && ok "exits non-zero on a fabricated citation" || bad "exit code on fabrication"

  # 5. A hard-404 Google slug must be reported unreachable
  mkdir -p "$WORK/dead"
  echo "Source: https://support.google.com/googleplay/android-developer/answer/datasafety" > "$WORK/dead/bad.md"
  out="$(python3 "$VERIFY" --dir "$WORK/dead" 2>&1)"
  echo "$out" | grep -qE "UNREACHABLE|404" && ok "catches hard-404 Google citation" || bad "missed hard-404"

  # 6. NEGATIVE CASE. Genuine citations must pass clean, or the gate is noise.
  mkdir -p "$WORK/good"
  cat > "$WORK/good/ok.md" <<'EOF'
https://support.google.com/googleplay/android-developer/answer/10787469
https://developer.apple.com/support/privacy-manifest-files
EOF
  out="$(python3 "$VERIFY" --dir "$WORK/good" 2>&1)"
  rc=$?
  echo "$out" | grep -q "PASS" && ok "genuine citations pass clean (no false positive)" || bad "false positive on real URLs"
  [ "$rc" -eq 0 ] && ok "exits 0 when all citations are real" || bad "exit code on clean input"

  # 7. allowlist suppresses an intentional unreachable fixture URL
  mkdir -p "$WORK/alw"
  echo "https://randomblogsite.com/gdpr-rumor" > "$WORK/alw/f.md"
  echo "https://randomblogsite.com/gdpr-rumor" > "$WORK/alw/.citation-allowlist"
  python3 "$VERIFY" --dir "$WORK/alw" >/dev/null 2>&1 && ok "allowlist suppresses test fixture URL" || bad "allowlist"
fi

echo
echo "verify-citations gauntlet. $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] || exit 1
