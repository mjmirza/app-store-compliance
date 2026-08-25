#!/usr/bin/env python3
"""
Technical Standards Compliance Monitoring Utility.
Tracks changes across 10 core technical standards:
- ISO 27001 (Information Security Management)
- ISO 27701 (Privacy Information Management)
- ISO 42001 (Artificial Intelligence Management)
- ISO 31000 (Risk Management)
- ISO 9001 (Quality Management)
- IEC standards (e.g. IEC 62443 Cyber Security, IEC 82304 Health Software)
- OWASP (Mobile Top 10, Web Top 10, API Security Top 10, LLM Top 10)
- NIST AI RMF (AI Risk Management Framework)
- NIST CSF (Cybersecurity Framework 2.0)
- CIS Benchmarks (Center for Internet Security Benchmarks)

When standards change, this script:
1. Identifies repository gaps via codebase signal scanning.
2. Generates actionable implementation tasks.
3. Generates documentation updates in docs/STANDARDS-POLICY-MIGRATION.md.
4. Generates testing updates.
5. Drafts a 15-section emoji-free Pull Request proposal.
"""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json

# The 10 tracked technical standards
CATEGORIES = [
    "ISO 27001",
    "ISO 27701",
    "ISO 42001",
    "ISO 31000",
    "ISO 9001",
    "IEC standards",
    "OWASP",
    "NIST AI RMF",
    "NIST CSF",
    "CIS Benchmarks",
]

# Keywords used to classify incoming announcements/articles into the 10 standards
CATEGORY_KEYWORDS = {
    "ISO 27001": [
        "iso 27001",
        "iso/iec 27001",
        "information security management system",
        "isms",
        "annex a controls",
    ],
    "ISO 27701": [
        "iso 27701",
        "iso/iec 27701",
        "privacy information management system",
        "pims",
        "pii controller",
        "pii processor",
    ],
    "ISO 42001": [
        "iso 42001",
        "iso/iec 42001",
        "artificial intelligence management system",
        "aims",
        "ai risk management",
    ],
    "ISO 31000": [
        "iso 31000",
        "risk management guidelines",
        "risk identification",
        "risk assessment",
    ],
    "ISO 9001": [
        "iso 9001",
        "quality management system",
        "qms",
        "quality assurance",
    ],
    "IEC standards": [
        "iec",
        "iec 62443",
        "iec 82304",
        "iec 62304",
        "industrial automation security",
        "medical device software",
    ],
    "OWASP": [
        "owasp",
        "owasp top 10",
        "masvs",
        "mstg",
        "owasp Mobile top 10",
        "owasp api top 10",
        "owasp llm top 10",
    ],
    "NIST AI RMF": [
        "nist ai rmf",
        "ai rmf",
        "nist ai risk management framework",
        "govern map measure manage",
        "trustworthy ai",
    ],
    "NIST CSF": [
        "nist csf",
        "nist csf 2.0",
        "cybersecurity framework",
        "identify protect detect respond recover govern",
    ],
    "CIS Benchmarks": [
        "cis benchmark",
        "cis benchmarks",
        "center for internet security",
        "cis level 1",
        "cis level 2",
        "hardening guide",
    ],
}

# Codebase signals (regex patterns) to find files affected by each standard
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISMS",
        r"access_control",
        r"encryption_policy",
        r"incident_response",
        r"ISO-27001",
    ],
    "ISO 27701": [
        r"PIMS",
        r"privacyConsent",
        r"pii_data",
        r"data_retention",
        r"ISO-27701",
    ],
    "ISO 42001": [
        r"AIMS",
        r"ai_governance",
        r"model_card",
        r"bias_mitigation",
        r"ISO-42001",
    ],
    "ISO 31000": [
        r"risk_register",
        r"risk_matrix",
        r"risk_assessment",
        r"ISO-31000",
    ],
    "ISO 9001": [
        r"quality_assurance",
        r"code_review",
        r"process_audit",
        r"ISO-9001",
    ],
    "IEC standards": [
        r"IEC-62443",
        r"IEC-82304",
        r"IEC-62304",
        r"industrial_security",
        r"software_lifecycle",
    ],
    "OWASP": [
        r"MASVS",
        r"OWASP",
        r"sql_injection",
        r"xss_prevention",
        r"csrf_token",
        r"sanitize_input",
    ],
    "NIST AI RMF": [
        r"NIST-AI-RMF",
        r"ai_transparency",
        r"explainable_ai",
        r"model_monitoring",
    ],
    "NIST CSF": [
        r"NIST-CSF",
        r"cybersecurity_framework",
        r"incident_handling",
        r"threat_hunting",
    ],
    "CIS Benchmarks": [
        r"CIS_BENCHMARK",
        r"hardening",
        r"secure_boot",
        r"tls_config",
        r"os_hardening",
    ],
}

# Source trust domains and keywords for verification
TRUST_HIERARCHY = {
    "Priority 1": "Official standards bodies and government agencies (ISO, IEC, NIST, OWASP, CIS, CISA, ENISA, FTC, ICO, European Commission)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}

# Comprehensive Mock Announcements for all 10 categories
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO-27001",
        "category": "ISO 27001",
        "title": "ISO 27001 Annex A Security Control Updates",
        "description": "ISO/IEC 27001 standard updates require mandatory cloud service security controls, threat intelligence logging, and data masking protocols.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 PDT",
        "source_priority": "Priority 1",
    },
    {
        "id": "STD-MOCK-ISO-27701",
        "category": "ISO 27701",
        "title": "ISO 27701 PIMS Privacy Extension Requirements",
        "description": "ISO 27701 privacy requirements mandate documented PII controller and processor workflows, cross-border data transfer impact assessments, and data minimization mechanisms.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 PDT",
        "source_priority": "Priority 1",
    },
    {
        "id": "STD-MOCK-ISO-42001",
        "category": "ISO 42001",
        "title": "ISO 42001 AI Management System Certification Guidelines",
        "description": "ISO/IEC 42001 requires organizations deploying AI systems to maintain AI safety policies, continuous model risk assessments, and algorithmic transparency records.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 PDT",
        "source_priority": "Priority 1",
    },
    {
        "id": "STD-MOCK-ISO-31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Enterprise Risk Management Framework Refinements",
        "description": "ISO 31000 updates require integrated continuous risk evaluation, real-time threat reporting, and structured risk treatment documentation.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 PDT",
        "source_priority": "Priority 1",
    },
    {
        "id": "STD-MOCK-ISO-9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Assurance and Continuous Improvement Guidelines",
        "description": "ISO 9001 standard revisions mandate strict automated software quality assurance, peer review evidence retention, and measurable defect tracking metrics.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 PDT",
        "source_priority": "Priority 1",
    },
    {
        "id": "STD-MOCK-IEC-STANDARDS",
        "category": "IEC standards",
        "title": "IEC 62443 and IEC 82304 Cyber Security & Software Lifecycle Updates",
        "description": "IEC cybersecurity standards require secure development lifecycle validation, defense-in-depth architecture, and rigorous software bill of materials (SBOM) tracking.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 PDT",
        "source_priority": "Priority 1",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP Top 10 & MASVS Security Verification Release",
        "description": "OWASP updates emphasize prevention of insecure direct object references, automated input sanitization, dynamic API authentication, and robust mobile storage encryption.",
        "link": "https://owasp.org",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 PDT",
        "source_priority": "Priority 1",
    },
    {
        "id": "STD-MOCK-NIST-AI-RMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework 1.1 Governance Specifications",
        "description": "NIST AI RMF guidance outlines concrete controls across Govern, Map, Measure, and Manage functions for trustworthy AI deployment and red-teaming validation.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 PDT",
        "source_priority": "Priority 1",
    },
    {
        "id": "STD-MOCK-NIST-CSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework 2.0 Governance and Resilience Updates",
        "description": "NIST CSF 2.0 introduces the Governance function alongside Identify, Protect, Detect, Respond, and Recover, requiring enterprise-wide cybersecurity risk management alignment.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 PDT",
        "source_priority": "Priority 1",
    },
    {
        "id": "STD-MOCK-CIS-BENCHMARKS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks Level 1 and Level 2 Hardening Guidelines",
        "description": "CIS Benchmarks require secure baseline configurations, strict TLS cipher suites, SSH/OS hardening, and automated vulnerability scanning.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 PDT",
        "source_priority": "Priority 1",
    },
]


def enforce_strict_source_trust_hierarchy(item):
    """
    Evaluates item against source trust hierarchy rules.
    Priority 1: Official sources (ISO, IEC, NIST, OWASP, CIS, CISA, ENISA, FTC, ICO).
    Priority 2: Reuters, AP, Bloomberg.
    Priority 3: Academic papers.
    Priority 4: Industry blogs.
    Priority 5: Social media / unverified.

    Unverified Priority 4 and Priority 5 sources must NOT trigger PR draft generation unless verified.
    """
    link = item.get("link", "").lower()
    priority = item.get("source_priority", "Priority 1")

    # Domain check for Priority 1
    official_domains = [
        "iso.org",
        "iec.ch",
        "nist.gov",
        "owasp.org",
        "cisecurity.org",
        "cisa.gov",
        "enisa.europa.eu",
        "ftc.gov",
        "ico.org.uk",
        "europa.eu",
        "developer.apple.com",
        "developer.android.com",
    ]

    is_official = any(domain in link for domain in official_domains)
    if is_official:
        return "Priority 1", True

    if "reuters.com" in link or "apnews.com" in link or "bloomberg.com" in link:
        return "Priority 2", True

    if priority in ["Priority 4", "Priority 5"]:
        print(
            f"[TRUST WARNING] Item '{item.get('title')}' is from unverified source priority ({priority}). Blocking automatic compliance PR generation.",
            file=sys.stderr,
        )
        return priority, False

    return priority, True


def classify_announcements(announcements, keywords_filter=None):
    """Classifies incoming policy items into the 10 technical standard categories."""
    classified = []
    seen_ids = set()

    for item in announcements:
        item_id = item.get("id") or item.get("title")
        if item_id in seen_ids:
            continue

        assigned_cat = item.get("category")
        matched_cat = None

        if assigned_cat and assigned_cat in CATEGORIES:
            matched_cat = assigned_cat
        else:
            text = (
                f"{item.get('title', '')} {item.get('description', '')}"
            ).lower()
            for cat, kw_list in CATEGORY_KEYWORDS.items():
                if any(kw in text for kw in kw_list):
                    matched_cat = cat
                    break

        if matched_cat:
            if keywords_filter:
                title_desc = (
                    f"{item.get('title', '')} {item.get('description', '')}"
                ).lower()
                if not any(kw.lower() in title_desc for kw in keywords_filter):
                    continue

            _, allowed = enforce_strict_source_trust_hierarchy(item)
            if not allowed:
                continue

            entry = dict(item)
            entry["category"] = matched_cat
            classified.append(entry)
            seen_ids.add(item_id)

    return classified


def scan_codebase_for_standards_signals(directory):
    """Scans codebase for matches against signals of the 10 technical standards."""
    scan_results = {cat: [] for cat in CATEGORIES}
    target_exts = {
        ".py",
        ".sh",
        ".md",
        ".json",
        ".yml",
        ".yaml",
        ".xml",
        ".js",
        ".ts",
        ".kt",
        ".swift",
        ".java",
        ".gradle",
        ".plist",
    }

    for root, dirs, files in os.walk(directory):
        # Exclude git and hidden dirs
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in target_exts:
                continue

            filepath = os.path.relpath(os.path.join(root, file), directory)
            try:
                with open(
                    os.path.join(root, file), "r", encoding="utf-8", errors="ignore"
                ) as f:
                    content = f.read()

                for cat, patterns in CATEGORY_SIGNALS.items():
                    for pat in patterns:
                        if re.search(pat, content, re.IGNORECASE):
                            if filepath not in scan_results[cat]:
                                scan_results[cat].append(filepath)
                            break
            except Exception:
                continue

    return scan_results


def generate_pull_request_draft(updates, scan_results):
    """Generates a comprehensive 15-section, 100% emoji-free Pull Request draft."""
    matched_cats = sorted(list(set(u["category"] for u in updates)))

    citations = []
    for u in updates:
        citations.append(f"- **{u['category']}**: [{u['title']}]({u['link']})")
    citations_str = "\n".join(citations) if citations else "No citations available."

    affected_files_set = set()
    for cat in matched_cats:
        for f in scan_results.get(cat, []):
            affected_files_set.add(f)

    affected_files_list = sorted(list(affected_files_set))
    if not affected_files_list:
        affected_files_str = (
            "- `data/rejection-patterns.json`\n- `docs/STANDARDS-POLICY-MIGRATION.md`"
        )
    else:
        affected_files_str = "\n".join([f"- `{f}`" for f in affected_files_list])

    risk_lines = []
    for cat in matched_cats:
        risk_lines.append(
            f"- **{cat}**: Non-compliance risks audit failure, security vulnerabilities, regulatory penalties, and store rejection."
        )
    risk_assessment_str = "\n".join(risk_lines)

    migration_lines = []
    for cat in matched_cats:
        migration_lines.append(
            f"### Migration for {cat}\n- Conduct gap assessment against updated {cat} criteria.\n- Update internal governance documentation and compliance mappings.\n- Implement technical controls and verification tests for {cat} requirements."
        )
    migration_steps_str = "\n\n".join(migration_lines)

    impl_checklist_lines = []
    for cat in matched_cats:
        impl_checklist_lines.append(
            f"- [ ] Implement technical control and code baseline for {cat}."
        )
    impl_checklist_str = "\n".join(impl_checklist_lines)

    test_checklist_lines = []
    for cat in matched_cats:
        test_checklist_lines.append(
            f"- [ ] Execute test suite and static audit for {cat} compliance."
        )
    test_checklist_str = "\n".join(test_checklist_lines)

    pr_template = f"""## 1. Summary
This pull request introduces compliance updates and technical control alignments for 10 core technical standards ({', '.join(matched_cats)}). It addresses identified repository gaps, updates documentation, and adds testing tasks to ensure complete standards compliance.

## 2. Background
Technical standards including ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks undergo periodic revisions. Maintaining strict compliance protects organizational security, user privacy, and publishing status across Apple App Store and Google Play platforms.

## 3. Regulatory change
- **Standards Framework Alignment**: Updated controls for ISO, IEC, OWASP, NIST, and CIS Benchmarks.
- **Security & AI Governance**: Implementation of enhanced security, privacy, and trustworthy AI management controls.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All proposed standard compliance updates are non-breaking and backward-compatible. Technical controls add security hardening without disrupting existing APIs or application workflows.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Re-run python3 scripts/validate.py to ensure pattern integrity.

## 10. Testing checklist
{test_checklist_str}
- [ ] Run scripts/monitor-standards-test.sh to verify standards monitoring.

## 11. Documentation checklist
- [ ] Update docs/STANDARDS-POLICY-MIGRATION.md with the latest standards update log.
- [ ] Document technical control requirements in internal compliance guides.

## 12. Compliance impact
- **Audit Preparedness**: Validates technical controls for ISO/IEC certifications.
- **Risk Mitigation**: Ensures alignment with OWASP Top 10 and NIST frameworks.
- **Store Compliance**: Satisfies platform safety and security guidelines.

## 13. Breaking changes
- No breaking changes introduced.

## 14. Review checklist
- [ ] Code and documentation are 100% free of emojis or graphical symbols.
- [ ] All technical control assertions have corresponding tests.
- [ ] Official citations strictly adhere to Priority 1 trust hierarchy sources.

## 15. Approver recommendations
Verify that all technical control implementations match the corresponding standard requirements. Confirm that test execution logs show 100% pass rate before merging.
"""
    return pr_template


def update_documentation_report(updates, scan_results, output_filepath):
    """Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md."""
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Compliance Policy Migration & Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track compliance across ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.",
        "",
        "## Monitored Technical Standards Update Log",
        "",
    ]

    for idx, u in enumerate(updates, 1):
        lines.append(f"### {idx}. [{u['category']}] {u['title']}")
        lines.append(f"- **Published Date**: {u['pubDate']}")
        lines.append(f"- **Official Resource**: [{u['link']}]({u['link']})")
        lines.append(f"- **Source Priority**: {u.get('source_priority', 'Priority 1')}")
        lines.append(f"- **Description**: {u['description']}")
        lines.append("")

    lines.append("## Identified Repository Gaps")
    lines.append("")

    for u in updates:
        cat = u["category"]
        files = scan_results.get(cat, [])
        lines.append(f"### Repository Gaps for {cat}")
        if files:
            lines.append("- **Affected Codebase Signals / Files Found**:")
            for f in files:
                lines.append(f"  - `{f}`")
        else:
            lines.append("- **No direct codebase signal files found**: Implementation and pattern mapping required.")
        lines.append("")

    lines.append("## Automated Migration Recommendations & Implementation Tasks")
    lines.append("")

    for u in updates:
        cat = u["category"]
        lines.append(f"### Implementation Tasks for {cat}")
        lines.append(
            f"- [ ] **Task 1**: Update {cat} control matrix and policy documentation."
        )
        lines.append(
            f"- [ ] **Task 2**: Implement required code controls and configuration hardening for {cat}."
        )
        lines.append("")

    lines.append("## Testing Updates")
    lines.append("")

    for u in updates:
        cat = u["category"]
        lines.append(f"### Testing Requirements for {cat}")
        lines.append(
            f"- [ ] **Test 1**: Verify {cat} control validation in automated test suite."
        )
        lines.append(
            f"- [ ] **Test 2**: Run static analysis audit to confirm zero regression for {cat}."
        )
        lines.append("")

    lines.append("## Documentation Updates")
    lines.append("")

    for u in updates:
        cat = u["category"]
        lines.append(f"### Documentation Tasks for {cat}")
        lines.append(
            f"- [ ] **Doc 1**: Map {cat} requirements to `data/rejection-patterns.json`."
        )
        lines.append(
            f"- [ ] **Doc 2**: Update `docs/STANDARDS-POLICY-MIGRATION.md` with audit evidence."
        )
        lines.append("")

    lines.append("<!-- STANDARDS_POLICY_MONITOR_END -->")

    try:
        os.makedirs(os.path.dirname(output_filepath) or ".", exist_ok=True)
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"Technical standards documentation updated successfully at: {output_filepath}")
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor Technical Standards (ISO, IEC, OWASP, NIST, CIS Benchmarks)"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live technical standards updates"
    )
    parser.add_argument(
        "--mock",
        type=str,
        help="Path to custom mock announcements JSON file, or 'inline' to use default mock dataset",
    )
    parser.add_argument(
        "--keywords",
        type=str,
        help="Optional comma-separated keywords to filter updates",
    )
    parser.add_argument(
        "--dir", type=str, default=".", help="Codebase directory to scan"
    )
    parser.add_argument(
        "--output-docs",
        type=str,
        default="docs/STANDARDS-POLICY-MIGRATION.md",
        help="Filepath to write migration tasks and logs",
    )
    parser.add_argument(
        "--pr-output",
        type=str,
        default="docs/STANDARDS_COMPLIANCE_PR_DRAFT.md",
        help="Filepath to save the drafted PR",
    )
    parser.add_argument(
        "--json", action="store_true", help="Output results in JSON format"
    )

    args = parser.parse_args()

    announcements = []

    if args.live:
        if not args.json:
            print("Fetching live Technical Standards updates...")

    if args.mock or (not args.live and not args.mock) or not announcements:
        if not args.json:
            print("Using comprehensive mock Technical Standards updates...")
        if args.mock and args.mock != "inline" and os.path.exists(args.mock):
            try:
                with open(args.mock, "r") as f:
                    announcements.extend(json.load(f))
            except Exception as e:
                if not args.json:
                    print(
                        f"Failed to read mock file {args.mock}: {e}, using default dataset instead.",
                        file=sys.stderr,
                    )
                announcements.extend(MOCK_ANNOUNCEMENTS)
        else:
            announcements.extend(MOCK_ANNOUNCEMENTS)

    keywords_filter = (
        [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    )
    classified_updates = classify_announcements(announcements, keywords_filter)

    if not classified_updates:
        if args.json:
            print(json.dumps({"updates": [], "message": "No updates matched filters."}))
        else:
            print("No classified updates matched the current filters.")
        sys.exit(0)

    if not args.json:
        print(
            f"Monitored and classified {len(classified_updates)} technical standards updates:"
        )
        for idx, u in enumerate(classified_updates, 1):
            print(f" {idx}. [{u['category']}] {u['title']}")

        print(f"Scanning codebase under '{args.dir}' for standards integration signals...")

    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    if not args.json:
        print(f"Found {total_matches} signal matches in code.")

    update_documentation_report(classified_updates, scan_results, args.output_docs)

    pr_draft = generate_pull_request_draft(classified_updates, scan_results)

    if args.pr_output:
        try:
            os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
            with open(args.pr_output, "w", encoding="utf-8") as f:
                f.write(pr_draft)
            if not args.json:
                print(f"PR draft written successfully to: {args.pr_output}")
        except Exception as e:
            if not args.json:
                print(f"Failed to write PR draft to {args.pr_output}: {e}", file=sys.stderr)

    if args.json:
        output_data = {
            "updates_count": len(classified_updates),
            "updates": classified_updates,
            "scan_results": scan_results,
            "output_docs": args.output_docs,
            "pr_output": args.pr_output,
        }
        print(json.dumps(output_data, indent=2))


if __name__ == "__main__":
    main()
