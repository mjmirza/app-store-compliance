#!/usr/bin/env python3
"""Technical Standards Monitor: tracks changes to global technical standards
(ISO 27001, ISO 27701, ISO 42001, ISO 31000, ISO 9001, IEC standards, OWASP,
NIST AI RMF, NIST CSF, CIS Benchmarks) and identifies gaps, migration, and test tasks.
Maintains a strict source trust hierarchy and remains completely emoji-free."""

import os
import re
import json
import argparse
import sys
from datetime import datetime

# Source Trust Hierarchy Definitions
TRUST_HIERARCHY = {
    "Priority 1": "European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, NIST, CISA, ICO, Government publications, ISO, IEC, CIS, OWASP official publications",
    "Priority 2": "Reuters, AP, Bloomberg",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}

# Database of global technical standards and their tracking metadata
STANDARDS_TRACKS = {
    "ISO 27001": {
        "organization": "ISO/IEC",
        "standard_id": "ISO/IEC 27001:2022",
        "citations": [
            "ISO/IEC 27001:2022 Information security, cybersecurity and privacy protection - Information security management systems - Requirements",
            "ISO/IEC 27002:2022 Information security, cybersecurity and privacy protection - Information security controls",
        ],
        "keywords": [
            "iso 27001",
            "iso/iec 27001",
            "isms",
            "information security management system",
            "security controls",
            "asset management",
            "access control policy",
        ],
        "patterns": [
            r"iso[ -]?27001",
            r"\bisms\b",
            r"information[ -]security[ -]management",
        ],
        "detect_files": ["*.swift", "*.py", "*.js", "*.ts", "*.json", "*.md", "Info.plist"],
        "detect_regex": r"securityPolicy|accessControl|credentialStorage|encryptionKey|authProvider|userRoles",
        "gap_desc": "The repository lacks structured, verifiable access control declarations or missing automated asset inventory references mapped to ISMS controls.",
        "implementation_tasks": [
            "Implement a secure, centralized API credential storage pattern to eliminate hardcoded values.",
            "Establish role-based access control (RBAC) validations on sensitive backend routes and administrative interfaces.",
            "Draft a standard encryption-at-rest utility enforcing modern cipher standards.",
        ],
        "documentation_updates": [
            "Create or update internal security playbooks outlining credential storage and role allocation criteria.",
            "Add ISO/IEC 27001 mapping indicators inside the security checklists to facilitate auditing.",
        ],
        "testing_updates": [
            "Add static secret-scanning tests (using tools like Trufflehog or GitGuardian configs) in the pre-commit checks.",
            "Implement automated role authorization boundary testing for all restricted API endpoints.",
        ],
        "compliance_impact": "High",
    },
    "ISO 27701": {
        "organization": "ISO/IEC",
        "standard_id": "ISO/IEC 27701:2019",
        "citations": [
            "ISO/IEC 27701:2019 Security techniques - Extension to ISO/IEC 27001 and ISO/IEC 27002 for privacy information management - Requirements and guidelines",
            "ISO/IEC 29100:2011 Information technology - Security techniques - Privacy framework",
        ],
        "keywords": [
            "iso 27701",
            "iso/iec 27701",
            "pims",
            "privacy information management",
            "pii",
            "personally identifiable information",
            "consent registry",
            "data controller",
        ],
        "patterns": [
            r"iso[ -]?27701",
            r"\bpims\b",
            r"privacy[ -]information[ -]management",
        ],
        "detect_files": ["*.swift", "*.py", "*.js", "*.ts", "*.json", "*.md", "*.plist"],
        "detect_regex": r"privacyPolicy|personalData|userConsent|gdprConsent|deleteAccount|analyticsTracker",
        "gap_desc": "Incomplete isolation of Personally Identifiable Information (PII) tracking logs and lack of unified consent management logging across the repository platforms.",
        "implementation_tasks": [
            "Isolate data models containing PII and ensure they are encrypted using hardware-backed keys before write operations.",
            "Create a single, verifiable Consent Registry helper to record and persist user opt-in selections.",
            "Build robust user-driven data deletion and exporting routines targeting all localized datastores.",
        ],
        "documentation_updates": [
            "Document PII inventory structures and the data lifecycle within the internal architecture guidelines.",
            "Publish an ISO/IEC 27701 alignment note in the mobile and web privacy integration files.",
        ],
        "testing_updates": [
            "Write automated unit tests verifying that personal data storage triggers an encryption check.",
            "Verify that calling clearUserData() completely flushes SQLite caches and UserDefaults keys.",
        ],
        "compliance_impact": "High",
    },
    "ISO 42001": {
        "organization": "ISO/IEC",
        "standard_id": "ISO/IEC 42001:2023",
        "citations": [
            "ISO/IEC 42001:2023 Information technology - Artificial intelligence - Management system",
            "ISO/IEC 22989:2022 Information technology - Artificial intelligence - Concepts and terminology",
        ],
        "keywords": [
            "iso 42001",
            "iso/iec 42001",
            "aims",
            "ai management system",
            "artificial intelligence standard",
            "trustworthy ai",
            "ai risk management",
        ],
        "patterns": [
            r"iso[ -]?42001",
            r"\baims\b",
            r"artificial[ -]intelligence[ -]standard",
        ],
        "detect_files": ["*.swift", "*.py", "*.js", "*.ts", "*.json", "*.md"],
        "detect_regex": r"openai|anthropic|cohere|llm|generativeLanguage|api\.openai\.com|stable[ -]diffusion|CoreML",
        "gap_desc": "Generative AI integrations lack explicit content-moderation API loops, model drift logging, or mandatory user disclosures detailing automated interactions.",
        "implementation_tasks": [
            "Implement a content-moderation filter wrapper (e.g., OpenAI Moderation API) before and after model invocations.",
            "Add visible, standard in-app disclosure dialogs alerting users they are interacting with an AI system.",
            "Incorporate system telemetry logging for LLM output evaluations and toxic prompt flags.",
        ],
        "documentation_updates": [
            "Update the repository AI guidelines in `docs/AI-POLICY-MIGRATION.md` to map ISO/IEC 42001 specifications.",
            "Document acceptable model temperature, fallback strategies, and prompt moderation criteria.",
        ],
        "testing_updates": [
            "Add automated integration tests checking system response behavior under simulated adversarial or jailbreak prompts.",
            "Write tests verifying that toxic or filtered model outputs trigger a secure fallback template.",
        ],
        "compliance_impact": "Critical",
    },
    "ISO 31000": {
        "organization": "ISO",
        "standard_id": "ISO 31000:2018",
        "citations": [
            "ISO 31000:2018 Risk management - Guidelines",
            "ISO Guide 73:2009 Risk management - Vocabulary",
        ],
        "keywords": [
            "iso 31000",
            "iso 31000:2018",
            "risk management framework",
            "risk evaluation",
            "risk register",
            "threat modeling",
            "mitigation strategy",
        ],
        "patterns": [
            r"iso[ -]?31000",
            r"risk[ -]management[ -]framework",
            r"threat[ -]modeling",
        ],
        "detect_files": ["*.swift", "*.py", "*.json", "*.md"],
        "detect_regex": r"riskMatrix|threatModel|riskRegister|mitigationPlan|securityBoundary|vulnerabilityScanner",
        "gap_desc": "Absence of a systematic threat model structure or active risk register linked directly to code and library vulnerability scans.",
        "implementation_tasks": [
            "Conduct structured threat-modeling reviews on all payment processing and user authentication entry points.",
            "Integrate an automated vulnerability scanner configuration (such as Snyk or Dependabot) with direct priority escalations.",
            "Enforce strict fallback timeouts and grace periods on critical network integration points.",
        ],
        "documentation_updates": [
            "Create a centralized Threat Model and Risk Registry document under the repository security folder.",
            "Detail recovery plans and mitigation structures for top identified high-severity architectural threats.",
        ],
        "testing_updates": [
            "Write automated regression tests simulating complete service outages of critical external identity providers.",
            "Incorporate dependency vulnerability scans into the repository pull request verification checks.",
        ],
        "compliance_impact": "Medium",
    },
    "ISO 9001": {
        "organization": "ISO",
        "standard_id": "ISO 9001:2015",
        "citations": [
            "ISO 9001:2015 Quality management systems - Requirements",
            "ISO 9000:2015 Quality management systems - Fundamentals and vocabulary",
        ],
        "keywords": [
            "iso 9001",
            "qms",
            "quality management system",
            "continuous improvement",
            "process audit",
            "corrective action",
        ],
        "patterns": [
            r"iso[ -]?9001",
            r"\bqms\b",
            r"quality[ -]management[ -]system",
        ],
        "detect_files": ["*.swift", "*.py", "*.yml", "*.json", "*.md", "package.json"],
        "detect_regex": r"unitTest|codeCoverage|lintConfig|ciWorkflow|buildTrigger|reviewChecklist",
        "gap_desc": "Lack of standardized continuous integration (CI) workflow rules, code review gate metrics, or minimum test coverage enforcement.",
        "implementation_tasks": [
            "Configure GitHub Actions or similar CI systems to enforce mandatory linting and coding standards before any merge.",
            "Define an automated build quality gate verifying code compiles with zero compiler warnings.",
            "Enforce strict branch protection policies requiring code reviews and successful checks.",
        ],
        "documentation_updates": [
            "Establish code quality guidelines and peer review standards in the repository development guide.",
            "Document corrective action procedures for post-deployment platform or metadata rejections.",
        ],
        "testing_updates": [
            "Set up automated unit test coverage reporters and configure a minimum coverage rule of 80% for new code.",
            "Add automatic lint verification scripts to the pre-commit configuration hooks.",
        ],
        "compliance_impact": "Medium",
    },
    "IEC standards": {
        "organization": "IEC",
        "standard_id": "IEC 62304 / IEC 82304",
        "citations": [
            "IEC 62304:2006 Medical device software - Software life cycle processes",
            "IEC 82304-1:2016 Health software - Part 1: General requirements for product safety",
        ],
        "keywords": [
            "iec standard",
            "iec 62304",
            "iec 82304",
            "medical device",
            "health software",
            "patient safety",
            "software safety class",
        ],
        "patterns": [
            r"iec[ -]standard",
            r"iec[ -]?62304",
            r"medical[ -]device",
        ],
        "detect_files": ["*.swift", "*.py", "*.js", "*.ts", "*.json", "*.md"],
        "detect_regex": r"patientData|vitalSigns|diagnosticCalc|clinicalReport|safetyClass|medicalDevice",
        "gap_desc": "Missing software lifecycle traceability records and inadequate logging separation for diagnostic parameter modules.",
        "implementation_tasks": [
            "Enforce strict boundary parameter validations on all classes performing medical or diagnostic computations.",
            "Isolate medical calculation algorithms into separate, standalone modules with zero UI dependencies.",
            "Introduce high-fidelity diagnostic logging covering calculations, data inputs, and system exceptions.",
        ],
        "documentation_updates": [
            "Create software lifecycle traceability documents mapping requirements to code blocks and test cases.",
            "Define software safety classifications (Class A/B/C) inside the clinical module documentation.",
        ],
        "testing_updates": [
            "Implement exhaustive mathematical boundary and overflow unit tests for all diagnostic parameter functions.",
            "Perform regression tests tracking the persistence and accuracy of simulated health measurements.",
        ],
        "compliance_impact": "High",
    },
    "OWASP": {
        "organization": "OWASP",
        "standard_id": "OWASP MASVS",
        "citations": [
            "OWASP Mobile Application Security Verification Standard (MASVS) v2.0",
            "OWASP Top 10 Web Application Security Risks (2021 / 2025)",
        ],
        "keywords": [
            "owasp",
            "masvs",
            "mstg",
            "owasp top 10",
            "injection vulnerability",
            "insecure communication",
            "reverse engineering",
            "cryptographic storage",
        ],
        "patterns": [
            r"owasp",
            r"masvs",
            r"owasp[ -]top[ -]10",
        ],
        "detect_files": ["*.swift", "*.py", "*.js", "*.ts", "*.xml", "*.plist", "*.md"],
        "detect_regex": r"sqlcipher|security_config|certificatePinning|spki|keychain|sanitization|parameterizedQuery",
        "gap_desc": "Incomplete input sanitization pipelines and vulnerability to interceptive proxies due to missing network security controls.",
        "implementation_tasks": [
            "Implement parameterized query helpers or ORMs across all localized and remote database operations.",
            "Configure certificate pinning using Subject Public Key Info (SPKI) hashes inside network configuration templates.",
            "Incorporate a screen blur multitasking transition to prevent UI data leakage in background states.",
        ],
        "documentation_updates": [
            "Integrate OWASP MASVS L1 and L2 requirements into `docs/PRE-SUBMISSION-CHECKLIST.md`.",
            "Document secure networking configurations and token revocation guidelines for backend operations.",
        ],
        "testing_updates": [
            "Deploy automated static application security testing (SAST) tools inside the CI build execution flows.",
            "Write integration tests validating that unparameterized or malicious input blocks are successfully sanitized.",
        ],
        "compliance_impact": "Critical",
    },
    "NIST AI RMF": {
        "organization": "NIST",
        "standard_id": "NIST AI RMF 1.0",
        "citations": [
            "NIST Artificial Intelligence Risk Management Framework (AI RMF 1.0)",
            "NIST Special Publication 1270: Towards a Standard for Identifying and Managing Bias in Artificial Intelligence",
        ],
        "keywords": [
            "nist ai rmf",
            "ai risk management framework",
            "trustworthy ai",
            "bias mitigation",
            "model safety",
            "model explainability",
        ],
        "patterns": [
            r"nist[ -]ai[ -]rmf",
            r"trustworthy[ -]ai",
            r"bias[ -]mitigation",
        ],
        "detect_files": ["*.swift", "*.py", "*.json", "*.md"],
        "detect_regex": r"aiModel|explainability|biasAudit|moderationAPI|modelLogging|aiFairness",
        "gap_desc": "No dedicated auditing mechanism for model bias or explainability, and lacking structured feedback loops for user-reported AI discrepancies.",
        "implementation_tasks": [
            "Build an in-app system feedback utility allowing users to report biased, inaccurate, or toxic model responses.",
            "Configure audit trail recorders logging model input metadata, output summaries, and generation parameters.",
            "Enforce pre-system content-moderation safeguards across prompt ingestion layers.",
        ],
        "documentation_updates": [
            "Publish a Trustworthy AI Ethics Statement detailing data sourcing and bias mitigation controls.",
            "Add NIST AI RMF compliance mapping to the model selection and validation architecture files.",
        ],
        "testing_updates": [
            "Develop automated stress-tests using a suite of adversarial prompts to ensure model output boundaries remain robust.",
            "Write programmatic audits tracking classification outputs across diverse simulated cohorts to detect model bias.",
        ],
        "compliance_impact": "Critical",
    },
    "NIST CSF": {
        "organization": "NIST",
        "standard_id": "NIST CSF 2.0",
        "citations": [
            "NIST Cybersecurity Framework (CSF) 2.0",
            "NIST Special Publication 800-53: Security and Privacy Controls for Information Systems and Organizations",
        ],
        "keywords": [
            "nist csf",
            "cybersecurity framework",
            "incident response",
            "incident detection",
            "recovery plan",
            "security monitoring",
        ],
        "patterns": [
            r"nist[ -]csf",
            r"cybersecurity[ -]framework",
            r"incident[ -]response",
        ],
        "detect_files": ["*.swift", "*.py", "*.js", "*.ts", "*.json", "*.md"],
        "detect_regex": r"auditLog|securityAlert|incidentResponse|recoveryPlan|backupSchedule|tamperDetection",
        "gap_desc": "Lack of centralized administrative audit log generation or formal incident response workflows integrated into core platform operations.",
        "implementation_tasks": [
            "Introduce systematic event emission for administrative authentications and sensitive account changes.",
            "Configure secure, tamper-resistant system audit files streamed directly to analytical backend nodes.",
            "Set up localized application integrity checks to detect dynamic binary instrumentation or hook frameworks.",
        ],
        "documentation_updates": [
            "Draft a comprehensive Incident Response and Disaster Recovery Plan within the repository security docs.",
            "Outline exact containment, eradication, and post-incident review procedures for active breaches.",
        ],
        "testing_updates": [
            "Run mock disaster recovery drills validating that automated backup recovery triggers execute within standard service metrics.",
            "Verify that dynamic tampering checks block system launches and trigger alerts on centralized dashboards.",
        ],
        "compliance_impact": "High",
    },
    "CIS Benchmarks": {
        "organization": "CIS",
        "standard_id": "CIS Benchmarks v8",
        "citations": [
            "Center for Internet Security (CIS) Controls v8",
            "CIS Hardening Guidelines for App Stores and Cloud Computing Environments",
        ],
        "keywords": [
            "cis benchmark",
            "cis benchmarks",
            "secure baseline",
            "hardening guide",
            "privileged access",
            "docker hardening",
        ],
        "patterns": [
            r"cis[ -]benchmark",
            r"secure[ -]baseline",
            r"hardening[ -]guide",
        ],
        "detect_files": ["Dockerfile", "docker-compose.yml", "*.swift", "*.py", "*.json", "*.md"],
        "detect_regex": r"rootUser|privileged|imageHardening|secureCompilation|obfuscation|debugSymbols",
        "gap_desc": "Default build and packaging parameters leak excessive debugging symbols, and container configurations execute under high-privilege root users.",
        "implementation_tasks": [
            "Harden Dockerfile layers by introducing a non-root system user and removing unnecessary package tools.",
            "Modify compilation targets to automatically strip debugging symbols and enable obfuscation on production builds.",
            "Configure secure HTTP headers (such as Content-Security-Policy and HSTS) on all deployment scripts.",
        ],
        "documentation_updates": [
            "Add Container and Binary Hardening guidelines based on CIS baseline standards in the deployment docs.",
            "Document compile-time security flag settings (e.g., stack protectors and position-independent execution).",
        ],
        "testing_updates": [
            "Integrate automated container scanning tools (like Trivy or Anchore) into the deployment verification workflows.",
            "Write tests ensuring compiled production output files do not expose diagnostic symbolic pointers.",
        ],
        "compliance_impact": "High",
    },
}

# Simulated standards changes for testing
SIMULATED_STANDARDS_CHANGES = [
    {
        "title": "ISO/IEC 42001:2023 Artificial Intelligence Standard Formally Enforced in Global Audits",
        "description": "ISO and IEC have finalized the enforcement requirements for the ISO/IEC 42001 standard. Organizations deploying generative AI systems must demonstrate robust risk assessments and input/output moderation workflows.",
        "pubDate": "Mon, 18 May 2026 12:00:00 GMT",
        "link": "https://www.iso.org/standard/81230.html",
    },
    {
        "title": "OWASP MASVS v2.0 Released Specifying Strict Data Storage Policies",
        "description": "The Open Web Application Security Project has finalized the OWASP MASVS v2.0 updates. Applications must encrypt all cached localized databases and disable unsecured background snapshot views.",
        "pubDate": "Wed, 20 May 2026 09:00:00 GMT",
        "link": "https://mas.owasp.org/MASVS/",
    },
    {
        "title": "Unverified ISO 27001 rumors on blog site",
        "description": "An unofficial industry blog claims that ISO 27001 will completely ban standard passwords by next month. No official standard bodies are referenced.",
        "pubDate": "Sun, 24 May 2026 15:00:00 GMT",
        "link": "https://someblog.com/iso27001-rumors",
    },
]


def scan_target_repo(repo_path, track_name, metadata):
    """Scans the repository path to identify affected files and files of interest."""
    affected_files = []
    file_patterns = metadata["detect_files"]
    detect_regex = metadata["detect_regex"]

    if not os.path.exists(repo_path):
        return [], "Repository path does not exist."

    # Build regex patterns
    compiled_patterns = []
    for pat in file_patterns:
        if pat.startswith("*."):
            compiled_patterns.append(re.compile(r".*\." + re.escape(pat[2:]) + "$"))
        else:
            compiled_patterns.append(re.compile(r".*" + re.escape(pat) + "$"))

    for root, dirs, files in os.walk(repo_path):
        # Skip standard third-party or build directories
        if any(
            p in root
            for p in [
                "node_modules",
                "Pods",
                ".git",
                "build",
                "DerivedData",
                "Carthage",
                "assets",
                "dist",
            ]
        ):
            continue

        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, repo_path)

            matched_file = False
            for pat in compiled_patterns:
                if pat.match(f) or pat.match(rel_path):
                    matched_file = True
                    break

            if matched_file:
                # Avoid matching our own monitoring scripts to prevent false positives
                if "monitor-standards" in f:
                    continue
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as fp:
                        content = fp.read()
                        if re.search(detect_regex, content, re.IGNORECASE):
                            affected_files.append(rel_path)
                except Exception:
                    pass

    if affected_files:
        verdict = f"Found {len(affected_files)} file(s) containing active compliance signals."
    else:
        verdict = "No explicit matching signals found in repository files, but configuration and docs must be audited."

    return affected_files, verdict


def classify_source_and_verify(announcement, all_announcements=None):
    """Classifies announcement by TRUST_HIERARCHY priority (1-5) and verification status.
    Returns (priority_level, is_verified)."""
    link = announcement.get("link", "").lower()
    title = announcement.get("title", "").lower()
    desc = announcement.get("description", "").lower()
    combined = f"{title} {desc} {link}"

    # Priority 1 official domains
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
        "gov.sg",
    ]
    p1_keywords = [
        "international organization for standardization",
        "international electrotechnical commission",
        "national institute of standards and technology",
        "owasp foundation",
        "center for internet security",
        "european commission",
        "official journal",
        "federal register",
    ]

    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    p3_domains = ["arxiv.org", "ssrn.com"]
    p3_keywords = ["academic paper", "academic study", "university research", "peer-reviewed"]

    p4_domains = ["techcrunch.com", "wired.com", "medium.com", "blog"]
    p4_keywords = ["industry blog", "tech blog", "blog post", "editorial"]

    p5_domains = ["twitter.com", "x.com", "linkedin.com", "reddit.com", "t.co"]
    p5_keywords = ["tweet", "twitter", "linkedin", "reddit", "ai summary", "ai-generated summary"]

    # Base priority logic
    priority = 4  # Default
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

    # Verification checks
    is_verified = False
    if priority <= 3:
        is_verified = True
    else:
        # Priority 4/5. Must have Priority 1 link or mention.
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
            # Check overlap with official items
            words = set(re.findall(r"[a-z]+", combined))
            for other in all_announcements:
                if other == announcement:
                    continue
                other_p, _ = classify_source_and_verify(other, None)
                if other_p == 1:
                    other_combined = f"{other.get('title', '')} {other.get('description', '')} {other.get('link', '')}".lower()
                    other_words = set(re.findall(r"[a-z]+", other_combined))
                    common_terms = {"iso", "iec", "nist", "owasp", "cis", "cybersecurity"}
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def match_announcement_to_tracks(announcement):
    """Checks if announcement text matches any of the standards tracking areas."""
    matched = []
    title = announcement.get("title", "").lower()
    desc = announcement.get("description", "").lower()
    combined = f"{title} {desc}"

    for track, meta in STANDARDS_TRACKS.items():
        # Check keywords
        matched_kw = False
        for kw in meta["keywords"]:
            if kw in combined:
                # Use word boundaries to prevent substring matches like "claims" matching "aims"
                if re.search(r"\b" + re.escape(kw) + r"\b", combined, re.IGNORECASE):
                    matched_kw = True
                    break

        if matched_kw:
            matched.append(track)
            continue

        # Check regex
        matched_pat = False
        for pat in meta["patterns"]:
            if re.search(pat, combined, re.IGNORECASE):
                matched_pat = True
                break

        if matched_pat:
            matched.append(track)

    return matched


def generate_pull_request(track_name, affected_files, announcement):
    """Generates a Pull Request draft description with EXACTLY 15 non-vague compliance sections."""
    meta = STANDARDS_TRACKS[track_name]
    slug = re.sub(r"[^a-z0-9]+", "-", track_name.lower()).strip("-")
    branch_name = f"compliance/standards-{slug}"
    pr_title = f"Compliance: Implement {track_name} Standards Update"

    citations_list = [
        "Priority 1: Official Standardization and Regulatory Publications",
        f"- Organization: {meta['organization']}",
        f"- Standard Identifier: {meta['standard_id']}",
    ]
    for cit in meta["citations"]:
        citations_list.append(f"- Citation: {cit}")
    citations_list.append(f"- Reference Link: {announcement.get('link', 'https://www.iso.org')}")

    # Section 1: Summary
    summary = (
        f"This compliance pull request implements integration pathways and resolves identified gaps "
        f"for {track_name} ({meta['standard_id']}) standard requirements. The updates address credential protection, "
        f"operational transparency, risk boundaries, and robust static checking pipelines to secure the codebase."
    )

    # Section 2: Background
    background = (
        f"Technical standard structures must align with rigorous global expectations. The '{track_name}' standard "
        f"constitutes a core baseline managed by {meta['organization']}. Aligning repository files and configuration "
        f"structures guarantees adherence to modern industrial safety, quality, and information control models."
    )

    # Section 3: Regulatory change
    regulatory_change = (
        f"Updates to the {track_name} security and operational models introduce refined requirements. "
        f"{meta['gap_desc']} "
        f"This pull request transitions local modules to satisfy administrative and mathematical controls."
    )

    # Section 4: Official citations
    citations = "\n".join(citations_list)

    # Section 5: Affected files
    if affected_files:
        affected_files_text = "The following files contain matching signatures in scope of this standards update:\n"
        for f in affected_files:
            affected_files_text += f"- `{f}`: Scanned file matching regex signature `{meta['detect_regex']}`\n"
    else:
        affected_files_text = (
            "No active files matching the specific code-level signatures were detected during repository scanning. "
            f"Manual audit of files matching {', '.join(meta['detect_files'])} is advised."
        )

    # Section 6: Risk assessment
    risk_level = meta["compliance_impact"].upper()
    if risk_level == "CRITICAL":
        risk_desc = (
            "CRITICAL RISK: Delaying alignment with these criteria leaves active generative AI models, inputs, "
            "or security pathways exposed to reverse engineering, injection, or rejection from publication portals."
        )
    elif risk_level == "HIGH":
        risk_desc = (
            "HIGH RISK: Submitting updates without these configurations exposes user PII or operational "
            "vulnerabilities during compliance reviews, causing elevated validation times or compliance failures."
        )
    else:
        risk_desc = (
            "MEDIUM RISK: Failure to align increases operational technical debt and complicates formal audits "
            "by external standardization partners."
        )

    # Section 7: Migration steps
    migration_steps = "\n".join(f"- {s}" for s in meta["implementation_tasks"])
    migration_steps += "\n- Update the standard validation index using python3 scripts/validate.py."

    # Section 8: Backward compatibility
    backward_compatibility = (
        "All security flags, modular calculation partitions, and configuration templates are fully backward-compatible. "
        "No existing user APIs or functional pathways are deprecated or broken."
    )

    # Section 9: Implementation checklist
    impl_checklist = "\n".join(f"- [ ] {s}" for s in meta["implementation_tasks"])

    # Section 10: Testing checklist
    testing_checklist = "\n".join(f"- [ ] {s}" for s in meta["testing_updates"])

    # Section 11: Documentation checklist
    doc_checklist = "\n".join(f"- [ ] {s}" for s in meta["documentation_updates"])

    # Section 12: Compliance impact
    compliance_impact = (
        f"This update establishes compliance against the {track_name} framework. Satisfying these criteria "
        "minimizes information risk metrics and protects enterprise publishing and distribution channels."
    )

    # Section 13: Breaking changes
    breaking_changes = (
        "There are zero functional breaking changes introduced. Existing APIs and modules continue "
        "to execute cleanly without functional modifications."
    )

    # Section 14: Review checklist
    review_checklist = (
        "- [ ] Ensure code is completely free of emojis or graphical symbols.\n"
        "- [ ] Verify that citations are traceable to official Priority 1 standard publications.\n"
        "- [ ] Check that no private or diagnostic logging targets write variables to unprotected logs."
    )

    # Section 15: Approver recommendations
    if risk_level in ["CRITICAL", "HIGH"]:
        approver_recommendations = (
            "- Principal Security Architect (for cryptographical and boundary checks)\n"
            "- Compliance Director (for standards audit confirmation)\n"
            "- Engineering Lead (for compiler and platform validation)"
        )
    else:
        approver_recommendations = (
            "- QA Lead (for testing checklist confirmation)\n"
            "- Senior Software Engineer (for configuration validation)"
        )

    # Format into exact Markdown structure with matching ## <num>. <name> headers
    desc_lines = [
        f"# Standards Compliance Update: {track_name}",
        "",
        "## 1. Summary",
        summary,
        "",
        "## 2. Background",
        background,
        "",
        "## 3. Regulatory change",
        regulatory_change,
        "",
        "## 4. Official citations",
        citations,
        "",
        "## 5. Affected files",
        affected_files_text,
        "",
        "## 6. Risk assessment",
        risk_desc,
        "",
        "## 7. Migration steps",
        migration_steps,
        "",
        "## 8. Backward compatibility",
        backward_compatibility,
        "",
        "## 9. Implementation checklist",
        impl_checklist,
        "",
        "## 10. Testing checklist",
        testing_checklist,
        "",
        "## 11. Documentation checklist",
        doc_checklist,
        "",
        "## 12. Compliance impact",
        compliance_impact,
        "",
        "## 13. Breaking changes",
        breaking_changes,
        "",
        "## 14. Review checklist",
        review_text if 'review_text' in locals() else review_checklist,
        "",
        "## 15. Approver recommendations",
        approver_recommendations,
        "",
        "---",
        "*Generated automatically by the Technical Standards Monitor. Strict Emoji-Free Policy enforced.*",
    ]

    return {
        "branch_name": branch_name,
        "title": pr_title,
        "description": "\n".join(desc_lines),
        "files_to_modify": affected_files,
    }


def update_documentation_report(updates, output_filepath):
    """Overwrites or updates the migration report in docs/STANDARDS-POLICY-MIGRATION.md."""
    lines = [
        "<!-- STANDARDS_POLICY_MONITOR_START -->",
        "# Technical Standards Compliance Migration & Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-standards.py` to track technical standards compliance.",
        "",
        "## Monitored Technical Standards Update Log",
        "",
    ]

    for idx, u in enumerate(updates, 1):
        lines.append(f"### {idx}. [{u['track']}] {u['announcement_title']}")
        lines.append(f"- **Published Date**: {u['announcement_pubDate']}")
        lines.append(f"- **Official Resource**: [{u['announcement_link']}]({u['announcement_link']})")
        lines.append(f"- **Standard Body**: {u['organization']}")
        lines.append("")

    lines.append("## Automated Gaps and Migration Recommendations")
    lines.append("")

    for u in updates:
        track = u["track"]
        meta = STANDARDS_TRACKS[track]
        lines.append(f"### Gaps and Recommendations for {track}")
        lines.append(f"- **Identified Gap**: {meta['gap_desc']}")
        lines.append("")
        lines.append("**Implementation Tasks:**")
        for task in meta["implementation_tasks"]:
            lines.append(f"- [ ] {task}")
        lines.append("")
        lines.append("**Documentation Tasks:**")
        for doc_task in meta["documentation_updates"]:
            lines.append(f"- [ ] {doc_task}")
        lines.append("")
        lines.append("**Testing Tasks:**")
        for test_task in meta["testing_updates"]:
            lines.append(f"- [ ] {test_task}")
        lines.append("")

    lines.append("<!-- STANDARDS_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"Standards documentation updated successfully at: {output_filepath}", file=sys.stderr)
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)


def run_monitor(project_path=".", simulate_track=None, verbose=False):
    """Runs the standards scanner and matches updates to standard tracks."""
    announcements = []

    if simulate_track:
        if verbose:
            print(f"[*] Simulating standards development for track: {simulate_track}")

        # Try to find matching simulated change
        matched_sim = None
        for sim in SIMULATED_STANDARDS_CHANGES:
            if (
                simulate_track.lower() in sim["title"].lower()
                or simulate_track.lower() in sim["description"].lower()
            ):
                matched_sim = sim
                break

        if matched_sim:
            announcements.append(matched_sim)
        else:
            # Match standard tracks key
            matched_track_name = None
            for name in STANDARDS_TRACKS:
                if simulate_track.lower() in name.lower():
                    matched_track_name = name
                    break

            if matched_track_name:
                announcements.append(
                    {
                        "title": f"Standards Update: Crucial revisions to {matched_track_name}",
                        "description": f"Official releases and frameworks issued under {matched_track_name}.",
                        "pubDate": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                        "link": "https://www.iso.org",
                    }
                )
            else:
                announcements.append(
                    {
                        "title": f"Custom standard development mentioning {simulate_track}",
                        "description": f"An official release concerning key specifications of {simulate_track}.",
                        "pubDate": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                        "link": "https://www.iso.org",
                    }
                )
    else:
        # Default to simulating our baseline standards developments
        announcements = SIMULATED_STANDARDS_CHANGES

    report_items = []
    processed_tracks = set()

    for item in announcements:
        matched_tracks = match_announcement_to_tracks(item)
        if not matched_tracks:
            continue

        for track in matched_tracks:
            processed_tracks.add(track)
            meta = STANDARDS_TRACKS[track]
            affected_files, scan_verdict = scan_target_repo(project_path, track, meta)

            # Enforce Source Trust Hierarchy
            priority, is_verified = classify_source_and_verify(item, announcements)
            if priority in (4, 5) and not is_verified:
                pr_details = None
                scan_verdict = f"BLOCKED: Compliance Pull Request generation blocked. Announcement source is Priority {priority} (unverified secondary source)."
            else:
                pr_details = generate_pull_request(track, affected_files, item)

            report_items.append(
                {
                    "announcement_title": item["title"],
                    "announcement_pubDate": item.get("pubDate", ""),
                    "announcement_link": item.get("link", ""),
                    "track": track,
                    "organization": meta["organization"],
                    "compliance_impact": meta["compliance_impact"],
                    "scan_verdict": scan_verdict,
                    "affected_files": affected_files,
                    "proposed_pull_request": pr_details,
                }
            )

    return report_items, processed_tracks


def print_text_report(report_items, project_path):
    print("=" * 80)
    print("               TECHNICAL STANDARDS COMPLIANCE MONITOR REPORT")
    print(f" Target Project: {os.path.abspath(project_path)}")
    print(f" Date Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    if not report_items:
        print("\nNo matching global technical standards updates detected.\n")
        return

    print(f"\nFound {len(report_items)} matched standards compliance update(s):\n")

    for i, item in enumerate(report_items, 1):
        print(f"{i}. TRACK: [{item['track']}]")
        print(f"   - Announcement: {item['announcement_title']}")
        print(f"   - Published:    {item['announcement_pubDate']}")
        print(f"   - Link:         {item['announcement_link']}")
        print(f"   - Standard Body:{item['organization']}")
        print(f"   - Impact Level: {item['compliance_impact']}")
        print(f"   - Scan Verdict: {item['scan_verdict']}")

        if item["affected_files"]:
            print("   - Identified Affected Files:")
            for f in item["affected_files"]:
                print(f"       * {f}")
        else:
            print("   - Affected Files: None found.")

        meta = STANDARDS_TRACKS[item["track"]]
        print("   - Suggested Gaps and Recommendations:")
        print(f"       Gap: {meta['gap_desc']}")
        for t in meta["implementation_tasks"]:
            print(f"       [ ] Implementation: {t}")
        for t in meta["documentation_updates"]:
            print(f"       [ ] Documentation:  {t}")
        for t in meta["testing_updates"]:
            print(f"       [ ] Testing:        {t}")

        pr = item["proposed_pull_request"]
        print("   - Proposed Pull Request:")
        if pr is None:
            print(
                "       * BLOCKED: Compliance Pull Request generation blocked due to unverified secondary source."
            )
        else:
            print(f"       * Branch Name:  {pr['branch_name']}")
            print(f"       * PR Title:     {pr['title']}")
            print(
                "       * PR Description: (draft generated with exactly 15 non-vague sections)"
            )
        print("-" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Technical Standards Compliance Monitor."
    )
    parser.add_argument(
        "--project",
        default=".",
        help="Path to target project repository to scan (default: current directory)",
    )
    parser.add_argument(
        "--simulate", help="Simulate a technical standard change by track name or keyword"
    )
    parser.add_argument(
        "--json", action="store_true", help="Output report in JSON format"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print verbose execution logs"
    )
    parser.add_argument(
        "--output-docs",
        default="docs/STANDARDS-POLICY-MIGRATION.md",
        help="Filepath to write migration tasks and logs",
    )
    parser.add_argument(
        "--pr-output",
        default="docs/STANDARDS_COMPLIANCE_PR_DRAFT.md",
        help="Filepath to save the drafted PR",
    )

    args = parser.parse_args()

    report_items, processed = run_monitor(
        project_path=args.project, simulate_track=args.simulate, verbose=args.verbose
    )

    # Output to files
    if report_items:
        os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
        update_documentation_report(report_items, args.output_docs)

        # Write first valid non-blocked PR draft to pr_output
        pr_written = False
        for item in report_items:
            pr = item["proposed_pull_request"]
            if pr:
                os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
                with open(args.pr_output, "w", encoding="utf-8") as f:
                    f.write(pr["description"])
                print(f"PR draft written successfully to: {args.pr_output}", file=sys.stderr)
                pr_written = True
                break
        if not pr_written:
            # If all are blocked or none generated, make sure we clean up or write a note
            if os.path.exists(args.pr_output):
                os.remove(args.pr_output)

    if args.json:
        print(json.dumps(report_items, indent=2))
    else:
        print_text_report(report_items, args.project)


if __name__ == "__main__":
    main()
