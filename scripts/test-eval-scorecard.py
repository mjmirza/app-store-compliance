#!/usr/bin/env python3
"""Gold-set checks that must run before the scorecard launches any case."""
import importlib.util
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

script = Path(__file__).with_name("eval-scorecard.py")
spec = importlib.util.spec_from_file_location("scorecard", script)
scorecard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scorecard)


class GoldCoverage(unittest.TestCase):
    def setUp(self):
        self.gold = json.loads(scorecard.GOLD.read_text(encoding="utf-8"))

    def test_current_gold_has_every_feature(self):
        self.assertEqual(scorecard.check_gold(self.gold), [])

    def test_missing_feature_is_rejected_before_execution(self):
        self.gold["cases"] = [case for case in self.gold["cases"] if case["feature"] != "register"]
        with TemporaryDirectory() as directory:
            path = Path(directory) / "gold.json"
            path.write_text(json.dumps(self.gold), encoding="utf-8")
            with patch.object(scorecard, "GOLD", path), patch.object(
                scorecard, "run_case", side_effect=lambda case, *_: (case["expect"], [])
            ) as run:
                self.assertEqual(scorecard.main(), 1)
                run.assert_not_called()

    def test_duplicate_name_cannot_count_twice_within_a_feature(self):
        self.gold["cases"].append(self.gold["cases"][0])
        self.assertTrue(any("duplicate case" in error for error in scorecard.check_gold(self.gold)))


if __name__ == "__main__":
    unittest.main()
