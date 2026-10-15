#!/usr/bin/env python3
"""Monitors technical standards changes across 10 tracked categories:
ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards,
OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks. Identifies repository gaps,
generates implementation tasks, documentation updates, and testing updates."""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json

# 10 Tracked Technical Standards Categories
TRACKED_CATEGORIES = [
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

# Source Trust Hierarchy Definitions
TRUST_HIERARCHY = {
    "Priority 1": "ISO, IEC, NIST, OWASP, CIS, European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, CISA, ICO, Government publications",
    "Priority 2": "Reuters, AP, Bloomberg",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}

CATEGORY_KEYWORDS = {
    "ISO 27001": [
        "iso 27001",
        "iso27001",
        "isms",
        "information security management",
        "iso/iec 27001",
    ],
    "ISO 27701": [
        "iso 27701",
        "iso27701",
        "pims",
        "privacy information management",
        "iso/iec 27701",
    ],
    "ISO 42001": [
        "iso 42001",
        "iso42001",
        "aims",
        "ai management system",
        "iso/iec 42001",
    ],
    "ISO 31000": [
        "iso 31000",
        "iso31000",
        "risk management guidelines",
        "iso 31000:2018",
    ],
    "ISO 9001": [
        "iso 9001",
        "iso9001",
        "qms",
        "quality management system",
    ],
    "IEC standards": [
        "iec standards",
        "iec 62443",
        "iec 82304",
        "iec 62304",
        "iec",
    ],
    "OWASP": [
        "owasp",
        "owasp top 10",
        "masvs",
        "mstg",
        "asvs",
        "owasp mobile",
    ],
    "NIST AI RMF": [
        "nist ai rmf",
        "ai rmf",
        "ai risk management framework",
        "nist ai 100-1",
    ],
    "NIST CSF": [
        "nist csf",
        "cybersecurity framework",
        "nist csf 2.0",
        "csf 2.0",
    ],
    "CIS Benchmarks": [
        "cis benchmarks",
        "cis benchmark",
        "center for internet security",
        "cis controls",
    ],
}

CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO27001",
        r"ISMS",
        r"information_security",
        r"security_policy",
    ],
    "ISO 27701": [
        r"ISO27701",
        r"PIMS",
        r"privacy_management",
        r"privacy_policy",
    ],
    "ISO 42001": [
        r"ISO42001",
        r"AIMS",
        r"ai_governance",
        r"ai_management",
    ],
    "ISO 31000": [
        r"ISO31000",
        r"risk_assessment",
        r"risk_management",
        r"risk_register",
    ],
    "ISO 9001": [
        r"ISO9001",
        r"QMS",
        r"quality_assurance",
        r"quality_management",
    ],
    "IEC standards": [
        r"IEC",
        r"IEC62443",
        r"IEC82304",
        r"IEC62304",
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"MSTG",
    ],
    "NIST AI RMF": [
        r"NIST_AI_RMF",
        r"AIRMF",
        r"NIST_AI",
        r"ai_risk",
    ],
    "NIST CSF": [
        r"NIST_CSF",
        r"CSF",
        r"cybersecurity_framework",
    ],
    "CIS Benchmarks": [
        r"CIS_Benchmark",
        r"CIS_Control",
        r"cis_hardening",
    ],
}

MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001 Information Security Management Standard Revision",
        "description": "Updated controls for cloud security, threat intelligence, and secure coding mandating ISMS alignment and risk treatment updates.",
        "link": "https://www.iso.org/isoiec-27001-information-security.html",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Privacy Information Management System Requirements Update",
        "description": "Refined PIMS guidelines for personal data processors, consent management, and data subject rights enforcement.",
        "link": "https://www.iso.org/standard/71670.html",
        "pubDate": "Wed, 17 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 Artificial Intelligence Management System Implementation Standard",
        "description": "Establishment of governance, transparency, and risk controls for organizational deployment of AI systems.",
        "link": "https://www.iso.org/standard/81230.html",
        "pubDate": "Fri, 19 Jun 2026 12:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management Guidelines Update",
        "description": "Enhanced principles for identifying, assessing, and mitigating operational and technological risks.",
        "link": "https://www.iso.org/iso-31000-risk-management.html",
        "pubDate": "Mon, 22 Jun 2026 09:00:00 GMT",
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System Revisions",
        "description": "Updated QMS requirements focusing on software lifecycle quality, continuous improvement, and customer satisfaction metrics.",
        "link": "https://www.iso.org/iso-9001-quality-management.html",
        "pubDate": "Wed, 24 Jun 2026 14:00:00 GMT",
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62443 / IEC 82304 Industrial and Health Software Security Standard",
        "description": "Requirements for secure product development lifecycle, component verification, and medical/industrial software safety.",
        "link": "https://www.iec.ch/",
        "pubDate": "Fri, 26 Jun 2026 15:00:00 GMT",
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP MASVS / Top 10 Security Verification Standard Update",
        "description": "Revised mobile and web application security verification criteria targeting API security, authentication, and data storage.",
        "link": "https://owasp.org/",
        "pubDate": "Mon, 29 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework (AI RMF 1.0) Guidance",
        "description": "Framework guidelines for managing risks to individuals, organizations, and society from AI systems.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Wed, 01 Jul 2026 11:00:00 GMT",
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework 2.0 Governance and Implementation Guidelines",
        "description": "Expanded CSF functions adding Governance to Identify, Protect, Detect, Respond, and Recover pillars.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Fri, 03 Jul 2026 13:00:00 GMT",
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Controls and CIS Benchmarks Infrastructure Hardening Directives",
        "description": "Updated technical benchmarks for mobile OS, cloud environment, and container security configuration hardening.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Mon, 06 Jul 2026 14:00:00 GMT",
    },
]


def enforce_strict_source_trust_hierarchy(announcement):
    """Enforces source credibility hierarchy and logs verification alerts to stderr."""
    link = announcement.get("link", "").lower()
    title = announcement.get("title", "").lower()
    desc = announcement.get("description", "").lower()
    combined = f"{title} {desc} {link}"

    p1_domains = [
        "iso.org",
        "iec.ch",
        "nist.gov",
        "owasp.org",
        "cisecurity.org",
        "europa.eu",
        "eur-lex.europa.eu",
        "enisa.europa.eu",
        "edpb.europa.eu",
        "ftc.gov",
        "cisa.gov",
        "ico.org.uk",
        "gov.uk",
    ]
    p1_keywords = [
        "iso",
        "iec",
        "nist",
        "owasp",
        "cis",
        "european commission",
        "enisa",
        "edpb",
        "ftc",
        "cisa",
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p3_domains = ["arxiv.org", "ssrn.com"]
    p4_domains = ["techcrunch.com", "wired.com", "medium.com", "blog"]
    p5_domains = ["twitter.com", "x.com", "linkedin.com", "reddit.com"]

    priority = 4
    if any(d in link for d in p5_domains):
        priority = 5
    elif any(d in link for d in p4_domains):
        priority = 4
    elif any(d in link for d in p3_domains) or ".edu" in link:
        priority = 3
    elif any(d in link for d in p2_domains):
        priority = 2

    if any(d in link for d in p1_domains) or ".gov" in link or any(kw in combined for kw in p1_keywords):
        priority = 1

    if priority >= 4:
        sys.stderr.write(
            f"[TRUST ALERT] Announcement '{announcement.get('title')}' classified as Priority {priority}. Verification against Priority 1 source required.\n"
        )
    return priority


def scan_codebase_for_standards_signals(start_dir="."):
    """Scans codebase for signals related to each of the 10 standards categories."""
    matches = {cat: [] for cat in TRACKED_CATEGORIES}
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
        "dist",
    }

    compiled_signals = {
        cat: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        for cat, patterns in CATEGORY_SIGNALS.items()
    }

    for root, dirs, files in os.walk(start_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.endswith("Tests")]

        for file in files:
            if not file.endswith(
                (
                    ".kt",
                    ".java",
                    ".xml",
                    ".gradle",
                    ".kts",
                    ".json",
                    ".js",
                    ".ts",
                    ".swift",
                    ".m",
                    ".h",
                    ".plist",
                    ".entitlements",
                    ".md",
                    ".py",
                    ".sh",
                )
            ):
                continue

            filepath = os.path.join(root, file)
            if "monitor-standards" in file or "monitor-standards-test" in file:
                continue

            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        for cat, patterns in compiled_signals.items():
                            for pattern in patterns:
                                if pattern.search(line):
                                    matches[cat].append(
                                        {
                                            "file": filepath,
                                            "line_num": i,
                                            "content": line.strip()[:100],
                                            "matched_pattern": pattern.pattern,
                                        }
                                    )
                                    break
            except Exception:
                pass
    return matches


def parse_rss_feed(url):
    """Fetches and parses live RSS or Atom XML feeds."""
    items = []
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (StandardsComplianceMonitor/1.0)"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)

            def clean_tag(tag):
                return tag.split("}", 1)[1] if "}" in tag else tag

            for elem in root.iter():
                tag = clean_tag(elem.tag)
                if tag in ("item", "entry"):
                    title = desc = link = pub_date = ""
                    for child in elem:
                        ctag = clean_tag(child.tag)
                        if ctag == "title":
                            title = child.text or ""
                        elif ctag in ("description", "summary", "content"):
                            desc = child.text or ""
                        elif ctag == "link":
                            link_val = child.get("href")
                            link = link_val if link_val else (child.text or "")
                        elif ctag in ("pubDate", "published", "updated"):
                            pub_date = child.text or ""

                    items.append(
                        {
                            "title": title.strip(),
                            "description": desc.strip() if desc else "",
                            "link": link.strip(),
                            "pubDate": pub_date.strip(),
                        }
                    )
    except Exception as e:
        print(f"Warning: Failed to fetch live feed {url}: {e}", file=sys.stderr)
    return items


def classify_announcements(announcements, keywords_filter=None):
    """Classifies incoming announcements into the 10 technical standards categories."""
    classified_updates = []

    for ann in announcements:
        enforce_strict_source_trust_hierarchy(ann)
        title = ann.get("title", "")
        desc = ann.get("description", "")
        text_to_search = (title + " " + desc).lower()

        if keywords_filter:
            if not any(k.lower() in text_to_search for k in keywords_filter):
                continue

        matched_categories = []
        for cat, keywords in CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in text_to_search:
                    matched_categories.append(cat)
                    break

        if not matched_categories and ann.get("category"):
            matched_categories.append(ann["category"])

        if matched_categories:
            for cat in matched_categories:
                classified_updates.append(
                    {
                        "id": ann.get("id", "STD-UPDATE-" + str(hash(title))[:6]),
                        "category": cat,
                        "title": title,
                        "description": desc,
                        "link": ann.get("link", ""),
                        "pubDate": ann.get("pubDate", ""),
                    }
                )
    return classified_updates


def generate_pull_request_draft(updates, scan_results):
    """Generates a draft of a pull request complying with the exact 15 required sections."""
    citations_list = []
    affected_files_set = set()
    migration_steps = []
    impl_checklist = []
    risk_assessment = []
    testing_tasks = []
    processed_categories = set()

    for idx, u in enumerate(updates, 1):
        cat = u["category"]
        citations_list.append(
            f"- **{cat}**: [{u['title']}]({u['link']}) (Published: {u['pubDate']})"
        )

        files = scan_results.get(cat, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        if cat in processed_categories:
            continue
        processed_categories.add(cat)

        migration_steps.append(
            f"- **{cat}**: Align system architecture, policies, and controls with the updated {cat} framework requirements."
        )
        impl_checklist.append(
            f"- [ ] Implement {cat} policy controls and update corresponding codebase modules."
        )
        risk_assessment.append(
            f"- *{cat}*: Non-compliance may lead to audit failures, security vulnerabilities, or loss of technical certification."
        )
        testing_tasks.append(
            f"- [ ] Execute {cat} verification suite and confirm compliance controls pass automated tests."
        )

    citations_str = "\n".join(citations_list)

    if affected_files_set:
        affected_files_str = "\n".join(
            f"- `{f}`" for f in sorted(list(affected_files_set))
        )
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual audit).* "

    migration_steps_str = "\n".join(migration_steps)
    impl_checklist_str = "\n".join(impl_checklist)
    risk_assessment_str = "\n".join(risk_assessment)
    testing_tasks_str = "\n".join(testing_tasks)

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request aligns the codebase and technical infrastructure with updated technical standards across monitored domains (ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks).

## 2. Background
Technical standards evolve to address emerging security vulnerabilities, privacy expectations, quality assurance metrics, and artificial intelligence governance requirements. Adherence to industry standards ensures organizational integrity and regulatory alignment.

## 3. Regulatory change
- **Technical Standards Alignment**: Synchronizes security, privacy, risk management, and AI governance practices with updated official publication guidelines.
- **Verification Framework**: Mandates continuous scanning, gaps identification, implementation tracking, and automated verification.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: Operational and compliance risk managed through structured controls update and automated testing verification.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes maintain backward compatibility. System interfaces and existing APIs remain functional while security and governance controls are upgraded.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Re-run the automated compliance guard checks locally.

## 10. Testing checklist
{testing_tasks_str}
- [ ] Verify static analysis rules and compliance monitoring scripts pass with zero errors.

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with completed migration tasks.
- [ ] Document technical controls, risk treatment plans, and testing results in repository guides.

## 12. Compliance impact
- **Standards Aligned**: Satisfies requirements for ISO, IEC, OWASP, NIST, and CIS benchmarks.
- **Risk Mitigation**: Ensures gap closure and audit readiness across organizational policies.

## 13. Breaking changes
- No breaking schema or API changes introduced.

## 14. Review checklist
- [ ] Code and documentation are 100% free of emojis or graphical symbols.
- [ ] Official citations reference verified Priority 1 sources.
- [ ] Implementation and testing tasks are fully defined per standard category.

## 15. Approver recommendations
Verify that all category-level implementation and testing tasks have been executed and validated against official standards documentation.
"""
    return pr_template


SIMULATED_NOTICE = [
    "",
    "> **Simulated output, not live announcements.** This file was generated from sample",
    "> announcements (the built-in set, the default, or a file passed with `--mock`). The titles,",
    "> publish dates, and descriptions below are examples that show the shape of a migration",
    "> report, not real publications. Only the linked official documentation URLs are real.",
    "> Re-run the monitor with `--live` against the real feeds before treating anything here",
    "> as an actual requirement.",
    "",
]


def update_documentation_report(updates, scan_results, output_filepath, is_simulated=False):
    """Writes or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md."""
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
    ]
    if is_simulated:
        lines.extend(SIMULATED_NOTICE)
    lines.extend([
        "# Technical Standards Policy Migration & Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track technical standards compliance.",
        "",
        "## Monitored Technical Standards Update Log",
        "",
    ])

    for idx, u in enumerate(updates, 1):
        lines.append(f"### {idx}. [{u['category']}] {u['title']}")
        lines.append(f"- **Published Date**: {u['pubDate']}")
        lines.append(f"- **Official Resource**: [{u['link']}]({u['link']})")
        lines.append(f"- **Description**: {u['description']}")
        lines.append("")

    lines.append("## Identified Repository Gaps")
    lines.append("")
    for cat in TRACKED_CATEGORIES:
        matches = scan_results.get(cat, [])
        if matches:
            lines.append(f"### Gaps for {cat}")
            for m in matches:
                lines.append(f"- Found signal `{m['matched_pattern']}` in `{m['file']}` (Line {m['line_num']})")
            lines.append("")

    lines.append("## Implementation Tasks")
    lines.append("")
    processed_cats = set()
    for u in updates:
        cat = u["category"]
        if cat in processed_cats:
            continue
        processed_cats.add(cat)
        lines.append(f"### Tasks for {cat}")
        lines.append(f"- [ ] **Task 1**: Update architecture and code controls to satisfy {cat} requirement.")
        lines.append(f"- [ ] **Task 2**: Document risk treatment and control mappings for {cat}.")
        lines.append("")

    lines.append("## Documentation Updates")
    lines.append("")
    for cat in processed_cats:
        lines.append(f"- [ ] Update policy guides and compliance reports for {cat}.")
    lines.append("")

    lines.append("## Testing Updates")
    lines.append("")
    for cat in processed_cats:
        lines.append(f"- [ ] Execute test verification suite for {cat} controls.")
    lines.append("")

    lines.append("<!-- STANDARDS_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"Standards documentation updated successfully at: {output_filepath}")
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor Technical Standards Changes (ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC, OWASP, NIST AI RMF, NIST CSF, CIS Benchmarks)"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live feeds for technical standards"
    )
    parser.add_argument(
        "--mock",
        type=str,
        help="Path to custom mock announcements JSON file, or 'inline' to use default mock data",
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
        default=None,
        help="Filepath to write migration tasks and logs",
    )
    parser.add_argument(
        "--pr-output",
        type=str,
        default=None,
        help="Filepath to save the drafted PR",
    )

    args = parser.parse_args()

    announcements = []

    ISO_RSS = "https://www.iso.org/rss/x"

    if args.live:
        announcements.extend(parse_rss_feed(ISO_RSS))

    used_mock = False
    if args.mock or (not args.live and not args.mock) or not announcements:
        used_mock = True
        print("Data. sample announcements built into this script, not live news.")
        print("Using comprehensive mock Technical Standards policy updates for compliance scanning...")
        if args.mock and args.mock != "inline" and os.path.exists(args.mock):
            try:
                with open(args.mock, "r") as f:
                    announcements.extend(json.load(f))
            except Exception as e:
                print(
                    f"Failed to read mock file {args.mock}: {e}, using default mock dataset instead.",
                    file=sys.stderr,
                )
                announcements.extend(MOCK_ANNOUNCEMENTS)
        else:
            announcements.extend(MOCK_ANNOUNCEMENTS)
    else:
        print("Data. live feeds, fetched just now.")

    keywords_filter = (
        [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    )
    classified_updates = classify_announcements(announcements, keywords_filter)

    if not classified_updates:
        print("No classified updates matched the current filters.")
        sys.exit(0)

    print(f"Monitored and classified {len(classified_updates)} technical standards updates:")
    for idx, u in enumerate(classified_updates, 1):
        print(f" {idx}. [{u['category']}] {u['title']}")

    print(f"Scanning codebase under '{args.dir}' for technical standards integration signals...")
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    if args.output_docs:
        os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
        update_documentation_report(classified_updates, scan_results, args.output_docs, is_simulated=used_mock)
    else:
        print("No file written. Pass --output-docs <path> to save this report.")

    pr_draft = generate_pull_request_draft(classified_updates, scan_results)
    if used_mock:
        pr_draft = "\n".join(SIMULATED_NOTICE[1:]) + "\n" + pr_draft

    if args.pr_output:
        try:
            os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
            with open(args.pr_output, "w", encoding="utf-8") as f:
                f.write(pr_draft)
            print(f"PR draft written successfully to: {args.pr_output}")
        except Exception as e:
            print(f"Failed to write PR draft to {args.pr_output}: {e}", file=sys.stderr)
    else:
        print("No PR draft written. Pass --pr-output <path> to save it.")


if __name__ == "__main__":
    main()
