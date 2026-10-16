#!/usr/bin/env python3
"""
Metadata audit + autofix for App Store Connect and Google Play listings.

This is the live-listing layer. A large share of rejections live in the store
metadata (name, subtitle, keywords, description, promotional text, review notes,
URLs), not the code. This tool audits a pulled metadata directory or explicit
fields against the metadata-class rejection patterns, then can propose fixes and
re-validate.

Pull the metadata first (Apple):
    brew install asc
    asc metadata pull --app "<APP_ID>" --version "<VERSION>" --dir ./metadata
Or point at a fastlane metadata/ directory. Google Play metadata can be exported
from the Play Console or the Play Developer API and placed in the same dir.

Usage:
    metadata-audit.py <metadata-dir>            audit a directory
    metadata-audit.py --name "..." --keywords "..." --description "..."   audit fields
    metadata-audit.py <dir> --propose           write <dir>/.metadata-fixes.md with suggested fixes
    metadata-audit.py <dir> --check-urls        also HEAD-check URLs (needs network)
    metadata-audit.py <dir> --platform google   use the Google Play limits and rules (default apple)

Every locale folder is audited on its own and each finding names its locale.
A folder named android in the path is audited with the Google rules unless
--platform is given.

Exit codes: 0 clean or advisory, 1 the directory held nothing to audit, 2 a critical finding.
"""

import itertools
import os
import sys
import re
import json
import glob
from urllib.parse import urlparse

FIELD_LIMITS = {
    "name": 30,
    "subtitle": 30,
    "keywords": 100,
    "promotional_text": 170,
    "description": 4000,
}
# Google Play listing limits, verified 2026-10-15 at support.google.com/googleplay/android-developer/answer/9859152
GOOGLE_FIELD_LIMITS = {"name": 30, "short_description": 80, "description": 4000}
PLATFORMS = ("apple", "google")
APPLE_STD_EULA = "apple.com/legal/internet-services/itunes/dev/stdeula"
URL_FIELDS = ("privacy_url", "support_url", "marketing_url", "terms_url")
# fastlane / asc field file name aliases -> canonical field
ALIASES = {
    "name": "name",
    "title": "name",
    "app_name": "name",
    "subtitle": "subtitle",
    "keywords": "keywords",
    "description": "description",
    "full_description": "description",
    "promotional_text": "promotional_text",
    "promo_text": "promotional_text",
    "short_description": "promotional_text",
    "release_notes": "release_notes",
    "whats_new": "release_notes",
    "review_notes": "review_notes",
    "notes": "review_notes",
    "privacy_url": "privacy_url",
    "privacy_policy_url": "privacy_url",
    "support_url": "support_url",
    "marketing_url": "marketing_url",
    "terms_url": "terms_url",
    "eula_url": "terms_url",
    "license_agreement_url": "terms_url",
    "contact_email": "contact_email",
    "email": "contact_email",
}
# On Google Play short_description is its own 80 char field, not Apple promotional text.
GOOGLE_ALIASES = dict(ALIASES, short_description="short_description")

OTHER_PLATFORMS = [
    "android",
    "google play",
    "play store",
    "windows phone",
    "blackberry",
]
FUTURE = [
    "coming soon",
    "coming-soon",
    "will be available",
    "in a future update",
    "stay tuned",
    "future release",
]
NEGATIVE_APPLE = ["ios bug", "apple bug", "broken on ios", "fix for ios bug"]
PLACEHOLDER = [
    "lorem ipsum",
    "placeholder",
    "todo",
    "fixme",
    "test data",
    "dummy",
    "example.com",
]
CHINA_AI = ["chatgpt", "openai", "gemini", "claude", "anthropic", "copilot"]
RANKING = ["#1", "number one", "best app", "top app", "free", "no.1", "no. 1"]
# small safe profanity sample; teams extend in their own config
CURSE = ["fuck", "shit", "asshole", "bitch", "bastard"]


def add(findings, sev, rule, field, msg, fix):
    findings.append(
        {"severity": sev, "rule": rule, "field": field, "message": msg, "fix": fix}
    )


def url_syntax_ok(u):
    """True when u is an http or https URL with a host."""
    u = (u or "").strip()
    try:
        p = urlparse(u)
        host = p.hostname
    except ValueError:
        return False
    return p.scheme in ("http", "https") and bool(host) and " " not in u


def is_terms_url(u):
    low = (u or "").lower()
    if not url_syntax_ok(low):
        return False
    p = urlparse(low)
    # Apple's standard EULA counts only as that page itself, never as text inside another URL.
    if p.netloc in ("apple.com", "www.apple.com") and p.path.startswith("/" + APPLE_STD_EULA.split("/", 1)[1]):
        return True
    if "privacy" in p.path:
        return False
    return bool(
        re.search(
            r"(^|[^a-z])(terms|eula|conditions|licen[cs]e)|(^|[^a-z])(tos|agb|legal)([^a-z]|$)",
            p.path,
        )
    )


def has_emoji(s):
    for ch in s:
        o = ord(ch)
        if (
            0x1F000 <= o <= 0x1FAFF
            or 0x2600 <= o <= 0x27BF
            or 0x2190 <= o <= 0x21FF
            or o in (0x2122, 0x2B50, 0xFE0F)
        ):
            return True
    return False


def lc(s):
    return (s or "").lower()


def audit_fields(fields, check_urls=False, platform="apple"):
    findings = []
    apple = platform == "apple"
    name = fields.get("name", "")
    subtitle = fields.get("subtitle", "")
    keywords = fields.get("keywords", "")

    # char limits
    for f, limit in (FIELD_LIMITS if apple else GOOGLE_FIELD_LIMITS).items():
        v = fields.get(f, "")
        if v and len(v) > limit:
            add(
                findings,
                "high",
                "BOTH-METADATA-DECORATION",
                f,
                f"{f} is {len(v)} chars, over the {limit} limit",
                f"Trim {f} to {limit} characters or fewer",
            )

    # decoration in name / subtitle
    for f in ("name", "subtitle"):
        v = fields.get(f, "")
        if v and has_emoji(v):
            add(
                findings,
                "medium",
                "BOTH-METADATA-DECORATION",
                f,
                f"{f} contains an emoji",
                f"Remove emoji from {f}",
            )
        for r in RANKING:
            if r in lc(v):
                add(
                    findings,
                    "high",
                    "BOTH-METADATA-DECORATION",
                    f,
                    f"{f} contains a ranking or price claim ({r})",
                    f"Remove ranking and price claims from {f}",
                )
        words = [w for w in re.findall(r"[A-Za-z]{3,}", v) if w.isupper()]
        if len(words) >= 2:
            add(
                findings,
                "medium",
                "BOTH-METADATA-DECORATION",
                f,
                f"{f} uses ALL CAPS words",
                f"Use normal case in {f} except a real brand",
            )

    # other platform mentions (Apple side only, an Android listing may say Android)
    for f, v in fields.items() if apple else ():
        for term in OTHER_PLATFORMS:
            if term in lc(v):
                add(
                    findings,
                    "high",
                    "APPLE-2.3-CROSS-PLATFORM-REFERENCE",
                    f,
                    f"{f} mentions another platform ({term})",
                    f"Remove the reference to {term} from {f}",
                )

    # future functionality
    for f, v in fields.items() if apple else ():
        for term in FUTURE:
            if term in lc(v):
                add(
                    findings,
                    "medium",
                    "APPLE-2.3-FUTURE-FUNCTIONALITY",
                    f,
                    f"{f} promises future functionality ({term})",
                    "Describe only what the build does today",
                )

    # negative apple sentiment
    for f, v in fields.items() if apple else ():
        for term in NEGATIVE_APPLE:
            if term in lc(v):
                add(
                    findings,
                    "medium",
                    "APPLE-2.3-NEGATIVE-APPLE-SENTIMENT",
                    f,
                    f"{f} references an iOS bug or Apple negatively",
                    "Remove negative Apple references",
                )

    # placeholder / test
    for f, v in fields.items():
        for term in PLACEHOLDER:
            if term in lc(v):
                add(
                    findings,
                    "high",
                    "BOTH-PLACEHOLDER",
                    f,
                    f"{f} contains placeholder text ({term})",
                    "Replace placeholder with real content",
                )

    # curse words
    for f, v in fields.items():
        for term in CURSE:
            if re.search(r"\b" + re.escape(term) + r"\b", lc(v)):
                add(
                    findings,
                    "high",
                    "APPLE-2.3-CURSE-WORD",
                    f,
                    f"{f} contains profanity",
                    "Remove profanity from the listing",
                )

    # keywords formatting (Apple only, Google Play has no keywords field)
    if keywords and apple:
        if ", " in keywords:
            add(
                findings,
                "low",
                "APPLE-2.3-KEYWORD-FORMAT",
                "keywords",
                "keywords field has spaces after commas, which wastes the 100 char budget",
                "Use commas with no spaces between keywords",
            )
        kw = set(w for w in re.split(r"[,\s]+", lc(keywords)) if w)
        dup = kw & set(re.findall(r"[a-z]{3,}", lc(name + " " + subtitle)))
        if dup:
            add(
                findings,
                "low",
                "APPLE-2.3-KEYWORD-FORMAT",
                "keywords",
                f"keywords repeat words already in name or subtitle ({', '.join(sorted(dup))})",
                "Drop duplicated words, the name and subtitle are already indexed",
            )

    # missing privacy policy url
    if not fields.get("privacy_url"):
        add(
            findings,
            "high",
            "BOTH-MISSING-PRIVACY-POLICY",
            "privacy_url",
            "no privacy policy URL found in the metadata",
            "Set the Privacy Policy URL in App Store Connect and the Play listing",
        )

    # URL fields must be real http or https URLs, checked before any network call
    for f in URL_FIELDS:
        v = fields.get(f, "")
        if v and not url_syntax_ok(v):
            add(
                findings,
                "high",
                "BOTH-INVALID-METADATA-URL",
                f,
                f"{f} is not an http or https URL with a host ({v[:60]})",
                f"Set {f} to a full https URL",
            )

    if apple and not fields.get("support_url"):
        add(
            findings,
            "high",
            "APPLE-MISSING-SUPPORT-URL",
            "support_url",
            "no support URL found in the metadata, App Store Connect requires one",
            "Set the Support URL in App Store Connect",
        )
    if not apple:
        email = fields.get("contact_email", "")
        if not email:
            add(
                findings,
                "medium",
                "GOOGLE-MISSING-CONTACT-EMAIL",
                "contact_email",
                "no contact email found, the Play listing requires one",
                "Set the contact email in the Play Console store listing",
            )
        elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email.strip()):
            add(
                findings,
                "medium",
                "GOOGLE-MISSING-CONTACT-EMAIL",
                "contact_email",
                f"contact email is not a valid address ({email[:60]})",
                "Set a working contact email in the Play Console",
            )

    # subscription terms, a real Terms or EULA URL is required, the word alone is not enough
    raw_desc = fields.get("description", "") + " " + fields.get("promotional_text", "")
    desc = lc(raw_desc)
    if apple and any(
        t in desc
        for t in ("subscription", "subscribe", "auto-renew", "per month", "per year")
    ):
        links = re.findall(
            r"https?://[^\s)\"']+|(?:www\.)?apple\.com/legal/[^\s)\"']+",
            fields.get("description", ""),
            re.IGNORECASE,
        )
        # Apple reads the link in the description itself, so promotional text or a terms_url field never replaces it.
        has_terms = any(is_terms_url(u) for u in links) and ("terms" in desc or "eula" in desc)
        if not has_terms:
            add(
                findings,
                "high",
                "APPLE-3.1.2-MISLEADING-PRICING",
                "description",
                "subscription mentioned but no Terms of Use or EULA link in the description",
                "Add functional Terms of Use and Privacy Policy links to the description and the paywall",
            )

    # china AI references (advisory, storefront dependent, Apple only)
    for f in ("name", "subtitle", "keywords", "description") if apple else ():
        v = lc(fields.get(f, ""))
        for term in CHINA_AI:
            if term in v:
                add(
                    findings,
                    "medium",
                    "CHINA-AI-REFERENCES",
                    f,
                    f"{f} references an external AI service ({term}), which can trigger a China storefront rejection",
                    "Remove or localize external AI references for the China storefront",
                )
                break

    # unreachable URLs
    if check_urls:
        urls = set()
        for v in fields.values():
            urls.update(re.findall(r"https?://[^\s)\"']+", v or ""))
        for u in sorted(u for u in urls if not url_syntax_ok(u)):
            add(
                findings,
                "high",
                "BOTH-UNREACHABLE-METADATA-URL",
                "url",
                f"URL is malformed: {u}",
                "Fix or remove the broken URL before submission",
            )
        for u in sorted(u for u in urls if url_syntax_ok(u)):
            ok = _url_ok(u)
            if ok is False:
                add(
                    findings,
                    "high",
                    "BOTH-UNREACHABLE-METADATA-URL",
                    "url",
                    f"URL does not load: {u}",
                    "Fix or remove the broken URL before submission",
                )

    return findings


def _url_ok(u):
    try:
        import urllib.request

        req = urllib.request.Request(
            u, method="HEAD", headers={"User-Agent": "metadata-audit"}
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            return 200 <= r.status < 400
    except Exception:
        return False


def _read_text(path):
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            return fh.read().strip()
    except Exception:
        return None


def _read_json(path):
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            return json.load(fh)
    except Exception:
        return None


def _read_group_files(d):
    """Return {folder relative to d: [(path, base or None, text or dict)]} for listing files."""
    groups = {}
    for path in sorted(glob.glob(os.path.join(d, "**", "*.txt"), recursive=True)):
        txt = _read_text(path)
        if txt is None:
            continue
        rel = os.path.relpath(os.path.dirname(path), d)
        groups.setdefault(rel, []).append(
            (path, os.path.splitext(os.path.basename(path))[0].lower(), txt)
        )
    for path in sorted(glob.glob(os.path.join(d, "**", "*.json"), recursive=True)):
        data = _read_json(path)
        if isinstance(data, dict):
            groups.setdefault(os.path.relpath(os.path.dirname(path), d), []).append(
                (path, None, data)
            )
    return groups


def group_platform(rel, root=None):
    # The root's own name and its parent count too, so metadata/android and metadata/android/en-US stay Google.
    parts = rel.split(os.sep)
    if root:
        parts = os.path.abspath(root).split(os.sep)[-2:] + parts
    return "google" if "android" in [p.lower() for p in parts] else "apple"


def _fields_from(entries, aliases, conflicts=None):
    """Two files for one field keep the longest value, as origin/main did, and the clash goes to conflicts."""
    fields, src = {}, {}
    for path, base, val in entries:
        pairs = (
            [(aliases.get(base), val)]
            if base is not None
            else [
                (aliases.get(str(k).lower()), v.strip() if isinstance(v, str) else "")
                for k, v in val.items()
            ]
        )
        for canon, v in pairs:
            if not canon or not v:
                continue
            name = os.path.basename(path)
            if canon in fields and fields[canon] != v:
                keep_old = len(v) <= len(fields[canon])
                if conflicts is not None:
                    conflicts.append((canon, src[canon], name, v if keep_old else fields[canon]))
                if keep_old:
                    continue
            fields[canon], src[canon] = v, name
    return fields


def _is_below(child, parent):
    return child != parent and (parent == "." or child.startswith(parent + os.sep))


NON_LOCALE_DIRS = {"review_information", "trade_representative_contact_information"}


def load_locales(d, platform=None):
    """One audit unit per locale folder, each audited on its own.
    Files in a parent folder fill gaps in every locale below it.
    Returns a list of (label, platform, fields, conflicts)."""
    groups = _read_group_files(d)
    rels = sorted(groups)
    units = []
    unit_rels = []
    app_level = {}
    for rel in rels:
        # fastlane keeps app review and trade contact details in these folders, they are not store listings
        if os.path.basename(rel) in NON_LOCALE_DIRS:
            app_level.setdefault(os.path.dirname(rel), {}).update(_fields_from(groups[rel], ALIASES))
            continue
        plat = platform or group_platform(rel, d)
        aliases = GOOGLE_ALIASES if plat == "google" else ALIASES
        # fastlane's default folder only fills the real locales beside it, it is not a listing of its own
        if os.path.basename(rel) == "default" and any(
            o != rel and os.path.dirname(o) == os.path.dirname(rel)
            and os.path.basename(o) not in NON_LOCALE_DIRS and _fields_from(groups[o], aliases)
            for o in rels
        ):
            continue
        clash = []
        own = _fields_from(groups[rel], aliases, clash)
        if not own:
            continue
        # a folder that holds only shared values (urls, email) is not a locale when locales sit below it
        has_children = any(
            _is_below(o, rel) and _fields_from(groups[o], aliases) for o in rels
        )
        if has_children and not (set(own) - set(URL_FIELDS) - {"contact_email"}):
            continue
        merged, inherited = {}, []
        for a in sorted((o for o in rels if _is_below(rel, o)), key=len):
            near = []
            got = _fields_from(groups[a], aliases, near)
            inherited = [c for c in inherited if c[0] not in got] + near
            merged.update(got)
        # fastlane fills a locale from its default folder, which wins over a file further up, and both values are audited
        sib = os.path.join(os.path.dirname(rel), "default") if rel != "." else None
        if sib and sib.startswith("." + os.sep):
            sib = sib[2:]
        if sib and sib != rel and sib in groups and os.path.basename(rel) != "default":
            near = []
            got = _fields_from(groups[sib], aliases, near)
            up = [(k, "default", "parent folder", merged[k]) for k, v in got.items() if k in merged and merged[k] != v]
            inherited = [c for c in inherited if c[0] not in got] + near + up
            merged.update(got)
        merged.update(own)
        clash += [c for c in inherited if c[0] not in own]
        label = rel if rel != "." else (os.path.basename(os.path.abspath(d)) or d)
        units.append((label, plat, merged, sorted(set(clash))))
        unit_rels.append(rel)
    # review notes belong to their own app, so each app's notes are audited once with that app's first listing
    for parent, fields in sorted(app_level.items()):
        home = next((i for i, r in enumerate(unit_rels) if parent in ("", ".") or r == parent or _is_below(r, parent)), None)
        if home is None:
            units.append((os.path.join(parent, "review_information") if parent else "review_information", platform or "apple", fields, []))
        else:
            label, plat, merged, clash = units[home]
            extra = [(k, "review_information", "locale", merged[k]) for k, v in fields.items() if k in merged and merged[k] != v]
            units[home] = (label, plat, {**merged, **fields}, sorted(set(list(clash) + extra)))
    return units


def load_dir(d):
    """Backward compatible flat view, the union of every locale, the longest value wins as on origin/main."""
    fields = {}
    for _label, _plat, f, _clash in load_locales(d):
        for k, v in f.items():
            if len(v) > len(fields.get(k, "")):
                fields[k] = v
    return fields


def main():
    args = sys.argv[1:]
    check_urls = "--check-urls" in args
    propose = "--propose" in args
    args = [a for a in args if a not in ("--check-urls", "--propose")]

    platform = None
    if "--platform" in args:
        i = args.index("--platform")
        platform = (args[i + 1] if i + 1 < len(args) else "").lower()
        del args[i : i + 2]
        if platform not in PLATFORMS:
            print(
                f"metadata-audit. unknown platform '{platform}'. Use apple or google.",
                file=sys.stderr,
            )
            return 1

    raw = []
    d = None
    i = 0
    while i < len(args):
        a = args[i]
        if a.startswith("--"):
            raw.append((a[2:], args[i + 1] if i + 1 < len(args) else ""))
            i += 2
        elif os.path.isdir(a) or d is None:
            d = a
            i += 1
        else:
            i += 1

    if d and not os.path.isdir(d):
        print(
            f"metadata-audit. {d} is not a directory. Nothing was audited.",
            file=sys.stderr,
        )
        return 1

    def cli_fields(plat):
        aliases = GOOGLE_ALIASES if plat == "google" else ALIASES
        out = {}
        for k, v in raw:
            out[aliases.get(k, k)] = v
        return out

    units = []
    if d:
        for label, plat, f, clash in load_locales(d, platform):
            cli = cli_fields(plat)
            f.update(cli)
            units.append((label, plat, f, [c for c in clash if c[0] not in cli]))
    if not units and raw:
        plat = platform or "apple"
        units.append(("command line", plat, cli_fields(plat), []))

    if not units and d:
        print(f"metadata-audit. no listing files found in {d}. Nothing was audited.")
        print(
            "Add name.txt, subtitle.txt, keywords.txt and description.txt (the fastlane metadata layout),"
        )
        print(
            "or pull them with scripts/pull-metadata.sh, or pass --name, --keywords and --description."
        )
        return 1
    if not units:
        print(
            "metadata-audit. nothing to audit. Pass a metadata directory, or --name, --keywords and --description."
        )
        return 0

    findings = []
    print("== Metadata Audit ==")
    for label, plat, fields, clash in units:
        print(
            f"Locale {label} ({plat}). Fields audited. {', '.join(sorted(fields.keys()))}"
        )
        unit = audit_fields(fields, check_urls=check_urls, platform=plat)
        seen = {(f["severity"], f["rule"], f["field"], f["message"]) for f in unit}
        # Every combination of the conflicting values is audited, so no pairing across fields hides a rejection risk.
        options = {}
        for canon, a, b, alt in clash:
            options.setdefault(canon, [fields.get(canon)])
            if alt not in options[canon]:
                options[canon].append(alt)
        names = sorted(options)
        total = 1
        for n in names:
            total *= len(options[n])
        for combo in itertools.islice(itertools.product(*(options[n] for n in names)), 1, 4096):
            for f in audit_fields({**fields, **dict(zip(names, combo))}, check_urls=check_urls, platform=plat):
                key = (f["severity"], f["rule"], f["field"], f["message"])
                if key not in seen:
                    seen.add(key)
                    unit.append(f)
        for canon, a, b, alt in clash:
            add(
                unit,
                "medium",
                "BOTH-METADATA-DECORATION",
                canon,
                f"{canon} has conflicting values in {a} and {b}, both were audited"
                + ("" if total <= 4096 else f" (the first 4096 of {total} value combinations)"),
                f"Keep one file for {canon} so the store gets the value you audited",
            )
        for f in unit:
            f["locale"] = label
            findings.append(f)
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    findings.sort(key=lambda f: order.get(f["severity"], 9))

    crit = sum(1 for f in findings if f["severity"] == "critical")
    high = sum(1 for f in findings if f["severity"] == "high")
    med = sum(1 for f in findings if f["severity"] == "medium")
    low = sum(1 for f in findings if f["severity"] == "low")

    print("")
    if not findings:
        print("Clean. No metadata rejection risks found.")
    for f in findings:
        print(f"  [{f['severity'].upper()}] {f['rule']}  ({f['field']}, {f['locale']})")
        print(f"      {f['message']}")
        print(f"      fix. {f['fix']}")
    print("")
    print(f"Summary. critical={crit} high={high} medium={med} low={low}")

    if propose and d:
        report = os.path.join(d, ".metadata-fixes.md")
        lines = [
            "# Metadata fix suggestions",
            "",
            "Proposed fixes from metadata-audit. Review each before applying. Source copy is not overwritten.",
            "",
        ]
        for f in findings:
            lines.append(
                f"- [{f['severity']}] {f['locale']} {f['field']}. {f['message']}"
            )
            lines.append(f"  - fix. {f['fix']}")
        with open(report, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        print(f"Wrote suggestions to {report}")

    return 2 if crit > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
