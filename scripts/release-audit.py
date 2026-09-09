#!/usr/bin/env python3
"""Runs metadata/guard scans against a target project and compiles a
release-readiness report. Exits non-zero on any critical finding."""

import os
import sys
import subprocess
import json
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 15 Required review domains
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

# Recommended reviewers for each domain
RECOMMENDED_REVIEWERS = {
    "permissions": "Lead Developer, Mobile Platform Leads",
    "privacy disclosures": "Data Protection Officer (DPO), Legal Counsel (Privacy)",
    "screenshots": "Product Marketing Manager (PMM), App Store Optimization (ASO) Specialist",
    "metadata": "Product Marketing Manager (PMM), App Store Optimization (ASO) Specialist",
    "age rating": "Compliance Officer, Product Manager",
    "AI disclosures": "AI Ethics and Governance Committee, Lead AI Architect",
    "subscription disclosures": "Growth Lead, Legal Counsel (Commercial)",
    "payment compliance": "Mobile Tech Lead, Payment Integration Specialist",
    "accessibility": "Frontend QA Team, Accessibility Specialist",
    "legal documents": "Legal Counsel (Commercial/IP), Compliance Officer",
    "support URL": "Customer Support Lead, Web Master",
    "privacy policy": "Data Protection Officer (DPO), Legal Counsel (Privacy)",
    "terms of service": "Legal Counsel (Commercial/IP)",
    "export compliance": "Trade Compliance Officer, Legal Counsel",
    "encryption declarations": "Security Lead, iOS Platform Architect",
}

# Manual mapping of specific patterns to review domains
MAP_PATTERNS_TO_AREAS = {
    "APPLE-2.1-MISSING-DEMO-ACCOUNT": ["metadata"],
    "APPLE-2.1-PLACEHOLDER-CONTENT": ["metadata", "screenshots"],
    "APPLE-2.1-STAGING-BACKEND": ["metadata"],
    "APPLE-5.1.1-MISSING-PRIVACY-POLICY": ["privacy policy"],
    "APPLE-5.1.1-VAGUE-PURPOSE-STRING": ["permissions"],
    "APPLE-5.1.1-MISSING-USAGE-DESCRIPTION": ["permissions"],
    "APPLE-5.1.1-NO-ACCOUNT-DELETION": ["privacy disclosures"],
    "APPLE-5.1.2-MISSING-ATT": ["privacy disclosures"],
    "APPLE-3.1.1-EXTERNAL-PAYMENT": ["payment compliance"],
    "APPLE-4.8-SOCIAL-LOGIN-ONLY": ["privacy disclosures"],
    "APPLE-4.2-WEB-WRAPPER": ["metadata"],
    "APPLE-2.5.1-PRIVATE-API": ["permissions"],
    "APPLE-2.3-CROSS-PLATFORM-REFERENCE": ["metadata"],
    "APPLE-2.3-AGE-RATING-2026": ["age rating"],
    "APPLE-5.1.2-AI-NO-CONSENT-MODAL": ["AI disclosures", "privacy disclosures"],
    "GOOGLE-DATASAFETY-MISMATCH": ["privacy disclosures"],
    "GOOGLE-PERM-BACKGROUND-LOCATION": ["permissions"],
    "GOOGLE-PERM-ALL-FILES": ["permissions"],
    "GOOGLE-PERM-SMS-CALLLOG": ["permissions"],
    "GOOGLE-PERM-ACCESSIBILITY-MISUSE": ["accessibility"],
    "GOOGLE-TARGET-API": ["metadata"],
    "GOOGLE-12-TESTER-RULE": ["metadata"],
    "GOOGLE-PLAY-BILLING": ["payment compliance"],
    "GOOGLE-MISSING-PRIVACY-POLICY": ["privacy policy"],
    "GOOGLE-MISLEADING-LISTING": ["metadata"],
    "GOOGLE-FAMILIES-AD-SDK": ["privacy disclosures"],
    "BOTH-SDK-SUPPLY-CHAIN": ["privacy disclosures"],
    "BOTH-LOOTBOX-ODDS": ["legal documents"],
    "APPLE-PRIVACY-MANIFEST-MISSING": ["privacy disclosures"],
    "APPLE-EXPORT-COMPLIANCE-MISSING": ["export compliance"],
    "APPLE-RESTORE-PURCHASES-MISSING": ["payment compliance"],
    "APPLE-ACCOUNT-DELETION-WEAK": ["privacy disclosures"],
    "ANDROID-DYNAMIC-CODE-LOADING": ["permissions"],
    "ANDROID-QUERY-ALL-PACKAGES": ["permissions"],
    "ANDROID-OVERLAY-TAPJACKING": ["permissions"],
    "ANDROID-ACCOUNT-DELETION-URL": ["privacy disclosures"],
    "BOTH-AI-GENERATED-CONTENT": ["AI disclosures"],
    "BOTH-METADATA-DECORATION": ["metadata"],
    "BOTH-FINGERPRINTING": ["privacy disclosures"],
    "APPLE-2.3-FUTURE-FUNCTIONALITY": ["metadata"],
    "APPLE-2.3-NEGATIVE-APPLE-SENTIMENT": ["metadata"],
    "BOTH-UNREACHABLE-METADATA-URL": ["support URL"],
    "APPLE-5.2.5-APPLE-DEVICE-IMAGE": ["screenshots"],
    "APPLE-2.3.4-DEVICE-FRAMES-PREVIEW": ["screenshots"],
    "APPLE-3.1.2-MISLEADING-PRICING": ["subscription disclosures"],
    "BOTH-SUBSCRIPTION-HARD-CANCEL": ["subscription disclosures"],
    "APPLE-1.2-UGC-24H-ACTION": ["terms of service", "legal documents"],
    "CHINA-AI-REFERENCES": ["AI disclosures"],
    "APPLE-2.4.5-UNUSED-ENTITLEMENTS": ["permissions"],
    "APPLE-4.0-SIWA-UX": ["privacy disclosures"],
    "APPLE-5.1.1-UNNECESSARY-DATA": ["privacy disclosures"],
    "APPLE-2.1-DEBUG-FEATURES": ["metadata"],
    "APPLE-2.1-CLOUD-NOT-IN-PRODUCTION": ["metadata"],
    "APPLE-2.1-REVIEW-NOTES-INCOMPLETE": ["metadata"],
    "APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED": ["age rating"],
    "BOTH-PLACEHOLDER": ["metadata"],
}


def run_command(args, cwd=ROOT):
    try:
        res = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
        return res.returncode, res.stdout, res.stderr
    except Exception as e:
        return -1, "", str(e)


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
    title_lower = pdata.get("title", "").lower() + " " + pid.lower()

    areas = []
    if "perm" in title_lower or "usage-description" in title_lower:
        areas.append("permissions")
    if "privacy-policy" in title_lower or "missing-privacy-policy" in title_lower:
        areas.append("privacy policy")
    elif "privacy" in title_lower or "data-safety" in title_lower or "tracking" in title_lower or "fingerprinting" in title_lower:
        areas.append("privacy disclosures")
    if "screenshot" in title_lower or "device-image" in title_lower or "device-frame" in title_lower:
        areas.append("screenshots")
    if "age" in title_lower or "rating" in title_lower or "minor" in title_lower or "child" in title_lower:
        areas.append("age rating")
    if "ai" in title_lower or "openai" in title_lower or "gemini" in title_lower or "claude" in title_lower:
        areas.append("AI disclosures")
    if "subscr" in title_lower or "renew" in title_lower or "hard-cancel" in title_lower:
        areas.append("subscription disclosures")
    if "billing" in title_lower or "payment" in title_lower or "external-payment" in title_lower or "restore" in title_lower:
        areas.append("payment compliance")
    if "accessibility" in title_lower:
        areas.append("accessibility")
    if "legal" in title_lower or "lootbox" in title_lower or "dsa" in title_lower or "licens" in title_lower:
        areas.append("legal documents")
    if "support" in title_lower or "unreachable" in title_lower or "url" in title_lower:
        areas.append("support URL")
    if "terms" in title_lower or "eula" in title_lower or "tos" in title_lower:
        areas.append("terms of service")
    if "export" in title_lower:
        areas.append("export compliance")
    if "encrypt" in title_lower or "anssi" in title_lower:
        areas.append("encryption declarations")
    if "metadata" in title_lower or "placeholder" in title_lower or "future-func" in title_lower:
        areas.append("metadata")

    if not areas:
        areas.append("metadata")

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
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        target_dir = os.path.abspath(sys.argv[1])

    print("== Starting Release Readiness Compliance Audit ==")
    print(f"Target Directory: {target_dir}")
    print("")

    # --- Step 1. Run Internal Validation and Test Engines ---
    print("Running internal validation and test engines...")

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
    print("Executing compliance scanners on target...")

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
        match = re.match(
            r"^\s*\[(CRITICAL|HIGH|MEDIUM|LOW)\]\s+([A-Z0-9-._]+)\s+(.+)$",
            line,
            re.IGNORECASE,
        )
        if match:
            sev = match.group(1).lower()
            pid = match.group(2)
            title = match.group(3).strip()
            # Trim trailing (field) suffix in case of metadata-audit format
            title = re.sub(r"\s*\([^)]+\)$", "", title)

            fix = ""
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

    # --- Step 3. Compile Report and Map to 13 Areas ---
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

    # Also update docs/RELEASE-REVIEW-REPORT-2026.md in the repo
    doc_report_path = os.path.join(ROOT, "docs", "RELEASE-REVIEW-REPORT-2026.md")
    os.makedirs(os.path.dirname(doc_report_path), exist_ok=True)
    with open(doc_report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

    print(f"Release readiness report generated successfully at: {report_path}")
    print(f"Release review report updated at: {doc_report_path}")
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
