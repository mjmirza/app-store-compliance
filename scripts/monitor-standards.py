#!/usr/bin/env python3
"""
Technical Standards Compliance Requirements Monitoring Utility.
Tracks changes across 10 technical standards:
- ISO 27001
- ISO 27701
- ISO 42001
- ISO 31000
- ISO 9001
- IEC standards
- OWASP
- NIST AI RMF
- NIST CSF
- CIS Benchmarks

Identifies repository gaps, generates implementation tasks, documentation updates, and testing updates.
"""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json

# The 10 tracked technical standards categories
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
    "ISO 27001": [
        "iso 27001", "iso/iec 27001", "information security management system", "isms", "annex a controls"
    ],
    "ISO 27701": [
        "iso 27701", "iso/iec 27701", "privacy information management system", "pims", "privacy information management"
    ],
    "ISO 42001": [
        "iso 42001", "iso/iec 42001", "artificial intelligence management system", "aims", "ai management system"
    ],
    "ISO 31000": [
        "iso 31000", "risk management guidelines", "iso risk management", "enterprise risk management framework"
    ],
    "ISO 9001": [
        "iso 9001", "quality management system", "qms", "quality management principles"
    ],
    "IEC standards": [
        "iec standards", "iec 62443", "iec 82304", "iec 62304", "international electrotechnical commission", "iec"
    ],
    "OWASP": [
        "owasp", "owasp top 10", "masvs", "asvs", "owasp mobile top 10", "owasp ai exchange", "owasp llm top 10"
    ],
    "NIST AI RMF": [
        "nist ai rmf", "ai risk management framework", "nist ai 100-1", "govern map measure manage", "nist ai"
    ],
    "NIST CSF": [
        "nist csf", "nist csf 2.0", "cybersecurity framework", "nist sp 800-53", "identify protect detect respond recover govern"
    ],
    "CIS Benchmarks": [
        "cis benchmarks", "center for internet security", "cis controls", "cis hardened images", "cis benchmark"
    ]
}

# Codebase signals (regex patterns) to find files affected by each category
CATEGORY_SIGNALS = {
    "ISO 27001": [
        r"ISO[ -]?27001",
        r"ISMS",
        r"security_policy",
        r"access_control",
        r"information_security"
    ],
    "ISO 27701": [
        r"ISO[ -]?27701",
        r"PIMS",
        r"privacy_policy",
        r"data_protection_officer",
        r"pii_controller"
    ],
    "ISO 42001": [
        r"ISO[ -]?42001",
        r"AIMS",
        r"ai_governance",
        r"ai_impact_assessment",
        r"model_card"
    ],
    "ISO 31000": [
        r"ISO[ -]?31000",
        r"risk_register",
        r"risk_assessment",
        r"risk_matrix",
        r"risk_treatment"
    ],
    "ISO 9001": [
        r"ISO[ -]?9001",
        r"QMS",
        r"quality_policy",
        r"audit_log",
        r"continuous_improvement"
    ],
    "IEC standards": [
        r"IEC[ -]?62443",
        r"IEC[ -]?82304",
        r"IEC[ -]?62304",
        r"IEC[ -]?standards"
    ],
    "OWASP": [
        r"OWASP",
        r"MASVS",
        r"ASVS",
        r"sanitization",
        r"csrf_token"
    ],
    "NIST AI RMF": [
        r"NIST[ -]?AI[ -]?RMF",
        r"AI_RMF",
        r"model_bias",
        r"explainability",
        r"ai_fairness"
    ],
    "NIST CSF": [
        r"NIST[ -]?CSF",
        r"SP[ -]?800-53",
        r"incident_response",
        r"disaster_recovery",
        r"threat_hunting"
    ],
    "CIS Benchmarks": [
        r"CIS[ -]?Benchmark",
        r"CIS[ -]?Controls",
        r"hardening",
        r"secure_baseline"
    ]
}

# Source trust domains and keywords for verification
TRUST_HIERARCHY = {
    "Priority 1": "Official standards bodies & government publications (ISO, IEC, NIST, CIS, OWASP, Official Journal, EUR-Lex, FTC, ENISA, EDPB, CISA, ICO)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers and peer-reviewed journals",
    "Priority 4": "Industry blogs and corporate tech blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries"
}

# Comprehensive Mock Announcements covering all 10 categories + 1 unverified blog
MOCK_ANNOUNCEMENTS = [
    {
        "id": "STD-MOCK-ISO27001",
        "category": "ISO 27001",
        "title": "ISO/IEC 27001:2022 Amendment Updates for Cloud & Technological Controls",
        "description": "ISO updates guidance for Annex A controls including mandatory threat intelligence, web filtering, and secure coding practices for enterprise information security management systems.",
        "link": "https://www.iso.org/standard/27001",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO27701",
        "category": "ISO 27701",
        "title": "ISO/IEC 27701 Guidance on Privacy Information Management in Multi-Cloud Environments",
        "description": "Standard revisions require PII processors and controllers to establish automated record-keeping of data processing activities and third-party vendor privacy risk evaluations.",
        "link": "https://www.iso.org/standard/71670.html",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO42001",
        "category": "ISO 42001",
        "title": "ISO/IEC 42001 AI Management System (AIMS) Certification Standard Enforcement",
        "description": "ISO releases detailed audit criteria for Artificial Intelligence Management Systems, mandating algorithmic impact assessments, continuous bias monitoring, and human-in-the-loop overrides.",
        "link": "https://www.iso.org/standard/81230.html",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO31000",
        "category": "ISO 31000",
        "title": "ISO 31000 Risk Management Integration for Cyber and Emerging Technology Threats",
        "description": "Updated risk management principles require organizations to integrate quantitative cyber risk quantification models into enterprise risk registers.",
        "link": "https://www.iso.org/iso-31000-risk-management.html",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 GMT"
    },
    {
        "id": "STD-MOCK-ISO9001",
        "category": "ISO 9001",
        "title": "ISO 9001 Quality Management System Climate and Supply Chain Revision",
        "description": "Revisions to ISO 9001 clause 4 mandate that organizations evaluate climate change and software supply chain security as factors relevant to organizational purpose and quality context.",
        "link": "https://www.iso.org/standard/62085.html",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 GMT"
    },
    {
        "id": "STD-MOCK-IEC",
        "category": "IEC standards",
        "title": "IEC 62443 / IEC 82304 Standards for Industrial and Software Device Security",
        "description": "IEC publishes updated security lifecycle guidelines requiring secure boot, cryptographically signed firmware, and software bill of materials (SBOM) declarations.",
        "link": "https://www.iec.ch/homepage",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 GMT"
    },
    {
        "id": "STD-MOCK-OWASP",
        "category": "OWASP",
        "title": "OWASP Top 10 for Large Language Model Applications & MASVS v2.1 Release",
        "description": "OWASP updates security guidance for LLM applications and mobile security verification standards, emphasizing prompt injection defense, output sanitization, and secure storage.",
        "link": "https://owasp.org/www-project-top-10-for-large-language-model-applications/",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 GMT"
    },
    {
        "id": "STD-MOCK-NISTAIRMF",
        "category": "NIST AI RMF",
        "title": "NIST AI Risk Management Framework 1.0 Profile Updates for Generative AI",
        "description": "NIST expands AI RMF profiles for GOVERN, MAP, MEASURE, and MANAGE functions specifically targeting generative foundation models, red-teaming, and safety alignment.",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 GMT"
    },
    {
        "id": "STD-MOCK-NISTCSF",
        "category": "NIST CSF",
        "title": "NIST Cybersecurity Framework 2.0 Implementation Guide Release",
        "description": "NIST CSF 2.0 explicitly adds the GOVERN function and expands supply chain risk management expectations for modern software application ecosystems.",
        "link": "https://www.nist.gov/cyberframework",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 GMT"
    },
    {
        "id": "STD-MOCK-CIS",
        "category": "CIS Benchmarks",
        "title": "CIS Benchmarks for Cloud, Container, and Mobile Operating Systems Update",
        "description": "Center for Internet Security updates hardening benchmarks for Docker, Kubernetes, iOS, and Android to mitigate zero-day container breakouts and credential harvesting.",
        "link": "https://www.cisecurity.org/cis-benchmarks",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 GMT"
    },
    {
        "id": "STD-MOCK-UNVERIFIED-BLOG",
        "category": "ISO 27001",
        "title": "Unverified Tech Blog Post on ISO 27001 Mandates",
        "description": "An unverified personal blog claims ISO 27001 will revoke all certifications unless organizations migrate to a proprietary blockchain vendor. This is unverified secondary chatter.",
        "link": "https://randomblogsite.com/iso-rumor",
        "pubDate": "Thu, 25 Jun 2026 20:00:00 GMT"
    }
]


def classify_source_and_verify(announcement, all_announcements=None):
    """
    Classifies an announcement by TRUST_HIERARCHY priority (1-5) and verification status.
    Returns (priority_level, is_verified).
    """
    link = announcement.get("link", "").lower()
    title = announcement.get("title", "").lower()
    desc = announcement.get("description", "").lower()
    combined = f"{title} {desc} {link}"

    p1_domains = [
        "iso.org", "iec.ch", "nist.gov", "cisecurity.org", "owasp.org",
        "europa.eu", "eur-lex.europa.eu", "enisa.europa.eu", "edpb.europa.eu",
        "ftc.gov", "cisa.gov", "ico.org.uk", "gov.uk", "gov.sg"
    ]
    p1_keywords = [
        "iso standard", "iso/iec", "nist publication", "cis benchmark", "owasp project",
        "official journal", "european commission", "enisa", "edpb", "ftc", "cisa", "ico"
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com", "ieee.org", "acm.org"]
    p3_keywords = ["academic paper", "academic study", "university research", "peer-reviewed"]

    p4_domains = ["techcrunch.com", "wired.com", "medium.com", "blog", "randomblogsite.com"]
    p4_keywords = ["industry blog", "tech blog", "blog post", "editorial"]

    p5_domains = ["twitter.com", "x.com", "linkedin.com", "reddit.com", "t.co"]
    p5_keywords = ["tweet", "twitter", "linkedin", "reddit", "ai summary", "ai-generated summary", "chatgpt summary"]

    priority = 4  # Default priority

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
        # Priority 4 or 5: Must reference a Priority 1 source
        has_p1_ref = False
        for d in p1_domains:
            if d in combined:
                has_p1_ref = True
                break
        if not has_p1_ref:
            for kw in p1_keywords:
                if kw in combined:
                    has_p1_ref = True
                    break
        if ".gov" in combined:
            has_p1_ref = True

        if has_p1_ref:
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
                    common_terms = {"iso", "nist", "owasp", "cis", "iec", "security", "framework"}
                    if words.intersection(other_words).intersection(common_terms):
                        is_verified = True
                        break

    return priority, is_verified


def scan_codebase_for_standards_signals(start_dir="."):
    """
    Scans the codebase for files containing signals related to each of the 10 technical standards categories.
    Excludes build, dependency, and test directories.
    """
    matches = {cat: [] for cat in CATEGORIES}
    exclude_dirs = {
        "node_modules", "Pods", ".git", "build", "DerivedData", "vendor",
        ".dart_tool", "Carthage", "androidTest", "__tests__", "dist"
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
                    ".kt", ".java", ".xml", ".gradle", ".kts", ".json", ".js",
                    ".ts", ".md", ".swift", ".m", ".h", ".plist", ".html", ".py", ".sh"
                )
            ):
                continue

            filepath = os.path.join(root, file)
            if "monitor-standards" in file or "standards_checker" in file:
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
            url, headers={"User-Agent": "Mozilla/5.0 (TechnicalStandardsMonitor/1.0)"}
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
    Classifies incoming announcements into the 10 technical standards categories.
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
    seen_citations = set()
    affected_files_set = set()
    migration_steps = []
    impl_checklist = []
    risk_assessment = []
    processed_categories = set()

    for idx, u in enumerate(updates, 1):
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
        cite_key = (cat, u['title'], u['link'])
        if cite_key not in seen_citations:
            seen_citations.add(cite_key)
            citations_list.append(
                f"- **{cat}**: [{u['title']}]({u['link']}) (Published: {u['pubDate']}, Source: {status_str})"
            )

        files = scan_results.get(cat, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        if cat in processed_categories:
            continue
        processed_categories.add(cat)

        if cat == "ISO 27001":
            migration_steps.append(
                f"- **{cat}**: Update Information Security Management System (ISMS) controls, threat intelligence procedures, and access control policies."
            )
            impl_checklist.append("- [ ] Audit ISMS Annex A controls against ISO 27001:2022 amendments.")
            risk_assessment.append(f"- *{cat}*: Non-conformity in ISO 27001 ISMS audits leading to certification suspension or loss of enterprise customer trust.")
        elif cat == "ISO 27701":
            migration_steps.append(
                f"- **{cat}**: Update Privacy Information Management System (PIMS) data mapping, controller/processor agreements, and third-party risk assessments."
            )
            impl_checklist.append("- [ ] Update PIMS documentation and data processing activity records for ISO 27701.")
            risk_assessment.append(f"- *{cat}*: Exposure to regulatory privacy fines under GDPR/CCPA due to missing PIMS record-keeping.")
        elif cat == "ISO 42001":
            migration_steps.append(
                f"- **{cat}**: Establish Artificial Intelligence Management System (AIMS) governance, algorithmic impact assessments, and human oversight controls."
            )
            impl_checklist.append("- [ ] Implement ISO 42001 AIMS risk assessment and bias monitoring workflows for AI components.")
            risk_assessment.append(f"- *{cat}*: Non-compliance with emerging AI governance standards leading to AI Act enforcement actions.")
        elif cat == "ISO 31000":
            migration_steps.append(
                f"- **{cat}**: Align cyber and technological risk registers with ISO 31000 enterprise risk management guidelines."
            )
            impl_checklist.append("- [ ] Update enterprise risk matrix and risk treatment plans in accordance with ISO 31000.")
            risk_assessment.append(f"- *{cat}*: Unmitigated systemic technology risks failing organizational risk tolerance levels.")
        elif cat == "ISO 9001":
            migration_steps.append(
                f"- **{cat}**: Integrate software supply chain security and environmental context factors into Quality Management System (QMS) processes."
            )
            impl_checklist.append("- [ ] Review QMS clause 4 contextual factors and software delivery quality gates.")
            risk_assessment.append(f"- *{cat}*: QMS audit findings and delivery defects impacting release reliability.")
        elif cat == "IEC standards":
            migration_steps.append(
                f"- **{cat}**: Enforce IEC 62443 / IEC 82304 software security lifecycle requirements, secure boot, and Software Bill of Materials (SBOM) generation."
            )
            impl_checklist.append("- [ ] Generate and publish SBOM artifacts and verify secure boot build configurations.")
            risk_assessment.append(f"- *{cat}*: Inability to meet hardware/software device security certification requirements.")
        elif cat == "OWASP":
            migration_steps.append(
                f"- **{cat}**: Align mobile application controls with OWASP MASVS v2.1 and mitigate OWASP Top 10 for LLM Applications risks."
            )
            impl_checklist.append("- [ ] Conduct OWASP MASVS audit and verify LLM input sanitization and output escaping.")
            risk_assessment.append(f"- *{cat}*: High susceptibility to prompt injection, client-side data leakage, and OWASP top vulnerabilities.")
        elif cat == "NIST AI RMF":
            migration_steps.append(
                f"- **{cat}**: Operationalize NIST AI RMF GOVERN, MAP, MEASURE, and MANAGE functions across AI model lifecycle stages."
            )
            impl_checklist.append("- [ ] Complete NIST AI RMF profile assessments and document model red-teaming results.")
            risk_assessment.append(f"- *{cat}*: Unmanaged AI safety, fairness, and hallucination risks in production AI features.")
        elif cat == "NIST CSF":
            migration_steps.append(
                f"- **{cat}**: Map incident response, threat hunting, and supply chain controls to NIST Cybersecurity Framework 2.0 GOVERN function."
            )
            impl_checklist.append("- [ ] Map security operations and governance policies to NIST CSF 2.0 subcategories.")
            risk_assessment.append(f"- *{cat}*: Gaps in organizational cybersecurity posture failing federal or partner vendor requirements.")
        elif cat == "CIS Benchmarks":
            migration_steps.append(
                f"- **{cat}**: Apply updated CIS Benchmark hardening configurations to build environments, container images, and mobile operating targets."
            )
            impl_checklist.append("- [ ] Run CIS Benchmark automated compliance scans against container and host baselines.")
            risk_assessment.append(f"- *{cat}*: Vulnerabilities in unhardened host or container environments exposing infrastructure.")

    citations_str = "\n".join(citations_list) if citations_list else "- *No updates cited.*"

    if affected_files_set:
        affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set)))
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- *No migration steps identified.*"
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- [ ] Perform generic verification of technical standards compliance."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- *Low identified risk.*"

    pr_template = f"""# PULL REQUEST DRAFT: Technical Standards Compliance Update

## 1. Summary
This pull request introduces policy, architecture, testing, and implementation updates to bring the repository into full compliance with updated technical standards, including ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP, NIST AI RMF, NIST CSF, and CIS Benchmarks.

## 2. Background
Technical standards evolve continuously to address emerging cybersecurity, privacy, AI governance, and software quality requirements. Maintaining alignment with ISO/IEC standards, NIST frameworks, OWASP guidelines, and CIS benchmarks is essential for enterprise security posture and regulatory audit readiness.

## 3. Regulatory change
- **ISO/IEC Frameworks**: ISO 27001 ISMS Annex A updates, ISO 27701 PIMS record-keeping, ISO 42001 AIMS AI governance, ISO 31000 risk management, ISO 9001 supply chain quality, and IEC 62443/82304 software security lifecycles.
- **Security & AI Guidelines**: OWASP MASVS v2.1 and LLM Top 10 defenses, NIST AI RMF 1.0 GOVERN/MAP/MEASURE/MANAGE functions, NIST CSF 2.0 governance expansion, and CIS Benchmark OS/container hardening baselines.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: Medium to High risk of audit non-conformity or security vulnerability exposure if technical standard updates are unaddressed.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes maintain backward compatibility. Security and quality controls operate transparently alongside existing build pipelines and application workflows without breaking functional APIs.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Execute automated standards compliance verification script.

## 10. Testing checklist
- [ ] Run automated security static analysis and vulnerability scans.
- [ ] Validate OWASP MASVS controls and verify LLM prompt injection defenses.
- [ ] Execute CIS Benchmark automated compliance checks on build baselines.
- [ ] Verify that audit logs and system event registers capture required security events.

## 11. Documentation checklist
- [ ] Update `docs/STANDARDS-POLICY-MIGRATION.md` with completed implementation tasks.
- [ ] Document updated risk registers and ISMS/AIMS control mappings.
- [ ] Ensure architecture diagrams reflect current security and quality boundaries.

## 12. Compliance impact
- **Audit Readiness**: Ensures seamless conformity during ISO/IEC 27001/27701/42001 external audits.
- **Cyber Posture**: Strengthens organizational defense against OWASP and NIST CSF identified threat vectors.
- **Enterprise Trust**: Satisfies enterprise vendor assessment requirements and industry benchmark expectations.

## 13. Breaking changes
- No functional API breaking changes introduced. Security hardening rules strictly enforce authentication and input validation boundaries.

## 14. Review checklist
- [ ] Code and documentation diffs are completely emoji-free.
- [ ] Official citations cite Priority 1-3 verified sources or verified Priority 4/5 references.
- [ ] Security configurations enforce principle of least privilege and zero trust baselines.

## 15. Approver recommendations
Verify that all mandatory ISMS, PIMS, and AIMS control updates are logged in internal risk registers and confirm that automated build pipeline security scans pass cleanly prior to merge.
"""
    return pr_template


SIMULATED_NOTICE = [
    "",
    "> **Simulated output, not live announcements.** This file was generated from sample",
    "> announcements (the built-in set, the default, or a file passed with `--mock`). The titles,",
    "> publish dates, and descriptions below are examples that show the shape of a migration",
    "> report, not real publications. Only the linked official documentation URLs are real.",
    "> Re-run the monitor with `--live` against real feeds before treating anything here",
    "> as an actual requirement.",
    "",
]


def update_documentation_report(updates, output_filepath, is_simulated=False):
    """
    Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md.
    Generates implementation tasks, documentation updates, and testing updates.
    """
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
    ]
    if is_simulated:
        lines.extend(SIMULATED_NOTICE)
    lines.extend([
        "# Technical Standards Policy Migration & Requirements Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track compliance across technical standards.",
        "",
        "## Monitored Technical Standards Update Log",
        "",
    ])

    for idx, u in enumerate(updates, 1):
        priority, is_verified = classify_source_and_verify(u)
        status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
        lines.append(f"### {idx}. [{u['category']}] {u['title']}")
        lines.append(f"- **Published Date**: {u['pubDate']}")
        lines.append(f"- **Official Resource**: [{u['link']}]({u['link']})")
        lines.append(f"- **Verification Status**: {status_str}")
        lines.append(f"- **Description**: {u['description']}")
        lines.append("")

    lines.append("## Automated Migration Recommendations & Actionable Tasks")
    lines.append("")

    processed_task_categories = set()
    for u in updates:
        cat = u["category"]
        priority, is_verified = classify_source_and_verify(u)
        task_key = (cat, is_verified)
        if task_key in processed_task_categories:
            continue
        processed_task_categories.add(task_key)

        if priority in (4, 5) and not is_verified:
            lines.append(f"### Tasks for {cat} (BLOCKED: Announcement source is unverified)")
            lines.append("- **Regulatory Status**: Suspended. Source is an unverified Priority 4/5 secondary source.")
            lines.append("")
            continue

        lines.append(f"### Implementation, Documentation & Testing Tasks for {cat}")
        lines.append("- **Regulatory Impact**: High priority technical standard compliance area.")

        if cat == "ISO 27001":
            lines.append("- [ ] **Implementation Task**: Update ISMS Annex A security control implementations and access control rules.")
            lines.append("- [ ] **Documentation Update**: Revise Information Security Management System (ISMS) policy manual.")
            lines.append("- [ ] **Testing Update**: Add automated tests verifying access control enforcement and audit log generation.")
        elif cat == "ISO 27701":
            lines.append("- [ ] **Implementation Task**: Implement automated PII processing activity logs and data subject request workflows.")
            lines.append("- [ ] **Documentation Update**: Update Privacy Information Management System (PIMS) manual and DPO records.")
            lines.append("- [ ] **Testing Update**: Add tests verifying PII encryption at rest and data retention purging.")
        elif cat == "ISO 42001":
            lines.append("- [ ] **Implementation Task**: Implement AI Management System (AIMS) algorithmic impact assessments and human override controls.")
            lines.append("- [ ] **Documentation Update**: Publish AI governance framework and model card documentation.")
            lines.append("- [ ] **Testing Update**: Add automated tests for AI model output validation and bias monitoring.")
        elif cat == "ISO 31000":
            lines.append("- [ ] **Implementation Task**: Integrate quantitative cyber risk metrics into risk assessment pipelines.")
            lines.append("- [ ] **Documentation Update**: Update enterprise risk register and risk matrix documentation.")
            lines.append("- [ ] **Testing Update**: Validate automated risk threshold alerting and incident escalation paths.")
        elif cat == "ISO 9001":
            lines.append("- [ ] **Implementation Task**: Add software supply chain quality gates and SBOM validation to build pipelines.")
            lines.append("- [ ] **Documentation Update**: Revise Quality Management System (QMS) release quality guidelines.")
            lines.append("- [ ] **Testing Update**: Implement continuous integration quality gate checks and defect regression tests.")
        elif cat == "IEC standards":
            lines.append("- [ ] **Implementation Task**: Implement IEC 62443 / IEC 82304 secure boot and cryptographically signed release builds.")
            lines.append("- [ ] **Documentation Update**: Document software security lifecycle processes and SBOM architecture.")
            lines.append("- [ ] **Testing Update**: Add automated firmware/binary signature verification tests.")
        elif cat == "OWASP":
            lines.append("- [ ] **Implementation Task**: Enforce OWASP MASVS mobile security controls and LLM prompt injection defenses.")
            lines.append("- [ ] **Documentation Update**: Document OWASP security checklist alignment and LLM safety guidelines.")
            lines.append("- [ ] **Testing Update**: Integrate OWASP ZAP / SAST security scanning in CI test suite.")
        elif cat == "NIST AI RMF":
            lines.append("- [ ] **Implementation Task**: Operationalize NIST AI RMF GOVERN, MAP, MEASURE, and MANAGE controls.")
            lines.append("- [ ] **Documentation Update**: Publish NIST AI RMF profile alignment document and red-teaming report.")
            lines.append("- [ ] **Testing Update**: Add unit tests for AI input filtering, output sanitization, and hallucination bounds.")
        elif cat == "NIST CSF":
            lines.append("- [ ] **Implementation Task**: Map incident response and threat hunting controls to NIST CSF 2.0 GOVERN subcategories.")
            lines.append("- [ ] **Documentation Update**: Update Incident Response Plan and Cybersecurity Framework control matrix.")
            lines.append("- [ ] **Testing Update**: Conduct simulated incident response exercises and automated log integrity tests.")
        elif cat == "CIS Benchmarks":
            lines.append("- [ ] **Implementation Task**: Apply CIS Benchmark OS, container, and mobile hardening profiles.")
            lines.append("- [ ] **Documentation Update**: Document hardening baseline configurations and security exceptions.")
            lines.append("- [ ] **Testing Update**: Run automated CIS Benchmark compliance scanning tools on build artifacts.")
        else:
            lines.append(f"- [ ] **Task**: Verify that all criteria for {cat} are checked and handled.")
        lines.append("")

    lines.append("<!-- STANDARDS_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"Technical standards documentation report updated successfully at: {output_filepath}")
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor Technical Standards Compliance Requirements (ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC, OWASP, NIST AI RMF, NIST CSF, CIS)"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live technical standards RSS/Atom feeds"
    )
    parser.add_argument(
        "--mock",
        type=str,
        default=None,
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
        default=None,
        help="Filepath to write migration tasks and report",
    )
    parser.add_argument(
        "--pr-output",
        type=str,
        default=None,
        help="Filepath to save the drafted PR",
    )
    parser.add_argument(
        "--json", action="store_true", help="Output JSON report to stdout"
    )

    args = parser.parse_args()

    announcements = []

    if args.live:
        print("Fetching live technical standards RSS feeds...")
        announcements.extend(parse_rss_feed("https://www.iso.org/rss/xnews.xml"))
        announcements.extend(parse_rss_feed("https://www.nist.gov/news-events/news/rss.xml"))
        announcements.extend(parse_rss_feed("https://owasp.org/feed.xml"))

    used_mock = False
    if args.mock or (not args.live and not args.mock) or not announcements:
        used_mock = True
        print("Data. sample announcements built into this script, not live news.")
        if args.mock and args.mock != "inline" and os.path.exists(args.mock):
            try:
                with open(args.mock, "r", encoding="utf-8") as f:
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

    classified_updates = sorted(classified_updates, key=lambda x: x["category"])

    verified_updates = []
    blocked_updates_count = 0
    for u in classified_updates:
        priority, is_verified = classify_source_and_verify(u, classified_updates)
        if priority in (4, 5) and not is_verified:
            blocked_updates_count += 1
        else:
            verified_updates.append(u)

    print(f"Monitored and classified {len(classified_updates)} technical standards updates ({blocked_updates_count} blocked due to source trust validation):")
    for idx, u in enumerate(classified_updates, 1):
        priority, is_verified = classify_source_and_verify(u, classified_updates)
        status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
        print(f" {idx}. [{u['category']}] {u['title']} - {status_str}")

    print(f"Scanning codebase under '{args.dir}' for technical standards integration signals...")
    scan_results = scan_codebase_for_standards_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    if args.output_docs:
        os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
        update_documentation_report(classified_updates, args.output_docs, is_simulated=used_mock)
    else:
        print("No file written. Pass --output-docs <path> to save this report.")

    pr_draft = generate_pull_request_draft(verified_updates, scan_results)
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

    if args.json:
        report_data = []
        for u in classified_updates:
            priority, is_verified = classify_source_and_verify(u, classified_updates)
            cat = u["category"]
            report_data.append({
                "category": cat,
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
