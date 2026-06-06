#!/usr/bin/env python3
"""
Generate the structured references tree the way the best open source playbooks do it.
Reads data/rejection-patterns.json and docs/BY-APP-TYPE.md and writes:
  references/rules/<category>.md        one structured file per rule category
  references/guidelines/by-app-type/<slug>.md   one file per app type
  references/README.md                  the index
Source of truth stays the JSON and the by-app-type doc. Re-run after either changes.
"""

import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATTERNS = os.path.join(ROOT, "data", "rejection-patterns.json")
BY_APP_TYPE = os.path.join(ROOT, "docs", "BY-APP-TYPE.md")
REF = os.path.join(ROOT, "references")
RULES_DIR = os.path.join(REF, "rules")
BAT_DIR = os.path.join(REF, "guidelines", "by-app-type")

CATEGORIES = [
    (
        "metadata",
        "Metadata and store listing",
        (
            "2.3",
            "5.2.5",
            "2.3.4",
            "METADATA",
            "CROSS-PLATFORM",
            "FUTURE",
            "NEGATIVE",
            "UNREACHABLE",
            "AGE-RATING",
            "CHINA",
        ),
    ),
    (
        "privacy",
        "Privacy and data",
        (
            "5.1.1",
            "5.1.2",
            "PRIVACY",
            "ATT",
            "ACCOUNT-DELETION",
            "USAGE-DESCRIPTION",
            "UNNECESSARY",
            "FINGERPRINT",
            "AI-NO-CONSENT",
            "MANIFEST",
        ),
    ),
    (
        "payments",
        "Payments, in app purchase, subscriptions",
        (
            "3.1",
            "PLAY-BILLING",
            "EXTERNAL-PAYMENT",
            "RESTORE",
            "MISLEADING-PRICING",
            "LOOTBOX",
            "PHYSICAL",
        ),
    ),
    (
        "design",
        "Design and login",
        ("4.0", "4.2", "4.3", "4.8", "SIWA", "WEB-WRAPPER", "SOCIAL-LOGIN"),
    ),
    (
        "performance",
        "Performance and completeness",
        (
            "2.1",
            "2.5",
            "STAGING",
            "PLACEHOLDER",
            "DEBUG",
            "CLOUD",
            "REVIEW-NOTES",
            "PRIVATE-API",
        ),
    ),
    ("entitlements", "Entitlements", ("ENTITLEMENT",)),
    ("safety", "Safety and user generated content", ("1.2", "UGC", "AI-GENERATED")),
    ("android", "Google Play specific", ("GOOGLE", "ANDROID")),
    ("export", "Export and build", ("EXPORT-COMPLIANCE",)),
]


def categorize(p):
    pid = p.get("id", "")
    gl = str(p.get("guideline", ""))
    hay = (pid + " " + gl).upper()
    for slug, _title, keys in CATEGORIES:
        for k in keys:
            if k.upper() in hay:
                return slug
    if p.get("platform") == "google":
        return "android"
    return "performance"


def esc(s):
    return (s or "").strip()


def load_recipes():
    path = os.path.join(ROOT, "data", "detection-recipes.json")
    try:
        return json.load(open(path)).get("recipes", {})
    except Exception:
        return {}


def write_rules():
    data = json.load(open(PATTERNS))
    patterns = data["patterns"]
    recipes = load_recipes()
    buckets = {slug: [] for slug, _t, _k in CATEGORIES}
    for p in patterns:
        buckets.setdefault(categorize(p), []).append(p)
    os.makedirs(RULES_DIR, exist_ok=True)
    titles = {slug: t for slug, t, _k in CATEGORIES}
    written = []
    for slug, _t, _k in CATEGORIES:
        items = buckets.get(slug, [])
        if not items:
            continue
        lines = [f"# Rules. {titles[slug]}", ""]
        lines.append(
            f"{len(items)} rules in this category. Generated from data/rejection-patterns.json. Each rule names the guideline, the severity, what triggers it, and the fix."
        )
        lines.append("")
        for p in sorted(
            items,
            key=lambda x: {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(
                x.get("severity"), 9
            ),
        ):
            lines.append(f"## {p['id']}")
            lines.append("")
            lines.append(f"- Title. {esc(p.get('title'))}")
            lines.append(f"- Platform. {esc(p.get('platform'))}")
            lines.append(f"- Guideline or policy. {esc(p.get('guideline'))}")
            lines.append(f"- Severity. {esc(p.get('severity'))}")
            lines.append(f"- What triggers it. {esc(p.get('detection'))}")
            lines.append(f"- How to fix it. {esc(p.get('fix'))}")
            sig = p.get("signals") or []
            if sig:
                lines.append(f"- Detection signals. {', '.join(sig)}")
            cs = p.get("counterSignals") or []
            if cs:
                lines.append(f"- Present means handled. {', '.join(cs)}")
            cmd = recipes.get(p["id"])
            if cmd:
                lines.append("")
                lines.append("How to detect.")
                lines.append("")
                lines.append("```bash")
                lines.append(cmd)
                lines.append("```")
            lines.append("")
        path = os.path.join(RULES_DIR, f"{slug}.md")
        open(path, "w").write("\n".join(lines))
        written.append((slug, titles[slug], len(items)))
    return written


def write_by_app_type():
    os.makedirs(BAT_DIR, exist_ok=True)
    text = open(BY_APP_TYPE).read()
    # split on H2 sections
    parts = re.split(r"\n## ", text)
    written = []
    for part in parts[1:]:
        head, _, body = part.partition("\n")
        title = head.strip()
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        if not slug:
            continue
        content = f"# {title}\n\n{body.strip()}\n"
        open(os.path.join(BAT_DIR, f"{slug}.md"), "w").write(content)
        written.append((slug, title))
    return written


def write_index(rule_files, app_types):
    os.makedirs(REF, exist_ok=True)
    lines = [
        "# References",
        "",
        "A structured, AI loadable reference tree. Load the rule category and the app type that match the task, then check the project against them. Generated by scripts/generate-references.py from the rejection pattern taxonomy and the by app type map.",
        "",
        "## Rules by category",
        "",
    ]
    for slug, title, n in rule_files:
        lines.append(f"- [rules/{slug}.md](rules/{slug}.md). {title}. {n} rules")
    lines += ["", "## Guidelines by app type", ""]
    for slug, title in app_types:
        lines.append(
            f"- [guidelines/by-app-type/{slug}.md](guidelines/by-app-type/{slug}.md). {title}"
        )
    lines += [
        "",
        "## How an AI agent should use this",
        "",
        "1. Identify the app type and load the matching by app type file.",
        "2. Load the rule categories relevant to what the app does.",
        "3. Check the project and the live metadata against every rule, ranked by severity.",
        "4. Report findings with the guideline, the fix, and a clear verdict.",
        "",
        "Full context beats a checklist. Loading the right slices of this tree gives the agent what it needs to decide.",
        "",
    ]
    open(os.path.join(REF, "README.md"), "w").write("\n".join(lines))


if __name__ == "__main__":
    rf = write_rules()
    at = write_by_app_type()
    write_index(rf, at)
    print(f"generated {len(rf)} rule categories, {len(at)} app type files")
    for slug, title, n in rf:
        print(f"  rules/{slug}.md  ({n})")
    for slug, title in at:
        print(f"  by-app-type/{slug}.md")
