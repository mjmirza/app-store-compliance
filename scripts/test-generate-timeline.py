#!/usr/bin/env python3
"""Tests generate-timeline.py against a mock set of regulatory deadlines.
Verifies parsing, chronological sorting, console warning detection on stderr,
and markdown document generation without any emojis or emoticons."""

import unittest
import os
import sys
import subprocess
import json
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMP_DB_PATH = os.path.join(ROOT, "data", "regulatory-deadlines-temp-test-timeline.json")
TEMP_OUT_PATH = os.path.join(ROOT, "docs", "REGULATORY-TIMELINE-temp-test.md")


class TestGenerateTimeline(unittest.TestCase):
    def setUp(self):
        # Create a mock json deadlines database with relative dates
        now = datetime.now(timezone.utc)

        # 10 days overdue
        self.overdue_date = (now - timedelta(days=10)).strftime("%Y-%m-%d")
        # 5 days in the future (approaching)
        self.upcoming_date = (now + timedelta(days=5)).strftime("%Y-%m-%d")
        # 200 days in the future (far future)
        self.future_date = (now + timedelta(days=200)).strftime("%Y-%m-%d")

        self.mock_data = {
            "deadlines": [
                {
                    "id": "TEST-UPCOMING-1",
                    "jurisdiction": "Jurisdiction B",
                    "law": "Upcoming Regulation B",
                    "requirement": "Requirement B",
                    "effective_date": self.upcoming_date,
                    "grace_period": "None",
                    "mandatory_date": self.upcoming_date,
                    "enforcement_date": self.upcoming_date,
                    "affected_repository_sections": "docs/APPLE.md",
                    "priority": "High"
                },
                {
                    "id": "TEST-OVERDUE-1",
                    "jurisdiction": "Jurisdiction A",
                    "law": "Passed Act A",
                    "requirement": "Requirement A",
                    "effective_date": self.overdue_date,
                    "grace_period": "None",
                    "mandatory_date": self.overdue_date,
                    "enforcement_date": self.overdue_date,
                    "affected_repository_sections": ["docs/GOOGLE-PLAY.md"],
                    "priority": "Critical"
                },
                {
                    "id": "TEST-FUTURE-1",
                    "jurisdiction": "Jurisdiction C",
                    "law": "Future Law C",
                    "requirement": "Requirement C",
                    "effective_date": self.future_date,
                    "grace_period": "None",
                    "mandatory_date": self.future_date,
                    "enforcement_date": self.future_date,
                    "affected_repository_sections": "docs/ADVANCED-2026.md",
                    "priority": "Medium"
                }
            ]
        }

        with open(TEMP_DB_PATH, "w") as f:
            json.dump(self.mock_data, f, indent=2)

    def tearDown(self):
        if os.path.exists(TEMP_DB_PATH):
            os.remove(TEMP_DB_PATH)
        if os.path.exists(TEMP_OUT_PATH):
            os.remove(TEMP_OUT_PATH)

    def test_timeline_generation(self):
        # We will temporarily back up the real database and output path
        real_db_path = os.path.join(ROOT, "data", "regulatory-deadlines.json")
        backup_db_path = os.path.join(ROOT, "data", "regulatory-deadlines-backup-timeline.json")

        real_out_path = os.path.join(ROOT, "docs", "REGULATORY-TIMELINE.md")
        backup_out_path = os.path.join(ROOT, "docs", "REGULATORY-TIMELINE-backup.md")

        if os.path.exists(real_db_path):
            os.rename(real_db_path, backup_db_path)
        if os.path.exists(real_out_path):
            os.rename(real_out_path, backup_out_path)

        try:
            # Put our mock database in place of the real database
            os.rename(TEMP_DB_PATH, real_db_path)

            # Run generate-timeline.py
            cmd = [sys.executable, os.path.join(ROOT, "scripts", "generate-timeline.py")]
            result = subprocess.run(cmd, capture_output=True, text=True)

            # Check stderr output warnings
            stderr_output = result.stderr
            self.assertIn("WARNING: Active / Overdue Regulatory Compliance Deadlines Detected:", stderr_output)
            self.assertIn("Passed Act A", stderr_output)
            self.assertIn("WARNING: Approaching Regulatory Compliance Deadlines Detected (Within 90 Days):", stderr_output)
            self.assertIn("Upcoming Regulation B", stderr_output)
            # Far future should not be warned about
            self.assertNotIn("Future Law C", stderr_output)

            # Ensure there are no emojis in the output logs
            for char in stderr_output + result.stdout:
                self.assertLess(
                    ord(char),
                    0x1F600,
                    "Found an emoji or high unicode character in stderr/stdout logs!",
                )

            # Verify markdown file generation
            self.assertTrue(os.path.exists(real_out_path))
            with open(real_out_path, "r") as f:
                md_content = f.read()

            # The full chronological timeline should list Passed Act A (overdue) then Upcoming Regulation B then Future Law C
            # Chronological order search: Passed Act A must appear before Upcoming Regulation B, and Upcoming before Future Law C
            idx_act_a = md_content.find("Passed Act A")
            idx_reg_b = md_content.find("Upcoming Regulation B")
            idx_law_c = md_content.find("Future Law C")

            self.assertNotEqual(idx_act_a, -1, "Passed Act A not found in MD")
            self.assertNotEqual(idx_reg_b, -1, "Upcoming Regulation B not found in MD")
            self.assertNotEqual(idx_law_c, -1, "Future Law C not found in MD")

            self.assertTrue(idx_act_a < idx_reg_b, "Passed Act A should be chronologically before Upcoming Regulation B")
            self.assertTrue(idx_reg_b < idx_law_c, "Upcoming Regulation B should be chronologically before Future Law C")

            # Check for the warning sections
            self.assertIn("Active / Overdue Deadlines (Action Required)", md_content)
            self.assertIn("Approaching Deadlines (Within 90 Days)", md_content)

            # Check detailed record fields
            self.assertIn("ID: TEST-OVERDUE-1", md_content)
            self.assertIn("- **Jurisdiction:** Jurisdiction A", md_content)
            self.assertIn("- **Law:** Passed Act A", md_content)
            self.assertIn("- **Requirement:** Requirement A", md_content)
            self.assertIn(f"- **Effective Date:** {self.overdue_date}", md_content)
            self.assertIn("- **Grace Period:** None", md_content)
            self.assertIn(f"- **Mandatory Date:** {self.overdue_date}", md_content)
            self.assertIn(f"- **Enforcement Date:** {self.overdue_date}", md_content)
            self.assertIn("- **Priority:** CRITICAL", md_content)
            self.assertIn("- **Affected Repository Sections:** docs/GOOGLE-PLAY.md", md_content)

            # Check for list format mapping to string
            self.assertIn("ID: TEST-UPCOMING-1", md_content)
            self.assertIn("- **Affected Repository Sections:** docs/APPLE.md", md_content)

            # Ensure NO emoji is present in the markdown output
            for char in md_content:
                self.assertLess(
                    ord(char),
                    0x1F600,
                    "Found an emoji or high unicode character in generated markdown document!",
                )

        finally:
            # Restore
            if os.path.exists(real_db_path):
                os.remove(real_db_path)
            if os.path.exists(backup_db_path):
                os.rename(backup_db_path, real_db_path)

            if os.path.exists(real_out_path):
                os.remove(real_out_path)
            if os.path.exists(backup_out_path):
                os.rename(backup_out_path, real_out_path)


if __name__ == "__main__":
    unittest.main()
