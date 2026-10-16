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

# 12 an entry that names the guard but cannot fire for Bash does not count as registered
bash_entries() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(sum(1 for e in d["hooks"]["PreToolUse"] if e.get("matcher")=="Bash" for h in e["hooks"] if h.get("command","").startswith("bash ") and "#" not in h["command"] and h["command"].rstrip().rstrip(chr(39)).endswith("app-store-compliance-guard.sh")))' "$C/settings.json"; }
fresh
printf '{"hooks":{"PreToolUse":[{"matcher":"Read","hooks":[{"type":"command","command":"bash ~/.claude/hooks/app-store-compliance-guard.sh"}]},{"matcher":"Bash","hooks":[{"type":"command","command":"true # app-store-compliance-guard.sh"}]}]}}' > "$C/settings.json"
run >/dev/null; RC=$?
[ "$RC" -eq 0 ] && [ "$(bash_entries)" = "1" ] && ok "a guard entry on the wrong matcher or behind a comment is not trusted, a working one is added" || bad "a guard entry on the wrong matcher or behind a comment is not trusted (rc=$RC)"

# 13 a config folder with a space still yields a hook command the shell can run, and it blocks
C="$WORK/claude config $RANDOM"; mkdir -p "$C"
OUT="$(run)"; RC=$?
HOOKCMD="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print([h["command"] for e in d["hooks"]["PreToolUse"] for h in e["hooks"]][0])' "$C/settings.json")"
FX="$(mktemp -d)"; mkdir -p "$FX/App"; printf '<plist><dict></dict></plist>' > "$FX/App/Info.plist"
printf 'class A { func signIn(){} func createAccount(){} }\nlet u="https://staging.example.com"\n' > "$FX/App/X.swift"
( cd "$FX" && printf '{"tool_name":"Bash","tool_input":{"command":"fastlane deliver"}}' | env -u CLAUDE_PROJECT_DIR bash -c "$HOOKCMD" >/dev/null 2>&1 ); HRC=$?
[ "$RC" -eq 0 ] && [ "$HRC" -eq 2 ] && ok "a config path with a space gives a runnable hook command that blocks" || bad "a config path with a space gives a runnable hook command that blocks (install rc=$RC hook rc=$HRC)"
rm -rf "$FX"

# 14 doctor runs the registered command itself, so an entry that cannot fire fails the check
fresh; run >/dev/null
python3 -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); d["hooks"]["PreToolUse"][0]["hooks"][0]["command"]="bash /no/such/app-store-compliance-guard.sh"; json.dump(d,open(p,"w"))' "$C/settings.json"
run doctor >/dev/null; RC=$?
[ "$RC" -eq 1 ] && ok "doctor fails when the registered command cannot run" || bad "doctor fails when the registered command cannot run (rc=$RC)"
for patch in 'h["type"]="prompt"' 'h["timeout"]=1'; do
  fresh; run >/dev/null
  python3 -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); h=d["hooks"]["PreToolUse"][0]["hooks"][0]; exec(sys.argv[2]); json.dump(d,open(p,"w"))' "$C/settings.json" "$patch"
  run doctor >/dev/null; RC=$?
  [ "$RC" -eq 1 ] && ok "doctor fails for a hook Claude would not run as intended. $patch" || bad "doctor fails for a hook Claude would not run as intended. $patch (rc=$RC)"
done

# 15 a settings.json with a repeated key is ambiguous and is never rewritten
fresh
printf '{"hooks":{"Stop":[{"hooks":[{"type":"command","command":"x"}]}]},"hooks":{"PreToolUse":[]}}' > "$C/settings.json"; BEFORE="$(cat "$C/settings.json")"
OUT="$(run)"; RC=$?
[ "$BEFORE" = "$(cat "$C/settings.json")" ] && [ "$RC" -eq 1 ] && echo "$OUT" | grep -q '"PreToolUse"' && ok "a repeated key leaves settings.json untouched" || bad "a repeated key leaves settings.json untouched (rc=$RC)"

# 16 a read-only settings.json is respected
fresh
printf '{"model":"opus"}' > "$C/settings.json"; chmod 0444 "$C/settings.json"
run >/dev/null; RC=$?
[ "$(cat "$C/settings.json")" = '{"model":"opus"}' ] && [ "$RC" -eq 1 ] && ok "a read-only settings.json is left untouched" || bad "a read-only settings.json is left untouched (rc=$RC)"
chmod 0644 "$C/settings.json"

# 17 with jq and no python3 the hook is still merged, other keys kept, and a second run adds nothing
if command -v jq >/dev/null 2>&1; then
  fresh
  SHIM="$(mktemp -d)"
  for b in bash cp rm mkdir chmod cat grep sed awk find xargs tr head tail mktemp printf wc sort uniq cut dirname basename date cmp mv ls env plutil xmllint file od comm tee sleep expr touch jq; do p="$(command -v "$b" 2>/dev/null)"; [ -n "$p" ] && ln -s "$p" "$SHIM/$b"; done
  printf '{"model":"opus","hooks":{"Stop":[]}}' > "$C/settings.json"
  OUT="$(PATH="$SHIM" CLAUDE_CONFIG_DIR="$C" bash "$INSTALL" 2>&1)"; RC=$?
  PATH="$SHIM" CLAUDE_CONFIG_DIR="$C" bash "$INSTALL" >/dev/null 2>&1
  [ "$RC" -eq 0 ] && echo "$OUT" | grep -q "^Install verified\." && [ "$(hooks)" = "1" ] && grep -q '"opus"' "$C/settings.json" && ok "with jq only the hook is merged once and verified" || bad "with jq only the hook is merged once and verified (rc=$RC entries=$(hooks))"
  # jq keeps only the last of two repeated keys, so a repeated key must stop the jq path too
  for body in '{"permissions":{"deny":["Bash(*)"]},"permissions":{"allow":["Bash(*)"]}}' '{"hooks":{"PreToolUse":[]},"a":{"b":1,"b":2}}'; do
    fresh; printf '%s' "$body" > "$C/settings.json"
    OUT="$(PATH="$SHIM" CLAUDE_CONFIG_DIR="$C" bash "$INSTALL" 2>&1)"; RC=$?
    [ "$RC" -eq 1 ] && [ "$(cat "$C/settings.json")" = "$body" ] && echo "$OUT" | grep -q '"PreToolUse"' && ok "with jq only a repeated key leaves settings.json untouched" || bad "with jq only a repeated key leaves settings.json untouched (rc=$RC)"
  done
  rm -rf "$SHIM"
fi

# 18 a hook for a guard of the same file name in another folder is somebody else's. It is not trusted and not removed.
fresh
python3 -c 'import json,sys; json.dump({"hooks":{"PreToolUse":[{"matcher":"Bash","hooks":[{"type":"command","command":"bash /opt/other/app-store-compliance-guard.sh"}]}]}}, sys.stdout)' > "$C/settings.json"
run >/dev/null; RC=$?
[ "$RC" -eq 0 ] && [ "$(hooks "$C/settings.json")" = "2" ] && ok "a same-named guard in another folder does not count as installed" || bad "a same-named guard in another folder does not count as installed (rc=$RC entries=$(hooks "$C/settings.json"))"
run uninstall >/dev/null
[ "$(hooks "$C/settings.json")" = "1" ] && grep -q "/opt/other/app-store-compliance-guard.sh" "$C/settings.json" && ok "uninstall leaves the other folder's hook in place" || bad "uninstall leaves the other folder's hook in place (entries=$(hooks "$C/settings.json"))"

# 19 no HOME and no CLAUDE_CONFIG_DIR is a clear message, never a crash. HOME alone missing still works.
OUT="$(env -u HOME -u CLAUDE_CONFIG_DIR bash "$INSTALL" --dry-run 2>&1)"; RC=$?
[ "$RC" -ne 0 ] && echo "$OUT" | grep -q 'HOME is not set' && ! echo "$OUT" | grep -q 'unbound variable' && ok "an unset HOME is reported, not a crash" || bad "an unset HOME is reported, not a crash (rc=$RC)"
fresh
OUT="$(env -u HOME CLAUDE_CONFIG_DIR="$C" bash "$INSTALL" --dry-run 2>&1)"; RC=$?
[ "$RC" -eq 0 ] && ! echo "$OUT" | grep -q 'unbound variable' && ok "a custom folder works with HOME unset" || bad "a custom folder works with HOME unset (rc=$RC)"
# 20 the default folder written with a braced HOME is still this folder's hook, so no second entry is added.
H="$WORK/home$RANDOM"; mkdir -p "$H/.claude"
C="$H/.claude"
python3 -c 'import json,sys; json.dump({"hooks":{"PreToolUse":[{"matcher":"Bash","hooks":[{"type":"command","command":"bash \"${HOME}/.claude/hooks/app-store-compliance-guard.sh\"","timeout":120}]}]}}, sys.stdout)' > "$H/.claude/settings.json"
env -u CLAUDE_CONFIG_DIR HOME="$H" bash "$INSTALL" >/dev/null 2>&1; RC=$?
[ "$RC" -eq 0 ] && [ "$(hooks)" = "1" ] && ok "a hook written with a braced HOME counts as installed" || bad "a hook written with a braced HOME counts as installed (rc=$RC entries=$(hooks))"

# 21 a hook that runs some other script and only passes this guard's path as an argument is not ours.
fresh
python3 - "$C" > "$C/settings.json" <<'PYT'
import json, sys
cmd = "bash %s/hooks/audit-wrapper.sh --guard %s/hooks/app-store-compliance-guard.sh" % (sys.argv[1], sys.argv[1])
json.dump({"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": cmd}]}]}}, sys.stdout)
PYT
run >/dev/null; RC=$?
[ "$RC" -eq 0 ] && [ "$(hooks)" = "2" ] && ok "a wrapper that only names the guard as an argument does not count as installed" || bad "a wrapper that only names the guard as an argument does not count as installed (rc=$RC entries=$(hooks))"
run uninstall >/dev/null
[ "$(hooks)" = "1" ] && grep -q "audit-wrapper.sh" "$C/settings.json" && ok "uninstall leaves the wrapper hook in place" || bad "uninstall leaves the wrapper hook in place (entries=$(hooks))"

# 22 only the exact command counts. A longer file name, or the path run without bash, is somebody else's hook.
for OTHER in "bash $WORK/x/hooks/app-store-compliance-guard.sh.backdoor" "$WORK/x/hooks/app-store-compliance-guard.sh"; do
  C="$WORK/x"; rm -rf "$C"; mkdir -p "$C"
  python3 -c 'import json,sys; json.dump({"hooks":{"PreToolUse":[{"matcher":"Bash","hooks":[{"type":"command","command":sys.argv[1]}]}]}}, sys.stdout)' "$OTHER" > "$C/settings.json"
  run >/dev/null; RC=$?
  [ "$RC" -eq 0 ] && [ "$(hooks)" = "2" ] && ok "a look-alike command is not taken for this guard (${OTHER##*/})" || bad "a look-alike command is not taken for this guard (${OTHER##*/}) (rc=$RC entries=$(hooks))"
  run uninstall >/dev/null
  [ "$(hooks)" = "1" ] && grep -qF "$OTHER" "$C/settings.json" && ok "uninstall leaves the look-alike in place (${OTHER##*/})" || bad "uninstall leaves the look-alike in place (${OTHER##*/}) (entries=$(hooks))"
done

# 23 a config folder with an apostrophe in its name installs once, verifies, and uninstalls.
C="$WORK/O'Reilly cfg"; mkdir -p "$C"
OUT="$(run)"; RC=$?
run >/dev/null
[ "$RC" -eq 0 ] && [ "$(hooks)" = "1" ] && ok "a folder with an apostrophe installs once and verifies" || bad "a folder with an apostrophe installs once and verifies (rc=$RC entries=$(hooks))"
run doctor >/dev/null; RC=$?
[ "$RC" -eq 0 ] && ok "doctor passes for a folder with an apostrophe" || bad "doctor passes for a folder with an apostrophe (rc=$RC)"
run uninstall >/dev/null
[ "$(hooks)" = "0" ] && ok "uninstall removes the hook for a folder with an apostrophe" || bad "uninstall removes the hook for a folder with an apostrophe (entries=$(hooks))"

# 24 the installed version is recorded and reported, so a user can tell what they run
fresh
run >/dev/null
V="$(cat VERSION 2>/dev/null)"
[ -n "$V" ] && [ "$(cat "$C/skills/app-store-compliance/VERSION" 2>/dev/null)" = "$V" ] && ok "install records the playbook version" || bad "install records the playbook version (repo=$V)"
OUT="$(run doctor)"; echo "$OUT" | grep -q "^  ok    version $V" && ok "doctor prints the installed version" || bad "doctor prints the installed version"
[ "$(run --version)" = "app-store-compliance $V" ] && ok "--version prints the checkout version" || bad "--version prints the checkout version"

# 25 on Windows (Git Bash, MSYS, Cygwin) the hook also covers PowerShell, and doctor proves a PowerShell call is blocked
fresh
OUT="$(ASC_UNAME=MINGW64_NT-10.0 run)"; RC=$?
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); m=[e["matcher"] for e in d["hooks"]["PreToolUse"]]; sys.exit(0 if m==["Bash|PowerShell"] else 1)' "$C/settings.json" && [ "$RC" -eq 0 ] && ok "Git Bash registers Bash|PowerShell" || bad "Git Bash registers Bash|PowerShell (rc=$RC)"
echo "$OUT" | grep -q "blocks a submit command run through PowerShell" && ok "doctor proves the PowerShell path on Windows" || bad "doctor proves the PowerShell path on Windows"
fresh; run >/dev/null
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); m=[e["matcher"] for e in d["hooks"]["PreToolUse"]]; sys.exit(0 if m==["Bash"] else 1)' "$C/settings.json" && ok "macOS and Linux keep the Bash matcher" || bad "macOS and Linux keep the Bash matcher"

# 26 a Bash-only entry written by an older install on Windows is upgraded to Bash|PowerShell, and doctor checks the matcher
fresh; run >/dev/null
ASC_UNAME=MINGW64_NT-10.0 run doctor >/dev/null; RC=$?
[ "$RC" -eq 1 ] && ok "Windows doctor fails while the matcher covers only Bash" || bad "Windows doctor fails while the matcher covers only Bash (rc=$RC)"
OUT="$(ASC_UNAME=MINGW64_NT-10.0 run)"; RC=$?
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); m=[e["matcher"] for e in d["hooks"]["PreToolUse"]]; sys.exit(0 if m==["Bash|PowerShell"] else 1)' "$C/settings.json" && [ "$(hooks)" = "1" ] && [ "$RC" -eq 0 ] \
  && ok "a Windows reinstall upgrades the owned Bash matcher once" || bad "a Windows reinstall upgrades the owned Bash matcher once (rc=$RC entries=$(hooks))"
ASC_UNAME=MINGW64_NT-10.0 run doctor >/dev/null; RC=$?
[ "$RC" -eq 0 ] && ok "Windows doctor passes after the upgrade" || bad "Windows doctor passes after the upgrade (rc=$RC)"
if command -v jq >/dev/null 2>&1; then
  fresh; run >/dev/null
  SHIM="$(mktemp -d)"
  for b in bash cp rm mkdir chmod cat grep sed awk find xargs tr head tail mktemp printf wc sort uniq cut dirname basename date cmp mv ls env plutil xmllint file od comm tee sleep expr touch jq; do p="$(command -v "$b" 2>/dev/null)"; [ -n "$p" ] && ln -s "$p" "$SHIM/$b"; done
  OUT="$(ASC_UNAME=MINGW64_NT-10.0 PATH="$SHIM" CLAUDE_CONFIG_DIR="$C" bash "$INSTALL" 2>&1)"; RC=$?
  python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); m=[e["matcher"] for e in d["hooks"]["PreToolUse"]]; sys.exit(0 if m==["Bash|PowerShell"] else 1)' "$C/settings.json" && [ "$(hooks)" = "1" ] && [ "$RC" -eq 0 ] \
    && ok "with jq only a Windows reinstall upgrades the matcher once" || bad "with jq only a Windows reinstall upgrades the matcher once (rc=$RC entries=$(hooks))"
  # an old Bash-only entry is still removed by a jq-only Windows uninstall
  fresh; run >/dev/null
  ASC_UNAME=MINGW64_NT-10.0 PATH="$SHIM" CLAUDE_CONFIG_DIR="$C" bash "$INSTALL" uninstall >/dev/null 2>&1; RC=$?
  [ "$(hooks)" = "0" ] && [ "$RC" -eq 0 ] && ok "with jq only a Windows uninstall removes an old Bash-only entry" || bad "with jq only a Windows uninstall removes an old Bash-only entry (rc=$RC entries=$(hooks))"
  rm -rf "$SHIM"
fi

# an async guard runs in the background and cannot block, so doctor fails and install repairs it, with python3 and with jq only
mkasync() { python3 -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); [h.__setitem__("async", True) for e in d["hooks"]["PreToolUse"] for h in e["hooks"] if "guard.sh" in h["command"]]; json.dump(d, open(p,"w"))' "$C/settings.json"; }
noasync() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if all(not h.get("async") for e in d["hooks"]["PreToolUse"] for h in e["hooks"] if "guard.sh" in h["command"]) else 1)' "$C/settings.json"; }
fresh; run >/dev/null; mkasync
run doctor >/dev/null; RC=$?
[ "$RC" -eq 1 ] && ok "doctor fails on an async guard hook" || bad "doctor fails on an async guard hook (rc=$RC)"
run >/dev/null; noasync && [ "$(hooks)" = "1" ] && ok "install repairs an async guard hook" || bad "install repairs an async guard hook"
if command -v jq >/dev/null 2>&1; then
  fresh; run >/dev/null; mkasync
  JQS="$(mktemp -d)"
  for b in bash cp rm mkdir chmod cat grep sed awk find xargs tr head tail mktemp printf wc sort uniq cut dirname basename date cmp mv ls env jq plutil xmllint; do p="$(command -v "$b" 2>/dev/null)"; [ -n "$p" ] && ln -s "$p" "$JQS/$b"; done
  PATH="$JQS" CLAUDE_CONFIG_DIR="$C" bash "$INSTALL" doctor >/dev/null 2>&1; RC=$?
  [ "$RC" -eq 1 ] && ok "jq-only doctor fails on an async guard hook" || bad "jq-only doctor fails on an async guard hook (rc=$RC)"
  PATH="$JQS" CLAUDE_CONFIG_DIR="$C" bash "$INSTALL" >/dev/null 2>&1
  noasync && [ "$(hooks)" = "1" ] && ok "jq-only install repairs an async guard hook" || bad "jq-only install repairs an async guard hook"
  rm -rf "$JQS"
fi

# a jq-only install repairs an owned hook whose timeout is too short or whose type is not a command
if command -v jq >/dev/null 2>&1; then
  for fix in 'h["timeout"]=1' 'h["type"]="prompt"'; do
    fresh; run >/dev/null
    python3 -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p))
for e in d["hooks"]["PreToolUse"]:
    for h in e["hooks"]:
        if "guard.sh" in h["command"]: '"$fix"'
json.dump(d, open(p,"w"))' "$C/settings.json"
    JQS="$(mktemp -d)"
    for b in bash cp rm mkdir chmod cat grep sed awk find xargs tr head tail mktemp printf wc sort uniq cut dirname basename date cmp mv ls env jq plutil xmllint; do p="$(command -v "$b" 2>/dev/null)"; [ -n "$p" ] && ln -s "$p" "$JQS/$b"; done
    PATH="$JQS" CLAUDE_CONFIG_DIR="$C" bash "$INSTALL" >/dev/null 2>&1
    python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); hs=[h for e in d["hooks"]["PreToolUse"] for h in e["hooks"] if "guard.sh" in h["command"]]; sys.exit(0 if len(hs)==1 and hs[0].get("type","command")=="command" and hs[0].get("timeout",600)>=120 else 1)' "$C/settings.json" \
      && ok "jq-only install repairs an owned hook ($fix)" || bad "jq-only install repairs an owned hook ($fix)"
    rm -rf "$JQS"
  done
fi

echo ""
echo "install-test: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
