#!/usr/bin/env python3
"""
Validate the data files and their consistency. Run in CI and before any release.
Checks:
  1. rejection-patterns.json is well formed and every pattern has required fields.
  2. pattern ids are unique, severity and platform are from the allowed sets.
  3. every detection recipe key maps to a real pattern id (no dead recipes).
  4. reports automatable-looking patterns that have no recipe yet (info only).
Exit code 0 on pass, 1 on any error.
"""
import json, os, sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATTERNS = os.path.join(ROOT, "data", "rejection-patterns.json")
RECIPES = os.path.join(ROOT, "data", "detection-recipes.json")
DEADLINES = os.path.join(ROOT, "data", "regulatory-deadlines.json")

REQUIRED = ["id", "platform", "guideline", "title", "severity", "detection", "fix"]
SEVERITIES = {"critical", "high", "medium", "low"}
PLATFORMS = {"apple", "google", "both"}

errors = []
warnings = []

def main():
    data = json.load(open(PATTERNS))
    patterns = data.get("patterns", [])
    if not patterns:
        errors.append("rejection-patterns.json has no patterns")
        return finish()

    ids = set()
    for p in patterns:
        pid = p.get("id", "<no id>")
        for f in REQUIRED:
            if not p.get(f):
                errors.append(f"{pid} missing required field {f}")
        if pid in ids:
            errors.append(f"duplicate pattern id {pid}")
        ids.add(pid)
        if p.get("severity") not in SEVERITIES:
            errors.append(f"{pid} has invalid severity {p.get('severity')}")
        if p.get("platform") not in PLATFORMS:
            errors.append(f"{pid} has invalid platform {p.get('platform')}")

    recipes = json.load(open(RECIPES)).get("recipes", {})
    for rid in recipes:
        if rid not in ids:
            errors.append(f"detection recipe '{rid}' has no matching pattern id, it will never surface")

    with_recipe = set(recipes.keys())
    for p in patterns:
        sig = p.get("signals")
        if sig and p["id"] not in with_recipe:
            warnings.append(f"{p['id']} has detection signals but no recipe command yet")

    # Validate regulatory-deadlines.json
    if not os.path.exists(DEADLINES):
        errors.append("regulatory-deadlines.json is missing")
    else:
        try:
            with open(DEADLINES, "r", encoding="utf-8") as f:
                deadlines_data = json.load(f)
            if not isinstance(deadlines_data, list):
                errors.append("regulatory-deadlines.json is not a JSON list")
            else:
                required_deadline_fields = [
                    "jurisdiction", "law", "requirement", "effective_date",
                    "grace_period", "mandatory_date", "enforcement_date",
                    "affected_repository_sections", "priority"
                ]
                for idx, dl in enumerate(deadlines_data):
                    dl_desc = dl.get("law", f"index {idx}")
                    for fld in required_deadline_fields:
                        if fld not in dl:
                            errors.append(f"Deadline '{dl_desc}' is missing field '{fld}'")
                        elif dl[fld] is None or dl[fld] == "":
                            if fld in ["jurisdiction", "law", "requirement", "priority"]:
                                errors.append(f"Deadline '{dl_desc}' has empty required field '{fld}'")

                    # Validate priority value
                    prio = dl.get("priority")
                    if prio and prio not in SEVERITIES:
                        errors.append(f"Deadline '{dl_desc}' has invalid priority '{prio}'")

                    # Validate date formats
                    for date_fld in ["effective_date", "mandatory_date", "enforcement_date"]:
                        d_val = dl.get(date_fld)
                        if d_val:
                            try:
                                datetime.strptime(d_val, "%Y-%m-%d")
                            except ValueError:
                                errors.append(f"Deadline '{dl_desc}' has invalid '{date_fld}' format: '{d_val}' (must be YYYY-MM-DD)")

                    # Validate affected repo sections
                    sections = dl.get("affected_repository_sections")
                    if isinstance(sections, list):
                        for sec in sections:
                            sec_path = os.path.join(ROOT, sec)
                            if not os.path.exists(sec_path):
                                errors.append(f"Deadline '{dl_desc}' references non-existent repository section '{sec}'")
                    elif sections is not None:
                        errors.append(f"Deadline '{dl_desc}' 'affected_repository_sections' is not a list")
        except Exception as ex:
            errors.append(f"Failed to parse regulatory-deadlines.json: {ex}")

    return finish(len(patterns), len(recipes))

def finish(npat=0, nrec=0):
    for w in warnings:
        print(f"  warn. {w}")
    for e in errors:
        print(f"  ERROR. {e}")
    if errors:
        print(f"\nvalidate. FAILED with {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"validate. OK. {npat} patterns, {nrec} recipes, {len(warnings)} warning(s), 0 errors")
    return 0

if __name__ == "__main__":
    sys.exit(main())
