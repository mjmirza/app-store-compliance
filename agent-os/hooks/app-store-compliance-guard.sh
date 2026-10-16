#!/usr/bin/env bash
# App Store Compliance Guard. Native and cross-platform (Flutter, RN/Expo, Ionic/Capacitor).
# Standalone or PreToolUse Bash hook on a submit command. See docs/CROSS-PLATFORM-FRAMEWORKS.md.
# @event: PreToolUse
# @matcher: Bash
set -uo pipefail

HOOK_LOG="${HOME:-}/.claude/hooks/hook-log.sh"
# shellcheck disable=SC1090
[ -f "$HOOK_LOG" ] && source "$HOOK_LOG" 2>/dev/null || true
log_err() { if type hlog_error >/dev/null 2>&1; then hlog_error "app-store-compliance-guard" "$@"; else echo "app-store-compliance-guard: $*" >&2; fi; }

CRIT=0; HIGH=0; MED=0; ANY_IOS=0; ANY_AND=0; ANY_NATIVE=0; ANY_RN=0; ANY_WEB=0; ANY_NEEDS_NATIVE=0; NATIVE_HINT=""; UNCHECKED=""; EXPO_READ=0
FILELIST=""
REPORT=""; REPORT_DEGRADED=0
cleanup() { [ -n "$FILELIST" ] && rm -f "$FILELIST" "$FILELIST.blob" "$FILELIST.manifest" "$FILELIST.code" "$FILELIST.impl" 2>/dev/null; [ -n "$REPORT" ] && rm -f "$REPORT" 2>/dev/null; true; }
trap cleanup EXIT

# ----- resolve mode and project dir -----
DIR=""
STDIN_JSON=""
CMD=""
if [ "$#" -ge 1 ] && [ -d "$1" ]; then
  DIR="$1"                                   # standalone with explicit path
elif [ "$#" -ge 1 ] && [ ! -d "$1" ]; then
  # An explicit path that is not a directory is a typo. Say so and exit 1, a path that was not read is never a pass.
  echo "app-store-compliance-guard: $1 is not a directory. Nothing was scanned." >&2; exit 1
elif [ ! -t 0 ]; then
  STDIN_JSON="$(cat 2>/dev/null || true)"    # hook mode, payload on stdin
  # An empty hook payload has no command to judge; falling back to scanning the working directory can take minutes.
  [ -z "$STDIN_JSON" ] && exit 0
fi
# Cursor beforeShellExecution reads a permission object on stdout, prose there is a schema error (cursor.com/docs/hooks).
IS_CURSOR=0; CURSOR_SENT=0; CURSOR_FD=0; CURSOR_IDS=""
printf '%s' "$STDIN_JSON" | tr -d '\n\r' | grep -qE '"hook_event_name"[[:space:]]*:[[:space:]]*"beforeShellExecution"' && IS_CURSOR=1
cursor_reply() {  # $1 exit code about to be returned. Prints the permission JSON once, on the real stdout
  [ "$IS_CURSOR" -eq 1 ] && [ "$CURSOR_SENT" -eq 0 ] || return 0
  CURSOR_SENT=1
  if [ "$1" -eq 2 ]; then
    local why="with ${CRIT:-0} critical rejection risk(s)"
    [ "${CRIT:-0}" -eq 0 ] && why="because the scan did not finish"
    printf '{"permission":"deny","user_message":"App Store Compliance Guard blocked this submit %s.","agent_message":"Blocked by app-store-compliance-guard %s. Critical findings. %s Fix each one using the report on stderr, or set APP_STORE_GUARD_OK=1 to override."}\n' "$why" "$why" "${CURSOR_IDS:-none listed.}"
  else
    printf '{"permission":"allow"}\n'
  fi
}

# Read .tool_input.command as JSON (issue #610). The best installed parser decides. jq, else python3,
# else a backslash-aware regex. A payload the chosen parser rejects yields no command, so the guard stays silent.
tool_ok() { command -v "$1" >/dev/null 2>&1 && "$@" >/dev/null 2>&1; }   # present AND able to run
payload_command() {
  local out
  if tool_ok jq -n true; then
    out="$(printf '%s' "$STDIN_JSON" | jq -rs 'if length != 1 then empty else .[0] | if type != "object" then empty else (.tool_name? // .toolName? // (if (.tool_info.command_line? | type) == "string" then "shell" else "Bash" end)) as $t | if (($t | type) != "string") or ((["Bash","PowerShell","bash","powershell","run_shell_command","shell","Execute","launch-process","execute_bash","execute_cmd","runInTerminal","run_in_terminal","run_terminal_command","run_terminal_cmd","monitor","execute_pwsh"] | any(. == $t)) | not) then empty else ((.tool_input.command? | strings) // (.toolInput.command? | strings) // (.toolArgs? | if type == "string" then (try fromjson catch null) else . end | if type == "object" then (.command? | strings) else empty end) // (.tool_info.command_line? | strings) // (.command? | strings) // empty) end end end' 2>/dev/null)" && { printf '%s' "$out"; return 0; }
  fi
  if tool_ok python3 -c pass; then
    out="$(printf '%s' "$STDIN_JSON" | python3 -c '
import json, sys
try:
    d = json.loads(sys.stdin.buffer.read().decode("utf-8-sig"))
except Exception:
    sys.exit(4)
c = None
SHELLS = ("Bash", "PowerShell", "bash", "powershell", "run_shell_command", "shell", "Execute", "launch-process", "execute_bash", "execute_cmd", "runInTerminal", "run_in_terminal", "run_terminal_command", "run_terminal_cmd", "monitor", "execute_pwsh")
info = d.get("tool_info") if isinstance(d, dict) else None
default = "shell" if isinstance(info, dict) and isinstance(info.get("command_line"), str) else "Bash"
t = d.get("tool_name", d.get("toolName", default)) if isinstance(d, dict) else None
if isinstance(d, dict) and isinstance(t, str) and t in SHELLS:
    ti = d.get("tool_input")
    if not isinstance(ti, dict) and isinstance(d.get("toolInput"), dict):
        ti = d["toolInput"]
    if not isinstance(ti, dict) and isinstance(info, dict) and isinstance(info.get("command_line"), str):
        ti = {"command": info["command_line"]}
    ta = d.get("toolArgs")
    if isinstance(ta, str):
        try:
            ta = json.loads(ta)
        except Exception:
            ta = None
    if isinstance(ti, dict) and isinstance(ti.get("command"), str):
        c = ti["command"]
    elif isinstance(ta, dict) and isinstance(ta.get("command"), str):
        c = ta["command"]
    elif isinstance(d.get("command"), str):
        c = d["command"]
sys.stdout.buffer.write((c or "").encode("utf-8"))' 2>/dev/null)"; rc=$?
    [ "$rc" -eq 0 ] && { printf '%s' "$out"; return 0; }
    [ "$rc" -eq 4 ] && return 0
  fi
  # No working tool. Prefer the command inside tool_input, then a Copilot toolArgs JSON string, then the first command key.
  local body ta tn
  # A named tool that is not a shell stays quiet here too, the same list jq and python3 use.
  tn="$(printf '%s' "$STDIN_JSON" | tr -d '\n\r' | grep -oE '"(tool_name|toolName)"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed -E 's/.*:[[:space:]]*"//; s/"$//')"
  if [ -n "$tn" ] && [ "$(printf '%s' "$STDIN_JSON" | grep -oE '"(tool_name|toolName)"[[:space:]]*:' | wc -l | tr -d ' ')" -eq 1 ]; then
    case "$tn" in Bash|PowerShell|bash|powershell|run_shell_command|shell|Execute|launch-process|execute_bash|execute_cmd|runInTerminal|run_in_terminal|run_terminal_command|run_terminal_cmd|monitor|execute_pwsh) ;; *) return 0 ;; esac
  fi
  body="$(printf '%s' "$STDIN_JSON" | tr -d '\n\r' | grep -oE '"tool_input"[[:space:]]*:[[:space:]]*\{([^{}]|\{[^{}]*\})*"command"[[:space:]]*:[[:space:]]*"([^"\\]|\\.)*"' | head -1)"
  if [ -z "$body" ]; then
    ta="$(printf '%s' "$STDIN_JSON" | tr -d '\n\r' | grep -oE '"toolArgs"[[:space:]]*:[[:space:]]*"([^"\\]|\\.)*"' | head -1 | sed -E 's/^"toolArgs"[[:space:]]*:[[:space:]]*"//; s/"$//')"
    [ -n "$ta" ] && body="$(printf '%s' "$ta" | json_unescape | tr -d '\n\r' | grep -oE '"command"[[:space:]]*:[[:space:]]*"([^"\\]|\\.)*"' | head -1)"
  fi
  [ -z "$body" ] && body="$(printf '%s' "$STDIN_JSON" | tr -d '\n\r' | grep -oE '"command"[[:space:]]*:[[:space:]]*"([^"\\]|\\.)*"' | head -1)"
  [ -z "$body" ] && body="$(printf '%s' "$STDIN_JSON" | tr -d '\n\r' | grep -oE '"command_line"[[:space:]]*:[[:space:]]*"([^"\\]|\\.)*"' | head -1 | sed 's/"command_line"/"command"/')"
  [ -z "$body" ] && return 0
  printf '%s' "$body" | sed -E 's/.*"command"[[:space:]]*:[[:space:]]*"//; s/"$//' | json_unescape
}
# Decodes JSON string escapes on stdin (newline, tab, quote, ASCII \u), for the no-tools tier.
json_unescape() {
  awk 'BEGIN { hx="0123456789abcdef" }
      { n=split($0, part, /\\/); o=part[1]; lit=0
        for (i=2; i<=n; i++) { p=part[i]
          if (lit) { o=o p; lit=0; continue }
          if (p=="") { o=o "\\"; lit=1; continue }
          d=substr(p,1,1); rest=substr(p,2)
          if (d=="n") o=o "\n" rest; else if (d=="t") o=o "\t" rest; else if (d=="r") o=o "\r" rest
          else if (d=="\"") o=o "\"" rest; else if (d=="/") o=o "/" rest
          else if (d=="f") o=o sprintf("%c", 12) rest; else if (d=="b") o=o sprintf("%c", 8) rest
          else if (d=="u" && length(p)>=5) { h=tolower(substr(p,2,4)); v=0; ok=1
            for (j=1;j<=4;j++) { q=index(hx,substr(h,j,1)); if (q==0) {ok=0; break}; v=v*16+q-1 }
            if (ok && v>0 && v<128) o=o sprintf("%c", v) substr(p,6); else o=o "\\" p }
          else o=o "\\" p }
        printf "%s", o }'
}

# The working folder another harness reports in the payload (Codex, Gemini CLI, Cursor, Copilot CLI send cwd).
payload_cwd() {
  if tool_ok jq -n true; then
    printf '%s' "$STDIN_JSON" | jq -rs 'if length == 1 and (.[0] | type) == "object" then .[0] | ((.cwd? | strings) // (.tool_info.cwd? | strings) // (.working_dir? | strings) // (.tool_input.cwd? | strings) // (.workspace_roots[0]? | strings) // empty) else empty end' 2>/dev/null
    return 0
  fi
  if tool_ok python3 -c pass; then
    printf '%s' "$STDIN_JSON" | python3 -c '
import json, sys
try:
    d = json.loads(sys.stdin.buffer.read().decode("utf-8-sig"))
except Exception:
    sys.exit(0)
c = None
if isinstance(d, dict):
    ti, info, roots = d.get("tool_input"), d.get("tool_info"), d.get("workspace_roots")
    for v in (d.get("cwd"), info.get("cwd") if isinstance(info, dict) else None, d.get("working_dir"),
              ti.get("cwd") if isinstance(ti, dict) else None, roots[0] if isinstance(roots, list) and roots else None):
        if isinstance(v, str) and v:
            c = v
            break
sys.stdout.write(c or "")' 2>/dev/null
  fi
}

if [ -n "$STDIN_JSON" ]; then
  # Only a shell tool call (Bash, run_shell_command, Grok run_terminal_command, and kin) carries a shell command. The jq and python3 tiers check the top-level tool_name.
  # The no-tools tier cannot tell a top-level key from a nested one, so it scans rather than skips.
  CMD="$(payload_command 2>/dev/null | tr -d '\000')"
  # Fold a backslash-newline continuation (odd trailing backslashes) into one space. Bare newlines stay,
  # and grep matches per line, so a trigger split across two commands is never invented.
  CMD="$(printf '%s' "$CMD" | tr -d '\r' | awk '
    { l=$0; if (cont) { sub(/^[ \t]*/, "", l); cont=0 }
      n=length(l); k=0; while (k<n && substr(l,n-k,1)=="\\") k++
      if (k%2==1) { acc=acc substr(l,1,n-1) " "; cont=1 } else { printf "%s%s\n", acc, l; acc="" } }
    END { if (cont) printf "%s\n", acc }' 2>/dev/null)"
  [ -z "$CMD" ] && exit 0
  # A commit, tag, note, or gh PR or issue message is text. Its quoted -m, --body, or --title value is blanked,
  # Only inside that git or gh segment, never a later command's, and never when the segment holds any substitution.
  IFS= read -r -d '' INERT_AWK <<'INERT'
BEGIN { sq=sprintf("%c", 39); dq="\""; bt=sprintf("%c", 96) }
function msgflag(w) { return w ~ /^(-[A-Za-z]*m|--message|-b|--body|-t|--title)$/ }
function blank(s,   o, i, n, c, w, prev, j, body) {
  o=""; w=""; prev=""; i=1; n=length(s)
  while (i <= n) { c=substr(s, i, 1)
    if (c == " " || c == "\t") { if (w != "") { prev=w; w="" }; o=o c; i++; continue }
    if (c == "\\") { o=o substr(s, i, 2); w=w substr(s, i, 2); i+=2; continue }
    if (c == sq || c == dq) {
      j=i+1; while (j <= n && substr(s, j, 1) != c) { if (c == dq && substr(s, j, 1) == "\\") j++; j++ }
      body=substr(s, i+1, j-i-1)
      if (j <= n && ((w == "" && msgflag(prev)) || (w ~ /=$/ && msgflag(substr(w, 1, length(w)-1)))) && (c == sq || (index(body, "$") == 0 && index(body, bt) == 0))) {
        o=o c c; w=w c c; i=j+1; continue }
      o=o substr(s, i, j-i+1); w=w substr(s, i, j-i+1); i=j+1; continue }
    o=o c; w=w c; i++ }
  return o }
function seg(s,   t) {
  if (index(s, "$(") || index(s, bt) || index(s, "<(") || index(s, ">(") || index(s, "=(")) return s
  t=s; sub(/^[ \t({!]+/, "", t)
  while (t ~ /^[A-Za-z_][A-Za-z0-9_]*=[^ \t]*[ \t]+/) sub(/^[A-Za-z_][A-Za-z0-9_]*=[^ \t]*[ \t]+/, "", t)
  if (t ~ /^git([ \t]+-C[ \t]+[^ \t]+)?[ \t]+(commit|tag|notes)([ \t]|$)/ || t ~ /^gh[ \t]+(pr|issue)[ \t]+(create|comment|edit)([ \t]|$)/) return blank(s)
  return s }
{ l=$0; n=length(l); cur=""; out=""; q=""; i=1
  while (i <= n) { c=substr(l, i, 1)
    if (q != "") { if (c == "\\" && q == dq) { cur=cur substr(l, i, 2); i+=2; continue }; if (c == q) q=""; cur=cur c; i++; continue }
    if (c == "\\") { cur=cur substr(l, i, 2); i+=2; continue }
    if (c == sq || c == dq) { q=c; cur=cur c; i++; continue }
    if (c == ";" || c == "|" || c == "&") { out=out seg(cur) c; cur=""; i++; continue }
    cur=cur c; i++ }
  raw[NR]=l; msk[NR]=out seg(cur); if (q != "") open=1 }
END { for (k=1; k<=NR; k++) print (open ? raw[k] : msk[k]) }
INERT
  # Match raw with quotes and letter escapes stripped. Only a single simple line led by an inert text command
  # (echo, grep, cat) has quoted spans blanked, and a heredoc body is blanked unless an interpreter consumes it.
  CMD_MATCH="$( { printf '%s\n' "$CMD" | awk "$INERT_AWK" 2>/dev/null || printf '%s' "$CMD"; } | awk 'BEGIN { sq=sprintf("%c", 39); dq="\""; bt=sprintf("%c", 96); hd=0 }
    { l=$0
      if (hd) { t=l; sub(/^\t+/, "", t); if (t == hd_end) { hd=0 } else if (!hd_keep) { l="" } ; print l; next }
      if (match(l, /<<-?[ \t]*[\047"]?[A-Za-z_][A-Za-z0-9_]*[\047"]?/) && substr(l, RSTART+2, 1) != "<") {
        tag=substr(l, RSTART, RLENGTH); sub(/^<<-?[ \t]*/, "", tag); gsub(/[\047"]/, "", tag); hd=1; hd_end=tag
        hd_keep = (l ~ /(^|[^A-Za-z0-9_\/-])((ba|z|da|k)?sh|eval|ssh|sudo|su|xargs|python[0-9.]*|node|ruby|perl|docker|kubectl|source)([^A-Za-z0-9_-]|$)/) }
      f=l; sub(/^[ \t]*/, "", f)
      while (f ~ /^[A-Za-z_][A-Za-z0-9_]*=[^ \t]*[ \t]+/) sub(/^[A-Za-z_][A-Za-z0-9_]*=[^ \t]*[ \t]+/, "", f)
      split(f, w, /[ \t]+/); c=w[1]
      simple = (index(l, "$(") == 0 && index(l, bt) == 0 && l !~ /[|;&<>]/)
      if (simple && c ~ /^(echo|printf|grep|egrep|fgrep|cat|head|tail|wc|sort|uniq|tee)$/) {
        gsub(sq "[^" sq "]*" sq, sq sq, l); gsub(dq "[^" dq "]*" dq, dq dq, l); sub(/(^|[ \t])#.*$/, "", l) }
      else { gsub(sq, "", l); gsub(dq, "", l) }
      print l }' 2>/dev/null | sed -E 's/\\([A-Za-z0-9])/\1/g')"
  # Only act on submission style commands. Otherwise stay silent.
  # Installing a package named like a submit tool (npm install bundletool) is not a submit.
  CMD_MATCH="$(printf '%s' "$CMD_MATCH" | sed -E 's/(npm|pnpm|yarn|bun|brew|pip3?|gem|cargo)[[:space:]]+(install|add|i|uninstall|remove)([[:space:]][^;&|$`]*)?//g')"
  # A Debug publish is a local build, never a store upload.
  CMD_MATCH="$(printf '%s' "$CMD_MATCH" | sed -E 's/dotnet[[:space:]]+publish[^;&|]*(-c|--configuration)[[:space:]=]+[Dd]ebug[^;&|]*//g')"
  # fastlane global options sit before the action or lane (fastlane --env production deliver). Drop them.
  fl_norm() { printf '%s' "$1" | sed -E ':a
s/(fastlane)[[:space:]]+--env([[:space:]]+|=)[^-[:space:];&|][^[:space:];&|]*/\1/
ta
s/(fastlane)[[:space:]]+--?[A-Za-z][A-Za-z0-9_-]*/\1/
ta'; }
  CMD_MATCH="$(fl_norm "$CMD_MATCH")"
  SUBMIT_RE='fastlane[[:space:]]+(run[[:space:]]+)?(deliver|pilot|supply|submit|appstore|testflight|upload_to_app_store|upload_to_testflight|upload_to_play_store)([^A-Za-z0-9_]|$)|eas([[:space:]]+--?[A-Za-z][A-Za-z0-9-]*([=[:space:]][^-[:space:]][^[:space:]]*)?)*[[:space:]]+(submit|build)|xcrun[[:space:]]+(altool|notarytool)|transporter|gradlew?[^&|;]*(bundleRelease|assembleRelease|publish[A-Za-z]*(Bundle|Apk|Apps)|promote[A-Za-z]*Artifact)|bundletool|xcodebuild[^&|;]*archive|flutter[[:space:]]+build[[:space:]]+(ipa|appbundle|apk|ios)|(npx[[:space:]]+)?(expo[[:space:]]+(prebuild|run:ios|run:android|submit|upload:(ios|android)|build:(ios|android))|cap[[:space:]]+(sync|build|run|copy|open)|react-native[[:space:]]+run-(ios|android))|ionic[[:space:]]+capacitor[[:space:]]+(build|run)|cordova[[:space:]]+build([[:space:]]+--release)?|(^|[^A-Za-z0-9_])unity(-editor|\.exe)?[[:space:]][^;&|]*-buildtarget[[:space:]]+(ios|android)|dotnet[[:space:]]+publish[^;&|]*(-f|--framework)[[:space:]=]+net[0-9.]+-(ios|android)|tauri[[:space:]]+(ios|android)[[:space:]]+build'
  UPLOAD_ACTION_RE='(^|[^A-Za-z0-9_])(upload_to_app_store|upload_to_testflight|upload_to_play_store|deliver|pilot|supply|appstore|testflight)([^A-Za-z0-9_]|$)'
  # A custom fastlane lane submits when a word in its name says so, when its Fastfile block calls an
  # upload action, or when the lane is a variable the guard cannot read (scanned, never assumed safe).
  fastlane_lane_submits() {
    local lane ff
    lane="$(printf '%s' "$1" | sed -nE 's/.*(^|[^A-Za-z0-9_.\/-])fastlane[[:space:]]+((ios|android|mac)[[:space:]]+)?([$`]|[A-Za-z_][A-Za-z0-9_]*).*/\4/p' | head -1)"
    [ -z "$lane" ] && return 1
    case "$lane" in '$'*|'`'*) return 0 ;; esac
    case "$lane" in *[!A-Za-z0-9_]*) return 1 ;; esac
    printf '%s' "$lane" | tr '_' '\n' | grep -qixE 'release|beta|deploy|production|prod|publish|submit|upload|appstore|playstore|testflight|distribute' && return 0
    while IFS= read -r ff; do
      [ -f "$ff" ] || continue
      awk -v n="$lane" '$0 ~ "lane[[:space:]]+:" n "([^A-Za-z0-9_]|$)" { on=1; next } on && /^[[:space:]]*(private_)?lane[[:space:]]+:/ { on=0 } on' "$ff" 2>/dev/null \
        | grep -qE "$UPLOAD_ACTION_RE" && return 0
    done <<FASTFILES
$(find "$DIR" -maxdepth 3 -name Fastfile -not -path '*/node_modules/*' 2>/dev/null | head -5)
FASTFILES
    return 1
  }
  submits() { set -- "$(fl_norm "$1")"; printf '%s' "$1" | grep -qiE "$SUBMIT_RE" || printf '%s' "$1" | grep -qE 'gradlew?[[:space:]]+\$' || fastlane_lane_submits "$1"; }
  # What a package script or a make target runs, one level deep, so a wrapped submit is still seen.
  runner_body() {  # $1 one command segment
    local name esc sub pj seg w prev mf targets mfiles
    local opts='([[:space:]]+--?[A-Za-z][A-Za-z-]*([=[:space:]][^-[:space:]][^[:space:]]*)?)*'
    local pre='.*(^|[^A-Za-z0-9_./-])'
    name="$(printf '%s' "$1" | sed -nE "s/${pre}(npm|pnpm|bun)${opts}[[:space:]]+run(-script)?${opts}[[:space:]]+([A-Za-z0-9:_.][A-Za-z0-9:_.-]*).*/\8/p" | head -1)"
    [ -z "$name" ] && name="$(printf '%s' "$1" | sed -nE "s/${pre}yarn[[:space:]]+workspace[[:space:]]+[^[:space:]]+[[:space:]]+(run[[:space:]]+)?([A-Za-z0-9:_.-]+).*/\3/p" | head -1)"
    [ -z "$name" ] && name="$(printf '%s' "$1" | sed -nE "s/${pre}yarn[[:space:]]+workspaces[[:space:]]+foreach${opts}[[:space:]]+(run[[:space:]]+)?([A-Za-z0-9:_.-]+).*/\5/p" | head -1)"
    [ -z "$name" ] && name="$(printf '%s' "$1" | sed -nE "s/${pre}(turbo|lerna)${opts}[[:space:]]+run[[:space:]]+([A-Za-z0-9:_.-]+).*/\5/p" | head -1)"
    [ -z "$name" ] && name="$(printf '%s' "$1" | sed -nE "s/${pre}nx${opts}[[:space:]]+run(-many)?[[:space:]]+([A-Za-z0-9_.@\/-]+:)?([A-Za-z0-9_.][A-Za-z0-9_.-]*).*/\6/p" | head -1)"
    [ -z "$name" ] && name="$(printf '%s' "$1" | sed -nE "s/${pre}nx${opts}[[:space:]]+(run-many|affected)([[:space:]]+[^[:space:]]+)*[[:space:]]+(-t|--targets?)[=[:space:]]+([A-Za-z0-9_.-]+).*/\7/p" | head -1)"
    [ -z "$name" ] && name="$(printf '%s' "$1" | sed -nE "s/${pre}(pnpm|bun|turbo)${opts}[[:space:]]+([A-Za-z0-9:_.-]+).*/\5/p" | head -1)"
    [ -z "$name" ] && name="$(printf '%s' "$1" | sed -nE "s/${pre}nx${opts}[[:space:]]+([A-Za-z0-9:_.-]+).*/\4/p" | head -1)"
    case "$name" in run|run-many|affected|exec|install|i|add|x|dlx) name="" ;; esac
    [ -z "$name" ] && name="$(printf '%s' "$1" | sed -nE "s/${pre}yarn${opts}[[:space:]]+(run[[:space:]]+)?([A-Za-z0-9:_.-]+).*/\5/p" | head -1)"
    if [ -n "$name" ]; then
      local sel sub all files pick s2 base f d pat scoped one
      esc="$(printf '%s' "$name" | sed 's/\./\\./g')"
      # The package the runner names, or the folder it runs in. Unknown or none named means every package is read.
      local rseg="$1"
      sel="$(printf '%s\n' "$rseg" | grep -oE '(yarn[[:space:]]+workspace|(^|[[:space:]])(--filter|-F|--workspace|-w|--scope))[=[:space:]]+[^[:space:]]+' | sed -E 's/.*[=[:space:]]//')"
      [ -z "$sel" ] && sel="$(printf '%s' "$rseg" | sed -nE 's/.*nx[^;&|]*[[:space:]]run[[:space:]]+([A-Za-z0-9_.@\/-]+):.*/\1/p' | head -1)"
      sub="$(printf '%s' "$rseg" | sed -nE 's/.*[[:space:]](--dir|--prefix|--cwd|-C)[=[:space:]]+([^[:space:]]+).*/\2/p' | head -1)"
      case "$sub" in /*|*..*) sub="" ;; esac
      all=0; printf '%s' "$rseg" | grep -qE '(^|[^A-Za-z0-9_./-])(turbo|lerna)[[:space:]]|(^|[^A-Za-z0-9_./-])nx[[:space:]]|[[:space:]](-r|--recursive|-ws|--workspaces|foreach)([[:space:]=]|$)' && all=1
      files="$(find "$DIR" -maxdepth 6 \( -type d \( -name node_modules -o -name .git -o -name Pods -o -name build \) -prune \) -o \( -name package.json -o -name project.json \) -print 2>/dev/null | head -200)"
      if [ -n "$sub" ] && [ -f "$DIR/$sub/package.json" ]; then pick="$DIR/$sub/package.json"
      elif [ -n "$sel" ]; then
        pick=""
        while IFS= read -r s2; do
          [ -n "$s2" ] || continue
          # an exclusion such as '!@acme/docs' selects every other package, so every package is read
          case "$s2" in '!'*) pick="$files"; break ;; esac
          s2="${s2#./}"; s2="${s2#!}"; s2="${s2#^}"; s2="${s2#...}"; s2="${s2%...}"; s2="${s2#\{}"; s2="${s2%\}}"; s2="${s2%/}"; base="${s2##*/}"
          # bash 3.2 misreads a case pattern inside $( ), so the scope test sits out here.
          scoped=0; pat="(@[^/\"]+/)?$base"
          case "$s2" in @*/*) scoped=1; pat="$s2" ;; esac
          one="$(printf '%s\n' "$files" | while IFS= read -r f; do
            [ -n "$f" ] || continue; d="$(dirname "$f")"
            if [ "$scoped" -eq 0 ] && { [ "${d##*/}" = "$base" ] || [ "${d%/$s2}" != "$d" ]; }; then echo "$f"; continue; fi
            tr -d '\n' < "$f" 2>/dev/null | grep -qE "\"name\"[[:space:]]*:[[:space:]]*\"$pat\"" && echo "$f"
          done)"
          if [ -z "$one" ]; then pick="$files"; break; fi
          pick="$pick
$one"
        done <<SELS
$sel
SELS
      elif [ "$all" -eq 1 ]; then pick="$files"
      else pick="$DIR/package.json"; fi
      pick="$(printf '%s\n%s' "$DIR/package.json" "$pick" | awk 'NF && !seen[$0]++')"
      printf '%s\n' "$pick" | while IFS= read -r pj; do
        [ -f "$pj" ] || continue
        tr -d '\n' < "$pj" 2>/dev/null | grep -oE "\"$esc\"[[:space:]]*:[[:space:]]*(\"([^\"\\\\]|\\\\.)*\"|\{([^{}]|\{([^{}]|\{[^{}]*\})*\})*)"
      done
    fi
    seg="$(printf '%s' "$1" | sed -nE 's/.*(^|[^A-Za-z0-9_.\/-])make[[:space:]]+([^;&|]*).*/\2/p' | head -1)"
    if [ -n "$seg" ]; then
      targets=""; mfiles="Makefile makefile GNUmakefile"; prev=""
      set -f
      for w in $seg; do
        if [ "$prev" = "-f" ]; then case "$w" in /*|*..*) ;; *) mfiles="$mfiles $w" ;; esac
        else case "$w" in -*|*=*) ;; *[!A-Za-z0-9_.-]*) ;; *) targets="$targets $w" ;; esac
        fi
        prev="$w"
      done
      for w in $targets; do
        for mf in $mfiles; do
          [ -f "$DIR/$mf" ] && awk -v t="$w" 'index($0, t ":") == 1 { on=1; next } on && /^[^\t#]/ { on=0 } on' "$DIR/$mf" 2>/dev/null
        done
      done
      set +f
    fi
  }
  wrapper_body() {  # every runner and make segment, so a later web build never masks an earlier submit
    local sg
    runner_body "$CMD_MATCH"
    printf '%s\n' "$CMD_MATCH" | tr ';&|$()`' '\n\n\n\n\n\n\n' | while IFS= read -r sg; do
      [ -n "$sg" ] && runner_body "$sg"
    done
  }
  # Cheap exit for the everyday command. Nothing below runs unless a submit tool or a wrapper is named.
  if ! printf '%s' "$CMD_MATCH" | grep -qiE "$SUBMIT_RE" \
    && ! printf '%s' "$CMD_MATCH" | grep -qE '(^|[^A-Za-z0-9_./-])(fastlane|npm|pnpm|bun|yarn|make|turbo|nx|lerna)[[:space:]]|gradlew?[[:space:]]+\$'; then
    exit 0
  fi
  DIR="${CLAUDE_PROJECT_DIR:-}"
  if [ -z "$DIR" ]; then
    PCWD="$(payload_cwd 2>/dev/null)"
    if [ -n "$PCWD" ] && [ -d "$PCWD" ]; then DIR="$PCWD"
    elif [ -n "${GEMINI_PROJECT_DIR:-}" ] && [ -d "${GEMINI_PROJECT_DIR}" ]; then DIR="$GEMINI_PROJECT_DIR"
    elif [ -n "${AUGMENT_PROJECT_DIR:-}" ] && [ -d "${AUGMENT_PROJECT_DIR}" ]; then DIR="$AUGMENT_PROJECT_DIR"
    else DIR="$PWD"; fi
  fi
  # A leading "cd <dir> &&" scopes the scan to that app (an EAS monorepo submits from apps/<app>).
  # The target must resolve inside the project root, otherwise the root is scanned as before.
  FIRST="$(printf '%s' "$CMD" | head -1)"
  CD_COUNT="$(printf '%s' "$CMD" | grep -oE '(^|[;&|(][[:space:]]*)(cd|pushd|popd|source|\.)[[:space:]]' | wc -l | tr -d ' ')"
  if [ "$CD_COUNT" -eq 1 ] && printf '%s' "$FIRST" | grep -qE '^[[:space:]]*cd[[:space:]]+[^&|;]+(&&|;)'; then
    TARGET="$(printf '%s' "$FIRST" | sed -E 's/^[[:space:]]*cd[[:space:]]+//; s/[[:space:]]*(&&|;).*$//; s/^"(.*)"$/\1/; s/^'"'"'(.*)'"'"'$/\1/')"
    TARGET="${TARGET//\$\{CLAUDE_PROJECT_DIR\}/$DIR}"; TARGET="${TARGET//\$CLAUDE_PROJECT_DIR/$DIR}"
    case "$TARGET" in /*) ;; '~'*) TARGET="${HOME:-}${TARGET#\~}" ;; *) TARGET="$DIR/$TARGET" ;; esac
    if [ -d "$TARGET" ]; then
      REAL_T="$(cd "$TARGET" 2>/dev/null && pwd -P)"; REAL_R="$(cd "$DIR" 2>/dev/null && pwd -P)"
      case "$REAL_T/" in "$REAL_R"/*) DIR="$REAL_T" ;; esac
    fi
  fi
  if ! submits "$CMD_MATCH"; then
    WRAPPED="$(wrapper_body | tr -d "\"'\\\\")"
    { [ -n "$WRAPPED" ] && submits "$WRAPPED"; } || exit 0
  fi
fi

# See docs/CROSS-PLATFORM-FRAMEWORKS.md: an Android-only command beats a committed ios/
# folder for the Apple-only checks below (standalone mode has no CMD, unaffected).
CMD_TARGET_ANDROID_ONLY=0
# An Android token must be the gradle task, the platform flag or the build verb itself, never a word inside another argument.
W_END='([[:space:]]|$)'
AND_TARGET_RE="(^|[[:space:]])flutter[[:space:]]+build[[:space:]]+(apk|appbundle)$W_END|(^|[[:space:]/])gradlew?([[:space:]]+[^[:space:]]+)*[[:space:]]+:?([A-Za-z0-9_.-]+:)*(assembleRelease|bundleRelease)$W_END|(^|[[:space:]])(run-android|run:android)$W_END|(^|[[:space:]])(-p|--platform)([[:space:]]+|=)android$W_END|capacitor[[:space:]]+android$W_END|(^|[[:space:]])-buildtarget[[:space:]]+android$W_END|(^|[[:space:]=])net[0-9.]+-android$W_END|tauri[[:space:]]+android$W_END"
# An Apple upload in a segment means that segment is never Android, whatever words its arguments carry.
IOS_TARGET_RE='\bios\b|\bipa\b|xcodebuild|altool|notarytool|transporter|fastlane[[:space:]]+(run[[:space:]]+)?(deliver|pilot|appstore|testflight|upload_to_app_store|upload_to_testflight)([^A-Za-z0-9_]|$)'
if [ -n "$CMD" ]; then
  # Each submitting segment is classified on its own. Android only means every submit in the command is Android.
  SEG_SUBMITS=0; SEG_ALL_AND=1
  # Beside an Android submit only a known harmless command keeps it Android only. Anything else may upload to Apple.
  SAFE_SEG_RE='^(cd|pushd|popd|echo|printf|export|unset|set|true|false|:|test|sleep|ls|pwd|mkdir|rm|cp|mv|cat|touch|tee|grep|head|tail|wc|date|clear)$'
  SUBST=0; printf '%s' "$CMD" | grep -qE '\$\(|`|<\(|>\(|=\(' && SUBST=1
  while IFS= read -r SEG; do
    W1="$(printf '%s' "$SEG" | awk '{ sub(/^[ \t({!]+/, ""); while (match($0, /^[A-Za-z_][A-Za-z0-9_]*=[^ \t]*[ \t]+/)) $0 = substr($0, RLENGTH + 1); print $1 }')"
    [ -n "$W1" ] || continue
    if ! submits "$SEG"; then
      { [ "$SUBST" -eq 0 ] && printf '%s' "$W1" | grep -qE "$SAFE_SEG_RE"; } || SEG_ALL_AND=0
      continue
    fi
    SEG_SUBMITS=$((SEG_SUBMITS+1))
    SEGN="$(fl_norm "$SEG")"
    { printf '%s' "$SEGN" | grep -qiE "$AND_TARGET_RE" && ! printf '%s' "$SEGN" | grep -qiE "$IOS_TARGET_RE"; } || SEG_ALL_AND=0
  done <<SEGS
$(printf '%s\n' "$CMD_MATCH" | tr ';&|' '\n\n\n')
SEGS
  if printf '%s' "$CMD" | grep -qiE "$IOS_TARGET_RE"; then
    :   # an Apple word anywhere in the command keeps the Apple checks, as on main
  elif [ "$SEG_SUBMITS" -gt 0 ]; then
    [ "$SEG_ALL_AND" -eq 1 ] && CMD_TARGET_ANDROID_ONLY=1
  # A wrapped submit (npm run, make) names no tool in the command itself, so the whole command decides, as before.
  elif printf '%s' "$CMD" | grep -qiE "$AND_TARGET_RE" && ! printf '%s' "$CMD" | grep -qiE "$IOS_TARGET_RE"; then
    CMD_TARGET_ANDROID_ONLY=1
  fi
  # Each command in the line is read twice, quoted text kept and quoted text blanked, # comments dropped. A submit is found
  # in the kept text, its Android word only in the blanked text, and anything that is neither a submit nor harmless keeps Apple.
  if [ "$CMD_TARGET_ANDROID_ONLY" -eq 1 ]; then
    NQ_SEP="$(printf '\037')"
    CMD_PAIRS="$(printf '%s' "$CMD" | awk -v sq="'" -v sep="$NQ_SEP" '{ k=""; b=""; n=length($0); i=1
      while (i <= n) { c=substr($0, i, 1)
        if (c == "#" && (i == 1 || substr($0, i-1, 1) ~ /[ \t]/)) break
        if (c == sq || c == "\"") { j=i+1; while (j <= n && substr($0, j, 1) != c) { if (c == "\"" && substr($0, j, 1) == "\\") j++; j++ }
          k=k substr($0, i+1, j-i-1); b=b " "; i=j+1; continue }
        if (c == ";" || c == "&" || c == "|" || c == "(" || c == ")") { print k sep b; k=""; b=""; i++; continue }
        k=k c; b=b c; i++ }
      print k sep b }')"
    NQ_SUB=0; NQ_AND=1; NQ_WRAP=0; NQ_WRAP_AND=1
    while IFS="$NQ_SEP" read -r NQK NQB; do
      NQW="$(printf '%s' "$NQK" | awk '{ sub(/^[ \t({!]+/, ""); while (match($0, /^[A-Za-z_][A-Za-z0-9_]*=[^ \t]*[ \t]+/)) $0 = substr($0, RLENGTH + 1); print $1 }')"
      [ -n "$NQW" ] || continue
      if submits "$NQK"; then
        NQ_SUB=$((NQ_SUB+1))
        printf '%s' "$NQB" | grep -qiE "$AND_TARGET_RE" || NQ_AND=0
        # the outer arguments of bash -c, sh -c or eval never reach the quoted command, so they name no target
        printf '%s' "$NQB" | grep -qE '(^|[[:space:]/])(bash|sh|zsh|dash|ksh|fish|eval)([[:space:]]|$)' && NQ_AND=0
        # a submit seen only inside quotes runs in another program (python -c, ruby -e), which never passes it the outer arguments
        submits "$NQB" || NQ_AND=0
      elif ! printf '%s' "$NQW" | grep -qE "$SAFE_SEG_RE"; then
        NQ_AND=0; NQ_WRAP=$((NQ_WRAP+1))
        printf '%s' "$NQB" | grep -qiE "$AND_TARGET_RE" || NQ_WRAP_AND=0
      fi
    done <<NQSEGS
$CMD_PAIRS
NQSEGS
    if [ "$SEG_SUBMITS" -gt 0 ]; then
      [ "$NQ_SUB" -gt 0 ] && [ "$NQ_AND" -eq 1 ] || CMD_TARGET_ANDROID_ONLY=0
    else
      # A wrapped submit is Android only when every command that is not harmless names Android itself, never an echo beside it.
      [ "$NQ_WRAP" -gt 0 ] && [ "$NQ_WRAP_AND" -eq 1 ] || CMD_TARGET_ANDROID_ONLY=0
    fi
  fi
fi
# Android only also needs the 1.0.0 rule, so the Apple checks are never off where 1.0.0 ran them.
if [ "$CMD_TARGET_ANDROID_ONLY" -eq 1 ] && ! { printf '%s' "$CMD" | grep -qiE 'build[[:space:]]+(apk|appbundle)\b|assembleRelease|bundleRelease|run-android|run:android|--platform[[:space:]]+android\b|capacitor[[:space:]]+android\b|-buildtarget[[:space:]]+android|net[0-9.]+-android|tauri[[:space:]]+android\b' \
  && ! printf '%s' "$CMD" | grep -qiE '\bios\b|\bipa\b|xcodebuild|altool|notarytool'; }; then
  CMD_TARGET_ANDROID_ONLY=0
fi
CMD_TARGET_IOS_ONLY=0
if [ -n "$CMD" ] && printf '%s' "$CMD" | grep -qiE '(-p|--platform)[[:space:]=]+ios([^A-Za-z]|$)' \
  && ! printf '%s' "$CMD" | grep -qiE 'android|(-p|--platform)[[:space:]=]+all'; then
  CMD_TARGET_IOS_ONLY=1
fi

[ -z "$DIR" ] && DIR="$PWD"
[ -d "$DIR" ] || { log_err "project dir not found. $DIR"; cursor_reply 0; exit 0; }
[ -L "${DIR%/}" ] && DIR="$(cd "$DIR" 2>/dev/null && pwd -P)"   # find never descends a symlinked start point (issue #612)

# Every text file once, into one blob, so a hundred grep_has calls read one file instead of every file
# each (issue #612). The empty pattern keeps every line, -I drops binaries as before, the end marker proves a complete write.
BLOB_END="~~ascg~blob~end~$$~${RANDOM}~~"
build_blob() {
  BLOB_OK=0
  : > "$FILELIST.blob" 2>/dev/null || return 0
  [ -s "$FILELIST" ] || { BLOB_OK=1; return 0; }
  tr '\n' '\0' < "$FILELIST" | xargs -0 grep -EIh -e '' >> "$FILELIST.blob" 2>/dev/null
  printf '\n%s\n' "$BLOB_END" >> "$FILELIST.blob" 2>/dev/null
  [ "$(tail -n 1 "$FILELIST.blob" 2>/dev/null)" = "$BLOB_END" ] && BLOB_OK=1
}
grep_has() {  # 0 if regex found in any source file. Per-line regex, so the blob answers the same as a per-file grep
  [ -s "$FILELIST" ] || return 1
  if [ "${BLOB_OK:-0}" -eq 1 ]; then grep -Eqs -e "$1" "$FILELIST.blob" 2>/dev/null; return; fi
  local out
  out="$(tr '\n' '\0' < "$FILELIST" | xargs -0 grep -EIls -e "$1" 2>/dev/null | head -1)"
  [ -n "$out" ]
}

manifest_has() {  # 0 if regex found in any AndroidManifest.xml in the source list
  [ -s "$FILELIST" ] || return 1
  local out
  out="$(grep '/AndroidManifest\.xml$' "$FILELIST" | tr '\n' '\0' | xargs -0 grep -EIls -e "$1" 2>/dev/null | head -1)"
  [ -n "$out" ]
}

# Where a purpose string can live. Info.plist and its strings, build settings, XcodeGen, Expo config.
CONFIG_FILES_RE='(\.plist|\.pbxproj|\.xcconfig|\.ya?ml|/project\.json|/config\.xml|/Project\.swift|/Tuist/.*\.swift|\.csproj|/app\.json|/app\.config\.[cm]?[jt]s)$'
config_has() {  # 0 if regex found in a config file, never in Swift or Kotlin source or a comment there
  [ -s "$FILELIST" ] || return 1
  local out
  out="$(grep -E "$CONFIG_FILES_RE" "$FILELIST" | tr '\n' '\0' | xargs -0 grep -EIls -e "$1" 2>/dev/null | head -1)"
  [ -n "$out" ]
}

SRC_EXT_RE='\.(swift|m|mm|h|kt|kts|java|js|jsx|ts|tsx|dart|cs|rs)$'
# Comments dropped line by line, with no string state, so a misread quote can never hide a later line.
# Only the implementation buffer is stripped. Triggers read every line raw, as in 1.0.0, so no comment rule can hide a call.
STRIP_AWK='BEGIN { sq=sprintf("%c", 39) }
    function opener(s, m,   i) { for (i=2; i<length(s); i++) if (substr(s, i, 2) == m && substr(s, i-1, 1) ~ /[ \t;{},)]/) return i; return 0 }
    { l=$0; if (index(l, "/") == 0 && index(l, "*") == 0) { print l; next }
      t=l; sub(/^[ \t]+/, "", t)
      if (substr(t, 1, 2) == "//") { print ""; next }
      if (substr(t, 1, 2) == "*/") { print substr(t, 3); next }
      if (t == "*" || substr(t, 1, 2) == "* " || substr(t, 1, 2) == "*\t") { print ""; next }
      if (substr(t, 1, 2) == "/*") { r=t; sub(/[ \t]+$/, "", r); j=index(substr(r, 3), "*/")
        if (j == 0 || j + 3 == length(r)) { print ""; next } }
      if (tc) {
        while (index(l, "/*") && (o=opener(l, "/*")) > 0 && (c=index(substr(l, o+2), "*/")) > 0) { pre=substr(l, 1, o-1); if (pre !~ /#"/) gsub(/\\./, "", pre); gsub(/(^|[=(,:&|!?{};+*%<>~^-]|return)[ \t]*\/[^\/]+\//, " ", pre); p2=pre
          nq=gsub(/[\"`]/, "", pre); ns=gsub(sq, "", p2); if (nq % 2 || ns % 2) break; l=substr(l, 1, o-1) " ; " substr(l, o+c+3) }
        if (index(l, "//") && (o=opener(l, "//")) > 0 && substr(l, o+2) !~ /<\/|\/>/) { pre=substr(l, 1, o-1); if (pre !~ /#"/) gsub(/\\./, "", pre); gsub(/(^|[=(,:&|!?{};+*%<>~^-]|return)[ \t]*\/[^\/]+\//, " ", pre); p2=pre; nq=gsub(/[\"`]/, "", pre); ns=gsub(sq, "", p2); if (nq % 2 == 0 && ns % 2 == 0) l=substr(l, 1, o-1) } }
      print l }'
build_code() {  # .code is the trigger buffer, .impl the buffer an implementation must appear in (no config or translation text)
  CODE_OK=0
  : > "$FILELIST.code" 2>/dev/null || return 0
  : > "$FILELIST.impl" 2>/dev/null || return 0
  { grep -E "$SRC_EXT_RE" "$FILELIST" | tr '\n' '\0' | xargs -0 awk -v tc=1 "$STRIP_AWK" 2>/dev/null
    grep -E '\.html$' "$FILELIST" | tr '\n' '\0' | xargs -0 awk 'function flush(   k) { if (nh) { for (k=1; k<=nh; k++) print hr[k]; nh=0 } }
      FNR == 1 { flush(); hc=0 } { l=$0; o=""
        while (l != "") { if (hc) { p=index(l, "-->"); if (p == 0) { l=""; break }; l=substr(l, p+3); hc=0; continue }
          p=index(l, "<!--"); if (p == 0) { o=o l; break }
          pre=substr(l, 1, p-1); if (o pre !~ /(^[ \t]*|>[ \t]*)$/) { o=o substr(l, 1, p+3); l=substr(l, p+4); continue }
          o=o pre; l=substr(l, p+4); hc=1 }
        if (hc) { nh++; ho[nh]=o; hr[nh]=$0; next }
        if (nh) { for (k=1; k<=nh; k++) print ho[k]; nh=0 }
        print o } END { flush() }' 2>/dev/null
    printf '\n%s\n' "$BLOB_END"; } >> "$FILELIST.impl" 2>/dev/null
  { tr '\n' '\0' < "$FILELIST" | xargs -0 grep -EIh -e '' 2>/dev/null
    printf '\n%s\n' "$BLOB_END"; } >> "$FILELIST.code" 2>/dev/null
  [ "$(tail -n 1 "$FILELIST.code" 2>/dev/null)" = "$BLOB_END" ] && [ "$(tail -n 1 "$FILELIST.impl" 2>/dev/null)" = "$BLOB_END" ] && CODE_OK=1
}
code_has() {  # grep_has over every file read raw, as in 1.0.0. Falls back to grep_has without a buffer
  [ -s "$FILELIST" ] || return 1
  [ -n "${CODE_STATE:-}" ] || { build_code; CODE_STATE=1; }
  if [ "${CODE_OK:-0}" -eq 1 ]; then grep -Eqs -e "$1" "$FILELIST.code" 2>/dev/null; return; fi
  grep_has "$1"
}
impl_has() {  # comment-stripped source and HTML only. a .strings, plist or json mention never proves an implementation
  [ -s "$FILELIST" ] || return 1
  [ -n "${CODE_STATE:-}" ] || { build_code; CODE_STATE=1; }
  if [ "${CODE_OK:-0}" -eq 1 ]; then grep -Eqs -e "$1" "$FILELIST.impl" 2>/dev/null; return; fi
  grep_has "$1"
}

# The app's own privacy manifest. A copy under Pods, Carthage, node_modules, SwiftPM or Flutter symlinks is the SDK's.
own_privacy_manifest() {
  find "$DIR" -mindepth 1 \( -type d \( -name node_modules -o -name Pods -o -name Carthage -o -name .build -o -name checkouts \
    -o -name SourcePackages -o -name .symlinks -o -name vendor -o -name .pub-cache -o -name .dart_tool -o -name DerivedData \
    -o -name build -o -name .git ${NESTED_PRUNE[@]+"${NESTED_PRUNE[@]}"} \) -prune \) -o -name 'PrivacyInfo.xcprivacy' -print 2>/dev/null \
    | grep . >/dev/null
}

# True only if a STRING LITERAL containing the regex appears in RELEASE-reachable source. For
# Swift, `#if DEBUG` / `#if !RELEASE` debug-only regions are stripped first, so a URL only a debug
# build compiles is not flagged. The string-literal requirement (the match must sit inside "...")
# skips comments and identifiers. This is what makes the backend check precise instead of matching
# a localhost mentioned in a comment or guarded behind DEBUG. Without it the check cries wolf.
release_string_has() {
  [ -s "$FILELIST" ] || return 1
  local f
  while IFS= read -r f; do
    case "$f" in
      *.swift)
        awk '
          /^[ \t]*#if/    { d++; if ($0 ~ /#if[ \t]+DEBUG/ || $0 ~ /#if[ \t]+!RELEASE/) { dbg=d; skip=1 } next }
          /^[ \t]*#else/  { if (skip && d==dbg) skip=0; next }
          /^[ \t]*#elseif/ { next }
          /^[ \t]*#endif/ { if (skip && d==dbg) { skip=0; dbg=0 } d--; next }
          !skip { print }
        ' "$f" 2>/dev/null ;;
      *) cat "$f" 2>/dev/null ;;
    esac
  done < "$FILELIST" \
    | LC_ALL=C grep -E "\"[^\"]*($1)[^\"]*\"" >/dev/null 2>&1
  # NOTE. no `grep -q`. With `set -o pipefail`, `grep -q` exits on the first match and
  # closes the pipe, so the still-writing awk/cat producer gets SIGPIPE (141) and pipefail
  # then reports the whole pipeline non-zero even though grep matched. That made this check
  # silently miss on the CI runner (GNU grep, timing-dependent) while passing on a fast local
  # machine. Draining all input with plain grep and returning its status is deterministic.
}

# Prints the first file and line that match, relative to the scanned folder. $1 is src or manifest.
hit_file() {
  [ -s "$FILELIST" ] || return 0
  local f n
  if [ "$1" = "manifest" ]; then
    f="$(grep '/AndroidManifest[.]xml$' "$FILELIST" | tr '\n' '\0' | xargs -0 grep -EIls -e "$2" 2>/dev/null | head -1)"
  else
    f="$(tr '\n' '\0' < "$FILELIST" | xargs -0 grep -EIls -e "$2" 2>/dev/null | head -1)"
  fi
  [ -n "$f" ] || return 0
  n="$(grep -En -m1 -e "$2" "$f" 2>/dev/null | cut -d: -f1)"
  printf '%s%s' "${f#"${DIR%/}"/}" "${n:+:$n}"
}

# Findings are held and printed by flush_findings, critical first (issue #842).
F_CRIT=(); F_HIGH=(); F_MED=(); FOUND_IDS=""; POOL_PASS=0
finding() {  # severity id title fix [src|manifest regex]. The optional pair names the file that triggered it.
  local t w=""
  case "$FOUND_IDS" in *"|$1:$2|"*) [ "$POOL_PASS" -eq 1 ] && return 0 ;; esac
  FOUND_IDS="$FOUND_IDS|$1:$2|"
  [ -n "${5:-}" ] && w="$(hit_file "$5" "${6:-}")"
  case "$1" in
    critical) CRIT=$((CRIT+1)); t="  [CRITICAL] $2  $3" ;;
    high)     HIGH=$((HIGH+1)); t="  [HIGH]     $2  $3" ;;
    *)        MED=$((MED+1));   t="  [MEDIUM]   $2  $3" ;;
  esac
  [ -n "$w" ] && t="$t"$'\n'"      file. $w"
  t="$t"$'\n'"      fix. $4"
  case "$1" in critical) F_CRIT+=("$t") ;; high) F_HIGH+=("$t") ;; *) F_MED+=("$t") ;; esac
}
flush_findings() {
  local t
  for t in ${F_CRIT[@]+"${F_CRIT[@]}"} ${F_HIGH[@]+"${F_HIGH[@]}"} ${F_MED[@]+"${F_MED[@]}"}; do printf '%s\n' "$t"; done
  F_CRIT=(); F_HIGH=(); F_MED=()
}

# Cross-platform apps reach StoreKit and Play Billing through a plugin, so the native symbols never
# appear in their source. These are the plugins' own package names.
XPLAT_IAP='in_app_purchase|purchases_flutter|flutter_inapp_purchase|react-native-iap|react-native-purchases|expo-iap|cordova-plugin-purchase|@revenuecat/purchases-capacitor|UnityEngine\.Purchasing|com\.unity\.purchasing|Plugin\.InAppBilling|tauri-plugin-iap'

# Vendored trees never decide the platform, and the prune applies only below the project root, so a project
# that itself sits under a folder named build or test is still detected. Same SIGPIPE-safe grep as the source scan.
find_app() {  # find_app <maxdepth> <find name expression...>
  local depth="$1"; shift
  find "$DIR" -mindepth 1 -maxdepth "$depth" \
    \( -type d \( -name node_modules -o -name Pods -o -name .git -o -name build -o \( -name dist -not -path '*/src/dist' \) \
      -o -name DerivedData -o -name vendor -o -name .dart_tool -o -name Carthage -o -name .pub-cache \
      ${NESTED_PRUNE[@]+"${NESTED_PRUNE[@]}"} \) -prune \) \
    -o \( "$@" \) -print 2>/dev/null
}
NESTED_PRUNE=()
find_tree() {  # find "$DIR" <expr>, the whole tree as before, minus the nested app roots when the root is itself an app
  if [ "${#NESTED_PRUNE[@]}" -eq 0 ]; then find "$DIR" "$@" 2>/dev/null
  else find "$DIR" \( -type d \( -name '' "${NESTED_PRUNE[@]}" \) -prune \) -o "$@" 2>/dev/null; fi
}
FILELIST="$(mktemp 2>/dev/null)" || FILELIST=""
{ [ -n "$FILELIST" ] && : > "$FILELIST" 2>/dev/null; } || FILELIST="/tmp/ascg.$$"
# No scan buffer means no scan. Say so rather than end CLEAR on an empty file list.
if [ -z "$FILELIST" ] || ! : > "$FILELIST" 2>/dev/null; then
  NOTE="NOT CHECKED. The guard could not create its scan buffer in ${TMPDIR:-/tmp}, so nothing was scanned. Point TMPDIR at a writable folder and run it again."
  if [ -n "$STDIN_JSON" ]; then echo "app-store-compliance-guard. $NOTE" >&2; cursor_reply 0; exit 0; fi
  echo "$NOTE"; exit 1
fi
SCAN_ERROR=""

# ----- the scan of one tree (issue #612). Runs once per app root, or once on the project root -----
detect_frameworks() {  # sets the IS_<framework> flags for the tree under DIR
IS_FLUTTER=0; IS_RN=0; IS_IONIC=0
find_app 12 -name 'pubspec.yaml' | grep . >/dev/null && IS_FLUTTER=1
# Scan EVERY package.json within depth (not just the first), so a monorepo root's tooling
# package.json never shadows a real apps/mobile/package.json deeper in the tree.
while IFS= read -r pkg; do
  grep -qE '"react-native"|"expo"' "$pkg" 2>/dev/null && IS_RN=1
  grep -qE '"@capacitor/core"|"@capacitor/ios"|"@capacitor/android"|"@ionic/(angular|react|vue)"|"cordova-android"|"cordova-ios"' "$pkg" 2>/dev/null && IS_IONIC=1
done < <(find_app 12 -name 'package.json' | grep -vE '/(node_modules|ios/Pods)/')
find_app 12 -name 'capacitor.config.*' | grep . >/dev/null && IS_IONIC=1
# config.xml alone is ambiguous (Maven/NuGet/tooling also use that filename), so require the
# Cordova widget marker before it counts as a signal.
while IFS= read -r cfg; do
  grep -qE '<widget|xmlns:cdv' "$cfg" 2>/dev/null && IS_IONIC=1
done < <(find_app 12 -name 'config.xml')

# ----- Unity, .NET MAUI, Tauri mobile, Kotlin Multiplatform (issue #837) -----
IS_UNITY=0; IS_MAUI=0; IS_TAURI=0; IS_KMP=0
find_app 6 -name 'ProjectVersion.txt' -path '*/ProjectSettings/*' | grep . >/dev/null && IS_UNITY=1
while IFS= read -r cs; do
  grep -qE '<UseMaui>[[:space:]]*true|net[0-9.]+-(ios|android|maccatalyst)' "$cs" 2>/dev/null || continue
  IS_MAUI=1
  grep -qE 'net[0-9.]+-ios' "$cs" 2>/dev/null && IS_IOS=1
  grep -qE 'net[0-9.]+-android' "$cs" 2>/dev/null && IS_AND=1
done < <(find_app 6 -name '*.csproj')
find_app 6 -name 'tauri.conf.json' -o -name 'tauri.conf.json5' -o -name 'Tauri.toml' | grep . >/dev/null && IS_TAURI=1
while IFS= read -r g; do
  grep -qE 'kotlin\("multiplatform"\)|org\.jetbrains\.kotlin\.multiplatform|kotlinMultiplatform' "$g" 2>/dev/null && { IS_KMP=1; break; }
done < <(find_app 6 -name 'build.gradle.kts' -o -name 'build.gradle' -o -name 'libs.versions.toml')
}

scan_tree() {

# ----- build a source file list, excluding vendor dirs -----
# Directories are pruned by name, and only below the project root (-mindepth 1). The old full-path
# match also hit the folders ABOVE the root, so a project sitting under a folder named build was
# scanned as empty, and it still walked every excluded tree. Test code, Python virtualenvs, and
# bundled web output (dist) never ship in the binary, and a virtualenv's vendored JSON otherwise
# reads as app source. .xcprivacy is scanned because NSPrivacyCollectedDataTypes lives there.
find "$DIR" -mindepth 1 \
  \( -type d \( -name node_modules -o -name Pods -o -name .git -o -name build -o \( -name dist -not -path '*/src/dist' \) \
    -o -name DerivedData -o -name vendor -o -name .dart_tool -o -name Carthage \
    -o -name '*Tests' -o -name androidTest -o -name __tests__ -o -name test -o -name tests \
    -o -name integration_test -o -name .venv -o -name venv -o -name site-packages -o -name .pub-cache \
    ${NESTED_PRUNE[@]+"${NESTED_PRUNE[@]}"} \) -prune \) \
  -o -type f \( \
  -name '*.swift' -o -name '*.m' -o -name '*.h' -o -name '*.kt' -o -name '*.java' \
  -o -name '*.xml' -o -name '*.plist' -o -name '*.gradle' -o -name '*.kts' \
  -o -name '*.json' -o -name '*.js' -o -name '*.jsx' -o -name '*.ts' -o -name '*.tsx' \
  -o -name '*.dart' -o -name '*.xcconfig' -o -name '*.yaml' -o -name '*.yml' \
  -o -name '*.pbxproj' -o -name '*.entitlements' -o -name '*.html' -o -name '*.xcprivacy' \
  -o -name '*.cs' -o -name '*.rs' -o -name '*.csproj' -o -name '*.xaml' -o -name '*.toml' \
  \) -print 2>/dev/null \
  > "$FILELIST" || : 2>/dev/null >> "$FILELIST" || SCAN_ERROR="the file list could not be written to $FILELIST"
build_blob
CODE_STATE=""

# ----- platform detection -----
# Every find below pipes into `grep .`, never `grep -q .`, for the reason in release_string_has:
# grep -q exits on the first match, find dies of SIGPIPE, and pipefail turns "found" into "missing".
IS_IOS=0; IS_AND=0; IS_WEB=0  # depth 12, the reach of the manifest probe. depth 4 left packages/mobile/app/ios invisible (issue #612)
find_app 12 -name '*.xcodeproj' -o -name '*.xcworkspace' -o -name 'Package.swift' -o -name 'Podfile' | grep . >/dev/null && IS_IOS=1
find_app 12 -name 'Info.plist' | grep . >/dev/null && IS_IOS=1
find_app 12 -name 'AndroidManifest.xml' -o -name 'build.gradle' -o -name 'build.gradle.kts' | grep . >/dev/null && IS_AND=1
find_app 12 -name 'package.json' -o -name 'index.html' -o -name 'webpack.config.js' -o -name 'next.config.js' | grep . >/dev/null && IS_WEB=1

# ----- cross-platform framework detection -----
# IS_IOS/IS_AND above still fire on the built artifact. This adds framework-specific checks.
detect_frameworks
# The project root and a native app split off it keep every framework the pooled tree showed, as when it was one scan (#656).
for fw in ${INHERIT_FW:-}; do
  case "$fw" in flutter) IS_FLUTTER=1 ;; rn) IS_RN=1 ;; ionic) IS_IONIC=1 ;; unity) IS_UNITY=1 ;; maui) IS_MAUI=1 ;; tauri) IS_TAURI=1 ;; kmp) IS_KMP=1 ;; esac
done
# Unity holds no Xcode or Gradle project until export. The build target names the store, with none named both are scanned.
if [ "$IS_UNITY" -eq 1 ]; then
  case "$(printf '%s' "${CMD:-}" | grep -oiE -e '-buildtarget[[:space:]]+(ios|android)' | head -1 | tr '[:upper:]' '[:lower:]')" in
    *ios) IS_IOS=1 ;; *android) IS_AND=1 ;; *) IS_IOS=1; IS_AND=1 ;;
  esac
fi

# The actual gate the framework checks below use: a committed ios/ folder AND the
# invoking command (when known) does not explicitly target Android-only.
IOS_TARGET_ACTIVE=0
[ "$IS_IOS" -eq 1 ] && [ "$CMD_TARGET_ANDROID_ONLY" -eq 0 ] && IOS_TARGET_ACTIVE=1

echo "Platforms. iOS=$IS_IOS Android=$IS_AND Web=$IS_WEB"
{ [ "$IS_IOS" -eq 1 ] || [ "$IS_AND" -eq 1 ]; } && ANY_NATIVE=1
[ "$IS_IOS" -eq 1 ] && ANY_IOS=1
[ "$IS_AND" -eq 1 ] && ANY_AND=1
[ "$IS_RN" -eq 1 ] && ANY_RN=1
# A framework app builds its native project later. Until that exists the store checks have nothing to read.
NEEDS_NATIVE=0
if [ "$IS_IOS" -eq 0 ] && [ "$IS_AND" -eq 0 ]; then
  [ "$IS_RN" -eq 1 ] && { NEEDS_NATIVE=1; NATIVE_HINT="npx expo prebuild"; }
  [ "$IS_IONIC" -eq 1 ] && { NEEDS_NATIVE=1; NATIVE_HINT="npx cap add ios or npx cap add android"; }
  [ "$IS_FLUTTER" -eq 1 ] && { NEEDS_NATIVE=1; NATIVE_HINT="flutter create --platforms ios,android ."; }
  [ "$IS_TAURI" -eq 1 ] && { NEEDS_NATIVE=1; NATIVE_HINT="cargo tauri ios init or cargo tauri android init"; }
fi
[ "$NEEDS_NATIVE" -eq 1 ] && ANY_NEEDS_NATIVE=1
[ "$IS_WEB" -eq 1 ] && ANY_WEB=1
echo "Frameworks. Flutter=$IS_FLUTTER ReactNative/Expo=$IS_RN Ionic/Capacitor/Cordova=$IS_IONIC Unity=$IS_UNITY MAUI=$IS_MAUI Tauri=$IS_TAURI KotlinMultiplatform=$IS_KMP"
[ "$IS_UNITY" -eq 1 ] && echo "Unity. No Xcode or Gradle project exists before export, so Info.plist and the Gradle settings were not read. Scan the exported project too."
[ "$IS_TAURI" -eq 1 ] && [ "$IS_IOS" -eq 0 ] && [ "$IS_AND" -eq 0 ] && echo "Tauri. No src-tauri/gen/apple or gen/android folder. Run cargo tauri ios init or cargo tauri android init before a mobile submit, then scan again."
[ "$CMD_TARGET_ANDROID_ONLY" -eq 1 ] && echo "Command targets Android only. Apple-only checks suppressed for this run."
echo ""

# ===== shared checks =====
# App Store Connect API 4.3 and 4.4 removed the old age-rating declaration endpoints. a pipeline that still calls them stops the release.
if grep_has 'appStoreVersions/[^ "]*/ageRatingDeclaration|relationships/ageRatingDeclaration'; then
  finding critical "APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED" "Pipeline calls a removed App Store Connect API age-rating endpoint" "Switch to the current age-rating declaration read and update endpoints (ASC API 4.4 release notes)." src 'appStoreVersions/[^ "]*/ageRatingDeclaration|relationships/ageRatingDeclaration'
fi
# Genuine placeholder CONTENT only. the bare word "placeholder" matches every SwiftUI
# `placeholder:` parameter and a "TODO"/"FIXME" matches normal dev comments, neither of which is a
# rejection cause, so match real placeholder markers a reviewer would actually see.
if grep_has 'lorem ipsum|example\.(com|org)|YOUR_[A-Z_]+_(KEY|HERE)|INSERT_[A-Z_]+_HERE|dummy (text|content|data)|(john|jane)@example|"Acme( Inc| Corp)?"'; then
  finding high "BOTH-PLACEHOLDER" "Placeholder content (lorem ipsum, example.com, dummy text) found in sources" "Replace placeholder text and assets with real content." src 'lorem ipsum|example\.(com|org)|YOUR_[A-Z_]+_(KEY|HERE)|INSERT_[A-Z_]+_HERE|dummy (text|content|data)|(john|jane)@example|"Acme( Inc| Corp)?"'
fi
# ROSCA and CA/NY/MA negative-option laws bind regardless of the vacated federal rule.
# "call" and "write" match as whole words only, or "renews automatically until cancelled" and
# "overwrite ... cancel" read as an instruction to call or write in.
if grep_has 'subscri(be|ption)|auto.renew|membership' && grep_has '(^|[^A-Za-z])[Cc]all[^A-Za-z].{0,24}[Cc]ancel|[Cc]ancel.{0,25}[^A-Za-z][Cc]all([^A-Za-z]|$)|[Mm]ail.{0,25}[Cc]ancel|(^|[^A-Za-z])[Ww]rite[^A-Za-z].{0,24}[Cc]ancel|[Cc]ancel.{0,15}(in.person|by.phone|by.mail)'; then
  finding high "BOTH-SUBSCRIPTION-HARD-CANCEL" "Subscription cancellation appears to require a phone call, mail, or an in-person visit" "Provide a self-service cancellation path at least as easy as sign-up (FTC Section 5, ROSCA, and CA/NY/MA negative-option laws)." src '(^|[^A-Za-z])[Cc]all[^A-Za-z].{0,24}[Cc]ancel|[Cc]ancel.{0,25}[^A-Za-z][Cc]all([^A-Za-z]|$)|[Mm]ail.{0,25}[Cc]ancel|(^|[^A-Za-z])[Ww]rite[^A-Za-z].{0,24}[Cc]ancel|[Cc]ancel.{0,15}(in.person|by.phone|by.mail)'
fi
# fastlane precheck derived metadata checks
if grep_has 'coming soon|coming-soon|will be available|in a future update|stay tuned'; then
  finding medium "APPLE-2.3-FUTURE-FUNCTIONALITY" "Future functionality language found (coming soon, beta)" "Describe only what the build does today (fastlane precheck future_functionality, Apple 2.3.1)." src 'coming soon|coming-soon|will be available|in a future update|stay tuned'
fi
if grep_has 'iOS bug|apple bug|broken on iOS'; then
  finding medium "APPLE-2.3-NEGATIVE-APPLE-SENTIMENT" "Negative Apple or iOS bug reference in copy" "Remove negative references to Apple and iOS bugs (fastlane precheck negative_apple_sentiment)." src 'iOS bug|apple bug|broken on iOS'
fi
if grep_has 'loot ?box|gacha|mystery box|random reward'; then
  finding high "BOTH-LOOTBOX-ODDS" "Random reward mechanic present" "Disclose the odds for every random reward before purchase (Apple 3.1.1, Google gambling)." src 'loot ?box|gacha|mystery box|random reward'
fi

# ===== Flutter checks =====
# iOS-only Apple requirement, gated on IS_IOS so an Android-only build is never blocked for it.
if [ "$IS_FLUTTER" -eq 1 ]; then
  if [ "$IOS_TARGET_ACTIVE" -eq 1 ] && grep_has 'permission_handler|image_picker|geolocator|device_info_plus|package_info_plus|shared_preferences|sqflite|firebase_'; then
    if ! own_privacy_manifest; then
      finding critical "FLUTTER-PRIVACY-MANIFEST-MISSING" "Flutter plugins that touch required-reason APIs but no PrivacyInfo.xcprivacy anywhere in the project" "Add an app-level PrivacyInfo.xcprivacy AND confirm each Flutter plugin ships its own (permission_handler, image_picker, and most first-party plugins added theirs from Flutter 3.19+). A missing plugin-level manifest is invisible to Apple's aggregator unless the app manifest also declares that plugin's reason codes. This check only runs against an iOS target."
    fi
  fi
  if [ "$IS_IOS" -eq 0 ]; then
    finding medium "FLUTTER-NO-IOS-RUNNER-FOUND" "No ios/Runner target detected next to pubspec.yaml" "If this is an iOS submission, run flutter create . or confirm the ios/ platform folder exists. A pure Android build never needs one."
  fi
fi

# ===== React Native / Expo checks =====
# Both findings are Apple-specific (3.3.2/2.5.2 disclosure, iOS privacy manifest), IS_IOS-gated.
if [ "$IS_RN" -eq 1 ] && [ "$IOS_TARGET_ACTIVE" -eq 1 ]; then
  if grep_has 'react-native-code-push|CodePush\.|expo-updates|Updates\.checkForUpdate|react-native-ota-hot-update|@stallion-js|Stallion\.'; then
    if ! grep_has 'reviewNotes|App Review|bug.fix.only|bugfix.only'; then
      finding high "RN-OTA-UNDECLARED" "An over-the-air JS bundle updater (CodePush, Expo Updates, or similar) is present" "Disclose the OTA mechanism by name in App Review notes, restrict its use to bug fixes that do not change the app's purpose, UI, or add features beyond what was reviewed (Apple 3.3.2, 2.5.2)." src 'react-native-code-push|CodePush\.|expo-updates|Updates\.checkForUpdate|react-native-ota-hot-update|@stallion-js|Stallion\.'
    fi
  fi
  if grep_has 'Firebase|@react-native-firebase|expo-file-system|expo-application|AsyncStorage|@react-native-async-storage'; then
    if ! own_privacy_manifest; then
      finding critical "RN-PRIVACY-MANIFEST-MISSING" "React Native native modules that touch required-reason APIs but no PrivacyInfo.xcprivacy anywhere" "Add an app-level PrivacyInfo.xcprivacy. Native modules bundled transitively via JS deps (analytics, storage, device-info libraries) each need their own manifest aggregated in the final IPA; this is easy to miss because the dependency is JS-side." src 'Firebase|@react-native-firebase|expo-file-system|expo-application|AsyncStorage|@react-native-async-storage'
    fi
  fi
fi

# ===== Managed Expo app config, read when no ios or android folder exists yet =====
# EAS builds the native folders in the cloud, so the config is all there is to read. Native code stays NOT CHECKED.
if [ "$IS_RN" -eq 1 ] && [ "$NEEDS_NATIVE" -eq 1 ]; then
  EXPO_CFG=()
  for f in "$DIR/app.json" "$DIR/app.config.js" "$DIR/app.config.ts" "$DIR/app.config.mjs" "$DIR/app.config.cjs"; do
    if [ -f "$f" ]; then EXPO_CFG+=("$f"); fi
  done
  if [ "${#EXPO_CFG[@]}" -gt 0 ]; then
    EXPO_READ=1
    echo "Expo config. No ios or android folder, so only the app config was read for store checks."
    ex_cfg() { grep -Eqs -e "$1" "${EXPO_CFG[@]}"; }
    ex_dep() { grep -Eqs -e "$1" "$DIR/package.json" "${EXPO_CFG[@]}"; }
    if [ "$CMD_TARGET_ANDROID_ONLY" -eq 0 ]; then
      if ex_dep '"(expo-camera|expo-image-picker|expo-barcode-scanner|react-native-vision-camera)"' && ! ex_cfg 'NSCameraUsageDescription|cameraPermission'; then
        finding high "APPLE-5.1.1-MISSING-USAGE-DESCRIPTION" "Camera module in the Expo app with no camera purpose string in the app config" "Set ios.infoPlist.NSCameraUsageDescription, or the plugin cameraPermission option, to a specific reason. The generic plugin default is a common 5.1.1 rejection."
      fi
      if ex_dep '"(expo-location|react-native-geolocation-service|@react-native-community/geolocation)"' && ! ex_cfg 'NSLocation[A-Za-z]*UsageDescription|location(WhenInUse|AlwaysAndWhenInUse|Always)Permission'; then
        finding high "APPLE-5.1.1-MISSING-USAGE-DESCRIPTION" "Location module in the Expo app with no location purpose string in the app config" "Set ios.infoPlist.NSLocationWhenInUseUsageDescription, or the plugin locationWhenInUsePermission option, to a specific reason."
      fi
      if ex_dep '"(@react-native-async-storage/async-storage|expo-file-system|expo-application|@react-native-firebase/[a-z-]+)"' && ! ex_cfg 'privacyManifests'; then
        finding medium "RN-PRIVACY-MANIFEST-MISSING" "Required-reason modules installed but the Expo app config sets no ios.privacyManifests" "Declare the accessed API categories and reasons under ios.privacyManifests, so the manifest EAS generates carries them."
      fi
    fi
    if [ "$CMD_TARGET_IOS_ONLY" -eq 0 ]; then
      # Only the permissions array counts. blockedPermissions removes a permission, it never adds one.
      EX_PERMS="$(cat "${EXPO_CFG[@]}" 2>/dev/null | tr -d '\n\r' | grep -oE "(^|[^A-Za-z])[\"']?permissions[\"']?[[:space:]]*:[[:space:]]*\\[[^]]*\\]")"
      # A JS or TS config may quote a key either way, or not at all.
      if printf '%s' "$EX_PERMS" | grep -q 'ACCESS_BACKGROUND_LOCATION' || ex_cfg "isAndroidBackgroundLocationEnabled[\"']?[[:space:]]*:[[:space:]]*true"; then
        finding critical "GOOGLE-PERM-BACKGROUND-LOCATION" "Background location requested in the Expo app config" "Justify with a core feature and prominent disclosure, or use foreground location."
      fi
      if printf '%s' "$EX_PERMS" | grep -qE 'READ_SMS|SEND_SMS|RECEIVE_SMS|READ_CALL_LOG|WRITE_CALL_LOG'; then
        finding critical "GOOGLE-PERM-SMS-CALLLOG" "SMS or Call Log permission in the Expo app config" "Use the permissions declaration for an approved core use case, or drop it."
      fi
      if printf '%s' "$EX_PERMS" | grep -q 'MANAGE_EXTERNAL_STORAGE'; then
        finding critical "GOOGLE-PERM-ALL-FILES" "All files access in the Expo app config" "Use scoped storage. Request all files access only for a qualifying use case."
      fi
    fi
  fi
fi

# ===== Ionic / Capacitor / Cordova checks =====
# All three are Apple-side (4.2, UIWebView, iOS privacy manifest), IS_IOS-gated as above.
if [ "$IS_IONIC" -eq 1 ] && [ "$IOS_TARGET_ACTIVE" -eq 1 ]; then
  WRAPPER_COUNT="$( [ -s "$FILELIST" ] && tr '\n' '\0' < "$FILELIST" | xargs -0 grep -EIl -e 'WKWebView|loadRequest|Capacitor|Cordova' 2>/dev/null | wc -l | tr -d '[:space:]' || echo 0)"
  NATIVE_PLUGIN_COUNT="$( [ -s "$FILELIST" ] && tr '\n' '\0' < "$FILELIST" | xargs -0 grep -EIho -e '@capacitor/(push-notifications|status-bar|splash-screen|haptics|share|camera|local-notifications)|cordova-plugin-(statusbar|splashscreen|push)' 2>/dev/null | sort -u | wc -l | tr -d '[:space:]' || echo 0)"
  if [ "${WRAPPER_COUNT:-0}" -gt 0 ] && [ "${NATIVE_PLUGIN_COUNT:-0}" -lt 2 ]; then
    finding high "IONIC-4.2-THIN-WRAPPER" "WebView/Capacitor/Cordova present with fewer than 2 recognized native-feel plugins (status bar, splash screen, push, haptics)" "This is a heuristic proxy, not the actual Apple 4.2 test (features/content/UI beyond a repackaged website); review manually before treating it as a hard blocker. Add native Capacitor/Cordova plugins for status bar, splash transition, push, and haptics, or ship as an installable PWA to skip App Review entirely."
  fi
  if grep_has 'UIWebView'; then
    finding critical "IONIC-UIWEBVIEW-DEPRECATED" "Deprecated UIWebView symbol referenced (directly or via a stale plugin)" "Apple auto-rejects (ITMS-90809) any binary statically linking UIWebView. Update every Capacitor/Cordova plugin to a version using WKWebView; a stale plugin can pull this in even when app code never references it." src 'UIWebView'
  fi
  if grep_has '@capacitor/|Capacitor\.'; then
    if ! own_privacy_manifest; then
      finding high "IONIC-PRIVACY-MANIFEST-MISSING" "Capacitor/Cordova plugins present but no PrivacyInfo.xcprivacy" "Capacitor plugin manifest support is less standardized than Flutter's; verify each plugin wrapping a native SDK (camera, geolocation, ads) ships PrivacyInfo.xcprivacy, and add the app-level one." src '@capacitor/|Capacitor\.'
    fi
  fi
fi

# ===== iOS checks =====
# Gated like the framework checks, so an Android-only command never meets an Apple finding.
if [ "$IOS_TARGET_ACTIVE" -eq 1 ]; then
  if release_string_has 'localhost|127\.0\.0\.1|staging\.[a-z]|ngrok\.io'; then
    finding critical "APPLE-2.1-STAGING-BACKEND" "A release-build string points at localhost or a staging host" "Point the release build at the live production backend. A localhost/staging URL inside #if DEBUG or a comment is fine. this only flags strings the release build actually compiles." src 'localhost|127\.0\.0\.1|staging\.[a-z]|ngrok\.io'
  fi
  if grep_has 'signIn|logIn|LoginView|OAuth|FirebaseAuth|createAccount|signUp'; then
    if ! impl_has 'deleteAccount|delete_account|account deletion|deleteUser'; then
      finding critical "APPLE-5.1.1-NO-ACCOUNT-DELETION" "Account creation found but no in app account deletion" "Add an in app account deletion flow (Apple 5.1.1(v))." src 'signIn|logIn|LoginView|OAuth|FirebaseAuth|createAccount|signUp'
    fi
  fi
  if code_has 'AVCaptureDevice|UIImagePickerController'; then
    config_has 'NSCameraUsageDescription' || finding critical "APPLE-5.1.1-MISSING-USAGE-DESCRIPTION" "Camera used without NSCameraUsageDescription" "Add NSCameraUsageDescription with a specific reason." src 'AVCaptureDevice|UIImagePickerController'
  fi
  if code_has 'CLLocationManager'; then
    config_has 'NSLocation.*UsageDescription' || finding critical "APPLE-5.1.1-MISSING-USAGE-DESCRIPTION" "Location used without a location usage description" "Add the matching NSLocation usage description with a specific reason." src 'CLLocationManager'
  fi
  if code_has 'PHPhotoLibrary'; then
    config_has 'NSPhotoLibrary.*UsageDescription' || finding high "APPLE-5.1.1-MISSING-USAGE-DESCRIPTION" "Photos used without a photo library usage description" "Add NSPhotoLibraryUsageDescription with a specific reason." src 'PHPhotoLibrary'
  fi
  if code_has 'CNContactStore'; then
    config_has 'NSContactsUsageDescription' || finding high "APPLE-5.1.1-MISSING-USAGE-DESCRIPTION" "Contacts used without NSContactsUsageDescription" "Add NSContactsUsageDescription with a specific reason." src 'CNContactStore'
  fi
  if grep_has 'FacebookLogin|GoogleSignIn|GIDSignIn|LoginWithFacebook'; then
    grep_has 'SignInWithApple|ASAuthorizationAppleIDProvider' || finding high "APPLE-4.8-SOCIAL-LOGIN-ONLY" "Third party social login without Sign in with Apple" "Add Sign in with Apple or an equal privacy preserving login (Apple 4.8)." src 'FacebookLogin|GoogleSignIn|GIDSignIn|LoginWithFacebook'
  fi
  # Hide My Email relay addresses now also come from private.icloud.com (Apple news 1ptvdtcm, corrected 24 Aug 2026).
  if grep_has 'privaterelay\.appleid\.com' && ! grep_has 'private\.icloud\.com'; then
    finding critical "APPLE-4.0-SIWA-RELAY-DOMAIN" "Sign in with Apple relay allowlist accepts only privaterelay.appleid.com" "Accept private.icloud.com as well, everywhere relay addresses are validated or allowlisted." src 'privaterelay\.appleid\.com'
  fi
  # Age assurance. a parent can withdraw consent, Apple then blocks launch. the app must handle RESCIND_CONSENT.
  if grep_has 'DeclaredAgeRange|AgeRangeService' && ! grep_has 'RESCIND_CONSENT|rescindConsent'; then
    finding high "APPLE-5.1.1-RESCIND-CONSENT-UNHANDLED" "Declared Age Range used without RESCIND_CONSENT handling" "Handle the RESCIND_CONSENT server notification, revoke the minor session and consent-scoped data, and build with the iOS 26.2 SDK or later." src 'DeclaredAgeRange|AgeRangeService'
  fi
  # The no-entitlement external purchase link is a US-storefront carve-out only. everywhere else it is still 3.1.1.
  if grep_has 'ExternalPurchaseLink|external-purchase-link|openExternalPurchaseLink' && ! grep_has 'Storefront|storefront|countryCode'; then
    finding high "APPLE-3.1.1-EXTERNAL-LINK-REGION-GATING" "External purchase link is not gated on the storefront" "Show the link only on the US storefront (or where you hold the entitlement). gate on Storefront.current or countryCode." src 'ExternalPurchaseLink|external-purchase-link|openExternalPurchaseLink'
  fi
  # On-Demand Resources are deprecated from the 27 OS family (WWDC26).
  if grep_has 'NSBundleResourceRequest|OnDemandResources|on-demand-resource'; then
    finding high "APPLE-ODR-DEPRECATED-27" "On-Demand Resources in use, deprecated starting iOS 27" "Migrate tagged resources to the Background Assets framework." src 'NSBundleResourceRequest|OnDemandResources|on-demand-resource'
  fi
  # Since September 2026 the social media capability question gates every submission (Apple news 0d2gpmml).
  if grep_has 'newsFeed|NewsFeed|followers|chatRoom|ChatRoom|DirectMessage|liveStream|LiveStream'; then
    finding medium "APPLE-2.3.6-SOCIAL-MEDIA-DECLARATION" "Social features detected, confirm the social media capability declaration in App Store Connect" "Answer the social media question before submitting. it sets a 13+ minimum and requires Declared Age Range for under-13 users." src 'newsFeed|NewsFeed|followers|chatRoom|ChatRoom|DirectMessage|liveStream|LiveStream'
  fi
  # Match the tracking SDKs by their own type names / imports, never the bare words "Adjust" or
  # "Branch", which collide with ordinary English ("Adjust times", a git branch) and false-flag a
  # tracking SDK that is not present.
  if grep_has 'AppsFlyerLib|import AppsFlyer|AdjustConfig|AdjustEvent|import Adjust[^A-Za-z]|BranchEvent|BranchUniversalObject|import Branch[^A-Za-z]|FBSDKCoreKit|FBSDKLogin|ASIdentifierManager|advertisingIdentifier'; then
    ATT_MISS=""
    config_has 'NSUserTrackingUsageDescription|userTrackingPermission' || ATT_MISS="NSUserTrackingUsageDescription in Info.plist or the build settings"
    impl_has 'requestTrackingAuthorization|requestTrackingPermission' || ATT_MISS="${ATT_MISS:+$ATT_MISS and }the ATTrackingManager.requestTrackingAuthorization call"
    [ -z "$ATT_MISS" ] || finding high "APPLE-5.1.2-MISSING-ATT" "Tracking SDK without App Tracking Transparency, missing $ATT_MISS" "Call the ATT prompt and add NSUserTrackingUsageDescription, both are required (Apple 5.1.2)." src 'AppsFlyerLib|import AppsFlyer|AdjustConfig|AdjustEvent|import Adjust[^A-Za-z]|BranchEvent|BranchUniversalObject|import Branch[^A-Za-z]|FBSDKCoreKit|FBSDKLogin|ASIdentifierManager|advertisingIdentifier'
  fi
  if grep_has 'Stripe|PayPalCheckout|braintree|razorpay'; then
    grep_has "StoreKit|SKProduct|Product\.purchase|$XPLAT_IAP" || finding critical "APPLE-3.1.1-EXTERNAL-PAYMENT" "External payment SDK without StoreKit" "Route digital goods through in app purchase unless the app is a documented exempt category (Apple 3.1.1)." src 'Stripe|PayPalCheckout|braintree|razorpay'
  fi
  if grep_has 'api\.openai\.com|anthropic|generativelanguage|chat/completions'; then
    finding medium "APPLE-5.1.2-AI-NO-CONSENT-MODAL" "Third party AI integration detected" "If personal data is sent, show a consent modal naming the AI provider and data types (Apple 5.1.2)." src 'api\.openai\.com|anthropic|generativelanguage|chat/completions'
  fi
  if ! grep_has 'privacyPolicy|privacy-policy|PrivacyPolicy'; then
    finding high "APPLE-5.1.1-MISSING-PRIVACY-POLICY" "No privacy policy reference found in sources" "Publish a privacy policy, link it in App Store Connect, and reach it from inside the app."
  fi
  if grep_has 'UserDefaults\.standard'; then
    if grep_has 'token|password|credential|secret|jwt' && ! grep_has 'Keychain|SecItemAdd|SecItemUpdate'; then
      finding high "BOTH-SECURE-STORAGE" "Plain UserDefaults storage is used for sensitive credentials" "Store access tokens and sensitive credentials in iOS Keychain instead." src 'token|password|credential|secret|jwt'
    fi
  fi
  if grep_has 'CFBundleURLSchemes'; then
    if ! grep_has 'apple-app-site-association'; then
      finding high "BOTH-UNSAFE-DEEPLINK" "Custom URL deep link schemes declared without Universal Links configuration" "Configure Universal Links (iOS) using apple-app-site-association verification to prevent URL hijacking." src 'CFBundleURLSchemes'
    fi
  fi
  # Privacy manifest, the top modern Apple upload rejection since 2024
  if grep_has 'Firebase|Alamofire|UserDefaults|systemUptime|FileManager\.default|ProcessInfo'; then
    if ! own_privacy_manifest; then
      finding critical "APPLE-PRIVACY-MANIFEST-MISSING" "Required reason APIs or SDKs present but no PrivacyInfo.xcprivacy" "Add a privacy manifest with approved reason codes and tracking domains, and confirm each SDK ships its signed manifest." src 'Firebase|Alamofire|UserDefaults|systemUptime|FileManager\.default|ProcessInfo'
    fi
  fi

  # A manifest that exists can still be internally inconsistent. Apple validates
  # these keys at upload and rejects by email (ITMS-91xxx) after processing, so
  # the binary installs from TestFlight and is still barred from review.
  MANIFEST_VALIDATOR=""
  for candidate in \
    "$(dirname "$0")/../../scripts/validate-privacy-manifest.py" \
    "$(dirname "$0")/../skills/app-store-compliance/scripts/validate-privacy-manifest.py" \
    "${HOME:-}/.claude/skills/app-store-compliance/scripts/validate-privacy-manifest.py" \
    "${HOME:-}/.agents/skills/app-store-compliance/scripts/validate-privacy-manifest.py"; do
    [ -f "$candidate" ] && { MANIFEST_VALIDATOR="$candidate"; break; }
  done
  if [ -n "$MANIFEST_VALIDATOR" ] && command -v python3 >/dev/null 2>&1; then
    # Same exclusions as the source file list. A pod's manifest is the vendor's job, a Tests fixture never ships.
    : > "$FILELIST.manifest" 2>/dev/null || SCAN_ERROR="the privacy manifest results could not be written to $FILELIST.manifest"
    find "$DIR" -mindepth 1 \
      \( -type d \( -name node_modules -o -name Pods -o -name .git -o -name build -o \( -name dist -not -path '*/src/dist' \) \
        -o -name DerivedData -o -name vendor -o -name .dart_tool -o -name Carthage \
        -o -name '*Tests' -o -name androidTest -o -name __tests__ -o -name test -o -name tests \
        -o -name integration_test -o -name .venv -o -name venv -o -name site-packages -o -name .pub-cache \
      ${NESTED_PRUNE[@]+"${NESTED_PRUNE[@]}"} \) -prune \) \
      -o -name 'PrivacyInfo.xcprivacy' -print 2>/dev/null \
      | while IFS= read -r manifest; do
          python3 "$MANIFEST_VALIDATOR" "$manifest" 2>/dev/null
        done > "$FILELIST.manifest" 2>/dev/null || true
    if [ -s "$FILELIST.manifest" ]; then
      while IFS="$(printf '\t')" read -r sev id msg; do
        [ -n "$id" ] || continue
        finding "$sev" "$id" "$msg" "Correct the privacy manifest so its keys agree, then rebuild. Reference. https://developer.apple.com/documentation/bundleresources/privacy_manifest_files"
      done < "$FILELIST.manifest"
    fi
    rm -f "$FILELIST.manifest" 2>/dev/null || true
  elif find_app 12 -name 'PrivacyInfo.xcprivacy' | grep . >/dev/null; then
    finding medium "APPLE-MANIFEST-VALIDATOR-UNAVAILABLE" "Privacy manifests present but python3 or scripts/validate-privacy-manifest.py is missing, so their internals were not validated" "Install python3 and keep scripts/validate-privacy-manifest.py next to the guard, or run plutil -lint on each manifest by hand."
  fi
  [ "$IS_UNITY" -eq 1 ] || grep_has 'ITSAppUsesNonExemptEncryption' || finding high "APPLE-EXPORT-COMPLIANCE-MISSING" "ITSAppUsesNonExemptEncryption not set" "Set it in Info.plist or the build stalls in Missing Compliance and never reaches review."
  # Native StoreKit keeps the original restore list. A plugin's own restore call only counts for a plugin app.
  RESTORE_RE='restorePurchases|restoreCompletedTransactions|AppStore\.sync|Restore Purchases'
  grep_has 'SKProduct|Product\.purchase|StoreKit' || RESTORE_RE="$RESTORE_RE|RestorePurchases|restoreTransactions|RestoreTransactions|getAvailablePurchases|queryPastPurchases"
  if grep_has "SKProduct|Product\\.purchase|StoreKit|$XPLAT_IAP"; then
    grep_has "$RESTORE_RE" || finding high "APPLE-RESTORE-PURCHASES-MISSING" "In-app purchases without a Restore Purchases control" "Add a visible Restore Purchases control. Required for non consumables." src "SKProduct|Product\\.purchase|StoreKit|$XPLAT_IAP"
  fi
  if grep_has 'deleteAccount|delete account'; then
    grep_has 'mailto:|deactivate' && finding high "APPLE-ACCOUNT-DELETION-WEAK" "Account removal may be deactivate or mailto only" "Provide genuine in app deletion of the account and its data, not a deactivate or external form." src 'mailto:|deactivate'
  fi
  if grep_has 'fixed-odds|betting'; then
    finding critical "APPLE-GAMBLING-BRAZIL-LICENSE" "Fixed-odds or betting keyword detected in sources" "Provide a valid fixed-odds betting license from the Secretariat of Prizes and Bets (SPA) in App Review Info, set age rating to A18, and submit a new version to trigger verification (Apple policy May 8, 2026)." src 'fixed-odds|betting'
  fi
  if grep_has 'Image\('; then
    if ! grep_has 'accessibilityLabel|accessibilityIdentifier|accessibilityHidden|accessibilityElement'; then
      finding medium "APPLE-ACCESSIBILITY-VOICEOVER" "SwiftUI Image or UIKit component without VoiceOver accessibility attribute" "Provide an accessibilityLabel or use decorative initializers (Apple Design - Accessibility)." src 'Image\('
    fi
  fi
  if grep_has '\.system\(size:'; then
    finding medium "APPLE-ACCESSIBILITY-DYNAMICTYPE" "Hardcoded system font size detected" "Use relative SwiftUI font styles or preferredFont APIs to support Dynamic Type (Apple Design - Accessibility)." src '\.system\(size:'
  fi
  if grep_has 'withAnimation|UIView\.animate'; then
    if ! grep_has 'isReduceMotionEnabled|accessibilityReduceMotion'; then
      finding medium "APPLE-ACCESSIBILITY-REDUCEMOTION" "Animations implemented without checking Reduce Motion" "Respect the Reduce Motion accessibility setting before executing complex custom animations (Apple Design - Accessibility)." src 'withAnimation|UIView\.animate'
    fi
  fi
  if grep_has 'UIColor\(\s*red:'; then
    if ! grep_has 'isDarkerSystemColorsEnabled|darkerSystemColors'; then
      finding medium "APPLE-ACCESSIBILITY-COLORCONTRAST" "Raw RGB UIColor without system dynamic color or high contrast checks" "Utilize dynamic named asset colors or check isDarkerSystemColorsEnabled (Apple Design - Accessibility)." src 'UIColor\(\s*red:'
    fi
  fi
  if grep_has 'onTapGesture|Button'; then
    if ! grep_has 'FeedbackGenerator|CoreHaptics'; then
      finding medium "APPLE-ACCESSIBILITY-HAPTICS" "Taps or button interactions without tactile feedback" "Integrate haptic feedback generators to improve interaction accessibility (Apple Design - Accessibility)." src 'onTapGesture|Button'
    fi
  fi
  if grep_has 'focusable'; then
    if ! grep_has 'FocusState|focused'; then
      finding medium "APPLE-ACCESSIBILITY-KEYBOARD" "Focusable controls declared without focus state tracking" "Support physical keyboards with FocusState tracking (Apple Design - Accessibility)." src 'focusable'
    fi
  fi
  finding medium "APPLE-2.3-AGE-RATING-2026" "Verify the 2026 age rating questionnaire" "Answer the updated age rating questions (13 plus, 16 plus, 18 plus) in App Store Connect."
  if grep_has 'email|phoneNumber|userName|location|coordinates'; then
    if ! grep_has 'NSPrivacyCollectedDataTypes|privacyNutritionLabels|privacy-nutrition-labels'; then
      finding high "APPLE-PRIVACY-NUTRITION-LABELS" "Missing Privacy Nutrition Labels data type declarations" "Update the app privacy manifest (PrivacyInfo.xcprivacy) with NSPrivacyCollectedDataTypes and complete corresponding Nutrition Labels in App Store Connect." src 'email|phoneNumber|userName|location|coordinates'
    fi
  fi
fi

# ===== Android checks =====
if [ "$IS_AND" -eq 1 ]; then
  if grep_has 'ACCESS_BACKGROUND_LOCATION'; then
    finding critical "GOOGLE-PERM-BACKGROUND-LOCATION" "Background location permission declared" "Justify with a core feature and prominent disclosure, or use foreground location." src 'ACCESS_BACKGROUND_LOCATION'
  fi
  if grep_has 'MANAGE_EXTERNAL_STORAGE'; then
    finding critical "GOOGLE-PERM-ALL-FILES" "All files access declared" "Use scoped storage. Request all files access only for a qualifying use case." src 'MANAGE_EXTERNAL_STORAGE'
  fi
  if grep_has 'android\.permission\.(READ_SMS|SEND_SMS|RECEIVE_SMS|READ_CALL_LOG|WRITE_CALL_LOG)'; then
    finding critical "GOOGLE-PERM-SMS-CALLLOG" "SMS or Call Log permission declared" "Use the permissions declaration for an approved core use case, or drop it." src 'android\.permission\.(READ_SMS|SEND_SMS|RECEIVE_SMS|READ_CALL_LOG|WRITE_CALL_LOG)'
  fi
  if grep_has 'BIND_ACCESSIBILITY_SERVICE|AccessibilityService'; then
    finding critical "GOOGLE-PERM-ACCESSIBILITY-MISUSE" "AccessibilityService present" "Use it only for genuine accessibility and declare the use, or remove it." src 'BIND_ACCESSIBILITY_SERVICE|AccessibilityService'
  fi
  if grep_has 'Stripe|PayPal|braintree|razorpay'; then
    grep_has "BillingClient|com\.android\.billingclient|$XPLAT_IAP" || finding critical "GOOGLE-PLAY-BILLING" "External payment without Play Billing" "Use Play Billing for in app digital goods." src 'Stripe|PayPal|braintree|razorpay'
  fi
  # Payments policy exception is literal. only a tax-exempt charity may take donations outside Play
  # billing (AnkiDroid, August 2026). A donate link to a funding platform is a Payments violation.
  if grep_has 'opencollective\.com|ko-fi\.com|patreon\.com|buymeacoffee\.com|github\.com/sponsors|liberapay\.com|paypal\.com/donate'; then
    finding high "GOOGLE-PAYMENTS-DONATION-LINK" "In-app donation link to a payment page outside Play billing" "Remove the donation entry point from the Play build or sell it through Play billing. Only a tax-exempt charity (501(c)(3)-class) may bypass Play billing, Google rejects 501(c)(6) and unincorporated projects (Payments policy)." src 'opencollective\.com|ko-fi\.com|patreon\.com|buymeacoffee\.com|github\.com/sponsors|liberapay\.com|paypal\.com/donate'
  fi
  # Since 3 August 2026 the developer bears chargeback costs. An app on Play billing that never
  # handles the refund-review notification loses every fraudulent dispute by default.
  # New apps and updates need Play Billing Library 8 or later since 31 August 2026 (deprecation ladder, extension to 1 November 2026).
  BILLING_MAJOR="$(grep -E '/build\.gradle(\.kts)?$' "$FILELIST" | tr '\n' '\0' | xargs -0 grep -hoE 'com\.android\.billingclient:billing(-ktx)?:[0-9]+' 2>/dev/null | grep -oE '[0-9]+$' | sort -n | tail -1)"
  if [ -n "$BILLING_MAJOR" ] && [ "$BILLING_MAJOR" -lt 8 ]; then
    finding critical "GOOGLE-PLAY-BILLING-V8-REQUIRED" "Play Billing Library $BILLING_MAJOR.x, new apps and updates need version 8 or later since 31 August 2026" "Upgrade com.android.billingclient:billing to 8.x, or request the Play Console extension available until 1 November 2026." src 'billingclient'
  fi
  if grep_has 'BillingClient|com\.android\.billingclient'; then
    grep_has 'PendingRefundReviewNotification|[Rr]eview[Rr]efund' || finding medium "GOOGLE-PLAY-CHARGEBACK-LIABILITY" "Play billing without chargeback dispute handling" "Handle PendingRefundReviewNotification and call the Review Refund API within 24 hours with the refund preference and usage evidence (Play Console Help answer 17068375)." src 'BillingClient|com\.android\.billingclient'
  fi
  # From 30 September 2026 regulated categories must publish from an organization account with a D-U-N-S number.
  if grep_has 'VpnService|HealthConnect|health\.connect|BankAccount|cryptocurrency'; then
    finding high "GOOGLE-ORG-REGISTRATION-REQUIRED" "Regulated-category signals (VPN, health, finance), organization account required from 30 Sep 2026" "Publish from an organization account with a D-U-N-S number matching the Dun and Bradstreet profile (Play Console Help 10788890)." src 'VpnService|HealthConnect|health\.connect|BankAccount|cryptocurrency'
  fi
  # Geofencing is no longer an approved foreground-service use case for API 37 targets (Play Console Help 16965181).
  if grep_has 'FOREGROUND_SERVICE_LOCATION' && grep_has '[Gg]eofenc'; then
    finding high "GOOGLE-FGS-GEOFENCE-REMOVED" "Foreground service used for geofencing" "Move to the Geofence API (GeofencingClient) and drop FOREGROUND_SERVICE_LOCATION if geofencing was its only use." src '[Gg]eofenc'
  fi
  # Random or anonymous chat is now in scope of Age-Restricted, Families, and Child Safety Standards (26 Aug 2026).
  if grep_has '[Rr]andom chat|[Aa]nonymous chat|chat with strangers|Omegle' && ! grep_has 'ageGate|minorBlock|csae'; then
    finding critical "GOOGLE-ANON-CHAT-MINOR-BLOCK" "Random or anonymous chat without minor blocking and child-safety standards" "Enable Play Console minor blocking, exclude children from the target audience, publish CSAE standards, add in-app reporting and a child-safety contact." src '[Rr]andom chat|[Aa]nonymous chat|chat with strangers|Omegle'
  fi
  # Generative image or video apps need NCII controls and a full-access test account (Android Developers Blog, 25 Aug 2026).
  if grep_has 'generateImage|imageGeneration|text-to-image|faceSwap|stable-diffusion' && ! grep_has '[Mm]oderation|safetyClassifier|contentFilter'; then
    finding high "GOOGLE-GENAI-NCII-CONTROLS" "Generative image or video feature without moderation controls" "Add input and output moderation for intimate and deepfake content, document tested safety prompts, and give the reviewer a full-access test account." src 'generateImage|imageGeneration|text-to-image|faceSwap|stable-diffusion'
  fi
  # From February 2027 release builds must be R8-optimized (25 percent minimum coverage, Play Console Help 17492799).
  R8_ON=0
  while IFS= read -r g; do
    grep -qE '(isMinifyEnabled|minifyEnabled)[[:space:]=]+true' "$g" 2>/dev/null && { R8_ON=1; break; }
  done < <(find_tree -type f \( -name '*.gradle' -o -name '*.kts' \) -print)
  if [ "$R8_ON" -eq 0 ] && [ "$IS_UNITY" -eq 0 ] && [ "$IS_MAUI" -eq 0 ]; then
    finding high "ANDROID-R8-OPTIMIZATION-MISSING" "No release build type with minifyEnabled true" "Enable R8 (isMinifyEnabled = true, isShrinkResources = true) in the release build type before February 2027."
  fi
  # From April 2027 sign-in apps must restore sign-in state on a new device (Restore Credentials API).
  if grep_has 'signInWith|CredentialManager|FirebaseAuth|LoginActivity' && ! grep_has 'RestoreCredential'; then
    finding medium "ANDROID-RESTORE-CREDENTIALS-REQUIRED" "Sign-in present without Restore Credentials integration" "Create a restore credential on sign-in and restore it after device transfer (Play technical quality requirement, April 2027)." src 'signInWith|CredentialManager|FirebaseAuth|LoginActivity'
  fi
  if grep_has 'firebase-analytics|com\.google\.android\.gms\.ads|appsflyer|com\.adjust|com\.facebook'; then
    finding high "GOOGLE-DATASAFETY-MISMATCH" "Analytics or ad SDK present. Verify the Data Safety form" "Declare every collection and sharing accurately. Data Safety mismatch is the top Google rejection." src 'firebase-analytics|com\.google\.android\.gms\.ads|appsflyer|com\.adjust|com\.facebook'
  fi
  if ! grep_has 'privacyPolicy|privacy-policy'; then
    finding high "GOOGLE-MISSING-PRIVACY-POLICY" "No privacy policy reference found" "Publish a privacy policy and set its URL in the Play Console store listing."
  fi
  # Every build.gradle in the source list. A bare ** glob without globstar only saw one directory level, so
  # android/app/build.gradle was never read. Play rejects new apps and updates below API 36 since 31 August 2026.
  TSDK="$(grep -E '/build\.gradle(\.kts)?$' "$FILELIST" | tr '\n' '\0' | xargs -0 grep -hoE 'targetSdk(Version)?[[:space:]=]+[0-9]+' 2>/dev/null | grep -oE '[0-9]+' | sort -n | tail -1)"
  if [ -n "$TSDK" ] && [ "$TSDK" -lt 36 ]; then
    finding critical "GOOGLE-TARGET-API" "targetSdk is $TSDK, below the API 36 floor Play enforces for new apps and updates since 31 August 2026" "Target API 36 or higher (Wear OS and Automotive 35, TV and XR 34), or request the Play Console extension available until 1 November 2026." src 'targetSdk'
  fi
  # Android 17 (API 37) targets. contacts picker, location button scope, and local network permission (27 Jan 2027).
  if [ -n "$TSDK" ] && [ "$TSDK" -ge 37 ] 2>/dev/null; then
    if grep_has 'READ_CONTACTS' && ! grep_has 'ACTION_PICK|ContactPicker'; then
      finding high "GOOGLE-CONTACTS-PICKER-REQUIRED" "READ_CONTACTS on an API 37 target where the Contact Picker may suffice" "Use the Android Contact Picker for one-off selection and keep READ_CONTACTS only for a declared core use (Play Console Help 16909972)." src 'READ_CONTACTS'
    fi
    if grep_has 'ACCESS_FINE_LOCATION|ACCESS_COARSE_LOCATION' && ! grep_has 'onlyForLocationButton'; then
      finding high "GOOGLE-LOCATION-BUTTON-SCOPE" "Location requested on an API 37 target without the location button scope" "Scope one-shot location to the Android location button with the onlyForLocationButton manifest flag (Play Console Help 16909972)." src 'ACCESS_FINE_LOCATION|ACCESS_COARSE_LOCATION'
    fi
    if grep_has 'NsdManager|MulticastSocket|_tcp\.local|mDNS' && ! grep_has 'ACCESS_LOCAL_NETWORK'; then
      finding high "ANDROID-LOCAL-NETWORK-PERMISSION" "Local network discovery on an API 37 target without ACCESS_LOCAL_NETWORK" "Declare and request android.permission.ACCESS_LOCAL_NETWORK before any LAN discovery or connection (Android 17 behavior changes)." src 'NsdManager|MulticastSocket|_tcp\.local|mDNS'
    fi
  fi
  if grep_has 'DexClassLoader|PathClassLoader|loadDex'; then
    finding high "ANDROID-DYNAMIC-CODE-LOADING" "Dynamic code loading at runtime" "Ship all code in the package. Server changes are data, not executable code." src 'DexClassLoader|PathClassLoader|loadDex'
  fi
  if grep_has 'getSharedPreferences'; then
    if grep_has 'token|password|credential|secret|jwt' && ! grep_has 'EncryptedSharedPreferences|KeyStore|SQLCipher'; then
      finding high "BOTH-SECURE-STORAGE" "Plain SharedPreferences storage is used for sensitive credentials" "Store access tokens and sensitive credentials in Android EncryptedSharedPreferences / Keystore instead." src 'token|password|credential|secret|jwt'
    fi
  fi
  if grep_has 'allowBackup="true"'; then
    if ! grep_has 'dataExtractionRules|fullBackupContent|allowBackup="false"'; then
      finding high "ANDROID-INSECURE-BACKUP" "Android allowBackup is enabled without strict filters" "Disable backups using android:allowBackup=\"false\", or restrict backup folders using dataExtractionRules." src 'allowBackup="true"'
    fi
  fi
  if grep_has 'android:scheme'; then
    if ! grep_has 'assetlinks.json'; then
      finding high "BOTH-UNSAFE-DEEPLINK" "Custom URL deep link schemes declared without App Links configuration" "Configure App Links (Android) using assetlinks.json verification to prevent URL hijacking." src 'android:scheme'
    fi
  fi
  if grep_has 'QUERY_ALL_PACKAGES'; then
    finding high "ANDROID-QUERY-ALL-PACKAGES" "QUERY_ALL_PACKAGES without a permitted use case" "Declare specific packages with a queries element, or qualify for a permitted use case." src 'QUERY_ALL_PACKAGES'
  fi
  if grep_has 'SYSTEM_ALERT_WINDOW|TYPE_APPLICATION_OVERLAY'; then
    finding high "ANDROID-OVERLAY-TAPJACKING" "System overlay permission present" "Remove overlay abuse. The overlay plus accessibility combination is a strong malware signal." src 'SYSTEM_ALERT_WINDOW|TYPE_APPLICATION_OVERLAY'
  fi
  if grep_has 'com\.google\.android\.play:age-signals|AgeSignalsManager|AgeSignalsRequest'; then
    finding critical "GOOGLE-PLAY-AGE-SIGNALS-MISUSE" "Play Age Signals API dependency found" "Ensure age signals are ONLY used to provide age-appropriate experiences. Using them for advertising, marketing, user profiling, or analytics is a direct ToS violation that can result in immediate app suspension or takedown." src 'com\.google\.android\.play:age-signals|AgeSignalsManager|AgeSignalsRequest'
  fi
  if grep_has '<ImageView|<ImageButton'; then
    if ! grep_has 'contentDescription'; then
      finding medium "ANDROID-ACCESSIBILITY-TALKBACK" "XML ImageView or ImageButton missing contentDescription" "Add an android:contentDescription attribute (Google User Experience - Accessibility)." src '<ImageView|<ImageButton'
    fi
  fi
  if grep_has 'android:textSize=.*dp'; then
    finding medium "ANDROID-ACCESSIBILITY-FONTSCALING" "Text size defined in dp instead of sp" "Always define text size in sp to allow system font scaling to work correctly (Google User Experience - Accessibility)." src 'android:textSize=.*dp'
  fi
  if grep_has 'android:(textColor|background)=.*#'; then
    finding medium "ANDROID-ACCESSIBILITY-HIGHCONTRAST" "Hardcoded hex colors ignoring high contrast settings" "Use semantic theme references or color resources instead of hardcoded hex values (Google User Experience - Accessibility)." src 'android:(textColor|background)=.*#'
  fi
  if grep_has 'android:(layout_width|layout_height|minWidth|minHeight)=.*dp'; then
    if grep_has 'clickable|onClick'; then
      finding medium "ANDROID-ACCESSIBILITY-SCANNER" "Interactive controls with hardcoded dimensions" "Verify touch target sizes are at least 48dp (Google User Experience - Accessibility)." src 'clickable|onClick'
    fi
  fi
  finding medium "GOOGLE-12-TESTER-RULE" "Verify the closed testing requirement" "A new personal account needs 12 testers over 14 consecutive days before production."
  # Play only allows READ_MEDIA_IMAGES and READ_MEDIA_VIDEO on API 33+ when the system picker cannot serve the core
  # feature, and a Play Console declaration is required either way (Photo and Video Permissions policy).
  if manifest_has 'android\.permission\.READ_MEDIA_(IMAGES|VIDEO)'; then
    if ! grep_has 'PickVisualMedia|ACTION_PICK_IMAGES|PhotoPicker|photo_picker'; then
      finding high "GOOGLE-PHOTO-VIDEO-PERMISSIONS-DECLARATION" "READ_MEDIA_IMAGES or READ_MEDIA_VIDEO declared without the Android photo picker" "Use the Android photo picker for one-off selection. Keep broad access only for a core gallery-style feature and complete the Photo and Video Permissions declaration in Play Console." manifest 'android\.permission\.READ_MEDIA_(IMAGES|VIDEO)'
    fi
  fi
  # Declared permissions in AndroidManifest.xml, the surface Play enforces on (#542). English words matched prose,
  # and bare API symbols match imports, comments and vendored SDKs. READ_MEDIA_* has its own check below.
  if manifest_has 'android\.permission\.(READ_CONTACTS|WRITE_CONTACTS|READ_SMS|SEND_SMS|RECEIVE_SMS|READ_CALL_LOG|WRITE_CALL_LOG|GET_ACCOUNTS|MANAGE_EXTERNAL_STORAGE)'; then
    if ! grep_has 'prominent disclosure|user consent|privacy consent|accept policy|[Pp]rominentDisclosure|[Dd]isclosureDialog|[Cc]onsentDialog|showDisclosure|requestConsent'; then
      finding critical "ANDROID-USER-DATA-DISCLOSURE" "Missing prominent disclosure for sensitive user data" "Provide a prominent in-app disclosure before collecting sensitive personal data, and obtain explicit user consent." manifest 'android\.permission\.(READ_CONTACTS|WRITE_CONTACTS|READ_SMS|SEND_SMS|RECEIVE_SMS|READ_CALL_LOG|WRITE_CALL_LOG|GET_ACCOUNTS|MANAGE_EXTERNAL_STORAGE)'
    fi
  fi
  if grep_has 'com\.google\.android\.gms\.permission\.AD_ID|AD_ID|getAdvertisingIdInfo'; then
    if ! grep_has 'opt-out|reset AD_ID|advertisingIdConsent|delete AD_ID'; then
      finding high "ANDROID-ADVERTISING-ID" "Google Play Advertising ID usage without disclosure or opt-out" "Declare the AD_ID permission in AndroidManifest.xml and handle user opt-out or deletion requests in full compliance with Google Play policy." src 'com\.google\.android\.gms\.permission\.AD_ID|AD_ID|getAdvertisingIdInfo'
    fi
  fi
  if grep_has 'requestPermissions|checkSelfPermission|shouldShowRequestPermissionRationale'; then
    if ! grep_has 'permission explanation|showPermissionRationale|explainPermission'; then
      finding high "ANDROID-RUNTIME-PERMISSIONS" "Sensitive runtime permissions requested without validation" "Check permissions dynamically at runtime, show a clear rationale if denied, and handle denials gracefully." src 'requestPermissions|checkSelfPermission|shouldShowRequestPermissionRationale'
    fi
  fi
  if grep_has 'HealthConnectClient|com\.google\.android\.gms\.permission\.HealthConnect|READ_STEPS|READ_HEART_RATE'; then
    if ! grep_has 'healthConnectConsent|healthPrivacyPolicy|Health Connect'; then
      finding critical "ANDROID-HEALTH-PERMISSIONS" "Health or fitness data access without Health Connect declaration" "Declare Health Connect permissions, complete the console Health Connect form, and maintain a dedicated health privacy policy." src 'HealthConnectClient|com\.google\.android\.gms\.permission\.HealthConnect|READ_STEPS|READ_HEART_RATE'
    fi
  fi
fi

# ===== Web checks =====
if [ "$IS_WEB" -eq 1 ]; then
  if grep_has 'processData|personalData|submitForm|registerWeb|webForm'; then
    if ! grep_has 'GDPR|opt-in|privacyConsent|deletePersonalData|exportData'; then
      finding critical "WEB-GDPR-COMPLIANCE" "Processing web personal data without GDPR compliance controls" "Integrate standard GDPR compliance gates including explicit opt-in for data processing and a mechanism for data deletion." src 'processData|personalData|submitForm|registerWeb|webForm'
    fi
  fi
  if grep_has 'document\.cookie|setCookie|cookieStore|js-cookie|cookieConsent'; then
    if ! grep_has 'cookieBanner|cookieConsentBanner|acceptCookies|cookiePreferences'; then
      finding critical "WEB-COOKIE-CONSENT" "Setting non-essential cookies without prior cookie consent" "Implement a compliant Cookie Consent banner that blocks non-essential cookies until the user gives explicit consent." src 'document\.cookie|setCookie|cookieStore|js-cookie|cookieConsent'
    fi
  fi
  if grep_has 'localStorage\.setItem|localStorage'; then
    if ! grep_has 'encryptedStorage|encryptToken|consentLocalStorage|clearLocalStorage'; then
      finding high "WEB-LOCAL-STORAGE" "Unencrypted sensitive personal data stored in localStorage" "Avoid storing plain sensitive personal info in localStorage, encrypt any stored tokens, and respect storage preferences." src 'localStorage\.setItem|localStorage'
    fi
  fi
  if grep_has 'sessionStorage\.setItem|sessionStorage'; then
    if ! grep_has 'encryptedSession|clearSessionStorage'; then
      finding high "WEB-SESSION-STORAGE" "Sensitive session details stored in sessionStorage without protection" "Limit and secure the data written to sessionStorage, apply encryption, and ensure data is deleted at session end." src 'sessionStorage\.setItem|sessionStorage'
    fi
  fi
  if grep_has 'indexedDB\.open|indexedDB|createObjectStore'; then
    if ! grep_has 'encryptDatabase|deleteDatabase|consentIndexedDB'; then
      finding high "WEB-INDEXEDDB" "Structured personal data stored in IndexedDB without security controls" "Use encrypted IndexedDB wrappers for structured sensitive records, check user consent, and clear databases upon logout." src 'indexedDB\.open|indexedDB|createObjectStore'
    fi
  fi
  if grep_has 'gtag|fbq|google-analytics|trackingPixel|analytics\.js|hotjar'; then
    if ! grep_has 'consentTracking|disableTracking|optOutTracking|trackingPreferences'; then
      finding high "WEB-TRACKING-TECHNOLOGIES" "Third-party tracking technologies loaded without consent" "Load third-party tracking scripts and pixels conditionally only after receiving explicit user cookie consent." src 'gtag|fbq|google-analytics|trackingPixel|analytics\.js|hotjar'
    fi
  fi
fi

}

# ----- app roots (issue #612). A root is an Expo, React Native, Flutter, or Capacitor app, an Android project, or an
# Xcode project. A platform folder is part of the app above it. A library, a Pods tree, or a Heroku app.json never counts.
is_library() {  # $1 dir. a Flutter plugin, or a React Native module (peerDependencies and no app config)
  local f
  [ -f "$1/pubspec.yaml" ] && grep -qE '^[[:space:]]*plugin:' "$1/pubspec.yaml" 2>/dev/null && return 0
  if [ -f "$1/package.json" ] && grep -q '"peerDependencies"' "$1/package.json" 2>/dev/null; then
    [ -f "$1/app.json" ] && return 1
    for f in app.config.js app.config.ts app.config.mjs app.config.cjs; do [ -f "$1/$f" ] && return 1; done
    for f in "$1"/android/settings.gradle "$1"/android/settings.gradle.kts "$1"/ios/Podfile "$1"/ios/*.xcodeproj "$1"/ios/*.xcworkspace; do [ -e "$f" ] && return 1; done
    return 0
  fi
  return 1
}
has_framework_marker() {  # $1 dir. Expo or React Native CLI app.json, app.config.*, Flutter pubspec, Capacitor config, RN package.json
  local f
  is_library "$1" && return 1
  [ -f "$1/pubspec.yaml" ] && return 0
  for f in "$1"/capacitor.config.*; do [ -e "$f" ] && return 0; done
  for f in app.config.js app.config.ts app.config.mjs app.config.cjs; do [ -f "$1/$f" ] && return 0; done
  [ -f "$1/app.json" ] && grep -qE '"(expo|displayName)"' "$1/app.json" 2>/dev/null && return 0
  [ -f "$1/package.json" ] && grep -qE '"react-native"|"expo"' "$1/package.json" 2>/dev/null && return 0
  return 1
}
rn_dependency() {  # $1 package.json. react-native or expo under "dependencies", never a dev or peer dependency (issue #655)
  tr -d '\n\r' < "$1" 2>/dev/null | grep -oE '"dependencies"[[:space:]]*:[[:space:]]*\{[^}]*\}' | grep -E '"(react-native|expo)"[[:space:]]*:' >/dev/null
}
native_dir_has_project() {  # $1 an ios or android folder. 0 when a project marker sits within four levels
  find "$1" -maxdepth 4 \( -type d \( -name Pods -o -name node_modules -o -name build \) -prune \) \
    -o \( -name 'Info.plist' -o -name '*.xcodeproj' -o -name 'AndroidManifest.xml' -o -name 'build.gradle' -o -name 'build.gradle.kts' \) -print 2>/dev/null \
    | grep . >/dev/null
}
linked_app_dir() {  # $1 a symlink below the root (issue #657). 0 when it points at an app directory outside the tree.
  # One level only. the target is read with plain find, which never follows a further link, so a cycle cannot loop.
  local t f
  case "${1##*/}" in ios|android) return 1 ;; esac   # a linked platform folder is not followed, see the documented limits
  case "${1##*/}" in node_modules|Pods|.git|build|dist|DerivedData|vendor|.dart_tool|Carthage|.pub-cache) return 1 ;; esac   # same names find_app prunes
  [ -d "$1" ] || return 1
  t="$(cd "$1" 2>/dev/null && pwd -P)" || return 1
  case "$t/" in "$ROOT_REAL"/*) return 1 ;; esac   # back into the tree, or the tree itself
  case "$ROOT_REAL/" in "$t"/*) return 1 ;; esac   # the tree's own parent or an ancestor
  is_library "$t" && return 1
  dir_has_app_marker "$t"
}
dir_has_app_marker() {  # $1 dir. 0 when an app marker sits at its top level
  local t="$1" f
  for f in app.config.js app.config.ts app.config.mjs app.config.cjs; do [ -f "$t/$f" ] && return 0; done
  for f in "$t"/capacitor.config.* "$t"/*.xcodeproj "$t"/*.xcworkspace "$t"/settings.gradle "$t"/settings.gradle.kts; do [ -e "$f" ] && return 0; done
  [ -f "$t/app.json" ] && grep -qE '"(expo|displayName)"' "$t/app.json" 2>/dev/null && return 0
  [ -f "$t/pubspec.yaml" ] && { [ -d "$t/ios" ] || [ -d "$t/android" ] || [ -f "$t/lib/main.dart" ]; } && return 0
  [ -f "$t/package.json" ] && { [ -d "$t/ios" ] || [ -d "$t/android" ]; } && rn_dependency "$t/package.json" && return 0
  for f in "$t"/build.gradle "$t"/build.gradle.kts; do [ -f "$f" ] && grep -qE 'com\.android\.application|android\.application' "$f" 2>/dev/null && return 0; done
  for f in "$t"/ios "$t"/android; do [ -d "$f" ] && native_dir_has_project "$f" && return 0; done
  # Unity, .NET MAUI, Tauri, Cordova and Capacitor, the same signals scan_tree reads
  [ -f "$t/ProjectSettings/ProjectVersion.txt" ] && return 0
  for f in "$t"/*.csproj; do [ -f "$f" ] && grep -qE '<UseMaui>[[:space:]]*true|net[0-9.]+-(ios|android|maccatalyst)' "$f" 2>/dev/null && return 0; done
  for f in "$t"/tauri.conf.json "$t"/tauri.conf.json5 "$t"/Tauri.toml "$t"/src-tauri/tauri.conf.json "$t"/src-tauri/tauri.conf.json5 "$t"/src-tauri/Tauri.toml; do [ -f "$f" ] && return 0; done
  [ -f "$t/config.xml" ] && grep -qE '<widget|xmlns:cdv' "$t/config.xml" 2>/dev/null && return 0
  [ -f "$t/package.json" ] && grep -qE '"@capacitor/core"|"cordova-(ios|android)"' "$t/package.json" 2>/dev/null && return 0
  return 1
}
# Issue #656. Under a root framework app, a bare native project with its own Info.plist or AndroidManifest.xml is a
# second app, unless a root build file (settings.gradle, Podfile, a workspace) names its path. A native root is unchanged.
bare_native_apart() {  # $1 candidate dir below $DIR
  local rel="${1#"${DIR%/}"/}" f
  case "$rel" in ios|ios/*|android|android/*) return 1 ;; esac
  # A folder named exactly demo, example, sample, or playground (or plural) holds a repo demo, so it stays in the root scan.
  printf '%s' "$rel" | tr '[:upper:]' '[:lower:]' | tr '/' '\n' | grep -qxE 'demos?|examples?|samples?|playgrounds?' && return 1
  find "$1" -maxdepth 4 \( -type d \( -name Pods -o -name node_modules -o -name build \) -prune \) \
    -o \( -name 'Info.plist' -o -name 'AndroidManifest.xml' \) -print 2>/dev/null | grep . >/dev/null || return 1
  # Only a shippable app splits off. a library module or a local native module stays with the app that uses it.
  find "$1" -maxdepth 5 \( -type d \( -name Pods -o -name node_modules -o -name build \) -prune \) -o -path '*.xcodeproj/project.pbxproj' -print 2>/dev/null \
    | while IFS= read -r f; do grep -q 'com\.apple\.product-type\.application' "$f" 2>/dev/null || ! grep -q 'com\.apple\.product-type\.' "$f" 2>/dev/null && echo "$f"; done | grep . >/dev/null \
    || find "$1" -maxdepth 4 \( -type d \( -name node_modules -o -name build \) -prune \) -o \( -name 'build.gradle' -o -name 'build.gradle.kts' \) -print 2>/dev/null \
      | while IFS= read -r f; do grep -lE 'com\.android\.application|android\.application' "$f" 2>/dev/null; done | grep . >/dev/null || return 1
  # A native host that embeds the root framework (brownfield) shares its dependencies, so it stays in the root scan.
  grep -rlsE 'RCTBridge|RCTRootView|RCTSurfaceHostingProxyRootView|RCTSurfaceHostingView|RCTReactNativeFactory|RCTAppDelegate|import React$|import React_|ReactActivity|ReactNativeHost|ReactApplication|ReactInstanceManager|DefaultReactNativeHost|RCTDefaultReactNativeFactoryDelegate|ReactNativeDelegate|ExpoAppDelegate|ExpoReactNativeFactory|React-Core|react-native|CodePush|ExpoModulesCore|EXAppDelegate|FlutterEngine|FlutterViewController|Flutter/Flutter\.h|<React/|import Capacitor|Capacitor/Capacitor\.h|CAPBridgeViewController|Cordova/|import Cordova|CDVViewController|CDVPlugin|CDVAppDelegate|import Flutter' "$1" \
    --include='*.swift' --include='*.m' --include='*.mm' --include='*.h' --include='*.kt' --include='*.java' --include='*.gradle' --include='*.kts' --include='Podfile' --include='*.pbxproj' \
    --exclude-dir=Pods --exclude-dir=node_modules --exclude-dir=build 2>/dev/null | grep . >/dev/null && return 1
  # The root keeps the scan for a platform it has no folder of, or its checks for that platform would vanish.
  native_dir_has_project "$DIR/ios" || ! find "$1" -maxdepth 4 -name 'Info.plist' -not -path '*/Pods/*' 2>/dev/null | grep . >/dev/null || return 1
  native_dir_has_project "$DIR/android" || ! find "$1" -maxdepth 4 -name 'AndroidManifest.xml' -not -path '*/build/*' 2>/dev/null | grep . >/dev/null || return 1
  for f in "$DIR"/settings.gradle "$DIR"/settings.gradle.kts "$DIR"/android/settings.gradle "$DIR"/android/settings.gradle.kts \
    "$DIR"/Podfile "$DIR"/ios/Podfile "$DIR"/*.xcworkspace/contents.xcworkspacedata "$DIR"/ios/*.xcworkspace/contents.xcworkspacedata; do
    [ -f "$f" ] && grep -qF -e "$rel" "$f" 2>/dev/null && return 1
  done
  return 0
}
app_roots() {  # prints the roots, one per line, only when two or more distinct apps exist. the project root itself may be one of them
  local m d r k t x keep=() seen=() atroot=0 rootfw=0 ROOT_REAL
  ROOT_REAL="$(cd "$DIR" 2>/dev/null && pwd -P)" || ROOT_REAL="${DIR%/}"
  has_framework_marker "$DIR" && rootfw=1
  {
    find_app 12 -name 'app.json' -o -name 'app.config.js' -o -name 'app.config.ts' -o -name 'app.config.mjs' -o -name 'app.config.cjs' \
      -o -name 'pubspec.yaml' -o -name 'capacitor.config.*' -o -name 'settings.gradle' -o -name 'settings.gradle.kts' \
      -o -name '*.xcodeproj' -o -name '*.xcworkspace' -o -name 'build.gradle' -o -name 'build.gradle.kts' -o -name 'package.json' | while IFS= read -r m; do
        case "$m" in *.xcodeproj/*|*.xcworkspace/*) continue ;; esac
        case "/$m/" in *Tests/*|*/androidTest/*|*/__tests__/*|*/test/*|*/tests/*|*/integration_test/*) continue ;; esac
        d="$(dirname "$m")"
        case "$m" in
          */app.json) grep -qE '"(expo|displayName)"' "$m" 2>/dev/null || continue ;;
          */pubspec.yaml) { [ -d "$d/ios" ] || [ -d "$d/android" ] || [ -f "$d/lib/main.dart" ]; } && ! is_library "$d" || continue ;;
          */build.gradle|*/build.gradle.kts) grep -qE 'com\.android\.application|android\.application' "$m" 2>/dev/null || continue ;;
          */package.json) { [ -d "$d/ios" ] || [ -d "$d/android" ]; } && rn_dependency "$m" && ! is_library "$d" || continue ;;  # issue #655
        esac
        printf '%s\n' "$d"
      done
    find_app 12 \( -type d \( -name ios -o -name android \) \) -o -type l | while IFS= read -r d; do
      case "/$d/" in *Tests/*|*/androidTest/*|*/__tests__/*|*/test/*|*/tests/*|*/integration_test/*) continue ;; esac
      if [ -L "$d" ]; then linked_app_dir "$d" && printf '%s\n' "$d"; continue; fi
      native_dir_has_project "$d" && printf '%s\n' "$d"
    done
  } 2>/dev/null | while IFS= read -r r; do
    case "${r##*/}" in ios|android) is_library "$(dirname "$r")" && continue; has_framework_marker "$(dirname "$r")" && r="$(dirname "$r")" ;; esac
    printf '%s\n' "$r"
  done | sort -u | {
    while IFS= read -r r; do
      [ "${r%/}" = "${DIR%/}" ] && { atroot=1; continue; }
      # A linked app is never inside another root's scan, find does not descend it, so it is always its own root.
      if [ -L "${r%/}" ]; then
        t="$(cd "$r" 2>/dev/null && pwd -P)" || continue
        for x in ${seen[@]+"${seen[@]}"}; do [ "$x" = "$t" ] && continue 2; done   # two links to one app scan it once
        seen+=("$t")
      else
        for k in ${keep[@]+"${keep[@]}"}; do case "$r/" in "$k"/*) continue 2 ;; esac; done
        [ "$atroot" -eq 1 ] && ! has_framework_marker "$r" && ! { [ "$rootfw" -eq 1 ] && bare_native_apart "$r"; } && continue
      fi
      keep+=("$r")
    done
    if [ "$atroot" -eq 1 ]; then
      [ "${#keep[@]}" -ge 1 ] && printf '%s\n' "$DIR" "${keep[@]}"
    else
      local plain=0 links=()
      for k in ${keep[@]+"${keep[@]}"}; do if [ -L "${k%/}" ]; then links+=("$k"); else plain=$((plain+1)); fi; done
      if [ "$plain" -ge 2 ]; then printf '%s\n' "${keep[@]}"
      # Fewer than two plain apps scan as one tree, as before. A linked app sits beside that scan, never in place of it.
      elif [ "${#links[@]}" -ge 1 ]; then printf '%s\n' "$DIR" "${links[@]}"; fi
    fi
  }
}

# ----- report routing (issue #610). Hook mode buffers the report. A block goes to stderr, the only
# stream Claude Code shows on exit 2. A pass stays on stdout. Standalone mode prints straight to stdout.
emit_report() {  # $1 is the exit code about to be returned
  if [ -n "$REPORT" ]; then
    exec 1>&3 3>&-
    CURSOR_IDS="$(grep -oE '\[CRITICAL\] [A-Za-z0-9._-]+' "$REPORT" 2>/dev/null | sed 's/^\[CRITICAL\] //' | sort -u | tr '\n' ' ')"
    if [ "$1" -eq 2 ] || [ "$IS_CURSOR" -eq 1 ]; then cat "$REPORT" >&2; else cat "$REPORT"; fi
    rm -f "$REPORT" 2>/dev/null; REPORT=""
  elif [ "$CURSOR_FD" -eq 1 ]; then
    exec 1>&3 3>&-; CURSOR_FD=0
  fi
  cursor_reply "$1"
}
# A hook timeout sends TERM. Flush what was buffered to stderr so the partial report is not lost.
trap 'emit_report 2; exit 143' INT TERM HUP
if [ -n "$STDIN_JSON" ]; then
  REPORT="$(mktemp 2>/dev/null)" || REPORT=""
  # An unusable mktemp falls back to /tmp, as the scan buffer does, so the report still reaches stderr.
  { [ -n "$REPORT" ] && : >"$REPORT" 2>/dev/null; } || REPORT="/tmp/ascg-report.$$"
  if [ -n "$REPORT" ] && : >"$REPORT" 2>/dev/null; then exec 3>&1; exec >"$REPORT"; else REPORT=""; REPORT_DEGRADED=1; fi
  # Unbuffered, Cursor still needs a clean stdout, so the live report goes to stderr instead.
  if [ -z "$REPORT" ] && [ "$IS_CURSOR" -eq 1 ]; then exec 3>&1; exec 1>&2; CURSOR_FD=1; fi
fi

# The deadline list prints after the findings, and only for the stores this project ships to (issue #842).
print_deadlines() {
  local hd py="" c plats=""
  hd="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  for c in "$hd/../../scripts/deadline-checker.py" "$hd/../skills/app-store-compliance/scripts/deadline-checker.py" "${HOME:-}/.agents/skills/app-store-compliance/scripts/deadline-checker.py"; do
    if [ -f "$c" ]; then py="$c"; break; fi
  done
  [ -n "$py" ] || return 0
  echo ""
  if ! tool_ok python3 -c pass; then echo "Regulatory deadline list skipped. python3 not found."; return 0; fi
  [ "$ANY_IOS" -eq 1 ] && plats="ios"
  [ "$ANY_AND" -eq 1 ] && plats="${plats:+$plats,}android"
  if [ -n "$plats" ]; then python3 "$py" --brief --platforms "$plats"; else python3 "$py" --brief; fi
}

echo "== App Store Compliance Guard =="
echo "Project. $DIR"
ROOTS="$(app_roots)"
if [ -n "$ROOTS" ]; then
  PROJECT_ROOT="${DIR%/}"
  echo "Apps. $(printf '%s\n' "$ROOTS" | grep -c .) app roots, each scanned on its own"
  echo ""
  POOL_FW=""; SPLIT_NATIVE=""
  if printf '%s\n' "$ROOTS" | sed 's:/$::' | grep -qxF "$PROJECT_ROOT"; then
    NESTED_PRUNE=()
    while IFS= read -r OTHER; do
      [ -n "$OTHER" ] && [ "${OTHER%/}" != "$PROJECT_ROOT" ] || continue
      if ! has_framework_marker "$OTHER" && (DIR="$PROJECT_ROOT"; bare_native_apart "$OTHER"); then
        SPLIT_NATIVE="$SPLIT_NATIVE${OTHER%/}
"
      else
        NESTED_PRUNE+=(-o -path "$(printf '%s' "$OTHER" | sed 's/[][*?\\]/\\&/g')")
      fi
    done <<EOF3
$ROOTS
EOF3
    POOL_PRUNE=(${NESTED_PRUNE[@]+"${NESTED_PRUNE[@]}"})
    if [ -n "$SPLIT_NATIVE" ]; then
      SAVE_DIR="$DIR"; SAVE_IOS="${IS_IOS:-0}"; SAVE_AND="${IS_AND:-0}"; DIR="$PROJECT_ROOT"; detect_frameworks; DIR="$SAVE_DIR"; IS_IOS="$SAVE_IOS"; IS_AND="$SAVE_AND"
      [ "$IS_FLUTTER" -eq 1 ] && POOL_FW="$POOL_FW flutter"; [ "$IS_RN" -eq 1 ] && POOL_FW="$POOL_FW rn"
      [ "$IS_IONIC" -eq 1 ] && POOL_FW="$POOL_FW ionic"; [ "$IS_UNITY" -eq 1 ] && POOL_FW="$POOL_FW unity"
      [ "$IS_MAUI" -eq 1 ] && POOL_FW="$POOL_FW maui"; [ "$IS_TAURI" -eq 1 ] && POOL_FW="$POOL_FW tauri"
      [ "$IS_KMP" -eq 1 ] && POOL_FW="$POOL_FW kmp"
    fi
  fi
  while IFS= read -r ROOT; do
    [ -n "$ROOT" ] || continue
    INHERIT_FW=""
    if [ -n "$POOL_FW" ] && { [ "${ROOT%/}" = "$PROJECT_ROOT" ] || printf '%s' "$SPLIT_NATIVE" | grep -qxF "${ROOT%/}"; }; then
      INHERIT_FW="$POOL_FW"
    fi
    NESTED_PRUNE=()
    if [ "${ROOT%/}" = "$PROJECT_ROOT" ]; then
      while IFS= read -r OTHER; do [ "${OTHER%/}" != "$PROJECT_ROOT" ] && NESTED_PRUNE+=(-o -path "$(printf '%s' "$OTHER" | sed 's/[][*?\\]/\\&/g')"); done <<EOF2
$ROOTS
EOF2
    fi
    DIR="$ROOT"
    [ -L "${DIR%/}" ] && DIR="$(cd "$DIR" 2>/dev/null && pwd -P)"   # a linked app (issue #657) is walked through its target
    echo "App. $ROOT"
    scan_tree
    flush_findings
    # One scannable sibling must not speak for a root the store checks never ran on.
    # The project root scanned only beside a linked app, with no marker and nothing found, is not an app (#657).
    if [ "${ROOT%/}" = "$PROJECT_ROOT" ] && [ "$IS_IOS" -eq 0 ] && [ "$IS_AND" -eq 0 ] && [ "$IS_WEB" -eq 0 ] && [ "$NEEDS_NATIVE" -eq 0 ] && ! dir_has_app_marker "$PROJECT_ROOT"; then
      :
    elif [ "$IS_IOS" -eq 0 ] && [ "$IS_AND" -eq 0 ] && { [ "$IS_WEB" -eq 0 ] || [ "$NEEDS_NATIVE" -eq 1 ]; }; then
      UNCHECKED="${UNCHECKED:+$UNCHECKED, }${ROOT#"$PROJECT_ROOT"/}"
    fi
  done <<EOF
$ROOTS
EOF
  # A split native app and the root it left are also scanned as one, as in 1.0.0, so evidence that spans
  # both (a shared source file and the split app) still counts. Only findings not listed above are added.
  if [ -n "$SPLIT_NATIVE" ]; then
    NESTED_PRUNE=(${POOL_PRUNE[@]+"${POOL_PRUNE[@]}"}); INHERIT_FW=""; DIR="$PROJECT_ROOT"; POOL_PASS=1
    scan_tree >/dev/null
    POOL_PASS=0
    if [ "$(( ${#F_CRIT[@]} + ${#F_HIGH[@]} + ${#F_MED[@]} ))" -gt 0 ]; then
      echo "App. $PROJECT_ROOT with its split native apps, scanned as one as in 1.0.0"
      flush_findings
    fi
  fi
else
  scan_tree
  flush_findings
fi
print_deadlines

# ===== summary and exit =====
echo ""
echo "Summary. critical=$CRIT high=$HIGH medium=$MED"
# Issue #658. A run killed by the hook timeout looks like a silent pass, so say how long this one took.
SLOW_SECS="${APP_STORE_GUARD_SLOW_SECS:-45}"
case "$SLOW_SECS" in ''|*[!0-9]*) SLOW_SECS=45 ;; esac
echo "Scan time. ${SECONDS}s"
[ "$SECONDS" -ge "$SLOW_SECS" ] && echo "Slow scan. This run is close to the Claude Code hook timeout of 60 seconds. Raise \"timeout\" on the hook entry in settings.json to at least 120."
echo "Reference. docs/ in the app-store-compliance repo, and data/rejection-patterns.json"

if [ "$CRIT" -gt 0 ]; then
  if [ "${APP_STORE_GUARD_OK:-0}" = "1" ]; then
    echo "APP_STORE_GUARD_OK set. Critical findings present but the submission is allowed."
    log_err "override used with $CRIT critical findings"
    emit_report 0; exit 0
  fi
  echo ""
  echo "BLOCKED. $CRIT critical rejection risk(s) above. Fix them, or set APP_STORE_GUARD_OK=1 to override."
  echo "Next. Fix each [CRITICAL] line using its fix. line, then run the same command again."
  [ "${REPORT_DEGRADED:-0}" = "1" ] && echo "BLOCKED. $CRIT critical rejection risk(s). Full report on stdout (no temp file available for buffering)." >&2
  emit_report 2; exit 2
fi
# A scan buffer that failed mid-run leaves the result unknown, never CLEAR.
if [ -n "$SCAN_ERROR" ]; then
  NOTE="NOT CHECKED. The scan could not run because $SCAN_ERROR."
  echo ""; echo "$NOTE"
  if [ -n "$STDIN_JSON" ]; then emit_report 0; echo "$NOTE" >&2; exit 0; fi
  exit 1
fi
# A verdict line every time. Exit 0 with nothing scanned reads as a pass, so it is named and, run by hand, exits 1.
if [ -n "$UNCHECKED" ] || { [ "$ANY_NATIVE" -eq 0 ] && { [ "$ANY_WEB" -eq 0 ] || [ "$ANY_NEEDS_NATIVE" -eq 1 ]; }; }; then
  NOTE="NOT CHECKED. No iOS or Android project was found in $DIR, so the store checks did not run."
  if [ -n "$UNCHECKED" ]; then
    NOTE="NOT CHECKED. No ios or android folder in $UNCHECKED, so the store checks did not run there. The other app roots had 0 critical risks."
    NEXT="Next. Create the native project in each folder named above (npx expo prebuild, npx cap add, flutter create, or cargo tauri ios init), then run the guard again."
  elif [ "$ANY_RN" -eq 1 ]; then NEXT="Next. This looks like an Expo or React Native app with no ios or android folder. Run npx expo prebuild, then run the guard again."
    [ "$EXPO_READ" -eq 1 ] && NOTE="NOT CHECKED. No ios or android folder in $DIR, so the native code checks did not run. Only the Expo app config was read."
  elif [ "$ANY_NEEDS_NATIVE" -eq 1 ]; then NEXT="Next. This app has no ios or android folder yet. Run $NATIVE_HINT, then run the guard again."
  else NEXT="Next. Point the guard at the folder that holds your Xcode project or your Android app folder."; fi
  echo ""; echo "$NOTE"; echo "$NEXT"
  if [ -n "$STDIN_JSON" ]; then emit_report 0; echo "$NOTE $NEXT" >&2; exit 0; fi
  exit 1
fi
echo ""
[ "$ANY_NATIVE" -eq 0 ] && echo "Web project only. No iOS or Android project was found here, so only the web checks ran."
echo "CLEAR. 0 critical risks in the code scan. Read any [HIGH] and [MEDIUM] lines above, then walk docs/PRE-SUBMISSION-CHECKLIST.md for the account and listing checks a scan cannot see."
emit_report 0; exit 0
