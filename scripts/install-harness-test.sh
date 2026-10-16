#!/usr/bin/env bash
# Tests install.sh --tool for every supported tool other than Claude Code, in a throwaway HOME.
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
run()   { env -u QWEN_HOME -u KIMI_CODE_HOME -u COPILOT_HOME -u CODEX_HOME -u XDG_CONFIG_HOME -u CLAUDE_CONFIG_DIR -u CLAUDE_PROJECT_DIR HOME="$H" bash "$INSTALL" "$@" 2>&1; }
cfg() {
  case "$1" in
    codex) echo "$H/.codex/hooks.json" ;;
    gemini) echo "$H/.gemini/settings.json" ;;
    opencode) echo "$H/.config/opencode/plugins/app-store-compliance.js" ;;
    cursor) echo "$H/.cursor/hooks.json" ;;
    copilot) echo "$H/.copilot/hooks/app-store-compliance.json" ;;
    grok) echo "$H/.grok/hooks/app-store-compliance.json" ;;
    qwen) echo "$H/.qwen/settings.json" ;;
    kimi) echo "$H/.kimi-code/config.toml" ;;
    droid) echo "$H/.factory/hooks.json" ;;
    auggie) echo "$H/.augment/settings.json" ;;
    windsurf) echo "$H/.codeium/windsurf/hooks.json" ;;
  esac
}
gdir() {  # where each tool's guard lands
  case "$1" in
    opencode) echo "$H/.config/opencode/hooks" ;; kimi) echo "$H/.kimi-code/hooks" ;; droid) echo "$H/.factory/hooks" ;;
    auggie) echo "$H/.augment/hooks" ;; windsurf) echo "$H/.codeium/windsurf/hooks" ;; *) echo "$H/.$1/hooks" ;;
  esac
}
count() {  # how many hook entries point at the guard
  if [ "$1" = "kimi" ]; then grep -c "app-store-compliance-guard.sh" "$(cfg kimi)" 2>/dev/null || true; return; fi
  python3 - "$1" "$(cfg "$1")" <<'PY'
import json, sys
tool, path = sys.argv[1], sys.argv[2]
key = {"codex": "PreToolUse", "gemini": "BeforeTool", "cursor": "beforeShellExecution", "copilot": "preToolUse",
       "grok": "PreToolUse", "qwen": "PreToolUse", "droid": "PreToolUse", "auggie": "PreToolUse", "windsurf": "pre_run_command"}[tool]
try:
    d = json.load(open(path))
except Exception:
    print(0); sys.exit()
box = d if tool == "droid" else d.get("hooks", {})
groups = box.get(key, [])
n = 0
for g in groups:
    items = g.get("hooks", []) if tool in ("codex", "gemini", "grok", "qwen", "droid", "auggie") else [g]
    n += sum("app-store-compliance-guard.sh" in str(h.get("command", h.get("bash", ""))) for h in items)
print(n)
PY
}

for t in codex gemini opencode cursor copilot grok qwen kimi droid auggie windsurf; do
  # 1 a fresh install verifies itself end to end
  fresh
  OUT="$(run --tool "$t")"; RC=$?
  [ "$RC" -eq 0 ] && echo "$OUT" | grep -q "^Install verified\." && ok "$t fresh install verifies" || { bad "$t fresh install verifies (rc=$RC)"; echo "$OUT" | tail -15; }
  [ -x "$(gdir "$t")/app-store-compliance-guard.sh" ] && ok "$t guard is installed and executable" || bad "$t guard is installed and executable"
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

# 2b vendor-specific shapes. Copilot carries its own entry and the one VS Code reads, Auggie counts milliseconds.
fresh; run --tool copilot >/dev/null; run --tool auggie >/dev/null; run --tool windsurf >/dev/null
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); a=d["hooks"]["preToolUse"][0]; b=d["hooks"]["PreToolUse"][0]; sys.exit(0 if d["version"]==1 and a["timeoutSec"]==120 and a["bash"].endswith("guard.sh'"'"'") and b["timeout"]==120 and b["command"]==a["bash"] else 1)' "$H/.copilot/hooks/app-store-compliance.json" \
  && ok "copilot file carries the Copilot entry and the VS Code entry" || bad "copilot file carries the Copilot entry and the VS Code entry"
python3 -c 'import json,sys; a=json.load(open(sys.argv[1]))["hooks"]["preToolUse"][0]; p=a.get("powershell",""); sys.exit(0 if p.startswith("$input | & bash ") and "app-store-compliance-guard.sh" in p and p.rstrip().endswith("exit $LASTEXITCODE") else 1)' "$H/.copilot/hooks/app-store-compliance.json" \
  && ok "copilot also carries a Windows powershell handler that pipes the payload to the guard and keeps its exit code" || bad "copilot also carries a Windows powershell handler that pipes the payload to the guard and keeps its exit code"
python3 -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); d["hooks"]["preToolUse"][0].pop("powershell",None); json.dump(d,open(p,"w"))' "$H/.copilot/hooks/app-store-compliance.json"
run --tool copilot doctor >/dev/null; RC=$?
[ "$RC" -eq 1 ] && ok "copilot doctor fails when the Windows handler is missing" || bad "copilot doctor fails when the Windows handler is missing (rc=$RC)"
run --tool copilot >/dev/null
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); e=d["hooks"]["preToolUse"]; sys.exit(0 if len(e)==1 and e[0].get("powershell") else 1)' "$H/.copilot/hooks/app-store-compliance.json" \
  && ok "copilot install adds the missing Windows handler without a duplicate" || bad "copilot install adds the missing Windows handler without a duplicate"
python3 -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); d["hooks"]["preToolUse"][0]["powershell"]="Write-Output app-store-compliance-guard.sh; exit $LASTEXITCODE"; json.dump(d,open(p,"w"))' "$H/.copilot/hooks/app-store-compliance.json"
run --tool copilot doctor >/dev/null; RC=$?
[ "$RC" -eq 1 ] && ok "copilot doctor fails when the Windows handler was edited" || bad "copilot doctor fails when the Windows handler was edited (rc=$RC)"
run --tool copilot >/dev/null
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); g=d["hooks"]["PreToolUse"][0]; sys.exit(0 if g["matcher"]=="launch-process" and g["hooks"][0]["timeout"]==120000 else 1)' "$H/.augment/settings.json" \
  && ok "auggie uses launch-process and a millisecond timeout" || bad "auggie uses launch-process and a millisecond timeout"
python3 -c 'import json,os,sys; c=json.load(open(sys.argv[1]))["hooks"]["PreToolUse"][0]["hooks"][0]["command"]; sys.exit(0 if c==sys.argv[2] and os.access(c,os.X_OK) and open(c).readline().startswith("#!") else 1)' "$H/.augment/settings.json" "$H/.augment/hooks/app-store-compliance-guard.sh" \
  && ok "auggie registers the executable guard script path, as its docs require" || bad "auggie registers the executable guard script path, as its docs require"
python3 -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); h=d["hooks"]["PreToolUse"][0]["hooks"][0]; h["command"]="bash "+h["command"]; json.dump(d,open(p,"w"))' "$H/.augment/settings.json"
run --tool auggie doctor >/dev/null; RC=$?
[ "$RC" -eq 1 ] && ok "auggie doctor fails on a shell command string" || bad "auggie doctor fails on a shell command string (rc=$RC)"
run --tool auggie >/dev/null; run --tool auggie doctor >/dev/null; RC=$?
[ "$RC" -eq 0 ] && [ "$(count auggie)" = "1" ] && ok "auggie install replaces the shell string with the script path once" || bad "auggie install replaces the shell string with the script path once (rc=$RC entries=$(count auggie))"
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); e=d["hooks"]["pre_run_command"][0]; sys.exit(0 if e["show_output"] is True else 1)' "$H/.codeium/windsurf/hooks.json" \
  && ok "windsurf shows the guard output to the user" || bad "windsurf shows the guard output to the user"

# 2b2 Grok runs its shell through run_terminal_command, run_terminal_cmd, bash and monitor, in a camelCase payload
fresh; run --tool grok >/dev/null
python3 -c 'import json,re,sys; m=json.load(open(sys.argv[1]))["hooks"]["PreToolUse"][0]["matcher"]; sys.exit(0 if m=="Bash|run_terminal_command|run_terminal_cmd|bash|monitor" and all(re.fullmatch(m,t) for t in ("run_terminal_command","run_terminal_cmd","bash","monitor")) else 1)' "$(cfg grok)" \
  && ok "grok matcher covers every Grok shell tool" || bad "grok matcher covers every Grok shell tool"
GLOG="$WORK/grok-payload$RANDOM.json"; GG="$(gdir grok)/app-store-compliance-guard.sh"; cp "$GG" "$WORK/grok-guard.bak"
printf '#!/usr/bin/env bash\ncat > "%s"\ngrep -q deliver "%s" && exit 2\nexit 0\n' "$GLOG" "$GLOG" > "$GG"
run --tool grok doctor >/dev/null
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if d.get("toolName")=="run_terminal_command" and d.get("hookEventName")=="PreToolUse" and "command" in d.get("toolInput",{}) else 1)' "$GLOG" 2>/dev/null \
  && ok "grok doctor feeds a run_terminal_command payload" || bad "grok doctor feeds a run_terminal_command payload"
cp "$WORK/grok-guard.bak" "$GG"
python3 -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); d["hooks"]["PreToolUse"][0]["matcher"]="Bash"; json.dump(d,open(p,"w"))' "$(cfg grok)"
run --tool grok doctor >/dev/null; RC=$?
[ "$RC" -eq 1 ] && ok "grok doctor fails on an old Bash-only matcher" || bad "grok doctor fails on an old Bash-only matcher (rc=$RC)"
run --tool grok >/dev/null; run --tool grok doctor >/dev/null; RC=$?
python3 -c 'import json,sys; g=json.load(open(sys.argv[1]))["hooks"]["PreToolUse"]; sys.exit(0 if [x["matcher"] for x in g]==["Bash|run_terminal_command|run_terminal_cmd|bash|monitor"] else 1)' "$(cfg grok)" && [ "$RC" -eq 0 ] && [ "$(count grok)" = "1" ] \
  && ok "grok install repairs a Bash-only matcher once and doctor then passes" || bad "grok install repairs a Bash-only matcher once and doctor then passes (rc=$RC entries=$(count grok))"

# 2c Droid keeps using settings.json when its hooks live there, and never shadows them with a new hooks.json
fresh; mkdir -p "$H/.factory"
printf '{"model":"x","hooks":{"PostToolUse":[{"matcher":"Edit","hooks":[{"type":"command","command":"fmt"}]}]}}' > "$H/.factory/settings.json"
OUT="$(run --tool droid)"; RC=$?
[ "$RC" -eq 0 ] && [ ! -e "$H/.factory/hooks.json" ] && python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if d["model"]=="x" and d["hooks"]["PostToolUse"] and d["hooks"]["PreToolUse"][0]["matcher"]=="Execute" else 1)' "$H/.factory/settings.json" \
  && ok "droid adds to settings.json when its hooks already live there" || bad "droid adds to settings.json when its hooks already live there (rc=$RC)"
run --tool droid uninstall >/dev/null
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if "PreToolUse" not in d["hooks"] and d["hooks"]["PostToolUse"] else 1)' "$H/.factory/settings.json" \
  && ok "droid uninstall keeps the other settings.json hooks" || bad "droid uninstall keeps the other settings.json hooks"

# 2d Kimi. A config holding a secret is appended to, never rewritten, and uninstall restores it exactly
fresh; mkdir -p "$H/.kimi-code"
printf 'default_model = "k2"\n\n[providers.moonshot]\n%s = "%s"\n' "api""_key" "fixture-not-a-secret" > "$H/.kimi-code/config.toml"
cp "$H/.kimi-code/config.toml" "$WORK/kimi-orig.toml"
OUT="$(run --tool kimi)"; RC=$?
[ "$RC" -eq 0 ] && grep -q '= "fixture-not-a-secret"' "$H/.kimi-code/config.toml" && python3 -c 'import sys,tomllib; d=tomllib.load(open(sys.argv[1],"rb")); h=d["hooks"][0]; sys.exit(0 if h["event"]=="PreToolUse" and h["matcher"]=="^Bash$" and h["timeout"]==120 else 1)' "$H/.kimi-code/config.toml" \
  && ok "kimi appends a valid hook block and keeps the existing settings" || bad "kimi appends a valid hook block and keeps the existing settings (rc=$RC)"
! echo "$OUT" | grep -q "fixture-not-a-secret" && ok "kimi install never prints the config contents" || bad "kimi install never prints the config contents"
run --tool kimi >/dev/null
[ "$(count kimi)" = "1" ] && ok "kimi a second run adds nothing" || bad "kimi a second run adds nothing"
run --tool kimi uninstall >/dev/null
cmp -s "$H/.kimi-code/config.toml" "$WORK/kimi-orig.toml" && ok "kimi uninstall restores the file exactly" || bad "kimi uninstall restores the file exactly"
for tail in "" "\n" "\n\n\n"; do
  fresh; mkdir -p "$H/.kimi-code"; printf "default_model = \"k2\"$tail" > "$H/.kimi-code/config.toml"; cp "$H/.kimi-code/config.toml" "$WORK/kimi-orig.toml"
  run --tool kimi >/dev/null; run --tool kimi uninstall >/dev/null
  cmp -s "$H/.kimi-code/config.toml" "$WORK/kimi-orig.toml" && ok "kimi uninstall keeps the original trailing newlines (${#tail} chars)" || bad "kimi uninstall keeps the original trailing newlines (${#tail} chars)"
done

# 2d2 KIMI_CODE_HOME moves Kimi's whole data folder, so the hook goes where Kimi reads it
fresh; mkdir -p "$H/kimi-custom"; printf 'default_model = "k2"\n' > "$H/kimi-custom/config.toml"
OUT="$(env -u QWEN_HOME -u CODEX_HOME -u XDG_CONFIG_HOME HOME="$H" KIMI_CODE_HOME="$H/kimi-custom" bash "$INSTALL" --tool kimi 2>&1)"; RC=$?
[ "$RC" -eq 0 ] && grep -q "app-store-compliance-guard.sh" "$H/kimi-custom/config.toml" && [ ! -e "$H/.kimi-code/config.toml" ] && ok "kimi follows KIMI_CODE_HOME" || bad "kimi follows KIMI_CODE_HOME (rc=$RC)"
OUT="$(env -u QWEN_HOME -u CODEX_HOME -u XDG_CONFIG_HOME HOME="$H" KIMI_CODE_HOME="$H/kimi-custom" bash "$INSTALL" --tool all 2>&1)"
echo "$OUT" | grep -q "== kimi ==" && ok "auto discovery finds Kimi under KIMI_CODE_HOME" || bad "auto discovery finds Kimi under KIMI_CODE_HOME"
# 2d3 an inline hooks array cannot take a [[hooks]] block, so the file is left as it was and the block is shown
fresh; mkdir -p "$H/.kimi-code"
printf 'hooks = [{event = "PreToolUse", matcher = "^Bash$", command = "bash /other/check.sh", timeout = 120}]\ndefault_model = "k2"\n' > "$H/.kimi-code/config.toml"
cp "$H/.kimi-code/config.toml" "$WORK/kimi-inline.toml"
OUT="$(run --tool kimi)"; RC=$?
[ "$RC" -ne 0 ] && cmp -s "$H/.kimi-code/config.toml" "$WORK/kimi-inline.toml" && echo "$OUT" | grep -q "\[\[hooks\]\]" && ok "kimi refuses an inline hooks array and changes nothing" || bad "kimi refuses an inline hooks array and changes nothing (rc=$RC)"

# 2d4 an async handler runs in the background and cannot block, so doctor fails and install repairs it
fresh; run --tool qwen >/dev/null
python3 -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); [h.__setitem__("async", True) for g in d["hooks"]["PreToolUse"] for h in g["hooks"] if "guard.sh" in h["command"]]; json.dump(d, open(p,"w"))' "$(cfg qwen)"
run --tool qwen doctor >/dev/null; RC=$?
[ "$RC" -eq 1 ] && ok "qwen doctor fails on an async guard handler" || bad "qwen doctor fails on an async guard handler (rc=$RC)"
run --tool qwen >/dev/null
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if all(not h.get("async") for g in d["hooks"]["PreToolUse"] for h in g["hooks"] if "guard.sh" in h["command"]) else 1)' "$(cfg qwen)" \
  && ok "qwen install repairs an async guard handler" || bad "qwen install repairs an async guard handler"
# Cursor runs a handler only when its type is command and its matcher takes the submit command, and needs a positive whole number version
for broken in 'h.__setitem__("matcher", "^git status$")' 'h.__setitem__("type", "prompt")'; do
  fresh; run --tool cursor >/dev/null
  python3 -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); [exec(sys.argv[2], {"h": h}) for ev in d["hooks"].values() for h in ev if "guard" in json.dumps(h)]; json.dump(d, open(p,"w"))' "$(cfg cursor)" "$broken"
  run --tool cursor doctor >/dev/null; RC=$?
  [ "$RC" -eq 1 ] && ok "cursor doctor fails on a handler that never runs the guard. $broken" || bad "cursor doctor fails on a handler that never runs the guard. $broken (rc=$RC)"
  run --tool cursor >/dev/null; run --tool cursor doctor >/dev/null; RC=$?
  [ "$RC" -eq 0 ] && ok "cursor install repairs the handler. $broken" || bad "cursor install repairs the handler. $broken (rc=$RC)"
done
for v in 0 true; do
  fresh; run --tool cursor >/dev/null
  python3 -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); d["version"]=json.loads(sys.argv[2]); json.dump(d, open(p,"w"))' "$(cfg cursor)" "$v"
  run --tool cursor doctor >/dev/null; RC=$?
  [ "$RC" -eq 1 ] && ok "cursor doctor fails on version $v" || bad "cursor doctor fails on version $v (rc=$RC)"
  run --tool cursor >/dev/null
  python3 -c 'import json,sys; v=json.load(open(sys.argv[1])).get("version"); sys.exit(0 if type(v) is int and v >= 1 else 1)' "$(cfg cursor)" \
    && ok "cursor install repairs version $v" || bad "cursor install repairs version $v"
done
# Copilot needs version to be the number 1, true is not 1, and a version repair is written even when the handlers are fine
fresh; mkdir -p "$(dirname "$(cfg copilot)")"; printf '{"version":true}\n' > "$(cfg copilot)"
run --tool copilot >/dev/null
python3 -c 'import json,sys; v=json.load(open(sys.argv[1])).get("version"); sys.exit(0 if type(v) is int and v == 1 else 1)' "$(cfg copilot)" \
  && ok "copilot install repairs a version of true" || bad "copilot install repairs a version of true"
python3 -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); d.pop("version", None); json.dump(d, open(p,"w"))' "$(cfg copilot)"
run --tool copilot >/dev/null
python3 -c 'import json,sys; v=json.load(open(sys.argv[1])).get("version"); sys.exit(0 if type(v) is int and v == 1 else 1)' "$(cfg copilot)" \
  && ok "copilot reinstall writes back a missing version" || bad "copilot reinstall writes back a missing version"
# Gemini runs no hook when hooksConfig.enabled is false
fresh; run --tool gemini >/dev/null
python3 -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); d["hooksConfig"]={"enabled": False}; json.dump(d, open(p,"w"))' "$(cfg gemini)"
run --tool gemini doctor >/dev/null; RC=$?
[ "$RC" -eq 1 ] && ok "gemini doctor fails when hooksConfig.enabled is false" || bad "gemini doctor fails when hooksConfig.enabled is false (rc=$RC)"
# Copilot rejects a hooks file whose version is not 1, and runs a handler only for the tools its matcher names
fresh; mkdir -p "$(dirname "$(cfg copilot)")"; printf '{"version":0}\n' > "$(cfg copilot)"
run --tool copilot >/dev/null
python3 -c 'import json,sys; sys.exit(0 if json.load(open(sys.argv[1])).get("version") == 1 else 1)' "$(cfg copilot)" \
  && ok "copilot install repairs a bad version" || bad "copilot install repairs a bad version"
python3 -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); d["version"]=0; json.dump(d, open(p,"w"))' "$(cfg copilot)"
run --tool copilot doctor >/dev/null; RC=$?
[ "$RC" -eq 1 ] && ok "copilot doctor fails on a bad version" || bad "copilot doctor fails on a bad version (rc=$RC)"
fresh; run --tool copilot >/dev/null
python3 -c 'import json,sys
p=sys.argv[1]; d=json.load(open(p))
for ev in d.get("hooks", {}).values():
    for h in ev:
        if "guard" in json.dumps(h): h["matcher"] = "^view$"
json.dump(d, open(p,"w"))' "$(cfg copilot)"
run --tool copilot doctor >/dev/null; RC=$?
[ "$RC" -eq 1 ] && ok "copilot doctor fails on a handler whose matcher skips the shell" || bad "copilot doctor fails on a handler whose matcher skips the shell (rc=$RC)"
run --tool copilot >/dev/null
run --tool copilot doctor >/dev/null; RC=$?
[ "$RC" -eq 0 ] && ok "copilot install repairs a handler whose matcher skips the shell" || bad "copilot install repairs a handler whose matcher skips the shell (rc=$RC)"
# Kimi refuses a timeout over 600 and any key beyond event, matcher, command and timeout
for broken in 's/^timeout = 120$/timeout = 601/' 's/^timeout = 120$/timeout = 120\nasync = true/'; do
  fresh; run --tool kimi >/dev/null
  python3 -c 'import re,sys; p=sys.argv[1]; s=open(p).read(); a,b=sys.argv[2][2:-1].split("/"); open(p,"w").write(re.sub(a, b.replace(chr(92)+"n", chr(10)), s, flags=re.M))' "$(cfg kimi)" "$broken"
  run --tool kimi doctor >/dev/null; RC=$?
  [ "$RC" -eq 1 ] && ok "kimi doctor fails on a hook Kimi refuses. $broken" || bad "kimi doctor fails on a hook Kimi refuses. $broken (rc=$RC)"
  run --tool kimi >/dev/null
  python3 -c 'import sys,tomllib; d=tomllib.load(open(sys.argv[1],"rb")); hs=[h for h in d.get("hooks",[]) if "guard.sh" in h.get("command","")]; sys.exit(0 if hs and all(set(h) <= {"event","matcher","command","timeout"} and h["timeout"] == 120 for h in hs) else 1)' "$(cfg kimi)" \
    && ok "kimi install repairs the hook. $broken" || bad "kimi install repairs the hook. $broken"
done
# Qwen and Copilot run no hook at all when disableAllHooks is true, so doctor must say so
for t in qwen copilot; do
  fresh; run --tool $t >/dev/null
  python3 -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); d["disableAllHooks"]=True; json.dump(d, open(p,"w"))' "$(cfg $t)"
  run --tool $t doctor >/dev/null; RC=$?
  [ "$RC" -eq 1 ] && ok "$t doctor fails when disableAllHooks is true" || bad "$t doctor fails when disableAllHooks is true (rc=$RC)"
done
# Qwen needs the type on every handler, and reads a timeout of 1000 or more as milliseconds
for broken in 'h.pop("type", None)' 'h.__setitem__("timeout", 1000)'; do
  fresh; run --tool qwen >/dev/null
  python3 -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); [exec(sys.argv[2], {"h": h}) for g in d["hooks"]["PreToolUse"] for h in g["hooks"] if "guard.sh" in h["command"]]; json.dump(d, open(p,"w"))' "$(cfg qwen)" "$broken"
  run --tool qwen doctor >/dev/null; RC=$?
  [ "$RC" -eq 1 ] && ok "qwen doctor fails on a handler Qwen would not run in time. $broken" || bad "qwen doctor fails on a handler Qwen would not run in time. $broken (rc=$RC)"
  run --tool qwen >/dev/null
  python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); hs=[h for g in d["hooks"]["PreToolUse"] for h in g["hooks"] if "guard.sh" in h["command"]]; sys.exit(0 if hs and all(h.get("type") == "command" and 120 <= h.get("timeout", 0) < 1000 for h in hs) else 1)' "$(cfg qwen)" \
    && ok "qwen install repairs the handler. $broken" || bad "qwen install repairs the handler. $broken"
done
# 2d5 COPILOT_HOME moves Copilot's user hooks folder, so the hook goes where Copilot reads it
fresh; mkdir -p "$H/cop"
OUT="$(env -u QWEN_HOME -u KIMI_CODE_HOME -u CODEX_HOME -u XDG_CONFIG_HOME HOME="$H" COPILOT_HOME="$H/cop" bash "$INSTALL" --tool copilot 2>&1)"; RC=$?
[ "$RC" -eq 0 ] && [ -f "$H/cop/hooks/app-store-compliance.json" ] && [ ! -e "$H/.copilot" ] && ok "copilot follows COPILOT_HOME" || bad "copilot follows COPILOT_HOME (rc=$RC)"
# 2d6 a CRLF [hooks] table and a quoted hooks key are refused too, and the file is left as it was
for body in '[hooks]\r\nx = 1\r\n' '"hooks" = []\n'; do
  fresh; mkdir -p "$H/.kimi-code"; printf "$body" > "$H/.kimi-code/config.toml"; cp "$H/.kimi-code/config.toml" "$WORK/kimi-k.toml"
  run --tool kimi >/dev/null; RC=$?
  [ "$RC" -ne 0 ] && cmp -s "$H/.kimi-code/config.toml" "$WORK/kimi-k.toml" && ok "kimi refuses an existing hooks key and changes nothing ($body)" || bad "kimi refuses an existing hooks key and changes nothing ($body) (rc=$RC)"
done

# 2d7 an escaped hooks key is refused even where Python has no TOML parser
NOTOML="$WORK/notoml"; mkdir -p "$NOTOML"; printf 'raise ImportError("no tomllib here")\n' > "$NOTOML/tomllib.py"
fresh; mkdir -p "$H/.kimi-code"; printf '"ho\\u006fks" = []\n' > "$H/.kimi-code/config.toml"; cp "$H/.kimi-code/config.toml" "$WORK/kimi-esc.toml"
PYTHONPATH="$NOTOML" run --tool kimi >/dev/null; RC=$?
[ "$RC" -ne 0 ] && cmp -s "$H/.kimi-code/config.toml" "$WORK/kimi-esc.toml" && ok "kimi refuses an escaped hooks key without a TOML parser" || bad "kimi refuses an escaped hooks key without a TOML parser (rc=$RC)"
# 2d8 repairing our marked block never turns a valid file invalid
fresh; mkdir -p "$H/.kimi-code"
printf 'hooks = []\n# >>> app-store-compliance guard >>>\n# old disabled hook\n# <<< app-store-compliance guard <<<\n' > "$H/.kimi-code/config.toml"
cp "$H/.kimi-code/config.toml" "$WORK/kimi-rep.toml"
run --tool kimi >/dev/null; RC=$?
[ "$RC" -ne 0 ] && cmp -s "$H/.kimi-code/config.toml" "$WORK/kimi-rep.toml" && ok "kimi refuses a block repair that would break the file" || bad "kimi refuses a block repair that would break the file (rc=$RC)"

# 2d9 a Windows path in the Gemini audit command still gives valid TOML
python3 -c '
import sys, tomllib
sys.path.insert(0, "scripts")
import install_harness as h
b = chr(92)
h.shown = lambda p: "~" + b + ".gemini" + b + "hooks" + b + "app-store-compliance-guard.sh"
t = tomllib.loads(h.command_text("gemini", "x"))
sys.exit(0 if (b + ".gemini" + b) in t["prompt"] else 1)
' 2>/dev/null && ok "gemini audit command stays valid TOML with a Windows path" || bad "gemini audit command stays valid TOML with a Windows path"

# 2e Copilot in the app repository (cloud agent, JetBrains, VS Code workspace)
fresh; APPR="$WORK/apprepo$RANDOM"; mkdir -p "$APPR"
OUT="$(run --tool copilot-repo)"; RC=$?
[ "$RC" -eq 2 ] && echo "$OUT" | grep -q "Pass --repo" && ok "copilot-repo without --repo exits 2 and says what to pass" || bad "copilot-repo without --repo exits 2 (rc=$RC)"
OUT="$(run --tool copilot-repo --repo "$APPR")"; RC=$?
[ "$RC" -eq 0 ] && echo "$OUT" | grep -q "^Install verified\." && [ -x "$APPR/.github/hooks/app-store-compliance-guard.sh" ] \
  && python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if d["hooks"]["preToolUse"][0]["bash"]=="bash ./.github/hooks/app-store-compliance-guard.sh" else 1)' "$APPR/.github/hooks/app-store-compliance.json" \
  && [ ! -e "$H/.agents" ] && ok "copilot-repo writes a relative hook into the repository and nothing in HOME" || { bad "copilot-repo writes a relative hook into the repository (rc=$RC)"; echo "$OUT" | tail -8; }
run --tool copilot-repo --repo "$APPR" uninstall >/dev/null
[ ! -e "$APPR/.github/hooks/app-store-compliance.json" ] && [ ! -e "$APPR/.github/hooks/app-store-compliance-guard.sh" ] && ok "copilot-repo uninstall removes both files" || bad "copilot-repo uninstall removes both files"

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

# 4b removing the most recently installed tool keeps the skill for the earlier one, in both orders
for pair in "codex gemini" "gemini codex"; do
  set -- $pair; fresh; run --tool "$1" >/dev/null; run --tool "$2" >/dev/null; run --tool "$2" uninstall >/dev/null
  run --tool "$1" doctor >/dev/null; RC=$?
  [ -f "$H/.agents/skills/app-store-compliance/SKILL.md" ] && [ "$RC" -eq 0 ] && grep -qx "$1" "$H/.agents/skills/app-store-compliance/.installed-by" \
    && ok "uninstalling $2 after $1 keeps the shared skill and $1 doctor passes" || bad "uninstalling $2 after $1 keeps the shared skill and $1 doctor passes (rc=$RC)"
done

# 4c an entry that names the guard but would never dispatch is caught by doctor and repaired by install
fresh; run --tool codex >/dev/null
python3 -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); d["hooks"]["PreToolUse"][0]["matcher"]="Read"; json.dump(d,open(p,"w"))' "$(cfg codex)"
run --tool codex doctor >/dev/null; RC=$?
[ "$RC" -eq 1 ] && ok "codex doctor fails when the guard sits on the Read matcher" || bad "codex doctor fails when the guard sits on the Read matcher (rc=$RC)"
run --tool codex >/dev/null; run --tool codex doctor >/dev/null; RC=$?
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); g=[g for g in d["hooks"]["PreToolUse"] if any("guard.sh" in h["command"] for h in g["hooks"])]; sys.exit(0 if [x["matcher"] for x in g]==["Bash"] else 1)' "$(cfg codex)" && [ "$RC" -eq 0 ] \
  && ok "codex install moves the guard back onto Bash and doctor then passes" || bad "codex install moves the guard back onto Bash and doctor then passes (rc=$RC)"
fresh; run --tool gemini >/dev/null
python3 -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); h=d["hooks"]["BeforeTool"][0]["hooks"][0]; h["type"]="prompt"; h.pop("timeout"); json.dump(d,open(p,"w"))' "$(cfg gemini)"
run --tool gemini doctor >/dev/null; RC=$?
[ "$RC" -eq 1 ] && ok "gemini doctor fails on a wrong handler type and a missing timeout" || bad "gemini doctor fails on a wrong handler type and a missing timeout (rc=$RC)"
run --tool gemini >/dev/null; run --tool gemini doctor >/dev/null; RC=$?
[ "$RC" -eq 0 ] && [ "$(count gemini)" = "1" ] && ok "gemini install repairs the handler once" || bad "gemini install repairs the handler once (rc=$RC entries=$(count gemini))"
fresh; run --tool kimi >/dev/null
python3 -c 'import sys; p=sys.argv[1]; t=open(p).read(); i=t.index("command = "); j=t.index("\n",i); open(p,"w").write(t[:i]+"command = \"bash /no/such/app-store-compliance-guard.sh\""+t[j:])' "$(cfg kimi)"
run --tool kimi doctor >/dev/null; RC=$?
[ "$RC" -eq 1 ] && ok "kimi doctor tests the command actually registered in config.toml" || bad "kimi doctor tests the command actually registered in config.toml (rc=$RC)"
run --tool kimi >/dev/null; run --tool kimi doctor >/dev/null; RC=$?
[ "$RC" -eq 0 ] && [ "$(count kimi)" = "1" ] && ok "kimi install rewrites a broken block once" || bad "kimi install rewrites a broken block once (rc=$RC entries=$(count kimi))"

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

# 6b release-audit.py run from the shared skill finds the guard installed under the tool's own folder
fresh; run --tool codex >/dev/null
OUT="$(env -u APP_STORE_GUARD_PATH HOME="$H" python3 "$H/.agents/skills/app-store-compliance/scripts/release-audit.py" "$APP" 2>&1)"
echo "$OUT" | grep -qF "Guard. $H/.codex/hooks/app-store-compliance-guard.sh" && ok "release-audit in the shared skill finds the codex guard" || { bad "release-audit in the shared skill finds the codex guard"; echo "$OUT" | grep -i guard | head -3; }
run --tool gemini >/dev/null; run --tool codex uninstall >/dev/null
OUT="$(env -u APP_STORE_GUARD_PATH HOME="$H" python3 "$H/.agents/skills/app-store-compliance/scripts/release-audit.py" "$APP" 2>&1)"
echo "$OUT" | grep -qF "Guard. $H/.gemini/hooks/app-store-compliance-guard.sh" && ok "after codex is removed release-audit uses the gemini guard" || bad "after codex is removed release-audit uses the gemini guard"
rm -rf "$APP"

# 7 the audit command points at the installed paths, and the Gemini command is valid TOML
fresh; run --tool gemini >/dev/null; run --tool opencode >/dev/null
python3 -c 'import sys,tomllib; d=tomllib.load(open(sys.argv[1],"rb")); sys.exit(0 if d["description"] and "{{args}}" in d["prompt"] else 1)' "$H/.gemini/commands/app-store-audit.toml" && ok "the gemini command is valid TOML with {{args}}" || bad "the gemini command is valid TOML with {{args}}"
! grep -q "[~]/.claude" "$H/.gemini/commands/app-store-audit.toml" "$H/.config/opencode/commands/app-store-audit.md" && ok "the commands name no Claude Code path" || bad "the commands name no Claude Code path"

# 8 --tool all installs into every tool it finds, and only those
fresh; mkdir -p "$H/.codex" "$H/.cursor"
OUT="$(run --tool all)"; RC=$?
[ "$RC" -eq 0 ] && echo "$OUT" | grep -q "^Found. codex cursor$" && [ "$(count codex)" = "1" ] && [ "$(count cursor)" = "1" ] && [ ! -e "$H/.gemini" ] && [ ! -e "$H/.claude" ] \
  && ok "--tool all installs into the found tools only" || { bad "--tool all installs into the found tools only (rc=$RC)"; echo "$OUT" | head -5; }
fresh; OUT="$(run --tool all)"; RC=$?
[ "$RC" -eq 1 ] && echo "$OUT" | grep -q "No supported AI coding tool" && ok "--tool all with no tool says so" || bad "--tool all with no tool says so (rc=$RC)"

# 8b Qwen reads $QWEN_HOME/settings.json when QWEN_HOME is set, so install, doctor, uninstall and --tool all follow it
fresh; Q="$WORK/qhome$RANDOM"; mkdir -p "$Q"
qrun() { env -u CODEX_HOME -u XDG_CONFIG_HOME -u CLAUDE_CONFIG_DIR -u CLAUDE_PROJECT_DIR QWEN_HOME="$Q" HOME="$H" bash "$INSTALL" "$@" 2>&1; }
OUT="$(qrun --tool qwen)"; RC=$?
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if any("guard.sh" in h["command"] for g in d["hooks"]["PreToolUse"] for h in g["hooks"]) else 1)' "$Q/settings.json" 2>/dev/null && [ "$RC" -eq 0 ] && [ ! -e "$H/.qwen/settings.json" ] \
  && ok "qwen installs into \$QWEN_HOME/settings.json" || bad "qwen installs into \$QWEN_HOME/settings.json (rc=$RC)"
qrun --tool qwen doctor >/dev/null; RC=$?
[ "$RC" -eq 0 ] && ok "qwen doctor checks \$QWEN_HOME" || bad "qwen doctor checks \$QWEN_HOME (rc=$RC)"
qrun --tool qwen uninstall >/dev/null
! grep -q "app-store-compliance-guard.sh" "$Q/settings.json" 2>/dev/null && ok "qwen uninstall edits \$QWEN_HOME/settings.json" || bad "qwen uninstall edits \$QWEN_HOME/settings.json"
fresh; Q="$WORK/qhome$RANDOM"; mkdir -p "$Q"
OUT="$(qrun --tool all --dry-run)"; RC=$?
echo "$OUT" | grep -q "^Found. qwen$" && ok "--tool all finds qwen through \$QWEN_HOME" || bad "--tool all finds qwen through \$QWEN_HOME (rc=$RC)"

# 8c two installs of one tool, in two config folders, each own the shared skill
fresh; CA="$WORK/codexa$RANDOM"; CB="$WORK/codexb$RANDOM"; mkdir -p "$CA" "$CB"
crun() { local c="$1"; shift; env -u QWEN_HOME -u XDG_CONFIG_HOME -u CLAUDE_CONFIG_DIR -u CLAUDE_PROJECT_DIR CODEX_HOME="$c" HOME="$H" bash "$INSTALL" "$@" 2>&1; }
crun "$CA" --tool codex >/dev/null; crun "$CB" --tool codex >/dev/null; crun "$CB" --tool codex uninstall >/dev/null
[ -f "$H/.agents/skills/app-store-compliance/SKILL.md" ] && grep -qF "$CA/hooks/app-store-compliance-guard.sh" "$H/.agents/skills/app-store-compliance/.guards" \
  && ok "uninstalling one codex folder keeps the shared skill for the other" || bad "uninstalling one codex folder keeps the shared skill for the other"
crun "$CA" --tool codex doctor >/dev/null; RC=$?
[ "$RC" -eq 0 ] && ok "the remaining codex folder still passes doctor" || bad "the remaining codex folder still passes doctor (rc=$RC)"
crun "$CA" --tool codex uninstall >/dev/null
[ ! -e "$H/.agents/skills/app-store-compliance" ] && ok "uninstalling the last codex folder removes the shared skill" || bad "uninstalling the last codex folder removes the shared skill"
# 8d --tool all expands a QWEN_HOME written with a Windows tilde, as the installer does
fresh; mkdir -p "$H/qwen-config"
OUT="$(env -u CODEX_HOME -u XDG_CONFIG_HOME -u CLAUDE_CONFIG_DIR -u CLAUDE_PROJECT_DIR QWEN_HOME='~\qwen-config' HOME="$H" bash "$INSTALL" --tool all --dry-run 2>&1)"
echo "$OUT" | grep -q "^Found. qwen$" && ok "--tool all finds a QWEN_HOME written as ~\folder" || bad "--tool all finds a QWEN_HOME written as ~\folder"

# 8e Kimi keeps CRLF line endings byte for byte through install and uninstall
fresh; mkdir -p "$H/.kimi-code"; printf 'default_model = "k2"\r\n\r\n' > "$H/.kimi-code/config.toml"; cp "$H/.kimi-code/config.toml" "$WORK/kimi-crlf.toml"
run --tool kimi >/dev/null; run --tool kimi uninstall >/dev/null
cmp -s "$H/.kimi-code/config.toml" "$WORK/kimi-crlf.toml" && ok "kimi uninstall keeps CRLF line endings" || bad "kimi uninstall keeps CRLF line endings"
# 8f the OpenCode plugin never lets a submit through when the guard cannot run
fresh; mkdir -p "$H/.config/opencode"; run --tool opencode >/dev/null
rm -f "$(gdir opencode)/app-store-compliance-guard.sh"
if command -v node >/dev/null 2>&1; then
  RES="$(node --input-type=module -e '
const m = await import(process.argv[1]);
const p = await m.AppStoreCompliance({ directory: process.argv[2] });
const run = async (c) => { try { await p["tool.execute.before"]({ tool: "bash" }, { args: { command: c } }); return "allowed" } catch (e) { return "thrown" } };
console.log((await run("fast" + "lane deliver")) + " " + (await run("f\\ast" + "lane deliver")) + " " + (await run("ea" + "s\tsubmit")) + " " + (await run("ls -la")));
' "$(cfg opencode)" "$H" 2>/dev/null)"
  [ "$RES" = "thrown thrown thrown allowed" ] && ok "opencode refuses a submit when the guard cannot run and allows other commands" || bad "opencode refuses a submit when the guard cannot run and allows other commands (got $RES)"
else ok "opencode guard-failure check skipped, node not installed"; fi
# 8j OpenCode loads both plugin folders, and a call is still checked once
fresh; mkdir -p "$H/.config/opencode"; run --tool opencode >/dev/null
printf '#!/usr/bin/env bash\necho x >> "%s/count"\nexit 0\n' "$H" > "$(gdir opencode)/app-store-compliance-guard.sh"
if command -v node >/dev/null 2>&1; then
  node --input-type=module -e '
const a = await (await import(process.argv[1])).AppStoreCompliance({ directory: process.argv[3] });
const b = await (await import(process.argv[2])).AppStoreCompliance({ directory: process.argv[3] });
const out = { args: { command: "ls" } };
await a["tool.execute.before"]({ tool: "bash" }, out); await b["tool.execute.before"]({ tool: "bash" }, out);
' "$(cfg opencode)" "$H/.config/opencode/plugin/app-store-compliance.js" "$H" 2>/dev/null
  [ "$(wc -l < "$H/count" | tr -d ' ')" = "1" ] && ok "opencode checks a call once with both plugin folders loaded" || bad "opencode checks a call once with both plugin folders loaded ($(wc -l < "$H/count" 2>/dev/null))"
else ok "opencode double-load check skipped, node not installed"; fi
# 8h a CRLF Kimi config reinstalls without a rewrite
fresh; mkdir -p "$H/.kimi-code"; printf 'default_model = "k2"\r\n' > "$H/.kimi-code/config.toml"
run --tool kimi >/dev/null; N1="$(find "$H/.kimi-code" -maxdepth 1 -name '*bak*' | wc -l | tr -d ' ')"; OUT="$(run --tool kimi)"; N2="$(find "$H/.kimi-code" -maxdepth 1 -name '*bak*' | wc -l | tr -d ' ')"
[ "$N1" = "$N2" ] && echo "$OUT" | grep -q 'already registered' && ok "kimi a second run on a CRLF config changes nothing" || bad "kimi a second run on a CRLF config changes nothing ($N1 $N2)"
# 8i without node the OpenCode install never says verified
fresh; mkdir -p "$H/.config/opencode"
NONODE="$WORK/nonode$RANDOM"; mkdir -p "$NONODE"; for b in bash sh python3 grep sed awk cat cp mv rm mkdir chmod dirname basename tr head tail find date ls env printf mktemp uname cmp wc sort; do p="$(command -v "$b" 2>/dev/null)"; [ -n "$p" ] && ln -s "$p" "$NONODE/$b"; done
OUT="$(env -u QWEN_HOME -u KIMI_CODE_HOME -u COPILOT_HOME -u CODEX_HOME -u XDG_CONFIG_HOME -u CLAUDE_CONFIG_DIR -u CLAUDE_PROJECT_DIR PATH="$NONODE" HOME="$H" bash "$INSTALL" --tool opencode 2>&1)"
echo "$OUT" | grep -q 'not fully verified' && ! echo "$OUT" | grep -q '^Install verified' && ok "opencode without node says not fully verified" || bad "opencode without node says not fully verified"
# 8g a non-Claude doctor says when the checkout is newer than the install
fresh; mkdir -p "$H/.codex"; run --tool codex >/dev/null; printf '1.0.0' > "$H/.agents/skills/app-store-compliance/VERSION"
OUT="$(run --tool codex doctor)"
echo "$OUT" | grep -q "this checkout is version" && ok "codex doctor says the checkout is newer" || bad "codex doctor says the checkout is newer"

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
