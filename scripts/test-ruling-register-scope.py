#!/usr/bin/env python3
"""An unknown query scope must not look like a clean result."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

script = Path(__file__).with_name("ruling-register.py")
spec = importlib.util.spec_from_file_location("register", script)
register = importlib.util.module_from_spec(spec)
spec.loader.exec_module(register)


class RegisterScope(unittest.TestCase):
    def test_invalid_scope_exits_with_a_diagnostic(self):
        for args, description in ((["--regions", "USA"], "two-letter country codes"),
                                  (["--regions", ""], "two-letter country codes"),
                                  (["--regions", "AU", "--stores", "ios"], "unknown stores ios")):
            with self.subTest(args=args):
                result = subprocess.run([sys.executable, str(script), "due", *args, "--json"],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 1)
                self.assertIn(description, result.stderr)
                self.assertEqual(result.stdout, "")

    def test_existing_register_and_normalized_scope_still_work(self):
        result = subprocess.run([sys.executable, str(script), "due", "--regions", " au ", "--stores", "apple",
                                 "--features", "social", "--json"], capture_output=True, text=True, check=True)
        self.assertIn("RR-AU-SOCIAL-MIN-AGE", {r["id"] for r in json.loads(result.stdout)})

    def test_invalid_rule_scope_is_rejected(self):
        rules = register.load(register.REGISTER)
        rules["requirements"][0]["jurisdiction"] = "USA"
        self.assertTrue(any("jurisdiction" in error for error in register.validate(rules, register.pattern_ids())))


if __name__ == "__main__":
    unittest.main()
