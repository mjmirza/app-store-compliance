#!/usr/bin/env python3
"""Runs metadata/guard scans against a target project and compiles a
release-readiness report. Exits non-zero on any critical finding."""

import os
import sys
import subprocess
import json
import re
import argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

# 15 Specific App Store & Google Play Review Domains
REVIEW_DOMAINS_15 = [
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

RECOMMENDED_REVIEWERS_15 = {
    "permissions": "Lead Developer, Mobile Platform Leads",
    "privacy disclosures": "Data Protection Officer (DPO), Legal Counsel (Privacy)",
    "screenshots": "Product Marketing Manager (PMM), App Store Optimization (ASO) Specialist",
    "metadata": "Product Marketing Manager (PMM), App Store Optimization (ASO) Specialist",
    "age rating": "Compliance Officer, Product Safety Lead",
    "AI disclosures": "AI Ethics and Governance Committee, Lead AI Architect",
    "subscription disclosures": "Legal Counsel (Commercial/IP), Monetization Lead",
    "payment compliance": "Payments Lead, Finance & Legal Counsel",
    "accessibility": "Frontend QA Team, Accessibility Specialist",
    "legal documents": "Legal Counsel (Commercial/IP), Compliance Officer",
    "support URL": "Customer Support Lead, Product Marketing Manager",
    "privacy policy": "Data Protection Officer (DPO), Legal Counsel (Privacy)",
    "terms of service": "Legal Counsel (Commercial/IP), Compliance Officer",
    "export compliance": "Trade Compliance Specialist, Legal Counsel",
    "encryption declarations": "Product Security Engineering Team, Cryptography Specialist",
}

# Manual mapping of specific patterns to areas & domains
MAP_PATTERNS_TO_AREAS = {
    "APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED": ["Apple requirements", "age rating"],
    "APPLE-2.1-MISSING-DEMO-ACCOUNT": ["Apple requirements"],
    "APPLE-2.1-PLACEHOLDER-CONTENT": ["Apple requirements", "Store metadata", "metadata"],
    "APPLE-2.1-STAGING-BACKEND": ["Apple requirements", "Security"],
    "APPLE-5.1.1-MISSING-PRIVACY-POLICY": ["Apple requirements", "Privacy", "privacy policy", "privacy disclosures"],
    "APPLE-5.1.1-VAGUE-PURPOSE-STRING": ["Apple requirements", "Permissions", "permissions"],
    "APPLE-5.1.1-MISSING-USAGE-DESCRIPTION": ["Apple requirements", "Permissions", "permissions"],
    "APPLE-5.1.1-NO-ACCOUNT-DELETION": ["Apple requirements", "Privacy", "privacy policy", "privacy disclosures"],
    "APPLE-5.1.2-MISSING-ATT": ["Apple requirements", "Privacy", "privacy disclosures"],
    "APPLE-3.1.1-EXTERNAL-PAYMENT": ["Apple requirements", "SDK compatibility", "payment compliance", "subscription disclosures"],
    "APPLE-4.8-SOCIAL-LOGIN-ONLY": ["Apple requirements", "Privacy"],
    "APPLE-4.2-WEB-WRAPPER": ["Apple requirements", "Web requirements"],
    "APPLE-2.5.1-PRIVATE-API": ["Apple requirements", "Deprecated APIs", "Security"],
    "APPLE-2.3-CROSS-PLATFORM-REFERENCE": ["Apple requirements", "Store metadata", "metadata"],
    "APPLE-2.3-AGE-RATING-2026": ["Apple requirements", "Platform announcements", "age rating"],
    "APPLE-5.1.2-AI-NO-CONSENT-MODAL": [
        "Apple requirements",
        "AI regulations",
        "Privacy",
        "AI disclosures",
        "privacy disclosures",
    ],
    "GOOGLE-DATASAFETY-MISMATCH": ["Google Play requirements", "Privacy", "privacy disclosures"],
    "GOOGLE-PERM-BACKGROUND-LOCATION": ["Google Play requirements", "Permissions", "permissions"],
    "GOOGLE-PERM-ALL-FILES": ["Google Play requirements", "Permissions", "permissions"],
    "GOOGLE-PERM-SMS-CALLLOG": ["Google Play requirements", "Permissions", "permissions"],
    "GOOGLE-PERM-ACCESSIBILITY-MISUSE": ["Google Play requirements", "Accessibility", "accessibility"],
    "GOOGLE-TARGET-API": ["Google Play requirements", "Platform announcements"],
    "GOOGLE-12-TESTER-RULE": ["Google Play requirements", "Platform announcements"],
    "GOOGLE-PLAY-BILLING": ["Google Play requirements", "SDK compatibility", "payment compliance", "subscription disclosures"],
    "GOOGLE-MISSING-PRIVACY-POLICY": ["Google Play requirements", "Privacy", "privacy policy", "privacy disclosures"],
    "GOOGLE-MISLEADING-LISTING": ["Google Play requirements", "Store metadata", "metadata"],
    "GOOGLE-FAMILIES-AD-SDK": ["Google Play requirements", "SDK compatibility"],
    "BOTH-SDK-SUPPLY-CHAIN": ["SDK compatibility"],
    "BOTH-LOOTBOX-ODDS": ["Legal documentation", "legal documents", "payment compliance"],
    "APPLE-PRIVACY-MANIFEST-MISSING": ["Apple requirements", "Privacy", "privacy disclosures"],
    "APPLE-EXPORT-COMPLIANCE-MISSING": ["Apple requirements", "Legal documentation", "export compliance", "encryption declarations"],
    "APPLE-RESTORE-PURCHASES-MISSING": ["Apple requirements", "payment compliance", "subscription disclosures"],
    "APPLE-ACCOUNT-DELETION-WEAK": ["Apple requirements", "Privacy", "privacy policy"],
    "ANDROID-DYNAMIC-CODE-LOADING": ["Google Play requirements", "Security"],
    "ANDROID-QUERY-ALL-PACKAGES": ["Google Play requirements", "Permissions", "permissions"],
    "ANDROID-OVERLAY-TAPJACKING": ["Google Play requirements", "Security"],
    "ANDROID-ACCOUNT-DELETION-URL": ["Google Play requirements", "Privacy", "privacy policy"],
    "BOTH-AI-GENERATED-CONTENT": ["AI regulations", "AI disclosures"],
    "BOTH-METADATA-DECORATION": ["Store metadata", "metadata"],
    "BOTH-FINGERPRINTING": ["Privacy", "Security", "privacy disclosures"],
    "APPLE-2.3-FUTURE-FUNCTIONALITY": ["Apple requirements", "Store metadata", "metadata"],
    "APPLE-2.3-NEGATIVE-APPLE-SENTIMENT": ["Apple requirements", "Store metadata", "metadata"],
    "BOTH-UNREACHABLE-METADATA-URL": ["Store metadata", "support URL", "privacy policy", "metadata"],
    "APPLE-5.2.5-APPLE-DEVICE-IMAGE": ["Apple requirements", "Store metadata", "metadata", "screenshots"],
    "APPLE-2.3.4-DEVICE-FRAMES-PREVIEW": ["Apple requirements", "Store metadata", "metadata", "screenshots"],
    "APPLE-3.1.2-MISLEADING-PRICING": ["Apple requirements", "Store metadata", "subscription disclosures", "payment compliance", "terms of service"],
    "APPLE-1.2-UGC-24H-ACTION": ["Apple requirements", "Legal documentation", "legal documents", "terms of service"],
    "CHINA-AI-REFERENCES": ["AI regulations", "AI disclosures"],
    "APPLE-2.4.5-UNUSED-ENTITLEMENTS": ["Apple requirements"],
    "APPLE-4.0-SIWA-UX": ["Apple requirements"],
    "APPLE-5.1.1-UNNECESSARY-DATA": ["Apple requirements", "Privacy", "privacy disclosures"],
    "APPLE-2.1-DEBUG-FEATURES": ["Apple requirements", "Security"],
    "APPLE-2.1-CLOUD-NOT-IN-PRODUCTION": ["Apple requirements"],
    "APPLE-2.1-REVIEW-NOTES-INCOMPLETE": ["Apple requirements", "Store metadata", "metadata"],
    "BOTH-PLACEHOLDER": ["Store metadata", "metadata", "screenshots", "support URL"],
    "BOTH-SUBSCRIPTION-HARD-CANCEL": ["Apple requirements", "Google Play requirements", "AI regulations", "subscription disclosures", "payment compliance", "terms of service"],
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
        areas.extend(["Privacy", "privacy disclosures", "privacy policy"])
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
        areas.extend(["Accessibility", "accessibility"])
    if (
        "ai" in title_lower
        or "openai" in title_lower
        or "gemini" in title_lower
        or "claude" in title_lower
    ):
        areas.extend(["AI regulations", "AI disclosures"])
    if (
        "metadata" in title_lower
        or "placeholder" in title_lower
        or "future-func" in title_lower
        or "unreachable" in title_lower
    ):
        areas.extend(["Store metadata", "metadata"])
    if "perm" in title_lower or "usage-description" in title_lower:
        areas.extend(["Permissions", "permissions"])
    if "billing" in title_lower or "payment" in title_lower or "sdk" in title_lower:
        areas.extend(["SDK compatibility", "payment compliance", "subscription disclosures"])

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

                has_signal = False
                if pid == "BOTH-PLACEHOLDER":
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
                        if (
                            "rejection-patterns.json" not in rel_path
                            and "release-audit.py" not in rel_path
                            and "app-store-compliance-guard.sh" not in rel_path
                            and "RELEASE-READINESS-REPORT.md" not in rel_path
                            and "RELEASE-REVIEW-REPORT" not in rel_path
                        ):
                            affected[pid].append(rel_path)

    return affected


def main():
    parser = argparse.ArgumentParser(description="Runs release readiness compliance audit.")
    parser.add_argument("target_dir", nargs="?", default=ROOT, help="Target directory to audit")
    parser.add_argument("--report-out", dest="report_out", default=None, help="Output file path for the release review report")
    args = parser.parse_args()

    target_dir = os.path.abspath(args.target_dir)

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
    meta_code, meta_out, meta_err = run_command(
        ["python3", "scripts/metadata-audit.py", target_dir]
    )

    # Parse findings
    patterns_dict = load_patterns()
    findings = []

    all_scanner_stdout = guard_out + "\n" + meta_out
    lines = all_scanner_stdout.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        # Ignore absorbed deadline notices
        if "absorbed into" in line and "(mandatory " in line:
            i += 1
            continue
        match = re.match(
            r"^\s*\[(CRITICAL|HIGH|MEDIUM|LOW)\]\s+([A-Z0-9-._]+)\s+(.+)$",
            line,
            re.IGNORECASE,
        )
        if match and "-" not in match.group(2):
            match = None
        if match:
            sev = match.group(1).lower()
            pid = match.group(2)
            title = match.group(3).strip()
            title = re.sub(r"\s*\([^)]+\)$", "", title)

            fix = ""
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                fix_match = re.match(r"^\s*fix\.\s+(.+)$", next_line, re.IGNORECASE)
                if fix_match:
                    fix = fix_match.group(1).strip()
                    i += 1

            if not any(f["id"] == pid for f in findings):
                findings.append(
                    {"id": pid, "severity": sev, "title": title, "fix": fix}
                )
        i += 1

    affected_files_map = find_affected_files(target_dir, patterns_dict)

    # --- Step 3. Compile Report ---
    all_known_areas = REQUIRED_AREAS + REVIEW_DOMAINS_15
    area_findings = {area: [] for area in all_known_areas}
    has_critical = False

    for f in findings:
        pid = f["id"]
        sev = f["severity"]
        if sev == "critical":
            has_critical = True

        areas = get_areas_for_pattern(pid, patterns_dict)
        for area in areas:
            if area in area_findings:
                area_findings[area].append(f)

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

    report_lines.append("## Compliance Summary Table (13 Required Areas)")
    report_lines.append("")
    report_lines.append("| Area | Status | Risks Found | Recommended Reviewers |")
    report_lines.append("| --- | --- | --- | --- |")

    for area in REQUIRED_AREAS:
        area_f = area_findings[area]
        area_status = "PASSED"
        if area_f:
            if any(af["severity"] == "critical" for af in area_f):
                area_status = "BLOCKED"
            else:
                area_status = "ADVISORY"

        num_risks = len(area_f)
        reviewers = RECOMMENDED_REVIEWERS.get(area, "Lead Developer")
        report_lines.append(f"| {area} | {area_status} | {num_risks} | {reviewers} |")
    report_lines.append("")

    report_lines.append("## App Store & Google Play Review Domains (15 Verification Areas)")
    report_lines.append("")
    report_lines.append("| Domain | Status | Risks Found | Recommended Reviewers |")
    report_lines.append("| --- | --- | --- | --- |")

    for domain in REVIEW_DOMAINS_15:
        dom_f = area_findings[domain]
        dom_status = "PASSED"
        if dom_f:
            if any(af["severity"] == "critical" for af in dom_f):
                dom_status = "BLOCKED"
            else:
                dom_status = "ADVISORY"

        num_risks = len(dom_f)
        reviewers = RECOMMENDED_REVIEWERS_15.get(domain, "Lead Developer")
        report_lines.append(f"| {domain} | {dom_status} | {num_risks} | {reviewers} |")
    report_lines.append("")

    report_lines.append("## Detailed Compliance Analysis (13 Required Areas)")
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

            aff_files = affected_files_map.get(pid, [])
            if not aff_files:
                files_str = "None detected (Config/Listing check)"
            else:
                files_str = "<br>".join(aff_files[:5])
                if len(aff_files) > 5:
                    files_str += f"<br>... and {len(aff_files) - 5} more files"

            report_lines.append(f"| {pid} | {sev} | {title} | {fix} | {files_str} |")
        report_lines.append("")

    report_lines.append("## Detailed Analysis of 15 Verification Review Domains")
    report_lines.append("")

    for idx, domain in enumerate(REVIEW_DOMAINS_15, 1):
        dom_f = area_findings[domain]
        dom_status = "PASSED"
        if dom_f:
            if any(af["severity"] == "critical" for af in dom_f):
                dom_status = "BLOCKED"
            else:
                dom_status = "ADVISORY"

        report_lines.append(f"### {idx}. {domain}")
        report_lines.append(f"- Status: {dom_status}")
        report_lines.append(
            f"- Recommended Reviewers: {RECOMMENDED_REVIEWERS_15.get(domain, 'Lead Developer')}"
        )
        report_lines.append("")

        if not dom_f:
            report_lines.append(f"No outstanding risks found for domain: {domain}.")
            report_lines.append("")
            continue

        report_lines.append(
            "| Finding ID | Severity | Description | Required Action | Affected Files |"
        )
        report_lines.append("| --- | --- | --- | --- | --- |")

        for af in dom_f:
            pid = af["id"]
            sev = af["severity"].upper()
            title = af["title"]
            fix = af["fix"] or "Refer to guidelines for remediation."

            aff_files = affected_files_map.get(pid, [])
            if not aff_files:
                files_str = "None detected (Config/Listing check)"
            else:
                files_str = "<br>".join(aff_files[:5])
                if len(aff_files) > 5:
                    files_str += f"<br>... and {len(aff_files) - 5} more files"

            report_lines.append(f"| {pid} | {sev} | {title} | {fix} | {files_str} |")
        report_lines.append("")

    report_content = "\n".join(report_lines) + "\n"

    # Write primary report in target directory
    report_path = os.path.join(target_dir, "RELEASE-READINESS-REPORT.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    # Write explicit --report-out file if specified
    if args.report_out:
        out_path = os.path.abspath(args.report_out)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"Custom release review report generated successfully at: {out_path}")

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
