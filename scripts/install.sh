#!/usr/bin/env bash
# One command setup for Claude Code and, with --tool, eleven other AI coding tools. Installs the guard,
# skill and command, registers the hook, then proves it blocks a bad app. Run with --help for usage.
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [ -z "${CLAUDE_CONFIG_DIR:-}" ] && [ -z "${HOME:-}" ]; then
  echo "HOME is not set, so there is no folder to install into. Set HOME or CLAUDE_CONFIG_DIR, then run this again." >&2
  exit 1
fi
CONF="${CLAUDE_CONFIG_DIR:-${HOME:-}/.claude}"
GUARD_NAME="app-store-compliance-guard.sh"
GUARD_SRC="$REPO/agent-os/hooks/$GUARD_NAME"
GUARD="$CONF/hooks/$GUARD_NAME"
SKILL="$CONF/skills/app-store-compliance"
CMD_FILE="$CONF/commands/app-store-audit.md"
SETTINGS="$CONF/settings.json"
PAYLOAD_DIRS="docs data references templates scripts"
# Claude Code on Windows may run commands through PowerShell, so the hook covers both there.
case "${ASC_UNAME:-$(uname -s 2>/dev/null)}" in
  MINGW*|MSYS*|CYGWIN*) MATCHER="Bash|PowerShell" ;;
  *) MATCHER="Bash" ;;
esac
export ASC_MATCHER="$MATCHER"

# shellcheck disable=SC2088
if [ "$CONF" = "${HOME:-}/.claude" ]; then SHOWN='~/.claude'; else SHOWN="$CONF"; fi
# The hook command is run by a shell, so a custom folder is single-quoted. The default keeps an unquoted tilde.
if [ "$CONF" = "${HOME:-}/.claude" ]; then
  HOOK_CMD="bash $SHOWN/hooks/$GUARD_NAME"
else
  HOOK_CMD="bash '$(printf '%s' "$GUARD" | sed "s/'/'\\\\''/g")'"
fi

MODE="install"; DRY=0; TOOL="claude"; REPO_DIR=""
TOOL_NAMES="claude|codex|gemini|opencode|cursor|copilot|copilot-repo|grok|qwen|kimi|droid|auggie|windsurf|all"
USAGE="Usage. install.sh [install|doctor|uninstall] [--tool $TOOL_NAMES] [--repo DIR] [--dry-run] [--version]"
while [ "$#" -gt 0 ]; do
  case "$1" in
    install|doctor|uninstall) MODE="$1" ;;
    --dry-run) DRY=1 ;;
    -h|--help) MODE="help" ;;
    --version) MODE="version" ;;
    --tool=*) TOOL="${1#--tool=}" ;;
    --tool) [ "$#" -ge 2 ] || { echo "--tool needs a name." >&2; echo "$USAGE" >&2; exit 2; }; TOOL="$2"; shift ;;
    --repo=*) REPO_DIR="${1#--repo=}" ;;
    --repo) [ "$#" -ge 2 ] || { echo "--repo needs a folder." >&2; exit 2; }; REPO_DIR="$2"; shift ;;
    *) echo "Unknown argument. $1" >&2; echo "$USAGE" >&2; exit 2 ;;
  esac
  shift
done
case "$TOOL" in
  claude|codex|gemini|opencode|cursor|copilot|copilot-repo|grok|qwen|kimi|droid|auggie|windsurf|all) ;;
  *) echo "Unknown tool. $TOOL" >&2; echo "$USAGE" >&2; exit 2 ;;
esac

# Every other tool is installed by install_harness.py, which merges that tool's own config file.
run_harness() {
  if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 is needed to install for $1. Install python3, or follow the manual steps in the README." >&2
    return 1
  fi
  local args=("$1" "$MODE"); [ "$DRY" -eq 1 ] && args+=(--dry-run); [ -n "$REPO_DIR" ] && args+=(--repo "$REPO_DIR")
  python3 "$REPO/scripts/install_harness.py" "${args[@]}"
}
if [ "$TOOL" = "all" ] && [ "$MODE" != "help" ] && [ "$MODE" != "version" ]; then
  found=""; rc_all=0
  [ -d "$CONF" ] && found="claude"
  [ -d "${CODEX_HOME:-${HOME:-}/.codex}" ] && found="$found codex"
  [ -d "${HOME:-}/.gemini" ] && found="$found gemini"
  [ -d "${XDG_CONFIG_HOME:-${HOME:-}/.config}/opencode" ] && found="$found opencode"
  [ -d "${HOME:-}/.cursor" ] && found="$found cursor"
  CDIR="${COPILOT_HOME:-${HOME:-}/.copilot}"; case "$CDIR" in [~]|[~]/*|[~]\\*) CDIR="${CDIR#\~}"; CDIR="${HOME:-}/${CDIR#?}" ;; esac
  [ -d "$CDIR" ] && found="$found copilot"
  [ -d "${HOME:-}/.grok" ] && found="$found grok"
  QDIR="${QWEN_HOME:-${HOME:-}/.qwen}"; case "$QDIR" in [~]|[~]/*|[~]\\*) QDIR="${QDIR#\~}"; QDIR="${HOME:-}/${QDIR#?}" ;; esac
  [ -d "$QDIR" ] && found="$found qwen"
  KDIR="${KIMI_CODE_HOME:-${HOME:-}/.kimi-code}"; case "$KDIR" in [~]|[~]/*|[~]\\*) KDIR="${KDIR#\~}"; KDIR="${HOME:-}/${KDIR#?}" ;; esac
  [ -d "$KDIR" ] && found="$found kimi"
  [ -d "${HOME:-}/.factory" ] && found="$found droid"
  [ -d "${HOME:-}/.augment" ] && found="$found auggie"
  [ -d "${HOME:-}/.codeium/windsurf" ] && found="$found windsurf"
  [ -z "$found" ] && { echo "No supported AI coding tool found in your home folder. Pass --tool with one name."; exit 1; }
  echo "Found.$found"
  for t in $found; do
    echo ""; echo "== $t =="
    flags=("$MODE"); [ "$DRY" -eq 1 ] && flags+=(--dry-run)
    bash "$0" --tool "$t" "${flags[@]}" || rc_all=1
  done
  echo ""
  if [ "$rc_all" -eq 0 ]; then echo "All tools done."; else echo "At least one tool reported a problem above."; fi
  exit "$rc_all"
fi
if [ "$TOOL" != "claude" ] && [ "$MODE" != "help" ] && [ "$MODE" != "version" ]; then
  run_harness "$TOOL"; exit $?
fi

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
        "matcher": "$MATCHER",
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
    python3 - "$SETTINGS" "$HOOK_CMD" "$GUARD_NAME" "$action" "$GUARD" "$SHOWN/hooks/$GUARD_NAME" <<'PY'
import json, os, re, shutil, sys, tempfile, time

path, cmd, name, action = sys.argv[1:5]
spots = list(sys.argv[5:7])
spots += [h + s[2:] for s in list(spots) if s.startswith("~/") for h in ("$HOME/", "${HOME}/")]
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
    # Ours means this folder's guard. A guard of the same file name somewhere else belongs to someone else.
    c = str(h.get("command", "")) if isinstance(h, dict) else ""
    c = c.strip()
    return c == cmd or any(c in ("bash " + s, "bash '" + s + "'", 'bash "' + s + '"') for s in spots)


TOOLS = ["Bash"] + (["PowerShell"] if "PowerShell" in os.environ.get("ASC_MATCHER", "") else [])


def hits(m, tool):
    try:
        return m in ("", "*") or re.fullmatch(m, tool) is not None
    except re.error:
        return False


def fires(e, h, tools=("Bash",)):
    # Only an entry Claude Code would run for a Bash call counts. Wrong matcher or a commented name does not.
    m = e.get("matcher", "")
    c = str(h.get("command", "")).strip()
    on_bash = all(hits(m, t) for t in tools)
    runs = c.startswith("bash ") and "#" not in c and c.rstrip("'\"").endswith(name)
    return ours(h) and on_bash and runs and h.get("type", "command") == "command"


changed = False
if action == "add":
    found = [h for e in pre for h in e.get("hooks", []) if fires(e, h)]
else:
    found = [h for e in pre for h in e.get("hooks", []) if ours(h)]
if action == "add" and found and len(TOOLS) > 1:
    # On Windows an owned entry must also match PowerShell. A group holding only ours is widened in place,
    # otherwise ours moves to its own group so another hook's matcher is never changed.
    for e in list(pre):
        mine = [h for h in e.get("hooks", []) if fires(e, h) and not fires(e, h, TOOLS)]
        if not mine:
            continue
        if len(mine) == len(e.get("hooks", [])):
            e["matcher"] = os.environ.get("ASC_MATCHER", "Bash")
        else:
            e["hooks"] = [h for h in e["hooks"] if h not in mine]
            pre.append({"matcher": os.environ.get("ASC_MATCHER", "Bash"), "hooks": mine})
        changed = True
if action == "add":
    if found:
        for h in found:
            t = h.get("timeout")
            if not isinstance(t, (int, float)) or t < 120:
                h["timeout"] = 120
                changed = True
            if h.get("async") not in (None, False):
                h.pop("async", None)
                changed = True
    else:
        pre.append(
            {"matcher": os.environ.get("ASC_MATCHER", "Bash"), "hooks": [{"type": "command", "command": cmd, "timeout": 120}]}
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
      # --stream reads every key as written, a parse keeps only the last of a repeated key. Unequal counts mean a repeat.
      [ "$(jq -c --stream . "$cur" 2>/dev/null | wc -l)" -eq "$(jq -c tostream "$cur" 2>/dev/null | wc -l)" ] || return 4
    fi
    local present=1
    [ -n "$cur" ] && jq -e --arg m "$MATCHER" --arg hc "$HOOK_CMD" --arg g "$GUARD" --arg t "$SHOWN/hooks/$GUARD_NAME" '[.hooks.PreToolUse[]? | select((.matcher // "") == $m or (.matcher // "") == "" or .matcher == "*") | .hooks[]? | select(type == "object" and ((.async // false) == false) and ((.type // "command") == "command") and (((.timeout // 600) | numbers) >= 120)) | .command? // "" | tostring | select(startswith("bash ") and (. as $c | $c == $hc or ([$g, $t] | any(. as $s | $c == "bash " + $s or $c == "bash \u0027" + $s + "\u0027" or $c == "bash \"" + $s + "\""))) and (contains("#") | not))] | length > 0' "$cur" >/dev/null 2>&1 && present=0
    if [ "$action" = "add" ]; then
      [ "$present" -eq 0 ] && return 3
      mkdir -p "$CONF"; tmp="$(mktemp "$CONF/.settings-XXXXXX")" || return 4
      if [ -n "$cur" ]; then cp -p "$cur" "$SETTINGS.bak-$(date +%Y%m%d-%H%M%S)"; else cur="/dev/null"; fi
      if [ "$cur" = "/dev/null" ]; then printf '{}' > "$tmp.in"; cur="$tmp.in"; fi
      # An owned entry on a narrower matcher is dropped first, so the widened one never duplicates it.
      jq --arg c "$HOOK_CMD" --arg m "$MATCHER" --arg g "$GUARD" --arg t "$SHOWN/hooks/$GUARD_NAME" '.hooks.PreToolUse = (((.hooks.PreToolUse // []) | map(.hooks |= map(select((.command? // "" | tostring | (. as $x | $x == $c or ([$g, $t] | any(. as $s | $x == "bash " + $s or $x == "bash \u0027" + $s + "\u0027" or $x == "bash \"" + $s + "\"")))) | not)) | select((.hooks | length) > 0))) + [{matcher: $m, hooks: [{type: "command", command: $c, timeout: 120}]}])' "$cur" > "$tmp" || { rm -f "$tmp" "$tmp.in"; return 4; }
      rm -f "$tmp.in"; mv "$tmp" "$SETTINGS"; return 0
    fi
    # Removal owns its handler under any matcher, so an older Bash-only entry is removed too.
    [ -n "$cur" ] && jq -e --arg hc "$HOOK_CMD" --arg g "$GUARD" --arg t "$SHOWN/hooks/$GUARD_NAME" '[.hooks.PreToolUse[]? | .hooks[]?.command? // "" | tostring | select(. as $c | $c == $hc or ([$g, $t] | any(. as $s | $c == "bash " + $s or $c == "bash \u0027" + $s + "\u0027" or $c == "bash \"" + $s + "\"")))] | length > 0' "$cur" >/dev/null 2>&1 && present=0
    [ "$present" -ne 0 ] && return 3
    tmp="$(mktemp "$CONF/.settings-XXXXXX")" || return 4
    cp -p "$cur" "$SETTINGS.bak-$(date +%Y%m%d-%H%M%S)"
    jq --arg hc "$HOOK_CMD" --arg g "$GUARD" --arg t "$SHOWN/hooks/$GUARD_NAME" '.hooks.PreToolUse |= (map(.hooks |= map(select((.command? // "" | tostring | (. as $c | $c == $hc or ([$g, $t] | any(. as $s | $c == "bash " + $s or $c == "bash \u0027" + $s + "\u0027" or $c == "bash \"" + $s + "\"")))) | not))) | map(select((.hooks | length) > 0)))' "$cur" > "$tmp" || { rm -f "$tmp"; return 4; }
    mv "$tmp" "$SETTINGS"; return 0
  fi
  return 5
}

# Prints the registered command Claude Code would run for a Bash call, empty when there is none.
registered_cmd() {
  [ -f "$SETTINGS" ] || return 0
  if have python3 -c pass; then
    python3 -c 'import json,os,re,sys
try: d=json.load(open(sys.argv[1]))
except Exception: sys.exit(0)
hc=sys.argv[2]
n=sys.argv[3:]
n+=[h+s[2:] for s in list(n) if s.startswith("~/") for h in ("$HOME/","${HOME}/")]
for e in d.get("hooks",{}).get("PreToolUse",[]):
    if not isinstance(e,dict): continue
    m=e.get("matcher","")
    tools=["Bash"]+(["PowerShell"] if "PowerShell" in os.environ.get("ASC_MATCHER","") else [])
    try: ok=all(m in ("","*") or re.fullmatch(m,t) is not None for t in tools)
    except re.error: ok=False
    if not ok: continue
    for h in e.get("hooks",[]):
        if not isinstance(h,dict) or h.get("type","command")!="command": continue
        t=h.get("timeout",600)
        if isinstance(t,bool) or not isinstance(t,(int,float)) or t<30: continue
        if h.get("async") not in (None,False): continue
        c=str(h.get("command",""))
        if (c.strip()==hc or any(c.strip() in ("bash " + s, "bash \"" + s + "\"", "bash \u0027" + s + "\u0027") for s in n)) and "#" not in c and c.strip().startswith("bash "):
            print(c); sys.exit(0)' "$SETTINGS" "$HOOK_CMD" "$GUARD" "$SHOWN/hooks/$GUARD_NAME" 2>/dev/null
    return 0
  fi
  if have jq -n true; then
    jq -r --arg m "$MATCHER" --arg hc "$HOOK_CMD" --arg g "$GUARD" --arg t "$SHOWN/hooks/$GUARD_NAME" '[.hooks.PreToolUse[]? | select((.matcher // "") == $m or (.matcher // "") == "" or .matcher == "*") | .hooks[]? | select(type == "object" and (.type // "command") == "command" and ((.async // false) == false) and (((.timeout // 600) | numbers) >= 30)) | .command? // "" | tostring | select(startswith("bash ") and (. as $c | $c == $hc or ([$g, $t] | any(. as $s | $c == "bash " + $s or $c == "bash \u0027" + $s + "\u0027" or $c == "bash \"" + $s + "\""))) and (contains("#") | not))] | first // empty' "$SETTINGS" 2>/dev/null
    return 0
  fi
  grep -qF "$SHOWN/hooks/$GUARD_NAME" "$SETTINGS" 2>/dev/null && printf '%s\n' "$HOOK_CMD"
  return 0
}

# Proves the install. Every line is a real check, the guard is run against a built-in app that must be blocked.
verify() {
  say ""; say "Checking the install."
  if [ -f "$GUARD" ]; then good "guard present at $SHOWN/hooks/$GUARD_NAME"; else fail "guard missing at $SHOWN/hooks/$GUARD_NAME"; fi
  if [ -f "$GUARD" ] && [ -f "$GUARD_SRC" ] && ! cmp -s "$GUARD" "$GUARD_SRC"; then
    warn "installed guard differs from this checkout. Run install.sh again to update it."
  fi
  if [ -f "$SKILL/VERSION" ]; then
    good "version $(cat "$SKILL/VERSION")"
    if [ -f "$REPO/VERSION" ] && ! cmp -s "$SKILL/VERSION" "$REPO/VERSION"; then
      warn "this checkout is version $(cat "$REPO/VERSION"). Run install.sh again to update."
    fi
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
      if [ "$MATCHER" != "Bash" ]; then
        ( cd "$fx" && printf '{"tool_name":"PowerShell","tool_input":{"command":"fastlane deliver"}}' | env -u CLAUDE_PROJECT_DIR bash -c "$reg" >/dev/null 2>&1 ); rc=$?
        if [ "$rc" -eq 2 ]; then good "the registered hook command blocks a submit command run through PowerShell"; else fail "the registered hook command did not block a PowerShell submit command (exit $rc)"; fi
      fi
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
  [ -f "$REPO/VERSION" ] && cp "$REPO/VERSION" "$SKILL/VERSION"
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
  version) printf 'app-store-compliance %s\n' "$(cat "$REPO/VERSION" 2>/dev/null || echo unknown)" ;;
  help) say "$USAGE"; say "  --tool     the AI coding tool to install into, claude by default. all installs into every one found"; say "  --repo     with --tool copilot-repo, the app repository whose .github/hooks gets the guard"; say "  install    copy the guard, skill and slash command, register the hook, verify (default)"; say "  doctor     verify an existing install, change nothing"; say "  uninstall  remove everything install added"; say "Set CLAUDE_CONFIG_DIR to target a config folder other than ~/.claude." ;;
  install) do_install ;;
  doctor) verify ;;
  uninstall) do_uninstall ;;
esac
