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

# 3b. hidden tool-state directories are not cited sources, but .github is part of the repo
mkdir -p "$WORK/hid/.gstack" "$WORK/hid/.github"
echo "https://example.org/from-a-browser-log" > "$WORK/hid/.gstack/browse-network.log"
echo "https://www.ftc.gov/legal-library" > "$WORK/hid/.github/CONTRIBUTING.md"
out="$(python3 "$VERIFY" --dir "$WORK/hid" --offline 2>&1)"
echo "$out" | grep -q "1 distinct URL" && echo "$out" | grep -q "ftc.gov" && ! echo "$out" | grep -q "browser-log" && ok "hidden tool-state directories are skipped, .github is scanned" || bad "hidden tool-state directories are skipped, .github is scanned"

# 3c. a --files path that does not exist is an error, and a relative one is tried under --dir
out="$(cd / && python3 "$VERIFY" --dir "$WORK" --files no-such-folder/ --offline 2>&1)"; rc=$?
[ "$rc" -eq 2 ] && echo "$out" | grep -q "does not exist" && ok "a missing --files path fails loudly" || bad "a missing --files path fails loudly (rc=$rc)"
out="$(cd / && python3 "$VERIFY" --dir "$WORK" --files a.md --offline 2>&1)"
echo "$out" | grep -q "2 distinct URL" && ok "a relative --files path resolves under --dir from any directory" || bad "a relative --files path resolves under --dir from any directory"

# 3d. a host that answers 404 even at its homepage refuses automation (ftc.gov does).
#     Its 404s are bot-blocked. A dead page on a host whose homepage works still fails.
SRV="$WORK/srv.py"
cat > "$SRV" <<'PY'
import http.server, sys
mode = sys.argv[1]
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        code = 200 if (mode == "healthy" and self.path == "/") else 404
        self.send_response(code); self.end_headers(); self.wfile.write(b"x" * 64)
    def log_message(self, *a): pass
s = http.server.HTTPServer(("127.0.0.1", 0), H)
print(s.server_port, flush=True)
s.serve_forever()
PY
start_srv() {
  python3 "$SRV" "$1" > "$WORK/port.$1" &
  echo $! > "$WORK/pid.$1"
  for _ in 1 2 3 4 5 6 7 8 9 10; do [ -s "$WORK/port.$1" ] && break; sleep 0.2; done
  cat "$WORK/port.$1"
}
BP="$(start_srv blocking)"; HP="$(start_srv healthy)"
mkdir -p "$WORK/hb" "$WORK/hd"
echo "http://127.0.0.1:$BP/business-guidance/real-page" > "$WORK/hb/a.md"
echo "http://127.0.0.1:$HP/gone-page" > "$WORK/hd/a.md"
out="$(python3 "$VERIFY" --dir "$WORK/hb" 2>&1)"; rc=$?
[ "$rc" -eq 0 ] && echo "$out" | grep -q "bot-blocked, not a defect. 1" && ok "a 404 from a host whose homepage is also 404 counts as bot-blocked" || bad "a 404 from a host whose homepage is also 404 counts as bot-blocked (rc=$rc)"
out="$(python3 "$VERIFY" --dir "$WORK/hd" 2>&1)"; rc=$?
[ "$rc" -ne 0 ] && echo "$out" | grep -q "\[404\] http://127.0.0.1:$HP/gone-page" && ok "a dead page on a healthy host still fails" || bad "a dead page on a healthy host still fails (rc=$rc)"
kill "$(cat "$WORK/pid.blocking")" "$(cat "$WORK/pid.healthy")" 2>/dev/null

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
