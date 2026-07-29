#!/usr/bin/env python3
"""Tests generate-timeline.py against a mock overdue/upcoming/far-future
deadline set, and asserts the output and generated markdown carry no emojis."""

import unittest
import os
import sys
import subprocess
import json
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMP_DB_PATH = os.path.join(ROOT, "data", "regulatory-deadlines-temp-test.json")
REAL_DB_PATH = os.path.join(ROOT, "data", "regulatory-deadlines.json")
BACKUP_DB_PATH = os.path.join(ROOT, "data", "regulatory-deadlines-backup-test.json")
OUTPUT_MD_PATH = os.path.join(ROOT, "docs", "REGULATORY-TIMELINE.md")


class TestGenerateTimeline(unittest.TestCase):
    def setUp(self):
        # Create a mock json deadlines DB with dynamic, relative dates
        now = datetime.now(timezone.utc)

        overdue_date = (now - timedelta(days=10)).strftime("%Y-%m-%d")
        upcoming_date = (now + timedelta(days=5)).strftime("%Y-%m-%d")
        future_date = (now + timedelta(days=200)).strftime("%Y-%m-%d")

        self.mock_data = {
            "deadlines": [
                {
                    "id": "TEST-OVERDUE",
                    "jurisdiction": "Test Jurisdiction A",
                    "law": "Passed Act 2024",
                    "requirement": "Registration",
                    "effective_date": overdue_date,
                    "grace_period": "None",
                    "mandatory_date": overdue_date,
                    "enforcement_date": overdue_date,
                    "affected_repository_sections": "docs/APPLE.md",
                    "priority": "Critical",
                },
                {
                    "id": "TEST-UPCOMING",
                    "jurisdiction": "Test Jurisdiction B",
                    "law": "Upcoming Regulation 2026",
                    "requirement": "Consent",
                    "effective_date": upcoming_date,
                    "grace_period": "None",
                    "mandatory_date": upcoming_date,
                    "enforcement_date": upcoming_date,
                    "affected_repository_sections": ["docs/APPLE.md"],
                    "priority": "High",
                },
                {
                    "id": "TEST-FAR-FUTURE",
                    "jurisdiction": "Test Jurisdiction C",
                    "law": "Far Future Law 2028",
                    "requirement": "Audit",
                    "effective_date": future_date,
                    "grace_period": "None",
                    "mandatory_date": future_date,
                    "enforcement_date": future_date,
                    "affected_repository_sections": ["docs/APPLE.md"],
                    "priority": "Medium",
                },
            ]
        }

        # Backup the real DB if it exists
        if os.path.exists(REAL_DB_PATH):
            os.rename(REAL_DB_PATH, BACKUP_DB_PATH)

        # Write the mock DB
        with open(REAL_DB_PATH, "w") as f:
            json.dump(self.mock_data, f, indent=2)

    def tearDown(self):
        # Clean up temporary/mock DB
        if os.path.exists(REAL_DB_PATH):
            os.remove(REAL_DB_PATH)

        # Restore the backup DB if it existed
        if os.path.exists(BACKUP_DB_PATH):
            os.rename(BACKUP_DB_PATH, REAL_DB_PATH)

            # Regenerate the real timeline to keep docs/REGULATORY-TIMELINE.md up-to-date
            cmd = [sys.executable, os.path.join(ROOT, "scripts", "generate-timeline.py")]
            subprocess.run(cmd, capture_output=True, text=True)

    def test_generate_timeline_behavior(self):
        # Execute generate-timeline.py
        cmd = [sys.executable, os.path.join(ROOT, "scripts", "generate-timeline.py")]
        result = subprocess.run(cmd, capture_output=True, text=True)

        # The warnings should be output on stderr
        stderr_output = result.stderr
        stdout_output = result.stdout

        # Verify passed/overdue warning exists in stderr
        self.assertIn("ACTIVE / PASSED COMPLIANCE DEADLINES", stderr_output)
        self.assertIn("Passed Act 2024", stderr_output)
        self.assertIn("days overdue", stderr_output)

        # Verify upcoming warning exists in stderr
        self.assertIn("UPCOMING COMPLIANCE DEADLINES", stderr_output)
        self.assertIn("Upcoming Regulation 2026", stderr_output)
        self.assertIn("days", stderr_output)

        # Verify far future deadline is NOT warned in stderr
        self.assertNotIn("Far Future Law 2028", stderr_output)

        # Ensure NO emoji is present in stderr
        for char in stderr_output:
            self.assertLess(
                ord(char),
                0x1F600,
                f"Found an emoji or high unicode character in stderr output: {char}",
            )

        # Check generated markdown file
        self.assertTrue(os.path.exists(OUTPUT_MD_PATH))
        with open(OUTPUT_MD_PATH, "r") as f:
            md_content = f.read()

        # Check document sections are generated
        self.assertIn("# Regulatory Compliance Timeline", md_content)
        self.assertIn("## Active and Approaching Compliance Warnings", md_content)
        self.assertIn("## Complete Chronological Timeline Summary", md_content)
        self.assertIn("## Detailed Compliance Breakdown", md_content)

        # Check individual mock data items are present and ordered
        # Overdue and upcoming should be in the warnings section
        self.assertIn("TEST-OVERDUE", md_content)
        self.assertIn("TEST-UPCOMING", md_content)

        # Complete Chronological Timeline should contain all three
        self.assertIn("TEST-FAR-FUTURE", md_content)

        # Check chronological sorting by date
        overdue_idx = md_content.find("TEST-OVERDUE")
        upcoming_idx = md_content.find("TEST-UPCOMING")
        future_idx = md_content.find("TEST-FAR-FUTURE")

        # Sorting should ensure overdue index is before upcoming, and upcoming is before future
        self.assertTrue(overdue_idx < upcoming_idx < future_idx)

        # Ensure NO emoji is present in the markdown
        for char in md_content:
            self.assertLess(
                ord(char),
                0x1F600,
                f"Found an emoji or high unicode character in markdown: {char}",
            )


if __name__ == "__main__":
    unittest.main()
