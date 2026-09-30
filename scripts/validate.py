#!/usr/bin/env python3
"""Validates patterns/recipes/deadlines data files for CI. Exit 0 on
pass, 1 on error; see README.md and AGENTS.md for the check list."""

import json
import os
import re
import sys
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATTERNS = os.path.join(ROOT, "data", "rejection-patterns.json")
RECIPES = os.path.join(ROOT, "data", "detection-recipes.json")
DEADLINES = os.environ.get(
    "DEADLINES_FILE", os.path.join(ROOT, "data", "regulatory-deadlines.json")
)
# a passed deadline with no absorbed_into is a warning for this many days, then an error
PASSED_GRACE_DAYS = 7

REQUIRED_PATTERN = [
    "id",
    "platform",
    "guideline",
    "title",
    "severity",
    "detection",
    "fix",
]
SEVERITIES = {"critical", "high", "medium", "low"}
PLATFORMS = {"apple", "google", "both", "web"}

REQUIRED_DEADLINE = [
    "id",
    "jurisdiction",
    "law",
    "requirement",
    "effective_date",
    "grace_period",
    "mandatory_date",
    "enforcement_date",
    "affected_repository_sections",
    "priority",
]

errors = []
warnings = []


def validate_date(date_str, field_name, item_id):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        errors.append(
            f"deadline '{item_id}' has invalid {field_name} '{date_str}', must be YYYY-MM-DD format"
        )


def parse_day(value):
    try:
        return datetime.datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


SECTION_PATH = re.compile(
    r"(?:docs|references|data|scripts|agent-os|templates)/[A-Za-z0-9_./-]+\.(?:md|json|py|sh)"
)


def validate_section_paths(d, did):
    """Every file named in affected_repository_sections must exist in the repo."""
    for path in SECTION_PATH.findall(str(d.get("affected_repository_sections") or "")):
        if not os.path.exists(os.path.join(ROOT, path)):
            errors.append(f"deadline '{did}' points at {path}, which does not exist")


def validate_deadline_dates(d, did, today):
    """Date order, and an owner for a deadline that has passed (#660)."""
    eff, mand, enf = (
        parse_day(d.get(k)) for k in ("effective_date", "mandatory_date", "enforcement_date")
    )
    if eff and mand and eff > mand:
        errors.append(
            f"deadline '{did}' has effective_date {eff} after mandatory_date {mand}"
        )
    if mand and enf and mand > enf:
        errors.append(
            f"deadline '{did}' has mandatory_date {mand} after enforcement_date {enf}"
        )
    if mand and mand < today and not str(d.get("absorbed_into") or "").strip():
        days = (today - mand).days
        msg = (
            f"deadline '{did}' passed {days} day(s) ago on {mand} with no absorbed_into. "
            "Name the doc section that now carries the rule."
        )
        if days > PASSED_GRACE_DAYS:
            errors.append(msg)
        else:
            warnings.append(msg)


def main():
    # 1. Validate rejection patterns
    if not os.path.exists(PATTERNS):
        errors.append(f"File not found: {PATTERNS}")
        return finish()

    try:
        data = json.load(open(PATTERNS))
    except Exception as e:
        errors.append(f"Failed to parse rejection-patterns.json: {e}")
        return finish()

    patterns = data.get("patterns", [])
    if not patterns:
        errors.append("rejection-patterns.json has no patterns")
    else:
        ids = set()
        for p in patterns:
            pid = p.get("id", "<no id>")
            for f in REQUIRED_PATTERN:
                if not p.get(f):
                    errors.append(f"{pid} missing required field {f}")
            if pid in ids:
                errors.append(f"duplicate pattern id {pid}")
            ids.add(pid)
            if p.get("severity") not in SEVERITIES:
                errors.append(f"{pid} has invalid severity {p.get('severity')}")
            if p.get("platform") not in PLATFORMS:
                errors.append(f"{pid} has invalid platform {p.get('platform')}")

    # 2. Validate recipes
    if os.path.exists(RECIPES):
        try:
            recipes = json.load(open(RECIPES)).get("recipes", {})
            for rid in recipes:
                if rid not in ids:
                    errors.append(
                        f"detection recipe '{rid}' has no matching pattern id, it will never surface"
                    )

            with_recipe = set(recipes.keys())
            for p in patterns:
                sig = p.get("signals")
                if sig and p["id"] not in with_recipe:
                    warnings.append(
                        f"{p['id']} has detection signals but no recipe command yet"
                    )
        except Exception as e:
            errors.append(f"Failed to parse detection-recipes.json: {e}")
    else:
        warnings.append("detection-recipes.json not found")

    # 3. Validate regulatory deadlines
    if not os.path.exists(DEADLINES):
        errors.append(f"File not found: {DEADLINES}")
    else:
        try:
            deadline_data = json.load(open(DEADLINES))
            deadlines = deadline_data.get("deadlines", [])
            if not deadlines:
                errors.append("regulatory-deadlines.json has no deadlines list")
            else:
                deadline_ids = set()
                for d in deadlines:
                    did = d.get("id", "<no id>")
                    if not did or did == "<no id>":
                        errors.append("deadline entry missing 'id' field")
                    elif did in deadline_ids:
                        errors.append(f"duplicate deadline id '{did}'")
                    deadline_ids.add(did)

                    for f in REQUIRED_DEADLINE:
                        if f not in d or d[f] is None:
                            errors.append(
                                f"deadline '{did}' missing required field '{f}'"
                            )

                    validate_section_paths(d, did)
                    if d.get("priority") not in SEVERITIES:
                        errors.append(
                            f"deadline '{did}' has invalid priority '{d.get('priority')}'"
                        )

                    # Validate date formats
                    for date_field in [
                        "effective_date",
                        "mandatory_date",
                        "enforcement_date",
                    ]:
                        val = d.get(date_field)
                        if val and val != "none":
                            validate_date(val, date_field, did)
                    validate_deadline_dates(
                        d, did, datetime.datetime.now(datetime.timezone.utc).date()
                    )
        except Exception as e:
            errors.append(f"Failed to parse regulatory-deadlines.json: {e}")

    return finish(
        len(patterns),
        len(recipes) if "recipes" in locals() else 0,
        len(deadlines) if "deadlines" in locals() else 0,
    )


def finish(npat=0, nrec=0, ndead=0):
    for w in warnings:
        print(f"  warn. {w}")
    for e in errors:
        print(f"  ERROR. {e}")
    if errors:
        print(
            f"\nvalidate. FAILED with {len(errors)} error(s), {len(warnings)} warning(s)"
        )
        return 1
    print(
        f"validate. OK. {npat} patterns, {nrec} recipes, {ndead} deadlines, {len(warnings)} warning(s), 0 errors"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
