#!/usr/bin/env bash
# Tests install.sh --tool for Codex, Gemini CLI, OpenCode, Cursor and Copilot CLI in a throwaway HOME.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

PASS=0
FAIL=0
ok()  { PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad() { FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

INSTALL="$PWD/scripts/install.sh"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
fresh() { H="$WORK/h$RANDOM$RANDOM"; mkdir -p "$H"; }
run()   { env -u CODEX_HOME -u XDG_CONFIG_HOME -u CLAUDE_CONFIG_DIR -u CLAUDE_PROJECT_DIR HOME="$H" bash "$INSTALL" "$@" 2>&1; }
cfg() {
  case "$1" in
    codex) echo "$H/.codex/hooks.json" ;;
    gemini) echo "$H/.gemini/settings.json" ;;
    opencode) echo "$H/.config/opencode/plugins/app-store-compliance.js" ;;
    cursor) echo "$H/.cursor/hooks.json" ;;
    copilot) echo "$H/.copilot/hooks/app-store-compliance.json" ;;
  esac
}
count() {  # how many hook entries point at the guard
  python3 - "$1" "$(cfg "$1")" <<'PY'
import json, sys
tool, path = sys.argv[1], sys.argv[2]
key = {"codex": "PreToolUse", "gemini": "BeforeTool", "cursor": "beforeShellExecution", "copilot": "preToolUse"}[tool]
try:
    d = json.load(open(path))
except Exception:
    print(0); sys.exit()
groups = d.get("hooks", {}).get(key, [])
n = 0
for g in groups:
    items = g.get("hooks", []) if tool in ("codex", "gemini") else [g]
    n += sum("app-store-compliance-guard.sh" in str(h.get("command", h.get("bash", ""))) for h in items)
print(n)
PY
}

for t in codex gemini opencode cursor copilot; do
  # 1 a fresh install verifies itself end to end
  fresh
  OUT="$(run --tool "$t")"; RC=$?
  [ "$RC" -eq 0 ] && echo "$OUT" | grep -q "^Install verified\." && ok "$t fresh install verifies" || { bad "$t fresh install verifies (rc=$RC)"; echo "$OUT" | tail -15; }
  case "$t" in opencode) GD="$H/.config/opencode/hooks" ;; *) GD="$H/.$t/hooks" ;; esac
  [ -x "$GD/app-store-compliance-guard.sh" ] && ok "$t guard is installed and executable" || bad "$t guard is installed and executable"
  [ -f "$H/.agents/skills/app-store-compliance/SKILL.md" ] && [ -f "$H/.agents/skills/app-store-compliance/VERSION" ] && ok "$t shared skill and version installed" || bad "$t shared skill and version installed"
  if [ "$t" != "opencode" ]; then
    [ "$(count "$t")" = "1" ] && ok "$t hook registered once" || bad "$t hook registered once (got $(count "$t"))"
    BEFORE="$(cat "$(cfg "$t")")"; run --tool "$t" >/dev/null
    [ "$BEFORE" = "$(cat "$(cfg "$t")")" ] && [ "$(count "$t")" = "1" ] && ok "$t a second run is idempotent" || bad "$t a second run is idempotent"
  else
    grep -q 'tool.execute.before' "$(cfg "$t")" && ok "$t plugin written" || bad "$t plugin written"
    # OpenCode before 1.0 loads plugin/, current OpenCode loads plugins/. Both must carry it.
    cmp -s "$(cfg "$t")" "$H/.config/opencode/plugin/app-store-compliance.js" && ok "$t plugin also in the plugin/ folder older OpenCode reads" || bad "$t plugin also in the plugin/ folder older OpenCode reads"
    echo "$OUT" | grep -q "the plugin stops a submit command" && ok "$t plugin blocks a submit command in node" || bad "$t plugin blocks a submit command in node"
  fi
  # 2 doctor passes, and fails after uninstall
  OUT="$(run --tool "$t" doctor)"; RC=$?
  [ "$RC" -eq 0 ] && ok "$t doctor passes" || bad "$t doctor passes (rc=$RC)"
  run --tool "$t" uninstall >/dev/null
  [ ! -e "$H/.agents/skills/app-store-compliance" ] && ok "$t uninstall removes the shared skill when no tool is left" || bad "$t uninstall removes the shared skill when no tool is left"
  if [ "$t" = "opencode" ]; then
    [ ! -e "$(cfg "$t")" ] && [ ! -e "$H/.config/opencode/plugin/app-store-compliance.js" ] && ok "$t uninstall removes the plugin from both folders" || bad "$t uninstall removes the plugin from both folders"
  else
    [ "$(count "$t")" = "0" ] && ok "$t uninstall removes the hook entry" || bad "$t uninstall removes the hook entry"
  fi
  run --tool "$t" doctor >/dev/null; RC=$?
  [ "$RC" -eq 1 ] && ok "$t doctor fails when nothing is installed" || bad "$t doctor fails when nothing is installed (rc=$RC)"
done

# 3 existing settings survive and get a backup (Gemini keeps ide and security, Codex keeps its other hooks)
fresh; mkdir -p "$H/.gemini" "$H/.codex"
printf '{"ide":{"enabled":true},"security":{"auth":{"selectedType":"oauth-personal"}}}' > "$H/.gemini/settings.json"
printf '{"hooks":{"PreToolUse":[{"matcher":"Bash","hooks":[{"type":"command","command":"bash ~/other.sh"}]}]}}' > "$H/.codex/hooks.json"
run --tool gemini >/dev/null; run --tool codex >/dev/null
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); h=d["hooks"]["BeforeTool"][0]; sys.exit(0 if d["ide"]=={"enabled":True} and d["security"]["auth"]["selectedType"]=="oauth-personal" and d["tools"]["enableHooks"] is True and h["matcher"]=="run_shell_command" and h["hooks"][0]["timeout"]==120000 else 1)' "$H/.gemini/settings.json" \
  && ok "gemini keeps existing keys, enables hooks, uses a millisecond timeout" || bad "gemini keeps existing keys, enables hooks, uses a millisecond timeout"
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); c=[h["command"] for g in d["hooks"]["PreToolUse"] for h in g["hooks"]]; sys.exit(0 if "bash ~/other.sh" in c and len(c)==2 else 1)' "$H/.codex/hooks.json" \
  && ok "codex keeps its existing hooks" || bad "codex keeps its existing hooks"
ls "$H"/.gemini/settings.json.bak-* >/dev/null 2>&1 && ls "$H"/.codex/hooks.json.bak-* >/dev/null 2>&1 && ok "a backup is kept for each edited config" || bad "a backup is kept for each edited config"
# 4 the shared skill stays while another tool still uses it
run --tool gemini uninstall >/dev/null
[ -f "$H/.agents/skills/app-store-compliance/SKILL.md" ] && ok "the shared skill stays while codex still uses it" || bad "the shared skill stays while codex still uses it"
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if d["ide"]=={"enabled":True} and "hooks" not in d else 1)' "$H/.gemini/settings.json" \
  && ok "gemini uninstall keeps every other key" || bad "gemini uninstall keeps every other key"
OUT="$(run --tool codex uninstall)"
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); c=[h["command"] for g in d["hooks"]["PreToolUse"] for h in g["hooks"]]; sys.exit(0 if c==["bash ~/other.sh"] else 1)' "$H/.codex/hooks.json" \
  && ok "codex uninstall keeps the other hook" || bad "codex uninstall keeps the other hook"

# 5 a config that is not valid JSON, or repeats a key, is never rewritten
for body in '{"hooks": [broken' '{"permissions":{"deny":["x"]},"permissions":{"allow":["x"]}}'; do
  fresh; mkdir -p "$H/.codex"; printf '%s' "$body" > "$H/.codex/hooks.json"
  OUT="$(run --tool codex)"; RC=$?
  [ "$RC" -ne 0 ] && [ "$(cat "$H/.codex/hooks.json")" = "$body" ] && echo "$OUT" | grep -q "Merge this into" && ok "an unsafe codex config is left untouched and a manual block is printed" || bad "an unsafe codex config is left untouched (rc=$RC)"
done

# 6 the installed guard finds the deadline list and the manifest validator in the shared skill
fresh; run --tool codex >/dev/null
APP="$WORK/app$RANDOM"; mkdir -p "$APP/App"; printf '<plist><dict></dict></plist>' > "$APP/App/Info.plist"; printf 'import UIKit\n' > "$APP/App/A.swift"
OUT="$(env HOME="$H" bash "$H/.codex/hooks/app-store-compliance-guard.sh" "$APP" 2>&1)"
echo "$OUT" | grep -q "Regulatory Compliance Deadline Status" && ok "the codex guard finds the deadline list in ~/.agents/skills" || bad "the codex guard finds the deadline list in ~/.agents/skills"

# 7 the audit command points at the installed paths, and the Gemini command is valid TOML
fresh; run --tool gemini >/dev/null; run --tool opencode >/dev/null
python3 -c 'import sys,tomllib; d=tomllib.load(open(sys.argv[1],"rb")); sys.exit(0 if d["description"] and "{{args}}" in d["prompt"] else 1)' "$H/.gemini/commands/app-store-audit.toml" && ok "the gemini command is valid TOML with {{args}}" || bad "the gemini command is valid TOML with {{args}}"
! grep -q "~/.claude" "$H/.gemini/commands/app-store-audit.toml" "$H/.config/opencode/commands/app-store-audit.md" && ok "the commands name no Claude Code path" || bad "the commands name no Claude Code path"

# 8 --tool all installs into every tool it finds, and only those
fresh; mkdir -p "$H/.codex" "$H/.cursor"
OUT="$(run --tool all)"; RC=$?
[ "$RC" -eq 0 ] && echo "$OUT" | grep -q "^Found. codex cursor$" && [ "$(count codex)" = "1" ] && [ "$(count cursor)" = "1" ] && [ ! -e "$H/.gemini" ] && [ ! -e "$H/.claude" ] \
  && ok "--tool all installs into the found tools only" || { bad "--tool all installs into the found tools only (rc=$RC)"; echo "$OUT" | head -5; }
fresh; OUT="$(run --tool all)"; RC=$?
[ "$RC" -eq 1 ] && echo "$OUT" | grep -q "No supported AI coding tool" && ok "--tool all with no tool says so" || bad "--tool all with no tool says so (rc=$RC)"

# 9 a home folder with an apostrophe still verifies
H="$WORK/O'Reilly home"; mkdir -p "$H"
OUT="$(run --tool cursor)"; RC=$?
[ "$RC" -eq 0 ] && [ "$(count cursor)" = "1" ] && ok "a home with an apostrophe installs and verifies" || bad "a home with an apostrophe installs and verifies (rc=$RC)"

# 10 bad input
fresh; OUT="$(run --tool vim)"; RC=$?
[ "$RC" -eq 2 ] && echo "$OUT" | grep -q "Unknown tool" && ok "an unknown tool exits 2" || bad "an unknown tool exits 2 (rc=$RC)"
OUT="$(run --tool)"; RC=$?
[ "$RC" -eq 2 ] && ok "--tool with no name exits 2" || bad "--tool with no name exits 2 (rc=$RC)"
OUT="$(run --tool gemini --dry-run)"; RC=$?
[ "$RC" -eq 0 ] && [ ! -e "$H/.gemini" ] && [ ! -e "$H/.agents" ] && ok "--dry-run writes nothing" || bad "--dry-run writes nothing (rc=$RC)"

echo ""
echo "install-harness-test: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
