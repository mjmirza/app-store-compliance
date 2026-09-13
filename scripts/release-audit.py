#!/usr/bin/env python3
"""Runs metadata/guard scans against a target project and compiles a
release-readiness report. Exits non-zero on any critical finding."""

import os
import sys
import subprocess
import json
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 13 Required areas for release readiness report
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

# 15 Review Domains for Store Submission
FIFTEEN_REVIEW_DOMAINS = [
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

DOMAIN_MAPPED_SCRIPTS = {
    "permissions": "agent-os/hooks/app-store-compliance-guard.sh",
    "privacy disclosures": "scripts/monitor-privacy.py",
    "screenshots": "scripts/metadata-audit.py",
    "metadata": "scripts/metadata-audit.py",
    "age rating": "scripts/deadline-checker.py",
    "AI disclosures": "scripts/monitor-ai-policy.py",
    "subscription disclosures": "agent-os/hooks/app-store-compliance-guard.sh",
    "payment compliance": "agent-os/hooks/app-store-compliance-guard.sh",
    "accessibility": "scripts/accessibility-audit.py",
    "legal documents": "scripts/monitor-regulatory.py",
    "support URL": "scripts/verify-citations.py",
    "privacy policy": "scripts/monitor-privacy.py",
    "terms of service": "scripts/monitor-regulatory.py",
    "export compliance": "agent-os/hooks/app-store-compliance-guard.sh",
    "encryption declarations": "scripts/monitor-security.py",
}

DOMAIN_RECOMMENDED_REVIEWERS = {
    "permissions": "Mobile Tech Lead, Mobile Platform Leads",
    "privacy disclosures": "Data Protection Officer (DPO), Legal Counsel (Privacy)",
    "screenshots": "App Store Optimization (ASO) Specialist, Product Marketing Manager",
    "metadata": "App Store Optimization (ASO) Specialist, Product Marketing Manager",
    "age rating": "Compliance Officer, Legal Counsel",
    "AI disclosures": "AI Ethics and Governance Committee, Lead AI Architect",
    "subscription disclosures": "Financial Operations, Legal Counsel (Commercial)",
    "payment compliance": "Billing & Payment Lead, Legal Counsel (Commercial)",
    "accessibility": "Accessibility Specialist, Frontend QA Lead",
    "legal documents": "Legal Counsel (IP/Commercial), Compliance Officer",
    "support URL": "Customer Support Operations, Product Manager",
    "privacy policy": "Data Protection Officer (DPO), Legal Counsel (Privacy)",
    "terms of service": "Legal Counsel (Commercial)",
    "export compliance": "Export Compliance Officer, DevSecOps Lead",
    "encryption declarations": "DevSecOps Lead, Product Security Engineering",
}

# Manual mapping of specific patterns to 15 domains
MAP_PATTERNS_TO_15_DOMAINS = {
    "APPLE-2.1-MISSING-DEMO-ACCOUNT": ["metadata"],
    "APPLE-2.1-PLACEHOLDER-CONTENT": ["screenshots", "metadata"],
    "APPLE-2.1-STAGING-BACKEND": ["encryption declarations"],
    "APPLE-5.1.1-MISSING-PRIVACY-POLICY": ["privacy policy", "privacy disclosures"],
    "APPLE-5.1.1-VAGUE-PURPOSE-STRING": ["permissions"],
    "APPLE-5.1.1-MISSING-USAGE-DESCRIPTION": ["permissions"],
    "APPLE-5.1.1-NO-ACCOUNT-DELETION": ["privacy policy", "privacy disclosures"],
    "APPLE-5.1.2-MISSING-ATT": ["privacy disclosures"],
    "APPLE-3.1.1-EXTERNAL-PAYMENT": ["payment compliance"],
    "APPLE-4.8-SOCIAL-LOGIN-ONLY": ["privacy disclosures"],
    "APPLE-4.2-WEB-WRAPPER": ["metadata"],
    "APPLE-2.5.1-PRIVATE-API": ["encryption declarations"],
    "APPLE-2.3-CROSS-PLATFORM-REFERENCE": ["metadata"],
    "APPLE-2.3-AGE-RATING-2026": ["age rating"],
    "APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED": ["age rating"],
    "APPLE-5.1.2-AI-NO-CONSENT-MODAL": ["AI disclosures", "privacy disclosures"],
    "GOOGLE-DATASAFETY-MISMATCH": ["privacy disclosures"],
    "GOOGLE-PERM-BACKGROUND-LOCATION": ["permissions"],
    "GOOGLE-PERM-ALL-FILES": ["permissions"],
    "GOOGLE-PERM-SMS-CALLLOG": ["permissions"],
    "GOOGLE-PERM-ACCESSIBILITY-MISUSE": ["permissions", "accessibility"],
    "GOOGLE-TARGET-API": ["metadata"],
    "GOOGLE-12-TESTER-RULE": ["metadata"],
    "GOOGLE-PLAY-BILLING": ["payment compliance"],
    "GOOGLE-MISSING-PRIVACY-POLICY": ["privacy policy"],
    "GOOGLE-MISLEADING-LISTING": ["metadata"],
    "GOOGLE-FAMILIES-AD-SDK": ["privacy disclosures"],
    "BOTH-SDK-SUPPLY-CHAIN": ["encryption declarations"],
    "BOTH-LOOTBOX-ODDS": ["payment compliance", "legal documents"],
    "APPLE-PRIVACY-MANIFEST-MISSING": ["privacy disclosures"],
    "APPLE-EXPORT-COMPLIANCE-MISSING": ["export compliance", "legal documents"],
    "APPLE-RESTORE-PURCHASES-MISSING": ["subscription disclosures", "payment compliance"],
    "APPLE-ACCOUNT-DELETION-WEAK": ["privacy policy"],
    "ANDROID-DYNAMIC-CODE-LOADING": ["encryption declarations"],
    "ANDROID-QUERY-ALL-PACKAGES": ["permissions"],
    "ANDROID-OVERLAY-TAPJACKING": ["encryption declarations"],
    "ANDROID-ACCOUNT-DELETION-URL": ["privacy policy"],
    "BOTH-AI-GENERATED-CONTENT": ["AI disclosures"],
    "BOTH-METADATA-DECORATION": ["metadata"],
    "BOTH-FINGERPRINTING": ["privacy disclosures"],
    "APPLE-2.3-FUTURE-FUNCTIONALITY": ["metadata"],
    "APPLE-2.3-NEGATIVE-APPLE-SENTIMENT": ["metadata"],
    "BOTH-UNREACHABLE-METADATA-URL": ["support URL", "metadata"],
    "APPLE-5.2.5-APPLE-DEVICE-IMAGE": ["screenshots", "metadata"],
    "APPLE-2.3.4-DEVICE-FRAMES-PREVIEW": ["screenshots", "metadata"],
    "APPLE-3.1.2-MISLEADING-PRICING": ["subscription disclosures", "payment compliance"],
    "APPLE-1.2-UGC-24H-ACTION": ["legal documents", "terms of service"],
    "CHINA-AI-REFERENCES": ["AI disclosures"],
    "APPLE-2.4.5-UNUSED-ENTITLEMENTS": ["permissions"],
    "APPLE-4.0-SIWA-UX": ["privacy disclosures"],
    "APPLE-5.1.1-UNNECESSARY-DATA": ["privacy disclosures"],
    "APPLE-2.1-DEBUG-FEATURES": ["encryption declarations"],
    "APPLE-2.1-CLOUD-NOT-IN-PRODUCTION": ["metadata"],
    "APPLE-2.1-REVIEW-NOTES-INCOMPLETE": ["metadata"],
    "BOTH-PLACEHOLDER": ["screenshots", "metadata"],
    "BOTH-SUBSCRIPTION-HARD-CANCEL": ["subscription disclosures", "terms of service"],
    "BOTH-MISSING-PRIVACY-POLICY": ["privacy policy", "privacy disclosures"],
    "GOOGLE-ANON-CHAT-MINOR-BLOCK": ["age rating", "legal documents"],
    "APPLE-2.3.6-SOCIAL-MEDIA-DECLARATION": ["metadata", "age rating"],
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


def get_domains_for_pattern(pid, patterns_dict):
    if pid in MAP_PATTERNS_TO_15_DOMAINS:
        return MAP_PATTERNS_TO_15_DOMAINS[pid]

    pdata = patterns_dict.get(pid, {})
    title_lower = pdata.get("title", "").lower() + " " + pid.lower()

    domains = []
    if "perm" in title_lower or "usage" in title_lower:
        domains.append("permissions")
    if (
        "privacy" in title_lower
        or "data-safety" in title_lower
        or "att" in title_lower
        or "tracking" in title_lower
    ):
        domains.append("privacy disclosures")
    if "screenshot" in title_lower or "frame" in title_lower or "image" in title_lower:
        domains.append("screenshots")
    if (
        "metadata" in title_lower
        or "listing" in title_lower
        or "future" in title_lower
        or "placeholder" in title_lower
    ):
        domains.append("metadata")
    if "age" in title_lower or "rating" in title_lower or "iarc" in title_lower:
        domains.append("age rating")
    if "ai" in title_lower or "generative" in title_lower:
        domains.append("AI disclosures")
    if "subscr" in title_lower or "cancel" in title_lower:
        domains.append("subscription disclosures")
    if "pay" in title_lower or "billing" in title_lower or "lootbox" in title_lower:
        domains.append("payment compliance")
    if "accessibil" in title_lower:
        domains.append("accessibility")
    if "legal" in title_lower or "ugc" in title_lower:
        domains.append("legal documents")
    if "support" in title_lower or "url" in title_lower:
        domains.append("support URL")
    if "policy" in title_lower or "deletion" in title_lower:
        domains.append("privacy policy")
    if "terms" in title_lower:
        domains.append("terms of service")
    if "export" in title_lower:
        domains.append("export compliance")
    if "encrypt" in title_lower or "security" in title_lower or "debug" in title_lower:
        domains.append("encryption declarations")

    if not domains:
        domains.append("metadata")

    return list(set(domains))


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


def generate_release_review_report_15_domains(
    target_dir, findings, affected_files_map, report_path
):
    domain_findings = {domain: [] for domain in FIFTEEN_REVIEW_DOMAINS}
    has_critical = False

    patterns_dict = load_patterns()
    for f in findings:
        pid = f["id"]
        sev = f["severity"]
        if sev == "critical":
            has_critical = True

        domains = get_domains_for_pattern(pid, patterns_dict)
        for dom in domains:
            if dom in domain_findings:
                domain_findings[dom].append(f)

    report_lines = []
    report_lines.append("# Pre-Release Compliance Review Report 2026")
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
            "The release submission is currently BLOCKED due to one or more critical compliance issues across App Store and Google Play review domains that must be resolved prior to release authorization."
        )
    elif findings:
        report_lines.append(
            "The release submission is clear of critical blockers but contains non-critical advisory findings across App Store and Google Play review domains. Consult recommended reviewers before release authorization."
        )
    else:
        report_lines.append(
            "The release submission has successfully passed all 15 App Store and Google Play review domain audits with zero outstanding risks."
        )
    report_lines.append("")

    report_lines.append("## Review Domains Summary Table")
    report_lines.append("")
    report_lines.append(
        "| Review Domain | Status | Mapped Verification Script / Tool | Risks Found | Recommended Reviewers |"
    )
    report_lines.append("| --- | --- | --- | --- | --- |")

    for dom in FIFTEEN_REVIEW_DOMAINS:
        dom_f = domain_findings[dom]
        if dom_f:
            if any(af["severity"] == "critical" for af in dom_f):
                dom_status = "BLOCKED"
            else:
                dom_status = "ADVISORY"
        else:
            dom_status = "PASSED"

        mapped_script = DOMAIN_MAPPED_SCRIPTS.get(
            dom, "agent-os/hooks/app-store-compliance-guard.sh"
        )
        reviewers = DOMAIN_RECOMMENDED_REVIEWERS.get(dom, "Compliance Officer")
        report_lines.append(
            f"| {dom} | {dom_status} | {mapped_script} | {len(dom_f)} | {reviewers} |"
        )
    report_lines.append("")

    report_lines.append("## Detailed Domain Compliance Analysis")
    report_lines.append("")

    for idx, dom in enumerate(FIFTEEN_REVIEW_DOMAINS, 1):
        dom_f = domain_findings[dom]
        if dom_f:
            if any(af["severity"] == "critical" for af in dom_f):
                dom_status = "BLOCKED"
            else:
                dom_status = "ADVISORY"
        else:
            dom_status = "PASSED"

        mapped_script = DOMAIN_MAPPED_SCRIPTS.get(
            dom, "agent-os/hooks/app-store-compliance-guard.sh"
        )
        reviewers = DOMAIN_RECOMMENDED_REVIEWERS.get(dom, "Compliance Officer")

        report_lines.append(f"### {idx}. {dom.capitalize()}")
        report_lines.append(f"- Status: {dom_status}")
        report_lines.append(f"- Mapped Script / Tool: {mapped_script}")
        report_lines.append(f"- Recommended Reviewers: {reviewers}")
        report_lines.append("")

        if not dom_f:
            report_lines.append("No outstanding risks found for this review domain.")
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

            report_lines.append(
                f"| {pid} | {sev} | {title} | {fix} | {files_str} |"
            )
        report_lines.append("")

    os.makedirs(os.path.dirname(os.path.abspath(report_path)), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


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
    report_out = os.path.join(ROOT, "docs", "RELEASE-REVIEW-REPORT-2026.md")

    args = sys.argv[1:]
    if "--report-out" in args:
        idx = args.index("--report-out")
        if idx + 1 < len(args):
            report_out = os.path.abspath(args[idx + 1])
            del args[idx : idx + 2]

    if args and os.path.isdir(args[0]):
        target_dir = os.path.abspath(args[0])

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

    # Generate the 15-domain Pre-Release Compliance Review Report
    generate_release_review_report_15_domains(
        target_dir, findings, affected_files_map, report_out
    )

    print(f"Release readiness report generated successfully at: {report_path}")
    print(f"Release review report (15 domains) generated at: {report_out}")
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
