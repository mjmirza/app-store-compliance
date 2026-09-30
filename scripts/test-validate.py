#!/usr/bin/env python3
"""Tests the deadline rules in validate.py (#660): a passed deadline needs an
owner, and the effective, mandatory, and enforcement dates must be in order."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def day(offset):
    return (datetime.now(timezone.utc).date() + timedelta(days=offset)).strftime(
        "%Y-%m-%d"
    )


def entry(**over):
    base = {
        "id": "TEST-ENTRY",
        "jurisdiction": "Test",
        "law": "Test Act",
        "requirement": "Fixture",
        "effective_date": day(100),
        "grace_period": "none",
        "mandatory_date": day(100),
        "enforcement_date": day(100),
        "affected_repository_sections": "docs/APPLE.md",
        "priority": "high",
    }
    base.update(over)
    return base


def run(*entries):
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "deadlines.json")
        with open(path, "w") as f:
            json.dump({"deadlines": list(entries)}, f)
        env = dict(os.environ, DEADLINES_FILE=path)
        cmd = [sys.executable, os.path.join(ROOT, "scripts", "validate.py")]
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return result.returncode, result.stdout + result.stderr


class TestPassedDeadlineNeedsOwner(unittest.TestCase):
    def test_passed_without_owner_fails(self):
        d = day(-8)
        rc, out = run(entry(effective_date=d, mandatory_date=d, enforcement_date=d))
        self.assertEqual(rc, 1, out)
        self.assertIn("passed", out)
        self.assertIn("absorbed_into", out)

    def test_passed_with_owner_is_ok(self):
        d = day(-8)
        rc, out = run(
            entry(
                effective_date=d,
                mandatory_date=d,
                enforcement_date=d,
                absorbed_into="docs/APPLE.md",
            )
        )
        self.assertEqual(rc, 0, out)

    def test_empty_owner_counts_as_missing(self):
        d = day(-8)
        rc, out = run(
            entry(
                effective_date=d,
                mandatory_date=d,
                enforcement_date=d,
                absorbed_into="  ",
            )
        )
        self.assertEqual(rc, 1, out)

    def test_seven_day_grace(self):
        d = day(-7)
        rc, out = run(entry(effective_date=d, mandatory_date=d, enforcement_date=d))
        self.assertEqual(rc, 0, out)
        self.assertIn("warning", out)


class TestDateOrder(unittest.TestCase):
    def test_effective_after_mandatory_fails(self):
        rc, out = run(
            entry(
                effective_date=day(120),
                mandatory_date=day(100),
                enforcement_date=day(130),
            )
        )
        self.assertEqual(rc, 1, out)
        self.assertIn("effective_date", out)

    def test_mandatory_after_enforcement_fails(self):
        rc, out = run(
            entry(
                effective_date=day(90),
                mandatory_date=day(100),
                enforcement_date=day(95),
            )
        )
        self.assertEqual(rc, 1, out)
        self.assertIn("enforcement_date", out)

    def test_ordered_and_equal_dates_are_ok(self):
        rc, out = run(
            entry(
                id="A",
                effective_date=day(90),
                mandatory_date=day(100),
                enforcement_date=day(110),
            ),
            entry(id="B"),
        )
        self.assertEqual(rc, 0, out)

    def test_dead_section_path_fails(self):
        rc, out = run(entry(affected_repository_sections="docs/NO-SUCH-FILE.md section 2"))
        self.assertEqual(rc, 1, out)
        self.assertIn("docs/NO-SUCH-FILE.md", out)

    def test_real_data_is_valid(self):
        cmd = [sys.executable, os.path.join(ROOT, "scripts", "validate.py")]
        env = {k: v for k, v in os.environ.items() if k != "DEADLINES_FILE"}
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
