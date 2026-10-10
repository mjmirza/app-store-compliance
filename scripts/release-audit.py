#!/usr/bin/env python3
"""Runs metadata/guard scans against a target project and compiles a
release-readiness report. Exits non-zero on any critical finding."""

import os
import sys
import subprocess
import json
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 15 Required release verification areas
REQUIRED_AREAS = [
    "permissions",
    "privacy disclosures",
    "screenshots",
    "metadata",
    "age rating",
    "AI disclosures",
    "subscription disclosures",
    "payment compliance",
    "accessibility",
    "legal documents",
    "support URL",
    "privacy policy",
    "terms of service",
    "export compliance",
    "encryption declarations",
]

# Recommended reviewers for each of the 15 areas
RECOMMENDED_REVIEWERS = {
    "permissions": "Lead Developer, Mobile Platform Leads",
    "privacy disclosures": "Data Protection Officer (DPO), Legal Counsel (Privacy)",
    "screenshots": "Product Marketing Manager (PMM), App Store Optimization (ASO) Specialist",
    "metadata": "Product Marketing Manager (PMM), App Store Optimization (ASO) Specialist",
    "age rating": "Compliance Officer, Content Rating Lead",
    "AI disclosures": "AI Ethics and Governance Committee, Lead AI Architect",
    "subscription disclosures": "Legal Counsel (Commercial/IP), Product Manager (Monetization)",
    "payment compliance": "Lead Developer, Payment Operations Lead",
    "accessibility": "Frontend QA Team, Accessibility Specialist",
    "legal documents": "Legal Counsel (Commercial/IP), Compliance Officer",
    "support URL": "Customer Support Lead, Product Operations",
    "privacy policy": "Data Protection Officer (DPO), Legal Counsel (Privacy)",
    "terms of service": "Legal Counsel (Commercial/IP), Compliance Officer",
    "export compliance": "Trade Compliance Specialist, Legal Counsel",
    "encryption declarations": "Product Security Engineering Team, DevSecOps Lead",
}

# Manual mapping of specific patterns to the 15 required areas
MAP_PATTERNS_TO_AREAS = {
    "APPLE-2.1-MISSING-DEMO-ACCOUNT": ["metadata", "legal documents"],
    "APPLE-2.1-PLACEHOLDER-CONTENT": ["metadata", "screenshots"],
    "APPLE-2.1-STAGING-BACKEND": ["metadata", "encryption declarations"],
    "APPLE-5.1.1-MISSING-PRIVACY-POLICY": ["privacy policy", "privacy disclosures", "legal documents"],
    "APPLE-5.1.1-VAGUE-PURPOSE-STRING": ["permissions", "privacy disclosures"],
    "APPLE-5.1.1-MISSING-USAGE-DESCRIPTION": ["permissions", "privacy disclosures"],
    "APPLE-5.1.1-NO-ACCOUNT-DELETION": ["privacy disclosures", "privacy policy", "terms of service"],
    "APPLE-5.1.2-MISSING-ATT": ["privacy disclosures", "permissions"],
    "APPLE-3.1.1-EXTERNAL-PAYMENT": ["payment compliance", "subscription disclosures"],
    "APPLE-4.8-SOCIAL-LOGIN-ONLY": ["privacy disclosures", "terms of service"],
    "APPLE-4.2-WEB-WRAPPER": ["metadata", "terms of service"],
    "APPLE-2.5.1-PRIVATE-API": ["permissions", "encryption declarations"],
    "APPLE-2.3-CROSS-PLATFORM-REFERENCE": ["metadata"],
    "APPLE-2.3-AGE-RATING-2026": ["age rating", "metadata"],
    "APPLE-5.1.2-AI-NO-CONSENT-MODAL": [
        "AI disclosures",
        "privacy disclosures",
        "privacy policy",
    ],
    "GOOGLE-DATASAFETY-MISMATCH": ["privacy disclosures", "privacy policy"],
    "GOOGLE-PERM-BACKGROUND-LOCATION": ["permissions"],
    "GOOGLE-PERM-ALL-FILES": ["permissions"],
    "GOOGLE-PERM-SMS-CALLLOG": ["permissions"],
    "GOOGLE-PERM-ACCESSIBILITY-MISUSE": ["accessibility", "permissions"],
    "GOOGLE-TARGET-API": ["metadata", "permissions"],
    "GOOGLE-12-TESTER-RULE": ["metadata"],
    "GOOGLE-PLAY-BILLING": ["payment compliance", "subscription disclosures"],
    "GOOGLE-MISSING-PRIVACY-POLICY": ["privacy policy", "privacy disclosures", "legal documents"],
    "GOOGLE-MISLEADING-LISTING": ["metadata", "screenshots"],
    "GOOGLE-FAMILIES-AD-SDK": ["privacy disclosures", "age rating"],
    "BOTH-SDK-SUPPLY-CHAIN": ["encryption declarations", "permissions"],
    "BOTH-LOOTBOX-ODDS": ["legal documents", "payment compliance", "age rating"],
    "APPLE-PRIVACY-MANIFEST-MISSING": ["privacy disclosures", "export compliance"],
    "APPLE-EXPORT-COMPLIANCE-MISSING": ["export compliance", "encryption declarations"],
    "APPLE-RESTORE-PURCHASES-MISSING": ["subscription disclosures", "payment compliance"],
    "APPLE-ACCOUNT-DELETION-WEAK": ["privacy disclosures", "privacy policy"],
    "ANDROID-DYNAMIC-CODE-LOADING": ["encryption declarations", "permissions"],
    "ANDROID-QUERY-ALL-PACKAGES": ["permissions"],
    "ANDROID-OVERLAY-TAPJACKING": ["permissions", "accessibility"],
    "ANDROID-ACCOUNT-DELETION-URL": ["privacy policy", "support URL"],
    "BOTH-AI-GENERATED-CONTENT": ["AI disclosures", "age rating"],
    "BOTH-METADATA-DECORATION": ["metadata", "screenshots"],
    "BOTH-FINGERPRINTING": ["privacy disclosures", "permissions"],
    "APPLE-2.3-FUTURE-FUNCTIONALITY": ["metadata"],
    "APPLE-2.3-NEGATIVE-APPLE-SENTIMENT": ["metadata"],
    "BOTH-UNREACHABLE-METADATA-URL": ["support URL", "metadata"],
    "APPLE-5.2.5-APPLE-DEVICE-IMAGE": ["screenshots", "metadata"],
    "APPLE-2.3.4-DEVICE-FRAMES-PREVIEW": ["screenshots", "metadata"],
    "APPLE-3.1.2-MISLEADING-PRICING": ["subscription disclosures", "payment compliance"],
    "APPLE-1.2-UGC-24H-ACTION": ["legal documents", "terms of service"],
    "CHINA-AI-REFERENCES": ["AI disclosures"],
    "APPLE-2.4.5-UNUSED-ENTITLEMENTS": ["permissions"],
    "APPLE-4.0-SIWA-UX": ["terms of service", "privacy disclosures"],
    "APPLE-5.1.1-UNNECESSARY-DATA": ["privacy disclosures", "privacy policy"],
    "APPLE-2.1-DEBUG-FEATURES": ["encryption declarations", "permissions"],
    "APPLE-2.1-CLOUD-NOT-IN-PRODUCTION": ["terms of service", "support URL"],
    "APPLE-2.1-REVIEW-NOTES-INCOMPLETE": ["metadata", "legal documents"],
    "APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED": ["age rating", "metadata"],
    "BOTH-SUBSCRIPTION-HARD-CANCEL": ["subscription disclosures", "payment compliance", "terms of service"],
    "BOTH-PLACEHOLDER": ["metadata", "screenshots"],
}


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
    title_lower = (pid + " " + pdata.get("title", "") + " " + pdata.get("description", "")).lower()

    areas = []

    if any(k in title_lower for k in ["perm", "usage-description", "purpose-string", "camera", "location", "contacts", "photos", "microphone", "health", "overlay", "query-all-packages", "advertising-id"]):
        areas.append("permissions")
    if any(k in title_lower for k in ["privacy", "manifest", "tracking", "att", "data-safety", "fingerprint", "xcprivacy", "user-data"]):
        areas.append("privacy disclosures")
    if any(k in title_lower for k in ["screenshot", "device-image", "device-frame", "preview", "misleading-listing"]):
        areas.append("screenshots")
    if any(k in title_lower for k in ["metadata", "title", "subtitle", "description", "keywords", "placeholder", "future-func", "cross-platform", "sentiment", "2.3"]):
        areas.append("metadata")
    if any(k in title_lower for k in ["age-rating", "age rating", "rating", "17+", "maturity", "gambling", "minor", "unrated", "agerating", "asaa"]):
        areas.append("age rating")
    if any(k in title_lower for k in ["ai", "ai-generated", "openai", "gemini", "claude", "llm", "generative", "bot"]):
        areas.append("AI disclosures")
    if any(k in title_lower for k in ["subscription", "recurring", "auto-renew", "trial", "hard-cancel", "cancellation", "pricing", "restore-purchases", "withdrawal"]):
        areas.append("subscription disclosures")
    if any(k in title_lower for k in ["payment", "billing", "in-app", "iap", "external-payment", "lootbox", "3.1.1", "3.1.2", "donation", "chargeback"]):
        areas.append("payment compliance")
    if any(k in title_lower for k in ["accessibility", "fontscaling", "highcontrast", "talkback", "voiceover", "scanner", "contrast", "dynamic-type", "reduce-motion"]):
        areas.append("accessibility")
    if any(k in title_lower for k in ["legal", "eula", "privacy-policy", "privacy policy", "ugc-24h", "withdrawal", "e-evidence", "gpsr", "lootbox", "terms"]):
        areas.append("legal documents")
    if any(k in title_lower for k in ["support-url", "support url", "unreachable-metadata-url", "contact", "e-evidence", "gpsr"]):
        areas.append("support URL")
    if any(k in title_lower for k in ["privacy-policy", "privacy policy", "missing-privacy-policy"]):
        areas.append("privacy policy")
    if any(k in title_lower for k in ["terms", "eula", "tos", "terms-of-service", "terms of service", "ugc-24h"]):
        areas.append("terms of service")
    if any(k in title_lower for k in ["export", "export-compliance", "french-encryption", "anssi"]):
        areas.append("export compliance")
    if any(k in title_lower for k in ["encryption", "export-compliance", "cipher", "crypto", "anssi"]):
        areas.append("encryption declarations")

    if not areas:
        areas.append("metadata")
        areas.append("legal documents")

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
    target_dir = ROOT
    if len(sys.argv) > 1:
        if not os.path.isdir(sys.argv[1]):
            print(f"release-audit. '{sys.argv[1]}' is not a directory.", file=sys.stderr)
            return 1
        target_dir = os.path.abspath(sys.argv[1])

    print("== Starting Release Readiness Compliance Audit ==")
    print(f"Target Directory: {target_dir}")
    print("")

    # --- Step 1. Run Internal Validation and Test Engines ---
    print("Step 1 of 2. Checking the playbook itself first. This takes about two minutes.", flush=True)

    val_code, val_out, val_err = run_command(["python3", "scripts/validate.py"])
    if val_code != 0:
        print("  ERROR: validate.py failed")
        print(val_out)
        print(val_err)
        return 1

    guard_test_code, guard_test_out, guard_test_err = run_command(
        ["bash", "agent-os/hooks/app-store-compliance-guard-test.sh"]
    )
    if guard_test_code != 0:
        print("  ERROR: compliance guard tests failed")
        print(guard_test_out)
        print(guard_test_err)
        return 1

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
    guard_code, guard_out, guard_err = run_command(
        ["bash", "agent-os/hooks/app-store-compliance-guard.sh", target_dir]
    )

    # Run metadata-audit.py
    # If en-US metadata exists, use it, otherwise let it run with default empty metadata scan
    meta_code, meta_out, meta_err = run_command(
        ["python3", "scripts/metadata-audit.py", target_dir]
    )

    # Parse findings
    patterns_dict = load_patterns()
    findings = []

    # Simple parse function for stdout of guard and metadata scripts
    all_scanner_stdout = guard_out + "\n" + meta_out
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

    # Programmatically scan for affected files
    affected_files_map = find_affected_files(target_dir, patterns_dict)

    # --- Step 3. Compile Report and Map to 15 Required Areas ---
    area_findings = {area: [] for area in REQUIRED_AREAS}
    has_critical = False

    for f in findings:
        pid = f["id"]
        sev = f["severity"]
        if sev == "critical":
            has_critical = True

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

    overall_status = (
        "BLOCKED" if has_critical else ("ADVISORY" if findings else "PASSED")
    )
    report_lines.append(f"Overall Compliance Status: {overall_status}")
    report_lines.append("")

    report_lines.append("## Executive Summary")
    if has_critical:
        report_lines.append(
            "The release is currently BLOCKED due to one or more critical compliance issues that must be resolved before submitting to the platforms."
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
            if any(af["severity"] == "critical" for af in area_f):
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
            if any(af["severity"] == "critical" for af in area_f):
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

    if has_critical:
        print("Release is BLOCKED. Resolve critical issues.")
        return 2
    else:
        print("Release is CLEAR TO SUBMIT.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
