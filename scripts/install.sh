#!/usr/bin/env bash
# One command setup for Claude Code. Installs the guard, the skill and the slash command, registers
# the hook, then proves the guard blocks a bad app. Usage: install.sh [install|doctor|uninstall] [--dry-run]
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONF="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
GUARD_NAME="app-store-compliance-guard.sh"
GUARD_SRC="$REPO/agent-os/hooks/$GUARD_NAME"
GUARD="$CONF/hooks/$GUARD_NAME"
SKILL="$CONF/skills/app-store-compliance"
CMD_FILE="$CONF/commands/app-store-audit.md"
SETTINGS="$CONF/settings.json"
PAYLOAD_DIRS="docs data references templates scripts"

# shellcheck disable=SC2088
if [ "$CONF" = "$HOME/.claude" ]; then SHOWN='~/.claude'; else SHOWN="$CONF"; fi
HOOK_CMD="bash $SHOWN/hooks/$GUARD_NAME"

MODE="install"; DRY=0
for arg in "$@"; do
  case "$arg" in
    install|doctor|uninstall) MODE="$arg" ;;
    --dry-run) DRY=1 ;;
    -h|--help) MODE="help" ;;
    *) echo "Unknown argument. $arg" >&2; echo "Usage. install.sh [install|doctor|uninstall] [--dry-run]" >&2; exit 2 ;;
  esac
done

have() { command -v "$1" >/dev/null 2>&1 && "$@" >/dev/null 2>&1; }
say()  { printf '%s\n' "$*"; }
good() { printf '  ok    %s\n' "$*"; }
warn() { printf '  note  %s\n' "$*"; }
fail() { printf '  FAIL  %s\n' "$*"; PROBLEMS=$((PROBLEMS+1)); }
PROBLEMS=0

manual_block() {
  say ""
  say "Add this to $SHOWN/settings.json yourself, inside the top level object."
  say "If a \"hooks\" or \"PreToolUse\" key is already there, add only the inner entry to its list."
  cat <<BLOCK

  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "$HOOK_CMD", "timeout": 120 }
        ]
      }
    ]
  }

BLOCK
  say "Then run. bash $REPO/scripts/install.sh doctor"
}

# Edits settings.json. $1 is add or remove. Exit 0 changed, 3 nothing to change, 4 not safe to edit, 5 no JSON tool.
settings_edit() {
  local action="$1"
  if have python3 -c pass; then
    python3 - "$SETTINGS" "$HOOK_CMD" "$GUARD_NAME" "$action" <<'PY'
import json, os, shutil, sys, tempfile, time

path, cmd, name, action = sys.argv[1:5]
real = os.path.realpath(path)
exists = os.path.exists(real)
data = {}
if exists:
    try:
        with open(real, encoding="utf-8") as f:
            text = f.read()
        data = json.loads(text) if text.strip() else {}
    except Exception:
        sys.exit(4)
if not isinstance(data, dict):
    sys.exit(4)
hooks = data.get("hooks", {})
if not isinstance(hooks, dict):
    sys.exit(4)
pre = hooks.get("PreToolUse", [])
if not isinstance(pre, list):
    sys.exit(4)
for e in pre:
    if not isinstance(e, dict) or not isinstance(e.get("hooks", []), list):
        sys.exit(4)


def ours(h):
    return isinstance(h, dict) and name in str(h.get("command", ""))


changed = False
found = [h for e in pre for h in e.get("hooks", []) if ours(h)]
if action == "add":
    if found:
        for h in found:
            t = h.get("timeout")
            if not isinstance(t, (int, float)) or t < 120:
                h["timeout"] = 120
                changed = True
    else:
        pre.append(
            {"matcher": "Bash", "hooks": [{"type": "command", "command": cmd, "timeout": 120}]}
        )
        hooks["PreToolUse"] = pre
        data["hooks"] = hooks
        changed = True
elif found:
    kept = []
    for e in pre:
        had = any(ours(h) for h in e.get("hooks", []))
        e["hooks"] = [h for h in e.get("hooks", []) if not ours(h)]
        if e["hooks"] or not had:
            kept.append(e)
    if kept:
        hooks["PreToolUse"] = kept
    else:
        hooks.pop("PreToolUse", None)
    if not hooks:
        data.pop("hooks", None)
    changed = True
if not changed:
    sys.exit(3)
folder = os.path.dirname(real) or "."
os.makedirs(folder, exist_ok=True)
if exists:
    shutil.copy2(real, path + ".bak-" + time.strftime("%Y%m%d-%H%M%S"))
fd, tmp = tempfile.mkstemp(dir=folder, prefix=".settings-")
with os.fdopen(fd, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")
if exists:
    shutil.copymode(real, tmp)
os.replace(tmp, real)
PY
    return $?
  fi
  if have jq -n true; then
    local cur tmp
    if [ -s "$SETTINGS" ]; then cur="$SETTINGS"; else cur=""; fi
    if [ -n "$cur" ]; then
      jq -e 'type == "object" and ((.hooks // {}) | type == "object") and ((.hooks.PreToolUse // []) | type == "array")' "$cur" >/dev/null 2>&1 || return 4
    fi
    local present=1
    [ -n "$cur" ] && jq -e --arg n "$GUARD_NAME" '[.hooks.PreToolUse[]?.hooks[]?.command? // "" | tostring | contains($n)] | any' "$cur" >/dev/null 2>&1 && present=0
    if [ "$action" = "add" ]; then
      [ "$present" -eq 0 ] && return 3
      mkdir -p "$CONF"; tmp="$(mktemp "$CONF/.settings-XXXXXX")" || return 4
      if [ -n "$cur" ]; then cp -p "$cur" "$SETTINGS.bak-$(date +%Y%m%d-%H%M%S)"; else cur="/dev/null"; fi
      if [ "$cur" = "/dev/null" ]; then printf '{}' > "$tmp.in"; cur="$tmp.in"; fi
      jq --arg c "$HOOK_CMD" '.hooks.PreToolUse = ((.hooks.PreToolUse // []) + [{matcher: "Bash", hooks: [{type: "command", command: $c, timeout: 120}]}])' "$cur" > "$tmp" || { rm -f "$tmp" "$tmp.in"; return 4; }
      rm -f "$tmp.in"; mv "$tmp" "$SETTINGS"; return 0
    fi
    [ "$present" -ne 0 ] && return 3
    tmp="$(mktemp "$CONF/.settings-XXXXXX")" || return 4
    cp -p "$cur" "$SETTINGS.bak-$(date +%Y%m%d-%H%M%S)"
    jq --arg n "$GUARD_NAME" '.hooks.PreToolUse |= (map(.hooks |= map(select((.command? // "" | tostring | contains($n)) | not))) | map(select((.hooks | length) > 0)))' "$cur" > "$tmp" || { rm -f "$tmp"; return 4; }
    mv "$tmp" "$SETTINGS"; return 0
  fi
  return 5
}

hook_registered() {
  [ -f "$SETTINGS" ] || return 1
  if have python3 -c pass; then
    python3 -c 'import json,sys
try: d=json.load(open(sys.argv[1]))
except Exception: sys.exit(1)
ok=any(sys.argv[2] in str(h.get("command","")) for e in d.get("hooks",{}).get("PreToolUse",[]) if isinstance(e,dict) for h in e.get("hooks",[]) if isinstance(h,dict))
sys.exit(0 if ok else 1)' "$SETTINGS" "$GUARD_NAME" 2>/dev/null
    return $?
  fi
  grep -q "$GUARD_NAME" "$SETTINGS" 2>/dev/null
}

# Proves the install. Every line is a real check, the guard is run against a built-in app that must be blocked.
verify() {
  say ""; say "Checking the install."
  if [ -f "$GUARD" ]; then good "guard present at $SHOWN/hooks/$GUARD_NAME"; else fail "guard missing at $SHOWN/hooks/$GUARD_NAME"; fi
  if [ -f "$GUARD" ] && [ -f "$GUARD_SRC" ] && ! cmp -s "$GUARD" "$GUARD_SRC"; then
    warn "installed guard differs from this checkout. Run install.sh again to update it."
  fi
  local missing="" p
  for p in SKILL.md data/rejection-patterns.json data/regulatory-deadlines.json docs/PRE-SUBMISSION-CHECKLIST.md references scripts/deadline-checker.py scripts/validate-privacy-manifest.py templates .citation-allowlist; do
    [ -e "$SKILL/$p" ] || missing="$missing $p"
  done
  if [ -z "$missing" ]; then good "skill payload complete at $SHOWN/skills/app-store-compliance"; else fail "skill payload is missing.$missing"; fi
  if [ -f "$CMD_FILE" ]; then good "slash command /app-store-audit installed"; else fail "slash command missing at $SHOWN/commands/app-store-audit.md"; fi
  if hook_registered; then good "hook registered in $SHOWN/settings.json"; else fail "hook is not registered in $SHOWN/settings.json"; fi

  if [ -f "$GUARD" ]; then
    local fx rc out
    fx="$(mktemp -d)"; mkdir -p "$fx/App"
    printf '<plist><dict></dict></plist>' > "$fx/App/Info.plist"
    printf 'import CoreLocation\nclass A { func signIn(){} func createAccount(){} }\nlet m=CLLocationManager()\nlet u="https://staging.example.com"\nimport Stripe\n' > "$fx/App/X.swift"
    bash "$GUARD" "$fx" >/dev/null 2>&1; rc=$?
    if [ "$rc" -eq 2 ]; then good "guard blocks a sample app with known rejection risks"; else fail "guard did not block the sample app when run directly (exit $rc, expected 2)"; fi
    ( cd "$fx" && printf '{"tool_name":"Bash","tool_input":{"command":"fastlane deliver"}}' | env -u CLAUDE_PROJECT_DIR bash "$GUARD" >/dev/null 2>&1 ); rc=$?
    if [ "$rc" -eq 2 ]; then good "guard blocks a submit command as a hook"; else fail "guard did not block a submit command as a hook (exit $rc, expected 2)"; fi
    out="$( cd "$fx" && printf '{"tool_name":"Bash","tool_input":{"command":"ls -la"}}' | env -u CLAUDE_PROJECT_DIR bash "$GUARD" 2>&1 )"; rc=$?
    if [ "$rc" -eq 0 ] && [ -z "$out" ]; then good "guard stays silent on an ordinary command"; else fail "guard reacted to an ordinary command (exit $rc)"; fi
    rm -rf "$fx"
  fi
  have python3 -c pass || warn "python3 not found. The guard still runs, the deadline list and the privacy manifest validator are skipped."
  say ""
  if [ "$PROBLEMS" -eq 0 ]; then
    say "Install verified."
    say "Check your app now.   bash $SHOWN/hooks/$GUARD_NAME /path/to/your/app"
    say "Inside Claude Code.   /app-store-audit"
    say "Restart Claude Code once so it loads the hook."
    return 0
  fi
  say "$PROBLEMS problem(s) above. Fix them, then run. bash $REPO/scripts/install.sh doctor"
  return 1
}

do_install() {
  [ -f "$GUARD_SRC" ] || { echo "Run this from a full checkout. $GUARD_SRC is missing." >&2; exit 1; }
  if [ "$DRY" -eq 1 ]; then
    say "Dry run. Nothing is written."
    say "  would copy the guard to          $SHOWN/hooks/$GUARD_NAME"
    say "  would copy the skill to          $SHOWN/skills/app-store-compliance (SKILL.md, $PAYLOAD_DIRS, .citation-allowlist)"
    say "  would copy the slash command to  $SHOWN/commands/app-store-audit.md"
    say "  would add one PreToolUse Bash hook entry to $SHOWN/settings.json, keeping every other key, with a backup"
    say "  would run the guard against a sample app to prove it blocks"
    exit 0
  fi
  say "Installing the App Store Compliance Playbook into $SHOWN"
  mkdir -p "$CONF/hooks" "$SKILL" "$CONF/commands" || { echo "Cannot write to $CONF" >&2; exit 1; }
  cp "$GUARD_SRC" "$GUARD" && chmod +x "$GUARD"
  cp "$REPO/agent-os/skill/SKILL.md" "$SKILL/SKILL.md"
  cp "$REPO/.citation-allowlist" "$SKILL/.citation-allowlist"
  local d
  for d in $PAYLOAD_DIRS; do
    rm -rf "${SKILL:?}/$d"
    cp -R "$REPO/$d" "$SKILL/$d"
  done
  rm -rf "$SKILL/scripts/__pycache__"
  cp "$REPO/agent-os/commands/app-store-audit.md" "$CMD_FILE"
  good "files copied"

  settings_edit add; local rc=$?
  case "$rc" in
    0) good "hook added to settings.json (a backup sits next to it when the file already existed)" ;;
    3) good "hook already registered, settings.json left as it is" ;;
    4) fail "settings.json is not valid JSON or has an unexpected shape. It was not changed."; manual_block ;;
    *) fail "neither python3 nor jq is installed, so settings.json was not edited."; manual_block ;;
  esac
  verify
}

do_uninstall() {
  if [ "$DRY" -eq 1 ]; then
    say "Dry run. Would remove the guard, the skill folder, the slash command and the hook entry from $SHOWN."; exit 0
  fi
  rm -f "$GUARD" "$CMD_FILE"; rm -rf "$SKILL"
  settings_edit remove; local rc=$?
  case "$rc" in
    0) say "Removed the guard, the skill, the slash command and the hook entry. A backup of settings.json sits next to it." ;;
    3) say "Removed the guard, the skill and the slash command. No hook entry was registered." ;;
    *) say "Removed the files. Could not edit settings.json, remove the $GUARD_NAME entry by hand."; exit 1 ;;
  esac
}

case "$MODE" in
  help) say "Usage. install.sh [install|doctor|uninstall] [--dry-run]"; say "  install    copy the guard, skill and slash command, register the hook, verify (default)"; say "  doctor     verify an existing install, change nothing"; say "  uninstall  remove everything install added"; say "Set CLAUDE_CONFIG_DIR to target a config folder other than ~/.claude." ;;
  install) do_install ;;
  doctor) verify ;;
  uninstall) do_uninstall ;;
esac
