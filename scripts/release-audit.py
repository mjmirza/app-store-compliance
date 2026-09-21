#!/usr/bin/env python3
"""Runs metadata/guard scans against a target project and compiles a
release-readiness report across 13 required compliance areas and 15 App Store
& Google Play review domains. Exits non-zero on any critical finding."""

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

# 15 App Store and Google Play review domains
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

# Recommended reviewers for each 13 area
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

# Recommended reviewers for each 15 review domain
RECOMMENDED_REVIEWERS_DOMAINS = {
    "permissions": "Lead Developer, Mobile Platform Leads",
    "privacy disclosures": "Data Protection Officer (DPO), Legal Counsel (Privacy)",
    "screenshots": "Product Marketing Manager (PMM), Design Lead",
    "metadata": "Product Marketing Manager (PMM), App Store Optimization (ASO) Specialist",
    "age rating": "Trust & Safety Lead, Legal Counsel",
    "AI disclosures": "AI Ethics and Governance Committee, Lead AI Architect",
    "subscription disclosures": "Growth Product Manager, Legal Counsel (Commercial)",
    "payment compliance": "Payments & Billing Engineering Lead, Finance Lead",
    "accessibility": "Frontend QA Team, Accessibility Specialist",
    "legal documents": "Legal Counsel (Commercial/IP), Compliance Officer",
    "support URL": "Customer Support Operations Lead, Technical Writer",
    "privacy policy": "Data Protection Officer (DPO), Legal Counsel (Privacy)",
    "terms of service": "Legal Counsel (Commercial/IP), Compliance Officer",
    "export compliance": "Trade Compliance Officer, Product Security Lead",
    "encryption declarations": "Product Security Engineering Team, DevSecOps Lead",
}

# Mapped scripts for 15 review domains
MAPPED_SCRIPTS_DOMAINS = {
    "permissions": "agent-os/hooks/app-store-compliance-guard.sh, scripts/monitor-android.py",
    "privacy disclosures": "scripts/monitor-privacy.py, scripts/validate-privacy-manifest.py",
    "screenshots": "scripts/metadata-audit.py",
    "metadata": "scripts/metadata-audit.py, scripts/monitor.py",
    "age rating": "scripts/deadline-checker.py, agent-os/hooks/app-store-compliance-guard.sh",
    "AI disclosures": "scripts/monitor-ai-policy.py, scripts/monitor-regulatory.py",
    "subscription disclosures": "agent-os/hooks/app-store-compliance-guard.sh",
    "payment compliance": "agent-os/hooks/app-store-compliance-guard.sh",
    "accessibility": "scripts/accessibility-audit.py",
    "legal documents": "scripts/monitor-regulatory.py, scripts/validate.py",
    "support URL": "scripts/metadata-audit.py, scripts/verify-citations.py",
    "privacy policy": "scripts/monitor-privacy.py, scripts/metadata-audit.py",
    "terms of service": "scripts/monitor-regulatory.py, agent-os/hooks/app-store-compliance-guard.sh",
    "export compliance": "agent-os/hooks/app-store-compliance-guard.sh",
    "encryption declarations": "scripts/monitor-security.py, agent-os/hooks/app-store-compliance-guard.sh",
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
    "APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED": ["Apple requirements", "Platform announcements"],
    "BOTH-SUBSCRIPTION-HARD-CANCEL": ["Apple requirements", "Google Play requirements", "Legal documentation"],
    "BOTH-PLACEHOLDER": ["Store metadata"],
}

# Explicit mapping of specific patterns to 15 review domains
MAP_PATTERNS_TO_DOMAINS = {
    "APPLE-5.1.1-MISSING-USAGE-DESCRIPTION": ["permissions"],
    "APPLE-5.1.1-VAGUE-PURPOSE-STRING": ["permissions"],
    "GOOGLE-PERM-BACKGROUND-LOCATION": ["permissions"],
    "GOOGLE-PERM-ALL-FILES": ["permissions"],
    "GOOGLE-PERM-SMS-CALLLOG": ["permissions"],
    "ANDROID-QUERY-ALL-PACKAGES": ["permissions"],
    "ANDROID-USER-DATA-DISCLOSURE": ["permissions"],
    "ANDROID-RUNTIME-PERMISSIONS": ["permissions"],
    "ANDROID-HEALTH-PERMISSIONS": ["permissions"],
    "GOOGLE-LOCATION-BUTTON-SCOPE": ["permissions"],
    "GOOGLE-CONTACTS-PICKER-REQUIRED": ["permissions"],
    "GOOGLE-PHOTO-VIDEO-PERMISSIONS-DECLARATION": ["permissions"],
    "ANDROID-LOCAL-NETWORK-PERMISSION": ["permissions"],

    "APPLE-PRIVACY-MANIFEST-MISSING": ["privacy disclosures", "encryption declarations"],
    "APPLE-5.1.1-UNNECESSARY-DATA": ["privacy disclosures"],
    "APPLE-5.1.2-MISSING-ATT": ["privacy disclosures", "permissions"],
    "GOOGLE-DATASAFETY-MISMATCH": ["privacy disclosures"],
    "ANDROID-ADVERTISING-ID": ["privacy disclosures"],
    "BOTH-FINGERPRINTING": ["privacy disclosures"],
    "APPLE-PRIVACY-NUTRITION-LABELS": ["privacy disclosures"],

    "APPLE-5.2.5-APPLE-DEVICE-IMAGE": ["screenshots", "metadata"],
    "APPLE-2.3.4-DEVICE-FRAMES-PREVIEW": ["screenshots", "metadata"],

    "BOTH-PLACEHOLDER": ["metadata", "screenshots", "support URL"],
    "APPLE-2.3-FUTURE-FUNCTIONALITY": ["metadata"],
    "APPLE-2.3-NEGATIVE-APPLE-SENTIMENT": ["metadata"],
    "APPLE-2.3-CROSS-PLATFORM-REFERENCE": ["metadata"],
    "BOTH-METADATA-DECORATION": ["metadata"],
    "APPLE-2.1-REVIEW-NOTES-INCOMPLETE": ["metadata", "support URL"],
    "APPLE-3.1.2-MISLEADING-PRICING": ["metadata", "subscription disclosures"],
    "GOOGLE-MISLEADING-LISTING": ["metadata"],

    "APPLE-2.3-AGE-RATING-2026": ["age rating"],
    "APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED": ["age rating"],
    "APPLE-2.3.6-SOCIAL-MEDIA-DECLARATION": ["age rating"],
    "GOOGLE-PLAY-AGE-SIGNALS-MISUSE": ["age rating"],
    "GOOGLE-ANON-CHAT-MINOR-BLOCK": ["age rating", "terms of service"],
    "APPLE-GAMBLING-BRAZIL-LICENSE": ["age rating", "legal documents"],

    "BOTH-AI-GENERATED-CONTENT": ["AI disclosures"],
    "APPLE-5.1.2-AI-NO-CONSENT-MODAL": ["AI disclosures", "privacy disclosures"],
    "CHINA-AI-REFERENCES": ["AI disclosures"],
    "GOOGLE-GENAI-NCII-CONTROLS": ["AI disclosures"],

    "BOTH-SUBSCRIPTION-HARD-CANCEL": ["subscription disclosures", "terms of service", "legal documents"],
    "APPLE-RESTORE-PURCHASES-MISSING": ["subscription disclosures", "payment compliance"],

    "APPLE-3.1.1-EXTERNAL-PAYMENT": ["payment compliance"],
    "GOOGLE-PLAY-BILLING": ["payment compliance"],
    "GOOGLE-PLAY-BILLING-V8-REQUIRED": ["payment compliance"],
    "BOTH-LOOTBOX-ODDS": ["payment compliance", "legal documents"],
    "APPLE-3.1.1-EXTERNAL-LINK-REGION-GATING": ["payment compliance"],
    "GOOGLE-PAYMENTS-DONATION-LINK": ["payment compliance"],
    "GOOGLE-PLAY-CHARGEBACK-LIABILITY": ["payment compliance"],

    "GOOGLE-PERM-ACCESSIBILITY-MISUSE": ["accessibility"],
    "APPLE-ACCESSIBILITY-VOICEOVER": ["accessibility"],
    "APPLE-ACCESSIBILITY-DYNAMICTYPE": ["accessibility"],
    "APPLE-ACCESSIBILITY-REDUCEMOTION": ["accessibility"],
    "APPLE-ACCESSIBILITY-COLORCONTRAST": ["accessibility"],
    "APPLE-ACCESSIBILITY-HAPTICS": ["accessibility"],
    "APPLE-ACCESSIBILITY-KEYBOARD": ["accessibility"],
    "ANDROID-ACCESSIBILITY-TALKBACK": ["accessibility"],
    "ANDROID-ACCESSIBILITY-FONTSCALING": ["accessibility"],
    "ANDROID-ACCESSIBILITY-HIGHCONTRAST": ["accessibility"],
    "ANDROID-ACCESSIBILITY-SCANNER": ["accessibility"],

    "APPLE-1.2-UGC-24H-ACTION": ["legal documents", "terms of service"],
    "GOOGLE-ORG-REGISTRATION-REQUIRED": ["legal documents"],

    "BOTH-UNREACHABLE-METADATA-URL": ["support URL", "metadata", "privacy policy"],

    "APPLE-5.1.1-MISSING-PRIVACY-POLICY": ["privacy policy"],
    "GOOGLE-MISSING-PRIVACY-POLICY": ["privacy policy"],
    "BOTH-MISSING-PRIVACY-POLICY": ["privacy policy"],
    "ANDROID-ACCOUNT-DELETION-URL": ["privacy policy", "privacy disclosures"],
    "APPLE-5.1.1-NO-ACCOUNT-DELETION": ["privacy policy", "privacy disclosures"],
    "APPLE-ACCOUNT-DELETION-WEAK": ["privacy policy", "privacy disclosures"],
    "WEB-GDPR-COMPLIANCE": ["privacy policy", "privacy disclosures"],

    "APPLE-EXPORT-COMPLIANCE-MISSING": ["export compliance", "encryption declarations"],

    "BOTH-SECURE-STORAGE": ["encryption declarations"],
    "ANDROID-INSECURE-BACKUP": ["encryption declarations"],
    "WEB-LOCAL-STORAGE": ["encryption declarations"],
    "WEB-SESSION-STORAGE": ["encryption declarations"],
    "WEB-INDEXEDDB": ["encryption declarations"],
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


def get_domains_for_pattern(pid, patterns_dict):
    if pid in MAP_PATTERNS_TO_DOMAINS:
        return MAP_PATTERNS_TO_DOMAINS[pid]

    pdata = patterns_dict.get(pid, {})
    title_lower = (pdata.get("title", "") + " " + pid).lower()

    domains = []
    if "perm" in title_lower or "usage-description" in title_lower or "location" in title_lower or "contacts" in title_lower:
        domains.append("permissions")
    if "privacy" in title_lower or "data-safety" in title_lower or "tracking" in title_lower or "att" in title_lower:
        domains.append("privacy disclosures")
    if "screenshot" in title_lower or "frame" in title_lower or "device-image" in title_lower:
        domains.append("screenshots")
    if "metadata" in title_lower or "placeholder" in title_lower or "future-func" in title_lower or "listing" in title_lower:
        domains.append("metadata")
    if "age" in title_lower or "rating" in title_lower or "minor" in title_lower:
        domains.append("age rating")
    if "ai" in title_lower or "openai" in title_lower or "genai" in title_lower:
        domains.append("AI disclosures")
    if "subscription" in title_lower or "auto-renew" in title_lower or "cancel" in title_lower or "restore" in title_lower:
        domains.append("subscription disclosures")
    if "payment" in title_lower or "billing" in title_lower or "lootbox" in title_lower or "donation" in title_lower or "chargeback" in title_lower:
        domains.append("payment compliance")
    if "accessibility" in title_lower or "voiceover" in title_lower or "talkback" in title_lower or "contrast" in title_lower:
        domains.append("accessibility")
    if "legal" in title_lower or "ugc" in title_lower or "organization" in title_lower or "terms" in title_lower:
        domains.append("legal documents")
    if "url" in title_lower or "unreachable" in title_lower or "support" in title_lower:
        domains.append("support URL")
    if "privacy policy" in title_lower or "privacy-policy" in title_lower or "account-deletion" in title_lower or "gdpr" in title_lower:
        domains.append("privacy policy")
    if "terms" in title_lower or "tos" in title_lower or "ugc" in title_lower:
        domains.append("terms of service")
    if "export" in title_lower or "nonexemptencryption" in title_lower:
        domains.append("export compliance")
    if "encryption" in title_lower or "secure-storage" in title_lower or "backup" in title_lower or "storage" in title_lower:
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


def main():
    parser = argparse.ArgumentParser(
        description="Runs metadata/guard scans against a target project and compiles release readiness reports."
    )
    parser.add_argument(
        "target_dir",
        nargs="?",
        default=ROOT,
        help="Target directory to audit (defaults to repo root).",
    )
    parser.add_argument(
        "--report-out",
        dest="report_out",
        default=None,
        help="Path to save the release readiness report.",
    )
    args_parsed = parser.parse_args()

    target_dir = os.path.abspath(args_parsed.target_dir)

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

    # Programmatically scan for affected files
    affected_files_map = find_affected_files(target_dir, patterns_dict)

    # --- Step 3. Compile Report across 13 Areas and 15 Review Domains ---
    area_findings = {area: [] for area in REQUIRED_AREAS}
    domain_findings = {dom: [] for dom in REVIEW_DOMAINS_15}
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
        for dom in domains:
            if dom in domain_findings:
                domain_findings[dom].append(f)

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

    report_lines.append("## 15 App Store and Google Play Review Domains")
    report_lines.append("")
    report_lines.append("| Review Domain | Status | Risks Found | Mapped Scripts | Recommended Reviewers |")
    report_lines.append("| --- | --- | --- | --- | --- |")

    for dom in REVIEW_DOMAINS_15:
        dom_status = "PASSED"
        dom_f = domain_findings[dom]
        if dom_f:
            if any(af["severity"] == "critical" for af in dom_f):
                dom_status = "BLOCKED"
            else:
                dom_status = "ADVISORY"

        num_risks = len(dom_f)
        reviewers = RECOMMENDED_REVIEWERS_DOMAINS.get(dom, "Lead Developer")
        scripts = MAPPED_SCRIPTS_DOMAINS.get(dom, "scripts/release-audit.py")
        report_lines.append(f"| {dom} | {dom_status} | {num_risks} | {scripts} | {reviewers} |")
    report_lines.append("")

    report_lines.append("## 13 Required Compliance Areas Summary")
    report_lines.append("")
    report_lines.append("| Compliance Area | Status | Risks Found | Recommended Reviewers |")
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
        reviewers = RECOMMENDED_REVIEWERS_AREAS.get(area, "Lead Developer")
        report_lines.append(f"| {area} | {area_status} | {num_risks} | {reviewers} |")
    report_lines.append("")

    report_lines.append("## Detailed Compliance Analysis: 15 Review Domains")
    report_lines.append("")

    for idx, dom in enumerate(REVIEW_DOMAINS_15, 1):
        dom_f = domain_findings[dom]
        dom_status = "PASSED"
        if dom_f:
            if any(af["severity"] == "critical" for af in dom_f):
                dom_status = "BLOCKED"
            else:
                dom_status = "ADVISORY"

        report_lines.append(f"### Domain {idx}: {dom.title()}")
        report_lines.append(f"- Status: {dom_status}")
        report_lines.append(
            f"- Recommended Reviewers: {RECOMMENDED_REVIEWERS_DOMAINS.get(dom, 'Lead Developer')}"
        )
        report_lines.append(
            f"- Mapped Scripts: {MAPPED_SCRIPTS_DOMAINS.get(dom, 'scripts/release-audit.py')}"
        )
        report_lines.append("")

        if not dom_f:
            report_lines.append("No outstanding risks found for this domain.")
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

    report_lines.append("## Detailed Compliance Analysis: 13 Compliance Areas")
    report_lines.append("")

    for idx, area in enumerate(REQUIRED_AREAS, 1):
        area_f = area_findings[area]
        area_status = "PASSED"
        if area_f:
            if any(af["severity"] == "critical" for af in area_f):
                area_status = "BLOCKED"
            else:
                area_status = "ADVISORY"

        report_lines.append(f"### Area {idx}: {area}")
        report_lines.append(f"- Status: {area_status}")
        report_lines.append(
            f"- Recommended Reviewers: {RECOMMENDED_REVIEWERS_AREAS.get(area, 'Lead Developer')}"
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

    report_content = "\n".join(report_lines) + "\n"

    # Determine report destination
    if args_parsed.report_out:
        report_path = os.path.abspath(args_parsed.report_out)
    else:
        report_path = os.path.join(target_dir, "RELEASE-READINESS-REPORT.md")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    # If target_dir is ROOT or report_out was not custom outside ROOT, also update docs/RELEASE-REVIEW-REPORT-2026.md
    if target_dir == ROOT:
        docs_review_path = os.path.join(ROOT, "docs", "RELEASE-REVIEW-REPORT-2026.md")
        os.makedirs(os.path.dirname(docs_review_path), exist_ok=True)
        with open(docs_review_path, "w", encoding="utf-8") as f:
            f.write(report_content)

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
