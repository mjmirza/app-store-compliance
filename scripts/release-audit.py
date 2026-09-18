#!/usr/bin/env python3
"""Runs metadata/guard scans against a target project and compiles
release-readiness reports. Exits non-zero on any critical finding."""

import os
import sys
import subprocess
import json
import re
import argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 13 Required compliance areas
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

# 15 Specific App Store & Google Play review domains
REVIEW_DOMAINS = [
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

# Recommended reviewers for compliance areas
RECOMMENDED_REVIEWERS_AREAS = {
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

# Recommended reviewers for the 15 review domains
RECOMMENDED_REVIEWERS_DOMAINS = {
    "permissions": "Lead Developer, Mobile Platform Leads",
    "privacy disclosures": "Data Protection Officer (DPO), Privacy Counsel",
    "screenshots": "Product Marketing Manager (PMM), ASO Specialist",
    "metadata": "Product Marketing Manager (PMM), Brand Specialist",
    "age rating": "Legal Counsel, Compliance Officer",
    "AI disclosures": "AI Ethics and Governance Committee, Lead AI Architect",
    "subscription disclosures": "Monetization PM, Legal Counsel",
    "payment compliance": "Finance Lead, Payments Architect",
    "accessibility": "Accessibility Specialist, Frontend QA Lead",
    "legal documents": "Legal Counsel (Commercial/IP), Compliance Officer",
    "support URL": "Customer Support Lead, Operations Manager",
    "privacy policy": "Data Protection Officer (DPO), Legal Counsel",
    "terms of service": "Legal Counsel, Commercial Director",
    "export compliance": "Trade Compliance Officer, Security Lead",
    "encryption declarations": "InfoSec Lead, Security Architect",
}

# Mapping review domains to primary verification scripts
DOMAIN_MAPPED_SCRIPTS = {
    "permissions": "agent-os/hooks/app-store-compliance-guard.sh",
    "privacy disclosures": "agent-os/hooks/app-store-compliance-guard.sh",
    "screenshots": "docs/PRE-SUBMISSION-CHECKLIST.md",
    "metadata": "scripts/metadata-audit.py",
    "age rating": "agent-os/hooks/app-store-compliance-guard.sh",
    "AI disclosures": "agent-os/hooks/app-store-compliance-guard.sh",
    "subscription disclosures": "scripts/metadata-audit.py",
    "payment compliance": "agent-os/hooks/app-store-compliance-guard.sh",
    "accessibility": "scripts/accessibility-audit.py",
    "legal documents": "scripts/deadline-checker.py",
    "support URL": "scripts/metadata-audit.py",
    "privacy policy": "scripts/metadata-audit.py",
    "terms of service": "scripts/metadata-audit.py",
    "export compliance": "agent-os/hooks/app-store-compliance-guard.sh",
    "encryption declarations": "agent-os/hooks/app-store-compliance-guard.sh",
}

# Mapping specific pattern IDs to 13 areas
MAP_PATTERNS_TO_AREAS = {
    "APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED": ["Apple requirements", "Deprecated APIs", "Platform announcements"],
    "BOTH-PLACEHOLDER": ["Store metadata", "Apple requirements", "Google Play requirements"],
    "BOTH-SUBSCRIPTION-HARD-CANCEL": ["Apple requirements", "Google Play requirements", "Legal documentation", "AI regulations"],
    "APPLE-2.3-FUTURE-FUNCTIONALITY": ["Apple requirements", "Store metadata"],
    "APPLE-2.3-NEGATIVE-APPLE-SENTIMENT": ["Apple requirements", "Store metadata"],
    "APPLE-2.3-CROSS-PLATFORM-REFERENCE": ["Apple requirements", "Store metadata"],
    "BOTH-LOOTBOX-ODDS": ["Legal documentation", "Apple requirements", "Google Play requirements"],
    "BOTH-MISSING-PRIVACY-POLICY": ["Privacy", "Store metadata", "Apple requirements", "Google Play requirements"],
}

# Mapping specific pattern IDs to 15 domains
MAP_PATTERNS_TO_DOMAINS = {
    "APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED": ["age rating"],
    "BOTH-PLACEHOLDER": ["metadata", "screenshots"],
    "BOTH-SUBSCRIPTION-HARD-CANCEL": ["subscription disclosures", "payment compliance", "terms of service"],
    "APPLE-2.3-FUTURE-FUNCTIONALITY": ["metadata"],
    "APPLE-2.3-NEGATIVE-APPLE-SENTIMENT": ["metadata"],
    "APPLE-2.3-CROSS-PLATFORM-REFERENCE": ["metadata"],
    "BOTH-LOOTBOX-ODDS": ["legal documents", "payment compliance"],
    "BOTH-MISSING-PRIVACY-POLICY": ["privacy policy", "privacy disclosures", "metadata"],
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

    if "privacy" in title_lower or "data-safety" in title_lower or "tracking" in title_lower or "fingerprinting" in title_lower:
        areas.append("Privacy")
    if "security" in title_lower or "staging" in title_lower or "backend" in title_lower or "private-api" in title_lower or "overlay" in title_lower or "dynamic" in title_lower:
        areas.append("Security")
    if "accessibility" in title_lower:
        areas.append("Accessibility")
    if "ai" in title_lower or "openai" in title_lower or "gemini" in title_lower or "claude" in title_lower:
        areas.append("AI regulations")
    if "metadata" in title_lower or "placeholder" in title_lower or "future-func" in title_lower or "unreachable" in title_lower:
        areas.append("Store metadata")
    if "perm" in title_lower or "usage-description" in title_lower:
        areas.append("Permissions")
    if "billing" in title_lower or "payment" in title_lower or "sdk" in title_lower:
        areas.append("SDK compatibility")

    if not areas:
        areas.append("Apple requirements")
        areas.append("Google Play requirements")

    return list(set(areas))


def get_domains_for_pattern(pid, patterns_dict):
    if pid in MAP_PATTERNS_TO_DOMAINS:
        return MAP_PATTERNS_TO_DOMAINS[pid]

    pdata = patterns_dict.get(pid, {})
    title_lower = pdata.get("title", "").lower() + " " + pid.lower()

    domains = []
    if "perm" in title_lower or "usage-description" in title_lower:
        domains.append("permissions")
    if "privacy" in title_lower or "att" in title_lower or "data-safety" in title_lower or "tracking" in title_lower:
        domains.append("privacy disclosures")
        domains.append("privacy policy")
    if "screenshot" in title_lower or "preview" in title_lower:
        domains.append("screenshots")
    if "metadata" in title_lower or "placeholder" in title_lower or "cross-platform" in title_lower or "future" in title_lower:
        domains.append("metadata")
    if "age" in title_lower or "rating" in title_lower:
        domains.append("age rating")
    if "ai" in title_lower or "generative" in title_lower:
        domains.append("AI disclosures")
    if "subscription" in title_lower or "pricing" in title_lower or "auto-renew" in title_lower:
        domains.append("subscription disclosures")
    if "billing" in title_lower or "payment" in title_lower or "external-payment" in title_lower or "lootbox" in title_lower:
        domains.append("payment compliance")
    if "accessibility" in title_lower:
        domains.append("accessibility")
    if "legal" in title_lower or "eula" in title_lower or "terms" in title_lower:
        domains.append("legal documents")
        domains.append("terms of service")
    if "support" in title_lower or "unreachable" in title_lower:
        domains.append("support URL")
    if "export" in title_lower:
        domains.append("export compliance")
    if "encryption" in title_lower:
        domains.append("encryption declarations")

    if not domains:
        domains.append("metadata")

    return list(set(domains))


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
    parser = argparse.ArgumentParser(description="Release Readiness Compliance Audit")
    parser.add_argument("target", nargs="?", default=ROOT, help="Target directory to audit")
    parser.add_argument("--report-out", default=None, help="Custom output path for the report")
    args = parser.parse_args()

    target_dir = os.path.abspath(args.target)

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

    # Parse guard_out, explicitly skipping absorbed deadlines
    all_scanner_stdout = guard_out + "\n" + meta_out
    lines = all_scanner_stdout.splitlines()
    in_absorbed_section = False
    i = 0
    while i < len(lines):
        line = lines[i]

        if "PASSED DEADLINES ABSORBED INTO THE PLAYBOOK" in line:
            in_absorbed_section = True
            i += 1
            continue

        if in_absorbed_section:
            if line.startswith("[CRITICAL]") or line.startswith("[HIGH]") or line.startswith("[MEDIUM]") or line.startswith("[LOW]"):
                if "absorbed into" in line:
                    i += 1
                    continue
            elif line.strip() == "" or line.startswith("Summary.") or line.startswith("BLOCKED."):
                in_absorbed_section = False

        if "absorbed into" in line:
            i += 1
            continue

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

    # Map findings to 13 areas and 15 review domains
    area_findings = {area: [] for area in REQUIRED_AREAS}
    domain_findings = {domain: [] for domain in REVIEW_DOMAINS}
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

        domains = get_domains_for_pattern(pid, patterns_dict)
        for domain in domains:
            if domain in domain_findings:
                domain_findings[domain].append(f)

    # --- Step 3. Compile Reports ---
    overall_status = "BLOCKED" if has_critical else ("ADVISORY" if findings else "PASSED")

    # Generate RELEASE-READINESS-REPORT.md
    report_lines = []
    report_lines.append("# Release Readiness Compliance Report")
    report_lines.append("")
    report_lines.append(f"Target Directory: {target_dir}")
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

    report_lines.append("## Compliance Summary Table (13 Areas)")
    report_lines.append("")
    report_lines.append("| Area | Status | Risks Found | Recommended Reviewers |")
    report_lines.append("| --- | --- | --- | --- |")

    for area in REQUIRED_AREAS:
        area_f = area_findings[area]
        if area_f:
            area_status = "BLOCKED" if any(af["severity"] == "critical" for af in area_f) else "ADVISORY"
        else:
            area_status = "PASSED"
        reviewers = RECOMMENDED_REVIEWERS_AREAS.get(area, "Lead Developer")
        report_lines.append(f"| {area} | {area_status} | {len(area_f)} | {reviewers} |")
    report_lines.append("")

    report_lines.append("## Detailed Compliance Analysis (13 Areas)")
    report_lines.append("")

    for idx, area in enumerate(REQUIRED_AREAS, 1):
        area_f = area_findings[area]
        if area_f:
            area_status = "BLOCKED" if any(af["severity"] == "critical" for af in area_f) else "ADVISORY"
        else:
            area_status = "PASSED"

        report_lines.append(f"### {idx}. {area}")
        report_lines.append(f"- Status: {area_status}")
        report_lines.append(f"- Recommended Reviewers: {RECOMMENDED_REVIEWERS_AREAS.get(area, 'Lead Developer')}")
        report_lines.append("")

        if not area_f:
            report_lines.append("No outstanding risks found for this area.")
            report_lines.append("")
            continue

        report_lines.append("| Finding ID | Severity | Description | Required Action | Affected Files |")
        report_lines.append("| --- | --- | --- | --- | --- |")

        for af in area_f:
            pid = af["id"]
            sev = af["severity"].upper()
            title = af["title"]
            fix = af["fix"] or "Refer to guidelines for remediation."
            aff_files = affected_files_map.get(pid, [])
            files_str = "<br>".join(aff_files[:5]) if aff_files else "None detected (Config/Listing check)"
            if len(aff_files) > 5:
                files_str += f"<br>... and {len(aff_files) - 5} more files"
            report_lines.append(f"| {pid} | {sev} | {title} | {fix} | {files_str} |")
        report_lines.append("")

    report_path = args.report_out or os.path.join(target_dir, "RELEASE-READINESS-REPORT.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

    # Generate docs/RELEASE-REVIEW-REPORT-2026.md (15 Review Domains Detailed Report)
    doc_lines = []
    doc_lines.append("# Pre-Release Compliance Review Report (2026)")
    doc_lines.append("")
    doc_lines.append(f"Target Directory: {target_dir}")
    doc_lines.append(f"Overall Compliance Status: {overall_status}")
    doc_lines.append("")
    doc_lines.append("## Executive Summary")
    doc_lines.append("This pre-release audit evaluates the repository against all fifteen distinct App Store and Google Play review domains required for release authorization.")
    doc_lines.append("")

    doc_lines.append("## 15-Domain Verification Summary Table")
    doc_lines.append("")
    doc_lines.append("| Domain | Status | Risks Found | Mapped Script / Source | Recommended Reviewers |")
    doc_lines.append("| --- | --- | --- | --- | --- |")

    for domain in REVIEW_DOMAINS:
        df = domain_findings[domain]
        if df:
            d_status = "BLOCKED" if any(f["severity"] == "critical" for f in df) else "ADVISORY"
        else:
            d_status = "PASSED"
        script = DOMAIN_MAPPED_SCRIPTS.get(domain, "agent-os/hooks/app-store-compliance-guard.sh")
        reviewers = RECOMMENDED_REVIEWERS_DOMAINS.get(domain, "Compliance Officer")
        doc_lines.append(f"| {domain.title()} | {d_status} | {len(df)} | `{script}` | {reviewers} |")
    doc_lines.append("")

    doc_lines.append("## Detailed Verification Across 15 Review Domains")
    doc_lines.append("")

    for idx, domain in enumerate(REVIEW_DOMAINS, 1):
        df = domain_findings[domain]
        if df:
            d_status = "BLOCKED" if any(f["severity"] == "critical" for f in df) else "ADVISORY"
        else:
            d_status = "PASSED"
        script = DOMAIN_MAPPED_SCRIPTS.get(domain, "agent-os/hooks/app-store-compliance-guard.sh")
        reviewers = RECOMMENDED_REVIEWERS_DOMAINS.get(domain, "Compliance Officer")

        doc_lines.append(f"### {idx}. {domain.title()}")
        doc_lines.append(f"- Status: {d_status}")
        doc_lines.append(f"- Mapped Script: `{script}`")
        doc_lines.append(f"- Recommended Reviewers: {reviewers}")
        doc_lines.append("")

        if not df:
            doc_lines.append("No outstanding compliance issues or risks identified in this domain.")
            doc_lines.append("")
            continue

        doc_lines.append("| Finding ID | Severity | Description | Required Action | Mapped Script | Affected Files |")
        doc_lines.append("| --- | --- | --- | --- | --- | --- |")

        for af in df:
            pid = af["id"]
            sev = af["severity"].upper()
            title = af["title"]
            fix = af["fix"] or "Refer to guidelines for remediation."
            aff_files = affected_files_map.get(pid, [])
            files_str = "<br>".join(aff_files[:5]) if aff_files else "None detected (Config/Listing check)"
            if len(aff_files) > 5:
                files_str += f"<br>... and {len(aff_files) - 5} more files"
            doc_lines.append(f"| {pid} | {sev} | {title} | {fix} | `{script}` | {files_str} |")
        doc_lines.append("")

    docs_dir = os.path.join(ROOT, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    review_report_path = os.path.join(docs_dir, "RELEASE-REVIEW-REPORT-2026.md")
    with open(review_report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(doc_lines) + "\n")

    print(f"Release readiness report generated successfully at: {report_path}")
    print(f"Release review report (2026) generated successfully at: {review_report_path}")
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
