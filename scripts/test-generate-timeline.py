#!/usr/bin/env python3
"""Tests generate-timeline.py against a mock set of regulatory deadlines.
Asserts proper chronological sorting, active/approaching/future deadline classification,
stderr warnings output, and ensures the compiled markdown contains no emojis.
"""

import unittest
import os
import sys
import subprocess
import json
import tempfile
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestGenerateTimeline(unittest.TestCase):
    def setUp(self):
        # Create a temp file for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.mock_db_path = os.path.join(self.temp_dir.name, "regulatory-deadlines.json")
        self.mock_out_path = os.path.join(self.temp_dir.name, "REGULATORY-TIMELINE.md")

        now = datetime.now(timezone.utc)
        self.overdue_date = (now - timedelta(days=5)).strftime("%Y-%m-%d")
        self.approaching_date = (now + timedelta(days=12)).strftime("%Y-%m-%d")
        self.future_date = (now + timedelta(days=120)).strftime("%Y-%m-%d")

        # Create unsorted entries to verify chronological sorting
        self.mock_data = {
            "deadlines": [
                {
                    "id": "DEADLINE-FUTURE",
                    "jurisdiction": "Global Union",
                    "law": "Future Privacy Act 2027",
                    "requirement": "Biometric protection policies",
                    "effective_date": self.future_date,
                    "grace_period": "None",
                    "mandatory_date": self.future_date,
                    "enforcement_date": self.future_date,
                    "affected_repository_sections": "docs/FUTURE.md",
                    "priority": "low",
                },
                {
                    "id": "DEADLINE-OVERDUE",
                    "jurisdiction": "Eldoria",
                    "law": "Eldorian Security Act 2025",
                    "requirement": "Implement data encryption at rest",
                    "effective_date": self.overdue_date,
                    "grace_period": "3 months",
                    "mandatory_date": self.overdue_date,
                    "enforcement_date": self.overdue_date,
                    "affected_repository_sections": ["docs/SECURITY.md"],
                    "priority": "critical",
                },
                {
                    "id": "DEADLINE-APPROACHING",
                    "jurisdiction": "Aethelgard",
                    "law": "Aethelgard Transparency Directive",
                    "requirement": "User disclosures for algorithms",
                    "effective_date": self.approaching_date,
                    "grace_period": "None",
                    "mandatory_date": self.approaching_date,
                    "enforcement_date": self.approaching_date,
                    "affected_repository_sections": ["docs/AI.md", "docs/LEGAL.md"],
                    "priority": "high",
                },
            ]
        }

        with open(self.mock_db_path, "w") as f:
            json.dump(self.mock_data, f, indent=2)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_generate_timeline_execution(self):
        # Run generate-timeline.py by overriding the DB path and output path using a subprocess or monkeypatching
        # To avoid side-effects on real docs/REGULATORY-TIMELINE.md, let's back up if existing
        real_db_path = os.path.join(ROOT, "data", "regulatory-deadlines.json")
        real_out_path = os.path.join(ROOT, "docs", "REGULATORY-TIMELINE.md")
        backup_db_path = os.path.join(ROOT, "data", "regulatory-deadlines-backup-test.json")
        backup_out_path = os.path.join(ROOT, "docs", "REGULATORY-TIMELINE-backup-test.md")

        if os.path.exists(real_db_path):
            os.rename(real_db_path, backup_db_path)
        if os.path.exists(real_out_path):
            os.rename(real_out_path, backup_out_path)

        try:
            # Copy test data to real location temporarily
            with open(real_db_path, "w") as f:
                json.dump(self.mock_data, f, indent=2)

            # Execute generate-timeline.py
            cmd = [sys.executable, os.path.join(ROOT, "scripts", "generate-timeline.py")]
            result = subprocess.run(cmd, capture_output=True, text=True)

            stderr_output = result.stderr
            stdout_output = result.stdout

            # Check that warnings went to stderr
            self.assertIn("WARNING: ACTIVE / OVERDUE COMPLIANCE DEADLINES DETECTED", stderr_output)
            self.assertIn("Eldorian Security Act 2025", stderr_output)
            self.assertIn("Overdue by", stderr_output)

            self.assertIn("WARNING: APPROACHING COMPLIANCE DEADLINES DETECTED (WITHIN 90 DAYS)", stderr_output)
            self.assertIn("Aethelgard Transparency Directive", stderr_output)
            self.assertIn("Due in", stderr_output)

            # Ensure "Future Privacy Act 2027" warning is NOT on stderr
            self.assertNotIn("Future Privacy Act 2027", stderr_output)

            # Verify compiled file content
            self.assertTrue(os.path.exists(real_out_path))
            with open(real_out_path, "r") as f:
                md_content = f.read()

            # Verify warnings table header and contents exist
            self.assertIn("## Active and Approaching Compliance Warnings", md_content)
            self.assertIn("### Active / Overdue Deadlines", md_content)
            self.assertIn("### Approaching Deadlines (Within 90 Days)", md_content)
            self.assertIn("Eldorian Security Act 2025", md_content)
            self.assertIn("Aethelgard Transparency Directive", md_content)

            # Check for chronological ordering (Eldoria -> Aethelgard -> Global Union)
            eldoria_idx = md_content.find("Eldoria")
            aethelgard_idx = md_content.find("Aethelgard")
            global_union_idx = md_content.find("Global Union")

            self.assertTrue(eldoria_idx < aethelgard_idx < global_union_idx, "Deadlines are not sorted chronologically!")

            # Verify list elements formatting
            self.assertIn("- **ID:** DEADLINE-OVERDUE", md_content)
            self.assertIn("- **Affected Repository Sections:** docs/AI.md, docs/LEGAL.md", md_content)

            # Ensure NO emoji is present in markdown or stdout/stderr
            for char in md_content + stdout_output + stderr_output:
                self.assertLess(
                    ord(char),
                    0x1F600,
                    f"Found an emoji or high unicode character in output: {char}",
                )

        finally:
            # Cleanup and restore
            if os.path.exists(real_db_path):
                os.remove(real_db_path)
            if os.path.exists(real_out_path):
                os.remove(real_out_path)

            if os.path.exists(backup_db_path):
                os.rename(backup_db_path, real_db_path)
            if os.path.exists(backup_out_path):
                os.rename(backup_out_path, real_out_path)


if __name__ == "__main__":
    unittest.main()
