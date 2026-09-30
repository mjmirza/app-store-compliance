#!/usr/bin/env bash
# Tests scripts/install.sh against a throwaway config directory. Never touches the real ~/.claude.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

PASS=0
FAIL=0
ok()  { PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad() { FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

INSTALL="$PWD/scripts/install.sh"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
fresh() { C="$WORK/c$RANDOM$RANDOM"; mkdir -p "$C"; }
run()   { CLAUDE_CONFIG_DIR="$C" bash "$INSTALL" "$@" 2>&1; }
hooks() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(sum("app-store-compliance-guard.sh" in h.get("command","") for e in d.get("hooks",{}).get("PreToolUse",[]) for h in e.get("hooks",[])))' "$C/settings.json"; }

# 1 a fresh install lands every part and proves itself
fresh
OUT="$(run)"; RC=$?
[ "$RC" -eq 0 ] && ok "fresh install exits 0" || bad "fresh install exits 0 (rc=$RC)"
[ -x "$C/hooks/app-store-compliance-guard.sh" ] && ok "guard is installed and executable" || bad "guard is installed and executable"
for p in SKILL.md data/rejection-patterns.json data/regulatory-deadlines.json docs/APPLE.md references scripts/deadline-checker.py scripts/validate-privacy-manifest.py templates .citation-allowlist; do
  [ -e "$C/skills/app-store-compliance/$p" ] || { bad "skill payload has $p"; continue; }
done
[ -e "$C/skills/app-store-compliance/.citation-allowlist" ] && ok "skill payload is complete, allowlist included" || bad "skill payload is complete, allowlist included"
[ -f "$C/commands/app-store-audit.md" ] && ok "slash command is installed" || bad "slash command is installed"
[ "$(hooks)" = "1" ] && ok "hook is registered once in settings.json" || bad "hook is registered once in settings.json (got $(hooks))"
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); e=[h for x in d["hooks"]["PreToolUse"] if x.get("matcher")=="Bash" for h in x["hooks"] if "app-store-compliance-guard.sh" in h["command"]]; sys.exit(0 if e and e[0].get("timeout",0)>=120 and e[0].get("type")=="command" else 1)' "$C/settings.json" && ok "hook entry is a Bash PreToolUse command with a 120 second timeout" || bad "hook entry is a Bash PreToolUse command with a 120 second timeout"
echo "$OUT" | grep -q "^Install verified\." && ok "install ends with a verified line" || bad "install ends with a verified line"
echo "$OUT" | grep -q "bash .*app-store-compliance-guard.sh /path/to/your/app" && ok "install prints the one command to run next" || bad "install prints the one command to run next"

# 2 running it again changes nothing and adds no second entry
BEFORE="$(cat "$C/settings.json")"
run >/dev/null; RC=$?
[ "$RC" -eq 0 ] && [ "$(hooks)" = "1" ] && [ "$BEFORE" = "$(cat "$C/settings.json")" ] && ok "a second run is idempotent" || bad "a second run is idempotent (rc=$RC entries=$(hooks))"

# 3 existing settings survive, and a backup is written
fresh
printf '{"model":"opus","hooks":{"PreToolUse":[{"matcher":"Bash","hooks":[{"type":"command","command":"bash ~/other.sh"}]}],"Stop":[{"hooks":[{"type":"command","command":"x"}]}]},"permissions":{"allow":["Read"]}}' > "$C/settings.json"
run >/dev/null
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); cmds=[h["command"] for e in d["hooks"]["PreToolUse"] for h in e["hooks"]]; sys.exit(0 if d["model"]=="opus" and d["permissions"]=={"allow":["Read"]} and "bash ~/other.sh" in cmds and len(d["hooks"]["Stop"])==1 else 1)' "$C/settings.json" && ok "existing keys and hooks are preserved" || bad "existing keys and hooks are preserved"
ls "$C"/settings.json.bak-* >/dev/null 2>&1 && ok "a backup of settings.json is kept" || bad "a backup of settings.json is kept"

# 4 a settings.json that is not valid JSON is never rewritten
fresh
printf '{ "model": "opus", broken' > "$C/settings.json"
OUT="$(run)"; RC=$?
[ "$(cat "$C/settings.json")" = '{ "model": "opus", broken' ] && ok "an unreadable settings.json is left untouched" || bad "an unreadable settings.json is left untouched"
echo "$OUT" | grep -q '"PreToolUse"' && [ "$RC" -eq 1 ] && ok "it prints the block to add by hand and exits 1" || bad "it prints the block to add by hand and exits 1 (rc=$RC)"

# 5 dry run writes nothing
fresh
OUT="$(run --dry-run)"; RC=$?
[ "$RC" -eq 0 ] && [ -z "$(ls -A "$C")" ] && echo "$OUT" | grep -q "Dry run" && ok "dry run writes nothing" || bad "dry run writes nothing (rc=$RC)"

# 6 doctor fails before an install and passes after
fresh
run doctor >/dev/null; RC=$?
[ "$RC" -eq 1 ] && ok "doctor fails when nothing is installed" || bad "doctor fails when nothing is installed (rc=$RC)"
run >/dev/null
OUT="$(run doctor)"; RC=$?
[ "$RC" -eq 0 ] && echo "$OUT" | grep -q "^Install verified\." && ok "doctor passes after an install" || bad "doctor passes after an install (rc=$RC)"

# 7 doctor notices a guard that was edited or is stale
printf '\n# local edit\n' >> "$C/hooks/app-store-compliance-guard.sh"
OUT="$(run doctor)"; RC=$?
echo "$OUT" | grep -q "differs from this checkout" && ok "doctor reports a guard that differs from the checkout" || bad "doctor reports a guard that differs from the checkout"

# 8 doctor catches a guard that no longer blocks
printf '#!/usr/bin/env bash\nexit 0\n' > "$C/hooks/app-store-compliance-guard.sh"
run doctor >/dev/null; RC=$?
[ "$RC" -eq 1 ] && ok "doctor fails when the guard does not block a bad app" || bad "doctor fails when the guard does not block a bad app (rc=$RC)"

# 9 with no python3 and no jq the files still install and the settings block is printed
fresh
SHIM="$(mktemp -d)"
for b in bash cp rm mkdir chmod cat grep sed awk find xargs tr head tail mktemp printf wc sort uniq cut dirname basename date cmp mv ls env plutil xmllint; do p="$(command -v "$b" 2>/dev/null)"; [ -n "$p" ] && ln -s "$p" "$SHIM/$b"; done
OUT="$(PATH="$SHIM" CLAUDE_CONFIG_DIR="$C" bash "$INSTALL" 2>&1)"; RC=$?
[ -x "$C/hooks/app-store-compliance-guard.sh" ] && [ ! -f "$C/settings.json" ] && echo "$OUT" | grep -q '"PreToolUse"' && [ "$RC" -eq 1 ] && ok "without python3 or jq the block is printed for a manual paste" || bad "without python3 or jq the block is printed for a manual paste (rc=$RC)"
rm -rf "$SHIM"

# 10 uninstall removes only what the installer added
fresh
printf '{"hooks":{"PreToolUse":[{"matcher":"Bash","hooks":[{"type":"command","command":"bash ~/other.sh"}]}]}}' > "$C/settings.json"
run >/dev/null
run uninstall >/dev/null; RC=$?
[ "$RC" -eq 0 ] && [ ! -e "$C/hooks/app-store-compliance-guard.sh" ] && [ ! -e "$C/skills/app-store-compliance" ] && [ "$(hooks)" = "0" ] && grep -q "other.sh" "$C/settings.json" && ok "uninstall removes the guard, skill and entry, and keeps other hooks" || bad "uninstall removes the guard, skill and entry, and keeps other hooks (rc=$RC)"

# 11 an unknown subcommand is refused
fresh
run frobnicate >/dev/null; RC=$?
[ "$RC" -eq 2 ] && [ -z "$(ls -A "$C")" ] && ok "an unknown subcommand exits 2 and writes nothing" || bad "an unknown subcommand exits 2 and writes nothing (rc=$RC)"

echo ""
echo "install-test: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
