#!/usr/bin/env bash
# App Store Compliance Guard. Native and cross-platform (Flutter, RN/Expo, Ionic/Capacitor).
# Standalone or PreToolUse Bash hook on a submit command. See docs/CROSS-PLATFORM-FRAMEWORKS.md.
# @event: PreToolUse
# @matcher: Bash
set -uo pipefail
# Reads all its input. grep -q stops early, and under pipefail its producer's SIGPIPE turns a match into a miss.
grep_q() { grep "$@" >/dev/null; }

HOOK_LOG="${HOME:-}/.claude/hooks/hook-log.sh"
# shellcheck disable=SC1090
[ -f "$HOOK_LOG" ] && source "$HOOK_LOG" 2>/dev/null || true
log_err() { if type hlog_error >/dev/null 2>&1; then hlog_error "app-store-compliance-guard" "$@"; else echo "app-store-compliance-guard: $*" >&2; fi; }

CRIT=0; HIGH=0; MED=0; ANY_IOS=0; ANY_AND=0; ANY_NATIVE=0; ANY_RN=0; ANY_WEB=0; ANY_NEEDS_NATIVE=0; NATIVE_HINT=""; UNCHECKED=""; EXPO_READ=0
FILELIST=""
REPORT=""; REPORT_DEGRADED=0
cleanup() { [ -n "$FILELIST" ] && rm -f "$FILELIST" "$FILELIST.blob" "$FILELIST.manifest" "$FILELIST.code" "$FILELIST.impl" "$FILELIST.ship" 2>/dev/null; [ -n "$REPORT" ] && rm -f "$REPORT" 2>/dev/null; true; }
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
printf '%s' "$STDIN_JSON" | tr -d '\n\r' | grep -E '"hook_event_name"[[:space:]]*:[[:space:]]*"beforeShellExecution"' >/dev/null && IS_CURSOR=1
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
  SUBMIT_RE='fastlane[[:space:]]+(run[[:space:]]+)?(deliver|pilot|supply|submit|appstore|testflight|upload_to_app_store|upload_to_testflight|upload_to_play_store)([^A-Za-z0-9_]|$)|eas([[:space:]]+--?[A-Za-z][A-Za-z0-9-]*([=[:space:]][^-[:space:]][^[:space:]]*)?)*[[:space:]]+(submit|build)|xcrun[[:space:]]+(altool|notarytool)|transporter|gradlew?[^&|;]*(bundleRelease|assembleRelease|publish[A-Za-z]*(Bundle|Apk|Apps)|promote[A-Za-z]*Artifact)|bundletool|xcodebuild[^&|;]*archive|flutter[[:space:]]+build[[:space:]]+(ipa|appbundle|apk|ios)|(npx[[:space:]]+)?(expo[[:space:]]+(prebuild|run:ios|run:android|submit|upload:(ios|android)|build:(ios|android))|cap[[:space:]]+(sync|build|run|copy|open)|react-native[[:space:]]+run-(ios|android))|ionic[[:space:]]+capacitor[[:space:]]+(build|run)|cordova[[:space:]]+build([[:space:]]+--release)?|(^|[^A-Za-z0-9_])unity(-editor|\.exe)?[[:space:]][^;&|]*-buildtarget[[:space:]]+(ios|android)|dotnet[[:space:]]+publish[^;&|]*(-f|--framework)[[:space:]=]+net[0-9.]+-(ios|android)|tauri[[:space:]]+(ios|android)[[:space:]]+build|helm-asc[^;&|]*([[:space:]]builds?[[:space:]]+upload|--submit|[[:space:]]submissions?[[:space:]]+(create|submit)|[[:space:]]review-submissions?)|(^|[[:space:]/])asc[[:space:]]+(builds?[[:space:]]+upload|submissions?[[:space:]]+(create|submit)|review-submissions?)|app-store-connect[[:space:]]+publish'
  UPLOAD_ACTION_RE='(^|[^A-Za-z0-9_])(upload_to_app_store|upload_to_testflight|upload_to_play_store|deliver|pilot|supply|appstore|testflight)([^A-Za-z0-9_]|$)'
  # A custom fastlane lane submits when a word in its name says so, when its Fastfile block calls an
  # upload action, or when the lane is a variable the guard cannot read (scanned, never assumed safe).
  fastlane_lane_submits() {
    local lane ff
    lane="$(printf '%s' "$1" | sed -nE 's/.*(^|[^A-Za-z0-9_.\/-])fastlane[[:space:]]+((ios|android|mac)[[:space:]]+)?([$`]|[A-Za-z_][A-Za-z0-9_]*).*/\4/p' | head -1)"
    [ -z "$lane" ] && return 1
    case "$lane" in '$'*|'`'*) return 0 ;; esac
    case "$lane" in *[!A-Za-z0-9_]*) return 1 ;; esac
    printf '%s' "$lane" | tr '_' '\n' | grep -ixE 'release|beta|deploy|production|prod|publish|submit|upload|appstore|playstore|testflight|distribute' >/dev/null && return 0
    while IFS= read -r ff; do
      [ -f "$ff" ] || continue
      awk -v n="$lane" '$0 ~ "lane[[:space:]]+:" n "([^A-Za-z0-9_]|$)" { on=1; next } on && /^[[:space:]]*(private_)?lane[[:space:]]+:/ { on=0 } on' "$ff" 2>/dev/null \
        | grep -E "$UPLOAD_ACTION_RE" >/dev/null && return 0
    done <<FASTFILES
$(find "$DIR" -maxdepth 3 -name Fastfile -not -path '*/node_modules/*' 2>/dev/null | head -5)
FASTFILES
    return 1
  }
  submits() { set -- "$(fl_norm "$1")"; printf '%s' "$1" | grep_q -iE "$SUBMIT_RE" || printf '%s' "$1" | grep_q -E 'gradlew?[[:space:]]+\$' || fastlane_lane_submits "$1"; }
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
      all=0; printf '%s' "$rseg" | grep_q -E '(^|[^A-Za-z0-9_./-])(turbo|lerna)[[:space:]]|(^|[^A-Za-z0-9_./-])nx[[:space:]]|[[:space:]](-r|--recursive|-ws|--workspaces|foreach)([[:space:]=]|$)' && all=1
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
            tr -d '\n' < "$f" 2>/dev/null | grep -E "\"name\"[[:space:]]*:[[:space:]]*\"$pat\"" >/dev/null && echo "$f"
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
  if ! printf '%s' "$CMD_MATCH" | grep_q -iE "$SUBMIT_RE" \
    && ! printf '%s' "$CMD_MATCH" | grep_q -E '(^|[^A-Za-z0-9_./-])(fastlane|npm|pnpm|bun|yarn|make|turbo|nx|lerna)[[:space:]]|gradlew?[[:space:]]+\$'; then
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
  if [ "$CD_COUNT" -eq 1 ] && printf '%s' "$FIRST" | grep_q -E '^[[:space:]]*cd[[:space:]]+[^&|;]+(&&|;)'; then
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
  SUBST=0; printf '%s' "$CMD" | grep_q -E '\$\(|`|<\(|>\(|=\(' && SUBST=1
  while IFS= read -r SEG; do
    W1="$(printf '%s' "$SEG" | awk '{ sub(/^[ \t({!]+/, ""); while (match($0, /^[A-Za-z_][A-Za-z0-9_]*=[^ \t]*[ \t]+/)) $0 = substr($0, RLENGTH + 1); print $1 }')"
    [ -n "$W1" ] || continue
    if ! submits "$SEG"; then
      { [ "$SUBST" -eq 0 ] && printf '%s' "$W1" | grep_q -E "$SAFE_SEG_RE"; } || SEG_ALL_AND=0
      continue
    fi
    SEG_SUBMITS=$((SEG_SUBMITS+1))
    SEGN="$(fl_norm "$SEG")"
    { printf '%s' "$SEGN" | grep_q -iE "$AND_TARGET_RE" && ! printf '%s' "$SEGN" | grep_q -iE "$IOS_TARGET_RE"; } || SEG_ALL_AND=0
  done <<SEGS
$(printf '%s\n' "$CMD_MATCH" | tr ';&|' '\n\n\n')
SEGS
  if printf '%s' "$CMD" | grep_q -iE "$IOS_TARGET_RE"; then
    :   # an Apple word anywhere in the command keeps the Apple checks, as on main
  elif [ "$SEG_SUBMITS" -gt 0 ]; then
    [ "$SEG_ALL_AND" -eq 1 ] && CMD_TARGET_ANDROID_ONLY=1
  # A wrapped submit (npm run, make) names no tool in the command itself, so the whole command decides, as before.
  elif printf '%s' "$CMD" | grep_q -iE "$AND_TARGET_RE" && ! printf '%s' "$CMD" | grep_q -iE "$IOS_TARGET_RE"; then
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
        printf '%s' "$NQB" | grep_q -iE "$AND_TARGET_RE" || NQ_AND=0
        # the outer arguments of bash -c, sh -c or eval never reach the quoted command, so they name no target
        printf '%s' "$NQB" | grep_q -E '(^|[[:space:]/])(bash|sh|zsh|dash|ksh|fish|eval)([[:space:]]|$)' && NQ_AND=0
        # a submit seen only inside quotes runs in another program (python -c, ruby -e), which never passes it the outer arguments
        submits "$NQB" || NQ_AND=0
      elif ! printf '%s' "$NQW" | grep_q -E "$SAFE_SEG_RE"; then
        NQ_AND=0; NQ_WRAP=$((NQ_WRAP+1))
        printf '%s' "$NQB" | grep_q -iE "$AND_TARGET_RE" || NQ_WRAP_AND=0
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
if [ "$CMD_TARGET_ANDROID_ONLY" -eq 1 ] && ! { printf '%s' "$CMD" | grep_q -iE 'build[[:space:]]+(apk|appbundle)\b|assembleRelease|bundleRelease|run-android|run:android|--platform[[:space:]]+android\b|capacitor[[:space:]]+android\b|-buildtarget[[:space:]]+android|net[0-9.]+-android|tauri[[:space:]]+android\b' \
  && ! printf '%s' "$CMD" | grep_q -iE '\bios\b|\bipa\b|xcodebuild|altool|notarytool'; }; then
  CMD_TARGET_ANDROID_ONLY=0
fi
CMD_TARGET_IOS_ONLY=0
if [ -n "$CMD" ] && printf '%s' "$CMD" | grep_q -iE '(-p|--platform)[[:space:]=]+ios([^A-Za-z]|$)' \
  && ! printf '%s' "$CMD" | grep_q -iE 'android|(-p|--platform)[[:space:]=]+all'; then
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

# Prints the first file:line that matches $1, or nothing. With $2 = manifest only AndroidManifest.xml counts.
# A <uses-permission> with tools:node="remove" strips a permission that an SDK merges in, so the merged manifest
# declares none. A removal scoped with tools:selector strips one library only, so the others still merge it in.
permission_at() {
  local re="$1" hits f n
  grep_has "$re" || return 0
  hits="$(tr '\n' '\0' < "$FILELIST" | xargs -0 grep -EIls -e "$re" 2>/dev/null)"
  [ "${2:-}" = "manifest" ] && hits="$(grep '/AndroidManifest[.]xml$' <<< "$hits")"
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    case "$f" in */AndroidManifest.xml)  # one element per line, so a tools:node on the next line is read
      [ -n "$(tr '\n\r\t' '   ' < "$f" | tr '<' '\n' | grep -E -e "$re" | grep -Ev "tools:node[[:space:]]*=[[:space:]]*[\"']remove[\"']" ; tr '\n\r\t' '   ' < "$f" | tr '<' '\n' | grep -E -e "$re" | grep -E 'tools:selector')" ] || continue ;;
    esac
    n="$(grep -En -m1 -e "$re" "$f" 2>/dev/null | cut -d: -f1)"
    printf '%s%s' "${f#"${DIR%/}"/}" "${n:+:$n}"
    return 0
  done <<< "$hits"
}

APPLE_SRC_RE='[.](swift|m|mm|h)$'
apple_has() {  # 0 if regex found in a Swift or Objective-C source. Compose, Flutter and JS share names like Image( and Button
  [ -s "$FILELIST" ] || return 1
  local out
  out="$(grep -E "$APPLE_SRC_RE" "$FILELIST" | tr '\n' '\0' | xargs -0 grep -EIls -e "$1" 2>/dev/null | head -1)"
  [ -n "$out" ]
}

# ImageCreator() and ImageCreator. in Swift or Objective-C, after comments and strings are skipped.
# A mention in a comment or a string is not a call. The sheet APIs are a different type, so they never match.
# Sets IMAGECREATOR_HIT to file:line. Test directories are already out of the file list.
apple_imagecreator_hit() {
  IMAGECREATOR_HIT=""
  [ -s "$FILELIST" ] || return 1
  command -v python3 >/dev/null 2>&1 || return 1
  local out
  # The list goes in on stdin, so one process sees every file and a declaration in any of them counts.
  out="$(grep -E "$APPLE_SRC_RE" "$FILELIST" | python3 -c "$(cat <<'ICPY'
import re
import sys

def use_at(text, i, end):
    name = "ImageCreator"
    if not text.startswith(name, i):
        return False
    if i and (text[i - 1].isalnum() or text[i - 1] == "_"):
        return False
    k = i + len(name)
    if k < end and (text[k].isalnum() or text[k] == "_"):
        return False
    # A type the app declares under this name is the app own type, not the Image Playground one.
    global DECLARED
    b = i - 1
    while b >= 0:
        if text[b] == chr(10):
            ls = text.rfind(chr(10), 0, b) + 1
            c = text.find("//", ls, b)
            b = (c if c >= 0 else b) - 1
        elif text[b].isspace():
            b -= 1
        elif text[b] == "/" and b and text[b - 1] == "*" and text.rfind("/*", 0, b - 1) >= 0:
            b = text.rfind("/*", 0, b - 1) - 1
        else:
            break
    w = b
    while w >= 0 and (text[w].isalnum() or text[w] == "_"):
        w -= 1
    t2 = k
    while t2 < end and text[t2].isspace():
        t2 += 1
    # A type from another module, as in RenderingKit::ImageCreator.
    if i >= 2 and text[i - 2:i] == "::" and not text[:i - 2].endswith("ImagePlayground"):
        return False
    # A constrained type parameter, as in <ImageCreator: P>, <T, ImageCreator: P> or where ImageCreator: P.
    generic = decl_generic(text, b) or t2 < end and text[t2] == ":" and not text.startswith("::", t2) and b >= 0 and (text[b] in ("<", ",") or text[w + 1:b + 1] == "where")
    # A C typedef names its alias last, as in typedef Renderer ImageCreator;
    st = max(text.rfind(";", 0, i), text.rfind(chr(123), 0, i), text.rfind(chr(125), 0, i)) + 1
    typedef = t2 < end and text[t2] in (";", ",") and "typedef" in text[st:i].split()
    if not typedef and t2 < end and text[t2] in (";", ",") and b >= 0 and text[b] == chr(125):
        # An anonymous body, as in typedef struct { int width; } ImageCreator;
        m = open_of(text, b)
        st = max(text.rfind(";", 0, m), text.rfind(chr(123), 0, m), text.rfind(chr(125), 0, m)) + 1 if m > 0 else m
        typedef = m > 0 and "typedef" in text[st:m].split()
    if text[w + 1:b + 1] == "typealias" and t2 < end and text[t2] == "=":
        rhs = text[t2 + 1:end].lstrip()
        q = len("ImagePlayground.ImageCreator")
        if rhs.startswith("ImagePlayground.ImageCreator") and not (rhs[q:q + 1].isalnum() or rhs[q:q + 1] == "_"):
            # An alias back to the Image Playground type is not an app type of the same name.
            return False
    if generic or typedef or text[w + 1:b + 1] in DECL_WORDS:
        # A text scan cannot follow Swift lookup through nesting, extensions or subclasses, so any
        # app type of this name silences unqualified calls. Missing one is never worse than main.
        DECLARED = True
        return False
    t = k
    while t < end and text[t] in " \t":
        t += 1
    if t < end and text[t] in "?!":
        t2 = t + 1
        while t2 < end and text[t2] in " \t":
            t2 += 1
        if t2 < end and text[t2] in "(.":
            return True
    if t < end and text[t] in "(.":
        return True
    b = i - 1
    while b >= 0 and text[b] in " \t":
        b -= 1
    if b >= 0 and text[b] == "[":
        if t < end and (text[t].isalnum() or text[t] == "_"):
            return True
    return False

NEST = False
CUR = ""
DECLARED = False
HITS = []
SKIP = dict()
IMPORTS = set()
EXPORTED = []
QUIET = set()
CODE = dict()

def decl_generic(text, b):
    # True when the name opens or follows a comma in a generic parameter list, as in func f<T, ImageCreator>.
    if b < 0 or text[b] not in ("<", ","):
        return False
    depth = 0
    j = b if text[b] == "<" else b - 1
    while j >= 0:
        c = text[j]
        if c in "{};":
            return False
        if c == ">" and not (j and text[j - 1] == "-"):
            depth += 1
        elif c == "<":
            if depth == 0:
                break
            depth -= 1
        j -= 1
    if j < 0:
        return False
    head = text[max(0, j - 200):j].split()
    if head and head[-1] in ("init", "subscript"):
        return True
    return len(head) >= 2 and head[-2] in ("func", "struct", "class", "enum", "actor", "typealias", "protocol")

def no_comments(text):
    # Blank out comments and string contents with spaces, keeping every offset and line break.
    out = list(text)
    i, n, depth = 0, len(text), 0
    while i < n:
        if text.startswith("/*", i):
            depth += 1
            out[i] = out[i + 1] = " "
            i += 2
        elif depth and text.startswith("*/", i):
            depth -= 1
            out[i] = out[i + 1] = " "
            i += 2
        elif depth:
            if text[i] != chr(10):
                out[i] = " "
            i += 1
        elif text.startswith("//", i):
            e = text.find(chr(10), i)
            e = n if e < 0 else e
            for j in range(i, e):
                out[j] = " "
            i = e
        elif text[i] == "/" and text[i + 1:i + 2] not in ("", " ", "=", chr(10)) and (text[:i].rstrip()[-1:] in ("=", "(", ",", ":", "[", chr(123), "!", "&", "|", "?", ";") or text[:i].rstrip().endswith("return")):
            # A bare regex literal /.../ can hold braces.
            j = i + 1
            while j < n and text[j] != "/" and text[j] != chr(10):
                j += 2 if text[j] == chr(92) else 1
            if j < n and text[j] == "/":
                for m in range(i + 1, j):
                    out[m] = " "
                i = j + 1
            else:
                i += 1
        elif text[i] == "#" and text[i:].lstrip("#").startswith("/"):
            # A Swift regex literal #/.../# can hold braces and quotes.
            h = len(text[i:]) - len(text[i:].lstrip("#"))
            close = "/" + "#" * h
            e = text.find(close, i + h + 1)
            e = n if e < 0 else e
            for m in range(i + h + 1, e):
                if text[m] != chr(10):
                    out[m] = " "
            i = e + len(close)
        elif text[i] == "#" and text[i:].lstrip("#").startswith(chr(34)):
            h = len(text[i:]) - len(text[i:].lstrip("#"))
            q = chr(34) * 3 if text.startswith(chr(34) * 3, i + h) else chr(34)
            close = q + "#" * h
            j = i + h + len(q)
            e = text.find(close, j)
            e = n if e < 0 else e
            for m in range(j, e):
                if text[m] != chr(10):
                    out[m] = " "
            i = e + len(close)
        elif text[i] == chr(34):
            q = chr(34) * 3 if text.startswith(chr(34) * 3, i) else chr(34)
            j = i + len(q)
            while j < n and not text.startswith(q, j) and (len(q) == 3 or text[j] != chr(10)):
                if text[j] == chr(92):
                    if text[j] != chr(10):
                        out[j] = " "
                    j += 1
                if j < n and text[j] != chr(10):
                    out[j] = " "
                j += 1
            i = j + len(q)
        else:
            i += 1
    return "".join(out)

def gates_27(code, keys=("#unavailable(",)):
    # Code under #unavailable(iOS N), or in the else of #available(iOS N), runs only below N.
    # It never reaches 27 when every listed version N is 27.0 or lower.
    for key in keys:
        k = code.find(key)
        while k >= 0:
            e = code.find(")", k)
            vers = []
            for part in code[k + len(key):e if e > 0 else len(code)].replace(",", " ").split():
                nums = part.split(".")
                if nums[0].isdigit():
                    vers.append((int(nums[0]), int(nums[1]) if len(nums) > 1 and nums[1].isdigit() else 0))
            # 27.1 still lets 27.0 through, so the whole version must be 27.0 or lower.
            if vers and max(vers) <= (27, 0):
                return True
            k = code.find(key, k + 1)
    return False

def open_of(code, j):
    # The offset of the brace that the closing brace at j matches, or -1.
    level = 0
    while j >= 0:
        if code[j] == chr(125):
            level += 1
        elif code[j] == chr(123):
            level -= 1
            if level == 0:
                return j
        j -= 1
    return -1

def head_of(code, k, pos=False):
    # The condition before the brace at k. Scans back past parentheses, which hold any closure,
    # and across a line break only when the condition continues on the next line.
    depth = 0
    j = k - 1
    while j >= 0:
        c = code[j]
        if c == ")":
            depth += 1
        elif c == "(":
            depth -= 1
        elif depth <= 0 and c == chr(125) and not code[j + 1:k].strip():
            # A trailing closure right before the brace can belong to the condition, as in
            # if #unavailable(iOS 27), items.contains { $0 > 0 } { ... }.
            m = open_of(code, j)
            hm = head_of(code, m) if m > 0 and (code[:m].rstrip()[-1:].isalnum() or code[:m].rstrip()[-1:] in (")", "_")) else ""
            if hm.split(" ")[0] in ("if", "guard", "while") or hm.startswith("else if"):
                j = m - 1
                continue
            break
        elif depth <= 0 and c in (chr(123), chr(125), ";"):
            break
        elif depth <= 0 and c == chr(10):
            prev = code[code.rfind(chr(10), 0, j) + 1:j].rstrip()
            cur = code[j + 1:k].strip()
            # A blank line, including one that held a comment, does not end the condition.
            ends_kw = prev.split()[-1:] in (["guard"], ["if"], ["while"])
            if cur and prev.strip() and not ends_kw and not prev.endswith((",", "&&", "||", "(", "=")) and not cur.startswith((",", "&&", "||", ")", "else")):
                break
        j -= 1
    if pos:
        return j + 1
    h = " ".join(code[j + 1:k].split())
    for key in ("#available", "#unavailable"):
        h = h.replace(key + " (", key + "(")
    return h

def outer(h):
    # The condition with every parenthesised group removed except the version list of an availability check.
    out = []
    i = 0
    while i < len(h):
        if h[i] == "(" and not "".join(out).rstrip().endswith(("#available", "#unavailable")):
            depth = 0
            while i < len(h):
                depth += {"(": 1, ")": -1}.get(h[i], 0)
                i += 1
                if depth == 0:
                    break
            continue
        out.append(h[i])
        i += 1
    return "".join(out)

def alone(h, key, joins):
    # True when no other clause is joined to the availability check by joins.
    k = h.find(key)
    e = h.find(")", k)
    rest = h[:k] + h[e + 1:] if k >= 0 and e > 0 else h
    return not any(j in rest for j in joins)

def first_word(s):
    # The leading keyword of a statement, so return(nil) and if(x) read as return and if.
    m = re.match(r"\s*([A-Za-z_]+)", s)
    return m.group(1) if m else ""

def last_stmt(body, raw=False):
    # The last top-level statement of a block, split on semicolons and line breaks outside brackets.
    depth = 0
    cur = ""
    last = ""
    for i, c in enumerate(body):
        if c in "([" + chr(123):
            depth += 1
        elif c in ")]" + chr(125):
            depth -= 1
        nxt = body[i + 1:].lstrip(" " + chr(9))
        prev = cur.rstrip()
        if depth == 0 and c == chr(10) and prev and (cur.count(chr(34) * 3) % 2 == 1 or (nxt.startswith(".") and not nxt.startswith("..")) or nxt.startswith(chr(123)) or nxt.startswith(("? ", ": ", "?? ", "&& ", "|| ", "+ ", "- ", "* ", "/ ", "== ", "!= ", "< ", "> ", "<= ", ">= ")) or first_word(nxt) in ("else", "catch") or prev.split()[-1] in ("try", "try?", "try!", "await", "return", "throw") or prev[-1] in "=+-*/&|<>?:,"):
            # A line that starts with a member access, or sits inside a multiline string, continues the statement above.
            cur += " "
        elif depth == 0 and c in (";", chr(10)):
            if cur.strip():
                last = cur
            cur = ""
        else:
            cur += c
    out = cur if cur.strip() else last
    # raw keeps the line breaks, which a nested switch needs to find its case labels.
    return out.strip() if raw else " ".join(out.split())

def is_case_label(code, k):
    # A switch label, not .default, an enum case, or the pattern in if case and guard case.
    if k > 0 and (code[k - 1].isalnum() or code[k - 1] == "_"):
        return False
    before = code[:k].rstrip()
    line = code[:k].rsplit(chr(10), 1)[-1]
    if before.endswith("@unknown"):
        # @unknown default: is a switch label too.
        before = before[:-8].rstrip()
        line = line.rstrip()[:-8]
    if before.endswith((".", ",", "(", "[")) or (before.split() or [""])[-1] in ("if", "guard", "while", "for", "else", "enum", "indirect"):
        return False
    if line.strip() and not before.endswith((chr(123), chr(125), ";")):
        # A label starts a statement, so default: inside a call is an argument label.
        return False
    if code.startswith("case ", k):
        return True
    rest = code[k + 7:]
    return code.startswith("default", k) and rest.lstrip().startswith(":") and not (rest[:1].isalnum() or rest[:1] == "_")

def obsoleted_27(code, k):
    # True when the declaration that opens the brace at k is obsoleted at iOS 27 or earlier.
    seg = code[:k]
    # The declaration starts after the last brace or semicolon outside parentheses,
    # so a default closure in the parameter list does not cut it short.
    cut, level = -1, 0
    for i in range(len(seg) - 1, -1, -1):
        c = seg[i]
        if c == ")":
            level += 1
        elif c == "(":
            level -= 1
        elif level <= 0 and c in (chr(123), chr(125), ";"):
            cut = i
            break
    lines = seg[cut + 1:].split(chr(10))
    # Only the attributes of this declaration count: its own line and the attribute lines right above it.
    decl = len(lines) - 1
    while decl > 0 and not lines[decl].strip():
        decl -= 1
    # A signature can wrap, so start from the line that holds the declaration keyword.
    # Only a keyword outside parentheses counts, so a let inside a default closure is skipped.
    text = chr(10).join(lines)
    level, depth = 0, []
    for c in text:
        depth.append(level)
        level += {"(": 1, ")": -1}.get(c, 0)
    hits = [m.start(2) for m in re.finditer(r"(^|[^A-Za-z0-9_.])(func|init|subscript|var|let|struct|class|enum|actor|extension|protocol|typealias)([^A-Za-z0-9_]|$)", text) if depth[m.start(2)] == 0]
    if hits:
        decl = text.count(chr(10), 0, hits[-1])
    # Walk back over the attributes stacked on this declaration, each @name or @name(...), even across lines.
    head = chr(10).join(lines[:decl])
    keep = len(head)
    while True:
        t = head[:keep].rstrip()
        if t.endswith(")"):
            o = t.rfind("(")
            level = 0
            for o in range(len(t) - 1, -1, -1):
                level += {")": 1, "(": -1}.get(t[o], 0)
                if level == 0:
                    break
            m = re.search(r"@[A-Za-z_][A-Za-z0-9_.]*[ ]*$", t[:o])
        else:
            m = re.search(r"@[A-Za-z_][A-Za-z0-9_.]*$", t)
        if not m:
            break
        keep = m.start()
    seg = head[keep:] + chr(10) + chr(10).join(lines[decl:])
    for m in re.finditer(r"@available[ ]*[(]([^)]*)[)]", seg):
        args = [a.strip() for a in m.group(1).split(",")]
        if not args or args[0] not in ("iOS", "iPadOS", "iOSApplicationExtension", "macOS", "macCatalyst", "visionOS", "*"):
            continue
        for a in args[1:]:
            if a == "unavailable":
                # Unavailable on macOS, macCatalyst or visionOS still compiles the body for iOS.
                if args[0] in ("iOS", "iPadOS", "iOSApplicationExtension", "*"):
                    return True
                continue
            if a.startswith("obsoleted") and args[0] in ("iOS", "iPadOS", "iOSApplicationExtension"):
                v = a.split(":", 1)[-1].strip().split(".")
                if v[0].isdigit() and (int(v[0]), int(v[1]) if len(v) > 1 and v[1].isdigit() else 0) <= (27, 0):
                    return True
    return False

def body_exits(body):
    # True when a block always leaves the function. A trailing #if ... #endif exits
    # when it has an #else and every compiled branch exits.
    lines = [l for l in body.split(chr(10)) if l.strip()]
    if lines and lines[-1].strip().startswith("#endif"):
        depth, branches, cur, i = 0, [], [], len(lines) - 2
        has_else = False
        while i >= 0:
            t = lines[i].strip()
            if t.startswith("#endif"):
                depth += 1
            elif t.startswith("#if") and depth > 0:
                depth -= 1
            elif depth == 0 and (t.startswith("#else") or t.startswith("#elseif") or t.startswith("#if")):
                has_else = has_else or t.startswith("#else") and not t.startswith("#elseif")
                branches.append(chr(10).join(reversed(cur)))
                cur = []
                if t.startswith("#if"):
                    break
                i -= 1
                continue
            cur.append(lines[i])
            i -= 1
        return has_else and bool(branches) and all(body_exits(b) for b in branches)
    return stmt_exits(last_stmt(body, True))

def stmt_exits(stmt):
    # True when a statement always leaves the function: return, throw, continue,
    # or an if chain that ends in else and whose every branch does.
    first = first_word(stmt)
    if first in ("return", "throw", "continue"):
        return True
    if first == "switch":
        # A nested switch exits when every one of its cases does.
        o = stmt.find(chr(123))
        c = stmt.rfind(chr(125))
        return o > 0 and c > o and not stmt[c + 1:].strip() and switch_exits(stmt[o + 1:c])
    if first not in ("if", "do"):
        return False
    blocks, gaps, level, start, prev, paren = [], [], 0, -1, 0, 0
    for i, c in enumerate(stmt):
        if level == 0 and c in "([":
            paren += 1
        elif level == 0 and c in ")]":
            paren -= 1
        elif paren > 0:
            # A closure inside the condition, as in if xs.contains(where: { $0 > 0 }) { ... }.
            continue
        elif c == chr(123):
            if level == 0:
                gaps.append(stmt[prev:i])
                start = i
            level += 1
        elif c == chr(125):
            level -= 1
            if level == 0:
                blocks.append(stmt[start + 1:i])
                prev = i + 1
    tail = stmt[prev:].strip()
    if not blocks or tail:
        return False
    # Two blocks with nothing between them mean the first was a trailing closure in the condition.
    i = 1
    while i < len(blocks):
        if not gaps[i].strip():
            del blocks[i - 1]
            del gaps[i]
        else:
            i += 1
    if first == "do":
        # A do and its catches, each of which must exit.
        if gaps[0].strip() != "do" or not all(g.strip().startswith("catch") for g in gaps[1:]):
            return False
    elif gaps[-1].strip() != "else":
        return False
    return all(body_exits(b) for b in blocks)

def switch_exits(body):
    # True when every case of a switch body ends with return, throw, continue or break out.
    starts = []
    level = 0
    for i, c in enumerate(body):
        if c in "([" + chr(123):
            level += 1
        elif c in ")]" + chr(125):
            level -= 1
        elif level == 0 and c in "cd" and is_case_label(" " + body, i + 1):
            starts.append(i)
    if not starts:
        return False
    nxt = True
    for n in range(len(starts) - 1, -1, -1):
        a = starts[n]
        part = body[a:starts[n + 1] if n + 1 < len(starts) else len(body)]
        colon, lvl = -1, 0
        for ci, ch in enumerate(part):
            if ch in "([":
                lvl += 1
            elif ch in ")]":
                lvl -= 1
            elif ch == ":" and lvl == 0:
                # The label ends at the first colon outside the parentheses of an associated value.
                colon = ci
                break
        rest = part[colon + 1:] if colon >= 0 else ""
        last = last_stmt(rest, True)
        # fallthrough runs the next case, so it exits when that case does.
        here = body_exits(rest) or (first_word(last) == "fallthrough" and n + 1 < len(starts) and nxt)
        if not here:
            return False
        nxt = here
    return True

def split_top(h):
    # The comma-separated clauses of a condition, ignoring commas inside parentheses.
    parts, cur, depth = [], "", 0
    for c in h:
        depth += {"(": 1, ")": -1}.get(c, 0)
        if c == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += c
    return parts + [cur]

def else_below_27(code, k):
    # True when the else if holding k follows a branch whose whole condition is #available(iOS 27),
    # so its condition is only evaluated below 27.
    def start(at):
        q = head_of(code, at, True)
        while q < at and code[q].isspace():
            q += 1
        return q if code.startswith("else", q) else -1
    # The else that begins this condition, never one inside a closure in it.
    p = start(k)
    while p > 0:
        b = code.rfind(chr(125), 0, p)
        if b < 0 or code[b + 1:p].strip():
            return False
        m = open_of(code, b)
        if m <= 0:
            return False
        ph = outer(head_of(code, m))
        cond = ph[len("else if"):] if ph.startswith("else if") else ph[len("if"):] if ph.split(" ")[0] == "if" else None
        if cond is None:
            return False
        parts = split_top(cond)
        if len(parts) == 1 and gates_27(parts[0], ("#available(",)):
            return True
        if not ph.startswith("else if"):
            return False
        p = start(m)
    return False

def cond_gated(code, k):
    # True when k sits in a condition after a clause such as #unavailable(iOS 27), which
    # short-circuits, so the rest of the condition never runs on 27.
    h = outer(head_of(code, k))
    if not (h.split(" ")[0] in ("if", "guard", "while") or h.startswith("else if")):
        return False
    if h.startswith("else if") and else_below_27(code, k):
        return True
    parts, cur, depth = [], "", 0
    for c in h:
        depth += {"(": 1, ")": -1}.get(c, 0)
        if c == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += c
    return any(gates_27(p) for p in parts)

def gated_at(code, stop):
    # True when the block holding offset stop only runs below version 27.
    k = min(stop, len(code))
    return gated_many(code, [k])[k]

def gated_many(code, stops):
    # gated_at for every offset in stops, in one pass over the file.
    # One frame per open block: runs below 27, starts a lone #available chain, is a guard #unavailable.
    stack = []
    open_at = []
    # Chain state is kept per nesting depth, so a block nested in a branch cannot reset its chain.
    chain_at = dict()
    exits_at = dict()
    top = False
    want = sorted(set(min(x, len(code)) for x in stops))
    res = dict()
    wi = 0
    for k in range((want[-1] if want else 0) + 1):
        while wi < len(want) and want[wi] == k:
            res[k] = top or any(f[0] for f in stack) or obsoleted_27(code, k) or cond_gated(code, k)
            wi += 1
        if k >= len(code) or wi >= len(want):
            break
        c = code[k]
        if c == chr(123):
            d = len(stack)
            chain = chain_at.get(d, False)
            chain_exits = exits_at.get(d, False)
            open_at.append(k)
            h = outer(head_of(code, k))
            if h.split(" ")[0] in ("case", "default", "@unknown") and ":" in h:
                # The commas of a case label are not clauses of the if that follows it.
                h = h.split(":", 1)[1].strip()
            words = h.split()
            first = words[0] if words else ""
            # An else runs whenever any comma clause fails, so only a lone #available check counts.
            avail = gates_27(h, ("#available(",)) and alone(h, "#available(", (",",))
            unavail = gates_27(h)
            if first == "else" and "if" in words:
                # An else if branch runs only when every earlier condition failed.
                stack.append([chain or unavail, chain or avail, False, k if avail else -1, "elif", chain or unavail, -1])
            elif first == "else":
                stack.append([chain or unavail, chain, False, -1, "else", chain or unavail, -1])
            elif "guard" in words:
                stack.append([avail, False, unavail, -1, "guard", avail, -1])
            elif obsoleted_27(code, k):
                # @available(iOS, obsoleted: 27) on the declaration keeps its body off iOS 27.
                stack.append([True, False, False, -1, "other", True, -1])
            else:
                # A case label or a statement label can sit before the if.
                stack.append([unavail, avail, False, k if avail else -1, "if" if "if" in words else ("do" if first == "do" else ("switch" if first == "switch" else ("catch" if first == "catch" else "other"))), unavail, -1])
        elif stack and c in "cd" and is_case_label(code, k):
            # A case label starts a new path, so an early exit in an earlier case does not gate it.
            stack[-1][0] = stack[-1][5]
        elif c == chr(125) and stack:
            done = stack.pop()
            d = len(stack)
            chain_at[d] = done[1]
            chain_exits = exits_at.get(d, False)
            body = code[open_at[-1] + 1:k]
            # A block exits when its last statement does, or when it ends with an if and else that both exit.
            ends_out = first_word(last_stmt(body)) in ("return", "throw", "continue", "break") or body_exits(body) or (done[6] >= 0 and not code[done[6] + 1:k].strip(" ;" + chr(9) + chr(10)))
            exits = done[4] in ("if", "elif") and ends_out
            if done[4] == "else" and ends_out and chain_exits and stack:
                stack[-1][6] = k
            open_at.pop()
            all_before = chain_exits
            exits_at[d] = exits and (done[4] == "if" or chain_exits)
            # if #available(iOS 27) { ...; return } leaves only versions below 27 for the code after it,
            # and so does an else if one, when every earlier branch of the chain exits too.
            if done[3] >= 0 and exits and (done[4] == "if" or all_before):
                if stack:
                    stack[-1][0] = True
                else:
                    top = True
            if done[4] == "do" and done[0] and not done[5] and not code[k + 1:].lstrip().startswith("catch"):
                # A do block whose body returned on 27 leaves only versions below 27 after it.
                if stack:
                    stack[-1][0] = True
                else:
                    top = True
            if done[2]:
                # Code after guard #unavailable(iOS 27) else { return } runs only below 27.
                if stack:
                    stack[-1][0] = True
                else:
                    top = True
    # A declaration without a body, such as a typealias, carries its @available on the same statement.
    return res

def imports_ip(text):
    # import ImagePlayground in any form, with attributes, an access level or a declaration kind.
    how = ""
    # One line can hold several imports, as in import SwiftUI; import ImagePlayground.
    for line in (seg for row in text.split(chr(10)) for seg in row.split(";")):
        words = [w for w in line.split() if not w.startswith("@") and w not in ("public", "internal", "package", "private", "fileprivate")]
        if len(words) < 2 or words[0] != "import":
            continue
        m = words[2] if words[1] in ("typealias", "struct", "class", "enum", "protocol", "let", "var", "func") and len(words) > 2 else words[1]
        m = m.rstrip(";")
        if m.endswith(".ImageCreator") and not m.startswith("ImagePlayground."):
            # import struct Graphics.ImageCreator brings in a type of that name for this file only.
            return "other"
        if m == "ImagePlayground" or m.startswith("ImagePlayground."):
            # @_exported makes the module visible in every file of the app.
            if "@_exported" in line.split():
                how = "exported"
            elif not how:
                how = "file"
    return how

def cond_value(cond):
    # The value of an #if condition in a Release build for an Apple platform.
    # T true, F false, P platform check (kept, later branches still possible), U unknown.
    toks = []
    c = cond.split("//")[0].strip()
    i = 0
    while i < len(c):
        ch = c[i]
        if ch.isspace():
            i += 1
        elif c.startswith("&&", i) or c.startswith("||", i):
            toks.append(c[i:i + 2])
            i += 2
        elif ch in "!()":
            toks.append(ch)
            i += 1
        else:
            j = i
            while j < len(c) and (c[j].isalnum() or c[j] in "_."):
                j += 1
            if j == i:
                return "U"
            name = c[i:j]
            if j < len(c) and c[j] == "(":
                e = c.find(")", j)
                if e < 0:
                    return "U"
                toks.append((name, c[j + 1:e].replace(" ", "")))
                i = e + 1
            else:
                toks.append((name, None))
                i = j
    pos = [0]

    def atom(t):
        name, arg = t
        if arg is None:
            return "F" if name == "DEBUG" else ("T" if name == "true" else "F" if name == "false" else "U")
        if name in ("os", "canImport", "arch", "targetEnvironment", "hasFeature", "hasAttribute"):
            return "P"
        if name in ("compiler", "swift") and arg.startswith((">=", "<")):
            op = ">=" if arg.startswith(">=") else "<"
            ver = arg[len(op):].split(".")
            try:
                v = (int(ver[0]), int(ver[1]) if len(ver) > 1 else 0)
            except ValueError:
                return "U"
            # ImageCreator needs Swift 6.1 or later, so any toolchain that builds it is at least 6.1.
            if v <= (6, 1):
                return "T" if op == ">=" else "F"
        return "U"

    def unary():
        if pos[0] >= len(toks):
            return "U"
        t = toks[pos[0]]
        pos[0] += 1
        if t == "!":
            v = unary()
            return {"T": "F", "F": "T"}.get(v, v)
        if t == "(":
            v = disj()
            if pos[0] < len(toks) and toks[pos[0]] == ")":
                pos[0] += 1
                return v
            return "U"
        if isinstance(t, tuple):
            return atom(t)
        return "U"

    def conj():
        vals = [unary()]
        while pos[0] < len(toks) and toks[pos[0]] == "&&":
            pos[0] += 1
            vals.append(unary())
        if "F" in vals:
            return "F"
        if "U" in vals:
            return "U"
        return "P" if "P" in vals else "T"

    def disj():
        vals = [conj()]
        while pos[0] < len(toks) and toks[pos[0]] == "||":
            pos[0] += 1
            vals.append(conj())
        if "T" in vals:
            return "T"
        if "U" in vals:
            return "U"
        return "P" if "P" in vals else "F"

    v = disj()
    return v if pos[0] == len(toks) else "U"

def cond_lines(text):
    # Lines a Release build does not compile. A branch whose flag cannot be
    # evaluated, such as a custom PRO flag, counts as compiled and is reported.
    out = set()
    stack = []
    for n, raw in enumerate(text.split(chr(10)), 1):
        s = raw.strip()
        if s.startswith("#elseif"):
            if stack:
                stack[-1]["branches"].append((n, cond_value(s[7:])))
        elif s.startswith("#else"):
            if stack:
                stack[-1]["branches"].append((n, "T"))
        elif s.startswith("#if"):
            stack.append({"start": n, "branches": [(n, cond_value(s[3:]))]})
        elif s.startswith("#endif"):
            if stack:
                chain = stack.pop()
                br = chain["branches"]
                live = True
                for idx, (bn, v) in enumerate(br):
                    end_n = br[idx + 1][0] if idx + 1 < len(br) else n
                    if not live or v == "F":
                        out.update(range(bn, end_n + 1))
                    if v == "T":
                        live = False
                out.add(n)
    return out
DECL_WORDS = ("struct", "class", "enum", "actor", "typealias", "protocol", "associatedtype", "interface", "implementation", "using")

def block_end(text, i, end):
    # Swift block comments nest, Objective-C ones do not. Returns where the comment closes, or -1.
    if not NEST:
        return text.find("*/", i + 2, end)
    depth = 0
    while i < end:
        if text.startswith("/*", i):
            depth += 1
            i += 2
        elif text.startswith("*/", i):
            depth -= 1
            if depth == 0:
                return i
            i += 2
        else:
            i += 1
    return -1

def walk(text, i, end, line, stop_paren):
    depth = 0
    while i < end:
        ch = text[i]
        if ch == "\n":
            line += 1
            i += 1
            continue
        if stop_paren and ch == ")" and depth == 0:
            return 0, i, line
        if text.startswith("//", i):
            nl = text.find("\n", i, end)
            if nl < 0:
                return 0, end, line
            i = nl
            continue
        if text.startswith("/*", i):
            close = block_end(text, i, end)
            if close < 0:
                line += text.count("\n", i, end)
                return 0, end, line
            line += text.count("\n", i, close + 2)
            i = close + 2
            continue
        h = 0
        j = i
        while j < end and text[j] == "#":
            h += 1
            j += 1
        if h and j < end and text[j] == '"':
            got, i, line = skip_delim(text, j, end, line, h, text.startswith('"""', j))
            if got:
                return got, i, line
            continue
        if h and j < end and text[j] == "/":
            # An extended regex literal #/.../# holds pattern text, never a call.
            close = text.find("/" + "#" * h, j + 1, end)
            stop_at = end if close < 0 else close + 1 + h
            line += text.count(chr(10), i, stop_at)
            i = stop_at
            continue
        if ch == "/" and text[i + 1:i + 2] not in ("", " ", "=", chr(10), "/", "*") and (text[:i].rstrip()[-1:] in ("=", "(", ",", ":", "[", chr(123), "!", "&", "|", "?", ";") or text[:i].rstrip().endswith("return")):
            # A bare regex literal /.../ on one line.
            r = i + 1
            while r < end and text[r] not in ("/", chr(10)):
                r += 2 if text[r] == chr(92) else 1
            if r < end and text[r] == "/":
                i = r + 1
                continue
        if ch == "@" and i + 1 < end and text[i + 1] == '"':
            got, i, line = skip_delim(text, i + 1, end, line, 0, False, True)
            if got:
                return got, i, line
            continue
        if text.startswith('"""', i):
            got, i, line = skip_delim(text, i, end, line, 0, True)
            if got:
                return got, i, line
            continue
        if ch == '"':
            got, i, line = skip_delim(text, i, end, line, 0, False)
            if got:
                return got, i, line
            continue
        if ch == "'":
            i = skip_char(text, i, end)
            continue
        if use_at(text, i, end):
            b = i - 1
            while b >= 0 and text[b] in (" ", chr(9)):
                b -= 1
            qual = False
            if b >= 0 and text[b] == ".":
                a = b - 1
                while a >= 0 and text[a] in (" ", chr(9)):
                    a -= 1
                mod = "ImagePlayground"
                s0 = a + 1 - len(mod)
                qual = s0 >= 0 and text[s0:a + 1] == mod and not (s0 and (text[s0 - 1].isalnum() or text[s0 - 1] == "_"))
            # Under any other namespace, Foo.ImageCreator is the app own type.
            if qual or not (b >= 0 and text[b] == "."):
                HITS.append((CUR, line, qual, i))
            i += len("ImageCreator")
            continue
        if ch == "(":
            depth += 1
        elif ch == ")" and depth:
            depth -= 1
        i += 1
    return 0, i, line

def skip_char(text, i, end):
    j = i + 1
    if j < end and text[j] == "\\":
        j += 2
    elif j < end and text[j] != "'":
        j += 1
    if j < end and text[j] == "'":
        return j + 1
    return i + 1

def skip_delim(text, i, end, line, h, triple, objc=False):
    closer = '"""' if triple else '"'
    i += len(closer)
    while i < end:
        if text[i] == "\n":
            line += 1
            i += 1
            continue
        if text[i] == "\\" and text.startswith("#" * h, i + 1):
            j = i + 1 + h
            if not objc and j < end and text[j] == "(":
                got, i, line = walk(text, j + 1, end, line, True)
                if got:
                    return got, i, line
                if i < end and text[i] == ")":
                    i += 1
                continue
            i = j + (1 if j < end else 0)
            continue
        if text.startswith(closer, i) and text.startswith("#" * h, i + len(closer)):
            return 0, i + len(closer) + h, line
        i += 1
    return 0, i, line

for path in sys.stdin.read().split(chr(10)):
    if not path:
        continue
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError:
        continue
    NEST = path.endswith(".swift")
    CUR = path
    walk(text, 0, len(text), 1, False)
    if NEST:
        SKIP[path] = cond_lines(text)
        code = no_comments(text)
        how = imports_ip(code)
        CODE[path] = code
        if how == "other":
            QUIET.add(path)
            how = "file"
        if how:
            IMPORTS.add(path)
        if how == "exported":
            EXPORTED.append(path)
# A typealias to the Apple type, as in typealias Gen = ImageCreator, makes Gen another name for it.
ALIAS_HIT = set()
for src, scode in list(CODE.items()):
    for am in re.finditer(r"(?<![A-Za-z0-9_.])typealias\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(ImagePlayground\s*\.\s*)?ImageCreator(?![A-Za-z0-9_.<])", scode):
        name, aq = am.group(1), bool(am.group(2))
        if name == "ImageCreator" or not (src in IMPORTS or EXPORTED) or (not aq and src in QUIET):
            continue
        use = re.compile(r"(?<![A-Za-z0-9_.])" + re.escape(name) + r"\s*[?!]?[ \t]*[" + chr(40) + ".]")
        for p, pcode in CODE.items():
            for um in use.finditer(pcode):
                HITS.append((p, pcode.count(chr(10), 0, um.start()) + 1, aq, um.start()))
                ALIAS_HIT.add((p, um.start()))
# With an app type of that name, only a call qualified as ImagePlayground.ImageCreator is the Apple one.
# ImageCreator is Swift-only, so only a Swift file that imports ImagePlayground can name it.
# Only the first ungated hit is printed, so stop there, and run the costly gated_at check last.
live = [h for h in HITS if ((h[0], h[3]) in ALIAS_HIT or (h[2] or h[0] not in QUIET) and (h[0] in IMPORTS or (EXPORTED and h[0].endswith(".swift")))) and (h[2] or not DECLARED) and h[1] not in SKIP.get(h[0], ())]
GATED = dict()
for h in live:
    if h[0] not in GATED:
        code = CODE.get(h[0], "")
        GATED[h[0]] = gated_many(code, [x[3] for x in live if x[0] == h[0]])
pick = next((h for h in live if not GATED[h[0]][min(h[3], len(CODE.get(h[0], "")))]), None)
if pick:
    sys.stdout.write("%s:%s" % (pick[0], pick[1]) + chr(10))
ICPY
)" 2>/dev/null)" || true
  [ -n "$out" ] || return 1
  IMAGECREATOR_HIT="${out%%$'\n'*}"
  IMAGECREATOR_HIT="${IMAGECREATOR_HIT#"${DIR%/}"/}"
  return 0
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
    FNR == 1 { blk=0 }
    { l=$0; if (index(l, "/") == 0 && index(l, "*") == 0) { blk=0; print l; next }
      t=l; sub(/^[ \t]+/, "", t)
      if (substr(t, 1, 2) == "//") { print ""; next }
      if (substr(t, 1, 2) == "*/") { blk=0; print substr(t, 3); next }
      # With gate=1 a leading * is comment text only in the unbroken run of lines right under a line that
      # opens /*. Any other line ends the run, so a /* misread in a string or regex hides no code (#2421).
      if ((!gate || blk) && (t == "*" || substr(t, 1, 2) == "* " || substr(t, 1, 2) == "*\t")) { if (index(t, "*/")) blk=0; print ""; next }
      if (substr(t, 1, 2) == "/*") { r=t; sub(/[ \t]+$/, "", r); j=index(substr(r, 3), "*/")
        if (j == 0) { blk=1; print ""; next }
        if (j + 3 == length(r)) { print ""; next } }
      blk=0
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
ship_has() {  # grep_has over the files that ship. Test files are left out when nothing imports them
  [ "${SHIPLIST:-$FILELIST}" = "$FILELIST" ] && { grep_has "$1"; return; }
  [ -s "$SHIPLIST" ] || return 1
  # Test the output, not the exit code. xargs splits a long list into batches, and one batch
  # with no match would otherwise make the whole pipeline fail under pipefail.
  [ -n "$(tr '\n' '\0' < "$SHIPLIST" | xargs -0 grep -EIl -e "$1" 2>/dev/null | head -n 1)" ]
}
# RELEASE_HIT is set to the file and line of the string that matched, for the finding to name (issue #2397).
release_string_has() {
  RELEASE_HIT=""
  [ -s "$FILELIST" ] || return 1
  local f m src
  while IFS= read -r f; do
    # Source comments go first (issue #2413). STRIP_AWK keeps one line per line and, with gate=1, only blanks
    # a line that itself looks like a comment, so a /* in a string or regex never hides later lines (#2421).
    # It runs in the C locale, and the raw file is read if awk still fails, so no byte can hide a file.
    src=""
    if [[ "$f" =~ $SRC_EXT_RE ]]; then src="$(LC_ALL=C awk -v tc=1 -v gate=1 "$STRIP_AWK" "$f" 2>/dev/null)" || src="$(cat "$f" 2>/dev/null)"; fi
    # Removed lines print empty, so a line number counts the lines of a DEBUG block too.
    case "$f" in
      *.swift)
        m="$(printf '%s\n' "$src" | LC_ALL=C awk '
          /^[ \t]*#if/    { d++; if ($0 ~ /#if[ \t]+DEBUG/ || $0 ~ /#if[ \t]+!RELEASE/) { dbg=d; skip=1 } print ""; next }
          /^[ \t]*#else/  { if (skip && d==dbg) skip=0; print ""; next }
          /^[ \t]*#elseif/ { print ""; next }
          /^[ \t]*#endif/ { if (skip && d==dbg) { skip=0; dbg=0 } d--; print ""; next }
          skip { print ""; next }
          { print }
        ' 2>/dev/null | LC_ALL=C grep -aEn "\"[^\"]*($1)[^\"]*\"" 2>/dev/null)" ;;
      *)
        if [[ "$f" =~ $SRC_EXT_RE ]]; then
          m="$(LC_ALL=C grep -aEn "\"[^\"]*($1)[^\"]*\"" <<< "$src" 2>/dev/null)"
        else
          m="$(LC_ALL=C grep -aEn "\"[^\"]*($1)[^\"]*\"" "$f" 2>/dev/null)"
        fi ;;
    esac
    # NOTE. no `grep -q` or `-m 1`. Either one stops reading early, the awk producer gets SIGPIPE,
    # and pipefail reports a miss though grep matched (timing-dependent, seen on the CI runner).
    # Plain grep drains its input. Only the captured output is read, never the exit status.
    if [ -n "$m" ]; then RELEASE_HIT="${f#"${DIR%/}"/}:${m%%:*}"; return 0; fi
  done < "${SHIPLIST:-$FILELIST}"
  return 1
}

# Prints the first file and line that match, relative to the scanned folder. $1 is src, ship, manifest or apple.
# ship reads SHIPLIST, so a check that leaves test files out never names one (issue #2397).
hit_file() {
  [ -s "$FILELIST" ] || return 0
  local f n
  if [ "$1" = "manifest" ]; then
    f="$(grep '/AndroidManifest[.]xml$' "$FILELIST" | tr '\n' '\0' | xargs -0 grep -EIls -e "$2" 2>/dev/null | head -1)"
  elif [ "$1" = "ship" ]; then
    f="$(tr '\n' '\0' < "${SHIPLIST:-$FILELIST}" | xargs -0 grep -EIls -e "$2" 2>/dev/null | head -1)"
  elif [ "$1" = "apple" ]; then
    f="$(grep -E "$APPLE_SRC_RE" "$FILELIST" | tr '\n' '\0' | xargs -0 grep -EIls -e "$2" 2>/dev/null | head -1)"
  else
    f="$(tr '\n' '\0' < "$FILELIST" | xargs -0 grep -EIls -e "$2" 2>/dev/null | head -1)"
  fi
  [ -n "$f" ] || return 0
  n="$(grep -En -m1 -e "$2" "$f" 2>/dev/null | cut -d: -f1)"
  printf '%s%s' "${f#"${DIR%/}"/}" "${n:+:$n}"
}

# Findings are held and printed by flush_findings, critical first (issue #842).
F_CRIT=(); F_HIGH=(); F_MED=(); FOUND_IDS=""; POOL_PASS=0
finding() {  # severity id title fix [src|manifest regex | at file:line]. The optional pair names the file that triggered it.
  local t w=""
  case "$FOUND_IDS" in *"|$1:$2|"*) [ "$POOL_PASS" -eq 1 ] && return 0 ;; esac
  FOUND_IDS="$FOUND_IDS|$1:$2|"
  case "${5:-}" in at) w="${6:-}" ;; ?*) w="$(hit_file "$5" "${6:-}")" ;; esac
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
# A hook lets an unchecked submit through by default. APP_STORE_GUARD_BLOCK_UNCHECKED=1 stops it instead.
block_unchecked() {
  [ "${APP_STORE_GUARD_BLOCK_UNCHECKED:-0}" = "1" ] || return 0
  if declare -F emit_report >/dev/null; then
    echo "BLOCKED. Nothing was checked, and APP_STORE_GUARD_BLOCK_UNCHECKED=1 is set."; emit_report 2
  else cursor_reply 2; fi
  echo "$1 Blocked because APP_STORE_GUARD_BLOCK_UNCHECKED=1." >&2; exit 2
}
FILELIST="$(mktemp 2>/dev/null)" || FILELIST=""
{ [ -n "$FILELIST" ] && : > "$FILELIST" 2>/dev/null; } || FILELIST="/tmp/ascg.$$"
# No scan buffer means no scan. Say so rather than end CLEAR on an empty file list.
if [ -z "$FILELIST" ] || ! : > "$FILELIST" 2>/dev/null; then
  NOTE="NOT CHECKED. The guard could not create its scan buffer in ${TMPDIR:-/tmp}, so nothing was scanned. Point TMPDIR at a writable folder and run it again."
  if [ -n "$STDIN_JSON" ]; then block_unchecked "$NOTE"; echo "app-store-compliance-guard. $NOTE" >&2; cursor_reply 0; exit 0; fi
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
# JS and TS test files (*.test.ts, *.spec.tsx) sit next to the code they test and never ship, unless
# app code or a web page names one (an import, a require, a <script src>). Then every test file stays.
JS_TEST_RE='[.](test|spec)[.][jt]sx?$'
# Vue, Svelte, Astro, .mjs and .cjs files are not in the source list, so they are found here, outside test folders.
# A glob or context import (import.meta.glob, require.context) can bundle a test file unnamed, so it keeps them too.
TEST_IMPORTERS="$({ grep -E '[.]([cm]?[jt]sx?|html?|vue|svelte|astro)$' "$FILELIST" 2>/dev/null | grep -vE "$JS_TEST_RE"
  find "$DIR" -mindepth 1 -maxdepth 8 \( -type d \( -name node_modules -o -name .git -o -name Pods -o -name build -o -name dist -o -name DerivedData -o -name vendor \
    -o -name '*Tests' -o -name androidTest -o -name __tests__ -o -name test -o -name tests -o -name integration_test -o -name e2e \) -prune \) \
    -o -type f \( -name '*.vue' -o -name '*.svelte' -o -name '*.astro' -o -name '*.html' -o -name '*.htm' -o -name '*.mjs' -o -name '*.cjs' \) -print 2>/dev/null; } \
  | tr '\n' '\0' | xargs -0 grep -EIl -e "['\"\`][^'\"\`]*[.](test|spec)([.][cm]?[jt]sx?)?([?#][^'\"\`]*)?['\"\`]" -e "=[[:space:]]*[^[:space:]>='\"\`]*[.](test|spec)[.][cm]?[jt]sx?([?#][^[:space:]>]*)?([[:space:]>]|$)" -e 'import[.]meta[.]glob|require[.]context' 2>/dev/null || true)"
# Expo Router bundles every file under app/ as a route, test files included, so those stay.
ROUTE_KEEP='^$'
grep '/package[.]json$' "$FILELIST" 2>/dev/null | tr '\n' '\0' | xargs -0 grep -Il '"expo-router"' 2>/dev/null | grep . >/dev/null && ROUTE_KEEP='/app/'
# Test files stay in the source list, so they still count as evidence the way they always did.
# Only the release-string checks (staging host, placeholder text) read SHIPLIST, which leaves them out.
# CI config, end-to-end flows and npm scripts never ship either, imported or not (issue #2397).
# Matched below the project root, so a project that itself sits in a folder named e2e is still read.
NOSHIP_RE='(^|/)([.]github|[.]circleci|[.]gitlab|[.]buildkite|[.]maestro|__e2e__|e2e)/|(^|/)([.]gitlab-ci|bitrise|codemagic|[.]travis|azure-pipelines)[.]ya?ml$'
# package.json ships only when code imports or requires it. Any path naming package.json counts, an
# extensionless one through a relative or alias path. Vue, Svelte, Astro and .mjs files are not in the source list, so they are found here too.
{ grep -v '/package[.]json$' "$FILELIST" 2>/dev/null
  find "$DIR" -mindepth 1 -maxdepth 8 \( -type d \( -name node_modules -o -name .git -o -name Pods -o -name build -o -name dist -o -name DerivedData -o -name vendor \) -prune \) \
    -o -type f \( -name '*.vue' -o -name '*.svelte' -o -name '*.astro' -o -name '*.mjs' -o -name '*.cjs' \) -print 2>/dev/null; } \
  | tr '\n' '\0' | xargs -0 grep -IlE "['\"\`]([^'\"\`]*package[.]json|[^'\"\`]*/package)([?][^'\"\`]*)?['\"\`]" 2>/dev/null | grep . >/dev/null \
  || NOSHIP_RE="$NOSHIP_RE|(^|/)package[.]json\$"
SHIP_TEST_RE='^$'
[ -z "$TEST_IMPORTERS" ] && SHIP_TEST_RE="$JS_TEST_RE"
SHIPLIST="$FILELIST"
if awk -v root="${DIR%/}/" -v n="$NOSHIP_RE" -v t="$SHIP_TEST_RE" -v k="$ROUTE_KEEP" \
     '{ p = (index($0, root) == 1) ? substr($0, length(root) + 1) : $0 } (p !~ n && $0 !~ t) || $0 ~ k' \
     "$FILELIST" > "$FILELIST.ship" 2>/dev/null && ! cmp -s "$FILELIST" "$FILELIST.ship"; then
  SHIPLIST="$FILELIST.ship"
fi
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
# Apple HIG, Privacy. a custom pre-alert screen titles its one button Continue or Next, never Allow.
# A button and a permission request in one Apple source file is evidence, so it is reported as possible.
PERM_REQ_RE='requestWhenInUseAuthorization|requestAlwaysAuthorization|requestTrackingAuthorization|requestAuthorization[(:]|requestAuthorizationWithOptions|requestAccess[(:]|requestAccessForMediaType|requestRecordPermission|request[(][[:space:]]*PERMISSIONS[.]IOS|requestMultiple[(][[:space:]]*[[]?[[:space:]]*PERMISSIONS[.]IOS|request[A-Za-z]*PermissionsAsync|Permission[.][A-Za-z]+[.]request[(]'
ALLOW_BTN_RE='(Button[(][[:space:]]*(LocalizedStringKey[(]|String[(]localized:[[:space:]]*|NSLocalizedString[(])?|setTitle[(]|setTitle:[[:space:]]*@|<Button[^>]*title=[{]?)["'"'"'`]Allow([[:space:]][A-Za-z ]{0,30})?["'"'"'`]'
ANDROID_SRC_RE='(^|/)android/|[.]android[.][A-Za-z]+$|[.](kt|kts|java)$'
strip_comments() {  # $1 file. Blanks // and /* */ comments outside strings, keeping line numbers
  local nest=0
  case "$1" in *.swift) nest=1 ;; esac
  awk -v nest="$nest" 'BEGIN { inb = 0; ml = 0 }
  { o = ""; if (q != "`") q = ""; n = length($0); i = 1
    while (i <= n) {
      c = substr($0, i, 1); t = substr($0, i, 2)
      if (ml) { o = o c; if (substr($0, i, 3) == "\"\"\"") { o = o "\"\""; ml = 0; i += 3 } else i++; continue }
      if (inb) {
        if (t == "*/") { inb--; i += 2 } else if (nest && t == "/*") { inb++; i += 2 } else i++
        continue
      }
      if (q == "#") { o = o c; if (t == "\"#") { o = o "#"; q = ""; i += 2 } else i++; continue }
      if (q != "") { o = o c; if (c == "\\") { o = o substr($0, i + 1, 1); i += 2; continue }; if (c == q) q = ""; i++; continue }
      if (t == "#\"") { o = o t; q = "#"; i += 2; continue }
      if (substr($0, i, 3) == "\"\"\"") { o = o "\"\"\""; ml = 1; i += 3; continue }
      if (t == "/*") { inb = 1; i += 2; continue }
      if (t == "//") break
      if (c == "\"" || c == "`" || c == "'"'"'") q = c
      o = o c; i++
    }
    print o }' "$1" 2>/dev/null
}
pre_prompt_hit() {  # prints path:line of an Allow button in an Apple source file that also requests a permission
  local f src hit
  while IFS= read -r f <&4; do
    src="$(strip_comments "$f")"
    # grep without -q reads all its input, so a large file never loses the match to SIGPIPE under pipefail.
    printf '%s\n' "$src" | grep -E -e "$PERM_REQ_RE" >/dev/null || continue
    hit="$(printf '%s\n' "$src" | grep -En -e "$ALLOW_BTN_RE" | head -1 | cut -d: -f1)"
    if [ -n "$hit" ]; then printf '%s:%s\n' "$f" "$hit"; return 0; fi
  done 4< <(grep -E "$SRC_EXT_RE" "$FILELIST" | grep -Ev "$ANDROID_SRC_RE" | tr '\n' '\0' | xargs -0 grep -El -e "$PERM_REQ_RE" 2>/dev/null | tr '\n' '\0' | xargs -0 grep -l -e 'Allow' 2>/dev/null)
  return 1
}
if [ "$IOS_TARGET_ACTIVE" -eq 1 ] && [ -s "$FILELIST" ]; then
  PRE_PROMPT_HIT="$(pre_prompt_hit)"
  if [ -n "$PRE_PROMPT_HIT" ]; then
    PRE_PROMPT_AT="${PRE_PROMPT_HIT#"${DIR%/}"/}"
    finding medium "APPLE-5.1.1-PRE-PROMPT-ALLOW-BUTTON" "Possible pre-permission screen with a button titled Allow, at $PRE_PROMPT_AT" "If this screen comes before a system permission alert, title its one button Continue or Next and let the alert ask. Add another action only to collect legally required consent (Apple HIG Privacy, Guideline 5.1.1(iv)). A Settings toggle or a plain label is fine."
  fi
fi
# Genuine placeholder CONTENT only. the bare word "placeholder" matches every SwiftUI
# `placeholder:` parameter and a "TODO"/"FIXME" matches normal dev comments, neither of which is a
# rejection cause, so match real placeholder markers a reviewer would actually see.
if ship_has 'lorem ipsum|example\.(com|org)|YOUR_[A-Z_]+_(KEY|HERE)|INSERT_[A-Z_]+_HERE|dummy (text|content|data)|(john|jane)@example|"Acme( Inc| Corp)?"'; then
  finding high "BOTH-PLACEHOLDER" "Placeholder content (lorem ipsum, example.com, dummy text) found in sources" "Replace placeholder text and assets with real content." ship 'lorem ipsum|example\.(com|org)|YOUR_[A-Z_]+_(KEY|HERE)|INSERT_[A-Z_]+_HERE|dummy (text|content|data)|(john|jane)@example|"Acme( Inc| Corp)?"'
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
      if printf '%s' "$EX_PERMS" | grep_q 'ACCESS_BACKGROUND_LOCATION' || ex_cfg "isAndroidBackgroundLocationEnabled[\"']?[[:space:]]*:[[:space:]]*true"; then
        finding critical "GOOGLE-PERM-BACKGROUND-LOCATION" "Background location requested in the Expo app config" "Justify with a core feature and prominent disclosure, or use foreground location."
      fi
      if printf '%s' "$EX_PERMS" | grep_q -E 'READ_SMS|SEND_SMS|RECEIVE_SMS|READ_CALL_LOG|WRITE_CALL_LOG'; then
        finding critical "GOOGLE-PERM-SMS-CALLLOG" "SMS or Call Log permission in the Expo app config" "Use the permissions declaration for an approved core use case, or drop it."
      fi
      if printf '%s' "$EX_PERMS" | grep_q 'MANAGE_EXTERNAL_STORAGE'; then
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
    finding critical "APPLE-2.1-STAGING-BACKEND" "A release-build string points at localhost or a staging host" "Point the release build at the live production backend. A localhost/staging URL inside #if DEBUG or a comment is fine. this only flags strings the release build actually compiles." at "$RELEASE_HIT"
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
js_apple_login_started() {  # 0 if JS or TS code calls signInAsync( or performRequest({... Operation.LOGIN ...})
    [ -s "$FILELIST" ] || return 1
    grep -E '[.][cm]?[jt]sx?$' "$FILELIST" | tr '\n' '\0' | xargs -0 python3 -c "$(cat <<'SIWAPY'
import re
import sys

TOKEN = re.compile(r'"(?:\\.|[^"\\\n])*"|' + r"'(?:\\.|[^'\\\n])*'|" + r"\x60(?:\\.|[^\x60\\])*\x60|/[*].*?[*]/|//[^\n]*", re.S)
EXPO = re.compile(r"AppleAuthentication\s*[.]\s*signInAsync\s*[(]")
INVERTASE = re.compile(r"[.]performRequest\s*[(]\s*[{][^{}]*?requestedOperation\s*:\s*appleAuth\s*[.]\s*Operation\s*[.]\s*LOGIN\b", re.S)
for path in sys.argv[1:]:
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            code = TOKEN.sub(" ", fh.read())
    except OSError:
        continue
    if EXPO.search(code) or INVERTASE.search(code):
        sys.exit(0)
sys.exit(1)
SIWAPY
  )" 2>/dev/null
  }
  if grep_has 'FacebookLogin|GoogleSignIn|GIDSignIn|LoginWithFacebook'; then
    # React Native and Expo sign in with Apple through a JS library. Only a started login counts, read
    # with comments and strings removed. Buttons, enums, options objects and logout do not.
    grep_has 'SignInWithApple|ASAuthorizationAppleIDProvider' || js_apple_login_started || finding high "APPLE-4.8-SOCIAL-LOGIN-ONLY" "Third party social login without Sign in with Apple" "Add Sign in with Apple or an equal privacy preserving login (Apple 4.8)." src 'FacebookLogin|GoogleSignIn|GIDSignIn|LoginWithFacebook'
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
  # ImageCreator is discontinued in iOS 27, iPadOS 27, macOS 27, and visionOS 27 (Apple news dz9wvq0r, 11 June 2026).
  # A call or member use counts outside #if chains that Release may drop. The sheet does not.
  if apple_imagecreator_hit; then
    finding high "APPLE-IMAGEPLAYGROUND-IMAGECREATOR-DISCONTINUED" "ImageCreator will not work on iOS 27 or later" "Present the Image Playground sheet (ImagePlaygroundViewController or imagePlaygroundSheet), or use another image generation service, before the public release of iOS 27, iPadOS 27, macOS 27, and visionOS 27." at "$IMAGECREATOR_HIT"
  fi
  # A Podfile has no extension, so it is outside the source list. Read it directly.
  podfile_below_ios13() {
    find "$DIR" -maxdepth 4 \( -type d \( -name Pods -o -name node_modules \) -prune \) -o -name Podfile -type f -print 2>/dev/null \
      | awk 'NR <= 5' | while IFS= read -r pf; do if grep -Eq "^[[:space:]]*platform[[:space:]]+:ios,[[:space:]]*.(8|9|10|11|12)([.][0-9]+)*." "$pf"; then echo hit; fi; done | grep_q hit
  }
  # App Store Connect refuses uploads that target below iOS 13 (Upcoming Requirements page).
  pbx_below_ios13() {  # reads the app target's build settings, never a framework's or a test bundle's
    [ -s "$FILELIST" ] || return 1
    command -v python3 >/dev/null 2>&1 || return 1
    local pf
    pf="$(grep '[.]xcodeproj/project[.]pbxproj$' "$FILELIST")"
    [ -n "$pf" ] || return 1
    printf '%s\n' "$pf" | tr '\n' '\0' | xargs -0 python3 -c "$(cat <<'PBXPY'
import re
import sys

BLOCK_RE = re.compile(
    r"isa = XCBuildConfiguration;.*?buildSettings = \{(.*?)\n\s*\};", re.S
)
DT_RE = re.compile(
    r"IPHONEOS_DEPLOYMENT_TARGET(?:\[[^\]]*\])?\s*=\s*\"?([0-9]+)(?:\.[0-9]+)*\"?\s*;"
)
# Xcode writes an SDK-conditional key in quotes. Only the device SDK ships, and only a value
# below the minimum is read from it, so a quoted key can add a finding but never hide one.
QDT_RE = re.compile(r'"IPHONEOS_DEPLOYMENT_TARGET\[sdk=iphoneos[*]\]"\s*=\s*"?([0-9]+)')
CONDITIONAL_RE = re.compile(r'IPHONEOS_DEPLOYMENT_TARGET\[')
COMMENT_RE = re.compile(r"//[^\n]*|/[*].*?[*]/", re.S)
PROJECT_RE = re.compile(r"isa = PBXProject;.*?buildConfigurationList = (\w+)", re.S)
TARGET_RE = re.compile(r"isa = PBXNativeTarget;((?:(?!isa = ).)*?)productType = " + chr(34) + "?([^" + chr(34) + ";]+)", re.S)
LIST_REF_RE = re.compile(r"buildConfigurationList = (\w+)")
ID_RE = re.compile(r"\w+")
OWNER_RE = re.compile(r"(\w+)(?:\s*/[*][^*]*[*]/)?\s*=\s*" + re.escape(chr(123)) + r"\s*$")
NAME_RE = re.compile(r"\s*name = ([^;]+);")
DEPENDENCY_MARKERS = (
    "SKIP_INSTALL = YES",
    "DYLIB_INSTALL_NAME_BASE",
    "TEST_HOST",
    "BUNDLE_LOADER",
    "MACH_O_TYPE",
    "TEST_TARGET_NAME",
)


def below(settings):
    return [int(v) < 13 for v in DT_RE.findall(settings)]


for path in sys.argv[1:]:
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError:
        continue
    app, project = [], []
    # The PBXProject configurations are project defaults, never the settings of a target.
    project_ids = set()
    pbx = PROJECT_RE.search(text)
    if pbx:
        lst = re.search(re.escape(pbx.group(1)) + r"\b[^=]*=\s*" + re.escape(chr(123)) + r"\s*isa = XCConfigurationList;\s*buildConfigurations = \((.*?)\);", text, re.S)
        if lst:
            project_ids = set(ID_RE.findall(COMMENT_RE.sub(" ", lst.group(1))))
    # When the file names its targets, only an application target configuration is read.
    app_ids, has_targets = set(), False
    for target in TARGET_RE.finditer(text):
        has_targets = True
        ref = LIST_REF_RE.search(target.group(1))
        if ref and target.group(2) == "com.apple.product-type.application":
            lst = re.search(re.escape(ref.group(1)) + r"\b[^=]*=\s*" + re.escape(chr(123)) + r"\s*isa = XCConfigurationList;\s*buildConfigurations = \((.*?)\);", text, re.S)
            if lst:
                app_ids |= set(ID_RE.findall(COMMENT_RE.sub(" ", lst.group(1))))
    for block in BLOCK_RE.finditer(text):
        owner = OWNER_RE.search(text[max(0, block.start() - 300):block.start()])
        settings = block.group(1)
        flags = below(settings)
        name = NAME_RE.match(text, block.end())
        live = COMMENT_RE.sub(" ", settings)
        # Only the Release configuration of an app with its own bundle id, and only when no
        # other conditional deployment key could override the quoted one.
        certain = ("PRODUCT_BUNDLE_IDENTIFIER" in live
                   and not any(marker in live for marker in DEPENDENCY_MARKERS)
                   and len(CONDITIONAL_RE.findall(live)) == len(QDT_RE.findall(live)))
        certain = certain and not (owner and owner.group(1) in project_ids)
        if has_targets:
            certain = certain and bool(owner) and owner.group(1) in app_ids
        if certain and name and name.group(1).strip().strip('"').lower() == "release":
            flags += [True for value in QDT_RE.findall(live) if int(value) < 13]
        if not flags:
            continue
        if "PRODUCT_BUNDLE_IDENTIFIER" in settings or "PRODUCT_NAME" in settings:
            if not any(marker in settings for marker in DEPENDENCY_MARKERS):
                app.extend(flags)
        else:
            project.extend(flags)
    # An app target that sets its own floor decides. Otherwise the project-level value is inherited.
    if (app and any(app)) or (not app and any(project)):
        sys.exit(0)
sys.exit(1)
PBXPY
)" 2>/dev/null
  }
  xcconfig_below_ios13() {
    [ -s "$FILELIST" ] || return 1
    grep '[.]xcconfig$' "$FILELIST" | grep -viE '(test|framework|pods)' | tr '\n' '\0' | xargs -0 grep -EIls -e 'IPHONEOS_DEPLOYMENT_TARGET(\[[^]]*\])?[[:space:]]*=[[:space:]]*"?(8|9|10|11|12)(\.[0-9]+)*"?[[:space:]]*(;|//|$)|platform[[:space:]]+:ios,[[:space:]]*.(8|9|10|11|12)(\.[0-9]+)*.' 2>/dev/null | grep . >/dev/null
  }
  if podfile_below_ios13 || pbx_below_ios13 || xcconfig_below_ios13; then
    finding high "APPLE-MIN-DEPLOYMENT-TARGET-IOS13" "iOS deployment target below iOS 13" "Raise the app target IPHONEOS_DEPLOYMENT_TARGET and the Podfile platform to 13.0 or later. A lower target on a dependency or test target alone is fine. App Store Connect refuses uploads that target an earlier iOS." src 'IPHONEOS_DEPLOYMENT_TARGET(\[[^]]*\])?[[:space:]]*=[[:space:]]*"?(8|9|10|11|12)(\.[0-9]+)*"?[[:space:]]*(;|//|$)|platform[[:space:]]+:ios,[[:space:]]*.(8|9|10|11|12)(\.[0-9]+)*.|"IPHONEOS_DEPLOYMENT_TARGET\[sdk=iphoneos[*]\]"[[:space:]]*=[[:space:]]*"?(8|9|10|11|12)(\.[0-9]+)*'
  fi
  # App Review runs on an IPv6-only NAT64 network (2.5.5). IPv4-only socket calls fail there.
  # C, C++ and Objective-C++ sit outside the shared source list, so read the app's own ones here.
  native_ipv4_only() {
    find "$DIR" -maxdepth 8 \( -type d \( -name Pods -o -name node_modules -o -name vendor -o -name Vendor -o -name ThirdParty -o -name third_party -o -name external -o -name External -o -name Carthage -o -name build -o -name .git \) -prune \) \
      -o -type f \( -name '*.c' -o -name '*.cpp' -o -name '*.cc' -o -name '*.mm' \) -print 2>/dev/null | awk 'NR <= 2000' \
      | tr '\n' '\0' | xargs -0 grep -EIls -e '(^|[^A-Za-z0-9_])(inet_addr|inet_aton|gethostbyname)[[:space:]]*\(' 2>/dev/null | grep . >/dev/null
  }
  if native_ipv4_only || grep_has '(^|[^A-Za-z0-9_])(inet_addr|inet_aton|gethostbyname)[[:space:]]*\('; then
    finding medium "APPLE-2.5.5-IPV4-ONLY-NETWORKING" "IPv4-only socket API in use" "Replace inet_addr, inet_aton and gethostbyname with getaddrinfo or Network.framework, and test on an IPv6-only NAT64 network (Mac Internet Sharing, Create NAT64 Network)." src '(^|[^A-Za-z0-9_])(inet_addr|inet_aton|gethostbyname)[[:space:]]*\('
  fi
  # 5.1.3(ii). personal health information may not be stored in iCloud.
  if grep_has 'HKHealthStore' && grep_has 'NSUbiquitousKeyValueStore|CKContainer|CKDatabase|NSPersistentCloudKitContainer|cloudKitContainerOptions'; then
    finding medium "APPLE-5.1.3-HEALTH-DATA-ICLOUD" "HealthKit and iCloud storage in the same app" "Confirm no HealthKit or other health data is written to iCloud, CloudKit or iCloud key-value storage (5.1.3(ii)). Keep health data on device or in a compliant backend you control." src 'NSUbiquitousKeyValueStore|CKContainer|CKDatabase|NSPersistentCloudKitContainer|cloudKitContainerOptions'
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
    # The app side of Universal Links is an applinks: entry in the associated domains entitlement. The file is on the website.
    # A scheme plist is cleared only by applinks in the Release entitlements of the iOS app target that owns it.
    universal_links_cover() {
      command -v python3 >/dev/null 2>&1 || return 1
      # A scheme is declared in a plist, in Expo app.json or app.config, or in build settings. Source code never declares one.
      local schemes in_settings=0
      schemes="$(grep -E '[.]plist$|/app[.]json$|/app[.]config[.][cm]?[jt]s$' "$FILELIST" | tr '\n' '\0' | xargs -0 grep -lIs -e 'CFBundleURLSchemes' 2>/dev/null)"
      [ -n "$(grep -E '[.](pbxproj|xcconfig)$' "$FILELIST" | tr '\n' '\0' | xargs -0 grep -lIs -e 'INFOPLIST_KEY_CFBundleURLTypes' 2>/dev/null)" ] && in_settings=1
      [ -n "$schemes" ] || [ "$in_settings" -eq 1 ] || return 1
      grep '[.]pbxproj$' "$FILELIST" | tr '\n' '\0' | DL_SCHEMES="$schemes" DL_IN_SETTINGS="$in_settings" xargs -0 python3 -c "$(cat <<'ENTPY'
import fnmatch
import os
import plistlib
import re
import sys

LB, RB, LP, RP, LS, RS = chr(123), chr(125), chr(40), chr(41), chr(91), chr(93)
DQ, NL, BS, DOL = chr(34), chr(10), chr(92), chr(36)
PUNCT = LB + RB + LP + RP + "=;,"
DOMAINS = "com.apple.developer.associated-domains"
UNSURE = object()


def tokens(text):
    out, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        if c.isspace():
            i += 1
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            i = n if j < 0 else j + 2
        elif text.startswith("//", i):
            j = text.find(NL, i)
            i = n if j < 0 else j + 1
        elif c == DQ:
            j, buf = i + 1, []
            while j < n and text[j] != DQ:
                if text[j] == BS and j + 1 < n:
                    j += 1
                buf.append(text[j])
                j += 1
            out.append(("s", "".join(buf)))
            i = j + 1
        elif c in PUNCT:
            out.append(("p", c))
            i += 1
        else:
            j = i
            while j < n and not text[j].isspace() and text[j] not in PUNCT and text[j] != DQ and not text.startswith("/*", j):
                j += 1
            out.append(("s", text[i:j]))
            i = j
    return out


def parse(toks, k):
    kind, val = toks[k]
    if kind == "p" and val == LB:
        obj, k = dict(), k + 1
        while toks[k] != ("p", RB):
            key = toks[k][1]
            value, k = parse(toks, k + 2)
            obj[key] = value
            if toks[k] == ("p", ";"):
                k += 1
        return obj, k + 1
    if kind == "p" and val == LP:
        arr, k = [], k + 1
        while toks[k] != ("p", RP):
            value, k = parse(toks, k)
            arr.append(value)
            if toks[k] == ("p", ","):
                k += 1
        return arr, k + 1
    return val, k + 1


def split_key(raw):
    raw = raw.replace(" ", "")
    i = 0
    while i < len(raw) and (raw[i].isalnum() or raw[i] == "_"):
        i += 1
    name, rest, conds = raw[:i], raw[i:], []
    while rest.startswith(LS):
        j = rest.find(RS)
        if j < 0:
            return None
        for part in rest[1:j].split(","):
            k, _, v = part.partition("=")
            conds.append((k, v))
        rest = rest[j + 1:]
    if rest or not name:
        return None
    return name, conds


def is_pods(path):
    return "Pods" in path.split(os.sep) or os.path.basename(path).startswith("Pods-")


def xcconfig(path, depth=0):
    if depth > 8:
        return UNSURE
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
    except OSError:
        return UNSURE
    found = dict()
    for line in lines:
        s = line.split("//", 1)[0].strip()
        if s.startswith("#include"):
            rest = s[len("#include"):]
            optional = rest.startswith("?")
            name = rest.lstrip("?").strip().strip(DQ).strip()
            if DOL in name or not name:
                return UNSURE
            inc = name if os.path.isabs(name) else os.path.join(os.path.dirname(path), name)
            if not os.path.exists(inc):
                if optional or is_pods(inc):
                    continue
                return UNSURE
            sub = xcconfig(inc, depth + 1)
            if sub is UNSURE:
                return UNSURE
            found.update(sub)
            continue
        level, cut = 0, -1
        for idx, ch in enumerate(s):
            if ch == LS:
                level += 1
            elif ch == RS:
                level -= 1
            elif ch == "=" and level == 0:
                cut = idx
                break
        if cut < 0:
            continue
        key = s[:cut].replace(" ", "")
        if split_key(key) is None:
            continue
        found[key] = s[cut + 1:].strip().rstrip(";").strip().strip(DQ)
    return found


def cond_state(conds, cfg_name):
    known_false, unknown, spec = False, False, 0
    for k, v in conds:
        if k == "sdk":
            hit = fnmatch.fnmatchcase("iphoneos", v) or fnmatch.fnmatchcase("iphoneos26.0", v)
        elif k == "config":
            hit = fnmatch.fnmatchcase(cfg_name, v)
        else:
            unknown = True
            continue
        if not hit:
            known_false = True
        elif v.strip("*"):
            spec += 1
    if known_false:
        return False, 0
    if unknown:
        return None, 0
    return True, spec


def pick(settings, name, cfg_name):
    if settings is UNSURE:
        return UNSURE
    best, top, unsure = [], -1, False
    for raw, value in settings.items():
        if isinstance(value, list):
            value = " ".join(str(x) for x in value)
        if not isinstance(value, str):
            continue
        parsed = split_key(raw)
        if parsed is None or parsed[0] != name:
            continue
        ok, spec = cond_state(parsed[1], cfg_name)
        if ok is False:
            continue
        if ok is None:
            unsure = True
        elif spec > top:
            best, top = [value], spec
        elif spec == top:
            best.append(value)
    if unsure:
        return UNSURE
    if not best:
        return None
    return best[0] if len(set(best)) == 1 else UNSURE


def setting(levels, name, cfg_name):
    for settings in levels:
        value = pick(settings, name, cfg_name)
        if value is not None:
            return value
    return None


REF_RE = re.compile(re.escape(DOL) + LP + "?:" + re.escape(LP) + "([A-Za-z0-9_]+)((?::[A-Za-z0-9_]+)*)" + re.escape(RP)
                    + "|" + re.escape(LB) + "([A-Za-z0-9_]+)((?::[A-Za-z0-9_]+)*)" + re.escape(RB) + RP)


def modify(value, mods):
    for mod in mods.split(":")[1:]:
        if mod in ("identifier", "c99extidentifier"):
            value = re.sub("[^A-Za-z0-9_]", "_", value)
            if value[:1].isdigit():
                value = "_" + value
        elif mod == "rfc1034identifier":
            value = re.sub("[^A-Za-z0-9.-]", "-", value)
        elif mod == "lower":
            value = value.lower()
        elif mod == "upper":
            value = value.upper()
        else:
            return None
    return value


def expand(value, names):
    def sub(m):
        var, mods = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
        if var not in names:
            return m.group(0)
        real = modify(names[var], mods)
        return m.group(0) if real is None else real
    for _ in range(6):
        before = value
        value = REF_RE.sub(sub, value)
        if value == before:
            break
    return UNSURE if DOL in value else value


def resolve(value, proj_dir, names):
    value = value.strip()
    if not value:
        return UNSURE
    value = expand(value, names)
    if value is UNSURE:
        return UNSURE
    if not os.path.isabs(value):
        value = os.path.join(proj_dir, value)
    return os.path.realpath(os.path.normpath(value))


def file_path(objects, parents, ref, proj_dir):
    parts, cur = [], ref
    for _ in range(64):
        node = objects.get(cur)
        if not isinstance(node, dict):
            return UNSURE
        if node.get("path"):
            parts.append(node["path"])
        tree = node.get("sourceTree", "<group>")
        if tree == "<group>" and cur in parents:
            cur = parents[cur]
            continue
        if tree == "<absolute>":
            return os.path.normpath(os.path.join(*reversed(parts)))
        if tree in ("<group>", "SOURCE_ROOT"):
            return os.path.normpath(os.path.join(proj_dir, *reversed(parts)))
        return UNSURE
    return UNSURE


def base_settings(objects, parents, cfg, proj_dir):
    ref = cfg.get("baseConfigurationReference")
    if not ref:
        return dict()
    path = file_path(objects, parents, ref, proj_dir)
    if path is UNSURE:
        return UNSURE
    if not os.path.exists(path):
        return dict() if is_pods(path) else UNSURE
    return xcconfig(path)


def configs(objects, list_id):
    lst = objects.get(list_id)
    if not isinstance(lst, dict):
        return []
    return [objects[c] for c in lst.get("buildConfigurations", []) if isinstance(objects.get(c), dict)]


def release_only(cfgs):
    words = ("release", "appstore", "app store", "production")
    named = [c for c in cfgs if any(w in str(c.get("name", "")).lower() for w in words)]
    return named or [c for c in cfgs if "debug" not in str(c.get("name", "")).lower()]


def is_ios(sdk, plats, dep):
    if isinstance(plats, str) and "iphoneos" in plats.split():
        return True
    if isinstance(sdk, str) and sdk.strip().lower() not in ("", "auto"):
        return sdk.strip().lower().startswith("iphoneos")
    if isinstance(plats, str) and plats.strip():
        return False
    return isinstance(dep, str) and bool(dep.strip())


def applinks(path):
    try:
        with open(path, "rb") as fh:
            data = plistlib.load(fh)
    except Exception:
        return False
    doms = data.get(DOMAINS) if isinstance(data, dict) else None
    if not isinstance(doms, list):
        return False
    for entry in doms:
        if isinstance(entry, str):
            entry = entry.strip()
            mode = entry.partition("?")[2].partition("mode=")[2]
            if entry.startswith("applinks:") and len(entry.partition("?")[0]) > 9 and "developer" not in mode and "managed" not in mode:
                return True
    return False


pairs, in_settings, unshipped, blind = [], [], set(), []
for pbx in sys.argv[1:]:
    try:
        with open(pbx, encoding="utf-8", errors="replace") as fh:
            root, _ = parse(tokens(fh.read()), 0)
    except (OSError, IndexError, TypeError):
        continue
    if not isinstance(root, dict):
        continue
    objects = root.get("objects", root)
    if not isinstance(objects, dict):
        continue
    proj_dir = os.path.dirname(os.path.dirname(os.path.abspath(pbx)))
    proj_name = os.path.splitext(os.path.basename(os.path.dirname(os.path.abspath(pbx))))[0]
    parents = dict()
    for oid, obj in objects.items():
        if isinstance(obj, dict) and isinstance(obj.get("children"), list):
            for child in obj["children"]:
                parents[child] = oid
    project = next((o for o in objects.values() if isinstance(o, dict) and o.get("isa") == "PBXProject"), None)
    project_cfgs = configs(objects, project.get("buildConfigurationList")) if project else []
    by_name = dict((str(c.get("name", "")), c) for c in project_cfgs)
    targets = [o for o in objects.values() if isinstance(o, dict) and o.get("isa") == "PBXNativeTarget"]
    work = []
    for t in targets:
        if t.get("productType") == "com.apple.product-type.application":
            work.append((str(t.get("name", "")), configs(objects, t.get("buildConfigurationList"))))
    if not targets:
        loose = [o for o in objects.values() if isinstance(o, dict) and o.get("isa") == "XCBuildConfiguration"
                 and o not in project_cfgs and "PRODUCT_BUNDLE_IDENTIFIER" in (o.get("buildSettings") or dict())]
        work.append(("", loose))
    for target_name, cfgs in work:
        shipped = release_only(cfgs)
        for cfg in cfgs:
            cname = str(cfg.get("name", ""))
            ships = any(cfg is c for c in shipped)
            levels = [cfg.get("buildSettings") or dict(), base_settings(objects, parents, cfg, proj_dir)]
            if cname in by_name:
                proj_cfg = by_name[cname]
                levels += [proj_cfg.get("buildSettings") or dict(), base_settings(objects, parents, proj_cfg, proj_dir)]
            sdk = setting(levels, "SDKROOT", cname)
            plats = setting(levels, "SUPPORTED_PLATFORMS", cname)
            dep = setting(levels, "IPHONEOS_DEPLOYMENT_TARGET", cname)
            if not is_ios(sdk, plats, dep):
                if UNSURE in (sdk, plats, dep):
                    blind.append(ships)
                continue
            names = dict(PROJECT_DIR=proj_dir, SRCROOT=proj_dir, SOURCE_ROOT=proj_dir, PROJECT_NAME=proj_name, CONFIGURATION=cname)
            if target_name:
                names["TARGET_NAME"] = target_name
            product = setting(levels, "PRODUCT_NAME", cname)
            if product is None and target_name:
                product = target_name
            if isinstance(product, str):
                product = expand(product, names)
                if isinstance(product, str) and product:
                    names["PRODUCT_NAME"] = product
            ent = setting(levels, "CODE_SIGN_ENTITLEMENTS", cname)
            if isinstance(ent, str):
                ent = resolve(ent, proj_dir, names)
            signed = isinstance(ent, str) and applinks(ent)
            if ships and setting(levels, "INFOPLIST_KEY_CFBundleURLTypes", cname) is not None:
                in_settings.append(signed)
            plist = setting(levels, "INFOPLIST_FILE", cname)
            if isinstance(plist, str):
                plist = resolve(plist, proj_dir, names)
            if not isinstance(plist, str):
                blind.append(ships)
                continue
            if ships:
                pairs.append((plist, signed))
            else:
                unshipped.add(plist)

schemes = [os.path.realpath(os.path.abspath(p)) for p in os.environ.get("DL_SCHEMES", "").split(NL) if p.strip()]
by_settings = os.environ.get("DL_IN_SETTINGS") == "1"
covered = bool(schemes) or by_settings
if by_settings and (not in_settings or not all(in_settings)):
    covered = False
for scheme in schemes:
    owners = [ok for plist, ok in pairs if plist == scheme]
    if not owners and scheme in unshipped and not any(blind):
        continue
    if not owners or not all(owners):
        covered = False
if covered:
    print("CLEAR")
ENTPY
)" 2>/dev/null | grep -qx CLEAR
    }
    if ! grep_has 'apple-app-site-association' && ! universal_links_cover; then
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
  del_follow() {  # follows the deleting code into the functions and constants it uses. WEAK<tab>file<tab>line, CLEAN or UNSURE
    command -v python3 >/dev/null 2>&1 || { echo UNSURE; return; }
    python3 -c "$(cat <<'DELPY'
import re
import sys

LP, RP, LB, RB, DQ, SQ, BS = (
    chr(40),
    chr(41),
    chr(123),
    chr(125),
    chr(34),
    chr(39),
    chr(92),
)
NL, TAB, LS, RS, BQ = chr(10), chr(9), chr(91), chr(93), chr(96)
MAX_HOPS, MAX_NAMES, MAX_BYTES, MAX_LINE = 6, 3000, 40000000, 20000


def rx(s):
    # Tilde stands for a backslash, the angle pair for a group.
    return re.compile(s.replace("~", BS).replace("<?", LP + "?:").replace(">>", RP))


TRIG = re.compile("deleteAccount|delete account")
WEAK = re.compile("mailto:|deactivate")
LAYOUT = rx("NSLayoutConstraint~s*~.~s*deactivate")
STR = rx(
    DQ + "<?~~.|[^" + DQ + "~~]>>*" + DQ + "|" + SQ + "<?~~.|[^" + SQ + "~~]>>*" + SQ
)
IDENT = re.compile("[A-Za-z_][A-Za-z0-9_]*")
STOP = set(
    """func fun function def fn let var val const static final private public protected internal
open override async await try catch throw throws return if else guard switch case default for while do in
self this super new nil null true false void Void String Int Bool Double Float URL some any is as
import class struct enum interface protocol extension object record data where get set willSet didSet
print println console log error Error Task DispatchQueue main shared""".split()
)
TYPEKW = set(
    "class struct enum interface protocol extension object record data typealias".split()
)
# Words that look like a call but are syntax, and words that open a definition.
CTRL = set(
    """if else elif while for switch when guard return throw try await catch do case match yield
not and or in is as typeof sizeof assert function init constructor selector available""".split()
)
DEFKW = set(
    "func fun function def fn sub class struct enum interface protocol extension object record typealias".split()
)
# Calls that are clearly the platform, never app code that could hide a mailto or a deactivate.
BUILTIN = set(
    """fetch print println require setTimeout setInterval clearTimeout parseInt parseFloat alert
encodeURIComponent decodeURIComponent precondition fatalError withAnimation len str int float list
dict range isinstance launch withContext runBlocking coroutineScope error async""".split()
)
FW_ROOTS = set(
    "firebase axios supabase window document navigator console process globalThis localStorage sessionStorage".split()
)
STD_MEMBERS = set(
    """map filter reduce forEach compactMap flatMap sorted sort first last contains append insert
removeAll push pop slice splice join joined split trim replace lowercased uppercased toLowerCase
toUpperCase toString includes indexOf startsWith endsWith hasPrefix hasSuffix then finally json
text resume cancel sink store encode decode navigate goBack dismiss""".split()
)
HTTP = set("get post put patch delete request".split())
ACCT_SDK = set([("user", "delete"), ("currentUser", "delete")])
JS_EXT = (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte")
MODS = "<?[A-Za-z_@][A-Za-z0-9_<>?,.~[~]]*~s+>>*"
GEN = "<?<[^>]*>~s*>>?"
REC = "<?[A-Za-z_][A-Za-z0-9_<>?,.]*~.>>?"
CALL = re.compile(LP + "[A-Za-z_][A-Za-z0-9_]*" + RP)
TYPEDEF = rx(
    "~b<?class|struct|enum|interface|protocol|object|record|typealias|extension>>~s+" + LP + "[A-Za-z_][A-Za-z0-9_]*" + RP
)
LOCAL = rx("~b<?let|var|val|const>>~s+<?mut~s+>>?" + LP + "[A-Za-z_][A-Za-z0-9_]*" + RP)
HOOK = rx("^use[A-Z]")
# A real account deletion call. CLEAN needs one of these in the code the deletion reaches.
Q = LS + DQ + SQ + BQ + RS
SDK = [
    rx("~b<?user|currentUser>>~s*[!?]*~s*~.~s*delete~s*~" + LP + "~s*~" + RP),
    rx("~bauth~s*~.~s*admin~s*~.~s*deleteUser~s*~" + LP),
    rx("~b<?Admin>>?DeleteUserCommand~b|~badminDeleteUser~s*~" + LP),
    rx("~b<?auth0|cognito|cognitoUser|management~s*~.~s*users>>[A-Za-z]*~s*~.~s*<?deleteUser|delete>>~s*~" + LP),
]
# A verb call that takes the path as an argument, and a method option that names the verb.
ARGCALL = rx(LP + "@DELETE|@POST|~.~s*delete|~.~s*post" + RP + "~s*~" + LP)
METHOD_DEL = rx("[Mm]ethod~s*[:=]~s*<?" + Q + "DELETE" + Q + "|<?HTTPMethod>>?~.delete~b>>")
METHOD_POST = rx("[Mm]ethod~s*[:=]~s*<?" + Q + "POST" + Q + "|<?HTTPMethod>>?~.post~b>>")
VERB = rx("~.~s*<?get|post|put|patch|delete|request>>~s*~" + LP + "|@<?GET|POST|PUT|PATCH|DELETE|HTTP>>~b|[Mm]ethod~s*[:=]")
LIT = rx(DQ + "[^" + DQ + "]*" + DQ + "|" + SQ + "[^" + SQ + "]*" + SQ + "|" + BQ + "[^" + BQ + "]*" + BQ)
JOIN = rx("~s*~+~s*")
JOIN_NAME = rx("~s*~+" + LS + "^,;" + RS + "*~+~s*")
TAIL = rx("~s*~+")
HEXID = rx(LS + "0-9a-fA-F-" + RS + LB + "8," + RB)
QCUT = rx(LS + "?#" + RS)
SEP = rx(LS + "-_" + RS)
NAMEREF = rx("~s*~+~s*" + LP + "[A-Za-z_][A-Za-z0-9_.?!]*" + RP)
NONAME = rx("[^A-Za-z0-9_.]")
PREFIX = rx("v~d+<?~.~d+>>?|api|rest")
# Ids that name the signed in user, and the bare id a path parameter usually carries.
SELF_IDS = set("me self current currentuser user.id auth.uid".split())
SELF_LAST = set("userid uid currentuserid".split())
GENERIC_IDS = set("id x".split())
SELFREF = rx("~b<?userId|uid|currentUser|currentUserId>>~b|~buser~s*[?!]?~s*~.~s*id~b|~bauth~s*~.~s*uid~b")
ACCT_LAST = set("me account user profile".split())
ACCT_COLL = set("users accounts user account".split())
ID_ALIAS = set("me current self".split())
DEL_WORDS = set("deleteaccount deleteuser deleteme deleteprofile accountdelete userdelete".split())
NEST_EXT = (".swift", ".kt", ".kts", ".rs", ".scala")
GETTER = rx("^~s*get~s*<?~" + LP + "~s*~" + RP + ">>?~s*" + LS + "=~" + LB + RS)
ELSE = rx("~s*else~b")
BRANCH = rx("~b<?if|else>>~b")
ARM = rx("->~s*$")
TERNARY = rx("~s~?~s|~belse~b")
ENUMCASE = rx("~bcase~s+<?[A-Za-z_][A-Za-z0-9_]*~s*,~s*>>*$")
IMPORTISH = rx("^~s*<?import~b|export~s*~" + LB + "|from~b>>|~b<?const|let|var|val>>~s*" + LS + "~" + LB + "~" + LS + LP + RS)
OBJC_DEF = rx("^~s*[-+]~s*~" + LP)
WORDS_ONLY = rx("~s*<?[A-Za-z_@][A-Za-z0-9_]*~s+>>*")
SIG_TAIL = rx("<?:|->|throws~b|rethrows~b|async~b>>")
NOT_TYPE = set("await return try throw yield defer go new delete".split())
TESTPATH = rx("<?^|/>><?Tests?|tests?|__tests__|specs?|UITests|androidTest>>/|[._-]<?test|spec>>~.[A-Za-z]+$|Tests?~.<?swift|kt|java|m>>$")
LABEL = rx(LS + LP + "," + RS + "~s*" + LP + "[A-Za-z_][A-Za-z0-9_]*" + RP + ":" + LP + "?!:" + RP)


def code(line):
    # The line without a trailing slash comment, strings kept.
    q, k = None, 0
    while k < len(line):
        ch = line[k]
        if q:
            if ch == BS:
                k += 1
            elif ch == q:
                q = None
        elif ch in DQ + SQ + BQ:
            q = ch
        elif line.startswith("//", k):
            return line[:k]
        k += 1
    return line


def uncomment(text, nest):
    # The text with every comment blanked and every newline kept, so line numbers still match.
    out, k, q, depth, n = [], 0, None, 0, len(text)
    while k < n:
        ch = text[k]
        if depth:
            if text.startswith("*/", k):
                depth, k = depth - 1, k + 2
                out.append("  ")
            elif nest and text.startswith("/*", k):
                depth, k = depth + 1, k + 2
                out.append("  ")
            else:
                out.append(NL if ch == NL else " ")
                k += 1
            continue
        if q:
            out.append(ch)
            if ch == BS and k + 1 < n:
                out.append(text[k + 1])
                k += 2
                continue
            if ch == q or (ch == NL and q != BQ):
                q = None
            k += 1
            continue
        if text.startswith("//", k):
            e = text.find(NL, k)
            e = n if e < 0 else e
            out.append(" " * (e - k))
            k = e
        elif text.startswith("/*", k):
            depth, k = 1, k + 2
            out.append("  ")
        else:
            if ch in DQ + SQ + BQ:
                q = ch
            out.append(ch)
            k += 1
    return "".join(out)


def id_kind(s):
    # What an id segment names. self is the signed in account, generic an unnamed id, other someone else.
    t = s.strip()
    if not t:
        return ""
    if t.lower() in ID_ALIAS:
        return "self"
    if t.isdigit() or HEXID.fullmatch(t):
        return "other"
    if not (t[0] in LB + ":$<" or t.startswith(BS + LP)):
        return ""
    name = NONAME.sub("", t).lower()
    if name in SELF_IDS or name.split(".")[-1] in SELF_LAST:
        return "self"
    return "generic" if name in GENERIC_IDS else "other"


def prefix_like(s, k):
    # A scheme, host, version or api segment, or a base url placeholder in first place.
    if PREFIX.fullmatch(s.lower()) or "." in s or s.endswith(":"):
        return True
    return k == 0 and s[0] in LB + "$<"


def segs(path):
    return [s for s in QCUT.split(path, 1)[0].split("/") if s]


def acct_kind(ss):
    # The path is the account or user itself, under nothing but a host, version or api prefix.
    k = 0
    while k < len(ss) - 1 and prefix_like(ss[k], k):
        k += 1
    raw = ss[k:]
    rest = [s.lower() for s in raw]
    if len(rest) == 1 and rest[0] in ACCT_LAST:
        return "strong"
    if len(rest) != 2:
        return ""
    if rest[0] == "me" and rest[1] in ACCT_LAST:
        return "strong"
    if rest[0] in ACCT_COLL or rest[0] == "profile":
        if rest[1] == "me":
            return "strong"
        kind = id_kind(raw[1])
        if kind == "self":
            return "strong"
        if kind == "generic" and rest[0] in ACCT_COLL:
            return "generic"
    return ""


def del_kind(ss):
    # A delete path whose delete word applies to the account or user.
    low = [SEP.sub("", s.lower()) for s in ss]
    if not low:
        return ""
    if low[-1] in DEL_WORDS:
        return "strong"
    if len(low) >= 2 and low[-2] in DEL_WORDS:
        kind = id_kind(ss[-1])
        if kind:
            return {"self": "strong", "generic": "generic"}.get(kind, "")
    if low[-1] == "delete":
        return acct_kind(ss[:-1])
    if "delete" in low[:-1]:
        k = len(low) - 1 - low[::-1].index("delete")
        return acct_kind(ss[k + 1 :]) if len(ss) - k - 1 <= 2 else ""
    return ""


def slot(gap):
    m = NAMEREF.match(gap)
    return LB + (m.group(1) if m else "x") + RB


def paths(text):
    # Each string literal joined to what it is concatenated with. A name in the join becomes a slot.
    ms, out, cur = list(LIT.finditer(text)), [], None
    for n, m in enumerate(ms):
        body = m.group(0)[1:-1]
        gap = text[ms[n - 1].end() : m.start()] if n else ""
        if cur is not None and JOIN.fullmatch(gap):
            cur += body
        elif cur is not None and JOIN_NAME.fullmatch(gap):
            cur += slot(gap) + body
        else:
            if cur is not None:
                out.append(cur)
            cur = body
        nxt = ms[n + 1].start() if n + 1 < len(ms) else len(text)
        rest = text[m.end() : nxt]
        if TAIL.match(rest) and not JOIN.fullmatch(rest) and not JOIN_NAME.fullmatch(rest):
            cur += slot(rest)
    if cur is not None:
        out.append(cur)
    return out


def args(t, k):
    # The argument text of the call whose open paren sits just before column k.
    depth = 1
    for j in range(k, len(t)):
        if t[j] == LP:
            depth += 1
        elif t[j] == RP:
            depth -= 1
            if depth == 0:
                return t[k:j]
    return t[k:]


def better(a, b):
    return "strong" if "strong" in (a, b) else (a or b)


def hit(text, post, slash):
    best = ""
    for p in paths(text):
        if slash and "/" not in p:
            continue
        ss = segs(p)
        best = better(best, del_kind(ss) if post else acct_kind(ss))
    return best


def real_delete(line, before=()):
    # strong is the account itself, generic a users id path that still needs the id to be the signed in user.
    t = code(line)
    if any(r.search(t) for r in SDK):
        return "strong"
    best = ""
    for m in ARGCALL.finditer(t):
        verb = m.group(1)
        post = verb.lower().endswith("post")
        best = better(best, hit(args(t, m.end()), post, not verb.startswith("@")))
    for pat, post in ((METHOD_DEL, False), (METHOD_POST, True)):
        if pat.search(t):
            for x in (t,) + tuple(before):
                best = better(best, hit(x, post, True))
    return best


def real_in(lines, region):
    # A method option may name the verb a few lines after the path, with no other call between.
    best = ""
    for n, j in enumerate(region):
        before = []
        for k in reversed(region[max(0, n - 3) : n]):
            if VERB.search(code(lines[k])):
                break
            before.append(code(lines[k]))
        best = better(best, real_delete(lines[j], before))
    return best


def pdepth(c, k):
    return c[:k].count(LP) - c[:k].count(RP)


def scrub(line):
    s = STR.sub(DQ + DQ, line)
    i = s.find("//")
    return s if i < 0 else s[:i]


def indent(line):
    return len(line) - len(line.lstrip())


def is_label(text):
    t = text.strip()
    return t.endswith(":") and (
        t.startswith("case ") or t.startswith("case.") or t.startswith("default")
    )


def block(lines, i, col):
    # Lines of the brace block opened from column col of line i, a switch arm, an indented block, or line i.
    depth, started, out = 0, False, []
    for j in range(i, min(len(lines), i + 600)):
        text = scrub(lines[j])[col if j == i else 0 :]
        out.append(j)
        for ch in text:
            if ch == LB:
                depth, started = depth + 1, True
            elif ch == RB:
                depth -= 1
                if depth < 0 and not started:
                    return [i], True
                if started and depth == 0:
                    return out, True
        if not started:
            nxt = lines[j + 1].strip() if j + 1 < len(lines) else ""
            if not nxt.startswith(LB):
                break
    if started:
        return out, False
    head = scrub(lines[i])
    if is_label(head):
        out, depth = [i], 0
        for j in range(i + 1, min(len(lines), i + 600)):
            text = scrub(lines[j])
            if depth == 0 and (is_label(text) or text.strip().startswith(RB)):
                return out, True
            depth += text.count(LB) - text.count(RB)
            out.append(j)
        return out, False
    if head.rstrip().endswith(":"):
        ind, out = indent(lines[i]), [i]
        for j in range(i + 1, min(len(lines), i + 600)):
            if lines[j].strip() and indent(lines[j]) <= ind:
                break
            out.append(j)
        return out, True
    return [i], True


def fn_pats(n):
    # The last pattern is the method head that body_def follows to its brace.
    return [
        rx("~b<?func|fun|function|def|fn|sub>>~s+" + GEN + REC + n + "~b"),
        rx("^~s*" + MODS + n + "~s*" + GEN + "~" + LP + "[^;]*~" + RP + "[^;=]*=>"),
        rx(
            "~b"
            + n
            + "~s*[:=]~s*<?async~s*>>?<?function~b|~"
            + LP
            + "[^=;]*=>|[A-Za-z_][A-Za-z0-9_]*~s*=>|~"
            + LB
            + ">>"
        ),
        rx("^~s*" + LP + MODS + RP + n + "~s*" + GEN + "~" + LP),
    ]


def body_def(lines, cl, i, head, js):
    # A method head whose brace body opens on the same line, the next line, or after a multi line parameter list.
    m = head.search(cl[i])
    if not m:
        return None
    words = m.group(1).split()
    if any(w in CTRL for w in words) or (not words and not js):
        return None
    depth, j, col = 0, i, m.end() - 1
    while j < len(lines) and j < i + 10:
        text = cl[j]
        k = col if j == i else 0
        while k < len(text):
            ch = text[k]
            if ch == LP:
                depth += 1
            elif ch == RP:
                depth -= 1
                if depth == 0:
                    rest = text[k + 1 :]
                    cut = rest.find(LB)
                    tail = rest if cut < 0 else rest[:cut]
                    if any(x in tail for x in ";=" + LP + RP + RB):
                        return None
                    if cut >= 0:
                        return j, k + 1 + cut
                    for q in range(j + 1, min(len(lines), j + 3)):
                        s = cl[q].strip()
                        if not s:
                            continue
                        return (q, cl[q].find(LB)) if s.startswith(LB) else None
                    return None
            elif ch in ";" + LB + RB:
                return None
            k += 1
        j += 1
    return None


def def_at(lines, cl, i, pats, js):
    m = pats[0].search(cl[i])
    if m:
        return i, m.start()
    d = body_def(lines, cl, i, pats[-1], js)
    if d:
        return d
    for pat in pats[1:-1]:
        m = pat.search(cl[i])
        if m and pdepth(cl[i], m.start()) <= 0:
            return i, m.start()
    return None


def val_defs(n):
    return [
        rx(
            "~b<?let|var|val|const|final|static|readonly|case>>~b[^=]*?~b"
            + n
            + "~b~s*<?:[^=]*>>?="
            + LP
            + "?!="
            + RP
        ),
        rx("~b<?let|var|val>>~s+" + n + "~s*:[^=]*~" + LB),
        rx("~b<?self|this>>~s*~.~s*" + n + "~s*=" + LP + "?!=" + RP),
        rx("^~s*" + n + "~s*[:=]" + LP + "?!=" + RP + "~s*~S"),
        rx("^~s*" + n + "~s*[:=]~s*$"),
    ]


def typed_decl(n):
    # A typed declaration with no value on its line, such as a Kotlin val read through a getter.
    return rx("~b<?let|var|val|const>>~s+" + n + "~s*:" + LS + "^=~" + LB + RS + "*$")


def skip_back(c, j):
    # From a closing paren or bracket at j, the index just before its opener.
    depth = 0
    while j >= 0:
        if c[j] in RP + RS:
            depth += 1
        elif c[j] in LP + LS:
            depth -= 1
            if depth == 0:
                return j - 1
        j -= 1
    return -1


def receiver(c, k):
    # Leftmost name of the dotted chain ending at column k. None means a bare call, ? an unnamed receiver.
    root = None
    while True:
        j = k
        if j < 0 or c[j] != ".":
            return root
        j -= 1
        if j >= 0 and c[j] in "?!":
            j -= 1
        while j >= 0 and c[j] in RP + RS:
            j = skip_back(c, j)
            if j >= 0 and c[j] in "?!":
                j -= 1
        e = j + 1
        while j >= 0 and (c[j].isalnum() or c[j] == "_"):
            j -= 1
        ident = c[j + 1 : e]
        if not ident:
            return "?"
        root, k = ident, j


def calls(c):
    out = []
    for m in CALL.finditer(c):
        name, q = m.group(1), m.end()
        if q < len(c) and c[q] in "?!":
            q += 1
        while q < len(c) and c[q] == " ":
            q += 1
        if q >= len(c) or c[q] != LP:
            continue
        s = m.start()
        if s > 0 and (c[s - 1] in chr(35) + chr(64) or c[s - 1].isalnum() or c[s - 1] == "_"):
            continue
        if name in CTRL or name.startswith("__"):
            continue
        w = re.search("([A-Za-z_]+)[ " + TAB + "]+$", c[max(0, s - 40) : s])
        if w and (w.start() > 0 or s <= 40) and w.group(1) in DEFKW:
            continue
        r = q + 1
        while r < len(c) and c[r] == " ":
            r += 1
        out.append((name, receiver(c, s - 1), r < len(c) and c[r] == DQ))
    return out


def allowed(name, root, lit, apptypes):
    # A call that needs no definition in the app because it is clearly the platform.
    if HOOK.search(name):
        return True
    if root is None or root in ("self", "this", "super"):
        return name in BUILTIN or (name[0].isupper() and name not in apptypes)
    if root == "?" or root in FW_ROOTS or (root, name) in ACCT_SDK:
        return True
    if root[0].isupper() and root not in apptypes:
        return True
    return (name in HTTP and lit) or name in STD_MEMBERS


def next_code(cl, j):
    for q in range(j + 1, min(len(cl), j + 6)):
        if cl[q].strip():
            return q
    return None


def cont(cl, j):
    # Line j and the lines it runs on to until its brackets close. None when it never ends.
    out, depth = [], 0
    for q in range(j, min(len(cl), j + 30)):
        t = cl[q]
        out.append(q)
        depth += sum(t.count(ch) for ch in LP + LS + LB) - sum(t.count(ch) for ch in RP + RS + RB)
        s = t.rstrip()
        if s.strip() and depth <= 0 and not s.endswith(("=", "+", ",", LP, "?", ":")):
            return out
    return None


def value_lines(cl, i, col):
    # The lines that hold the value a declaration names. None when no value can be found.
    if not cl[i][col:].rstrip().endswith("="):
        return []
    q = next_code(cl, i)
    if q is None:
        return None
    return cont(cl, q)


def getter_lines(cl, i):
    q = next_code(cl, i)
    if q is None or not GETTER.match(cl[q]):
        return []
    s = cl[q].rstrip()
    if s.endswith("="):
        r = next_code(cl, q)
        rest = cont(cl, r) if r is not None else None
        return None if rest is None else [q] + rest
    return cont(cl, q)


def opener(cc, i, col):
    # The brace that encloses column col of line i.
    depth = 0
    for j in range(i, max(-1, i - 400), -1):
        t = cc[j][:col] if j == i else cc[j]
        for x in range(len(t) - 1, -1, -1):
            if t[x] == RB:
                depth += 1
            elif t[x] == LB:
                if depth == 0:
                    return j, x
                depth -= 1
    return None


def closer(cc, i, col):
    # The brace that closes the one opened at column col of line i.
    depth = 0
    for j in range(i, min(len(cc), i + 600)):
        t = cc[j]
        for x in range(col if j == i else 0, len(t)):
            if t[x] == LB:
                depth += 1
            elif t[x] == RB:
                depth -= 1
                if depth == 0:
                    return j, x
    return None


def head_of(cc, j, x):
    # The text before a brace, or the line above when the brace opens its own line.
    h = cc[j][:x]
    if not h.strip() and j > 0:
        h = cc[j - 1]
    return h


def chain(cc, j, x):
    # Every line of the if and else chain whose branch opens at column x of line j. None when unclosed.
    while True:
        h = cc[j][:x].rstrip()
        k = h.rfind(RB)
        if k < 0 and not h.strip() and j > 0 and cc[j - 1].strip().startswith(RB + " else"):
            j, h = j - 1, cc[j - 1].rstrip()
            k = h.find(RB)
        if k < 0 or not ELSE.match(h[k + 1 :] + " "):
            break
        o = opener(cc, j, k)
        if not o:
            return None
        j, x = o
    start, lines = j, []
    while True:
        e = closer(cc, j, x)
        if not e:
            return None
        lines = list(range(start, e[0] + 1))
        tail, q, col = cc[e[0]][e[1] + 1 :], e[0], e[1] + 1
        if not tail.strip():
            q = next_code(cc, e[0])
            if q is None:
                break
            tail, col = cc[q], 0
        if not ELSE.match(tail.strip() + " "):
            break
        nb = cc[q].find(LB, col)
        if nb < 0:
            q2 = next_code(cc, q)
            if q2 is None or not cc[q2].strip().startswith(LB):
                return None
            q, nb = q2, cc[q2].find(LB)
        j, x = q, nb
    return lines


def branch_lines(cc, i, col):
    # The if, else and when chains around column col of line i, so a weak sibling branch is followed too.
    out, cur = set(), (i, col)
    for _ in range(8):
        o = opener(cc, *cur)
        if not o:
            break
        h = head_of(cc, *o)
        if ARM.search(h):
            p = opener(cc, *o)
            e = closer(cc, *p) if p else None
            if not e:
                return None
            out.update(range(p[0], e[0] + 1))
            cur = p
            continue
        if BRANCH.search(h):
            lines = chain(cc, *o)
            if lines is None:
                return None
            out.update(lines)
        cur = o
    return out


def decl_ref(c, m, before):
    # An occurrence that declares the entry point rather than using it.
    if ENUMCASE.search(before) or is_label(c) or IMPORTISH.search(c):
        return True
    if OBJC_DEF.match(before):
        return True
    rest = c[m.end() :].lstrip()
    if not rest.startswith(LP) or not WORDS_ONLY.fullmatch(before):
        return False
    after = c[m.end() :].lstrip()[len(args(rest, 1)) + 2 :].lstrip()
    if SIG_TAIL.match(after):
        return True
    words = set(before.split())
    return after.startswith(";") and bool(words) and not (words & NOT_TYPE)


def main():
    try:
        with open(sys.argv[1], encoding="utf-8", errors="replace") as fh:
            paths = [p for p in fh.read().split(NL) if p]
    except OSError:
        print("UNSURE")
        return
    src, clean, nocom, where, total, apptypes = {}, {}, {}, {}, 0, set()
    skipped = False
    for p in paths:
        try:
            with open(p, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError:
            continue
        total += len(text)
        if total > MAX_BYTES:
            print("UNSURE")
            return
        if max((len(x) for x in text.split(NL)), default=0) > MAX_LINE:
            # A minified file cannot be followed, so nothing reached through it is vouched for.
            skipped = True
            continue
        src[p] = text.split(NL)
        nocom[p] = uncomment(text, p.endswith(NEST_EXT)).split(NL)
        clean[p] = [scrub(x) for x in src[p]]
        for i, c in enumerate(clean[p]):
            for t in set(IDENT.findall(c)):
                where.setdefault(t, []).append((p, i))
            for m in TYPEDEF.finditer(c):
                apptypes.add(m.group(1))
    state = {"unsure": skipped, "real": False, "generic": False, "selfref": False}
    frontier, called, defined = set(), [], set()

    def evidence(p, region):
        kind = real_in(nocom[p], region)
        state["real"] = state["real"] or kind == "strong"
        state["generic"] = state["generic"] or kind == "generic"
        if any(SELFREF.search(scrub(nocom[p][j])) for j in region):
            state["selfref"] = True

    def harvest(p, region, scoped):
        # Names a region uses. A local declared before its first use, or an argument label, is never chased elsewhere.
        own = {}
        if scoped:
            for j in region[1:]:
                for m in LOCAL.finditer(clean[p][j]):
                    own.setdefault(m.group(1), j)
            for t, d in list(own.items()):
                pat = rx("~b" + re.escape(t) + "~b")
                if any(pat.search(clean[p][j]) for j in region[1:] if j < d):
                    del own[t]
        for j in region:
            c = clean[p][j]
            labels = set(m.start(1) for m in LABEL.finditer(c))
            for m in IDENT.finditer(c):
                t = m.group(0)
                member = c[: m.start()].rstrip().endswith(".")
                if t not in STOP and (t not in own or member) and m.start() not in labels:
                    frontier.add(t)
            for name, root, lit in calls(c):
                if name in own:
                    continue
                called.append((name, root, lit))
                platform = root == "?" or root in FW_ROOTS or (
                    root is not None and root[0].isupper() and root not in apptypes
                )
                if name in STOP and not name[0].isupper() and not platform:
                    frontier.add(name)

    anchored, seen, entry, own = False, set(), set(), {}
    for p, lines in src.items():
        js = p.endswith(JS_EXT)
        for i, line in enumerate(lines):
            if not TRIG.search(line):
                continue
            # A deleting function, or a switch arm labelled with the deletion, is where the path starts.
            fn = is_label(clean[p][i]) and "deleteAccount" in clean[p][i]
            if fn:
                entry.update(t for t in IDENT.findall(clean[p][i]) if "deleteAccount" in t)
            anchored = anchored or fn
            for t in IDENT.findall(clean[p][i]):
                if "deleteAccount" in t and def_at(lines, clean[p], i, fn_pats(re.escape(t)), js):
                    anchored = fn = True
                    entry.add(t)
            region, ok = block(lines, i, 0)
            if fn:
                own.setdefault(p, set()).update(region)
            state["unsure"] = state["unsure"] or not ok
            evidence(p, region)
            harvest(p, region, fn)
    if not anchored:
        print("UNSURE")
        return
    # The entry point must be used somewhere, as a call or an action handed to a control. A dead one proves nothing.
    used, early = False, []
    for name in sorted(entry):
        pat = rx("~b" + re.escape(name) + "~b")
        for p, i in where.get(name, []):
            if i in own.get(p, ()) or TESTPATH.search(p):
                continue
            cc = scrub(nocom[p][i])
            for m in pat.finditer(cc):
                if decl_ref(cc, m, cc[: m.start()]):
                    continue
                if def_at(src[p], clean[p], i, fn_pats(re.escape(name)), p.endswith(JS_EXT)):
                    continue
                used = True
                # A use inside an if, else or when branch, or a ternary, follows the sibling branches too.
                lines = {i} if TERNARY.search(cc) else set()
                br = branch_lines([scrub(x) for x in nocom[p]], i, m.start())
                if br is None:
                    state["unsure"] = True
                else:
                    lines.update(br)
                if lines:
                    region = sorted(lines)
                    early.extend((p, j) for j in region)
                    harvest(p, region, False)
                break
    # Nothing weak reached is still reported, but a deletion nothing uses is never called clean.
    state["unsure"] = state["unsure"] or not used
    for hop in range(MAX_HOPS):
        names = sorted(t for t in frontier if t not in seen)
        seen.update(names)
        if len(seen) > MAX_NAMES:
            print("UNSURE")
            return
        frontier.clear()
        reached, early = early, []
        for name in names:
            n = re.escape(name)
            vpats, fpats = val_defs(n), fn_pats(n)
            closure = rx(
                "~b<?let|var|val|lateinit var>>~s+"
                + n
                + "~s*:[^=~"
                + LB
                + "]*" + LP + "?:->|=>" + RP + "[^=~"
                + LB
                + "]*$"
            )
            bound = rx("~b" + n + "~s*[:=]")
            for p, i in where.get(name, []):
                c = clean[p][i]
                if any(w in TYPEKW for w in c.split(name)[0].split()):
                    continue
                if closure.search(c):
                    state["unsure"] = True
                    continue
                if bound.search(c) and "mailto:" in src[p][i]:
                    reached.append((p, i))
                d = def_at(src[p], clean[p], i, fpats, p.endswith(JS_EXT))
                scoped = d is not None
                extra = []
                if not d:
                    for pat in vpats:
                        m = pat.search(c)
                        if m:
                            d = (i, m.start())
                            extra = value_lines(clean[p], i, m.start())
                            break
                if not d:
                    m = typed_decl(n).search(c)
                    if m:
                        extra = getter_lines(clean[p], i)
                        if extra != []:
                            d = (i, m.start())
                if extra is None:
                    # A value that cannot be found is never vouched for.
                    state["unsure"] = True
                    extra = []
                if not d:
                    continue
                defined.add(name)
                region, ok = block(src[p], d[0], d[1])
                region = region + [q for q in extra if q not in region]
                if d[0] != i:
                    region = list(range(i, d[0])) + region
                k = region[0]
                while k > 0 and k > region[0] - 5 and src[p][k - 1].strip().startswith("@"):
                    k -= 1
                region = list(range(k, region[0])) + region
                state["unsure"] = state["unsure"] or not ok
                reached.extend((p, j) for j in region)
                evidence(p, region)
                harvest(p, region, scoped)
        for p, j in reached:
            if WEAK.search(LAYOUT.sub(" ", src[p][j])):
                print("WEAK" + TAB + p + TAB + str(j + 1))
                return
        if not (frontier - seen):
            if any(
                nm not in defined and not allowed(nm, rt, lit, apptypes)
                for nm, rt, lit in called
            ):
                state["unsure"] = True
            # CLEAN needs a real deletion call in what the deletion reaches, not just nothing weak found.
            # A users id path counts only when the deletion also names the signed in user.
            real = state["real"] or (state["generic"] and state["selfref"])
            print("CLEAN" if real and not state["unsure"] else "UNSURE")
            return
    print("UNSURE")


main()
DELPY
  )" "$FILELIST" 2>/dev/null || echo UNSURE
  }
  if grep_has 'deleteAccount|delete account'; then
    # The deleting file, then the code the deletion calls across files, then an account deactivation endpoint or a deletion mailto.
    # Where the calls cannot be followed, any mailto: or deactivate counts, as before.
    DEL_WEAK="$(tr '\n' '\0' < "$FILELIST" | xargs -0 grep -EIl -e 'deleteAccount|delete account' 2>/dev/null | tr '\n' '\0' | xargs -0 grep -EIl -e 'mailto:|deactivate' 2>/dev/null | head -1)"
    DEL_N=""; DEL_FOLLOW=""
    if [ -z "$DEL_WEAK" ]; then
      DEL_FOLLOW="$(del_follow | head -1)"
      case "$DEL_FOLLOW" in WEAK*) DEL_WEAK="$(printf '%s\n' "$DEL_FOLLOW" | cut -f2)"; DEL_N="$(printf '%s\n' "$DEL_FOLLOW" | cut -f3)" ;; esac
    fi
    [ -n "$DEL_WEAK" ] || DEL_WEAK="$(tr '\n' '\0' < "$FILELIST" | xargs -0 grep -EIl -e '/deactivate|deactivate(Account|User)' 2>/dev/null | while IFS= read -r f; do grep -E '/deactivate|deactivate(Account|User)' "$f" | grep -vqE '[Dd]evices?/deactivate' && echo "$f"; done | head -1)"
    [ -n "$DEL_WEAK" ] || DEL_WEAK="$(tr '\n' '\0' < "$FILELIST" | xargs -0 grep -EIl -e '([Dd]elet|[Rr]emov|[Aa]ccount).*mailto:|mailto:[^\"]*([Dd]elet|[Rr]emov|[Aa]ccount)' 2>/dev/null | head -1)"
    if [ -z "$DEL_WEAK" ] && [ "$DEL_FOLLOW" != CLEAN ]; then
      DEL_WEAK="$(tr '\n' '\0' < "$FILELIST" | xargs -0 grep -EIl -e 'mailto:|deactivate' 2>/dev/null | head -1)"
    fi
    if [ -n "$DEL_WEAK" ]; then
      [ -n "$DEL_N" ] || DEL_N="$(grep -En -m1 -e 'mailto:|deactivate' "$DEL_WEAK" 2>/dev/null | cut -d: -f1)"
      finding high "APPLE-ACCOUNT-DELETION-WEAK" "Account removal may be deactivate or mailto only" "Provide genuine in app deletion of the account and its data, not a deactivate or external form." at "${DEL_WEAK#"${DIR%/}"/}${DEL_N:+:$DEL_N}"
    fi
  fi
  if grep_has 'fixed-odds|betting'; then
    finding critical "APPLE-GAMBLING-BRAZIL-LICENSE" "Fixed-odds or betting keyword detected in sources" "Provide a valid fixed-odds betting license from the Secretariat of Prizes and Bets (SPA) in App Review Info, set age rating to A18, and submit a new version to trigger verification (Apple policy May 8, 2026)." src 'fixed-odds|betting'
  fi
  if apple_has 'Image\('; then
    if ! grep_has 'accessibilityLabel|accessibilityIdentifier|accessibilityHidden|accessibilityElement'; then
      finding medium "APPLE-ACCESSIBILITY-VOICEOVER" "SwiftUI Image or UIKit component without VoiceOver accessibility attribute" "Provide an accessibilityLabel or use decorative initializers (Apple Design - Accessibility)." apple 'Image\('
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
  if apple_has 'onTapGesture|Button'; then
    if ! grep_has 'FeedbackGenerator|CoreHaptics'; then
      finding medium "APPLE-ACCESSIBILITY-HAPTICS" "Taps or button interactions without tactile feedback" "Integrate haptic feedback generators to improve interaction accessibility (Apple Design - Accessibility)." apple 'onTapGesture|Button'
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
  PERM_AT="$(permission_at 'ACCESS_BACKGROUND_LOCATION')"
  if [ -n "$PERM_AT" ]; then
    finding critical "GOOGLE-PERM-BACKGROUND-LOCATION" "Background location permission declared" "Justify with a core feature and prominent disclosure, or use foreground location." at "$PERM_AT"
  fi
  PERM_AT="$(permission_at 'MANAGE_EXTERNAL_STORAGE')"
  if [ -n "$PERM_AT" ]; then
    finding critical "GOOGLE-PERM-ALL-FILES" "All files access declared" "Use scoped storage. Request all files access only for a qualifying use case." at "$PERM_AT"
  fi
  PERM_AT="$(permission_at 'android\.permission\.(READ_SMS|SEND_SMS|RECEIVE_SMS|READ_CALL_LOG|WRITE_CALL_LOG)')"
  if [ -n "$PERM_AT" ]; then
    finding critical "GOOGLE-PERM-SMS-CALLLOG" "SMS or Call Log permission declared" "Use the permissions declaration for an approved core use case, or drop it." at "$PERM_AT"
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
  # A scheme inside <queries> names apps this app wants to see (package visibility), not a link it handles.
  # Each manifest is read element by element, so the first android:scheme outside <queries> and comments is named.
  DL_AT="$(tr '\n' '\0' < "$FILELIST" | xargs -0 grep -l 'android:scheme' 2>/dev/null | tr '\n' '\0' | xargs -0 awk 'BEGIN { RS = "<" } FNR == 1 { q = 0; c = 0; ln = 1 }
    { s = $0
      if (c) { if (s ~ /-->/) c = 0 }
      else if (s ~ /^!--/) { if (s !~ /-->/) c = 1 }
      else if (s ~ /^queries[^>]*\/>/) { }
      else if (s ~ /^queries[ \t\r\n>]/) q = 1
      else if (s ~ /^\/queries[ \t\r\n>]/) q = 0
      else if (!q && s !~ /^!--/ && (p = index(s, "android:scheme")) > 0) { pre = substr(s, 1, p); print FILENAME ":" ln + gsub(/\n/, "", pre); exit }
      ln += gsub(/\n/, "", s) }' 2>/dev/null | head -1)"
  if [ -n "$DL_AT" ]; then
    if ! grep_has 'assetlinks.json'; then
      finding high "BOTH-UNSAFE-DEEPLINK" "Custom URL deep link schemes declared without App Links configuration" "Configure App Links (Android) using assetlinks.json verification to prevent URL hijacking." at "${DL_AT#"${DIR%/}"/}"
    fi
  fi
  # Play Console refuses a debuggable APK or app bundle.
  release_manifest_debuggable() {
    [ -s "$FILELIST" ] || return 1
    grep '/AndroidManifest[.]xml$' "$FILELIST" | grep -vE '/src/(debug|androidTest|test)[^/]*/' | tr '\n' '\0' \
      | xargs -0 grep -EIls -e "android:debuggable[[:space:]]*=[[:space:]]*[\"']true[\"']" 2>/dev/null | grep . >/dev/null
  }
  if release_manifest_debuggable; then
    finding critical "ANDROID-DEBUGGABLE-RELEASE" "android:debuggable is true in the manifest" "Remove android:debuggable from the manifest and let the build type set it. Play Console rejects a debuggable APK or app bundle." manifest 'android:debuggable'
  fi
  # A specialUse foreground service needs its subtype property and a Play Console declaration.
  special_use_undeclared() {  # XML parse per service, so comments and other services never count
    [ -s "$FILELIST" ] || return 1
    command -v python3 >/dev/null 2>&1 || return 1
    local mf
    mf="$(grep '/AndroidManifest[.]xml$' "$FILELIST" | grep -vE '/src/(debug|androidTest|test)[^/]*/')"
    [ -n "$mf" ] || return 1
    printf '%s\n' "$mf" | tr '\n' '\0' | xargs -0 python3 -c "$(cat <<'FGSPY'
import sys
import xml.etree.ElementTree as ET

A = "{http://schemas.android.com/apk/res/android}"
SUBTYPE = "android.app.PROPERTY_SPECIAL_USE_FGS_SUBTYPE"
for path in sys.argv[1:]:
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError):
        continue
    for svc in root.iter("service"):
        types = svc.get(A + "foregroundServiceType", "")
        if "specialUse" not in [t.strip() for t in types.split("|")]:
            continue
        if not any(p.get(A + "name") == SUBTYPE for p in svc.iter("property")):
            sys.exit(0)
sys.exit(1)
FGSPY
)" 2>/dev/null
  }
  if special_use_undeclared; then
    finding high "ANDROID-FGS-SPECIAL-USE-UNDECLARED" "specialUse foreground service without a subtype property" "Add a property named android.app.PROPERTY_SPECIAL_USE_FGS_SUBTYPE inside the service, and justify the use in the Play Console foreground service declaration." manifest 'android:foregroundServiceType=.*specialUse'
  fi
  # Play requires a 64-bit build of every native library that ships a 32-bit ABI.
  abi_missing_64() {  # comment-aware, brace-scoped, skips debug blocks, merges += statements per block
    [ -s "$FILELIST" ] || return 1
    command -v python3 >/dev/null 2>&1 || return 1
    local gf
    gf="$(grep -E '[.](gradle|kts)$' "$FILELIST")"
    [ -n "$gf" ] || return 1
    printf '%s\n' "$gf" | tr '\n' '\0' | xargs -0 python3 -c "$(cat <<'ABIPY'
import re
import sys

ABI_RE = re.compile(r"[\"'](armeabi-v7a|arm64-v8a|x86_64|x86)[\"']")
NAME_RE = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*(\([^(){}]*\))?\s*$")


def strip_comments(src):
    out, i, n, quote = [], 0, len(src), None
    while i < n:
        c = src[i]
        if quote:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(src[i + 1])
                i += 2
                continue
            if c == quote or c == "\n":
                quote = None
            i += 1
            continue
        if c in "\"'":
            quote = c
            out.append(c)
            i += 1
        elif src.startswith("//", i):
            j = src.find("\n", i)
            i = n if j < 0 else j
        elif src.startswith("/*", i):
            j = src.find("*/", i + 2)
            i = n if j < 0 else j + 2
            out.append(" ")
        else:
            out.append(c)
            i += 1
    return "".join(out)


def statement_end(text, start):
    depth, i = 0, start
    while i < len(text):
        c = text[i]
        if c in "([":
            depth += 1
        elif c in ")]":
            depth -= 1
        elif c == "}" and depth <= 0:
            return i
        elif (
            c == "\n"
            and depth <= 0
            and not text[start:i].rstrip().endswith((",", "(", "+=", "="))
        ):
            return i
        i += 1
    return i


def groups(text):
    found, stack, i = {}, [], 0
    while i < len(text):
        c = text[i]
        if c == "{":
            m = NAME_RE.search(text[max(0, i - 80) : i])
            label = (m.group(0) if m else "").lower()
            stack.append(
                "debug" if "debug" in label else (" ".join(label.split()) or "?")
            )
        elif c == "}":
            if stack:
                stack.pop()
        elif text.startswith("abiFilters", i):
            end = statement_end(text, i)
            if "debug" not in stack:
                stmt = text[i:end]
                bucket = found.setdefault(tuple(stack), set())
                rest = stmt[len("abiFilters"):].lstrip()
                if rest.startswith(".clear"):
                    bucket.clear()
                elif rest.startswith(("-=", ".remove")):
                    bucket.difference_update(ABI_RE.findall(stmt))
                else:
                    bucket.update(ABI_RE.findall(stmt))
            i = end
            continue
        i += 1
    return found


for path in sys.argv[1:]:
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = strip_comments(fh.read())
    except OSError:
        continue
    for abis in groups(text).values():
        if ("armeabi-v7a" in abis and "arm64-v8a" not in abis) or (
            "x86" in abis and "x86_64" not in abis
        ):
            sys.exit(0)
sys.exit(1)
ABIPY
)" 2>/dev/null
  }
  if abi_missing_64; then
    finding high "ANDROID-64BIT-ABI-MISSING" "abiFilters ship a 32-bit ABI without its 64-bit pair" "Add arm64-v8a, and x86_64 when x86 ships, to abiFilters. Google Play requires a 64-bit version of every native library." src 'abiFilters'
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
  PERM_AT="$(permission_at 'android\.permission\.(READ_CONTACTS|WRITE_CONTACTS|READ_SMS|SEND_SMS|RECEIVE_SMS|READ_CALL_LOG|WRITE_CALL_LOG|GET_ACCOUNTS|MANAGE_EXTERNAL_STORAGE)' manifest)"
  if [ -n "$PERM_AT" ]; then
    if ! grep_has 'prominent disclosure|user consent|privacy consent|accept policy|[Pp]rominentDisclosure|[Dd]isclosureDialog|[Cc]onsentDialog|showDisclosure|requestConsent'; then
      finding critical "ANDROID-USER-DATA-DISCLOSURE" "Missing prominent disclosure for sensitive user data" "Provide a prominent in-app disclosure before collecting sensitive personal data, and obtain explicit user consent." at "$PERM_AT"
    fi
  fi
  # Prints the first file:line that uses the advertising ID, or nothing. A removed AD_ID permission (firebase-analytics
  # merges one in) does not count. AD_ID after a letter or digit is the end of a longer word (THREAD_ID, UPLOAD_ID).
  advertising_id_at() {
    permission_at 'com\.google\.android\.gms\.permission\.AD_ID|(^|[^A-Za-z0-9])AD_ID|getAdvertisingIdInfo'
  }
  ADID_AT="$(advertising_id_at)"
  if [ -n "$ADID_AT" ]; then
    if ! grep_has 'opt-out|reset AD_ID|advertisingIdConsent|delete AD_ID'; then
      finding high "ANDROID-ADVERTISING-ID" "Google Play Advertising ID usage without disclosure or opt-out" "Declare the AD_ID permission in AndroidManifest.xml and handle user opt-out or deletion requests in full compliance with Google Play policy." at "$ADID_AT"
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
  printf '%s' "$rel" | tr '[:upper:]' '[:lower:]' | tr '/' '\n' | grep -xE 'demos?|examples?|samples?|playgrounds?' >/dev/null && return 1
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

# A stale checklist gives false confidence. Every report names its rule pack version and the newest
# verified_on date, and warns when that is older than APP_STORE_GUARD_STALE_DAYS (default 60).
rule_pack_line() {
  local hd root="" c ver="unknown" dates="" newest="" oldest="" total=0 old=0 cutoff age="" then_s now_s stale="${APP_STORE_GUARD_STALE_DAYS:-60}"
  case "$stale" in ''|*[!0-9]*) stale=60 ;; esac
  hd="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  for c in "$hd/../.." "$hd/../skills/app-store-compliance" "${HOME:-}/.agents/skills/app-store-compliance"; do
    if [ -f "$c/data/regulatory-deadlines.json" ]; then root="$(cd "$c" && pwd)"; break; fi
  done
  if [ -z "$root" ]; then
    echo "Rule pack. unknown. The guard runs without its data folder, so its rule dates cannot be shown. Reinstall with scripts/install.sh."
    return 0
  fi
  [ -f "$root/VERSION" ] && ver="$(tr -d '[:space:]' < "$root/VERSION")"
  dates="$(grep -oE '"verified_on":[[:space:]]*"[0-9]{4}-[0-9]{2}-[0-9]{2}"' "$root/data/regulatory-deadlines.json" 2>/dev/null | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | sort)"
  if [ -n "$dates" ]; then
    newest="$(printf '%s\n' "$dates" | tail -1)"; oldest="$(printf '%s\n' "$dates" | head -1)"
    total="$(printf '%s\n' "$dates" | wc -l | tr -d ' ')"
    now_s="$(date +%s 2>/dev/null)"
    then_s="$(date -j -f '%Y-%m-%d %H:%M:%S' "$newest 00:00:00" +%s 2>/dev/null || date -d "$newest 00:00:00" +%s 2>/dev/null)"
    cutoff="$(date -v-"${stale}"d +%Y-%m-%d 2>/dev/null || date -d "-$stale days" +%Y-%m-%d 2>/dev/null)"
    case "$now_s" in ''|*[!0-9]*) now_s="" ;; esac
    case "$then_s" in ''|*[!0-9]*) then_s="" ;; esac
    case "$cutoff" in [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]) ;; *) cutoff="" ;; esac
    if [ -n "$now_s" ] && [ -n "$then_s" ] && [ -n "$cutoff" ] && [ "$now_s" -ge "$then_s" ]; then
      age=$(( (now_s - then_s) / 86400 ))
      old="$(printf '%s\n' "$dates" | awk -v c="$cutoff" '$0 < c' | wc -l | tr -d ' ')"
    fi
  fi
  if [ -n "$newest" ]; then
    echo "Rule pack. v$ver. Its $total dated sources were verified between $oldest and $newest${age:+ (newest $age days ago)}. The checks run against this dated snapshot, not the live guideline pages."
  else
    echo "Rule pack. v$ver, sources last verified unknown. The checks run against this dated snapshot, not the live guideline pages."
  fi
  if [ -n "$age" ] && [ "$age" -le "$stale" ] && [ "${old:-0}" -gt 0 ]; then
    echo "Rule pack. $old of $total dated sources were last verified more than $stale days ago, so their rules may have changed since. Each one carries its date as verified_on in data/regulatory-deadlines.json."
  fi
  if [ -z "$age" ]; then
    echo "Rule pack freshness not checked. The verified date could not be read or compared, so treat these rules as possibly stale."
  elif [ "$age" -gt "$stale" ]; then
    echo "Rule pack STALE. Older than $stale days, so a rule Apple or Google changed since then is not checked. Update with git -C \"$root\" pull, or reinstall."
  fi
}

# What a code scan cannot prove, recorded per app in .app-review-readiness.json (else the workspace's).
# A recorded fail blocks. "enforce": true or APP_STORE_GUARD_REQUIRE_READINESS=1 makes an open check block too.
readiness_check() {  # $1 app root, $2 workspace root
  local app="${1%/}" ws="${2%/}" d f="" from="" label req="${APP_STORE_GUARD_REQUIRE_READINESS:-0}" out rc sev id title fix
  label="${app#"$ws"/}"; [ "$app" = "$ws" ] && label="this project"
  d="$app"
  while :; do
    if [ -e "$d/.app-review-readiness.json" ] || [ -L "$d/.app-review-readiness.json" ]; then f="$d/.app-review-readiness.json"; break; fi
    case "$d/" in "$ws"/*) ;; *) break ;; esac
    { [ "$d" = "$ws" ] || [ "$d" = "/" ] || [ -z "$d" ]; } && break
    d="$(dirname "$d")"
  done
  [ -z "$f" ] && { [ -e "$ws/.app-review-readiness.json" ] || [ -L "$ws/.app-review-readiness.json" ]; } && f="$ws/.app-review-readiness.json"
  if [ -n "$f" ] && [ "$f" != "$app/.app-review-readiness.json" ]; then
    from=", from ${f#"$ws"/}"; [ "$f" = "$ws/.app-review-readiness.json" ] && from=", from the workspace file"
  fi
  echo ""
  if [ -z "$f" ]; then
    echo "Manual checks for $label. Not attested. The scan proves code, config and manifests only. It cannot prove a working demo account, a live backend, review notes, screenshots of this build, account deletion on a real device, privacy labels that match runtime, or an in-app purchase the reviewer can reach. Copy templates/app-review-readiness.json to the app folder and record each one."
    [ "$req" = "1" ] && finding critical "MANUAL-READINESS-MISSING" "No .app-review-readiness.json for $label, and readiness is required" "Copy templates/app-review-readiness.json to the app folder, test each item on the release build, and record pass, fail, or n/a with a reason."
    flush_findings; return 0
  fi
  if [ ! -f "$f" ] || [ ! -r "$f" ]; then
    finding critical "MANUAL-READINESS-UNREADABLE" ".app-review-readiness.json for $label${from} exists but is not a readable file, so a fail inside it cannot be seen" "Replace it with a regular file shaped like templates/app-review-readiness.json, or remove it."
    flush_findings; return 0
  fi
  if ! tool_ok python3 -c pass; then
    finding critical "MANUAL-READINESS-UNREAD" ".app-review-readiness.json exists for $label, but python3 is not available to read it" "Install python3, then run the guard again."
    flush_findings; return 0
  fi
  out="$(python3 - "$f" "$req" "$from" <<'PYR'
import datetime, json, os, re, signal, stat, sys, threading

CHECKS = [
    ("demo_account", True, "A reviewer can sign in with the demo account in the review notes", "Create a demo account that works against production, put it in App Review Information, and sign in with it on the release build (Apple 2.1, Google Play app access)."),
    ("live_backend", True, "The backend the reviewer reaches is live and holds test data", "Point the release build at production, load the data a reviewer needs, and keep it up for the whole review (Apple 2.1)."),
    ("review_notes", True, "Review notes say where every feature is and how to reach it", "Write the tap path to each feature, the IAP, and anything behind login or region in App Review Information (Apple 2.1, 2.3.1)."),
    ("screenshots_match_build", True, "Screenshots show this build, in use, for each device family you support", "Capture screenshots from the release build with the app in use, and upload the required sizes for each device family you support, iPad included if the app runs there. App Store Connect scales the smaller sizes, so check those layouts on a device (Apple 2.3.3, 2.3.14)."),
    ("account_deletion_device_test", True, "Account deletion works end to end on a real device", "Delete an account on a real device. After the completion time you tell users, check that the account and its sessions are gone, that its data is deleted except what you disclose keeping (Apple allows records the law requires, Google Play also allows security, fraud-prevention, and regulatory records), and that signing in again does not bring the old account back (Apple 5.1.1(v), Google Play account deletion)."),
    ("privacy_labels_match_runtime", False, "Privacy labels and Data Safety match what the build and its SDKs collect", "Compare App Privacy answers and the Data Safety form with traffic from the release build, SDKs included (Apple 5.1.2, Google Play User Data). Every app has this check, so n/a is not accepted."),
    ("iap_reachable_by_reviewer", True, "A reviewer can find and complete every in-app purchase", "Make every product reachable in the review build, submit the IAPs with the version, and name where they are in the review notes (Apple 2.1(b), 3.1.1)."),
]


class Dup(list):
    pass


def keep_dups(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            prev = out[key]
            if isinstance(prev, Dup):
                prev.append(value)
            else:
                out[key] = Dup([prev, value])
        else:
            out[key] = value
    return out


def flat(value):
    if isinstance(value, Dup):
        for item in value:
            yield from flat(item)
    else:
        yield value


def merge_checks(value):
    """Every checks object is read, and every value kept, so a fail is never lost."""
    parts = list(flat(value))
    good = [p for p in parts if isinstance(p, dict)]
    merged = {}
    for part in good:
        for key, item in part.items():
            merged.setdefault(key, []).extend(flat(item))
    checks = {k: (Dup(v) if len(v) > 1 else v[0]) for k, v in merged.items()} if good else None
    return checks, len(good) < len(parts)


def clean(value, limit=300):
    text = str(value).encode("ascii", "replace").decode("ascii")
    return "".join(c if c.isprintable() and c not in "\t" else " " for c in text)[:limit]


def emit(*fields):
    sys.stdout.write("\t".join(clean(f) for f in fields) + "\n")


READ_LIMIT = 8 * 1024 * 1024
READ_DEADLINE = 10


class Late(Exception):
    pass


def late(signum, frame):
    raise Late()


FINISH = threading.Lock()
WATCHDOGS = []


def give_up():
    # Without SIGALRM a blocked read cannot be interrupted. Whichever side takes FINISH first owns END.
    if not FINISH.acquire(False):
        return
    try:
        emit("critical", "MANUAL-READINESS-UNREADABLE", ".app-review-readiness.json could not be read within %d seconds, so a fail inside it cannot be seen" % READ_DEADLINE, "Move it to a local disk as a regular file shaped like templates/app-review-readiness.json.")
        sys.stdout.write("END\n")
        sys.stdout.flush()
    finally:
        os._exit(0)


def run():
    path, required, src = sys.argv[1], sys.argv[2] == "1", sys.argv[3]
    raw = b""
    # A stalled read or a FIFO where O_NONBLOCK is missing must end in a finding, never a hang.
    if hasattr(signal, "SIGALRM"):
        signal.signal(signal.SIGALRM, late)
        signal.alarm(READ_DEADLINE)
    else:
        watchdog = threading.Timer(READ_DEADLINE, give_up)
        watchdog.daemon = True
        WATCHDOGS.append(watchdog)
        watchdog.start()
    try:
        # Non-blocking open and fstat on the same descriptor, so a file swapped for a FIFO cannot hang the read.
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0))
        try:
            if not stat.S_ISREG(os.fstat(fd).st_mode):
                emit("critical", "MANUAL-READINESS-UNREADABLE", ".app-review-readiness.json is not a regular file, so a fail inside it cannot be seen", "Replace it with a regular file shaped like templates/app-review-readiness.json, or remove it.")
                return
            fh = os.fdopen(fd, "rb")
            fd = -1
            with fh:
                raw = fh.read(READ_LIMIT + 1)
            if len(raw) > READ_LIMIT:
                emit("critical", "MANUAL-READINESS-UNREADABLE", ".app-review-readiness.json is larger than 8 MiB, so it was not read and a fail inside it cannot be seen", "Keep it to the shape of templates/app-review-readiness.json, which is under 1 KB.")
                return
        finally:
            if fd >= 0:
                os.close(fd)
        data = json.loads(raw, object_pairs_hook=keep_dups)
    except Late:
        emit("critical", "MANUAL-READINESS-UNREADABLE", ".app-review-readiness.json could not be read within %d seconds, so a fail inside it cannot be seen" % READ_DEADLINE, "Move it to a local disk as a regular file shaped like templates/app-review-readiness.json.")
        return
    except (OSError, ValueError, RecursionError):
        data = None
    dups = isinstance(data, dict) and any(isinstance(v, Dup) for v in data.values())
    if isinstance(data, dict):
        if isinstance(data.get("checks"), Dup):
            data["checks"], bad_part = merge_checks(data["checks"])
            if bad_part and data["checks"] is not None:
                emit("critical", "MANUAL-READINESS-UNREADABLE", ".app-review-readiness.json repeats checks and one of them is not an object, so a fail inside it cannot be ruled out", "Keep one checks object, as in templates/app-review-readiness.json.")
        strict = required or (data.get("enforce") is True if not isinstance(data.get("enforce"), Dup) else any(v is True for v in data["enforce"]))
    else:
        # Only an unparsed file falls back to the raw text, to stay on the safe side.
        strict = required or (data is None and re.search(rb'"enforce"\s*:\s*true', raw) is not None)
    if not isinstance(data, dict) or not isinstance(data.get("checks"), dict):
        emit("critical", "MANUAL-READINESS-UNREADABLE", ".app-review-readiness.json is not valid JSON with a checks object, so a fail inside it cannot be seen", "Fix the file using templates/app-review-readiness.json as the shape. Until then no manual check counts as done.")
        return
    checks = data["checks"]
    notes = data.get("notes")
    if notes is None:
        notes = {}
    elif not isinstance(notes, dict):
        emit("high", "MANUAL-READINESS-NOTES-INVALID", "notes in .app-review-readiness.json is not an object, so no n/a reason counts", "Make notes an object keyed by check name, as in templates/app-review-readiness.json.")
        notes = {}
    passed, still_open = 0, []
    for key, na_ok, title, fix in CHECKS:
        tag = "MANUAL-" + key.upper().replace("_", "-")
        value = checks.get(key, "missing")
        if isinstance(value, Dup):
            dups = True
        values = list(flat(value))
        if any(not isinstance(v, str) for v in values):
            emit("critical", tag + "-INVALID", "%s, recorded as something other than text, so a fail inside it cannot be ruled out" % title, "Write pass, fail, n/a, or todo as plain text, as in templates/app-review-readiness.json.")
            still_open.append(key)
            continue
        seen = {v.strip().lower() for v in values}
        value = "fail" if "fail" in seen else (seen.pop() if len(seen) == 1 else "conflicting")
        reason = notes.get(key)
        has_reason = isinstance(reason, str) and reason.strip() != ""
        if value == "pass" or (value in ("n/a", "na") and na_ok and has_reason):
            passed += 1
            continue
        if value == "fail":
            emit("critical", tag + "-FAILED", title + ", recorded as failed", fix)
            continue
        if value in ("n/a", "na"):
            value = "n/a not accepted" if not na_ok else "n/a with no reason in notes"
        still_open.append(key)
        if strict:
            emit("critical", tag + "-UNVERIFIED", "%s, not verified (%s)" % (title, value), fix)
    if dups:
        emit("high", "MANUAL-READINESS-DUPLICATE-KEY", ".app-review-readiness.json repeats a key, so the guard kept every value and a recorded fail still counts", "Keep each key once, as in templates/app-review-readiness.json.")
    when = data.get("checked_on")
    when = when if isinstance(when, str) else None
    try:
        age = (datetime.date.today() - datetime.date.fromisoformat(str(when))).days
    except (TypeError, ValueError):
        age = None
    build = data.get("build")
    build = build if isinstance(build, str) and build.strip() else "an unnamed build"
    emit("info", "Manual checks. %d of %d attested for %s%s%s.%s" % (
        passed, len(CHECKS), build, (", checked %s" % when) if age is not None else ", no valid checked_on date", src,
        (" Still open. " + ", ".join(still_open) + ".") if still_open else ""))
    if age is None:
        emit("high", "MANUAL-READINESS-STALE", ".app-review-readiness.json has no valid checked_on date", "Re-run the manual checks on the build you are submitting and set checked_on to that day, as YYYY-MM-DD.")
    elif age < 0:
        emit("high", "MANUAL-READINESS-STALE", ".app-review-readiness.json has a checked_on date in the future", "Set checked_on to the day the manual checks were actually run.")
    elif age > 30:
        emit("high", "MANUAL-READINESS-STALE", ".app-review-readiness.json is older than 30 days", "Re-run the manual checks on the build you are submitting and update checked_on.")


try:
    run()
except Exception:
    sys.stdout.write("CRASH\n")
finally:
    if hasattr(signal, "SIGALRM"):
        signal.alarm(0)
    for watchdog in WATCHDOGS:
        watchdog.cancel()
    if not FINISH.acquire(False):
        threading.Event().wait(5)
        os._exit(0)
sys.stdout.write("END\n")
PYR
)"; rc=$?
  if [ "$rc" -ne 0 ] || [ "$(printf '%s\n' "$out" | tail -n 1)" != "END" ] || printf '%s\n' "$out" | grep_q -x 'CRASH'; then
    finding critical "MANUAL-READINESS-UNREADABLE" ".app-review-readiness.json for $label could not be read" "Fix the file using templates/app-review-readiness.json as the shape. Until then no manual check counts as done."
    flush_findings; return 0
  fi
  while IFS="$(printf '\t')" read -r sev id title fix; do
    case "$sev" in
      info) echo "${id/Manual checks./Manual checks for $label.}" ;;
      critical|high|medium) case "$id" in MANUAL-[A-Z-]*) finding "$sev" "$id" "$title ($label)" "$fix" ;; esac ;;
    esac
  done <<READINESS_EOF
$out
READINESS_EOF
  flush_findings
}

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
rule_pack_line
ROOTS="$(app_roots)"
if [ -n "$ROOTS" ]; then
  PROJECT_ROOT="${DIR%/}"
  echo "Apps. $(printf '%s\n' "$ROOTS" | grep -c .) app roots, each scanned on its own"
  echo ""
  POOL_FW=""; SPLIT_NATIVE=""
  if printf '%s\n' "$ROOTS" | sed 's:/$::' | grep -xF "$PROJECT_ROOT" >/dev/null; then
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
    if [ -n "$POOL_FW" ] && { [ "${ROOT%/}" = "$PROJECT_ROOT" ] || printf '%s' "$SPLIT_NATIVE" | grep_q -xF "${ROOT%/}"; }; then
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
    else
      readiness_check "$ROOT" "$PROJECT_ROOT"
    fi
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
  readiness_check "$DIR" "$DIR"
  RD_OTHER="$(find "$DIR" -mindepth 2 -maxdepth 8 -name .app-review-readiness.json -type f -print 2>/dev/null | grep -v -e '/node_modules/' -e '/Pods/' -e '/[.]pub-cache/' -e '/[.]git/' | head -1)"
  if [ -n "$RD_OTHER" ]; then
    echo "Manual checks. Another readiness file below this folder was not read, for example ${RD_OTHER#"${DIR%/}"/}. The guard reads the file in the folder you scan, so scan that app folder to use it."
  fi
fi
print_deadlines


# ===== summary and exit =====
echo ""
echo "Summary. critical=$CRIT high=$HIGH medium=$MED"
# Printed before every exit, so a blocked run still says whether every app root was scanned (Fleet Sweep reads it).
COV_WHY=""
[ -n "$SCAN_ERROR" ] && COV_WHY="scan error"
[ -n "$UNCHECKED" ] && COV_WHY="${COV_WHY:+$COV_WHY; }no native project in $UNCHECKED"
{ [ "$ANY_NATIVE" -eq 0 ] && { [ "$ANY_WEB" -eq 0 ] || [ "$ANY_NEEDS_NATIVE" -eq 1 ]; }; } && COV_WHY="${COV_WHY:+$COV_WHY; }no iOS or Android project found"
echo "Coverage. $([ -n "$COV_WHY" ] && echo incomplete || echo complete) ios=$ANY_IOS android=$ANY_AND web=$ANY_WEB${COV_WHY:+ reason=$COV_WHY}"
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
  if [ -n "$STDIN_JSON" ]; then block_unchecked "$NOTE"; emit_report 0; echo "$NOTE" >&2; exit 0; fi
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
  if [ -n "$STDIN_JSON" ]; then block_unchecked "$NOTE $NEXT"; emit_report 0; echo "$NOTE $NEXT" >&2; exit 0; fi
  exit 1
fi
echo ""
[ "$ANY_NATIVE" -eq 0 ] && echo "Web project only. No iOS or Android project was found here, so only the web checks ran."
echo "CLEAR. 0 critical risks in the code scan. Read any [HIGH] and [MEDIUM] lines above, then walk docs/PRE-SUBMISSION-CHECKLIST.md for the account and listing checks a scan cannot see."
emit_report 0; exit 0
