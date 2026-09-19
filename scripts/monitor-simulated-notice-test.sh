#!/usr/bin/env bash
# Pins the sample-data notice across the four policy monitors, offline.
# A report built from sample announcements must say so; a live report must carry no samples.

set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

python3 - <<'PY'
import importlib.util, io, os, sys, tempfile, contextlib

MONITORS = {
    # name: (fallback_on_empty_live, live item text, or None when the monitor has no live feed)
    "monitor-ai-policy": (False, "Generative AI and large language model app review update"),
    "monitor-android": (True, "Google Play target API level and Play Billing Library update"),
    "monitor-security": (True, None),  # Android security bulletins publish no RSS feed
    "monitor-privacy": (True, "Privacy manifest and App Tracking Transparency requirement"),
}
LIVE_ITEM = lambda text: {
    "id": "LIVE-TEST-ITEM", "title": text, "description": text,
    "link": "https://developer.apple.com/news/", "pubDate": "Mon, 14 Sep 2026 10:00:00 GMT",
}
NOTICE = "Simulated output, not live announcements."
passed = failed = 0

def check(cond, label):
    global passed, failed
    if cond:
        passed += 1; print(f"PASS  {label}")
    else:
        failed += 1; print(f"FAIL  {label}")

def run(name, argv, feed):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), f"scripts/{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.parse_rss_feed = lambda url: [dict(i) for i in feed]
    with tempfile.TemporaryDirectory() as d:
        docs, pr = os.path.join(d, "docs.md"), os.path.join(d, "pr.md")
        sys.argv = [name] + argv + ["--dir", d, "--output-docs", docs, "--pr-output", pr]
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            try:
                mod.main()
            except SystemExit:
                pass
        text = open(docs).read() if os.path.exists(docs) else ""
        draft = open(pr).read() if os.path.exists(pr) else ""
    run.draft = draft
    return mod, text

for name, (falls_back, live_text) in MONITORS.items():
    mod, text = run(name, [], [])
    check(len(text) > 200, f"{name}: default run writes a report")
    check(text.count(NOTICE) == 1, f"{name}: default run writes the notice once")
    check(run.draft.lstrip().startswith("> **" + NOTICE), f"{name}: default run PR draft opens with the notice")
    lines = text.splitlines()
    check(bool(lines) and "MONITOR_START" in lines[0] and any(NOTICE in l for l in lines[1:4]),
          f"{name}: notice sits right after the START marker")
    headings = [l for l in text.splitlines() if l.startswith("### Tasks for")]
    check(len(headings) == len(set(headings)), f"{name}: no duplicate task headings")

    mod, text = run(name, ["--mock", "inline"], [])
    check(NOTICE in text, f"{name}: --mock inline writes the notice")

    if live_text is None:
        mod, text = run(name, ["--live"], [LIVE_ITEM("unused")])
        check(NOTICE in text, f"{name}: has no live feed, so --live output says it is sample data")
    else:
        mod, text = run(name, ["--live"], [LIVE_ITEM(live_text)])
        mock_titles = [a["title"] for a in getattr(mod, "MOCK_ANNOUNCEMENTS", [])]
        check(live_text in text, f"{name}: --live report contains the live feed item")
        check(NOTICE not in text, f"{name}: --live with feed items writes no notice")
        check(NOTICE not in run.draft, f"{name}: --live PR draft carries no notice")
        check(not any(t in text for t in mock_titles), f"{name}: --live output contains no sample announcements")

    mod, text = run(name, ["--live"], [])
    if falls_back:
        check(NOTICE in text, f"{name}: --live with an empty feed falls back and says so")
    else:
        check(NOTICE not in text, f"{name}: --live with an empty feed uses no samples")

print(f"Simulated notice test suite: {passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
PY
