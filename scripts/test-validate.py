#!/usr/bin/env python3
"""Tests the deadline rules in validate.py (#660, #661): a passed deadline needs an
owner, the effective, mandatory, and enforcement dates must be in order, and every
entry names its source and the day it was last read."""

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
        "source_url": "https://example.org/act",
        "verified_on": day(-1),
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


class TestVersionsAgree(unittest.TestCase):
    """VERSION, the data files and CITATION.cff must name one release."""

    def run_with(self, text):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "VERSION")
            with open(path, "w") as f:
                f.write(text)
            env = {k: v for k, v in os.environ.items() if k != "DEADLINES_FILE"}
            env["VERSION_FILE"] = path
            cmd = [sys.executable, os.path.join(ROOT, "scripts", "validate.py")]
            r = subprocess.run(cmd, capture_output=True, text=True, env=env)
        return r.returncode, r.stdout + r.stderr

    def test_mismatch_fails(self):
        rc, out = self.run_with("9.9.9\n")
        self.assertEqual(rc, 1, out)
        self.assertIn("9.9.9", out)
        self.assertIn("CITATION.cff", out)

    def test_real_version_matches(self):
        with open(os.path.join(ROOT, "VERSION")) as f:
            rc, out = self.run_with(f.read())
        self.assertEqual(rc, 0, out)



class TestSourceProvenance(unittest.TestCase):
    def strip(self, key):
        e = entry()
        del e[key]
        return e

    def test_missing_source_url_fails(self):
        rc, out = run(self.strip("source_url"))
        self.assertEqual(rc, 1, out)
        self.assertIn("source_url", out)

    def test_missing_verified_on_fails(self):
        rc, out = run(self.strip("verified_on"))
        self.assertEqual(rc, 1, out)
        self.assertIn("verified_on", out)

    def test_source_url_must_be_web_address(self):
        rc, out = run(entry(source_url="docs/APPLE.md"))
        self.assertEqual(rc, 1, out)
        self.assertIn("not a web address", out)

    def test_bad_verified_on_format_fails(self):
        rc, out = run(entry(verified_on="14 Nov 2026"))
        self.assertEqual(rc, 1, out)
        self.assertIn("verified_on", out)

    def test_future_verified_on_fails(self):
        rc, out = run(entry(verified_on=day(3)))
        self.assertEqual(rc, 1, out)
        self.assertIn("in the future", out)

    def test_stale_source_warns_but_passes(self):
        rc, out = run(entry(verified_on=day(-181)))
        self.assertEqual(rc, 0, out)
        self.assertIn("Re-read", out)

    def test_source_read_exactly_180_days_ago_is_quiet(self):
        rc, out = run(entry(verified_on=day(-180)))
        self.assertEqual(rc, 0, out)
        self.assertNotIn("Re-read", out)

    def test_empty_source_note_fails(self):
        rc, out = run(entry(source_note="  "))
        self.assertEqual(rc, 1, out)
        self.assertIn("source_note", out)

    def test_source_note_is_optional(self):
        rc, out = run(entry())
        self.assertEqual(rc, 0, out)


def run_with(db_path, **env_extra):
    env = dict(os.environ, DEADLINES_FILE=db_path, **env_extra)
    cmd = [sys.executable, os.path.join(ROOT, "scripts", "validate.py")]
    result = subprocess.run(cmd, capture_output=True, env=env)
    return result.returncode, (result.stdout + result.stderr).decode("utf-8", "replace")


class TestDataFilesReadAsUtf8(unittest.TestCase):
    """#2330: validate.py opens the data files as UTF-8, not the platform default."""

    def _db(self, tmp, law):
        path = os.path.join(tmp, "deadlines.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                {"deadlines": [entry(law=law)]}, f, ensure_ascii=False, indent=2
            )
        return path

    def test_non_ascii_entry_validates(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc, out = run_with(self._db(tmp, "Act 改正 第56号"))
        self.assertEqual(rc, 0, out)

    def test_no_default_encoding_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc, out = run_with(
                self._db(tmp, "Test Act"), PYTHONWARNDEFAULTENCODING="1"
            )
        self.assertEqual(rc, 0, out)
        self.assertNotIn("EncodingWarning", out)

    def test_non_ascii_id_is_read_exactly(self):
        # A wrong decoding still validates, so check the id the validator echoes back.
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "deadlines.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"deadlines": [entry(id="ACTE-\u00e9-1", verified_on="2026-13-40")]}, f, ensure_ascii=False)
            rc, out = run_with(path, PYTHONIOENCODING="utf-8")
        self.assertNotEqual(rc, 0, out)
        self.assertIn("deadline 'ACTE-\u00e9-1' has invalid verified_on", out)


if __name__ == "__main__":
    unittest.main()
