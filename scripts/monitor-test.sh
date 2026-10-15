#!/usr/bin/env bash
# Test suite for monitor.py
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
MONITOR="python3 $HERE/monitor.py"
PASS=0; FAIL=0
ok(){ PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad(){ FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

# 1. Verification of help output
OUT="$($MONITOR --help 2>&1)"
echo "$OUT" | grep -q "Monitor and track updates to Apple developer requirements" && ok "help output contains usage description" || bad "help output"

# 2. Simulation of a single track
OUT="$($MONITOR --simulate "Privacy Manifests" 2>&1)"
echo "$OUT" | grep -q "TRACK UPDATE: \[Privacy Manifests\]" && ok "simulating a track successfully matches and prints track header" || bad "simulate single track"
echo "$OUT" | grep -q "Proposed Pull Request Details:" && ok "simulating a track generates proposed pull request information" || bad "simulate PR generation"

# 3. Simulate all tracks to ensure no crashes
OUT="$($MONITOR --simulate "all" 2>&1)"
# Check some known tracks in the simulation
echo "$OUT" | grep -q "TRACK UPDATE: \[In-App Purchase policies\]" && \
echo "$OUT" | grep -q "TRACK UPDATE: \[DMA compliance changes\]" && \
echo "$OUT" | grep -q "TRACK UPDATE: \[Swift requirements\]" && \
ok "simulating all 25 tracks runs successfully with no crashes and outputs matches" || bad "simulate all tracks"
N_TRACKS="$($MONITOR --simulate "all" 2>&1 | grep -o 'TRACK UPDATE: \[[^]]*\]' | sort -u | wc -l | tr -d ' ')"
[ "$N_TRACKS" = "25" ] && ok "simulating all reaches every one of the 25 tracks" || bad "simulating all reaches every one of the 25 tracks (got $N_TRACKS)"

# 4. JSON output format verification
JSON_OUT="$($MONITOR --simulate "Required Reason APIs" --json 2>&1)"
# Validate if it is well-formed JSON
echo "$JSON_OUT" | python3 -c "import sys, json; data = json.load(sys.stdin); assert len(data) > 0; assert data[0]['track'] == 'Required Reason APIs'" 2>/dev/null && ok "json output format is valid and contains matched track" || bad "json output"

# 5. Repository scanning verification
T=$(mktemp -d)
# Create a dummy project structure with a signature matching Swift requirements
mkdir -p "$T/Sources"
printf "import SwiftUI\nlet swiftVersion = 6.0\nTask { @MainActor in print(\"async-await\") }" > "$T/Sources/App.swift"

# Run monitor pointing to the temp directory simulating Swift requirements
OUT_SCAN="$($MONITOR --project "$T" --simulate "Swift requirements" 2>&1)"
echo "$OUT_SCAN" | grep -q "Sources/App.swift" && ok "repo scanner correctly identifies affected source file" || bad "repo scanner affected file"

# Clean up
rm -rf "$T"

# 5. The proposed pull request carries sections numbered 1 to 15, in order
echo "$JSON_OUT" | python3 -c "
import sys, json, re
body = json.load(sys.stdin)[0]['proposed_pull_request']['description']
nums = [int(n) for n in re.findall(r'^## (\d+)\. ', body, re.M)]
assert nums == list(range(1, 16)), nums
" 2>/dev/null && ok "proposed pull request has sections 1 to 15 in order" || bad "numbered PR sections"

# 6. Mock announcements fallback or manual trigger
OUT_MOCK="$($MONITOR --mock 2>&1)"
echo "$OUT_MOCK" | grep -q "TRACK UPDATE: \[Privacy Manifests\]" && ok "mock announcements fallback runs and matches tracks" || bad "mock announcements"

# A long live report is cut to a readable first screen. --full prints every item.
T="$(mktemp -d)"
python3 -c 'import json,sys; json.dump([{"title":"Privacy manifest update %d" % i,"description":"Changes to privacy manifests and required reason APIs.","pubDate":"Mon, 01 Sep 2026 10:00:00 PDT","link":"https://mock.invalid/n/%d" % i} for i in range(40)], open(sys.argv[1],"w"))' "$T/news.json"
OUT="$($MONITOR --project "$T" --news-file "$T/news.json" 2>&1)"
N="$(echo "$OUT" | grep -c 'TRACK UPDATE')"
[ "$N" -eq 10 ] && echo "$OUT" | grep -q "Showing 10 of" && echo "$OUT" | grep -q "\-\-full" && ok "a long report shows 10 items and names --full" || bad "a long report shows 10 items and names --full (got $N)"
echo "$OUT" | grep -q "By track" && ok "a long report opens with a count per track" || bad "a long report opens with a count per track"
N="$($MONITOR --project "$T" --news-file "$T/news.json" --full 2>&1 | grep -c 'TRACK UPDATE')"
[ "$N" -ge 40 ] && ok "--full prints every item" || bad "--full prints every item (got $N)"
N="$($MONITOR --project "$T" --news-file "$T/news.json" --json 2>/dev/null | python3 -c 'import json,sys; print(len(json.load(sys.stdin)))')"
[ "$N" -ge 40 ] && ok "--json is never cut" || bad "--json is never cut (got $N)"
# A failed live fetch must say the items shown are samples, on stderr so --json stays parseable.
ERR="$(APPLE_NEWS_RSS_URL="http://127.0.0.1:9/none.rss" $MONITOR --project "$T" --json 2>&1 >/dev/null)"
echo "$ERR" | grep -q "sample announcements" && ok "a failed live fetch says the items are samples" || bad "a failed live fetch says the items are samples"
APPLE_NEWS_RSS_URL="http://127.0.0.1:9/none.rss" $MONITOR --project "$T" --json 2>/dev/null | python3 -c 'import json,sys; json.load(sys.stdin)' && ok "--json stays valid when the fetch fails" || bad "--json stays valid when the fetch fails"
rm -rf "$T"

# Atom text fields are plain text unless type says html or xhtml (RFC 4287 3.1.1). RSS stays HTML.
python3 - "$HERE" <<'PY' && ok "Atom plain-text fields keep angle brackets, html and xhtml are stripped, RSS stays HTML" || bad "Atom plain-text fields keep angle brackets, html and xhtml are stripped, RSS stays HTML"
import importlib.util, os, sys, tempfile, pathlib
d = sys.argv[1]
spec = importlib.util.spec_from_file_location("ai", os.path.join(d, "monitor-ai-policy.py"))
ai = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ai)
atom = """<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom">
<entry><title type="text">Policy changes for &lt;llm&gt; integrations</title><summary>Plain &lt;b&gt;kept&lt;/b&gt;</summary></entry>
<entry><title>No type &lt;llm&gt; here</title><summary type="html">&lt;p&gt;Rich &lt;a href="https://x/llm"&gt;body&lt;/a&gt;&lt;/p&gt;</summary></entry>
<entry><title type="xhtml"><div xmlns="http://www.w3.org/1999/xhtml">Xhtml <b>title</b></div></title><content type="xhtml"><div xmlns="http://www.w3.org/1999/xhtml"><p>Inner <a href="https://x/att">text</a></p></div></content></entry>
</feed>"""
rss = """<?xml version="1.0"?><rss><channel><item><title>T</title><description>&lt;p&gt;HTML &lt;a href="https://x/llm"&gt;body&lt;/a&gt;&lt;/p&gt;</description></item></channel></rss>"""
tmp = tempfile.mkdtemp()
fa = pathlib.Path(tmp, "a.xml"); fa.write_text(atom)
fr = pathlib.Path(tmp, "r.xml"); fr.write_text(rss)
a = ai.parse_rss_feed(fa.as_uri())
assert [x["title"] for x in a] == ["Policy changes for <llm> integrations", "No type <llm> here", "Xhtml title"], a
assert [x["description"] for x in a] == ["Plain <b>kept</b>", "Rich body", "Inner text"], a
r = ai.parse_rss_feed(fr.as_uri())
assert r[0]["description"] == "HTML body", r
assert ai.analyze_announcements([a[0]], ["llm"]), "plain-text <llm> no longer matches"
edge = """<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom">
<entry><title>A</title><content type="text/html">&lt;a href="https://example.org/llm/"&gt;Read&lt;/a&gt;</content></entry>
<entry><title>B</title><content type="application/xhtml+xml"><div xmlns="http://www.w3.org/1999/xhtml"><h2>Install</h2><p>macOS updates</p></div></content></entry>
<entry><title>C</title><summary>Keep the llm summary</summary><content src="https://example.org/x"/></entry>
<entry><title>D</title><content type="text/plain">Plain &lt;llm&gt; kept</content></entry>
</feed>"""
fe = pathlib.Path(tmp, "e.xml"); fe.write_text(edge)
e = ai.parse_rss_feed(fe.as_uri())
assert e[0]["description"] == "Read", e
assert e[1]["description"] == "Install macOS updates", e
assert "llm summary" in e[2]["description"], e
assert e[3]["description"] == "Plain <llm> kept", e
inl = '<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>I</title><content type="xhtml"><div xmlns="http://www.w3.org/1999/xhtml"><p>New <span>LL</span>M policy</p><ul><li>One</li><li>Two</li></ul></div></content></entry></feed>'
fi = pathlib.Path(tmp, "i.xml"); fi.write_text(inl)
i = ai.parse_rss_feed(fi.as_uri())
assert i[0]["description"] == "New LLM policy One Two", i
fs = '<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>F</title><content type="xhtml"><div xmlns="http://www.w3.org/1999/xhtml"><fieldset>Install</fieldset><fieldset>macOS updates</fieldset><custom-x>Fill</custom-x><custom-y>Mac</custom-y></div></content></entry></feed>'
ff = pathlib.Path(tmp, "f.xml"); ff.write_text(fs)
f = ai.parse_rss_feed(ff.as_uri())
assert f[0]["description"] == "Install macOS updates Fill Mac", f
assert not ai.analyze_announcements(f, ["llm"]), "an unlisted block element joined two words"
X = "http://www.w3.org/1999/xhtml"
sw = ('<feed xmlns="http://www.w3.org/2005/Atom" xmlns:e="urn:ext">'
      '<entry><title>S</title><content type="xhtml"><div xmlns="' + X + '"><script>generative AI</script><style>/* llm */</style><p>Pricing changes.</p></div></content></entry>'
      '<entry><title>Real</title><e:title>generative AI</e:title><e:summary>generative AI</e:summary><summary>Pricing changes.</summary>'
      '<e:entry><title>generative AI fake</title></e:entry></entry>'
      '<entry><title>M</title><content type="text/html; charset=utf-8">&lt;a href="/llm/"&gt;Read&lt;/a&gt;</content></entry>'
      '<entry><title>B</title><content type="application/octet-stream">aiAA</content></entry>'
      '</feed>')
fw = pathlib.Path(tmp, "w.xml"); fw.write_text(sw)
w = ai.parse_rss_feed(fw.as_uri())
assert [x["title"] for x in w] == ["S", "Real", "M", "B"], w
assert [x["description"] for x in w] == ["Pricing changes.", "Pricing changes.", "Read", ""], w
assert not ai.analyze_announcements(w, ["generative ai", "llm", "ai"]), "script, a foreign element, MIME parameters or binary content matched"
rt = '<rss><channel><item><title>New &lt;generative AI&gt; rules</title><description>&lt;p&gt;artificial&lt;em&gt;intelligence&lt;/em&gt;&lt;/p&gt;</description></item></channel></rss>'
fx = pathlib.Path(tmp, "x.xml"); fx.write_text(rt)
x = ai.parse_rss_feed(fx.as_uri())
assert x[0]["title"] == "New <generative AI> rules", x
amp = '<rss><channel><item><title>Tax &amp;amp; price updates</title><description>x</description></item></channel></rss>'
fq = pathlib.Path(tmp, "q.xml"); fq.write_text(amp)
assert ai.parse_rss_feed(fq.as_uri())[0]["title"] == "Tax & price updates"
spec2 = importlib.util.spec_from_file_location("mon2", os.path.join(d, "monitor.py"))
mon = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(mon)
assert "In-App Purchase policies" in mon.match_announcement_to_tracks({"title": "Policy changes for <StoreKit>", "description": ""}), "an RSS title lost its literal text"
assert x[0]["description"] == "artificialintelligence", x
for fn in (ai.clean_html_text,):
    assert fn("<p>Hello</p><p>World</p>") == "Hello World", fn
assert ai.analyze_announcements(i, ["llm"]), "an inline element split a keyword"
assert not ai.analyze_announcements([e[0]], ["llm"]) and not ai.analyze_announcements([e[1]], ["llm"]), "markup or joined blocks made a false llm match"
PY

# A feed full of unmatched angle brackets must not make tag stripping quadratic.
python3 - "$HERE" <<'PY' && ok "HTML stripping stays linear on unmatched angle brackets" || bad "HTML stripping stays linear on unmatched angle brackets"
import importlib.util, os, sys, time
d = sys.argv[1]
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m
mon = load("mon", os.path.join(d, "monitor.py"))
ai = load("ai", os.path.join(d, "monitor-ai-policy.py"))
for fn in (mon.strip_html, ai.clean_html_text):
    t = time.time()
    fn("<" * 200000)
    assert time.time() - t < 1.0, fn.__name__
    assert fn("<p>a</p> <b>b</b>") == "a b"
    assert fn('<a href="https://developer.example/llm/att" title="x < y">Read notes</a>') == "Read notes", fn.__name__
    t = time.time()
    fn('<a "' * 50000)
    assert time.time() - t < 1.0, fn.__name__
    assert fn("<!-- \" app tracking transparency -->Normal update") == "Normal update", fn.__name__
    assert fn("<!-- Don't publish -->Privacy manifests: developers' guide > old approach") == "Privacy manifests: developers' guide > old approach", fn.__name__
    t = time.time()
    fn("<!--" * 100000)
    assert time.time() - t < 1.0, fn.__name__
    assert fn('<a title="<!--">App Review Guidelines changed</a>') == "App Review Guidelines changed", fn.__name__
    for ending in ("<!-->", "<!--->", "<!--x--!>"):
        assert fn(ending + "Privacy manifests") == "Privacy manifests", (fn.__name__, ending)
    assert fn("Kept <!-- never closed") == "Kept", fn.__name__
    for hostile in (('<a "' + "<!--") * 50000, ("<!--x-->" + '<b "') * 40000, ("<a '" + '"') * 60000):
        t = time.time()
        fn(hostile)
        assert time.time() - t < 1.0, (fn.__name__, hostile[:12])
    for markup in ("<svg><text><![CDATA[Privacy manifests]]></text></svg>", "<textarea><!--</textarea>Privacy manifests", '<!x ">Privacy manifests">', "<TITLE>Privacy manifests</title>", "<![CDATA[<b>Privacy manifests</b>]]>"):
        assert "Privacy manifests" in fn(markup), (fn.__name__, markup, fn(markup))
    assert "<b>" not in fn("<![CDATA[<b>Privacy manifests</b>]]>"), fn.__name__
    assert "Privacy" not in fn('<textarea-x><a href="Privacy manifests">Read notes</a></textarea-x>'), fn.__name__
    assert "Privacy manifests" in fn("<textarea-x>Privacy <b>manifests</b></textarea-x>"), fn.__name__
    assert fn("<textarea>Privacy</textarea/><!-- hidden -->Next") == "Privacy Next", fn.__name__
    assert "Privacy manifests" in fn("<textarea>Kept</textarea" + chr(160) + "><!-- Privacy manifests -->Next"), fn.__name__
    assert "Privacy" not in fn("<t" + chr(305) + "tle><a href=\"Privacy manifests\">Read notes</a></t" + chr(305) + "tle>"), fn.__name__
    for hostile in ("<textarea>" * 50000, "<![CDATA[" * 50000, "<!x" * 100000, "<title a='" * 40000, "<![CDATA[<!--" * 40000):
        t = time.time()
        fn(hostile)
        assert time.time() - t < 1.0, (fn.__name__, hostile[:12])
PY
# Issue 833. Keywords match whole words on the visible text, not substrings of HTML.
T="$(mktemp -d)"
python3 - "$T/news.json" <<'PY'
import json, sys
items = [
    ("Display and platform updates", "<p>New <a href=\"https://developer.example/design/\">display</a> sizes on all platforms and marketplaces. Translations improved.</p>"),
    ("Retail-related pattern changes", "<p>Pay attention to the new retail-related pattern for administrators.</p>"),
    ("Updated PLA now available", "<p>The updated PLA is ready to review.</p>"),
    ("SLA update", "<p>Review the new SLA.</p>"),
    ("Updated review guidelines", "<p>The App Review Guidelines have changed.</p>"),
    ("Patched vulnerabilities", "<p>Several vulnerabilities are fixed in this release.</p>"),
    ("In-app purchasing changes", "<p>New rules for in-app purchasing.</p>"),
    ("Tracking API", "<p>ATTrackingManager authorization changes.</p>"),
    ("Camera key", "<p>Update NSCameraUsageDescription strings.</p>"),
    ("Location API", "<p>CLLocationManager authorization changes.</p>"),
    ("StoreKit2 update", "<p>New StoreKit2 APIs.</p>"),
    ("WCAG2.2 alignment", "<p>Apps should meet WCAG2.2.</p>"),
]
json.dump([{"title": t, "description": d, "pubDate": "Mon, 01 Sep 2026 10:00:00 PDT", "link": "https://mock.invalid/833/%d" % i}
           for i, (t, d) in enumerate(items)], open(sys.argv[1], "w"))
PY
$MONITOR --project "$T" --news-file "$T/news.json" --json 2>/dev/null | python3 -c '
import json, sys
by = {}
for i in json.load(sys.stdin):
    by.setdefault(i["announcement_title"], set()).add(i["track"])
lic = "Apple Developer Program License Agreement"
assert lic not in by.get("Display and platform updates", set()), by
assert not by.get("Retail-related pattern changes"), by
assert lic in by.get("Updated PLA now available", set()), by
assert lic in by.get("SLA update", set()), by
assert "App Store Review Guidelines" in by.get("Updated review guidelines", set()), by
assert "Security updates" in by.get("Patched vulnerabilities", set()), by
assert "In-App Purchase policies" in by.get("In-app purchasing changes", set()), by
assert "App Tracking Transparency" in by.get("Tracking API", set()), by
assert "Camera and microphone permissions" in by.get("Camera key", set()), by
assert "Location permissions" in by.get("Location API", set()), by
assert "In-App Purchase policies" in by.get("StoreKit2 update", set()), by
assert "Accessibility requirements" in by.get("WCAG2.2 alignment", set()), by
' && ok "keywords match whole words on stripped text (issue 833)" || bad "keywords match whole words on stripped text (issue 833)"
rm -rf "$T"

echo ""
echo "monitor-test: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
