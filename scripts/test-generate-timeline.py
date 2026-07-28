#!/usr/bin/env python3
"""Tests generate-timeline.py against a mock database with overdue,
upcoming, and far-future deadlines, ensuring correct sorting,
stderr warnings, and emoji-free output."""

import unittest
import os
import sys
import subprocess
import json
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMP_DB_PATH = os.path.join(ROOT, "data", "regulatory-deadlines-temp-test.json")
TIMELINE_FILE = os.path.join(ROOT, "docs", "REGULATORY-TIMELINE.md")


class TestGenerateTimeline(unittest.TestCase):
    def setUp(self):
        # Create a mock json deadlines DB with dynamic, relative dates
        now = datetime.now(timezone.utc)

        overdue_date = (now - timedelta(days=10)).strftime("%Y-%m-%d")
        upcoming_date = (now + timedelta(days=5)).strftime("%Y-%m-%d")
        future_date = (now + timedelta(days=200)).strftime("%Y-%m-%d")

        # Create two upcoming deadlines with different dates to test chronological sorting
        upcoming_date_later = (now + timedelta(days=20)).strftime("%Y-%m-%d")

        self.mock_data = {
            "deadlines": [
                {
                    "id": "TEST-UPCOMING-LATER",
                    "jurisdiction": "Test Jurisdiction D",
                    "law": "Upcoming Later Act 2026",
                    "requirement": "Consent Verification",
                    "effective_date": upcoming_date_later,
                    "grace_period": "None",
                    "mandatory_date": upcoming_date_later,
                    "enforcement_date": upcoming_date_later,
                    "affected_repository_sections": ["docs/APPLE.md"],
                    "priority": "High",
                },
                {
                    "id": "TEST-OVERDUE",
                    "jurisdiction": "Test Jurisdiction A",
                    "law": "Passed Act 2024",
                    "requirement": "Registration",
                    "effective_date": overdue_date,
                    "grace_period": "None",
                    "mandatory_date": overdue_date,
                    "enforcement_date": overdue_date,
                    "affected_repository_sections": ["docs/APPLE.md"],
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

        with open(TEMP_DB_PATH, "w") as f:
            json.dump(self.mock_data, f, indent=2)

    def tearDown(self):
        if os.path.exists(TEMP_DB_PATH):
            os.remove(TEMP_DB_PATH)

    def test_timeline_generation(self):
        real_db_path = os.path.join(ROOT, "data", "regulatory-deadlines.json")
        backup_db_path = os.path.join(
            ROOT, "data", "regulatory-deadlines-backup-test.json"
        )
        timeline_backup_path = os.path.join(
            ROOT, "docs", "REGULATORY-TIMELINE-backup-test.md"
        )

        if os.path.exists(real_db_path):
            os.rename(real_db_path, backup_db_path)
        if os.path.exists(TIMELINE_FILE):
            os.rename(TIMELINE_FILE, timeline_backup_path)

        try:
            os.rename(TEMP_DB_PATH, real_db_path)

            # Execute generate-timeline.py
            cmd = [sys.executable, os.path.join(ROOT, "scripts", "generate-timeline.py")]
            result = subprocess.run(cmd, capture_output=True, text=True)

            err_output = result.stderr
            out_output = result.stdout

            # Verify passed/overdue warning exists in stderr
            self.assertIn("ACTIVE / PASSED COMPLIANCE DEADLINES", err_output)
            self.assertIn("Passed Act 2024", err_output)

            # Verify upcoming warning exists in stderr
            self.assertIn("UPCOMING COMPLIANCE DEADLINES", err_output)
            self.assertIn("Upcoming Regulation 2026", err_output)
            self.assertIn("Upcoming Later Act 2026", err_output)

            # Verify far-future deadline is NOT in stderr warnings
            self.assertNotIn("Far Future Law 2028", err_output)

            # Verify docs/REGULATORY-TIMELINE.md was generated
            self.assertTrue(os.path.exists(TIMELINE_FILE))
            with open(TIMELINE_FILE, "r") as f:
                content = f.read()

            # Ensure warnings section is present in markdown
            self.assertIn("## Active and Approaching Compliance Warnings", content)
            self.assertIn("Passed Act 2024", content)
            self.assertIn("Upcoming Regulation 2026", content)
            self.assertIn("Upcoming Later Act 2026", content)
            self.assertNotIn("Far Future Law 2028", content.split("## Complete Chronological Timeline")[0])

            # Ensure chronological timeline is present and sorted
            self.assertIn("## Complete Chronological Timeline", content)
            self.assertIn("Passed Act 2024", content)
            self.assertIn("Upcoming Regulation 2026", content)
            self.assertIn("Upcoming Later Act 2026", content)
            self.assertIn("Far Future Law 2028", content)

            # Check that "Passed Act 2024" appears before "Upcoming Regulation 2026"
            idx_overdue = content.find("Passed Act 2024")
            idx_upcoming = content.find("Upcoming Regulation 2026")
            idx_upcoming_later = content.find("Upcoming Later Act 2026")
            idx_future = content.find("Far Future Law 2028")

            self.assertTrue(idx_overdue < idx_upcoming < idx_upcoming_later < idx_future)

            # Ensure NO emoji is present in the code or output files
            for char in content:
                self.assertLess(
                    ord(char),
                    0x1F600,
                    "Found an emoji or high unicode character in output!",
                )

        finally:
            if os.path.exists(real_db_path):
                if os.path.exists(TEMP_DB_PATH):
                    os.remove(TEMP_DB_PATH)
                os.rename(real_db_path, TEMP_DB_PATH)
            if os.path.exists(backup_db_path):
                os.rename(backup_db_path, real_db_path)
            if os.path.exists(TIMELINE_FILE):
                os.remove(TIMELINE_FILE)
            if os.path.exists(timeline_backup_path):
                os.rename(timeline_backup_path, TIMELINE_FILE)


if __name__ == "__main__":
    unittest.main()
