#!/usr/bin/env python3
"""Fleet Sweep treats malformed register attestations as blockers."""
from datetime import date
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("fleet", Path(__file__).with_name("fleet-sweep.py"))
fleet = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fleet)


class AttestationValidation(unittest.TestCase):
    def test_attestation_fields_require_typed_evidence(self):
        row = {"revision": 1, "proof_items": ["owner-1"], "jurisdiction": "US"}
        today = date(2026, 11, 5)
        attestation = {"attested_by": "Reviewer", "attested_on": "2026-10-01", "evidence": "Fixture", "outcome": "compliant",
                       "revision": 1, "covers": ["owner-1"], "regions": ["US"]}
        self.assertEqual(fleet.attestation_problem(attestation, row, ["US"], today), "")
        for field, value in (("revision", True), ("revision", 1.0),
                             ("covers", ["owner-1", {}]), ("regions", ["US", []])):
            with self.subTest(field=field, value=value):
                problem = fleet.attestation_problem({**attestation, field: value}, row, ["US"], today)
                self.assertIn(field, problem)


if __name__ == "__main__":
    unittest.main()
