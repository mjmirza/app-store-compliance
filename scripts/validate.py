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

DEADLINE_REQUIRED = [
    "jurisdiction", "law", "requirement", "effective_date",
    "grace_period", "mandatory_date", "enforcement_date",
    "affected_repository_sections", "priority"
]
DEADLINE_PRIORITIES = {"critical", "high", "medium", "low"}

errors = []
warnings = []

def validate_date(date_str, field, law):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        errors.append(f"Deadline for law '{law}' has invalid date format in {field}: '{date_str}'. Expected YYYY-MM-DD.")

def main():
    # Validate deadlines
    if not os.path.exists(DEADLINES):
        errors.append("regulatory-deadlines.json not found")
    else:
        try:
            dl_data = json.load(open(DEADLINES))
            deadlines = dl_data.get("deadlines", [])
            for dl in deadlines:
                law_name = dl.get("law", "<no law>")
                for f in DEADLINE_REQUIRED:
                    if f not in dl:
                        errors.append(f"Deadline for law '{law_name}' missing field: {f}")
                priority = dl.get("priority", "").lower()
                if priority not in DEADLINE_PRIORITIES:
                    errors.append(f"Deadline for law '{law_name}' has invalid priority: '{priority}'")

                # Validate date fields format
                if "effective_date" in dl:
                    validate_date(dl["effective_date"], "effective_date", law_name)
                if "mandatory_date" in dl:
                    validate_date(dl["mandatory_date"], "mandatory_date", law_name)
                if "enforcement_date" in dl:
                    validate_date(dl["enforcement_date"], "enforcement_date", law_name)

                # Validate affected repository sections exist
                if "affected_repository_sections" in dl:
                    sections = dl["affected_repository_sections"]
                    if not isinstance(sections, list):
                        errors.append(f"Deadline for law '{law_name}': affected_repository_sections must be a list")
                    else:
                        for s in sections:
                            if not os.path.exists(os.path.join(ROOT, s)):
                                errors.append(f"Deadline for law '{law_name}': affected section path does not exist: '{s}'")
        except Exception as e:
            errors.append(f"Failed to parse regulatory-deadlines.json: {e}")

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
