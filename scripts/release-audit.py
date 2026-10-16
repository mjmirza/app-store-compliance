#!/usr/bin/env python3
"""Release readiness audit. Usage. release-audit.py <app-dir> [--metadata <pulled-listing-dir>]
Exit 0 clear, 2 blocked on a critical or high finding, 3 incomplete scan, 1 bad input."""

import os
import sys
import subprocess
import json
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUARD_NAME = "app-store-compliance-guard.sh"
BLOCKING = ("critical", "high")
LISTING_HINT = "Store listing not audited. Pull it with scripts/pull-metadata.sh, then pass --metadata <dir>."

# 13 Required areas
REQUIRED_AREAS = [
    "Apple requirements",
    "Google Play requirements",
    "Web requirements",
    "Privacy",
    "Security",
    "Accessibility",
    "AI regulations",
    "Store metadata",
    "Permissions",
    "Legal documentation",
    "SDK compatibility",
    "Deprecated APIs",
    "Platform announcements",
]

# Recommended reviewers for each area
RECOMMENDED_REVIEWERS = {
    "Apple requirements": "Mobile Tech Lead, iOS Platform Architect",
    "Google Play requirements": "Mobile Tech Lead, Android Platform Architect",
    "Web requirements": "Frontend Technical Lead, Web Architect",
    "Privacy": "Data Protection Officer (DPO), Legal Counsel (Privacy)",
    "Security": "Product Security Engineering Team, DevSecOps Lead",
    "Accessibility": "Frontend QA Team, Accessibility Specialist",
    "AI regulations": "AI Ethics and Governance Committee, Lead AI Architect",
    "Store metadata": "Product Marketing Manager (PMM), App Store Optimization (ASO) Specialist",
    "Permissions": "Lead Developer, Mobile Platform Leads",
    "Legal documentation": "Legal Counsel (Commercial/IP), Compliance Officer",
    "SDK compatibility": "Lead Mobile Developer, Architecture Review Board",
    "Deprecated APIs": "Lead Developer, Tech Debt/Platform Team",
    "Platform announcements": "Lead Developer, Mobile Release Manager",
}

# Manual mapping of specific patterns to areas
MAP_PATTERNS_TO_AREAS = {
    "APPLE-2.1-MISSING-DEMO-ACCOUNT": ["Apple requirements"],
    "APPLE-2.1-PLACEHOLDER-CONTENT": ["Apple requirements", "Store metadata"],
    "APPLE-2.1-STAGING-BACKEND": ["Apple requirements", "Security"],
    "APPLE-5.1.1-MISSING-PRIVACY-POLICY": ["Apple requirements", "Privacy"],
    "APPLE-5.1.1-VAGUE-PURPOSE-STRING": ["Apple requirements", "Permissions"],
    "APPLE-5.1.1-MISSING-USAGE-DESCRIPTION": ["Apple requirements", "Permissions"],
    "APPLE-5.1.1-NO-ACCOUNT-DELETION": ["Apple requirements", "Privacy"],
    "APPLE-5.1.2-MISSING-ATT": ["Apple requirements", "Privacy"],
    "APPLE-3.1.1-EXTERNAL-PAYMENT": ["Apple requirements", "SDK compatibility"],
    "APPLE-4.8-SOCIAL-LOGIN-ONLY": ["Apple requirements", "Privacy"],
    "APPLE-4.2-WEB-WRAPPER": ["Apple requirements", "Web requirements"],
    "APPLE-2.5.1-PRIVATE-API": ["Apple requirements", "Deprecated APIs", "Security"],
    "APPLE-2.3-CROSS-PLATFORM-REFERENCE": ["Apple requirements", "Store metadata"],
    "APPLE-2.3-AGE-RATING-2026": ["Apple requirements", "Platform announcements"],
    "APPLE-5.1.2-AI-NO-CONSENT-MODAL": [
        "Apple requirements",
        "AI regulations",
        "Privacy",
    ],
    "GOOGLE-DATASAFETY-MISMATCH": ["Google Play requirements", "Privacy"],
    "GOOGLE-PERM-BACKGROUND-LOCATION": ["Google Play requirements", "Permissions"],
    "GOOGLE-PERM-ALL-FILES": ["Google Play requirements", "Permissions"],
    "GOOGLE-PERM-SMS-CALLLOG": ["Google Play requirements", "Permissions"],
    "GOOGLE-PERM-ACCESSIBILITY-MISUSE": ["Google Play requirements", "Accessibility"],
    "GOOGLE-TARGET-API": ["Google Play requirements", "Platform announcements"],
    "GOOGLE-12-TESTER-RULE": ["Google Play requirements", "Platform announcements"],
    "GOOGLE-PLAY-BILLING": ["Google Play requirements", "SDK compatibility"],
    "GOOGLE-MISSING-PRIVACY-POLICY": ["Google Play requirements", "Privacy"],
    "GOOGLE-MISLEADING-LISTING": ["Google Play requirements", "Store metadata"],
    "GOOGLE-FAMILIES-AD-SDK": ["Google Play requirements", "SDK compatibility"],
    "BOTH-SDK-SUPPLY-CHAIN": ["SDK compatibility"],
    "BOTH-LOOTBOX-ODDS": ["Legal documentation"],
    "APPLE-PRIVACY-MANIFEST-MISSING": ["Apple requirements", "Privacy"],
    "APPLE-EXPORT-COMPLIANCE-MISSING": ["Apple requirements", "Legal documentation"],
    "APPLE-RESTORE-PURCHASES-MISSING": ["Apple requirements"],
    "APPLE-ACCOUNT-DELETION-WEAK": ["Apple requirements", "Privacy"],
    "ANDROID-DYNAMIC-CODE-LOADING": ["Google Play requirements", "Security"],
    "ANDROID-QUERY-ALL-PACKAGES": ["Google Play requirements", "Permissions"],
    "ANDROID-OVERLAY-TAPJACKING": ["Google Play requirements", "Security"],
    "ANDROID-ACCOUNT-DELETION-URL": ["Google Play requirements", "Privacy"],
    "BOTH-AI-GENERATED-CONTENT": ["AI regulations"],
    "BOTH-METADATA-DECORATION": ["Store metadata"],
    "BOTH-FINGERPRINTING": ["Privacy", "Security"],
    "APPLE-2.3-FUTURE-FUNCTIONALITY": ["Apple requirements", "Store metadata"],
    "APPLE-2.3-NEGATIVE-APPLE-SENTIMENT": ["Apple requirements", "Store metadata"],
    "BOTH-UNREACHABLE-METADATA-URL": ["Store metadata"],
    "APPLE-5.2.5-APPLE-DEVICE-IMAGE": ["Apple requirements", "Store metadata"],
    "APPLE-2.3.4-DEVICE-FRAMES-PREVIEW": ["Apple requirements", "Store metadata"],
    "APPLE-3.1.2-MISLEADING-PRICING": ["Apple requirements", "Store metadata"],
    "APPLE-1.2-UGC-24H-ACTION": ["Apple requirements", "Legal documentation"],
    "CHINA-AI-REFERENCES": ["AI regulations"],
    "APPLE-2.4.5-UNUSED-ENTITLEMENTS": ["Apple requirements"],
    "APPLE-4.0-SIWA-UX": ["Apple requirements"],
    "APPLE-5.1.1-UNNECESSARY-DATA": ["Apple requirements", "Privacy"],
    "APPLE-2.1-DEBUG-FEATURES": ["Apple requirements", "Security"],
    "APPLE-2.1-CLOUD-NOT-IN-PRODUCTION": ["Apple requirements"],
    "APPLE-2.1-REVIEW-NOTES-INCOMPLETE": ["Apple requirements", "Store metadata"],
    "BOTH-INVALID-METADATA-URL": ["Store metadata"],
    "APPLE-MISSING-SUPPORT-URL": ["Apple requirements", "Store metadata"],
    "GOOGLE-MISSING-CONTACT-EMAIL": ["Google Play requirements", "Store metadata"],
}


def resolve_guard():
    """Find the guard. APP_STORE_GUARD_PATH wins, then the repo layout, then an installed skill.
    Returns (path, None) or (None, reason)."""
    env = os.environ.get("APP_STORE_GUARD_PATH", "").strip()
    if env:
        if os.path.isfile(env):
            return os.path.abspath(env), None
        return None, f"APP_STORE_GUARD_PATH points at {env}, which is not a file"
    candidates = [
        os.path.join(ROOT, "agent-os", "hooks", GUARD_NAME),
        # installed. <config>/skills/app-store-compliance/scripts -> <config>/hooks
        os.path.normpath(os.path.join(ROOT, "..", "..", "hooks", GUARD_NAME)),
    ]
    # shared skill in ~/.agents. the installer records each tool's guard path in .guards
    try:
        with open(os.path.join(ROOT, ".guards"), encoding="utf-8") as f:
            candidates += [ln.rstrip("\n").partition("\t")[2] for ln in f if "\t" in ln]
    except OSError:
        pass
    for c in candidates:
        if c and os.path.isfile(c):
            return c, None
    return None, "looked in " + " and ".join(candidates)


def scan_problems(name, code, out, err, ok_codes=(0, 2)):
    """Reasons a scanner run cannot be trusted as a complete check. Empty means it ran fine."""
    problems = []
    text = (out or "") + "\n" + (err or "")
    if code not in ok_codes:
        problems.append(f"{name} exited {code}")
    for marker in ("NOT CHECKED", "Nothing was audited"):
        if marker in text:
            line = next((ln.strip() for ln in text.splitlines() if marker in ln), marker)
            problems.append(f"{name} did not check everything. {line}")
    return problems


def tail(text, n=8):
    lines = [ln for ln in (text or "").splitlines() if ln.strip()]
    return lines[-n:]


def decide_status(findings, problems):
    """Overall status and exit code. A failed or partial scan never passes, a high finding blocks."""
    if problems:
        return "INCOMPLETE", 3
    if any(f["severity"] in BLOCKING for f in findings):
        return "BLOCKED", 2
    if findings:
        return "ADVISORY", 0
    return "PASSED", 0


def run_command(args, cwd=ROOT):
    try:
        res = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
        return res.returncode, res.stdout, res.stderr
    except Exception as e:
        return -1, "", str(e)


DEADLINE_LINE_RE = re.compile(r"\(mandatory \d{4}-\d{2}-\d{2}\)")

FINDING_SHAPE_RE = re.compile(r"^\s*\[\w+\]\s+[A-Z0-9]+(-[A-Z0-9.]+)+\s")


def is_deadline_line(line):
    """A deadline-checker line carries a date after the word mandatory. A finding does not."""
    if FINDING_SHAPE_RE.match(line):
        return False
    return bool(DEADLINE_LINE_RE.search(line))


def load_patterns():
    path = os.path.join(ROOT, "data", "rejection-patterns.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {p["id"]: p for p in data.get("patterns", [])}
        except Exception:
            pass
    return {}


def get_areas_for_pattern(pid, patterns_dict):
    if pid in MAP_PATTERNS_TO_AREAS:
        return MAP_PATTERNS_TO_AREAS[pid]

    pdata = patterns_dict.get(pid, {})
    platform = pdata.get("platform", "").lower()

    areas = []
    if platform == "apple":
        areas.append("Apple requirements")
    elif platform == "google":
        areas.append("Google Play requirements")
    elif platform == "web":
        areas.append("Web requirements")
    elif platform == "both":
        areas.append("Apple requirements")
        areas.append("Google Play requirements")

    title_lower = pdata.get("title", "").lower() + " " + pid.lower()

    if (
        "privacy" in title_lower
        or "data-safety" in title_lower
        or "tracking" in title_lower
        or "fingerprinting" in title_lower
    ):
        areas.append("Privacy")
    if (
        "security" in title_lower
        or "staging" in title_lower
        or "backend" in title_lower
        or "private-api" in title_lower
        or "overlay" in title_lower
        or "dynamic" in title_lower
    ):
        areas.append("Security")
    if "accessibility" in title_lower:
        areas.append("Accessibility")
    if (
        "ai" in title_lower
        or "openai" in title_lower
        or "gemini" in title_lower
        or "claude" in title_lower
    ):
        areas.append("AI regulations")
    if (
        "metadata" in title_lower
        or "placeholder" in title_lower
        or "future-func" in title_lower
        or "unreachable" in title_lower
    ):
        areas.append("Store metadata")
    if "perm" in title_lower or "usage-description" in title_lower:
        areas.append("Permissions")
    if "billing" in title_lower or "payment" in title_lower or "sdk" in title_lower:
        areas.append("SDK compatibility")

    if not areas:
        areas.append("Apple requirements")
        areas.append("Google Play requirements")

    return list(set(areas))


def find_affected_files(target_dir, patterns_dict):
    affected = {}
    exclude_dirs = {
        "node_modules",
        "Pods",
        ".git",
        "build",
        "DerivedData",
        "vendor",
        ".dart_tool",
        "Carthage",
        "androidTest",
        "__tests__",
    }
    allowed_exts = {
        ".swift",
        ".m",
        ".h",
        ".kt",
        ".java",
        ".xml",
        ".plist",
        ".gradle",
        ".kts",
        ".json",
        ".js",
        ".ts",
        ".dart",
        ".xcconfig",
        ".pbxproj",
        ".entitlements",
        ".md",
    }

    for root, dirs, files in os.walk(target_dir):
        # modify dirs in place to prune excluded dirs
        dirs[:] = [
            d
            for d in dirs
            if d not in exclude_dirs
            and not d.endswith("Tests")
            and not d.endswith("Tests__")
        ]

        for file in files:
            ext = os.path.splitext(file)[1]
            if ext not in allowed_exts:
                continue

            filepath = os.path.join(root, file)
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception:
                continue

            for pid, pdata in patterns_dict.items():
                signals = pdata.get("signals", [])
                counter_signals = pdata.get("counterSignals", [])

                if not signals:
                    continue

                # BOTH-PLACEHOLDER needs a refined regex; the JSON signal is a plain word.
                has_signal = False
                if pid == "BOTH-PLACEHOLDER":
                    # Check custom regexes or simple substrings
                    ph_regex = r'lorem ipsum|example\.(com|org)|YOUR_[A-Z_]+_(KEY|HERE)|INSERT_[A-Z_]+_HERE|dummy (text|content|data)|(john|jane)@example|"Acme( Inc| Corp)?"'
                    if re.search(ph_regex, content, re.IGNORECASE):
                        has_signal = True
                else:
                    for sig in signals:
                        if sig in content:
                            has_signal = True
                            break

                if has_signal:
                    has_counter = False
                    for csig in counter_signals:
                        if csig in content:
                            has_counter = True
                            break

                    if not has_counter:
                        rel_path = os.path.relpath(filepath, target_dir)
                        if pid not in affected:
                            affected[pid] = []
                        # Avoid adding the tool's own definition files if possible, unless they are the target
                        if (
                            "rejection-patterns.json" not in rel_path
                            and "release-audit.py" not in rel_path
                            and "app-store-compliance-guard.sh" not in rel_path
                            and "RELEASE-READINESS-REPORT.md" not in rel_path
                        ):
                            affected[pid].append(rel_path)

    return affected


def main():
    args = sys.argv[1:]
    meta_dir = None
    if "--metadata" in args:
        i = args.index("--metadata")
        meta_dir = args[i + 1] if i + 1 < len(args) else ""
        del args[i:i + 2]
        if not os.path.isdir(meta_dir):
            print(f"release-audit. --metadata '{meta_dir}' is not a directory.", file=sys.stderr)
            return 1
        meta_dir = os.path.abspath(meta_dir)
    target_dir = ROOT
    if args:
        if not os.path.isdir(args[0]):
            print(f"release-audit. '{args[0]}' is not a directory.", file=sys.stderr)
            return 1
        target_dir = os.path.abspath(args[0])

    guard_path, guard_missing = resolve_guard()
    if not guard_path:
        print(f"release-audit. compliance guard not found, {guard_missing}.", file=sys.stderr)
        print("Set APP_STORE_GUARD_PATH to the guard script, or reinstall with scripts/install.sh.", file=sys.stderr)
        return 1

    print("== Starting Release Readiness Compliance Audit ==")
    print(f"Target Directory: {target_dir}")
    print(f"Guard. {guard_path}")
    print(f"Store listing. {meta_dir or target_dir + ' (pass --metadata to audit a pulled listing)'}")
    print("")

    # --- Step 1. Run Internal Validation and Test Engines ---
    print("Step 1 of 2. Checking the playbook itself first. This takes about two minutes.", flush=True)

    val_code, val_out, val_err = run_command(["python3", "scripts/validate.py"])
    if val_code != 0:
        print("  ERROR: validate.py failed")
        print(val_out)
        print(val_err)
        return 1

    guard_test = os.path.join(ROOT, "agent-os", "hooks", "app-store-compliance-guard-test.sh")
    if os.path.isfile(guard_test):
        guard_test_code, guard_test_out, guard_test_err = run_command(["bash", guard_test])
        if guard_test_code != 0:
            print("  ERROR: compliance guard tests failed")
            print(guard_test_out)
            print(guard_test_err)
            return 1
    else:
        print("  The guard's own tests ship only with the repository, skipped in this installed copy.")

    meta_test_code, meta_test_out, meta_test_err = run_command(
        ["bash", "scripts/metadata-audit-test.sh"]
    )
    if meta_test_code != 0:
        print("  ERROR: metadata audit tests failed")
        print(meta_test_out)
        print(meta_test_err)
        return 1

    print("Internal validation and test engines passed successfully.")
    print("")

    # --- Step 2. Execute Compliance Scanners ---
    print("Step 2 of 2. Scanning your app...", flush=True)

    # Run the compliance guard
    guard_code, guard_out, guard_err = run_command(["bash", guard_path, target_dir])

    # Run metadata-audit.py
    # The pulled listing from --metadata when given, otherwise the app folder itself
    meta_code, meta_out, meta_err = run_command(
        ["python3", "scripts/metadata-audit.py", meta_dir or target_dir]
    )

    patterns_dict = load_patterns()
    findings = parse_findings(guard_out + "\n" + meta_out)

    problems = scan_problems("compliance guard", guard_code, guard_out, guard_err)
    listing_missing = meta_dir is None and "Nothing was audited" in meta_out + meta_err
    if listing_missing:
        problems.append(LISTING_HINT)
    else:
        problems += scan_problems("metadata audit", meta_code, meta_out, meta_err)
    if guard_code == 2 and not any(f["severity"] == "critical" for f in parse_findings(guard_out)):
        problems.append("compliance guard exited 2 but reported no critical finding")
    if problems:
        print("")
        print("Scan problems. The release cannot be approved until every scan completes.")
        for p in problems:
            print(f"  - {p}")
        for name, out, err in (("compliance guard", guard_out, guard_err), ("metadata audit", meta_out, meta_err)):
            if name in " ".join(problems):
                for ln in tail(err) or tail(out):
                    print(f"    {name}. {ln}")
        if listing_missing:
            seen = next((ln.strip() for ln in (meta_out + meta_err).splitlines() if "Nothing was audited" in ln), "")
            print(f"    metadata audit. {seen}")
        print("")

    # Programmatically scan for affected files
    affected_files_map = find_affected_files(target_dir, patterns_dict)
    return compile_report(target_dir, findings, problems, patterns_dict, affected_files_map)


def parse_findings(all_scanner_stdout):
    findings = []
    lines = all_scanner_stdout.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if is_deadline_line(line):
            i += 1
            continue
        match = re.match(
            r"^\s*\[(CRITICAL|HIGH|MEDIUM|LOW)\]\s+([A-Z0-9-._]+)\s+(.+)$",
            line,
            re.IGNORECASE,
        )
        # every real finding id is hyphenated (APPLE-5.1.1-..., BOTH-PLACEHOLDER); a bare word is prose
        if match and "-" not in match.group(2):
            match = None
        if match:
            sev = match.group(1).lower()
            pid = match.group(2)
            title = match.group(3).strip()
            # Trim trailing (field) suffix in case of metadata-audit format
            title = re.sub(r"\s*\([^)]+\)$", "", title)

            fix = ""
            if i + 1 < len(lines) and re.match(r"^\s*file\.\s", lines[i + 1]):
                i += 1
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                fix_match = re.match(r"^\s*fix\.\s+(.+)$", next_line, re.IGNORECASE)
                if fix_match:
                    fix = fix_match.group(1).strip()
                    i += 1

            # Avoid duplicate findings
            if not any(f["id"] == pid for f in findings):
                findings.append(
                    {"id": pid, "severity": sev, "title": title, "fix": fix}
                )
        i += 1
    return findings


def compile_report(target_dir, findings, problems, patterns_dict, affected_files_map):
    # --- Step 3. Compile Report and Map to 13 Areas ---
    area_findings = {area: [] for area in REQUIRED_AREAS}
    overall_status, exit_code = decide_status(findings, problems)
    has_blocking = any(f["severity"] in BLOCKING for f in findings)

    for f in findings:
        pid = f["id"]
        areas = get_areas_for_pattern(pid, patterns_dict)
        for area in areas:
            if area in area_findings:
                # Add finding to this area's list
                area_findings[area].append(f)

    # Compile the Markdown report text (Strictly NO EMOJIS or emoticons)
    report_lines = []
    report_lines.append("# Release Readiness Compliance Report")
    report_lines.append("")
    report_lines.append(f"Target Directory: {target_dir}")

    report_lines.append(f"Overall Compliance Status: {overall_status}")
    report_lines.append("")

    report_lines.append("## Executive Summary")
    if problems:
        report_lines.append(
            "The audit is INCOMPLETE. One or more scans failed or did not check the app, so the release cannot be approved. Fix the scan problems below and run the audit again."
        )
        report_lines.append("")
        report_lines.append("## Scan Problems")
        for p in problems:
            report_lines.append(f"- {p}")
    elif has_blocking:
        report_lines.append(
            "The release is currently BLOCKED due to one or more critical or high compliance issues that must be resolved before submitting to the platforms."
        )
    elif findings:
        report_lines.append(
            "The release is ready but has outstanding non-critical advisory risks. Review the required actions and consult the recommended reviewers before finalizing the release."
        )
    else:
        report_lines.append(
            "The release has successfully passed all compliance audits with zero outstanding risks. Ready for deployment."
        )
    report_lines.append("")

    report_lines.append("## Compliance Summary Table")
    report_lines.append("")
    report_lines.append("| Area | Status | Risks Found | Recommended Reviewers |")
    report_lines.append("| --- | --- | --- | --- |")

    for area in REQUIRED_AREAS:
        area_status = "PASSED"
        area_f = area_findings[area]
        if area_f:
            if any(af["severity"] in BLOCKING for af in area_f):
                area_status = "BLOCKED"
            else:
                area_status = "ADVISORY"

        num_risks = len(area_f)
        reviewers = RECOMMENDED_REVIEWERS.get(area, "Lead Developer")
        report_lines.append(f"| {area} | {area_status} | {num_risks} | {reviewers} |")
    report_lines.append("")

    report_lines.append("## Detailed Compliance Analysis")
    report_lines.append("")

    for idx, area in enumerate(REQUIRED_AREAS, 1):
        area_f = area_findings[area]
        area_status = "PASSED"
        if area_f:
            if any(af["severity"] in BLOCKING for af in area_f):
                area_status = "BLOCKED"
            else:
                area_status = "ADVISORY"

        report_lines.append(f"### {idx}. {area}")
        report_lines.append(f"- Status: {area_status}")
        report_lines.append(
            f"- Recommended Reviewers: {RECOMMENDED_REVIEWERS.get(area, 'Lead Developer')}"
        )
        report_lines.append("")

        if not area_f:
            report_lines.append("No outstanding risks found for this area.")
            report_lines.append("")
            continue

        report_lines.append(
            "| Finding ID | Severity | Description | Required Action | Affected Files |"
        )
        report_lines.append("| --- | --- | --- | --- | --- |")

        for af in area_f:
            pid = af["id"]
            sev = af["severity"].upper()
            title = af["title"]
            fix = af["fix"] or "Refer to guidelines for remediation."

            # Retrieve programmatically scanned affected files
            aff_files = affected_files_map.get(pid, [])
            if not aff_files:
                files_str = "None detected (Config/Listing check)"
            else:
                # Limit to first 5 paths to keep the table clean
                files_str = "<br>".join(aff_files[:5])
                if len(aff_files) > 5:
                    files_str += f"<br>... and {len(aff_files) - 5} more files"

            report_lines.append(f"| {pid} | {sev} | {title} | {fix} | {files_str} |")
        report_lines.append("")

    # Write report file into the audited target, not this playbook's own root
    report_path = os.path.join(target_dir, "RELEASE-READINESS-REPORT.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

    print(f"Release readiness report generated successfully at: {report_path}")
    print(
        f"Summary: critical={sum(1 for f in findings if f['severity'] == 'critical')} high={sum(1 for f in findings if f['severity'] == 'high')} medium={sum(1 for f in findings if f['severity'] == 'medium')} low={sum(1 for f in findings if f['severity'] == 'low')}"
    )
    print(f"Overall Status: {overall_status}")

    if overall_status == "INCOMPLETE":
        print("Release is NOT APPROVED. A scan failed or did not check the app, see Scan problems above.")
    elif overall_status == "BLOCKED":
        print("Release is BLOCKED. Resolve the critical and high issues.")
    else:
        print("Release is CLEAR TO SUBMIT.")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
