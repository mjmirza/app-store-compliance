#!/usr/bin/env python3
"""Ruling Register. Validates, queries and exports release requirements with their legal standing. See docs/RULING-REGISTER.md."""

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REGISTER = REPO / "data" / "ruling-register.json"
PATTERNS = REPO / "data" / "rejection-patterns.json"
STANDINGS = ("in_force", "in_force_later", "store_policy", "proposed", "guidance")
PROOFS = ("automated", "mixed", "owner_attested")
STORES = ("apple", "google")
FEATURES = (
    "lending",
    "crypto",
    "medical",
    "generative_ai",
    "personal_data",
    "subscriptions",
    "social",
    "marketplace",
    "children",
)
EU = {
    "AT",
    "BE",
    "BG",
    "HR",
    "CY",
    "CZ",
    "DK",
    "EE",
    "FI",
    "FR",
    "DE",
    "GR",
    "HU",
    "IE",
    "IT",
    "LV",
    "LT",
    "LU",
    "MT",
    "NL",
    "PL",
    "PT",
    "RO",
    "SK",
    "SI",
    "ES",
    "SE",
}
ID = re.compile(r"^RR-[A-Z0-9-]+$")
ITEM = re.compile(r"^[a-z0-9-]+$")
COUNTRY = re.compile(r"^[A-Z]{2}$")
SUPPORTS = ("obligation", "date")


def text(v):
    return isinstance(v, str) and v.strip() != ""


def is_date(v):
    try:
        dt.date.fromisoformat(v)
        return True
    except (TypeError, ValueError):
        return False


def verified(req):
    """True only when quoted sources support the obligation, and the start date if the rule has one."""
    covered = set()
    for s in req.get("sources", []):
        if isinstance(s, dict) and text(s.get("quote")) and isinstance(s.get("supports"), list):
            covered |= set(s["supports"])
    needed = {"obligation"} | ({"date"} if req.get("takes_effect") else set())
    return needed <= covered


def validate(doc, pattern_ids):
    """Returns a list of problems. Empty means the register is sound."""
    errors = []
    if (
        not isinstance(doc, dict)
        or not text(doc.get("register_version"))
        or not isinstance(doc.get("requirements"), list)
    ):
        return ["the register needs register_version and a requirements list"]
    if not re.fullmatch(r"\d+\.\d+\.\d+", doc["register_version"]):
        errors.append("register_version must look like 1.2.3")
    seen = set()
    for i, r in enumerate(doc["requirements"]):
        where = f"requirements[{i}]"
        if not isinstance(r, dict):
            errors.append(f"{where} is not an object")
            continue
        rid = r.get("id")
        where = rid if text(rid) else where
        if not (text(rid) and ID.match(rid)):
            errors.append(f"{where}. id must look like RR-SOMETHING")
        elif rid in seen:
            errors.append(f"{rid}. id is used twice, a new rule gets a new id")
        seen.add(rid)
        rev = r.get("revision")
        if not isinstance(rev, int) or isinstance(rev, bool) or rev < 1:
            errors.append(f"{where}. revision must be a whole number from 1, raise it when the rule changes")
        for key in ("title", "jurisdiction", "instrument", "authority", "check"):
            if not text(r.get(key)):
                errors.append(f"{where}. {key} is missing")
        if r.get("standing") not in STANDINGS:
            errors.append(f"{where}. standing must be one of {', '.join(STANDINGS)}")
        eff = r.get("takes_effect")
        if eff is not None and not is_date(eff):
            errors.append(f"{where}. takes_effect must be YYYY-MM-DD or null")
        if r.get("standing") == "in_force_later" and eff is None:
            errors.append(f"{where}. in_force_later needs a takes_effect date")
        if r.get("store") not in (None,) + STORES:
            errors.append(f"{where}. store must be apple, google or null")
        feats = r.get("features")
        if not isinstance(feats, list) or any(f not in FEATURES for f in feats):
            errors.append(
                f"{where}. features must be a list drawn from {', '.join(FEATURES)}"
            )
        items = r.get("proof_items")
        if not isinstance(items, list) or not items:
            errors.append(f"{where}. proof_items needs at least one item")
            items = []
        hows = set()
        for item in items:
            if (
                not isinstance(item, dict)
                or not text(item.get("what"))
                or item.get("how") not in ("automated", "owner_attested")
            ):
                errors.append(
                    f"{where}. each proof item needs what and how (automated or owner_attested)"
                )
            elif not (text(item.get("id")) and ITEM.match(item["id"])):
                errors.append(f"{where}. each proof item needs a lowercase id")
            else:
                hows.add(item["how"])
        item_ids = [it.get("id") for it in items if isinstance(it, dict)]
        if len(item_ids) != len(set(item_ids)):
            errors.append(f"{where}. proof item ids must be unique")
        proof = r.get("proof")
        if proof not in PROOFS:
            errors.append(f"{where}. proof must be one of {', '.join(PROOFS)}")
        elif hows and proof == "mixed" and hows != {"automated", "owner_attested"}:
            errors.append(
                f"{where}. mixed proof needs one automated and one owner_attested item"
            )
        elif hows and proof != "mixed" and hows != {proof}:
            errors.append(f"{where}. every proof item must be {proof}")
        sources = r.get("sources")
        if not isinstance(sources, list) or not sources:
            errors.append(f"{where}. needs at least one source")
            sources = []
        for s in sources:
            if (
                not isinstance(s, dict)
                or not text(s.get("url"))
                or not s["url"].startswith("https://")
            ):
                errors.append(f"{where}. each source needs an https url")
                continue
            if not is_date(s.get("checked_on")):
                errors.append(f"{where}. source {s['url']} needs checked_on")
            if text(s.get("quote")) == text(s.get("unverified")):
                errors.append(
                    f"{where}. source {s['url']} needs exactly one of quote or unverified"
                )
            sup = s.get("supports")
            if not isinstance(sup, list) or not sup or any(x not in SUPPORTS for x in sup):
                errors.append(f"{where}. source {s['url']} needs supports, drawn from {', '.join(SUPPORTS)}")
        for pid in r.get("pattern_ids", []):
            if pid not in pattern_ids:
                errors.append(
                    f"{where}. pattern_ids names {pid}, which is not in rejection-patterns.json"
                )
    return errors


def matches_region(req, regions):
    j = req["jurisdiction"]
    return j == "GLOBAL" or j in regions or (j == "EU" and bool(regions & EU))


def applies(req, regions, stores, features):
    if not matches_region(req, regions):
        return False
    if req.get("store") and req["store"] not in stores:
        return False
    return not req["features"] or bool(set(req["features"]) & features)


def blocking(req, today):
    """Only verified law or store policy that is in force today can block. Proposed or guidance never does."""
    if not verified(req):
        return False
    if req["standing"] in ("in_force", "store_policy"):
        return (
            req.get("takes_effect") is None
            or dt.date.fromisoformat(req["takes_effect"]) <= today
        )
    if req["standing"] == "in_force_later":
        return dt.date.fromisoformat(req["takes_effect"]) <= today
    return False


def due(doc, regions, stores, features, today):
    rows = []
    for r in doc["requirements"]:
        if not applies(r, regions, stores, features):
            continue
        rows.append(
            {
                "id": r["id"],
                "revision": r["revision"],
                "jurisdiction": r["jurisdiction"],
                "proof_items": [it["id"] for it in r["proof_items"]],
                "title": r["title"],
                "standing": r["standing"],
                "takes_effect": r.get("takes_effect"),
                "proof": r["proof"],
                "blocks_release": blocking(r, today),
                "source_verified": verified(r),
                "needs_attestation": True,
                "check": r["check"],
            }
        )
    return rows


def load(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        sys.exit(f"ruling-register. cannot read {path}. {exc}")


def pattern_ids():
    data = load(PATTERNS)
    return {p["id"] for p in data.get("patterns", [])}


def git_commit():
    try:
        return subprocess.run(
            ["git", "-C", str(REPO), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def csv_set(value):
    return {v.strip() for v in (value or "").split(",") if v.strip()}


def main():
    ap = argparse.ArgumentParser(
        description="Validate, query and export the Ruling Register."
    )
    ap.add_argument("--register", default=str(REGISTER))
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate")
    q = sub.add_parser(
        "due", help="what applies to an app and what blocks its release today"
    )
    q.add_argument(
        "--regions",
        required=True,
        help="comma list of ISO country codes, for example DE,AU,US",
    )
    q.add_argument("--stores", default="apple,google")
    q.add_argument(
        "--features", default="", help=f"comma list from {', '.join(FEATURES)}"
    )
    q.add_argument("--json", action="store_true")
    e = sub.add_parser(
        "export", help="write a versioned, commit-stamped copy for other tools"
    )
    e.add_argument("--out-dir", default=str(REPO / "exports"))
    args = ap.parse_args()

    doc = load(args.register)
    problems = validate(doc, pattern_ids())
    if args.cmd == "validate" or problems:
        for p in problems:
            print(f"  ERROR. {p}")
        unverified = [
            r["id"]
            for r in doc.get("requirements", [])
            if isinstance(r, dict) and not verified(r)
        ]
        for rid in unverified:
            print(
                f"  NOTE. {rid} is not fully verified (its obligation, and its start date if it has one, need a quoted source), so it can never block a release"
            )
        print(
            f"ruling-register. {'FAILED' if problems else 'OK'}. {len(doc.get('requirements', []))} requirements, {len(problems)} error(s)"
        )
        return 1 if problems else 0

    today = dt.date.today()
    if args.cmd == "due":
        features = csv_set(args.features)
        bad = features - set(FEATURES)
        if bad:
            print(
                f"ruling-register. unknown features {', '.join(sorted(bad))}",
                file=sys.stderr,
            )
            return 1
        rows = due(
            doc,
            {r.upper() for r in csv_set(args.regions)},
            csv_set(args.stores),
            features,
            today,
        )
        if args.json:
            print(json.dumps(rows, indent=2, ensure_ascii=False))
            return 0
        for row in rows:
            tag = (
                "BLOCKS"
                if row["blocks_release"]
                else ("CONFIRM-SOURCE" if not row["source_verified"] else "WATCH")
            )
            print(f"{tag:<15} {row['id']}  {row['title']}")
            if row["needs_attestation"]:
                print(
                    "    needs your attestation. No finding is not the same as a pass."
                )
        print(
            f"\n{len(rows)} requirements apply, {sum(r['blocks_release'] for r in rows)} block release today."
        )
        return 0

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    stamped = {
        "register_version": doc["register_version"],
        "source_commit": git_commit(),
        "exported_on": str(today),
        "license": "See LICENSE in mjmirza/app-store-compliance",
        "requirements": doc["requirements"],
    }
    path = out / f"ruling-register-v{doc['register_version']}.json"
    path.write_text(
        json.dumps(stamped, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"exported {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
