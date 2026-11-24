#!/usr/bin/env python3
"""Release reports must show the difference between no findings and missing coverage."""
import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

spec = importlib.util.spec_from_file_location("audit", Path(__file__).with_name("release-audit.py"))
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class ReleaseReport(unittest.TestCase):
    def test_empty_areas_never_claim_a_pass(self):
        positive = {"id": "GOOGLE-PERM-ACCESSIBILITY-MISUSE", "severity": "high", "title": "Fixture", "fix": "Review"}
        with TemporaryDirectory() as directory:
            path = Path(directory) / "RELEASE-READINESS-REPORT.md"
            self.assertEqual(audit.compile_report(directory, [], [], {}, {}), 0)
            self.assertIn("| Accessibility | NO_FINDINGS | 0 |", path.read_text(encoding="utf-8"))
            self.assertEqual(audit.compile_report(directory, [positive], ["fixture scanner failed"], {}, {}), 3)
            report = path.read_text(encoding="utf-8")
            self.assertIn("| Accessibility | BLOCKED | 1 |", report)
            self.assertIn("| Store metadata | NOT_CHECKED | 0 |", report)
            self.assertIn("### 8. Store metadata\n- Status: NOT_CHECKED", report)


if __name__ == "__main__":
    unittest.main()
