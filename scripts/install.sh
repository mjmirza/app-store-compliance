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
# The hook command is run by a shell, so a custom folder is single-quoted. The default keeps an unquoted tilde.
if [ "$CONF" = "$HOME/.claude" ]; then
  HOOK_CMD="bash $SHOWN/hooks/$GUARD_NAME"
else
  HOOK_CMD="bash '$(printf '%s' "$GUARD" | sed "s/'/'\\\\''/g")'"
fi

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
import json, os, re, shutil, sys, tempfile, time

path, cmd, name, action = sys.argv[1:5]
real = os.path.realpath(path)
exists = os.path.exists(real)
data = {}
if exists:
    try:
        with open(real, encoding="utf-8") as f:
            text = f.read()
        def no_repeats(pairs):
            keys = [k for k, _ in pairs]
            if len(keys) != len(set(keys)):
                raise ValueError("repeated key")
            return dict(pairs)

        data = json.loads(text, object_pairs_hook=no_repeats) if text.strip() else {}
    except Exception:
        sys.exit(4)
    if not os.access(real, os.W_OK):
        sys.exit(6)
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


def fires(e, h):
    # Only an entry Claude Code would run for a Bash call counts. Wrong matcher or a commented name does not.
    m = e.get("matcher", "")
    c = str(h.get("command", "")).strip()
    try:
        on_bash = m in ("", "*") or re.fullmatch(m, "Bash") is not None
    except re.error:
        on_bash = False
    runs = c.startswith("bash ") and "#" not in c and c.rstrip("'\"").endswith(name)
    return ours(h) and on_bash and runs and h.get("type", "command") == "command"


changed = False
if action == "add":
    found = [h for e in pre for h in e.get("hooks", []) if fires(e, h)]
else:
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
    shutil.copy2(real, path + ".bak-" + time.strftime("%Y%m%d-%H%M%S") + "-" + str(os.getpid()))
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
      jq -e 'type == "object" and ((.hooks // {}) | type == "object") and ((.hooks.PreToolUse // []) | type == "array") and ((.hooks.PreToolUse // []) | all(type == "object" and ((.hooks // []) | type == "array")))' "$cur" >/dev/null 2>&1 || return 4
      [ -w "$cur" ] || return 6
    fi
    local present=1
    [ -n "$cur" ] && jq -e --arg n "$GUARD_NAME" '[.hooks.PreToolUse[]? | select((.matcher // "") == "Bash" or (.matcher // "") == "" or .matcher == "*") | .hooks[]?.command? // "" | tostring | select(startswith("bash ") and contains($n) and (contains("#") | not))] | length > 0' "$cur" >/dev/null 2>&1 && present=0
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

# Prints the registered command Claude Code would run for a Bash call, empty when there is none.
registered_cmd() {
  [ -f "$SETTINGS" ] || return 0
  if have python3 -c pass; then
    python3 -c 'import json,re,sys
try: d=json.load(open(sys.argv[1]))
except Exception: sys.exit(0)
n=sys.argv[2]
for e in d.get("hooks",{}).get("PreToolUse",[]):
    if not isinstance(e,dict): continue
    m=e.get("matcher","")
    try: ok=m in ("","*") or re.fullmatch(m,"Bash") is not None
    except re.error: ok=False
    if not ok: continue
    for h in e.get("hooks",[]):
        c=str(h.get("command","")) if isinstance(h,dict) else ""
        if n in c and "#" not in c and c.strip().startswith("bash "):
            print(c); sys.exit(0)' "$SETTINGS" "$GUARD_NAME" 2>/dev/null
    return 0
  fi
  if have jq -n true; then
    jq -r --arg n "$GUARD_NAME" '[.hooks.PreToolUse[]? | select((.matcher // "") == "Bash" or (.matcher // "") == "" or .matcher == "*") | .hooks[]?.command? // "" | tostring | select(startswith("bash ") and contains($n) and (contains("#") | not))] | first // empty' "$SETTINGS" 2>/dev/null
    return 0
  fi
  grep -q "$GUARD_NAME" "$SETTINGS" 2>/dev/null && printf '%s\n' "$HOOK_CMD"
  return 0
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
  local reg; reg="$(registered_cmd)"
  if [ -n "$reg" ]; then good "hook registered for Bash in $SHOWN/settings.json"; else fail "no working hook entry for Bash in $SHOWN/settings.json"; fi

  if [ -f "$GUARD" ]; then
    local fx rc out
    fx="$(mktemp -d)"; mkdir -p "$fx/App"
    printf '<plist><dict></dict></plist>' > "$fx/App/Info.plist"
    printf 'import CoreLocation\nclass A { func signIn(){} func createAccount(){} }\nlet m=CLLocationManager()\nlet u="https://staging.example.com"\nimport Stripe\n' > "$fx/App/X.swift"
    bash "$GUARD" "$fx" >/dev/null 2>&1; rc=$?
    if [ "$rc" -eq 2 ]; then good "guard blocks a sample app with known rejection risks"; else fail "guard did not block the sample app when run directly (exit $rc, expected 2)"; fi
    # The registered command string is what Claude Code runs, so that exact string is what gets tested.
    if [ -n "$reg" ]; then
      ( cd "$fx" && printf '{"tool_name":"Bash","tool_input":{"command":"fastlane deliver"}}' | env -u CLAUDE_PROJECT_DIR bash -c "$reg" >/dev/null 2>&1 ); rc=$?
      if [ "$rc" -eq 2 ]; then good "the registered hook command blocks a submit command"; else fail "the registered hook command did not block a submit command (exit $rc, expected 2). Command. $reg"; fi
      out="$( cd "$fx" && printf '{"tool_name":"Bash","tool_input":{"command":"ls -la"}}' | env -u CLAUDE_PROJECT_DIR bash -c "$reg" 2>&1 )"; rc=$?
      if [ "$rc" -eq 0 ] && [ -z "$out" ]; then good "the registered hook command stays silent on an ordinary command"; else fail "the registered hook command reacted to an ordinary command (exit $rc)"; fi
    fi
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
    4) fail "settings.json is not valid JSON, repeats a key, or has an unexpected shape. It was not changed."; manual_block ;;
    6) fail "settings.json is read-only. It was not changed."; manual_block ;;
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
