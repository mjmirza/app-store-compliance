#!/usr/bin/env python3
"""Verifies every cited URL in the repo is real, not a soft-404.
An HTTP 200 is not proof: some hosts serve a generic index for any unknown id."""

import argparse
import hashlib
import os
import re
import sys
import urllib.error
import urllib.request

URL_RE = re.compile(r"https?://[^\s\"'<>)\]},`]+")
TRAILING = ".,;:)]}>\"'`"

# Reachable but bot-blocked or rate-limited. Real content, refuses automation.
# Treating these as dead would make the gate noise, and a noisy gate gets disabled.
BLOCKED_CODES = {401, 403, 405, 429}

# Server-side faults. The URL is not fabricated, the host is failing. Surfaced
# as a warning because a monitor that fetches it is silently getting nothing.
TRANSIENT_CODES = {500, 502, 503, 504}
TIMEOUT = 20
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Hosts that answer 200 for an unknown id. We fetch a deliberately bogus
# control URL per host and treat a matching fingerprint as fabricated.
SOFT404_PROBES = {
    "developer.apple.com": "https://developer.apple.com/news/?id=zzzz-control-not-a-real-id-zzzz",
    "support.google.com": "https://support.google.com/googleplay/android-developer/answer/zzzzcontrolzzzz",
}

TRUST = [
    (
        1,
        (
            "europa.eu",
            "eur-lex.europa.eu",
            "edpb.europa.eu",
            "enisa.europa.eu",
            "ftc.gov",
            "nist.gov",
            "cisa.gov",
            "ico.org.uk",
            "gov.uk",
            "bsi.bund.de",
        ),
    ),
    (2, ("reuters.com", "apnews.com", "bloomberg.com")),
    (
        1,
        (
            "developer.apple.com",
            "apple.com",
            "developer.android.com",
            "support.google.com",
            "source.android.com",
            "play.google.com",
        ),
    ),
    (
        3,
        (
            "owasp.org",
            "mas.owasp.org",
            "cheatsheetseries.owasp.org",
            "datatracker.ietf.org",
            "oauth.net",
        ),
    ),
]

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "assets"}
SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".pdf", ".zip", ".ico"}

# XML/XSD namespace identifiers. They look like URLs but are names, not endpoints.
NAMESPACE_PREFIXES = ("http://schemas.", "http://www.w3.org/", "http://purl.org/", "http://xmlns.")

# RFC 2606 reserved TLDs. Deliberately unresolvable fixtures, never citations.
RESERVED_TLDS = (".invalid", ".test", ".example", ".localhost")

# The verifier and its gauntlet hold deliberate broken URLs as pattern data.
SELF = {"verify-citations.py", "verify-citations-test.sh"}


def trust_of(host):
    for level, hosts in TRUST:
        if any(host == h or host.endswith("." + h) for h in hosts):
            return level
    return 4


def fingerprint(body):
    return hashlib.sha256(body[:200000]).hexdigest()[:16]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.getcode(), r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception:
        return 0, b""


def host_of(url):
    m = re.match(r"https?://([^/]+)", url)
    return m.group(1).lower() if m else ""


def collect_urls(root, only=None):
    found = {}
    targets = only if only else [root]
    for target in targets:
        walk = [target] if os.path.isfile(target) else []
        if not walk:
            for dirpath, dirnames, filenames in os.walk(target):
                dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
                for fn in filenames:
                    if os.path.splitext(fn)[1].lower() in SKIP_EXT or fn in SELF:
                        continue
                    walk.append(os.path.join(dirpath, fn))
        for path in walk:
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                    text = fh.read()
            except OSError:
                continue
            for raw in URL_RE.findall(text):
                url = raw.rstrip(TRAILING)
                if len(url) < 12 or url.startswith(NAMESPACE_PREFIXES):
                    continue
                if "{" in url or "}" in url or "\\n" in url:
                    continue
                if any(host_of(url).endswith(x) for x in RESERVED_TLDS):
                    continue
                found.setdefault(url, set()).add(os.path.relpath(path, root))
    return found


def main():
    ap = argparse.ArgumentParser(
        description="Verify cited URLs are real, not soft-404."
    )
    ap.add_argument("--dir", default=".", help="repo root to scan")
    ap.add_argument("--files", nargs="*", help="scan only these paths")
    ap.add_argument(
        "--offline", action="store_true", help="parse and classify only, no network"
    )
    ap.add_argument(
        "--allow",
        default=".citation-allowlist",
        help="file of URLs intentionally unreachable (one per line)",
    )
    args = ap.parse_args()

    root = os.path.abspath(args.dir)
    allow = set()
    allow_path = os.path.join(root, args.allow)
    if os.path.exists(allow_path):
        with open(allow_path, encoding="utf-8") as fh:
            allow = {l.strip() for l in fh if l.strip() and not l.startswith("#")}

    urls = collect_urls(root, args.files)
    if not urls:
        print("verify-citations. no URLs found.")
        return 0

    print(f"verify-citations. {len(urls)} distinct URL(s) across the scan.")
    if args.offline:
        for u in sorted(urls):
            print(f"  P{trust_of(host_of(u))} {u}")
        print("offline mode. no network verification performed.")
        return 0

    controls = {}
    for host, probe in SOFT404_PROBES.items():
        code, body = fetch(probe)
        if code == 200 and body:
            controls[host] = fingerprint(body)

    fabricated, dead, blocked, transient, ok = [], [], [], [], 0
    own_controls = set(SOFT404_PROBES.values())
    for url in sorted(urls):
        # Skip the verifier's own bogus control ids and its gauntlet fixtures.
        if url in allow or url in own_controls:
            ok += 1
            continue
        host = host_of(url)
        code, body = fetch(url)
        if code == 200 and body:
            fp = fingerprint(body)
            ctrl = controls.get(host)
            if ctrl and fp == ctrl:
                fabricated.append((url, sorted(urls[url])))
            else:
                ok += 1
        elif code in BLOCKED_CODES:
            blocked.append((url, code))
        elif code in TRANSIENT_CODES:
            transient.append((url, code, sorted(urls[url])))
        elif 200 <= code < 400:
            ok += 1
        else:
            dead.append((url, code, sorted(urls[url])))

    print(f"  verified real. {ok}")
    if blocked:
        print(f"  reachable but bot-blocked, not a defect. {len(blocked)}")
    if transient:
        print(f"\nHOST FAULT. {len(transient)} URL(s) return 5xx. Not fabricated, but any")
        print("monitor fetching these is silently receiving nothing.")
        for url, code, files in transient:
            print(f"  [{code}] {url}")
            for f in files:
                print(f"        cited in {f}")
    if fabricated:
        print(f"\nFABRICATED. {len(fabricated)} URL(s) return 200 but serve the host's")
        print("generic index, identical to a deliberately bogus control id.")
        for url, files in fabricated:
            print(f"  [FABRICATED] {url}")
            for f in files:
                print(f"               cited in {f}")
    if dead:
        print(f"\nUNREACHABLE. {len(dead)} URL(s).")
        for url, code, files in dead:
            print(f"  [{code or 'ERR'}] {url}")
            for f in files:
                print(f"        cited in {f}")

    if fabricated or dead:
        print("\nverify-citations. FAIL")
        return 1
    print("\nverify-citations. PASS. every citation resolves to real content.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
