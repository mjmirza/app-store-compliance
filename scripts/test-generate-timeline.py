#!/usr/bin/env python3
"""Tests generate-timeline.py against a mock database with relative dates
to assert proper sorting, warning logic, and formatting without emojis."""

import unittest
import os
import sys
import subprocess
import json
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEADLINES_FILE = os.path.join(ROOT, "data", "regulatory-deadlines.json")
TIMELINE_FILE = os.path.join(ROOT, "docs", "REGULATORY-TIMELINE.md")


class TestGenerateTimeline(unittest.TestCase):
    def setUp(self):
        # We will backup the real deadlines file and real timeline file if they exist
        self.real_deadlines_backup = os.path.join(ROOT, "data", "regulatory-deadlines-real-backup.json")
        self.real_timeline_backup = os.path.join(ROOT, "docs", "REGULATORY-TIMELINE-real-backup.md")

        if os.path.exists(DEADLINES_FILE):
            os.rename(DEADLINES_FILE, self.real_deadlines_backup)
        if os.path.exists(TIMELINE_FILE):
            os.rename(TIMELINE_FILE, self.real_timeline_backup)

        now = datetime.now(timezone.utc)
        self.overdue_date = (now - timedelta(days=15)).strftime("%Y-%m-%d")
        self.approaching_date = (now + timedelta(days=45)).strftime("%Y-%m-%d")
        self.future_date = (now + timedelta(days=120)).strftime("%Y-%m-%d")

        # Mock database with specific relative dates
        self.mock_data = {
            "deadlines": [
                {
                    "id": "TEST-FUTURE",
                    "jurisdiction": "Test Jurisdiction C",
                    "law": "Future Act 2028",
                    "requirement": "Audit requirement",
                    "effective_date": self.future_date,
                    "grace_period": "None",
                    "mandatory_date": self.future_date,
                    "enforcement_date": self.future_date,
                    "affected_repository_sections": "docs/FUTURE.md",
                    "priority": "medium"
                },
                {
                    "id": "TEST-OVERDUE",
                    "jurisdiction": "Test Jurisdiction A",
                    "law": "Overdue Act 2024",
                    "requirement": "Registration requirement",
                    "effective_date": self.overdue_date,
                    "grace_period": "None",
                    "mandatory_date": self.overdue_date,
                    "enforcement_date": self.overdue_date,
                    "affected_repository_sections": "docs/OVERDUE.md",
                    "priority": "critical"
                },
                {
                    "id": "TEST-APPROACHING",
                    "jurisdiction": "Test Jurisdiction B",
                    "law": "Approaching Act 2026",
                    "requirement": "Consent requirement",
                    "effective_date": self.approaching_date,
                    "grace_period": "None",
                    "mandatory_date": self.approaching_date,
                    "enforcement_date": self.approaching_date,
                    "affected_repository_sections": "docs/APPROACHING.md",
                    "priority": "high"
                }
            ]
        }

        with open(DEADLINES_FILE, "w") as f:
            json.dump(self.mock_data, f, indent=2)

    def tearDown(self):
        # Restore real files
        if os.path.exists(DEADLINES_FILE):
            os.remove(DEADLINES_FILE)
        if os.path.exists(TIMELINE_FILE):
            os.remove(TIMELINE_FILE)

        if os.path.exists(self.real_deadlines_backup):
            os.rename(self.real_deadlines_backup, DEADLINES_FILE)
        if os.path.exists(self.real_timeline_backup):
            os.rename(self.real_timeline_backup, TIMELINE_FILE)

    def test_timeline_generation(self):
        # Execute generate-timeline.py
        cmd = [sys.executable, os.path.join(ROOT, "scripts", "generate-timeline.py")]
        result = subprocess.run(cmd, capture_output=True, text=True)

        # 1. Assert that warnings are printed to stderr
        stderr_output = result.stderr
        self.assertIn("WARNING: OVERDUE [CRITICAL] Overdue Act 2024", stderr_output)
        self.assertIn("WARNING: APPROACHING [HIGH] Approaching Act 2026", stderr_output)
        self.assertNotIn("Future Act 2028", stderr_output)

        # 2. Check the output timeline file structure and content
        self.assertTrue(os.path.exists(TIMELINE_FILE))
        with open(TIMELINE_FILE, "r") as f:
            md_content = f.read()

        # 3. Assert proper timeline sections exist
        self.assertIn("# Regulatory Compliance Timeline", md_content)
        self.assertIn("## Active and Approaching Compliance Warnings", md_content)
        self.assertIn("### Active / Overdue Deadlines", md_content)
        self.assertIn("### Approaching Deadlines (Within 90 Days)", md_content)
        self.assertIn("## Chronological Compliance Timeline", md_content)

        # 4. Assert sorted chronological order in the markdown content or table
        overdue_idx = md_content.find("Overdue Act 2024")
        approaching_idx = md_content.find("Approaching Act 2026")
        future_idx = md_content.find("Future Act 2028")

        self.assertNotEqual(overdue_idx, -1)
        self.assertNotEqual(approaching_idx, -1)
        self.assertNotEqual(future_idx, -1)

        # Chronological order check
        self.assertLess(overdue_idx, approaching_idx, "Overdue Act 2024 must come before Approaching Act 2026")
        self.assertLess(approaching_idx, future_idx, "Approaching Act 2026 must come before Future Act 2028")

        # 5. Assert emoji-free rule across script, test, and generated markdown
        for char in stderr_output:
            self.assertLess(ord(char), 0x1F600, "Found emoji or high unicode in stderr!")
        for char in md_content:
            self.assertLess(ord(char), 0x1F600, "Found emoji or high unicode in timeline markdown!")


if __name__ == "__main__":
    unittest.main()
