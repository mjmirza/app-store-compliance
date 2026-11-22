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


class TestDatabaseReadAsUtf8(unittest.TestCase):
    """#2330: the database is read as UTF-8 whatever the platform default is, the
    report survives a law name outside ASCII on a cp1252 pipe, and a database that
    cannot be read still fails open."""

    SCRIPT = os.path.join(ROOT, "scripts", "deadline-checker.py")

    def _run(self, db_bytes, **env_extra):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "deadlines.json")
            with open(path, "wb") as f:
                f.write(db_bytes)
            env = dict(os.environ, DEADLINES_FILE=path, **env_extra)
            result = subprocess.run(
                [sys.executable, self.SCRIPT], capture_output=True, env=env
            )
        return (
            result.returncode,
            result.stdout.decode("utf-8", "replace"),
            result.stderr.decode("utf-8", "replace"),
        )

    def _upcoming(self, law):
        day = (datetime.now(timezone.utc) + timedelta(days=5)).strftime("%Y-%m-%d")
        row = {
            "id": "TEST-UTF8",
            "jurisdiction": "Test",
            "law": law,
            "requirement": "Fixture",
            "effective_date": day,
            "grace_period": "none",
            "mandatory_date": day,
            "enforcement_date": day,
            "affected_repository_sections": "docs/APPLE.md",
            "priority": "high",
        }
        return json.dumps({"deadlines": [row]}, ensure_ascii=False).encode("utf-8")

    def test_non_ascii_law_name_survives_a_cp1252_pipe(self):
        rc, out, err = self._run(
            self._upcoming("Act 17 July 2026 改正 第56号"), PYTHONIOENCODING="cp1252"
        )
        self.assertEqual(rc, 0, err)
        self.assertIn("改正 第56号", out)

    def test_no_default_encoding_warning(self):
        rc, out, err = self._run(
            self._upcoming("Test Act"), PYTHONWARNDEFAULTENCODING="1"
        )
        self.assertEqual(rc, 0, err)
        self.assertNotIn("EncodingWarning", out + err)

    def test_database_that_is_not_utf8_still_fails_open(self):
        db = b'{"deadlines": [{"law": "bad ' + bytes([255]) + b' byte"}]}'
        rc, out, err = self._run(db)
        self.assertEqual(rc, 0, err)
        self.assertIn("Error loading deadlines", err)

    @unittest.skipIf(sys.platform == "win32", "POSIX paths carry undecodable bytes")
    def test_missing_database_with_undecodable_path_fails_open(self):
        # Reconfiguring stdout must keep its error policy, or this message crashes.
        path = os.fsdecode(b"/nonexistent/act-\xff.json")
        env = dict(os.environ, DEADLINES_FILE=path)
        result = subprocess.run([sys.executable, self.SCRIPT], capture_output=True, env=env)
        err = result.stderr.decode("utf-8", "replace")
        self.assertEqual(result.returncode, 0, err)
        self.assertIn("Deadlines database not found at", err)


if __name__ == "__main__":
    unittest.main()
