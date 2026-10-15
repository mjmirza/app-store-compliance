#!/usr/bin/env python3
"""Tests deadline-checker.py against a mock overdue/upcoming/far-future
deadline set, and asserts the output carries no emojis."""

import unittest
import os
import sys
import subprocess
import json
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMP_DB_PATH = os.path.join(ROOT, "data", "regulatory-deadlines-temp-test.json")


class TestDeadlineChecker(unittest.TestCase):
    def setUp(self):
        # Create a mock json deadlines DB with dynamic, relative dates
        now = datetime.now(timezone.utc)

        overdue_date = (now - timedelta(days=10)).strftime("%Y-%m-%d")
        upcoming_date = (now + timedelta(days=5)).strftime("%Y-%m-%d")
        future_date = (now + timedelta(days=200)).strftime("%Y-%m-%d")

        self.mock_data = {
            "deadlines": [
                {
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

    def test_deadline_checker_warnings(self):
        # Run deadline-checker.py pointing to the temporary test DB using an environment variable or overriding python call
        # Since deadline-checker.py points directly to data/regulatory-deadlines.json, we can temporarily swap the files
        real_db_path = os.path.join(ROOT, "data", "regulatory-deadlines.json")
        backup_db_path = os.path.join(
            ROOT, "data", "regulatory-deadlines-backup-test.json"
        )

        if os.path.exists(real_db_path):
            os.rename(real_db_path, backup_db_path)

        try:
            os.rename(TEMP_DB_PATH, real_db_path)

            # Execute deadline-checker.py
            cmd = [sys.executable, os.path.join(ROOT, "scripts", "deadline-checker.py")]
            result = subprocess.run(cmd, capture_output=True, text=True)

            output = result.stdout

            # Verify passed/overdue warning exists in stdout
            self.assertIn("ACTIVE / PASSED COMPLIANCE DEADLINES", output)
            self.assertIn("Passed Act 2024", output)
            self.assertTrue("days overdue" in output)

            # Verify upcoming warning exists in stdout
            self.assertIn("UPCOMING COMPLIANCE DEADLINES", output)
            self.assertIn("Upcoming Regulation 2026", output)
            self.assertTrue("in " in output and " days" in output)

            # Verify all requested fields are present in the output
            self.assertIn("Effective date:", output)
            self.assertIn("Grace period:", output)
            self.assertIn("Enforcement date:", output)
            self.assertIn("Affected repository sections:", output)
            self.assertIn("Priority:", output)

            # Verify far future deadline is NOT in stdout
            self.assertNotIn("Far Future Law 2028", output)

            # Ensure NO emoji is present in the output
            for char in output:
                self.assertLess(
                    ord(char),
                    0x1F600,
                    "Found an emoji or high unicode character in output!",
                )

        finally:
            if os.path.exists(real_db_path):
                # Clean up and restore
                if os.path.exists(TEMP_DB_PATH):
                    os.remove(TEMP_DB_PATH)
                os.rename(real_db_path, TEMP_DB_PATH)
            if os.path.exists(backup_db_path):
                os.rename(backup_db_path, real_db_path)


class TestDeadlineDayBoundary(unittest.TestCase):
    """A deadline is due on its own date, not one day overdue, and tomorrow is one day away."""

    def _run(self, script, extra_env):
        env = dict(os.environ, **extra_env)
        cmd = [sys.executable, os.path.join(ROOT, "scripts", script)]
        return subprocess.run(cmd, capture_output=True, text=True, env=env)

    def _db(self, tmpdir):
        today = datetime.now(timezone.utc).date()
        rows = []
        for name, delta in (("Due Today Act", 0), ("Due Tomorrow Act", 1), ("Due Yesterday Act", -1)):
            day = (today + timedelta(days=delta)).strftime("%Y-%m-%d")
            rows.append({
                "id": name.upper().replace(" ", "-"),
                "jurisdiction": "Test",
                "law": name,
                "requirement": "Boundary",
                "effective_date": day,
                "grace_period": "none",
                "mandatory_date": day,
                "enforcement_date": day,
                "affected_repository_sections": "docs/APPLE.md",
                "priority": "high",
            })
        path = os.path.join(tmpdir, "deadlines.json")
        with open(path, "w") as f:
            json.dump({"deadlines": rows}, f)
        return path

    def test_checker_counts_whole_days(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out = self._run("deadline-checker.py", {"DEADLINES_FILE": self._db(tmp)}).stdout
        passed, _, upcoming = out.partition("UPCOMING COMPLIANCE DEADLINES")
        self.assertIn("Due Yesterday Act", passed)
        self.assertIn("(1 days overdue)", passed)
        self.assertNotIn("Due Today Act", passed)
        self.assertIn("Due Today Act", upcoming)
        self.assertIn("(in 0 days)", upcoming)
        self.assertIn("(in 1 days)", upcoming)

    def test_timeline_counts_whole_days(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out_md = os.path.join(tmp, "timeline.md")
            self._run("generate-timeline.py", {"DEADLINES_FILE": self._db(tmp), "TIMELINE_OUTPUT_FILE": out_md})
            with open(out_md, "r") as f:
                text = f.read()
        row = {}
        for line in text.splitlines():
            for name in ("Due Today Act", "Due Tomorrow Act", "Due Yesterday Act"):
                if line.startswith("|") and name in line:
                    row.setdefault(name, line)
        self.assertIn("| 0 days |", row["Due Today Act"])
        self.assertIn("| 1 days |", row["Due Tomorrow Act"])
        self.assertIn("| 1 days |", row["Due Yesterday Act"])
        overdue_part = text.split("### Approaching Deadlines")[0]
        self.assertIn("Due Yesterday Act", overdue_part)
        self.assertNotIn("Due Today Act", overdue_part)


if __name__ == "__main__":
    unittest.main()
