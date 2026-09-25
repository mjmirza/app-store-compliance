#!/usr/bin/env python3
"""Runs metadata/guard scans against a target project and compiles a
release-readiness report. Exits non-zero on any critical finding."""

import os
import sys
import subprocess
import json
import re

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

# 15 Specific App Store & Google Play Review Domains
REVIEW_DOMAINS_15 = [
    ("permissions", "Lead Developer, Mobile Platform Leads", "agent-os/hooks/app-store-compliance-guard.sh"),
    ("privacy disclosures", "Data Protection Officer (DPO), Mobile Tech Lead", "scripts/validate-privacy-manifest.py"),
    ("screenshots", "App Store Optimization Specialist, Product Marketing", "scripts/metadata-audit.py"),
    ("metadata", "Product Marketing Manager, ASO Specialist", "scripts/metadata-audit.py"),
    ("age rating", "Compliance Officer, Mobile Release Manager", "agent-os/hooks/app-store-compliance-guard.sh"),
    ("AI disclosures", "AI Ethics and Governance Committee, Lead AI Architect", "scripts/monitor-ai-policy.py"),
    ("subscription disclosures", "Commercial Legal Counsel, Product Monetization Lead", "agent-os/hooks/app-store-compliance-guard.sh"),
    ("payment compliance", "Monetization Lead, Financial Compliance Officer", "agent-os/hooks/app-store-compliance-guard.sh"),
    ("accessibility", "Accessibility Specialist, Frontend QA Lead", "scripts/accessibility-audit.py"),
    ("legal documents", "Legal Counsel, Compliance Officer", "scripts/monitor-regulatory.py"),
    ("support URL", "Customer Support Lead, ASO Specialist", "scripts/metadata-audit.py"),
    ("privacy policy", "Data Protection Officer (DPO), Legal Counsel", "scripts/monitor-privacy.py"),
    ("terms of service", "Legal Counsel, Operations Manager", "scripts/monitor-regulatory.py"),
    ("export compliance", "Trade Compliance Officer, Legal Counsel", "agent-os/hooks/app-store-compliance-guard.sh"),
    ("encryption declarations", "Product Security Engineering Team, Security Architect", "scripts/monitor-security.py"),
]

# Recommended reviewers for 13 required areas
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

# Manual mapping of specific patterns to 13 areas
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
}

# Manual mapping of specific patterns to 15 review domains
MAP_PATTERNS_TO_15_DOMAINS = {
    "APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED": ["age rating"],
    "BOTH-SUBSCRIPTION-HARD-CANCEL": ["subscription disclosures", "payment compliance"],
    "APPLE-2.3-FUTURE-FUNCTIONALITY": ["metadata"],
    "APPLE-2.3-NEGATIVE-APPLE-SENTIMENT": ["metadata"],
    "APPLE-2.3-CROSS-PLATFORM-REFERENCE": ["metadata"],
    "BOTH-PLACEHOLDER": ["metadata", "screenshots", "support URL"],
    "BOTH-LOOTBOX-ODDS": ["payment compliance", "legal documents"],
    "BOTH-MISSING-PRIVACY-POLICY": ["privacy policy", "privacy disclosures"],
    "APPLE-PRIVACY-MANIFEST-MISSING": ["privacy disclosures", "privacy policy"],
    "APPLE-EXPORT-COMPLIANCE-MISSING": ["export compliance", "legal documents"],
    "APPLE-5.1.1-VAGUE-PURPOSE-STRING": ["permissions"],
    "APPLE-5.1.1-MISSING-USAGE-DESCRIPTION": ["permissions"],
    "GOOGLE-PERM-BACKGROUND-LOCATION": ["permissions"],
    "GOOGLE-PERM-ALL-FILES": ["permissions"],
    "GOOGLE-PERM-SMS-CALLLOG": ["permissions"],
    "GOOGLE-PERM-ACCESSIBILITY-MISUSE": ["permissions", "accessibility"],
    "BOTH-AI-GENERATED-CONTENT": ["AI disclosures"],
    "APPLE-5.1.2-AI-NO-CONSENT-MODAL": ["AI disclosures", "privacy disclosures"],
    "APPLE-3.1.1-EXTERNAL-PAYMENT": ["payment compliance", "subscription disclosures"],
    "APPLE-2.3.4-DEVICE-FRAMES-PREVIEW": ["screenshots", "metadata"],
    "APPLE-5.2.5-APPLE-DEVICE-IMAGE": ["screenshots", "metadata"],
    "BOTH-UNREACHABLE-METADATA-URL": ["support URL", "metadata"],
    "APPLE-1.2-UGC-24H-ACTION": ["legal documents", "terms of service"],
    "ANDROID-ACCOUNT-DELETION-URL": ["privacy policy", "privacy disclosures"],
    "APPLE-ACCOUNT-DELETION-WEAK": ["privacy policy", "privacy disclosures"],
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


def get_15_domains_for_pattern(pid, patterns_dict):
    if pid in MAP_PATTERNS_TO_15_DOMAINS:
        return MAP_PATTERNS_TO_15_DOMAINS[pid]

    pdata = patterns_dict.get(pid, {})
    title_lower = pdata.get("title", "").lower() + " " + pid.lower()

    domains = []
    if "perm" in title_lower or "usage-description" in title_lower:
        domains.append("permissions")
    if "privacy" in title_lower or "manifest" in title_lower or "data" in title_lower:
        domains.append("privacy disclosures")
        domains.append("privacy policy")
    if "screenshot" in title_lower or "frame" in title_lower or "preview" in title_lower:
        domains.append("screenshots")
    if "metadata" in title_lower or "future" in title_lower or "sentiment" in title_lower or "placeholder" in title_lower:
        domains.append("metadata")
    if "age" in title_lower or "rating" in title_lower:
        domains.append("age rating")
    if "ai" in title_lower or "generative" in title_lower:
        domains.append("AI disclosures")
    if "subscription" in title_lower or "cancel" in title_lower or "recurring" in title_lower:
        domains.append("subscription disclosures")
    if "payment" in title_lower or "billing" in title_lower or "lootbox" in title_lower or "odds" in title_lower:
        domains.append("payment compliance")
    if "accessibility" in title_lower:
        domains.append("accessibility")
    if "legal" in title_lower or "ugc" in title_lower or "dsa" in title_lower:
        domains.append("legal documents")
    if "support" in title_lower or "url" in title_lower or "unreachable" in title_lower:
        domains.append("support URL")
    if "terms" in title_lower or "tos" in title_lower:
        domains.append("terms of service")
    if "export" in title_lower or "compliance" in title_lower:
        domains.append("export compliance")
    if "encrypt" in title_lower or "security" in title_lower or "cipher" in title_lower:
        domains.append("encryption declarations")

    if not domains:
        domains = ["metadata"]

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


def generate_15_domain_report(target_dir, findings, patterns_dict, affected_files_map):
    has_critical = any(f["severity"] == "critical" for f in findings)
    overall_status = "BLOCKED" if has_critical else ("ADVISORY" if findings else "PASSED")

    domain_findings = {dom[0]: [] for dom in REVIEW_DOMAINS_15}
    for f in findings:
        pid = f["id"]
        doms = get_15_domains_for_pattern(pid, patterns_dict)
        for dom in doms:
            if dom in domain_findings:
                domain_findings[dom].append(f)

    lines = []
    lines.append("# Pre-Release Compliance Review Report 2026")
    lines.append("")
    lines.append(f"Target Directory: {target_dir}")
    lines.append(f"Overall Compliance Status: {overall_status}")
    lines.append("")

    lines.append("## Executive Summary")
    lines.append(
        "This report provides an exhaustive pre-release compliance evaluation across all fifteen App Store and Google Play review domains before release authorization. All identified findings are mapped to specific review domains, verification scripts, affected repository files, and recommended reviewers."
    )
    lines.append("")
    if has_critical:
        lines.append(
            "Release Status: BLOCKED. Critical compliance issues were identified that must be resolved prior to App Store or Google Play release authorization."
        )
    elif findings:
        lines.append(
            "Release Status: ADVISORY. Outstanding non-critical advisory risks exist. Review required actions and consult domain reviewers prior to submission."
        )
    else:
        lines.append(
            "Release Status: PASSED. All fifteen review domains passed validation with zero outstanding risks."
        )
    lines.append("")

    lines.append("## 15 Review Domains Summary Table")
    lines.append("")
    lines.append("| Domain | Status | Risks Found | Mapped Verification Script | Recommended Reviewers |")
    lines.append("| --- | --- | --- | --- | --- |")

    for dom, reviewers, script in REVIEW_DOMAINS_15:
        dom_f = domain_findings[dom]
        dom_status = "PASSED"
        if dom_f:
            if any(f["severity"] == "critical" for f in dom_f):
                dom_status = "BLOCKED"
            else:
                dom_status = "ADVISORY"
        num_risks = len(dom_f)
        lines.append(f"| {dom} | {dom_status} | {num_risks} | `{script}` | {reviewers} |")

    lines.append("")

    lines.append("## Severity-Ranked Findings Summary")
    lines.append("")
    if not findings:
        lines.append("No compliance issues identified across any domain.")
        lines.append("")
    else:
        lines.append("| Severity | Finding ID | Title | Required Remediation Action |")
        lines.append("| --- | --- | --- | --- |")
        # Sort critical first, then high, medium, low
        sev_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        sorted_findings = sorted(findings, key=lambda x: sev_order.get(x["severity"], 9))
        for f in sorted_findings:
            sev_str = f["severity"].upper()
            fix_str = f["fix"] or "Refer to guidelines for remediation."
            lines.append(f"| {sev_str} | {f['id']} | {f['title']} | {fix_str} |")
        lines.append("")

    lines.append("## Detailed Review Domain Analysis")
    lines.append("")

    for idx, (dom, reviewers, script) in enumerate(REVIEW_DOMAINS_15, 1):
        dom_f = domain_findings[dom]
        dom_status = "PASSED"
        if dom_f:
            if any(f["severity"] == "critical" for f in dom_f):
                dom_status = "BLOCKED"
            else:
                dom_status = "ADVISORY"

        lines.append(f"### {idx}. Domain: {dom}")
        lines.append(f"- Status: {dom_status}")
        lines.append(f"- Mapped Verification Script: `{script}`")
        lines.append(f"- Recommended Reviewers: {reviewers}")
        lines.append("")

        if not dom_f:
            lines.append(f"No outstanding compliance risks found for domain '{dom}'.")
            lines.append("")
            continue

        lines.append("| Finding ID | Severity | Description | Required Remediation Action | Affected Files |")
        lines.append("| --- | --- | --- | --- | --- |")

        for f in dom_f:
            pid = f["id"]
            sev = f["severity"].upper()
            title = f["title"]
            fix = f["fix"] or "Refer to guidelines for remediation."
            aff_files = affected_files_map.get(pid, [])
            if not aff_files:
                files_str = "None detected (Config/Listing check)"
            else:
                files_str = "<br>".join(aff_files[:5])
                if len(aff_files) > 5:
                    files_str += f"<br>... and {len(aff_files) - 5} more files"

            lines.append(f"| {pid} | {sev} | {title} | {fix} | {files_str} |")
        lines.append("")

    return "\n".join(lines) + "\n"


def parse_args():
    target_dir = ROOT
    report_out = None
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--report-out" and i + 1 < len(args):
            report_out = args[i + 1]
            i += 2
        elif not arg.startswith("--"):
            target_dir = os.path.abspath(arg)
            i += 1
        else:
            i += 1
    return target_dir, report_out


def main():
    target_dir, report_out = parse_args()

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

    report_path = os.path.join(target_dir, "RELEASE-READINESS-REPORT.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

    # Generate 15-domain review report if --report-out is passed or when auditing ROOT
    fifteen_domain_report_text = generate_15_domain_report(target_dir, findings, patterns_dict, affected_files_map)

    if report_out:
        os.makedirs(os.path.dirname(os.path.abspath(report_out)), exist_ok=True)
        with open(report_out, "w", encoding="utf-8") as f:
            f.write(fifteen_domain_report_text)
        print(f"15-Domain release review report generated successfully at: {report_out}")
    elif target_dir == ROOT:
        docs_review_path = os.path.join(ROOT, "docs", "RELEASE-REVIEW-REPORT-2026.md")
        with open(docs_review_path, "w", encoding="utf-8") as f:
            f.write(fifteen_domain_report_text)
        print(f"15-Domain release review report generated successfully at: {docs_review_path}")

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
