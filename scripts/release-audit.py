#!/usr/bin/env python3
"""Runs metadata/guard scans against a target project and compiles a
release-readiness report across 15 review domains. Exits non-zero on any critical finding."""

import os
import sys
import subprocess
import json
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 15 Required App Store and Google Play Review Domains
REQUIRED_AREAS = [
    "Permissions",
    "Privacy disclosures",
    "Screenshots",
    "Metadata",
    "Age rating",
    "AI disclosures",
    "Subscription disclosures",
    "Payment compliance",
    "Accessibility",
    "Legal documents",
    "Support URL",
    "Privacy policy",
    "Terms of service",
    "Export compliance",
    "Encryption declarations",
]

# Recommended reviewers for each area
RECOMMENDED_REVIEWERS = {
    "Permissions": "Lead Mobile Developer, Platform Security Lead",
    "Privacy disclosures": "Data Protection Officer (DPO), Legal Counsel (Privacy)",
    "Screenshots": "App Store Optimization (ASO) Specialist, Product Designer",
    "Metadata": "Product Marketing Manager (PMM), ASO Specialist",
    "Age rating": "Content Ratings Officer, Legal Counsel",
    "AI disclosures": "AI Ethics and Governance Committee, Lead AI Architect",
    "Subscription disclosures": "Monetization Lead, Product Legal Counsel",
    "Payment compliance": "Fintech Architect, Payment Operations Lead",
    "Accessibility": "Accessibility Specialist, Frontend QA Lead",
    "Legal documents": "Legal Counsel (Commercial/IP), Compliance Officer",
    "Support URL": "Customer Support Operations Lead, Web Admin",
    "Privacy policy": "Data Protection Officer (DPO), Compliance Lead",
    "Terms of service": "Legal Counsel (Commercial), Product Lead",
    "Export compliance": "Global Trade & Export Compliance Officer",
    "Encryption declarations": "Security Engineering Lead, Cryptography Specialist",
}

# Manual mapping of specific patterns to 15 review domains
MAP_PATTERNS_TO_AREAS = {
    "APPLE-2.1-MISSING-DEMO-ACCOUNT": ["Metadata"],
    "APPLE-2.1-PLACEHOLDER-CONTENT": ["Metadata"],
    "APPLE-2.1-STAGING-BACKEND": ["Metadata"],
    "APPLE-5.1.1-MISSING-PRIVACY-POLICY": ["Privacy policy"],
    "APPLE-5.1.1-VAGUE-PURPOSE-STRING": ["Permissions"],
    "APPLE-5.1.1-MISSING-USAGE-DESCRIPTION": ["Permissions"],
    "APPLE-5.1.1-NO-ACCOUNT-DELETION": ["Privacy policy"],
    "APPLE-5.1.2-MISSING-ATT": ["Privacy disclosures"],
    "APPLE-3.1.1-EXTERNAL-PAYMENT": ["Payment compliance"],
    "APPLE-4.8-SOCIAL-LOGIN-ONLY": ["Privacy disclosures"],
    "APPLE-4.2-WEB-WRAPPER": ["Metadata"],
    "APPLE-2.5.1-PRIVATE-API": ["Metadata"],
    "APPLE-2.3-CROSS-PLATFORM-REFERENCE": ["Metadata"],
    "APPLE-2.3-AGE-RATING-2026": ["Age rating"],
    "APPLE-5.1.2-AI-NO-CONSENT-MODAL": ["AI disclosures", "Privacy disclosures"],
    "GOOGLE-DATASAFETY-MISMATCH": ["Privacy disclosures"],
    "GOOGLE-PERM-BACKGROUND-LOCATION": ["Permissions"],
    "GOOGLE-PERM-ALL-FILES": ["Permissions"],
    "GOOGLE-PERM-SMS-CALLLOG": ["Permissions"],
    "GOOGLE-PERM-ACCESSIBILITY-MISUSE": ["Accessibility"],
    "GOOGLE-TARGET-API": ["Metadata"],
    "GOOGLE-12-TESTER-RULE": ["Metadata"],
    "GOOGLE-PLAY-BILLING": ["Payment compliance"],
    "GOOGLE-MISSING-PRIVACY-POLICY": ["Privacy policy"],
    "GOOGLE-MISLEADING-LISTING": ["Metadata"],
    "GOOGLE-FAMILIES-AD-SDK": ["Privacy disclosures"],
    "BOTH-SDK-SUPPLY-CHAIN": ["Privacy disclosures"],
    "BOTH-LOOTBOX-ODDS": ["Legal documents"],
    "APPLE-PRIVACY-MANIFEST-MISSING": ["Privacy disclosures"],
    "APPLE-EXPORT-COMPLIANCE-MISSING": ["Export compliance", "Encryption declarations"],
    "APPLE-RESTORE-PURCHASES-MISSING": ["Payment compliance"],
    "APPLE-ACCOUNT-DELETION-WEAK": ["Privacy policy"],
    "ANDROID-DYNAMIC-CODE-LOADING": ["Metadata"],
    "ANDROID-QUERY-ALL-PACKAGES": ["Permissions"],
    "ANDROID-OVERLAY-TAPJACKING": ["Metadata"],
    "ANDROID-ACCOUNT-DELETION-URL": ["Privacy policy"],
    "BOTH-AI-GENERATED-CONTENT": ["AI disclosures"],
    "BOTH-METADATA-DECORATION": ["Metadata"],
    "BOTH-FINGERPRINTING": ["Privacy disclosures"],
    "APPLE-2.3-FUTURE-FUNCTIONALITY": ["Metadata"],
    "APPLE-2.3-NEGATIVE-APPLE-SENTIMENT": ["Metadata"],
    "BOTH-UNREACHABLE-METADATA-URL": ["Support URL", "Privacy policy", "Terms of service"],
    "APPLE-5.2.5-APPLE-DEVICE-IMAGE": ["Screenshots", "Metadata"],
    "APPLE-2.3.4-DEVICE-FRAMES-PREVIEW": ["Screenshots", "Metadata"],
    "APPLE-3.1.2-MISLEADING-PRICING": ["Subscription disclosures", "Terms of service"],
    "APPLE-1.2-UGC-24H-ACTION": ["Legal documents", "Terms of service"],
    "CHINA-AI-REFERENCES": ["AI disclosures"],
    "APPLE-2.4.5-UNUSED-ENTITLEMENTS": ["Metadata"],
    "APPLE-4.0-SIWA-UX": ["Metadata"],
    "APPLE-5.1.1-UNNECESSARY-DATA": ["Privacy disclosures"],
    "APPLE-2.1-DEBUG-FEATURES": ["Metadata"],
    "APPLE-2.1-CLOUD-NOT-IN-PRODUCTION": ["Metadata"],
    "APPLE-2.1-REVIEW-NOTES-INCOMPLETE": ["Metadata"],
    "BOTH-SUBSCRIPTION-HARD-CANCEL": ["Subscription disclosures", "Terms of service"],
    "BOTH-PLACEHOLDER": ["Metadata"],
    "BOTH-E-EVIDENCE-COMPLIANCE-MISSING": ["Legal documents"],
    "BOTH-GPSR-COMPLIANCE-MISSING": ["Legal documents"],
    "BOTH-WITHDRAWAL-BUTTON-MISSING": ["Terms of service", "Subscription disclosures"],
    "BOTH-US-ASAA-AGE-SIGNALS-MISSING": ["Age rating", "Legal documents"],
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
    title_lower = (pdata.get("title", "") + " " + pid).lower()

    areas = []
    if "perm" in title_lower or "usage-description" in title_lower or "location" in title_lower:
        areas.append("Permissions")
    if "privacy" in title_lower or "data" in title_lower or "tracking" in title_lower or "manifest" in title_lower:
        areas.append("Privacy disclosures")
    if "screenshot" in title_lower or "image" in title_lower or "preview" in title_lower:
        areas.append("Screenshots")
    if "metadata" in title_lower or "placeholder" in title_lower or "future-func" in title_lower:
        areas.append("Metadata")
    if "age" in title_lower or "rating" in title_lower or "child" in title_lower:
        areas.append("Age rating")
    if "ai" in title_lower or "llm" in title_lower or "generative" in title_lower:
        areas.append("AI disclosures")
    if "subscription" in title_lower or "pricing" in title_lower or "cancel" in title_lower:
        areas.append("Subscription disclosures")
    if "pay" in title_lower or "billing" in title_lower or "purchase" in title_lower or "restore" in title_lower:
        areas.append("Payment compliance")
    if "accessibility" in title_lower or "voiceover" in title_lower or "talkback" in title_lower:
        areas.append("Accessibility")
    if "legal" in title_lower or "e-evidence" in title_lower or "gpsr" in title_lower or "lootbox" in title_lower:
        areas.append("Legal documents")
    if "url" in title_lower or "support" in title_lower or "contact" in title_lower:
        areas.append("Support URL")
    if "privacy policy" in title_lower or "policy" in title_lower:
        areas.append("Privacy policy")
    if "terms" in title_lower or "tos" in title_lower or "eula" in title_lower:
        areas.append("Terms of service")
    if "export" in title_lower:
        areas.append("Export compliance")
    if "encryption" in title_lower:
        areas.append("Encryption declarations")

    if not areas:
        areas.append("Metadata")

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
                            and "RELEASE-REVIEW-REPORT-2026.md" not in rel_path
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

    guard_code, guard_out, guard_err = run_command(
        ["bash", "agent-os/hooks/app-store-compliance-guard.sh", target_dir]
    )

    meta_code, meta_out, meta_err = run_command(
        ["python3", "scripts/metadata-audit.py", target_dir]
    )

    patterns_dict = load_patterns()
    findings = []

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

    # --- Step 3. Compile Report and Map to 15 Areas ---
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

            aff_files = affected_files_map.get(pid, [])
            if not aff_files:
                files_str = "None detected (Config/Listing check)"
            else:
                files_str = "<br>".join(aff_files[:5])
                if len(aff_files) > 5:
                    files_str += f"<br>... and {len(aff_files) - 5} more files"

            report_lines.append(f"| {pid} | {sev} | {title} | {fix} | {files_str} |")
        report_lines.append("")

    # Write report file into the audited target
    report_path = os.path.join(target_dir, "RELEASE-READINESS-REPORT.md")
    report_content = "\n".join(report_lines) + "\n"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    # Also update docs/RELEASE-REVIEW-REPORT-2026.md in repo root if docs directory exists
    docs_dir = os.path.join(ROOT, "docs")
    if os.path.isdir(docs_dir):
        doc_report_path = os.path.join(docs_dir, "RELEASE-REVIEW-REPORT-2026.md")
        doc_report_lines = report_lines.copy()
        doc_report_lines[0] = "# Pre-Release Compliance Review Report (2026)"
        with open(doc_report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(doc_report_lines) + "\n")

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
