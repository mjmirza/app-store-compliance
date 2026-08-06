#!/usr/bin/env python3
"""
Technical Standards Compliance Requirements Monitoring Utility.
Tracks 10 key technical standards and maps repo-impact, gaps, and tasks.
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
    "CIS Benchmarks"
]

# Keywords used to classify incoming policy announcements/articles into the 10 categories
CATEGORY_KEYWORDS = {
    "ISO 27001": ["iso 27001", "iso27001", "information security management", "isms", "annex a"],
    "ISO 27701": ["iso 27701", "iso27701", "privacy information management", "pims", "privacy information"],
    "ISO 42001": ["iso 42001", "iso42001", "artificial intelligence management", "aims", "ai trustworthiness"],
    "ISO 31000": ["iso 31000", "iso31000", "risk management", "risk identification", "risk treatment"],
    "ISO 9001": ["iso 9001", "iso9001", "quality management", "qms", "quality policy"],
    "IEC standards": ["iec standards", "iec 62304", "iec 82304", "iec 60601", "medical device software"],
    "OWASP": ["owasp", "masvs", "asvs", "top 10", "owasp top ten"],
    "NIST AI RMF": ["nist ai rmf", "ai risk management framework", "trustworthy ai", "ai threat modeling"],
    "NIST CSF": ["nist csf", "cybersecurity framework", "identify protect detect respond recover", "nist framework"],
    "CIS Benchmarks": ["cis benchmarks", "center for internet security", "hardening guidelines", "cis control"]
}

# Codebase signals (regex patterns) to find files affected by each of the 10 categories
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"iso[- ]?27001",
        r"isms",
        r"information[- ]security[- ]policy",
        r"access[- ]control[- ]policy"
    ],
    "ISO 27701": [
        r"iso[- ]?27701",
        r"pims",
        r"privacy[- ]by[- ]design",
        r"pii[- ]processor"
    ],
    "ISO 42001": [
        r"iso[- ]?42001",
        r"aims",
        r"ai[- ]risk[- ]assessment",
        r"ai[- ]system[- ]logging"
    ],
    "ISO 31000": [
        r"iso[- ]?31000",
        r"risk[- ]register",
        r"risk[- ]assessment",
        r"risk[- ]treatment"
    ],
    "ISO 9001": [
        r"iso[- ]?9001",
        r"qms",
        r"quality[- ]manual",
        r"corrective[- ]action"
    ],
    "IEC standards": [
        r"iec[- ]?62304",
        r"iec[- ]?82304",
        r"iec[- ]?60601",
        r"medical[- ]device[- ]software"
    ],
    "OWASP": [
        r"owasp",
        r"masvs",
        r"asvs",
        r"top[- ]?10",
        r"injection[- ]protection"
    ],
    "NIST AI RMF": [
        r"nist[- ]ai[- ]rmf",
        r"trustworthy[- ]ai",
        r"ai[- ]threat[- ]modeling",
        r"ai[- ]bias"
    ],
    "NIST CSF": [
        r"nist[- ]csf",
        r"cybersecurity[- ]framework",
        r"incident[- ]response",
        r"access[- ]control"
    ],
    "CIS Benchmarks": [
        r"cis[- ]benchmarks",
        r"hardening[- ]guidelines",
        r"secure[- ]configuration",
        r"cis[- ]control"
    ]
}

# Source trust domains and keywords for verification
TRUST_HIERARCHY = {
    "Priority 1": "Official sources (ISO, IEC, NIST, CISA, FTC, European Commission, BSI, Government publications)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers and reputable bodies (OWASP, CISecurity)",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries"
}

# Comprehensive Mock Announcements for all 10 categories
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO 27001 Information Security Management Systems Standard Revision",
        "description": "ISO releases updated Annex A control definitions for ISO 27001, streamlining physical security controls, access control protocols, and network segmentations.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 PDT"
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO 27701 Privacy Information Management System Requirements Clarified",
        "description": "New ISO 27701 implementation guidelines specify direct requirements for PII controllers and processors, detailing data subject rights interfaces and localized processing bounds.",
        "link": "https://www.iso.org/standard/27701",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 PDT"
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO 42001 Artificial Intelligence Management System Standard Ratified",
        "description": "ISO 42001 defines mandatory AI system trustworthiness parameters, requiring documented AI threat modeling, bias mitigation, and systemic logging of AI outputs.",
        "link": "https://www.iso.org/standard/42001",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 PDT"
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management Framework Application Guidelines",
        "description": "Updated risk criteria under ISO 31000 emphasize continuous threat registers and active risk treatment models to address systemic supply chain vulnerabilities.",
        "link": "https://www.iso.org/standard/31000",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 PDT"
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System Continuous Audit Revision",
        "description": "ISO 9001 updates corrective action and documentation requirements, ensuring quality policy metrics are programmatically validated across all deployment pipelines.",
        "link": "https://www.iso.org/standard/9001",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 PDT"
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62304 Medical Device Software Lifecycle Requirements Update",
        "description": "IEC releases revisions to software lifecycle and validation requirements for medical device software (IEC 62304 and IEC 82304), emphasizing safety class boundaries and strict regression audits.",
        "link": "https://www.iec.ch/standard/62304",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 PDT"
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP Mobile Application Security Verification Standard (MASVS) Release",
        "description": "OWASP publishes the new MASVS framework, detailing modernized verification rules for secure local storage, cryptographic enclaves, and anti-tampering heuristics.",
        "link": "https://mas.owasp.org/MASVS",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 PDT"
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework Implementation Playbook",
        "description": "NIST publishes updated playbooks for the AI Risk Management Framework, prescribing precise risk-assessment methodologies and transparency requirements for generative models.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 PDT"
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework (CSF) Core Revisions",
        "description": "NIST updates the CSF core categories (Identify, Protect, Detect, Respond, Recover), highlighting automated supply chain risk tracking and incident response playbook alignment.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 PDT"
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks Secure Operating System and Container Hardening Rules",
        "description": "The Center for Internet Security (CIS) updates standard hardening rules, outlining critical baseline configurations for secure container builds and deployment instances.",
        "link": "https://www.cisecurity.org/benchmark",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 PDT"
    },
    # Unverified announcement to test blocking
    {
        "id": "STD-MOCK-UNVERIFIED-BLOG",
        "category": "ISO 27001",
        "title": "Unverified Blog Post on ISO 27001 Changes",
        "description": "A personal blog post claiming ISO 27001 Annex A controls are completely changing next week with zero evidence or official references.",
        "link": "https://randomblogsite.com/iso27001-rumors",
        "pubDate": "Thu, 25 Jun 2026 20:00:00 PDT"
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
        "iso.org", "iec.ch", "nist.gov", "cisa.gov", "ftc.gov", "europa.eu",
        "eur-lex.europa.eu", "enisa.europa.eu", "edpb.europa.eu", "ico.org.uk",
        "gov.uk", "gov.sg", "bsi.bund.de"
    ]
    p1_keywords = [
        "international organization for standardization", "international electrotechnical commission",
        "national institute of standards", "cybersecurity and infrastructure security",
        "european commission", "eur-lex", "official journal", "enisa", "edpb",
        "ftc", "nist", "cisa", "ico", "government publication"
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com", "owasp.org", "mas.owasp.org", "cisecurity.org"]
    p3_keywords = ["academic paper", "academic study", "university research", "peer-reviewed", "owasp", "masvs", "cis benchmarks"]

    p4_domains = ["techcrunch.com", "wired.com", "medium.com", "blog", "randomblogsite.com"]
    p4_keywords = ["industry blog", "tech blog", "blog post", "editorial"]

    p5_domains = ["twitter.com", "x.com", "linkedin.com", "reddit.com", "t.co"]
    p5_keywords = ["tweet", "twitter", "linkedin", "reddit", "ai summary", "ai-generated summary", "chatgpt summary"]

    priority = 4  # Default to 4

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
                    common_terms = {"standard", "iso", "iec", "nist", "owasp", "cybersecurity", "risk"}
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def scan_codebase_for_standards_signals(start_dir="."):
    """
    Scans the codebase for files containing signals related to each of the 10 standards categories.
    Excludes typical build, dependency, and test directories.
    """
    matches = {cat: [] for cat in CATEGORIES}
    exclude_dirs = {
        "node_modules", "Pods", ".git", "build", "DerivedData", "vendor",
        ".dart_tool", "Carthage", "androidTest", "__tests__", "dist"
    }

    # Compile the signal patterns
    compiled_signals = {
        cat: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        for cat, patterns in CATEGORY_SIGNALS.items()
    }

    for root, dirs, files in os.walk(start_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.endswith("Tests")]

        for file in files:
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
                                    break
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
    Classifies incoming announcements into the 10 standards categories.
    """
    classified_updates = []

    for ann in announcements:
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
    """
    Generates a draft of a pull request complying with the exact 15 required sections.
    """
    citations_list = []
    affected_files_set = set()
    migration_steps = []
    impl_checklist = []
    risk_assessment = []

    for idx, u in enumerate(updates, 1):
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
        citations_list.append(
            f"- **{cat}**: [{u['title']}]({u['link']}) (Published: {u['pubDate']}, Source: {status_str})"
        )

        files = scan_results.get(cat, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        if cat == "ISO 27001":
            migration_steps.append(
                f"- **{cat}**: Align access control mechanisms and local database segmentation with Annex A control updates."
            )
            impl_checklist.append("- [ ] Verify that all user credentials and sessions are governed by active access control parameters.")
            risk_assessment.append(f"- *{cat}*: Non-conformity regarding data containment and un-segregated local asset classes.")
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Audit privacy information handling; deploy user-facing PII management views and consent records."
            )
            impl_checklist.append("- [ ] Establish dedicated consent log states for all stored PII attributes.")
            risk_assessment.append(f"- *{cat}*: Failure of PII tracking transparency, which conflicts directly with modern regulatory mandates.")
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Implement dedicated AI risk registers and systematic logging for artificial intelligence outputs."
            )
            impl_checklist.append("- [ ] Establish systematic logging structures for all downstream generative model completions.")
            risk_assessment.append(f"- *{cat}*: Potential deployment of untruthful or non-moderated AI model endpoints.")
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Re-evaluate risk register thresholds; align repository dependency audits with risk treatment guidelines."
            )
            impl_checklist.append("- [ ] Document and update active mitigation plans inside the repository risk registers.")
            risk_assessment.append(f"- *{cat}*: Undetected supply chain or package-level vulnerabilities impacting operational security.")
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Standardize deployment validation scripts and programmatically enforce corrective actions in the CI pipeline."
            )
            impl_checklist.append("- [ ] Map and verify continuous deployment regression indicators.")
            risk_assessment.append(f"- *{cat}*: Undocumented code changes or build regressions affecting product quality baselines.")
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Establish software lifecycle boundaries under IEC 62304; verify safety-critical modules operate in isolation."
            )
            impl_checklist.append("- [ ] Perform safety class separation walkthroughs for health/medical telemetry integrations.")
            risk_assessment.append(f"- *{cat}*: Software failures in critical domains, triggering immediate compliance blocks.")
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Align mobile endpoints with OWASP MASVS local storage encryption and anti-tampering baseline expectations."
            )
            impl_checklist.append("- [ ] Audit key storage enclaves and verify certificates pin Subject Public Key Info (SPKI).")
            risk_assessment.append(f"- *{cat}*: High vulnerability to runtime instrumentation, reverse engineering, and proxy interceptions.")
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Conduct robust AI threat modeling, mapping safety guardrails to NIST Trustworthy AI classifications."
            )
            impl_checklist.append("- [ ] Build comprehensive input and output moderation filters for integrated AI modules.")
            risk_assessment.append(f"- *{cat}*: System exploits via prompt injection or data poisoning on exposed AI modules.")
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Establish documented incident response playbooks and automate credential rotation schedules."
            )
            impl_checklist.append("- [ ] Deploy automated secrets tracking tools on the repository CI gates.")
            risk_assessment.append(f"- *{cat}*: Increased dwell time during active network intrusions or credential compromises.")
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Hardening server-side deployment files and verify container image builds follow secure baseline rules."
            )
            impl_checklist.append("- [ ] Perform static container scan tests to remove unused packages and privileged access flags.")
            risk_assessment.append(f"- *{cat}*: Container escape or server intrusion due to weak default operating system parameters.")

    citations_str = "\n".join(citations_list) if citations_list else "- *No updates cited.*"

    if affected_files_set:
        affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set)))
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- *No migration steps identified.*"
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- [ ] Verify target file paths conform to secure design standards."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- *Low identified risk.*"

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request introduces configuration updates and implementation pathways to bring the application into full compliance with updated technical standards, specifically targeting ISO family standards, IEC rules, OWASP, NIST, and CIS Benchmarks.

## 2. Background
Compliance with technical and organizational standards guarantees repository reliability, information security, and product quality. This change ensures our codebase aligns with updated security-by-design frameworks and platform expectations.

## 3. Regulatory change
- **Security & Privacy Frameworks**: Standardizing data controls and privacy protections under ISO 27001/27701/42001 and NIST CSF/AI RMF.
- **Mobile Security & Reliability**: Solidifying secure local storage, key attestation, and component isolation following OWASP MASVS and IEC standards.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: Compliance gaps remain medium risk if active policy validations are not statically analyzed on every build.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All technical standards updates maintain full backward compatibility. Structural modifications only add monitoring, validation, or secure fallback layers.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run the repository-wide automated validation tools.

## 10. Testing checklist
- [ ] Verify that all localized files containing standards keywords pass static validation.
- [ ] Ensure secure local storage layers mount successfully.
- [ ] Validate container file outputs for appropriate security baseline settings.

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with the completed actions.
- [ ] Ensure that internal audit trails reference these completed standards benchmarks.

## 12. Compliance impact
- **Enterprise Alignment**: Establishes readiness for ISO audits and external penetration tests.
- **Security Posture**: Lowers threat vulnerability profile significantly under OWASP and CIS baselines.

## 13. Breaking changes
- No breaking changes are introduced. Advanced security policies execute fallback loops gracefully on older platforms.

## 14. Review checklist
- [ ] Confirm that the diff is entirely emoji-free.
- [ ] Confirm that all cited standardized sources are correct.
- [ ] Ensure that sensitive credentials are isolated from plain text files.

## 15. Approver recommendations
Verify that the updated encryption and logging frameworks have been reviewed by the security team. Ensure that safety-critical modules under IEC standards have dedicated test isolation suites in the CI loop.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """
    Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md.
    """
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Policy Migration & Compliance Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track technical standards.",
        "",
        "## Monitored Standards Update Log",
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

    lines.append("## Automated Migration Recommendations & Implementation Tasks")
    lines.append("")

    for u in updates:
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        if priority in (4, 5) and not is_verified:
            lines.append(f"### Tasks for {cat} (BLOCKED: Announcement source is unverified)")
            lines.append("- **Compliance Status**: Suspended. Source is an unverified secondary source.")
            lines.append("")
            continue

        lines.append(f"### Tasks for {cat}")
        lines.append("- **Compliance Impact**: High priority standards alignment.")

        if cat == "ISO 27001":
            lines.append("- [ ] **Task 1**: Update access controls and local database encryption patterns.")
            lines.append("- [ ] **Task 2**: Establish segmented logging folders inside deployment units.")
        elif cat == "ISO 27701":
            lines.append("- [ ] **Task 1**: Deploy dynamic consent recorders for user personal attributes.")
        elif cat == "ISO 42001":
            lines.append("- [ ] **Task 1**: Implement comprehensive AI threat modeling and systematic output logs.")
        elif cat == "ISO 31000":
            lines.append("- [ ] **Task 1**: Align active package-dependency scans with internal risk registries.")
        elif cat == "ISO 9001":
            lines.append("- [ ] **Task 1**: Build automated corrective regression tests inside build checks.")
        elif cat == "IEC standards":
            lines.append("- [ ] **Task 1**: Formulate safe class separation rules for medical telemetry variables.")
        elif cat == "OWASP":
            lines.append("- [ ] **Task 1**: Align storage routines with OWASP MASVS local database recommendations.")
            lines.append("- [ ] **Task 2**: Populate certificate pin records inside network_security_config.xml.")
        elif cat == "NIST AI RMF":
            lines.append("- [ ] **Task 1**: Configure input validation and output filters for integrated model pipelines.")
        elif cat == "NIST CSF":
            lines.append("- [ ] **Task 1**: Formalize automated secrets tracking within CI build checks.")
        elif cat == "CIS Benchmarks":
            lines.append("- [ ] **Task 1**: Deploy secure configuration scanners inside container environment targets.")
        else:
            lines.append(f"- [ ] **Task**: Verify that all platform criteria for {cat} are checked and handled.")
        lines.append("")

    lines.append("<!-- STANDARDS_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"Standards documentation report updated successfully at: {output_filepath}")
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor all Technical Standards Compliance"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live technical standards feeds"
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

    announcements = []

    if args.live:
        print("Fetching live technical standards feeds...")
        announcements.extend(parse_rss_feed("https://www.iso.org/contents/feeds/standards.rss"))
        announcements.extend(parse_rss_feed("https://www.nist.gov/news-events/cybersecurity-rss-feed"))

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

    keywords_filter = (
        [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    )
    classified_updates = classify_announcements(announcements, keywords_filter)

    if not classified_updates:
        print("No classified updates matched the current filters.")
        sys.exit(0)

    classified_updates = sorted(classified_updates, key=lambda x: x["category"])

    verified_updates = []
    blocked_updates_count = 0
    for u in classified_updates:
        priority, is_verified = classify_source_and_verify(u)
        if priority in (4, 5) and not is_verified:
            blocked_updates_count += 1
        else:
            verified_updates.append(u)

    print(f"Monitored and classified {len(classified_updates)} technical standards updates ({blocked_updates_count} blocked due to source trust validation):")
    for idx, u in enumerate(classified_updates, 1):
        priority, is_verified = classify_source_and_verify(u)
        status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
        print(f" {idx}. [{u['category']}] {u['title']} - {status_str}")

    print(f"Scanning codebase under '{args.dir}' for standards integration signals...")
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, args.output_docs)

    os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
    pr_draft = generate_pull_request_draft(verified_updates, scan_results)

    try:
        with open(args.pr_output, "w", encoding="utf-8") as f:
            f.write(pr_draft)
        print(f"PR draft written successfully to: {args.pr_output}")
    except Exception as e:
        print(f"Failed to write PR draft to {args.pr_output}: {e}", file=sys.stderr)

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
