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

echo ""
echo "monitor-test: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
