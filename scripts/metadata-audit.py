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

Exit codes: 0 clean or advisory, 2 a critical finding.
"""
import os, sys, re, json, glob

FIELD_LIMITS = {"name": 30, "subtitle": 30, "keywords": 100, "promotional_text": 170, "description": 4000}
# fastlane / asc field file name aliases -> canonical field
ALIASES = {
    "name": "name", "title": "name", "app_name": "name",
    "subtitle": "subtitle",
    "keywords": "keywords",
    "description": "description", "full_description": "description",
    "promotional_text": "promotional_text", "promo_text": "promotional_text", "short_description": "promotional_text",
    "release_notes": "release_notes", "whats_new": "release_notes",
    "review_notes": "review_notes", "notes": "review_notes",
    "privacy_url": "privacy_url", "privacy_policy_url": "privacy_url",
    "support_url": "support_url", "marketing_url": "marketing_url",
}

OTHER_PLATFORMS = ["android", "google play", "play store", "windows phone", "blackberry"]
FUTURE = ["coming soon", "coming-soon", "will be available", "in a future update", "stay tuned", "future release"]
NEGATIVE_APPLE = ["ios bug", "apple bug", "broken on ios", "fix for ios bug"]
PLACEHOLDER = ["lorem ipsum", "placeholder", "todo", "fixme", "test data", "dummy", "example.com"]
CHINA_AI = ["chatgpt", "openai", "gemini", "claude", "anthropic", "copilot"]
RANKING = ["#1", "number one", "best app", "top app", "free", "no.1", "no. 1"]
# small safe profanity sample; teams extend in their own config
CURSE = ["fuck", "shit", "asshole", "bitch", "bastard"]

def add(findings, sev, rule, field, msg, fix):
    findings.append({"severity": sev, "rule": rule, "field": field, "message": msg, "fix": fix})

def has_emoji(s):
    for ch in s:
        o = ord(ch)
        if 0x1F000 <= o <= 0x1FAFF or 0x2600 <= o <= 0x27BF or 0x2190 <= o <= 0x21FF or o in (0x2122, 0x2B50, 0xFE0F):
            return True
    return False

def lc(s):
    return (s or "").lower()

def audit_fields(fields, check_urls=False):
    findings = []
    name = fields.get("name", "")
    subtitle = fields.get("subtitle", "")
    keywords = fields.get("keywords", "")

    # char limits
    for f, limit in FIELD_LIMITS.items():
        v = fields.get(f, "")
        if v and len(v) > limit:
            add(findings, "high", "BOTH-METADATA-DECORATION", f,
                f"{f} is {len(v)} chars, over the {limit} limit", f"Trim {f} to {limit} characters or fewer")

    # decoration in name / subtitle
    for f in ("name", "subtitle"):
        v = fields.get(f, "")
        if v and has_emoji(v):
            add(findings, "medium", "BOTH-METADATA-DECORATION", f, f"{f} contains an emoji", f"Remove emoji from {f}")
        for r in RANKING:
            if r in lc(v):
                add(findings, "high", "BOTH-METADATA-DECORATION", f,
                    f"{f} contains a ranking or price claim ({r})", f"Remove ranking and price claims from {f}")
        words = [w for w in re.findall(r"[A-Za-z]{3,}", v) if w.isupper()]
        if len(words) >= 2:
            add(findings, "medium", "BOTH-METADATA-DECORATION", f, f"{f} uses ALL CAPS words", f"Use normal case in {f} except a real brand")

    # other platform mentions (Apple side)
    for f, v in fields.items():
        for term in OTHER_PLATFORMS:
            if term in lc(v):
                add(findings, "high", "APPLE-2.3-CROSS-PLATFORM-REFERENCE", f,
                    f"{f} mentions another platform ({term})", f"Remove the reference to {term} from {f}")

    # future functionality
    for f, v in fields.items():
        for term in FUTURE:
            if term in lc(v):
                add(findings, "medium", "APPLE-2.3-FUTURE-FUNCTIONALITY", f,
                    f"{f} promises future functionality ({term})", "Describe only what the build does today")

    # negative apple sentiment
    for f, v in fields.items():
        for term in NEGATIVE_APPLE:
            if term in lc(v):
                add(findings, "medium", "APPLE-2.3-NEGATIVE-APPLE-SENTIMENT", f,
                    f"{f} references an iOS bug or Apple negatively", "Remove negative Apple references")

    # placeholder / test
    for f, v in fields.items():
        for term in PLACEHOLDER:
            if term in lc(v):
                add(findings, "high", "BOTH-PLACEHOLDER", f, f"{f} contains placeholder text ({term})", "Replace placeholder with real content")

    # curse words
    for f, v in fields.items():
        for term in CURSE:
            if re.search(r"\b" + re.escape(term) + r"\b", lc(v)):
                add(findings, "high", "APPLE-2.3-CURSE-WORD", f, f"{f} contains profanity", "Remove profanity from the listing")

    # keywords formatting
    if keywords:
        if ", " in keywords:
            add(findings, "low", "APPLE-2.3-KEYWORD-FORMAT", "keywords",
                "keywords field has spaces after commas, which wastes the 100 char budget", "Use commas with no spaces between keywords")
        kw = set(w for w in re.split(r"[,\s]+", lc(keywords)) if w)
        dup = kw & set(re.findall(r"[a-z]{3,}", lc(name + " " + subtitle)))
        if dup:
            add(findings, "low", "APPLE-2.3-KEYWORD-FORMAT", "keywords",
                f"keywords repeat words already in name or subtitle ({', '.join(sorted(dup))})", "Drop duplicated words, the name and subtitle are already indexed")

    # missing privacy policy url
    if not fields.get("privacy_url"):
        add(findings, "high", "BOTH-MISSING-PRIVACY-POLICY", "privacy_url",
            "no privacy policy URL found in the metadata", "Set the Privacy Policy URL in App Store Connect and the Play listing")

    # subscription ToS / PP in description
    desc = lc(fields.get("description", "") + " " + fields.get("promotional_text", ""))
    if any(t in desc for t in ("subscription", "subscribe", "auto-renew", "per month", "per year")):
        if "terms" not in desc and "eula" not in desc:
            add(findings, "high", "APPLE-3.1.2-MISLEADING-PRICING", "description",
                "subscription mentioned but no Terms of Use or EULA link in the description", "Add functional Terms of Use and Privacy Policy links to the description and the paywall")

    # china AI references (advisory, storefront dependent)
    for f in ("name", "subtitle", "keywords", "description"):
        v = lc(fields.get(f, ""))
        for term in CHINA_AI:
            if term in v:
                add(findings, "medium", "CHINA-AI-REFERENCES", f,
                    f"{f} references an external AI service ({term}), which can trigger a China storefront rejection", "Remove or localize external AI references for the China storefront")
                break

    # unreachable URLs
    if check_urls:
        urls = set()
        for v in fields.values():
            urls.update(re.findall(r"https?://[^\s)\"']+", v or ""))
        for u in sorted(urls):
            ok = _url_ok(u)
            if ok is False:
                add(findings, "high", "BOTH-UNREACHABLE-METADATA-URL", "url", f"URL does not load: {u}", "Fix or remove the broken URL before submission")

    return findings

def _url_ok(u):
    try:
        import urllib.request
        req = urllib.request.Request(u, method="HEAD", headers={"User-Agent": "metadata-audit"})
        with urllib.request.urlopen(req, timeout=8) as r:
            return 200 <= r.status < 400
    except Exception:
        return False

def load_dir(d):
    fields = {}
    for path in glob.glob(os.path.join(d, "**", "*.txt"), recursive=True):
        base = os.path.splitext(os.path.basename(path))[0].lower()
        canon = ALIASES.get(base)
        if not canon:
            continue
        try:
            txt = open(path, encoding="utf-8", errors="ignore").read().strip()
        except Exception:
            continue
        # keep the longest value if multiple locales
        if len(txt) > len(fields.get(canon, "")):
            fields[canon] = txt
    # also look for a json metadata file with urls
    for jp in glob.glob(os.path.join(d, "**", "*.json"), recursive=True):
        try:
            data = json.load(open(jp, encoding="utf-8", errors="ignore"))
        except Exception:
            continue
        if isinstance(data, dict):
            for k, v in data.items():
                kk = ALIASES.get(k.lower())
                if kk and isinstance(v, str) and v.strip() and len(v) > len(fields.get(kk, "")):
                    fields[kk] = v.strip()
    return fields

def main():
    args = sys.argv[1:]
    check_urls = "--check-urls" in args
    propose = "--propose" in args
    args = [a for a in args if a not in ("--check-urls", "--propose")]

    fields = {}
    d = None
    i = 0
    while i < len(args):
        a = args[i]
        if a.startswith("--"):
            key = a[2:]
            val = args[i+1] if i+1 < len(args) else ""
            canon = ALIASES.get(key, key)
            fields[canon] = val
            i += 2
        elif os.path.isdir(a):
            d = a
            i += 1
        else:
            i += 1

    if d:
        fields.update({k: v for k, v in load_dir(d).items() if k not in fields})

    if not fields:
        print("metadata-audit. no metadata found. pass a directory or fields. see --help in the header.")
        return 0

    findings = audit_fields(fields, check_urls=check_urls)
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    findings.sort(key=lambda f: order.get(f["severity"], 9))

    crit = sum(1 for f in findings if f["severity"] == "critical")
    high = sum(1 for f in findings if f["severity"] == "high")
    med = sum(1 for f in findings if f["severity"] == "medium")
    low = sum(1 for f in findings if f["severity"] == "low")

    print("== Metadata Audit ==")
    print(f"Fields audited. {', '.join(sorted(fields.keys()))}")
    print("")
    if not findings:
        print("Clean. No metadata rejection risks found.")
    for f in findings:
        print(f"  [{f['severity'].upper()}] {f['rule']}  ({f['field']})")
        print(f"      {f['message']}")
        print(f"      fix. {f['fix']}")
    print("")
    print(f"Summary. critical={crit} high={high} medium={med} low={low}")

    if propose and d:
        report = os.path.join(d, ".metadata-fixes.md")
        lines = ["# Metadata fix suggestions", "",
                 "Proposed fixes from metadata-audit. Review each before applying. Source copy is not overwritten.", ""]
        for f in findings:
            lines.append(f"- [{f['severity']}] {f['field']}. {f['message']}")
            lines.append(f"  - fix. {f['fix']}")
        open(report, "w").write("\n".join(lines) + "\n")
        print(f"Wrote suggestions to {report}")

    return 2 if crit > 0 else 0

if __name__ == "__main__":
    sys.exit(main())
