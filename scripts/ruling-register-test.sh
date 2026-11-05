#!/usr/bin/env bash
# Gauntlet for ruling-register.py and its link into fleet-sweep.py.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
RR="$HERE/ruling-register.py"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
pass=0; fail=0
ok() { pass=$((pass+1)); }
bad() { fail=$((fail+1)); echo "FAIL $1"; }

# Validator and blocking logic, driven in-process with a fixed date.
python3 - "$HERE" <<'EOF' > "$T/py.txt" 2>&1
import copy, datetime as dt, importlib.util, json, sys
here = sys.argv[1]
spec = importlib.util.spec_from_file_location("rr", f"{here}/ruling-register.py")
rr = importlib.util.module_from_spec(spec); spec.loader.exec_module(rr)
real = json.load(open(f"{here}/../data/ruling-register.json"))
pids = rr.pattern_ids()
results = []
def check(name, cond):
    results.append(name if cond else f"FAIL {name}")

check("real register is valid", rr.validate(real, pids) == [])
base = {"id": "RR-T", "revision": 1, "title": "t", "jurisdiction": "DE", "store": None, "instrument": "i", "authority": "a",
        "standing": "in_force", "takes_effect": None, "features": [], "proof": "automated",
        "proof_items": [{"id": "auto-1", "what": "w", "how": "automated"}], "check": "c",
        "sources": [{"url": "https://example.org/x", "checked_on": "2026-11-05", "quote": "q", "supports": ["obligation", "date"]}]}
def doc(*reqs): return {"register_version": "1.0.0", "requirements": list(reqs)}
def errs(**change):
    r = copy.deepcopy(base); r.update(change); return rr.validate(doc(r), pids)
check("clean entry passes", errs() == [])
check("duplicate id refused", rr.validate(doc(base, base), pids) != [])
check("bad id refused", errs(id="X-1") != [])
check("unknown standing refused", errs(standing="maybe") != [])
check("in_force_later needs a date", errs(standing="in_force_later") != [])
check("bad date refused", errs(takes_effect="soon") != [])
check("unknown feature refused", errs(features=["gaming"]) != [])
check("bad store refused", errs(store="huawei") != [])
check("mixed needs both kinds", errs(proof="mixed") != [])
check("owner_attested with an automated item refused", errs(proof="owner_attested") != [])
check("no proof items refused", errs(proof_items=[]) != [])
check("no sources refused", errs(sources=[]) != [])
check("http source refused", errs(sources=[{"url": "http://x", "checked_on": "2026-11-05", "quote": "q", "supports": ["obligation"]}]) != [])
check("quote and unverified together refused", errs(sources=[{"url": "https://x", "checked_on": "2026-11-05", "quote": "q", "unverified": "u", "supports": ["obligation"]}]) != [])
check("neither quote nor unverified refused", errs(sources=[{"url": "https://x", "checked_on": "2026-11-05", "supports": ["obligation"]}]) != [])
check("missing checked_on refused", errs(sources=[{"url": "https://x", "quote": "q", "supports": ["obligation"]}]) != [])
check("unknown pattern id refused", errs(pattern_ids=["NOPE-1"]) != [])
check("missing check refused", errs(check="") != [])
check("missing revision refused", errs(revision=None) != [])
check("proof item without id refused", errs(proof_items=[{"what": "w", "how": "automated"}]) != [])
check("duplicate proof item ids refused", errs(proof_items=[{"id": "a", "what": "w", "how": "automated"}, {"id": "a", "what": "x", "how": "automated"}]) != [])
check("source without supports refused", errs(sources=[{"url": "https://x", "checked_on": "2026-11-05", "quote": "q"}]) != [])
check("non-object entry refused", rr.validate(doc("x"), pids) != [])
check("bad version refused", rr.validate({"register_version": "one", "requirements": [base]}, pids) != [])

d = dt.date(2026, 11, 5)
def blocks(**change):
    r = copy.deepcopy(base); r.update(change); return rr.blocking(r, d)
check("in force blocks", blocks())
check("store policy blocks", blocks(standing="store_policy"))
check("proposed never blocks", not blocks(standing="proposed", takes_effect="2020-01-01"))
check("guidance never blocks", not blocks(standing="guidance"))
check("in force later blocks once its date passes", blocks(standing="in_force_later", takes_effect="2026-11-05"))
check("in force later waits for its date", not blocks(standing="in_force_later", takes_effect="2026-11-06"))
check("in force with a future date waits", not blocks(takes_effect="2027-01-01"))
check("an unverified source never blocks", not blocks(sources=[{"url": "https://x", "checked_on": "2026-11-05", "unverified": "blocked", "supports": ["obligation"]}]))
check("a quote on the obligation alone does not verify a start date", not blocks(takes_effect="2020-01-01", sources=[{"url": "https://x", "checked_on": "2026-11-05", "quote": "q", "supports": ["obligation"]}, {"url": "https://y", "checked_on": "2026-11-05", "unverified": "u", "supports": ["date"]}]))
check("quotes on obligation and date together verify it", blocks(takes_effect="2020-01-01", sources=[{"url": "https://x", "checked_on": "2026-11-05", "quote": "q", "supports": ["obligation"]}, {"url": "https://y", "checked_on": "2026-11-05", "quote": "d", "supports": ["date"]}]))
check("the real AU minimum-age rule does not block on its unverified date",
      not any(r["blocks_release"] for r in rr.due(real, {"AU"}, {"apple"}, {"social"}, d) if r["id"] == "RR-AU-SOCIAL-MIN-AGE"))

eu = copy.deepcopy(base); eu["jurisdiction"] = "EU"
check("an EU country matches an EU rule", rr.applies(eu, {"DE"}, {"apple"}, set()))
check("a non-EU country does not", not rr.applies(eu, {"US"}, {"apple"}, set()))
g = copy.deepcopy(base); g["jurisdiction"] = "GLOBAL"
check("GLOBAL matches everywhere", rr.applies(g, {"BR"}, set(), set()))
s = copy.deepcopy(base); s["store"] = "google"
check("a store rule skips the other store", not rr.applies(s, {"DE"}, {"apple"}, set()))
f = copy.deepcopy(base); f["features"] = ["crypto"]
check("a feature rule skips apps without it", not rr.applies(f, {"DE"}, {"apple"}, {"social"}))
check("a feature rule applies with it", rr.applies(f, {"DE"}, {"apple"}, {"crypto", "social"}))
check("a rule with no features applies to every app", rr.applies(base, {"DE"}, {"apple"}, set()))
check("the real EU withdrawal rule never blocks while unverified",
      not any(r["blocks_release"] for r in rr.due(real, {"DE"}, {"apple"}, {"subscriptions"}, d) if r["id"] == "RR-EU-WITHDRAWAL-FUNCTION"))
check("the Children's Code is proposed, so it never blocks",
      not any(r["blocks_release"] for r in rr.due(real, {"AU"}, {"apple"}, {"children"}, dt.date(2027, 6, 1)) if r["id"] == "RR-AU-CHILDREN-PRIVACY-CODE"))
print("\n".join(results))
EOF
while read -r line; do case "$line" in FAIL*) bad "${line#FAIL }" ;; "") ;; Traceback*|*Error*) bad "python harness. $line" ;; *) ok ;; esac; done < "$T/py.txt"
# A harness that dies early prints few lines, which must never read as green.
[ "$(grep -c . "$T/py.txt")" -eq 45 ] && ok || bad "python harness expected 45 checks, ran $(grep -c . "$T/py.txt") checks"

# Command line.
python3 "$RR" validate > "$T/out.txt" 2>&1; [ $? = 0 ] && grep -q "OK" "$T/out.txt" && ok || bad "validate exits 0 on the real register"
python3 "$RR" --register "$T/nope.json" validate >/dev/null 2>&1; [ $? = 1 ] && ok || bad "a missing register exits 1"
printf '{"register_version":"1.0.0","requirements":[{"id":"bad"}]}' > "$T/bad.json"
python3 "$RR" --register "$T/bad.json" validate >/dev/null 2>&1; [ $? = 1 ] && ok || bad "an invalid register exits 1"
python3 "$RR" due --regions AU --features gaming >/dev/null 2>&1; [ $? = 1 ] && ok || bad "unknown feature exits 1"
python3 "$RR" due --regions AU --stores apple --features social --json > "$T/due.json" && python3 -c "
import json,sys; rows=json.load(open('$T/due.json')); ids={r['id'] for r in rows}
assert 'RR-AU-SOCIAL-MIN-AGE' in ids and 'RR-PLAY-LENDING-IN' not in ids" && ok || bad "due returns the matching rules as JSON"
python3 "$RR" export --out-dir "$T/exp" >/dev/null && python3 -c "
import json,glob; f=glob.glob('$T/exp/ruling-register-v*.json'); d=json.load(open(f[0]))
assert d['source_commit'] and d['exported_on'] and len(d['requirements'])>=14" && ok || bad "export is versioned and commit-stamped"

# Fleet Sweep picks up the register.
cat > "$T/guard.sh" <<'EOF2'
#!/usr/bin/env bash
printf 'Summary. critical=0 high=0 medium=0\nCoverage. complete ios=1 android=1 web=0\nCLEAR.\n'
EOF2
mkdir -p "$T/app"
export FLEET_SWEEP_GUARD="$T/guard.sh" FLEET_SWEEP_TESTING=1 FLEET_SWEEP_TEST_TODAY=2026-11-05
fleet() { python3 -c "import json,sys;print(json.dumps({'apps':[dict({'name':'app','path':'$T/app','platforms':['ios'],'regions':['US'],'features':[],'readiness':{'a':True}},**json.loads(sys.argv[1]))]}))" "$1" > "$T/fleet.json"; }
sweep() { python3 "$HERE/fleet-sweep.py" "$T/fleet.json" "$@" > "$T/out.txt" 2>&1; echo $?; }
has() { grep -q -- "$1" "$T/out.txt"; }
att() {  # rule-id, then python dict overrides
  python3 - "$1" "${2:-{\}}" <<'EOF2'
import json, sys
a = {"attested_by": "Mirza", "attested_on": "2026-10-01", "evidence": "see docs/review.md", "outcome": "compliant",
     "revision": 1, "covers": ["owner-1"], "regions": ["US"]}
a.update(json.loads(sys.argv[2]))
print(json.dumps({sys.argv[1]: a}))
EOF2
}
MED='"regions":["US"],"features":["medical"]'
fleet "{$MED}"
[ "$(sweep)" = 2 ] && has "\[REGISTER\] RR-US-FDA-DEVICE-SOFTWARE needs your attestation, which is missing" && ok || bad "an unattested in-force rule blocks the release"
fleet "{$MED,\"attestations\":$(att RR-US-FDA-DEVICE-SOFTWARE)}"
[ "$(sweep)" = 0 ] && ok || bad "a complete compliant attestation clears the rule"
fleet "{$MED,\"attestations\":$(att RR-US-FDA-DEVICE-SOFTWARE '{"outcome":"not_compliant"}')}"
[ "$(sweep)" = 2 ] && has "only compliant clears" && ok || bad "a negative outcome never clears a rule"
fleet "{$MED,\"attestations\":$(att RR-US-FDA-DEVICE-SOFTWARE '{"outcome":null,"approved":false}')}"
[ "$(sweep)" = 2 ] && has "missing outcome" && ok || bad "an attestation with no outcome is refused"
fleet "{$MED,\"attestations\":$(att RR-US-FDA-DEVICE-SOFTWARE '{"revision":0}')}"
[ "$(sweep)" = 2 ] && has "revision" && ok || bad "an attestation for an old revision is refused"
fleet "{$MED,\"attestations\":$(att RR-US-FDA-DEVICE-SOFTWARE '{"evidence":""}')}"
[ "$(sweep)" = 2 ] && has "missing evidence" && ok || bad "an attestation without evidence is refused"
fleet "{$MED,\"attestations\":$(att RR-US-FDA-DEVICE-SOFTWARE '{"attested_on":"2027-01-01"}')}"
[ "$(sweep)" = 2 ] && has "in the future" && ok || bad "a future-dated attestation is refused"
fleet "{$MED,\"attestations\":$(att RR-US-FDA-DEVICE-SOFTWARE '{"attested_on":"2025-01-01"}')}"
[ "$(sweep)" = 2 ] && has "more than a year old" && ok || bad "a stale attestation is refused"
VN='"regions":["VN"],"features":["social"]'
fleet "{$VN,\"attestations\":$(att RR-VN-SOCIAL-AUTH '{"regions":["VN"]}')}"
[ "$(sweep)" = 2 ] && has "does not cover proof items auto-1" && ok || bad "a mixed rule needs its automated check result too"
fleet "{$VN,\"attestations\":$(att RR-VN-SOCIAL-AUTH '{"regions":["VN"],"covers":["auto-1","owner-2"]}')}"
[ "$(sweep)" = 0 ] && ok || bad "covering every proof item clears a mixed rule"
CR='"platforms":["android"],"regions":["DE","FR"],"features":["crypto"]'
fleet "{$CR,\"attestations\":$(att RR-PLAY-CRYPTO-EU '{"regions":["DE"]}' | python3 -c "import json,sys;a=json.load(sys.stdin);a.update(json.loads('$(att RR-EU-CRA-REPORTING '{"regions":["DE","FR"]}')'));print(json.dumps(a))")}"
[ "$(sweep)" = 2 ] && has "does not cover FR" && ok || bad "an attestation must cover every country the rule reaches"
fleet '{"regions":["AU"],"features":["social"]}'
[ "$(sweep)" = 3 ] && has "RR-AU-SOCIAL-MIN-AGE applies but its source is unconfirmed" && ok || bad "a rule with an unverified date is flagged, not blocking"
fleet '{"regions":["DE"],"features":["subscriptions"]}'
sweep >/dev/null; has "RR-EU-WITHDRAWAL-FUNCTION applies but its source is unconfirmed" && ok || bad "an unverified rule is flagged"
fleet '{"regions":[" us "],"features":["medical"]}'
[ "$(sweep)" = 2 ] && has "RR-US-FDA-DEVICE-SOFTWARE" && ok || bad "padded lower-case regions are normalised, not dropped"
fleet '{"regions":["USA"],"features":[]}'
[ "$(sweep)" = 1 ] && has "two-letter" && ok || bad "a three-letter region is an input error"
python3 -c "import json;print(json.dumps({'apps':[{'name':'app','path':'$T/app','platforms':['ios'],'features':['medical'],'readiness':{'a':True}}]}))" > "$T/fleet.json"
[ "$(sweep)" = 1 ] && has "must declare regions" && ok || bad "missing regions is refused"
python3 -c "import json;print(json.dumps({'apps':[{'name':'app','path':'$T/app','platforms':['ios'],'regions':['US'],'readiness':{'a':True}}]}))" > "$T/fleet.json"
[ "$(sweep)" = 1 ] && has "must declare features" && ok || bad "missing features is refused"
python3 -c "import json;print(json.dumps({'apps':[{'name':'app','path':'$T/app','regions':['IN'],'features':['lending'],'readiness':{'a':True}}]}))" > "$T/fleet.json"
[ "$(sweep)" = 1 ] && has "must declare platforms" && ok || bad "missing platforms is refused"
fleet '{"regions":["US"],"features":["medical"]}'
[ "$(sweep --no-register)" = 0 ] && ok || bad "--no-register skips the register"
[ "$(sweep --register "$T/bad.json")" = 1 ] && has "ruling register is invalid" && ok || bad "an invalid register stops the sweep"
fleet '{"regions":["US"],"features":["gaming"]}'
[ "$(sweep)" = 1 ] && has "features must be" && ok || bad "an unknown app feature is an input error"
fleet '{"regions":["US"],"features":["social"]}'
[ "$(sweep)" = 0 ] && ok || bad "an app outside every applicable rule stays READY"

echo "ruling-register-test. $pass passed, $fail failed"
exit "$fail"
