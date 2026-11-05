#!/usr/bin/env bash
# Gauntlet for fleet-sweep.py. A stub guard prints scripted reports, so every case is deterministic.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SWEEP="$HERE/fleet-sweep.py"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
pass=0; fail=0
ok() { pass=$((pass+1)); }
bad() { fail=$((fail+1)); echo "FAIL $1"; }
export FLEET_SWEEP_TESTING=1 FLEET_SWEEP_TEST_TODAY=2026-11-05

cat > "$T/guard.sh" <<'EOF'
#!/usr/bin/env bash
[ -f "$1/sleep" ] && sleep 5
[ -f "$1/report.txt" ] && cat "$1/report.txt"
exit "$(cat "$1/exit.txt" 2>/dev/null || echo 0)"
EOF
export FLEET_SWEEP_GUARD="$T/guard.sh"

app() { mkdir -p "$T/$1"; printf '%s' "$2" > "$T/$1/exit.txt"; printf '%b' "$3" > "$T/$1/report.txt"; }
COV='Coverage. complete ios=1 android=1 web=0\n'
CLEAN="Summary. critical=0 high=0 medium=0\n${COV}CLEAR.\n"
CRIT="  [CRITICAL] X  Missing privacy manifest\n      file. ios/App/Info.plist\n      fix. Add PrivacyInfo.xcprivacy\n  [HIGH]     H  Arbitrary loads allowed\n      fix. Remove NSAllowsArbitraryLoads\n\nSummary. critical=1 high=1 medium=0\n${COV}BLOCKED.\n"
HIGHONLY="  [HIGH]     H  Arbitrary loads allowed\n      file. ios/App/Info.plist\n      fix. Remove NSAllowsArbitraryLoads\n\nSummary. critical=0 high=1 medium=0\n${COV}CLEAR.\n"

fleet() {  # args are name, name:platforms, or name:platforms:readinessjson
  python3 - "$T" "$@" > "$T/fleet.json" <<'EOF'
import json, sys
t, apps = sys.argv[1], []
for spec in sys.argv[2:]:
    name, plats, ready = (spec.split(":", 2) + ["", ""])[:3]
    a = {"name": name, "path": f"{t}/{name}"}
    if plats:
        a["platforms"] = plats.split(",")
    a["readiness"] = json.loads(ready) if ready else {"apple_agreements_signed": True}
    apps.append(a)
print(json.dumps({"fleet_name": "Test fleet", "apps": apps}))
EOF
}
run() { python3 "$SWEEP" "$T/fleet.json" "$@" > "$T/out.txt" 2>&1; echo $?; }
has() { grep -q -- "$1" "$T/out.txt"; }

# Verdicts and exit codes.
app clean 0 "$CLEAN"; fleet clean
[ "$(run)" = 0 ] && has "Fleet verdict. READY" && ok || bad "clean app is READY, exit 0"
app blocked 2 "$CRIT"; fleet clean blocked
[ "$(run)" = 2 ] && has "Fleet verdict. BLOCKED" && ok || bad "one blocked app blocks the fleet, exit 2"
app highonly 0 "$HIGHONLY"; fleet highonly
[ "$(run)" = 3 ] && has "READY_WITH_ACTIONS" && ok || bad "unresolved high exits 3, never 0"
has "fix. Remove NSAllowsArbitraryLoads" && has "file. ios/App/Info.plist" && ok || bad "every finding prints with file and fix"

# Readiness. Unknown is never success.
python3 -c "import json;print(json.dumps({'apps':[{'name':'clean','path':'$T/clean'}]}))" > "$T/fleet.json"
[ "$(run)" = 3 ] && has "readiness not tracked" && ok || bad "missing readiness is an owner action, exit 3"
fleet "clean::{\"a\": true, \"play_data_safety_matches_runtime\": false}"
[ "$(run)" = 3 ] && has "owner action. play_data_safety_matches_runtime" && ok || bad "false readiness is an owner action"
fleet "clean::{\"a\": \"yes\"}"
[ "$(run)" = 1 ] && has "true or false" && ok || bad "non-boolean readiness is an input error"

# Report integrity. Absence and contradiction are never success.
app nosummary 0 "  [HIGH]     X  y\n${COV}"; fleet nosummary
[ "$(run)" = 1 ] && has "exactly one well formed Summary" && ok || bad "missing Summary is NOT_CHECKED"
app nocov 0 "Summary. critical=0 high=0 medium=0\n"; fleet nocov
[ "$(run)" = 1 ] && has "Coverage line" && ok || bad "missing Coverage is NOT_CHECKED"
app hidhigh 0 "Summary. critical=0 high=7 medium=0\n${COV}"; fleet hidhigh
[ "$(run)" = 1 ] && has "do not match" && ok || bad "high count with no high findings is NOT_CHECKED"
app hidmed 0 "Summary. critical=0 high=0 medium=9\n${COV}"; fleet hidmed
[ "$(run)" = 1 ] && ok || bad "medium count with no medium findings is NOT_CHECKED"
app exit2clean 2 "Summary. critical=0 high=0 medium=0\n${COV}"; fleet exit2clean
[ "$(run)" = 1 ] && has "contradicts" && ok || bad "exit 2 with no criticals is NOT_CHECKED"
app twosum 0 "Summary. critical=1 high=1 medium=1\nSummary. critical=0 high=0 medium=0\n${COV}"; fleet twosum
[ "$(run)" = 1 ] && ok || bad "two Summary lines is NOT_CHECKED"
app suffix 0 "Summary. critical=0 high=0 medium=0BROKEN\n${COV}"; fleet suffix
[ "$(run)" = 1 ] && ok || bad "malformed Summary suffix is NOT_CHECKED"
app exit1 1 "NOT CHECKED.\nSummary. critical=0 high=0 medium=0\n${COV}"; fleet exit1
[ "$(run)" = 1 ] && ok || bad "guard exit 1 is NOT_CHECKED"
fleet ghost; [ "$(run)" = 1 ] && has "is not a folder" && ok || bad "missing app folder is NOT_CHECKED"
mkdir -p "$T/slow"; : > "$T/slow/sleep"; fleet slow
[ "$(run --timeout 1)" = 1 ] && has "did not finish" && ok || bad "guard timeout is NOT_CHECKED"

# Coverage. A waiver can never turn an incomplete scan into READY (Codex finding 1).
INC='Coverage. incomplete ios=1 android=0 web=0 reason=no native project in apps/unbuilt\n'
app partial 2 "  [CRITICAL] X  Missing privacy manifest\n      file. ios/App/Info.plist\n      fix. f\n\nSummary. critical=1 high=0 medium=0\n${INC}"
fleet partial
waiver() { python3 -c "import json,sys;print(json.dumps({'waivers':[json.loads(a) for a in sys.argv[1:]]}))" "$@" > "$T/w.json"; }
W='{"app":"APPNAME","finding_id":"X","severity":"critical","file":"ios/App/Info.plist","reason":"r","evidence":"e","reviewed_by":"Mirza","expires":"2027-01-01"}'
waiver "${W/APPNAME/partial}"
[ "$(run --waivers "$T/w.json")" = 1 ] && has "scan was incomplete" && ok || bad "waiver on an incomplete scan stays NOT_CHECKED"
app webonly 0 "Summary. critical=0 high=0 medium=0\nCoverage. complete ios=0 android=0 web=1\n"; fleet "webonly:ios,android"
[ "$(run)" = 1 ] && has "declared ios, android" && ok || bad "declared platform not scanned is NOT_CHECKED"
fleet "clean:ios"; [ "$(run)" = 0 ] && ok || bad "declared platform that was scanned passes"

# Waiver Ledger.
fleet blocked; waiver "${W/APPNAME/blocked}"
[ "$(run --waivers "$T/w.json")" = 3 ] && has "waived until 2027-01-01" && ok || bad "valid waiver sets aside the critical"
app twox 2 "  [CRITICAL] X  fixture\n      file. tests/fixture.plist\n  [CRITICAL] X  production\n      file. ios/App/Info.plist\n\nSummary. critical=2 high=0 medium=0\n${COV}"
fleet twox; waiver "$(echo "${W/APPNAME/twox}" | sed 's#ios/App/Info.plist#tests/fixture.plist#')"
[ "$(run --waivers "$T/w.json")" = 2 ] && has "production" && ok || bad "a waiver covers one occurrence, not every finding with that ID"
fleet blocked; waiver "$(echo "${W/APPNAME/blocked}" | sed 's/"critical"/"high"/')"
[ "$(run --waivers "$T/w.json")" = 2 ] && ok || bad "a waiver for a lower severity never hides a critical"
fleet blocked clean; waiver "${W/APPNAME/blocked}" "${W/APPNAME/blocked}"
[ "$(run --waivers "$T/w.json")" = 2 ] && has "none applied" && ok || bad "duplicate waivers cancel out"
waiver "${W/APPNAME/blocked}" "$(echo "${W/APPNAME/blocked}" | sed 's/2027-01-01/2026-11-01/')"
[ "$(run --waivers "$T/w.json")" = 2 ] && ok || bad "a valid and an expired duplicate cancel out"
for field in reason evidence reviewed_by; do
  for val in null false '[]' '{}' '""'; do
    waiver "$(python3 -c "import json,sys;w=json.loads(sys.argv[1]);w['$field']=json.loads('$val');print(json.dumps(w))" "${W/APPNAME/blocked}")"
    [ "$(run --waivers "$T/w.json")" = 2 ] || { bad "waiver with $field=$val was accepted"; continue 2; }
  done
done; ok
waiver "$(echo "${W/APPNAME/blocked}" | sed 's/2027-01-01/2026-11-01/')"
[ "$(run --waivers "$T/w.json")" = 2 ] && has "expired on 2026-11-01" && ok || bad "expired waiver brings the finding back"
waiver "$(echo "${W/APPNAME/blocked}" | sed 's/2027-01-01/2028-01-01/')"
[ "$(run --waivers "$T/w.json")" = 2 ] && has "more than 180 days" && ok || bad "waiver over 180 days is refused"
waiver "$(echo "${W/APPNAME/blocked}" | sed 's/2027-01-01/soon/')"
[ "$(run --waivers "$T/w.json")" = 2 ] && has "YYYY-MM-DD" && ok || bad "bad expiry is refused"
fleet clean; waiver "${W/APPNAME/clean}"; run --waivers "$T/w.json" >/dev/null
has "retire this waiver" && ok || bad "stale waiver is reported"
fleet blocked; waiver "${W/APPNAME/other}"
[ "$(run --waivers "$T/w.json")" = 2 ] && ok || bad "a waiver for another app never applies"
waiver "$(echo "${W/APPNAME/blocked}" | sed 's/2027-01-01/2026-11-01/')"
FLEET_SWEEP_TESTING=0 FLEET_SWEEP_TEST_TODAY=2026-10-31 python3 "$SWEEP" "$T/fleet.json" --waivers "$T/w.json" >/dev/null 2>&1
[ $? = 2 ] && ok || bad "the clock cannot be moved outside the test suite"

# Inputs are validated before any guard runs (Codex findings 3 and 11).
python3 -c "import json;print(json.dumps({'apps':[{'name':'A','path':'$T/clean'},{'name':'A','path':'$T/blocked'}]}))" > "$T/fleet.json"
[ "$(run)" = 1 ] && has "must be unique" && ok || bad "duplicate app names are refused"
printf '{"apps":[null]}' > "$T/fleet.json"; [ "$(run)" = 1 ] && has "not an object" && ok || bad "null app is an input error"
fleet clean; printf '{"waivers":[null]}' > "$T/w.json"
[ "$(run --waivers "$T/w.json")" = 1 ] && ok || bad "null waiver is an input error"
printf '{bad' > "$T/fleet.json"; [ "$(run)" = 1 ] && has "not valid JSON" && ok || bad "malformed fleet file exits 1"
printf '{"apps": []}' > "$T/fleet.json"; [ "$(run)" = 1 ] && has "lists no apps" && ok || bad "empty fleet exits 1"
[ "$(python3 "$SWEEP" "$T/nope.json" >/dev/null 2>&1; echo $?)" = 1 ] && ok || bad "missing fleet file exits 1"
FLEETDIR="$T" python3 -c 'import json;print(json.dumps({"apps":[{"name":"clean","path":"$FLEETDIR/clean","readiness":{"a":True}}]}))' > "$T/fleet.json"
[ "$(FLEETDIR="$T" run)" = 0 ] && ok || bad "env var in path expands"

# Code-scanning export (Codex finding 10).
mkdir -p "$T/b2"; cp "$T/blocked/"* "$T/b2/"; fleet blocked b2 exit1
waiver "${W/APPNAME/b2}"
run --waivers "$T/w.json" --json "$T/r.json" --scanning-export "$T/s.sarif" >/dev/null
python3 - "$T" <<'EOF' && ok || bad "export keeps app identity, waived findings and failed runs"
import json, sys
t = sys.argv[1]
s = json.load(open(f"{t}/s.sarif")); r = json.load(open(f"{t}/r.json"))
run = s["runs"][0]
assert r["verdict"] == "BLOCKED" and len(r["apps"]) == 3
uris = sorted(x["locations"][0]["physicalLocation"]["artifactLocation"]["uri"] for x in run["results"])
assert "blocked/ios/App/Info.plist" in uris and "b2/ios/App/Info.plist" in uris, uris
assert sum(1 for x in run["results"] if x.get("suppressions")) == 1
assert run["invocations"][0]["executionSuccessful"] is False
assert any("exit1 was not checked" in n["message"]["text"] for n in run["invocations"][0]["toolExecutionNotifications"])
EOF

# Real guard, end to end. An empty folder must never be READY.
mkdir -p "$T/empty"; python3 -c "import json;print(json.dumps({'apps':[{'name':'empty','path':'$T/empty','readiness':{'a':True}}]}))" > "$T/fleet.json"
FLEET_SWEEP_GUARD="$HERE/../agent-os/hooks/app-store-compliance-guard.sh" python3 "$SWEEP" "$T/fleet.json" > "$T/out.txt" 2>&1; rc=$?
[ "$rc" = 1 ] && has "NOT_CHECKED" && ok || bad "real guard on an empty folder is NOT_CHECKED (rc=$rc)"

echo "fleet-sweep-test. $pass passed, $fail failed"
exit "$fail"
