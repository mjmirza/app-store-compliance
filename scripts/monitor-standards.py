#!/usr/bin/env python3
"""
Technical Standards Compliance Requirements Monitoring Utility.
Tracks 10 key technical standards and generates repo-gap/migration tasks for each.
"""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json

# The 10 tracked technical standards
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
    "CIS Benchmarks"
]

# Keywords used to classify incoming policy announcements/articles into the 10 categories
CATEGORY_KEYWORDS = {
    "ISO 27001": ["iso 27001", "iso/iec 27001", "isms", "information security management system", "annex a"],
    "ISO 27701": ["iso 27701", "iso/iec 27701", "pims", "privacy information management system"],
    "ISO 42001": ["iso 42001", "iso/iec 42001", "aims", "artificial intelligence management system", "ai governance"],
    "ISO 31000": ["iso 31000", "risk management guidelines", "risk assessment framework", "risk treatment"],
    "ISO 9001": ["iso 9001", "qms", "quality management system", "quality policy"],
    "IEC standards": ["iec standard", "iec 62304", "iec 82304", "medical device software", "software lifecycle"],
    "OWASP": ["owasp", "masvs", "mstg", "asvs", "owasp top 10"],
    "NIST AI RMF": ["nist ai rmf", "ai risk management framework", "trustworthy ai", "nist-ai"],
    "NIST CSF": ["nist csf", "cybersecurity framework", "nist-csf", "identify protect detect"],
    "CIS Benchmarks": ["cis benchmark", "cis critical security controls", "cis-controls", "secure baseline"]
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO 27001",
        r"ISMS",
        r"access-control-policy",
        r"information-security-policy"
    ],
    "ISO 27701": [
        r"ISO 27701",
        r"PIMS",
        r"privacy-information-management",
        r"PII-protection"
    ],
    "ISO 42001": [
        r"ISO 42001",
        r"AIMS",
        r"ai-governance-policy",
        r"model-risk-management"
    ],
    "ISO 31000": [
        r"ISO 31000",
        r"risk-assessment",
        r"risk-register",
        r"risk-mitigation-plan"
    ],
    "ISO 9001": [
        r"ISO 9001",
        r"QMS",
        r"quality-assurance-policy",
        r"continual-improvement"
    ],
    "IEC standards": [
        r"IEC-62304",
        r"IEC-82304",
        r"software-lifecycle-processes",
        r"medical-device-software"
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"MSTG",
        r"ASVS"
    ],
    "NIST AI RMF": [
        r"NIST AI RMF",
        r"AI-RMF",
        r"trustworthy-ai-system",
        r"bias-mitigation"
    ],
    "NIST CSF": [
        r"NIST CSF",
        r"cybersecurity-framework",
        r"incident-response-plan",
        r"continuous-monitoring-plan"
    ],
    "CIS Benchmarks": [
        r"CIS Benchmark",
        r"CIS-Controls",
        r"secure-hardening-baseline",
        r"cis-hardening"
    ]
}

# Source trust domains and keywords for verification
TRUST_HIERARCHY = {
    "Priority 1": "Official sources (ISO, IEC, NIST, CISA, OWASP, FTC, EDPB, European Commission, ICO, Government publications)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries"
}

# 10 Comprehensive Mock Announcements for all 10 categories
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STAND-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO 27001:2022 Transition and ISMS Policy Requirements Update",
        "description": "Organizations must transition their ISMS to ISO 27001:2022, introducing new controls under Annex A. Access control policy, asset management, and physical/digital security-by-design are mandated.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 PDT",
    },
    {
        "id": "STAND-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO 27701 Privacy Information Management Guidelines Extension",
        "description": "ISO/IEC 27701:2019 defines requirements for establishing a Privacy Information Management System (PIMS). Organizations must ensure strict PII-protection and dynamic consent recording.",
        "link": "https://www.iso.org/standard/71670.html",
        "pubDate": "Wed, 17 Jun 2026 11:00:00 PDT",
    },
    {
        "id": "STAND-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO 42001 Artificial Intelligence Management System (AIMS) Launch",
        "description": "ISO/IEC 42001:2023 specifies AI governance rules. Model transparency, ethical checks, bias mitigations, and systemic model risk management are required under this framework.",
        "link": "https://www.iso.org/standard/81230.html",
        "pubDate": "Fri, 19 Jun 2026 12:00:00 PDT",
    },
    {
        "id": "STAND-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Enterprise Risk Management Update and Assessment Guidelines",
        "description": "New directives under ISO 31000 mandate dynamic risk registers, clear risk-assessment workflows, and formalized risk-mitigation plans across all critical corporate IT systems.",
        "link": "https://www.iso.org/iso-31000-risk-management.html",
        "pubDate": "Mon, 22 Jun 2026 09:00:00 PDT",
    },
    {
        "id": "STAND-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System (QMS) Digital Improvement Standards",
        "description": "Updates to ISO 9001 mandate explicit quality-assurance policies and continual-improvement benchmarks to ensure digital deliverables are consistently built to standard.",
        "link": "https://www.iso.org/standard/62085.html",
        "pubDate": "Wed, 24 Jun 2026 14:00:00 PDT",
    },
    {
        "id": "STAND-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62304 Medical Device Software Lifecycle Processes Policy",
        "description": "IEC 62304 defines software development and lifecycle requirements for medical software. Robust verification, risk tracking, and secure lifecycle processes are strictly audited.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Fri, 26 Jun 2026 15:00:00 PDT",
    },
    {
        "id": "STAND-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP MASVS Compliance Guidelines for Enterprise App Publishing",
        "description": "The Mobile Application Security Verification Standard (MASVS) establishes baseline security profiles. Apps must satisfy L1 and L2 requirements, verified via continuous automated guards.",
        "link": "https://mas.owasp.org/MASVS/",
        "pubDate": "Mon, 29 Jun 2026 10:00:00 PDT",
    },
    {
        "id": "STAND-MOCK-NISTAI",
        "category": "NIST AI RMF",
        "title": "NIST AI RMF Playbook: Trustworthy AI System Guardrails",
        "description": "The NIST Artificial Intelligence Risk Management Framework provides guidance to manage AI risks. Developers must audit systems for bias-mitigation, transparency, and safety metrics.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Wed, 01 Jul 2026 11:00:00 PDT",
    },
    {
        "id": "STAND-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST CSF 2.0 Cybersecurity Framework Revision",
        "description": "NIST Cybersecurity Framework 2.0 expands governing standards, requiring rapid incident response plans, continuous monitoring plans, and broader organizational risk profiles.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Fri, 03 Jul 2026 13:00:00 PDT",
    },
    {
        "id": "STAND-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Controls and Secure Hardening Baselines Guidelines",
        "description": "CIS Benchmarks establish secure configuration and hardening profiles. Cloud systems and mobile container boundaries must be verified against official hardening baselines.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Mon, 06 Jul 2026 14:00:00 PDT",
    },
    {
        "id": "STAND-MOCK-UNVERIFIED-BLOG",
        "category": "ISO 27001",
        "title": "Unverified Industry Blog Rumors on ISO 27001",
        "description": "A random industry blog claims ISO 27001 rules are being completely revoked next week. This is an unverified blog post.",
        "link": "https://randomblogsite.com/iso-rumor",
        "pubDate": "Wed, 08 Jul 2026 11:00:00 PDT",
    }
]


def classify_source_and_verify(announcement, all_announcements=None):
    """
    Classifies an announcement by TRUST_HIERARCHY priority (1-5) and
    verification status. Returns (priority_level, is_verified).
    """
    link = announcement.get("link", "").lower()
    title = announcement.get("title", "").lower()
    desc = announcement.get("description", "").lower()
    combined = f"{title} {desc} {link}"

    # Priority 1 official domains and keywords
    p1_domains = [
        "iso.org", "iec.ch", "nist.gov", "cisa.gov", "owasp.org", "mas.owasp.org",
        "europa.eu", "eur-lex.europa.eu", "enisa.europa.eu", "edpb.europa.eu",
        "ftc.gov", "ico.org.uk", "gov.uk", "gov.sg", "cisecurity.org"
    ]
    p1_keywords = [
        "international organization for standardization", "iec", "nist", "cisa", "owasp",
        "european commission", "eur-lex", "official journal", "enisa", "edpb",
        "ftc", "ico", "government publication", "cis benchmarks"
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com"]
    p3_keywords = ["academic paper", "academic study", "university research", "peer-reviewed"]

    p4_domains = ["techcrunch.com", "wired.com", "medium.com", "blog", "randomblogsite.com"]
    p4_keywords = ["industry blog", "tech blog", "blog post", "editorial"]

    p5_domains = ["twitter.com", "x.com", "linkedin.com", "reddit.com", "t.co"]
    p5_keywords = ["tweet", "twitter", "linkedin", "reddit", "ai summary", "ai-generated summary", "ai generated summaries", "chatgpt summary"]

    priority = 4  # Default to 4 if nothing matches

    if any(d in link for d in p5_domains) or any(kw in combined for kw in p5_keywords):
        priority = 5
    elif any(d in link for d in p4_domains) or any(kw in combined for kw in p4_keywords):
        priority = 4
    elif any(d in link for d in p3_domains) or any(kw in combined for kw in p3_keywords) or ".edu" in link:
        priority = 3
    elif any(d in link for d in p2_domains) or any(kw in combined for kw in p2_keywords):
        priority = 2

    if any(d in link for d in p1_domains) or any(kw in combined for kw in p1_keywords) or ".gov" in link:
        priority = 1

    is_verified = False
    if priority <= 3:
        is_verified = True
    else:
        # Priority 4 or 5: Must be verified by a Priority 1 official source
        has_p1_ref_in_text = False
        for d in p1_domains:
            if d in combined:
                has_p1_ref_in_text = True
                break
        if not has_p1_ref_in_text:
            for kw in p1_keywords:
                if kw in combined:
                    has_p1_ref_in_text = True
                    break
        if ".gov" in combined:
            has_p1_ref_in_text = True

        if has_p1_ref_in_text:
            is_verified = True
        elif all_announcements:
            words = set(re.findall(r"[a-z]+", combined))
            for other in all_announcements:
                if other == announcement:
                    continue
                other_p, _ = classify_source_and_verify(other, None)
                if other_p == 1:
                    other_combined = f"{other.get('title', '')} {other.get('description', '')} {other.get('link', '')}".lower()
                    other_words = set(re.findall(r"[a-z]+", other_combined))
                    common_terms = {"standard", "security", "framework", "compliance", "iso", "nist", "owasp"}
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def enforce_strict_source_trust_hierarchy(announcement, all_announcements=None):
    """
    Enforces strict source trust hierarchy, logs alerts to stderr, and returns
    whether the announcement source is verified.
    """
    priority, is_verified = classify_source_and_verify(announcement, all_announcements)
    if priority in (4, 5) and not is_verified:
        print(f"ALERT: Announcement '{announcement.get('title')}' is from an unverified source (Priority {priority}). Blocking PR draft generation.", file=sys.stderr)
        return False
    return True


def scan_codebase_for_standards_signals(start_dir="."):
    """
    Scans the codebase for files containing signals related to each of the 10 technical standards.
    Excludes typical build, dependency, and test directories.
    """
    matches = {cat: [] for cat in TRACKED_CATEGORIES}
    exclude_dirs = {
        "node_modules", "Pods", ".git", "build", "DerivedData", "vendor",
        ".dart_tool", "Carthage", "androidTest", "__tests__", "dist", "docs"
    }

    # Compile the signal patterns
    compiled_signals = {
        cat: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        for cat, patterns in CATEGORY_SIGNALS.items()
    }

    for root, dirs, files in os.walk(start_dir):
        # Prune excluded directories in-place
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.endswith("Tests")]

        for file in files:
            # Check applicable file types
            if not file.endswith(
                (
                    ".kt", ".java", ".xml", ".gradle", ".kts", ".json", ".js",
                    ".ts", ".md", ".swift", ".m", ".h", ".plist", ".html"
                )
            ):
                continue

            filepath = os.path.join(root, file)
            # Skip monitor scripts to avoid self-referencing matches
            if "monitor-standards" in file:
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
                                    break  # match found for this line and category, proceed
            except Exception:
                pass
    return matches


def parse_rss_feed(url):
    """
    Fetches and parses live RSS or Atom XML feeds.
    """
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
                    title = ""
                    desc = ""
                    link = ""
                    pub_date = ""

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
    """
    Classifies incoming announcements into the 10 Technical Standards categories.
    """
    classified_updates = []

    for ann in announcements:
        title = ann.get("title", "")
        desc = ann.get("description", "")
        text_to_search = (title + " " + desc).lower()

        # If keywords_filter is supplied, verify if any filter matches
        if keywords_filter:
            if not any(k.lower() in text_to_search for k in keywords_filter):
                continue

        # Match against categories
        matched_categories = []
        for cat, keywords in CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in text_to_search:
                    matched_categories.append(cat)
                    break  # Break keyword loop for this category

        # Fallback to predefined category if set
        if not matched_categories and ann.get("category"):
            matched_categories.append(ann["category"])

        if matched_categories:
            for cat in matched_categories:
                classified_updates.append(
                    {
                        "id": ann.get("id", "STAND-UPDATE-" + str(hash(title))[:6]),
                        "category": cat,
                        "title": title,
                        "description": desc,
                        "link": ann.get("link", ""),
                        "pubDate": ann.get("pubDate", ""),
                    }
                )
    return classified_updates


def generate_pull_request_draft(updates, scan_results):
    """
    Generates a draft of a pull request complying with the exact 15 required sections.
    """
    citations_list = []
    affected_files_set = set()
    migration_steps = []
    impl_checklist = []
    risk_assessment = []
    testing_steps = []

    for idx, u in enumerate(updates, 1):
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
        citations_list.append(
            f"- **{cat}**: [{u['title']}]({u['link']}) (Published: {u['pubDate']}, Source: {status_str})"
        )

        # Pull affected files
        files = scan_results.get(cat, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        # Category-specific details (including gaps, implementation tasks, testing updates)
        if cat == "ISO 27001":
            migration_steps.append(
                f"- **{cat}**: Update access control policies and asset management frameworks to align with Annex A controls."
            )
            impl_checklist.append("- [ ] Document access control policies and asset register frameworks.")
            risk_assessment.append(f"- *{cat}*: Non-conformity in information security management systems (ISMS), exposing organizational data assets.")
            testing_steps.append("- [ ] Verify no unencrypted tokens or keys are present in repository configurations.")
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Audit PII data flows and define structural PII-protection guidelines."
            )
            impl_checklist.append("- [ ] Create a detailed inventory of personally identifiable information (PII).")
            risk_assessment.append(f"- *{cat}*: Improper handling of PII data violating privacy-by-design frameworks.")
            testing_steps.append("- [ ] Test restricted logging functions to confirm zero PII is leaked in log outputs.")
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Implement ethical model checks, safety boundaries, and robust AI governance controls."
            )
            impl_checklist.append("- [ ] Document AI system risk assessments and model-risk-management declarations.")
            risk_assessment.append(f"- *{cat}*: Unregulated generative AI integrations violating global transparency requirements.")
            testing_steps.append("- [ ] Run verification tests ensuring proper content moderation boundaries are active.")
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Maintain a dynamic risk register and integrate structured risk-assessment workflows."
            )
            impl_checklist.append("- [ ] Create/update the enterprise risk register file inside standard playbooks.")
            risk_assessment.append(f"- *{cat}*: Undocumented system risks leading to untracked software delivery vulnerabilities.")
            testing_steps.append("- [ ] Verify pipeline checks trigger warnings for any vulnerable dependency imports.")
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Formulate quality-assurance policies and configure continual-improvement gates."
            )
            impl_checklist.append("- [ ] Document quality management system (QMS) guidelines.")
            risk_assessment.append(f"- *{cat}*: Decline in software quality due to lack of standard regression targets.")
            testing_steps.append("- [ ] Confirm build pipeline enforces strict linting and code coverage gates.")
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Separate software lifecycle processes for safety-critical pathways."
            )
            impl_checklist.append("- [ ] Document lifecycle processes matching IEC 62304 / IEC 82304 requirements.")
            risk_assessment.append(f"- *{cat}*: Inadequate verification of safety-critical software pathways.")
            testing_steps.append("- [ ] Execute automated path coverage tests for medical/critical modules.")
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Align with OWASP MASVS baseline security requirements."
            )
            impl_checklist.append("- [ ] Implement security configurations to mitigate MASVS identified vulnerabilities.")
            risk_assessment.append(f"- *{cat}*: Vulnerabilities listed in OWASP Top 10 exposed in mobile or web clients.")
            testing_steps.append("- [ ] Run static application security tests (SAST) during local compilation audits.")
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Set up bias-mitigation checks and establish trustworthy-ai logging metrics."
            )
            impl_checklist.append("- [ ] Add trustworthy-ai system declarations in AI development rules.")
            risk_assessment.append(f"- *{cat}*: Model drift, algorithmic bias, or unaligned AI behavior.")
            testing_steps.append("- [ ] Validate AI model outputs using structured baseline test datasets.")
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Configure incident-response plans and continuous-monitoring configurations."
            )
            impl_checklist.append("- [ ] Document the incident-response procedures in security folders.")
            risk_assessment.append(f"- *{cat}*: Inability to detect or recover from zero-day cybersecurity incidents.")
            testing_steps.append("- [ ] Execute simulated incident response tabletops and verify automated alerts.")
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Hardon deployment containers to establish secure configuration baselines."
            )
            impl_checklist.append("- [ ] Align Dockerfiles and deployment scripts to CIS critical security controls.")
            risk_assessment.append(f"- *{cat}*: Exploit vectors inside default, unhardened infrastructure runtimes.")
            testing_steps.append("- [ ] Run automated secure baseline hardening scans on final container bundles.")

    citations_str = "\n".join(citations_list) if citations_list else "- *No updates cited.*"

    if affected_files_set:
        affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set)))
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- *No migration steps identified.*"
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- [ ] Perform general verification of compliance policies."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- *Low identified risk.*"
    testing_steps_str = "\n".join(testing_steps) if testing_steps else "- [ ] Perform generic security unit tests."

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request introduces critical configuration and documentation modifications to bring our systems into complete alignment with international standards and frameworks. It addresses security, privacy, quality, and AI governance requirements to maintain absolute regulatory compliance.

## 2. Background
Adhering to recognized technical standards ensures that our systems are built on secure, reliable, and compliant foundations. This PR proactively resolves identified repository gaps and integrates continuous verification safeguards.

## 3. Regulatory change
- **Security and Privacy Standards**: Adopting Annex A controls under ISO 27001:2022, PII protections under ISO 27701, and secure baseline hardening under CIS Benchmarks and NIST CSF.
- **AI Governance Frameworks**: Implementing ethical boundaries, risk management, and bias mitigation metrics in alignment with ISO 42001 and NIST AI RMF guidelines.
- **Quality and Safety Guidelines**: Enhancing quality-assurance gates under ISO 9001 and lifecycle management under IEC standards.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High operational risk and potential compliance failures if our development models do not enforce these rigorous frameworks.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes are fully backward-compatible. Technical standard adjustments consist of modular configuration hardening, updated risk registries, and documentation audits, which preserve existing functional boundaries.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run the repository-wide automated compliance guard.

## 10. Testing checklist
{testing_steps_str}
- [ ] Ensure that build pipelines execute successfully with no security alerts.

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with the completed actions.
- [ ] Document specific hardening controls and incident response policies in developer playbooks.

## 12. Compliance impact
- **Enterprise Readiness**: Satisfies vendor compliance requirements and clears third-party information security audits.
- **System Hardening**: Mitigates exposure to zero-day vulnerabilities and data leakage exploits.
- **Ethics and Transparency**: Builds trusted AI pathways in alignment with NIST and ISO.

## 13. Breaking changes
- No functional breaking changes are introduced. Strict security controls may restrict certain unrestricted legacy debug access points.

## 14. Review checklist
- [ ] Verify that the diff is completely emoji-free.
- [ ] Verify that all official sources cited are correct and verified.
- [ ] Verify that sensitive local credentials are fully encrypted.

## 15. Approver recommendations
Ensure that the updated risk registers and QA policies are formally integrated into the corporate compliance database. Review the CIS Benchmarks container hardening reports prior to merging this update.
"""
    return pr_template


def update_documentation_report(updates, scan_results, output_filepath):
    """
    Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md.
    """
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Policy Migration & Requirements Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track technical standards compliance.",
        "",
        "## Monitored Technical Standards Update Log",
        "",
    ]

    for idx, u in enumerate(updates, 1):
        priority, is_verified = classify_source_and_verify(u)
        status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
        lines.append(f"### {idx}. [{u['category']}] {u['title']}")
        lines.append(f"- **Published Date**: {u['pubDate']}")
        lines.append(f"- **Official Resource**: [{u['link']}]({u['link']})")
        lines.append(f"- **Verification Status**: {status_str}")
        lines.append(f"- **Description**: {u['description']}")
        lines.append("")

    lines.append("## Repository Gap Analysis")
    lines.append("")
    for cat in TRACKED_CATEGORIES:
        matches = scan_results.get(cat, [])
        lines.append(f"### Gap Analysis for {cat}")
        if matches:
            lines.append(f"- **Status**: Signal detected in codebase ({len(matches)} match(es)).")
            lines.append("- **Detected Files**:")
            for m in matches:
                lines.append(f"  - `{m['file']}` (Line {m['line_num']}): `{m['content']}`")
        else:
            lines.append("- **Status**: No direct matching signal detected. Manual verification recommended.")
        lines.append("")

    lines.append("## Automated Migration Recommendations & Implementation Tasks")
    lines.append("")

    for u in updates:
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        if priority in (4, 5) and not is_verified:
            lines.append(f"### Tasks for {cat} (BLOCKED: Announcement source is unverified)")
            lines.append("- **Regulatory Status**: Suspended. Source is an unverified Priority 4/5 secondary source.")
            lines.append("")
            continue

        lines.append(f"### Tasks for {cat}")
        lines.append("- **Regulatory Impact**: High priority compliance area.")

        if cat == "ISO 27001":
            lines.append("- [ ] **Task 1**: Update standard access control policies to align with ISO 27001:2022 Annex A controls.")
            lines.append("- [ ] **Task 2**: Formulate the digital and physical security-by-design baseline.")
        elif cat == "ISO 27701":
            lines.append("- [ ] **Task 1**: Perform a thorough audit of all PII data flows in the application.")
            lines.append("- [ ] **Task 2**: Establish PIMS guidelines and data minimization constraints.")
        elif cat == "ISO 42001":
            lines.append("- [ ] **Task 1**: Draft an AI system risk assessment covering ethics, bias, and safety metrics.")
            lines.append("- [ ] **Task 2**: Implement content moderation and model transparency disclosures.")
        elif cat == "ISO 31000":
            lines.append("- [ ] **Task 1**: Construct a dynamic enterprise risk register.")
            lines.append("- [ ] **Task 2**: Configure risk-assessment triggers in the software release workflow.")
        elif cat == "ISO 9001":
            lines.append("- [ ] **Task 1**: Document quality management system (QMS) policies.")
            lines.append("- [ ] **Task 2**: Enforce code coverage thresholds and regression testing benchmarks.")
        elif cat == "IEC standards":
            lines.append("- [ ] **Task 1**: Document software lifecycle processes in compliance with IEC 62304 / IEC 82304.")
            lines.append("- [ ] **Task 2**: Implement automated path coverage verification for critical safety components.")
        elif cat == "OWASP":
            lines.append("- [ ] **Task 1**: Review codebase against OWASP MASVS baseline profiles.")
            lines.append("- [ ] **Task 2**: Mitigate standard OWASP Top 10 vulnerabilities (such as insecure local storage).")
        elif cat == "NIST AI RMF":
            lines.append("- [ ] **Task 1**: Establish bias-mitigation filters and construct model behavior logging.")
            lines.append("- [ ] **Task 2**: Conduct safety and trustworthiness evaluation tests on AI systems.")
        elif cat == "NIST CSF":
            lines.append("- [ ] **Task 1**: Configure a formal incident response plan.")
            lines.append("- [ ] **Task 2**: Set up automated alerting rules for continuous cybersecurity monitoring.")
        elif cat == "CIS Benchmarks":
            lines.append("- [ ] **Task 1**: Harden container deployment scripts (e.g., Dockerfiles).")
            lines.append("- [ ] **Task 2**: Run secure hardening baseline scans prior to bundling builds.")
        else:
            lines.append(f"- [ ] **Task**: Verify that all standard criteria for {cat} are checked and handled.")
        lines.append("")

    lines.append("## Automated Testing Updates")
    lines.append("")
    for u in updates:
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        if priority in (4, 5) and not is_verified:
            continue
        lines.append(f"### Testing Updates for {cat}")
        if cat == "ISO 27001":
            lines.append("- [ ] Test access-control-policy implementations and scan configurations for raw credentials.")
        elif cat == "ISO 27701":
            lines.append("- [ ] Validate that debug logs are sanitized of all personally identifiable information (PII).")
        elif cat == "ISO 42001":
            lines.append("- [ ] Verify content moderation boundaries and model-risk-management consent dialogues.")
        elif cat == "ISO 31000":
            lines.append("- [ ] Automate dependency vulnerability scanner checks to flag vulnerable third-party imports.")
        elif cat == "ISO 9001":
            lines.append("- [ ] Integrate automated linting, type-checking, and code coverage checks in CI pipelines.")
        elif cat == "IEC standards":
            lines.append("- [ ] Enforce automated unit testing and safety-critical path checks for critical modules.")
        elif cat == "OWASP":
            lines.append("- [ ] Execute static and dynamic application security scans (SAST/DAST) during release audits.")
        elif cat == "NIST AI RMF":
            lines.append("- [ ] Run verification test cases against AI system models to identify drift and bias metrics.")
        elif cat == "NIST CSF":
            lines.append("- [ ] Run continuous vulnerability checks and simulated incident tabletop verification.")
        elif cat == "CIS Benchmarks":
            lines.append("- [ ] Execute automated CIS hardening validation scans against configuration files.")
        lines.append("")

    lines.append("<!-- STANDARDS_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        # Status log should be printed to stderr if --json is active, else stdout
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor all Technical Standards Requirements"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live standards news feeds"
    )
    parser.add_argument(
        "--mock",
        type=str,
        default="inline",
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
        "--json", action="store_true", help="Output JSON report to stdout"
    )

    args = parser.parse_args()

    # Determine logging destination
    log_file = sys.stderr if args.json else sys.stdout

    # 1. Gather announcements
    announcements = []

    if args.live:
        print("Fetching live standards news RSS feeds...", file=log_file)
        announcements.extend(parse_rss_feed("https://www.iso.org/contents/feeds/news.xml"))
        announcements.extend(parse_rss_feed("https://www.nist.gov/news-events/cybersecurity/rss.xml"))

    # Fallback to mock data if live has no updates, or mock is explicitly requested (default)
    if args.mock or (not args.live and not args.mock) or not announcements:
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

    # 2. Classify updates into the 10 required categories
    keywords_filter = (
        [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    )
    classified_updates = classify_announcements(announcements, keywords_filter)

    if not classified_updates:
        print("No classified updates matched the current filters.", file=log_file)
        sys.exit(0)

    # Sort classified updates to keep them structured
    classified_updates = sorted(classified_updates, key=lambda x: x["category"])

    # Filter out announcements with unverified sources for PR generation
    verified_updates = []
    blocked_updates_count = 0
    for u in classified_updates:
        if not enforce_strict_source_trust_hierarchy(u, classified_updates):
            blocked_updates_count += 1
        else:
            verified_updates.append(u)

    print(f"Monitored and classified {len(classified_updates)} policy/requirement updates ({blocked_updates_count} blocked due to source trust validation):", file=log_file)
    for idx, u in enumerate(classified_updates, 1):
        priority, is_verified = classify_source_and_verify(u)
        status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
        print(f" {idx}. [{u['category']}] {u['title']} - {status_str}", file=log_file)

    # 3. Scan the codebase for signals related to these categories
    print(f"Scanning codebase under '{args.dir}' for standards integration signals...", file=log_file)
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.", file=log_file)

    # 4. Write/Update documentation
    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, scan_results, args.output_docs)
    print(f"Standards documentation updated successfully at: {args.output_docs}", file=log_file)

    # 5. Generate Pull Request draft using verified updates
    pr_draft = generate_pull_request_draft(verified_updates, scan_results)

    # Save drafted PR
    os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
    try:
        with open(args.pr_output, "w", encoding="utf-8") as f:
            f.write(pr_draft)
        print(f"PR draft written successfully to: {args.pr_output}", file=log_file)
    except Exception as e:
        print(f"Failed to write PR draft to {args.pr_output}: {e}", file=sys.stderr)

    # 6. JSON output format verification if requested
    if args.json:
        report_data = []
        for u in classified_updates:
            priority, is_verified = classify_source_and_verify(u)
            cat = u["category"]
            report_data.append({
                "track": cat,
                "title": u["title"],
                "pubDate": u["pubDate"],
                "link": u["link"],
                "priority": priority,
                "verified": is_verified,
                "matches": scan_results.get(cat, [])
            })
        print(json.dumps(report_data, indent=2))


if __name__ == "__main__":
    main()
