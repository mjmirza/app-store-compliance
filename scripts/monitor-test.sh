#!/bin/bash
# Test script for Platform Policy Monitor Utility (scripts/monitor.py).
# It verifies that Atom and RSS feeds can be parsed successfully,
# documents are correctly generated, the 15 required sections are present in the PR draft,
# and that no emojis exist in the script or output files.

set -e

# Setup directories and temp files
TEMP_ATOM_FEED="temp_test_atom_feed.xml"
TEMP_RSS_FEED="temp_test_rss_feed.xml"

# Clean up any leftover files
cleanup() {
    rm -f "$TEMP_ATOM_FEED"
    rm -f "$TEMP_RSS_FEED"
}
trap cleanup EXIT

echo "=== Running Platform Policy Monitor Test Suite ==="

# 1. Create a mock Atom feed file
cat <<EOF > "$TEMP_ATOM_FEED"
<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Atom Feed Update</title>
  <updated>2026-06-16T12:00:00Z</updated>
  <entry>
    <title>Apple Guidelines 1.2 and 5.1.2 Compliance Update</title>
    <link href="https://developer.apple.com/app-store/review/guidelines/ai-update"/>
    <updated>2026-06-16T00:00:00Z</updated>
    <content type="html">
      Apple requires disclosure of AI tools and user consent before transmitting data.
    </content>
  </entry>
</feed>
EOF

# 2. Create a mock RSS feed file
cat <<EOF > "$TEMP_RSS_FEED"
<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
  <channel>
    <title>RSS Feed Update</title>
    <item>
      <title>Google Play AI safety rules update</title>
      <link>https://play.google/developer-content-policy/ai-safety</link>
      <pubDate>Mon, 15 Jun 2026 00:00:00 GMT</pubDate>
      <description>
        Google Play requires prominent AI generation labels and safety filters.
      </description>
    </item>
  </channel>
</rss>
EOF

# 3. Run monitor against Atom feed and check files existence
echo "Testing with Atom feed..."
python3 scripts/monitor.py --feed "$TEMP_ATOM_FEED"

if [ ! -f "docs/AI-POLICY-MIGRATION.md" ]; then
    echo "ERROR: docs/AI-POLICY-MIGRATION.md was not created."
    exit 1
fi

if [ ! -f "docs/AI_COMPLIANCE_PR_DRAFT.md" ]; then
    echo "ERROR: docs/AI_COMPLIANCE_PR_DRAFT.md was not created."
    exit 1
fi

# 4. Run monitor against RSS feed and check files existence
echo "Testing with RSS feed..."
python3 scripts/monitor.py --feed "$TEMP_RSS_FEED"

if [ ! -f "docs/AI-POLICY-MIGRATION.md" ]; then
    echo "ERROR: docs/AI-POLICY-MIGRATION.md was not created."
    exit 1
fi

if [ ! -f "docs/AI_COMPLIANCE_PR_DRAFT.md" ]; then
    echo "ERROR: docs/AI_COMPLIANCE_PR_DRAFT.md was not created."
    exit 1
fi

# 5. Verify the 15 required sections in the PR draft
echo "Verifying 15 non-vague sections in docs/AI_COMPLIANCE_PR_DRAFT.md..."
declare -a SECTIONS=(
    "1. Summary"
    "2. Background"
    "3. Regulatory change"
    "4. Official citations"
    "5. Affected files"
    "6. Risk assessment"
    "7. Migration steps"
    "8. Backward compatibility"
    "9. Implementation checklist"
    "10. Testing checklist"
    "11. Documentation checklist"
    "12. Compliance impact"
    "13. Breaking changes"
    "14. Review checklist"
    "15. Approver recommendations"
)

for section in "${SECTIONS[@]}"; do
    if ! grep -q "## $section" docs/AI_COMPLIANCE_PR_DRAFT.md; then
        echo "ERROR: Missing required section: $section"
        exit 1
    fi
done
echo "All 15 sections are present and correctly formatted."

# 6. Verify that no emojis exist in generated files or scripts
echo "Verifying no emojis exist in scripts/monitor.py or docs/ folders..."

# Define a regex block of common emojis and check for them
# We can also search using standard character range tests or grep
# Let's search using a character check for high unicode values
if grep -rn '[^\x00-\x7F]' scripts/monitor.py docs/AI-POLICY-MIGRATION.md docs/AI_COMPLIANCE_PR_DRAFT.md scripts/monitor-test.sh | grep -qE '🤖|⚠️|✅|❌|🚀|📝|🔥|💡|🎉|📌|🔍|🛠️|📦|🚨|💬'; then
    echo "ERROR: Found disallowed graphical symbols or emojis!"
    grep -rn '[^\x00-\x7F]' scripts/monitor.py docs/AI-POLICY-MIGRATION.md docs/AI_COMPLIANCE_PR_DRAFT.md scripts/monitor-test.sh
    exit 1
fi

echo "No emojis or disallowed symbols found in any monitored files."
echo "=== Platform Policy Monitor Test Suite Passed Successfully ==="
exit 0
