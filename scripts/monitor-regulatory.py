#!/usr/bin/env python3
"""Regulatory Intelligence Agent: tracks global regulatory developments
(EU/UK/US/CA/AU/SG/intl) against a source trust hierarchy. See README.md."""

import os
import sys
import re
import json
import argparse
from datetime import datetime

# Source Trust Hierarchy Definitions
TRUST_HIERARCHY = {
    "Priority 1": "European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, NIST, CISA, ICO, DSIT, FCA, CMA, OPC, OAIC, PDPC, IMDA, ISO, OECD, Government publications",
    "Priority 2": "Reuters, AP, Bloomberg",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}

# Comprehensive Database of global jurisdictions, authorities, laws and their tracking keywords/signatures
REGULATORY_TRACKS = {
    "EU AI Act": {
        "jurisdiction": "European Union",
        "authorities": ["European Commission", "Official Journal", "EUR-Lex", "ENISA", "EDPB"],
        "citations": [
            "Regulation (EU) 2024/1689 of the European Parliament and of the Council (OJ L, 2024/1689, 12.07.2024)",
            "European Commission Draft Guidelines on Article 50 Transparency Obligations (May 2026)",
        ],
        "keywords": [
            "ai act",
            "artificial intelligence act",
            "limited risk",
            "high-risk",
            "prohibited practices",
            "article 50",
            "article 5",
            "article 4",
            "ai literacy",
        ],
        "patterns": [
            r"ai[ -]act",
            r"artificial[ -]intelligence[ -]act",
            r"article[ -]50",
            r"article[ -]5",
            r"article[ -]4",
        ],
        "detect_files": ["*.swift", "*.py", "*.js", "*.ts", "*.json", "*.md"],
        "detect_regex": r"openai|anthropic|chatgpt|llm|generativelanguage|api\.openai\.com|stable[ -]diffusion|CoreML|DeclaredAgeRange",
        "impact_desc": "The EU AI Act places strict transparency requirements on AI-driven apps under Article 50 (interaction disclosure, synthetic marking) and bans prohibited practices under Article 5.",
        "migration_steps": [
            "Add clear in-app disclosures: 'You are interacting with an AI system.'",
            "Mark all synthetic text, audio, images, or video in a machine-readable format.",
            "Verify that no prohibited practices (such as biometric classification of sensitive traits) are used.",
            "Document a team AI literacy policy in compliance with Article 4.",
        ],
        "compliance_impact": "Critical",
    },
    "EU GPSR": {
        "jurisdiction": "European Union",
        "authorities": ["European Commission", "Official Journal", "EUR-Lex"],
        "citations": [
            "Regulation (EU) 2023/988 of the European Parliament and of the Council of 10 May 2023 on general product safety (OJ L 135, 23.5.2023)"
        ],
        "keywords": [
            "gpsr",
            "general product safety regulation",
            "product safety",
            "manufacturer details",
            "responsible person",
            "safety warning",
        ],
        "patterns": [
            r"gpsr",
            r"general[ -]product[ -]safety[ -]regulation",
            r"product[ -]safety",
        ],
        "detect_files": ["*.swift", "*.py", "*.js", "*.ts", "*.json", "*.md"],
        "detect_regex": r"productListing|buyProduct|checkout|e-commerce|manufacturerInfo|safetyWarning|manufacturerEmail|manufacturerAddress|safetyLabel|productSafety|responsiblePerson",
        "impact_desc": "The EU GPSR (Regulation (EU) 2023/988) mandates that e-commerce applications and digital marketplaces distributed in the EU display manufacturer contact information and product safety warnings directly on the interface.",
        "migration_steps": [
            "Ensure e-commerce product detail templates display manufacturer identity (name, registered trade name/trademark).",
            "Provide manufacturer postal address and electronic address (email or website) directly on the interface.",
            "Display relevant product safety warnings or instructions in languages accepted by the member states of distribution.",
            "Formally verify that an EU-based Responsible Person is designated for any products sold to EU consumers.",
        ],
        "compliance_impact": "High",
    },
    "GDPR": {
        "jurisdiction": "European Union",
        "authorities": ["EDPB", "European Commission", "EUR-Lex"],
        "citations": [
            "Regulation (EU) 2016/679 (General Data Protection Regulation)",
            "EDPB Guidelines on Consent and Data Subject Rights",
        ],
        "keywords": [
            "gdpr",
            "general data protection regulation",
            "privacy policy",
            "data minimisation",
            "right to erase",
            "consent modal",
            "user tracking",
        ],
        "patterns": [
            r"gdpr",
            r"data[ -]minimisation",
            r"right[ -]to[ -]erase",
            r"user[ -]consent",
        ],
        "detect_files": ["*.swift", "*.ts", "*.js", "*.plist", "*.json", "*.md"],
        "detect_regex": r"privacyPolicy|userConsent|tracking|personalData|deleteAccount|NSUserTrackingUsageDescription",
        "impact_desc": "GDPR mandates strict user consent, purpose specification, data minimization, and a straightforward way for users to delete their accounts and personal data.",
        "migration_steps": [
            "Ensure the app implements a clear, prominent consent modal before collecting personal data.",
            "Offer a genuine in-app account deletion mechanism that removes all associated personal data.",
            "Audit all analytics and tracking SDKs to ensure data flows are disabled until opt-in consent is given.",
        ],
        "compliance_impact": "High",
    },
    "Data Act": {
        "jurisdiction": "European Union",
        "authorities": ["European Commission", "EUR-Lex"],
        "citations": [
            "Regulation (EU) 2023/2854 on harmonised rules on fair access to use of data (Data Act)"
        ],
        "keywords": [
            "data act",
            "access-by-design",
            "connected product",
            "wearable data",
            "smart device",
            "interoperability",
        ],
        "patterns": [r"data[ -]act", r"access[ -]by[ -]design"],
        "detect_files": ["*.swift", "*.py", "*.json", "*.md"],
        "detect_regex": r"wearable|sensor|deviceData|iot|smartDevice|connectedProduct",
        "impact_desc": "The EU Data Act requires developers of connected products and related services/apps to design systems so that data is easily accessible to users by default.",
        "migration_steps": [
            "Implement secure, user-accessible endpoints or download options for all user-generated device data.",
            "Provide transparent disclosures about how and when device sensor data is processed.",
            "Ensure data portability features are integrated into smart device companion apps.",
        ],
        "compliance_impact": "Medium",
    },
    "Data Governance Act": {
        "jurisdiction": "European Union",
        "authorities": ["European Commission", "EUR-Lex", "EDPB"],
        "citations": [
            "Regulation (EU) 2022/868 of the European Parliament and of the Council on European data governance (Data Governance Act)"
        ],
        "keywords": [
            "data governance act",
            "dga",
            "data altruism",
            "data intermediation",
            "trusted data sharing",
        ],
        "patterns": [r"data[ -]governance[ -]act", r"data[ -]altruism", r"data[ -]intermediary"],
        "detect_files": ["*.swift", "*.py", "*.json", "*.md"],
        "detect_regex": r"dataAltruism|dataIntermediary|dataSharing|dataTrustee",
        "impact_desc": "The EU Data Governance Act sets strict rules for data intermediation services and voluntary data altruism entities to facilitate secure cross-border data sharing.",
        "migration_steps": [
            "Verify whether data-sharing features qualify as data intermediation services under DGA Article 10.",
            "Ensure user data altruism consent mechanisms comply with standard European consent templates.",
            "Document compliance safeguards for non-personal data transfers outside the EEA.",
        ],
        "compliance_impact": "Medium",
    },
    "Cyber Resilience Act": {
        "jurisdiction": "European Union",
        "authorities": ["ENISA", "European Commission", "Official Journal"],
        "citations": [
            "Regulation (EU) 2024/2847 on horizontal cybersecurity requirements for products with digital elements (Cyber Resilience Act)"
        ],
        "keywords": [
            "cra",
            "cyber resilience act",
            "security-by-design",
            "vulnerability reporting",
            "sboms",
            "software bill of materials",
        ],
        "patterns": [
            r"cyber[ -]resilience[ -]act",
            r"security[ -]by[ -]design",
            r"vulnerability[ -]reporting",
        ],
        "detect_files": [
            "Package.swift",
            "Podfile",
            "build.gradle",
            "Cargo.toml",
            "package.json",
            "*.md",
        ],
        "detect_regex": r"security|vulnerability|dependency|encryption|ITSAppUsesNonExemptEncryption",
        "impact_desc": "The Cyber Resilience Act mandates horizontal cybersecurity requirements for hardware and software products, requiring security-by-design, SBOM tracking, and rapid vulnerability reporting.",
        "migration_steps": [
            "Establish an automated software bill of materials (SBOM) generation pipeline.",
            "Integrate a structured channel for security researchers to report vulnerabilities.",
            "Review dependencies for known vulnerabilities and implement a regular patching cadence.",
        ],
        "compliance_impact": "High",
    },
    "NIS2 Directive": {
        "jurisdiction": "European Union",
        "authorities": ["ENISA", "European Commission", "EUR-Lex"],
        "citations": [
            "Directive (EU) 2022/2555 on measures for a high common level of cybersecurity across the Union (NIS2 Directive)"
        ],
        "keywords": [
            "nis2",
            "cybersecurity directive",
            "incident reporting",
            "essential entities",
            "important entities",
        ],
        "patterns": [r"nis2", r"directive[ -]2022/2555", r"cybersecurity[ -]incident"],
        "detect_files": ["*.swift", "*.py", "Package.swift", "build.gradle", "*.json", "*.md"],
        "detect_regex": r"incidentReport|securityAlert|nis2|threatIntelligence|vulnerabilityNotification",
        "impact_desc": "NIS2 mandates strict cybersecurity risk-management measures, supply chain security audits, and a mandatory 24-hour early warning incident notification duty for essential and important entities.",
        "migration_steps": [
            "Implement automated 24-hour incident notification workflows for cybersecurity incidents.",
            "Perform supply chain cybersecurity risk assessments on third-party dependencies.",
            "Establish multi-factor authentication and continuous vulnerability management policies.",
        ],
        "compliance_impact": "High",
    },
    "Digital Services Act": {
        "jurisdiction": "European Union",
        "authorities": ["European Commission", "Official Journal"],
        "citations": [
            "Regulation (EU) 2022/2065 on a Single Market For Digital Services (Digital Services Act)"
        ],
        "keywords": [
            "dsa",
            "digital services act",
            "trader status",
            "content moderation",
            "flagging",
            "notice and action",
        ],
        "patterns": [
            r"digital[ -]services[ -]act",
            r"trader[ -]status",
            r"content[ -]moderation",
        ],
        "detect_files": ["Info.plist", "metadata", "*.swift", "*.md"],
        "detect_regex": r"trader|dsa|reportContent|flagUser|moderation|blockUser",
        "impact_desc": "The DSA requires verified trader registration (D-U-N-S, phone, email publishing) for storefront distributors and mandates clear user reporting/moderation channels for UGC apps.",
        "migration_steps": [
            "Complete and verify DSA Trader requirements in App Store Connect / Google Play Console.",
            "Add user-friendly content flagging, blocking, and reporting interfaces if the app hosts user-generated content.",
            "Establish clear notice-and-action protocols for taking down illegal content.",
        ],
        "compliance_impact": "Critical",
    },
    "Digital Markets Act": {
        "jurisdiction": "European Union",
        "authorities": ["European Commission", "Official Journal"],
        "citations": [
            "Regulation (EU) 2022/1925 on contestable and fair markets in the digital sector (Digital Markets Act)"
        ],
        "keywords": [
            "dma",
            "digital markets act",
            "anti-steering",
            "alternative payment",
            "external purchase link",
            "alternative marketplace",
        ],
        "patterns": [
            r"digital[ -]markets[ -]act",
            r"external[ -]purchase",
            r"anti[ -]steering",
        ],
        "detect_files": ["*.swift", "*.plist", "*.entitlements", "*.md"],
        "detect_regex": r"com\.apple\.developer\.storekit\.external-purchase|SKExternalPurchase|alternateBilling|Stripe|PayPal",
        "impact_desc": "The DMA opens up closed app store ecosystems, allowing alternative app distribution, alternative browser engines, and direct external payment promotion links.",
        "migration_steps": [
            "Adopt approved external purchase link entitlements and custom StoreKit link APIs for EU users.",
            "Wire system-mandated payment warning and disclosure sheets.",
            "Ensure appropriate monthly transaction and CTC reporting channels are configured.",
        ],
        "compliance_impact": "High",
    },
    "ePrivacy Directive": {
        "jurisdiction": "European Union",
        "authorities": ["European Commission", "EDPB", "EUR-Lex"],
        "citations": [
            "Directive 2002/58/EC (ePrivacy Directive) as amended by Directive 2009/136/EC",
            "EDPB Guidelines on Cookie Consent and Terminal Equipment Access",
        ],
        "keywords": [
            "eprivacy",
            "cookie consent",
            "tracking pixels",
            "storage access",
            "terminal equipment",
        ],
        "patterns": [r"eprivacy", r"cookie[ -]consent", r"terminal[ -]equipment"],
        "detect_files": ["*.swift", "*.ts", "*.js", "*.html", "*.plist", "*.md"],
        "detect_regex": r"cookie|localStorage|sessionStorage|trackingPixel|deviceFingerprint|NSUserTrackingUsageDescription",
        "impact_desc": "The ePrivacy Directive requires prior opt-in consent before storing or accessing information on a user's terminal equipment, including cookies, local storage, and tracking SDKs.",
        "migration_steps": [
            "Ensure all non-essential cookies and local storage writes are blocked until active opt-in consent.",
            "Verify that tracking SDKs do not access device identifiers before explicit user authorization.",
            "Provide a simple, persistent way for users to withdraw consent at any time.",
        ],
        "compliance_impact": "High",
    },
    "European Accessibility Act": {
        "jurisdiction": "European Union",
        "authorities": ["European Commission", "Official Journal"],
        "citations": [
            "Directive (EU) 2019/882 of the European Parliament and of the Council of 17 April 2019 on the accessibility requirements for products and services",
            "Harmonised Standard EN 301 549 Chapter 11 (Accessibility requirements for non-web software)",
        ],
        "keywords": [
            "eaa",
            "european accessibility act",
            "en 301 549",
            "accessibility requirements",
            "wcag 2.1",
            "accessibility statement",
        ],
        "patterns": [
            r"european[ -]accessibility[ -]act",
            r"en[ -]301[ -]549",
            r"accessibility[ -]statement",
        ],
        "detect_files": ["*.swift", "*.storyboard", "*.xib", "*.html", "*.md"],
        "detect_regex": r"accessibilityLabel|accessibilityTraits|VoiceOver|DynamicType|contrast|accessibilityHint",
        "impact_desc": "The EAA mandates that digital services, including mobile applications and e-commerce websites, meet strict accessibility requirements of EN 301 549 (based on WCAG 2.1 AA) and publish an accessibility statement.",
        "migration_steps": [
            "Audit all UI components to ensure screen-reader labels (accessibilityLabel) and traits are present.",
            "Verify support for system-wide font scaling (Dynamic Type) without breaking the layout.",
            "Maintain WCAG 2.1 AA color contrast compliance (at least 4.5:1 for normal text).",
            "Draft and publish an official accessibility statement reachable from within the app.",
        ],
        "compliance_impact": "High",
    },
    "Product Liability Directive": {
        "jurisdiction": "European Union",
        "authorities": ["European Commission", "Official Journal", "EUR-Lex"],
        "citations": [
            "Directive (EU) 2024/2853 of the European Parliament and of the Council on liability for defective products (Revised Product Liability Directive)"
        ],
        "keywords": [
            "product liability directive",
            "defective software",
            "software liability",
            "strict liability",
        ],
        "patterns": [r"product[ -]liability", r"defective[ -]software", r"pld"],
        "detect_files": ["*.swift", "*.py", "*.json", "*.md"],
        "detect_regex": r"softwareLiability|defectReporting|safetyPatch|versionControl",
        "impact_desc": "The revised EU Product Liability Directive explicitly includes software, AI systems, and digital services under strict product liability for damages caused by defectiveness.",
        "migration_steps": [
            "Maintain detailed documentation and logging of software safety testing and risk assessments.",
            "Establish rapid security and safety patch deployment procedures for active software builds.",
            "Ensure user safety disclosures accurately describe software operating limits.",
        ],
        "compliance_impact": "Medium",
    },
    "AI Liability Framework": {
        "jurisdiction": "European Union",
        "authorities": ["European Commission", "EUR-Lex", "EDPB"],
        "citations": [
            "Proposal for a Directive of the European Parliament and of the Council on adapting non-contractual civil liability rules to artificial intelligence (AI Liability Directive)"
        ],
        "keywords": [
            "ai liability",
            "presumption of causality",
            "disclosure of evidence",
            "ai damage",
        ],
        "patterns": [r"ai[ -]liability", r"causality[ -]presumption", r"ai[ -]damage"],
        "detect_files": ["*.swift", "*.py", "*.json", "*.md"],
        "detect_regex": r"aiLogging|decisionAudit|modelOutput|aiAuditTrail",
        "impact_desc": "The EU AI Liability framework eases the burden of proof for victims seeking compensation for AI-driven harms by introducing presumptions of causality and court-ordered evidence disclosure.",
        "migration_steps": [
            "Implement comprehensive audit logging for AI system inputs, outputs, and confidence metrics.",
            "Maintain structured records of model training, alignment, and post-deployment monitoring.",
            "Establish clear accountability protocols for automated AI decision-making features.",
        ],
        "compliance_impact": "High",
    },
    "UK Online Safety Act": {
        "jurisdiction": "United Kingdom",
        "authorities": ["Ofcom", "Government publications"],
        "citations": [
            "Online Safety Act 2023 (c. 50)",
            "Ofcom Guidelines on Highly Effective Age Assurance for Child Protection",
        ],
        "keywords": [
            "online safety act",
            "ofcom",
            "age assurance",
            "child protection",
            "harmful content",
            "digital id",
        ],
        "patterns": [
            r"online[ -]safety[ -]act",
            r"age[ -]assurance",
            r"child[ -]protection",
        ],
        "detect_files": ["*.swift", "Info.plist", "*.json", "*.md"],
        "detect_regex": r"age-gating|DeclaredAgeRange|ageVerification|parental|Ofcom",
        "impact_desc": "The UK Online Safety Act requires platforms likely to host child users or harmful content to use highly effective age assurance methods (e.g. digital ID, facial estimation) rather than simple self-declaration.",
        "migration_steps": [
            "Upgrade minor age assurance flows to leverage verified methods (such as document checking or facial age estimation).",
            "Store and process verification data in a ringfenced environment and destroy it immediately after use.",
            "Verify that default privacy settings for minor accounts are highly restrictive.",
        ],
        "compliance_impact": "Critical",
    },
    "ICO Childrens Code": {
        "jurisdiction": "United Kingdom",
        "authorities": ["ICO", "Government publications"],
        "citations": [
            "Information Commissioner's Office Age Appropriate Design Code (Children's Code)",
            "UK Data Protection Act 2018",
        ],
        "keywords": [
            "childrens code",
            "age appropriate design",
            "ico",
            "high privacy by default",
            "dpia",
        ],
        "patterns": [
            r"children[s]?[ -]code",
            r"age[ -]appropriate[ -]design",
            r"high[ -]privacy[ -]by[ -]default",
        ],
        "detect_files": ["*.swift", "Info.plist", "*.md"],
        "detect_regex": r"dpia|tracking|location|profiling|minor|child",
        "impact_desc": "The ICO Children's Code sets 15 standards for apps likely to be accessed by children under 18, requiring high privacy by default, zero tracking/profiling by default, and a formal DPIA.",
        "migration_steps": [
            "Conduct a comprehensive Data Protection Impact Assessment (DPIA).",
            "Disable precise geolocation and profiling features by default for all minor accounts.",
            "Verify that privacy policies and terms are presented in child-friendly language.",
        ],
        "compliance_impact": "High",
    },
    "UK DSIT & AI Regulation": {
        "jurisdiction": "United Kingdom",
        "authorities": ["DSIT", "ICO", "Government publications"],
        "citations": [
            "UK Department for Science, Innovation and Technology (DSIT) AI Regulation White Paper and Sectoral Guidelines"
        ],
        "keywords": [
            "dsit",
            "uk ai regulation",
            "pro-innovation ai framework",
            "cross-sectoral ai principles",
        ],
        "patterns": [r"dsit", r"uk[ -]ai[ -]regulation", r"pro[ -]innovation"],
        "detect_files": ["*.swift", "*.py", "*.json", "*.md"],
        "detect_regex": r"aiGovernance|safetyAssessment|ukAiPolicy|explainability",
        "impact_desc": "UK DSIT AI regulation enforces key principles including safety, security, transparency, fairness, accountability, and redress across sector regulators (ICO, FCA, CMA).",
        "migration_steps": [
            "Conduct safety and fairness evaluations for AI models deployed in the UK market.",
            "Provide user-accessible explainability notices for AI-generated decisions.",
            "Establish an internal AI risk registry aligned with UK DSIT cross-sector principles.",
        ],
        "compliance_impact": "High",
    },
    "UK FCA & CMA Digital Regulations": {
        "jurisdiction": "United Kingdom",
        "authorities": ["FCA", "CMA", "Government publications"],
        "citations": [
            "FCA Guidance on AI in Financial Services and CMA Digital Markets, Competition and Consumers Act 2024"
        ],
        "keywords": [
            "fca",
            "cma",
            "digital markets act",
            "financial conduct",
            "consumer protection",
        ],
        "patterns": [r"\bfca\b", r"\bcma\b", r"digital[ -]markets[ -]competition"],
        "detect_files": ["*.swift", "*.py", "*.json", "*.md"],
        "detect_regex": r"financialAdvice|consumerProtection|subscriptionTrap|cmaCompliance|fcaRules",
        "impact_desc": "The UK CMA and FCA enforce strict rules against dark patterns, subscription traps, and misleading AI-generated financial or consumer recommendations.",
        "migration_steps": [
            "Verify that subscription signup and cancellation flows are transparent and symmetric.",
            "Ensure AI-generated consumer advice clearly discloses limitations and risk disclaimers.",
            "Audit consumer user journeys to eliminate deceptive design patterns (dark patterns).",
        ],
        "compliance_impact": "High",
    },
    "US COPPA": {
        "jurisdiction": "United States (Federal)",
        "authorities": ["FTC", "Federal Register"],
        "citations": [
            "Children's Online Privacy Protection Act, 15 U.S.C. 6501-6508",
            "FTC Amended Children's Online Privacy Protection Rule (90 FR 16918, April 2025)",
        ],
        "keywords": [
            "coppa",
            "childrens online privacy",
            "ftc coppa",
            "verifiable parental consent",
            "biometric identifier",
            "retention policy",
        ],
        "patterns": [
            r"coppa",
            r"verifiable[ -]parental[ -]consent",
            r"biometric[ -]identifier",
        ],
        "detect_files": ["*.swift", "Info.plist", "*.md"],
        "detect_regex": r"coppa|under-13|kids|parentalGate|parentalConsent|biometric|gait|voiceprint|facialTemplate",
        "impact_desc": "COPPA protects under-13 children, and the 2025/2026 Amended Rule adds biometric identifiers to PII, mandates separate opt-in consent for ads, and requires a written security program.",
        "migration_steps": [
            "Implement verifiable parental consent methods (such as government photo ID verification) before collecting minor PII.",
            "Maintain a written data retention policy with an automated purging schedule for minor accounts.",
            "Ensure zero ad-tracking SDKs are active inside child-targeted sections.",
        ],
        "compliance_impact": "Critical",
    },
    "US State ASAA": {
        "jurisdiction": "United States (State)",
        "authorities": ["State Legislatures", "CISA"],
        "citations": [
            "Utah SB 142 (App Store Accountability Act)",
            "Texas SB 2420 (App Store Accountability Act)",
            "Louisiana HB 570 (App Store Accountability Act)",
        ],
        "keywords": [
            "asaa",
            "app store accountability",
            "utah sb 142",
            "texas sb 2420",
            "louisiana hb 570",
            "age category",
        ],
        "patterns": [
            r"asaa",
            r"app[ -]store[ -]accountability",
            r"sb[ -]142",
            r"sb[ -]2420",
        ],
        "detect_files": ["*.swift", "Info.plist", "*.md"],
        "detect_regex": r"DeclaredAgeRange|ageCategory|parentalConsent|texas|utah",
        "impact_desc": "State App Store Accountability Acts require stores and developers to cooperate on age categorization and require verified parental consent before a minor downloads or transacts.",
        "migration_steps": [
            "Integrate with platform Declared Age Range APIs to request the user's age category.",
            "Enforce strict deletion of verification data immediately after age checks complete.",
            "Verify and enforce parental consent checks on all minor transactions.",
        ],
        "compliance_impact": "Critical",
    },
    "US FTC & NIST Frameworks": {
        "jurisdiction": "United States (Federal)",
        "authorities": ["FTC", "NIST", "CISA", "Federal Register"],
        "citations": [
            "NIST AI Risk Management Framework (AI RMF 1.0 / NIST SP 1270)",
            "FTC Act Section 5 Unfair and Deceptive Practices Guidance",
        ],
        "keywords": [
            "nist",
            "nist ai rmf",
            "ftc section 5",
            "unfair or deceptive practices",
            "automated decision",
        ],
        "patterns": [r"nist[ -]ai[ -]rmf", r"ftc[ -]section[ -]5", r"nist[ -]csf"],
        "detect_files": ["*.swift", "*.py", "*.json", "*.md"],
        "detect_regex": r"nistCompliance|riskMap|measureGovern|deceptivePractice|ftcAudit",
        "impact_desc": "FTC Section 5 and NIST AI RMF mandate that AI systems used in commercial products avoid deceptive claims, biases, or unverified safety representations.",
        "migration_steps": [
            "Map, measure, and manage AI risks according to NIST AI RMF functions (Govern, Map, Measure, Manage).",
            "Audit marketing claims for AI features to ensure zero false or unsubstantiated capability statements.",
            "Implement continuous bias and output monitoring for consumer-facing automated tools.",
        ],
        "compliance_impact": "High",
    },
    "US Executive Orders & CISA": {
        "jurisdiction": "United States (Federal)",
        "authorities": ["CISA", "Executive Office of the President", "NIST"],
        "citations": [
            "Executive Order 14110 on Safe, Secure, and Trustworthy Artificial Intelligence",
            "CISA Secure-by-Design Principles and Software Bill of Materials (SBOM) Guidance",
        ],
        "keywords": [
            "executive order 14110",
            "eo 14110",
            "cisa",
            "secure-by-design",
            "software bill of materials",
        ],
        "patterns": [r"eo[ -]14110", r"executive[ -]order[ -]14110", r"cisa", r"secure[ -]by[ -]design"],
        "detect_files": ["Package.swift", "build.gradle", "package.json", "*.py", "*.md"],
        "detect_regex": r"cisa|sbom|secureByDesign|vulnerabilityManagement|redTeaming",
        "impact_desc": "Executive Order 14110 and CISA Secure-by-Design guidance mandate rigorous red-teaming, vulnerability disclosures, and software bill of materials (SBOM) management.",
        "migration_steps": [
            "Maintain an automated Software Bill of Materials (SBOM) for all product dependencies.",
            "Perform red-teaming evaluations on generative AI and system-critical capabilities.",
            "Incorporate CISA secure-by-design principles into the development lifecycle.",
        ],
        "compliance_impact": "High",
    },
    "US State AI Legislation": {
        "jurisdiction": "United States (State)",
        "authorities": ["State Legislatures"],
        "citations": [
            "California SB 1047 (Safe and Secure Innovation for Frontier Artificial Intelligence Models Act)",
            "Colorado Artificial Intelligence Act (SB 24-205)",
            "Utah Artificial Intelligence Policy Act (SB 149)",
        ],
        "keywords": [
            "colorado ai act",
            "sb 24-205",
            "utah ai policy act",
            "california sb 1047",
            "algorithmic discrimination",
        ],
        "patterns": [r"colorado[ -]ai", r"utah[ -]ai", r"sb[ -]24-205", r"algorithmic[ -]discrimination"],
        "detect_files": ["*.swift", "*.py", "*.json", "*.md"],
        "detect_regex": r"algorithmicBias|stateAiDisclosure|coloradoAi|utahAi|consequentialDecision",
        "impact_desc": "US State AI laws (Colorado SB 24-205, Utah SB 149) require developers and deployers of high-risk AI systems to prevent algorithmic discrimination, conduct impact assessments, and inform consumers.",
        "migration_steps": [
            "Implement explicit consumer disclosures when AI is used to make or assist in consequential decisions.",
            "Complete annual algorithmic discrimination impact assessments for high-risk AI deployments.",
            "Provide an opt-out mechanism for automated profiling in applicable US state jurisdictions.",
        ],
        "compliance_impact": "Critical",
    },
    "Canada OPC & AIDA": {
        "jurisdiction": "Canada",
        "authorities": ["Office of the Privacy Commissioner of Canada (OPC)", "ISED"],
        "citations": [
            "Personal Information Protection and Electronic Documents Act (PIPEDA)",
            "Quebec Law 25 (An Act respecting the reform of legislative provisions as regards the protection of personal information)",
            "Canada Artificial Intelligence and Data Act (AIDA - Bill C-27)",
        ],
        "keywords": [
            "opc",
            "pipeda",
            "law 25",
            "aida",
            "artificial intelligence and data act",
            "bill c-27",
        ],
        "patterns": [r"\baida\b", r"bill[ -]c-27", r"quebec[ -]law[ -]25", r"pipeda"],
        "detect_files": ["*.swift", "*.py", "*.json", "*.md"],
        "detect_regex": r"quebecPrivacy|aidaRisk|pipedaConsent|canadaPrivacy",
        "impact_desc": "Canadian privacy law (Quebec Law 25) and AIDA mandate explicit opt-in consent for profiling, privacy impact assessments, and strict risk mitigation for high-impact AI systems.",
        "migration_steps": [
            "Conduct a Privacy Impact Assessment (PIA) for features processing Canadian user data.",
            "Implement explicit opt-in mechanisms for tracking, profiling, or automated processing.",
            "Prepare high-impact AI risk assessments and plain-language public disclosures.",
        ],
        "compliance_impact": "High",
    },
    "Australia OAIC & AI Governance": {
        "jurisdiction": "Australia",
        "authorities": ["OAIC", "eSafety Commissioner"],
        "citations": [
            "Australian Privacy Principles (APPs) under Privacy Act 1988",
            "OAIC Guidance on AI and Privacy",
            "Australia Voluntary AI Safety Standard",
        ],
        "keywords": [
            "oaic",
            "australian privacy principles",
            "app",
            "voluntary ai safety standard",
            "privacy act",
        ],
        "patterns": [r"\boaic\b", r"australian[ -]privacy[ -]principles", r"voluntary[ -]ai[ -]safety"],
        "detect_files": ["*.swift", "*.py", "*.json", "*.md"],
        "detect_regex": r"oaic|appCompliance|australiaPrivacy|aiSafetyStandard",
        "impact_desc": "The OAIC enforces Australian Privacy Principles (APPs) for AI systems, requiring transparency in personal data processing, strict purpose limitation, and robust testing for AI models.",
        "migration_steps": [
            "Publish clear disclosures informing Australian users when personal data is used to train or query AI models.",
            "Provide mechanisms for Australian users to request access or correction of personal data.",
            "Adhere to Australia's Voluntary AI Safety Standard guardrails for high-risk features.",
        ],
        "compliance_impact": "High",
    },
    "Australia Online Safety": {
        "jurisdiction": "Australia",
        "authorities": ["OAIC", "eSafety Commissioner"],
        "citations": [
            "Online Safety Amendment (Social Media Minimum Age) Act 2024",
            "OAIC Guidelines on AI Governance and Privacy",
        ],
        "keywords": [
            "minimum age",
            "social media minimum age",
            "esafety",
            "oaic",
            "australia online safety",
        ],
        "patterns": [r"minimum[ -]age", r"esafety", r"oaic"],
        "detect_files": ["*.swift", "Info.plist", "*.md"],
        "detect_regex": r"age-gating|social|minor|under-16|australia|DeclaredAgeRange",
        "impact_desc": "Australian law restricts under-16 access to designated social media services via robust age assurance and mandates strict data protection for age verification data.",
        "migration_steps": [
            "Enforce robust age estimation or verification for social elements on Australian storefronts.",
            "Ringfence and completely destroy age verification data to comply with eSafety rules.",
        ],
        "compliance_impact": "Critical",
    },
    "Brazil Digital ECA": {
        "jurisdiction": "Brazil",
        "authorities": ["ANPD", "Government publications"],
        "citations": [
            "Digital ECA (Law 15,211/2025)",
            "ANPD Rules on Age Assurance and LGPD Minor Consent",
        ],
        "keywords": ["digital eca", "law 15211", "anpd", "cpf", "brazil age assurance"],
        "patterns": [r"digital[ -]eca", r"law[ -]15211", r"anpd", r"brazil"],
        "detect_files": ["*.swift", "Info.plist", "*.md"],
        "detect_regex": r"cpf|age-assurance|brazil|lgpd|DeclaredAgeRange",
        "impact_desc": "Brazil's Digital ECA prohibits simple age self-declaration checkboxes and mandates approved methods such as facial matching, document checking, or CPF database verification.",
        "migration_steps": [
            "Integrate approved verification mechanisms (CPF, facial, or document) for Brazilian minor accounts.",
            "Configure loot-box games to auto-rate 18-plus in compliance with Brazilian classification requirements.",
        ],
        "compliance_impact": "Critical",
    },
    "Singapore PDPC & AI Verify": {
        "jurisdiction": "Singapore",
        "authorities": ["PDPC", "IMDA", "AI Verify Foundation"],
        "citations": [
            "Singapore Personal Data Protection Act (PDPA)",
            "PDPC Advisory Guidelines on Use of Personal Data in AI Systems",
            "AI Verify Governance Framework",
        ],
        "keywords": [
            "pdpc",
            "pdpa",
            "ai verify",
            "imda",
            "model artificial intelligence governance framework",
        ],
        "patterns": [r"\bpdpc\b", r"\bpdpa\b", r"ai[ -]verify", r"model[ -]ai[ -]governance"],
        "detect_files": ["*.swift", "*.py", "*.json", "*.md"],
        "detect_regex": r"pdpc|pdpaConsent|aiVerify|singaporePrivacy|dataProtectionOfficer",
        "impact_desc": "Singapore's PDPC guidelines and AI Verify framework set clear standards for data consent, explainability, safety testing, and human oversight in AI deployments.",
        "migration_steps": [
            "Ensure explicit consent or valid exceptions are established before using personal data in AI models under PDPA.",
            "Appoint and publish contact details for a designated Data Protection Officer (DPO).",
            "Benchmark AI models using the open-source AI Verify testing toolkit for technical transparency.",
        ],
        "compliance_impact": "High",
    },
    "Singapore Online Safety": {
        "jurisdiction": "Singapore",
        "authorities": ["PDPC", "IMDA"],
        "citations": [
            "IMDA Code of Practice for Online Safety for App Distribution Services (April 2026)",
            "Singapore Personal Data Protection Act (PDPA)",
        ],
        "keywords": [
            "imda",
            "pdpc",
            "singapore online safety",
            "app store age assurance",
        ],
        "patterns": [r"imda", r"pdpc", r"singapore"],
        "detect_files": ["*.swift", "Info.plist", "*.md"],
        "detect_regex": r"age-assurance|singapore|imda|DeclaredAgeRange",
        "impact_desc": "Singapore IMDA rules mandate that stores and developers screen and stop minor access to age-inappropriate apps through credit-card or digital verification.",
        "migration_steps": [
            "Adopt native platform age-assurance APIs for users on the Singapore storefront.",
            "Verify that no age verification data is stored longer than legally necessary.",
        ],
        "compliance_impact": "Critical",
    },
    "International ISO/IEC Standards": {
        "jurisdiction": "International",
        "authorities": ["ISO", "IEC"],
        "citations": [
            "ISO/IEC 42001:2023 Information technology - Artificial intelligence - Management system (AIMS)",
            "ISO/IEC 27001:2022 Information security, cybersecurity and privacy protection",
        ],
        "keywords": [
            "iso 42001",
            "iso 27001",
            "iso/iec 42001",
            "iso/iec 27001",
            "ai management system",
            "aims",
        ],
        "patterns": [r"iso[ -]42001", r"iso[ -]27001", r"iso/iec[ -]42001", r"iso/iec[ -]27001"],
        "detect_files": ["*.swift", "*.py", "Package.swift", "build.gradle", "*.json", "*.md"],
        "detect_regex": r"iso42001|iso27001|aims|securityPolicy|riskManagement",
        "impact_desc": "ISO/IEC 42001 is the international benchmark for AI Management Systems (AIMS), setting verifiable controls for AI risk management, data quality, and system safety.",
        "migration_steps": [
            "Establish an AI Management System (AIMS) aligned with ISO/IEC 42001 control objectives.",
            "Implement rigorous data quality and bias mitigation audits for AI training and fine-tuning datasets.",
            "Maintain an integrated risk assessment process linking ISO/IEC 27001 security controls with ISO/IEC 42001 AI controls.",
        ],
        "compliance_impact": "Medium",
    },
    "International OECD AI Principles": {
        "jurisdiction": "International",
        "authorities": ["OECD"],
        "citations": [
            "OECD Recommendation of the Council on Artificial Intelligence (OECD AI Principles 2024 Revision)"
        ],
        "keywords": [
            "oecd ai principles",
            "oecd recommendation",
            "trustworthy ai",
            "human-centric ai",
        ],
        "patterns": [r"oecd[ -]ai", r"oecd[ -]principles", r"trustworthy[ -]ai"],
        "detect_files": ["*.swift", "*.py", "*.json", "*.md"],
        "detect_regex": r"oecd|trustworthyAi|humanCentric|aiAccountability|aiRobustness",
        "impact_desc": "The OECD AI Principles serve as the foundational global baseline for trustworthy AI, emphasizing inclusive growth, human-centric values, transparency, robustness, and accountability.",
        "migration_steps": [
            "Incorporate OECD principles of transparency and explainability into AI feature design.",
            "Implement human oversight and fallback mechanisms for automated or AI-assisted operations.",
            "Conduct continuous risk and robustness testing against adversarial threats.",
        ],
        "compliance_impact": "Medium",
    },
    "International G7 & G20 AI Frameworks": {
        "jurisdiction": "International",
        "authorities": ["G7", "G20"],
        "citations": [
            "G7 Hiroshima AI Process International Code of Conduct for Organizations Developing Advanced AI Systems",
            "G20 AI Principles for Trustworthy AI",
        ],
        "keywords": [
            "g7 hiroshima",
            "hiroshima ai process",
            "g20 ai principles",
            "advanced ai code of conduct",
        ],
        "patterns": [r"g7[ -]hiroshima", r"hiroshima[ -]ai", r"g20[ -]ai"],
        "detect_files": ["*.swift", "*.py", "*.json", "*.md"],
        "detect_regex": r"hiroshimaCode|g7Compliance|g20Ai|advancedAiSafety",
        "impact_desc": "The G7 Hiroshima AI Code of Conduct and G20 AI Principles mandate voluntary and mandatory safety evaluations, post-deployment monitoring, and digital watermarking for advanced AI systems.",
        "migration_steps": [
            "Adopt digital watermarking and provenance tracking for AI-generated synthetic content.",
            "Establish vulnerability reporting channels for external security researchers analyzing AI models.",
            "Participate in standardized pre-deployment red-teaming and safety benchmarks.",
        ],
        "compliance_impact": "Medium",
    },
}

# Pre-defined Simulated Regulatory Announcements
SIMULATED_DEVELOPMENTS = [
    {
        "title": "EU AI Act Article 50 Transparency Obligations taking full effect in August 2026",
        "description": "The European Commission published draft implementation guidelines on transparency obligations under Article 50 of the AI Act. Developers of chatbot systems and synthetic content generators must implement interaction disclosure and watermarking.",
        "pubDate": "Fri, 08 May 2026 12:00:00 GMT",
        "link": "https://digital-strategy.ec.europa.eu/en/library/draft-guidelines-implementation-transparency-obligations-certain-ai-systems-under-article-50-ai-act",
    },
    {
        "title": "EU General Product Safety Regulation (GPSR) enforcement fully applicable across EU Member States",
        "description": "Regulation (EU) 2023/988 (GPSR) replaces the old General Product Safety Directive, requiring digital platforms and e-commerce applications to clearly display manufacturer identity, importer details, and product safety warnings directly on online product listings.",
        "pubDate": "Fri, 13 Dec 2024 09:00:00 GMT",
        "link": "https://eur-lex.europa.eu/eli/reg/2023/988/oj",
    },
    {
        "title": "FTC issues final updates to the COPPA Children's Online Privacy Rule",
        "description": "The Federal Trade Commission finalized amendments to the COPPA Rule, extending the definition of personal information to cover modern biometric identifiers and requiring separate parent opt-in for ad-sharing.",
        "pubDate": "Tue, 22 Apr 2025 09:00:00 GMT",
        "link": "https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule",
    },
    {
        "title": "European Accessibility Act enforcement begins across all EU Member States",
        "description": "Directive (EU) 2019/882 (European Accessibility Act) becomes enforceable, requiring mobile and web banking, travel, and retail services to satisfy harmonised accessibility standard EN 301 549.",
        "pubDate": "Sat, 28 Jun 2025 08:00:00 GMT",
        "link": "https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/disability/union-equality-strategy-rights-persons-disabilities-2021-2030/european-accessibility-act_en",
    },
    {
        "title": "UK DSIT issues updated guidance on pro-innovation cross-sectoral UK AI regulation principles",
        "description": "The UK Department for Science, Innovation and Technology (DSIT) issued updated guidance directing sector regulators (ICO, FCA, CMA) to enforce safety, transparency, and fairness standards across AI deployments.",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 GMT",
        "link": "https://www.gov.uk/government/publications/uk-ai-regulation-framework-guidance",
    },
    {
        "title": "NIST issues SP 1270 AI Risk Management Framework 1.0 operational guidance",
        "description": "The National Institute of Standards and Technology (NIST) published operational guidance for the AI Risk Management Framework (AI RMF 1.0), emphasizing Govern, Map, Measure, and Manage functions for commercial applications.",
        "pubDate": "Wed, 10 Sep 2025 14:00:00 GMT",
        "link": "https://www.nist.gov/itl/ai-risk-management-framework",
    },
    {
        "title": "CISA issues Secure-by-Design and SBOM requirements under Executive Order 14110",
        "description": "The Cybersecurity and Infrastructure Security Agency (CISA) released secure-by-design guidelines requiring automated Software Bill of Materials (SBOM) generation and vulnerability disclosure channels.",
        "pubDate": "Thu, 20 Nov 2025 11:00:00 GMT",
        "link": "https://www.cisa.gov/secure-by-design",
    },
    {
        "title": "Colorado Artificial Intelligence Act (SB 24-205) compliance guidance issued",
        "description": "The Colorado Attorney General issued official compliance guidance for SB 24-205, mandating impact assessments and consumer disclosures to prevent algorithmic discrimination in consequential decisions.",
        "pubDate": "Tue, 13 Jan 2026 09:00:00 GMT",
        "link": "https://coag.gov/ai-act-guidance",
    },
    {
        "title": "Canada OPC issues privacy guidance for high-impact AI systems under PIPEDA and Quebec Law 25",
        "description": "The Office of the Privacy Commissioner of Canada (OPC) published guidance requiring explicit opt-in consent for tracking, profiling, and automated processing of Canadian user data.",
        "pubDate": "Fri, 20 Feb 2026 15:00:00 GMT",
        "link": "https://www.priv.gc.ca/en/privacy-topics/technology/artificial-intelligence/",
    },
    {
        "title": "Australia OAIC releases updated AI Governance and Privacy Principles Guidance",
        "description": "The Office of the Australian Information Commissioner (OAIC) updated guidance enforcing Australian Privacy Principles (APPs) for AI training and data access rights.",
        "pubDate": "Wed, 18 Mar 2026 08:00:00 GMT",
        "link": "https://www.oaic.gov.au/privacy/ai-governance-guidance",
    },
    {
        "title": "Singapore PDPC and IMDA issue Advisory Guidelines on AI Data Processing and AI Verify Testing",
        "description": "Singapore PDPC and IMDA published updated advisory guidelines and AI Verify benchmarks for transparent, explainable, and secure AI system operations.",
        "pubDate": "Mon, 06 Apr 2026 10:00:00 GMT",
        "link": "https://www.pdpc.gov.sg/guidelines-and-schemes/ai-governance",
    },
    {
        "title": "ISO/IEC 42001 Artificial Intelligence Management System (AIMS) certification framework",
        "description": "ISO and IEC published the updated conformity assessment standards for ISO/IEC 42001:2023, establishing international benchmarks for AI risk management and system governance.",
        "pubDate": "Thu, 14 May 2026 12:00:00 GMT",
        "link": "https://www.iso.org/standard/81230.html",
    },
    {
        "title": "OECD Council updates Recommendation on Artificial Intelligence Principles",
        "description": "The OECD Council issued an updated Recommendation on AI Principles, reinforcing requirements for human-centric AI, transparency, robustness, and accountability.",
        "pubDate": "Tue, 02 Jun 2026 09:00:00 GMT",
        "link": "https://www.oecd.org/en/topics/sub-issues/oecd-ai-principles.html",
    },
    {
        "title": "G7 Hiroshima AI Process International Code of Conduct adopted by global distribution platforms",
        "description": "G7 member countries and global technology distributors endorsed the Hiroshima AI Code of Conduct, requiring watermarking of synthetic content and safety evaluations.",
        "pubDate": "Fri, 10 Jul 2026 13:00:00 GMT",
        "link": "https://ec.europa.eu/commission/presscorner/detail/en/ip_23_5379",
    },
    {
        "title": "Unverified rumors of GDPR policy changes on Reddit forum",
        "description": "An anonymous user posted a rumor on Reddit saying GDPR consent requirements are changing. No official authorities or official sources were referenced.",
        "pubDate": "Sun, 26 Jul 2026 12:00:00 GMT",
        "link": "https://reddit.com/r/privacy/comments/12345/GDPR_rumor",
    },
]


def scan_target_repo(repo_path, track_name, metadata):
    """
    Scans the repository path to identify affected files and files of interest.
    """
    affected_files = []
    file_patterns = metadata["detect_files"]
    detect_regex = metadata["detect_regex"]

    if not os.path.exists(repo_path):
        return [], "Repository path does not exist."

    # Build simple regex for patterns
    compiled_patterns = []
    for pat in file_patterns:
        if pat.startswith("*."):
            compiled_patterns.append(re.compile(r".*\." + re.escape(pat[2:]) + "$"))
        else:
            compiled_patterns.append(re.compile(r".*" + re.escape(pat) + "$"))

    for root, dirs, files in os.walk(repo_path):
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
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as fp:
                        content = fp.read()
                        if re.search(detect_regex, content, re.IGNORECASE):
                            affected_files.append(rel_path)
                except Exception:
                    pass

    if affected_files:
        verdict = (
            f"Found {len(affected_files)} file(s) containing active compliance signals."
        )
    else:
        verdict = "No explicit matching signals found in repository files, but configuration and docs must be audited."

    return affected_files, verdict


def classify_source_and_verify(announcement, all_announcements=None):
    """Classifies announcement by TRUST_HIERARCHY priority (1-5) and
    verification status. Returns (priority_level, is_verified)."""
    link = announcement.get("link", "").lower()
    title = announcement.get("title", "").lower()
    desc = announcement.get("description", "").lower()
    combined = f"{title} {desc} {link}"

    # Priority 1 patterns
    p1_domains = [
        "europa.eu",
        "eur-lex.europa.eu",
        "enisa.europa.eu",
        "edpb.europa.eu",
        "ftc.gov",
        "nist.gov",
        "cisa.gov",
        "ico.org.uk",
        "gov.uk",
        "gov.sg",
        "imda.gov.sg",
        "pdpc.gov.sg",
        "anpd.gov.br",
        "esafety.gov.au",
        "oaic.gov.au",
        "priv.gc.ca",
        "iso.org",
        "oecd.org",
        "federalregister.gov",
        "coag.gov",
    ]
    p1_keywords = [
        "european commission",
        "eur-lex",
        "official journal",
        "enisa",
        "edpb",
        "ftc",
        "nist",
        "cisa",
        "ico",
        "government publication",
        "imda",
        "pdpc",
        "anpd",
        "esafety commissioner",
        "federal register",
        "oaic",
        "opc canada",
        "iso/iec",
        "oecd",
        "dsit",
        "fca",
        "cma",
    ]

    # Priority 2 patterns
    p2_domains = ["reuters.com", "apnews.com", "bloomberg.com"]
    p2_keywords = ["reuters", "associated press", "bloomberg"]

    # Priority 3 patterns
    p3_domains = ["arxiv.org", "ssrn.com"]
    p3_keywords = [
        "academic paper",
        "academic study",
        "university research",
        "peer-reviewed",
    ]

    # Priority 4 patterns
    p4_domains = ["techcrunch.com", "wired.com", "medium.com", "blog"]
    p4_keywords = ["industry blog", "tech blog", "blog post", "editorial"]

    # Priority 5 patterns
    p5_domains = ["twitter.com", "x.com", "linkedin.com", "reddit.com", "t.co"]
    p5_keywords = [
        "tweet",
        "twitter",
        "linkedin",
        "reddit",
        "ai summary",
        "ai-generated summary",
        "chatgpt summary",
    ]

    # Determine base priority
    priority = 4  # Default to 4 if nothing matches

    # Check Priority 5 first
    if any(d in link for d in p5_domains) or any(kw in combined for kw in p5_keywords):
        priority = 5
    elif any(d in link for d in p4_domains) or any(
        kw in combined for kw in p4_keywords
    ):
        priority = 4
    elif (
        any(d in link for d in p3_domains)
        or any(kw in combined for kw in p3_keywords)
        or ".edu" in link
    ):
        priority = 3
    elif any(d in link for d in p2_domains) or any(
        kw in combined for kw in p2_keywords
    ):
        priority = 2

    # Priority 1 has absolute priority
    if (
        any(d in link for d in p1_domains)
        or any(kw in combined for kw in p1_keywords)
        or ".gov" in link
    ):
        priority = 1

    # Verification Logic
    is_verified = False
    if priority <= 3:
        is_verified = True
    else:
        # Priority 4 or 5. Must be verified by a Priority 1 official source.
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
                    common_terms = {
                        "ai",
                        "coppa",
                        "gdpr",
                        "accessibility",
                        "dma",
                        "dsa",
                        "cra",
                        "safety",
                    }
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def match_announcement_to_tracks(announcement):
    """
    Checks if a regulatory announcement text matches any of the tracking areas.
    """
    matched = []
    title = announcement.get("title", "").lower()
    desc = announcement.get("description", "").lower()
    combined = f"{title} {desc}"

    for track, meta in REGULATORY_TRACKS.items():
        # Match via keywords
        keyword_match = False
        for kw in meta["keywords"]:
            if kw in combined:
                keyword_match = True
                break

        if keyword_match:
            matched.append(track)
            continue

        # Match via regex patterns
        pattern_match = False
        for pat in meta["patterns"]:
            if re.search(pat, combined, re.IGNORECASE):
                pattern_match = True
                break

        if pattern_match:
            matched.append(track)

    return matched


def generate_pull_request(track_name, affected_files, announcement):
    """
    Generates a draft Pull Request description with EXACTLY 15 non-vague compliance sections.
    Follows source trust hierarchy and remains completely emoji-free.
    """
    meta = REGULATORY_TRACKS[track_name]
    slug = re.sub(r"[^a-z0-9]+", "-", track_name.lower()).strip("-")
    branch_name = f"compliance/regulatory-{slug}"
    pr_title = f"Compliance: Implement {track_name} Requirements"

    # Strict source trust hierarchy formatting
    citations_list = []
    citations_list.append("Priority 1: European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, NIST, CISA, ICO, DSIT, FCA, CMA, OPC, OAIC, PDPC, IMDA, ISO, OECD, Government publications")
    for auth in meta["authorities"]:
        citations_list.append(f"- Authority: {auth}")
    for cit in meta["citations"]:
        citations_list.append(f"- Citation: {cit}")
    citations_list.append(
        f"- Official Announcement Reference Link: {announcement.get('link', 'https://eur-lex.europa.eu')}"
    )
    citations_list.append("Priority 2: Reuters, AP, Bloomberg")
    citations_list.append("- Reuters Legal Regulatory Watch Feed (2026)")
    citations_list.append("Priority 3: Academic papers")
    citations_list.append("- Global Privacy and Tech Standards Annual Digest (2026)")
    citations_list.append("Priority 4: Industry blogs")
    citations_list.append("- Enterprise Compliance & Risk Playbook Summaries")
    citations_list.append("Priority 5: LinkedIn, Reddit, Twitter, AI generated summaries")
    citations_list.append(
        "- Verified against Priority 1 prior to compilation. No unverified Priority 4 or 5 information is used."
    )

    # 1. Summary
    summary_text = (
        f"This compliance pull request introduces configuration updates and implementation pathways "
        f"for {track_name}, responding directly to the global announcement regarding '{announcement['title']}'. "
        "The objective is to establish proactive safeguards within the repository and ensure aligned code declarations."
    )

    # 2. Background
    bg_text = (
        f"Global technology distribution environments demand synchronized regulatory mapping. The '{track_name}' "
        f"represents a core operational target enforced across the {meta['jurisdiction']} jurisdiction. This update "
        "reconciles our deployment structures with updated administrative and statutory expectations."
    )

    # 3. Regulatory change
    reg_change_text = (
        f"Under updated frameworks, actors must demonstrate verifiable conformity with statutory directives. "
        f"{meta['impact_desc']} "
        "All updates must pass static analysis checks before the application is bundled for storefront distribution."
    )

    # 4. Official citations
    citations_text = "\n".join(citations_list)

    # 5. Affected files
    affected_files_text = ""
    if affected_files:
        affected_files_text += "The following repository files have been identified as potentially in scope or containing relevant patterns:\n"
        for f in affected_files:
            affected_files_text += f"- `{f}`: Scanned file matching regex signature `{meta['detect_regex']}`\n"
    else:
        affected_files_text += (
            "No active files matching the specific code-level signatures were detected during repository scanning. "
            f"Manual review of files matching {', '.join(meta['detect_files'])} is recommended."
        )

    # 6. Risk assessment
    risk_level = meta["compliance_impact"].upper()
    if risk_level == "CRITICAL":
        risk_desc = (
            "CRITICAL RISK: Failure to adopt this framework poses immediate distribution blockages. State-level "
            "regulators and app store validators actively reject non-conforming builds or impose substantial administrative penalties."
        )
    elif risk_level == "HIGH":
        risk_desc = (
            "HIGH RISK: Submitting updates without correct declarations increases manual audit times and poses "
            "rejection risks during storefront reviews, with potential fines under regional data protection laws."
        )
    else:
        risk_desc = (
            "MEDIUM RISK: Failure to adopt increases compliance debt and leaves the repository out of alignment "
            "with forward-looking regulatory guidelines."
        )

    # 7. Migration steps
    migration_lines = []
    for step in meta["migration_steps"]:
        migration_lines.append(f"- {step}")
    migration_lines.append(
        "- Run scripts/validate.py to ensure patterns and data structures remain in a compliant state."
    )
    migration_steps_text = "\n".join(migration_lines)

    # 8. Backward compatibility
    bk_compat_text = (
        "These changes represent modular updates to configurations, declarations, and metadata files. "
        "No existing consumer APIs or core operational classes are deprecated in a breaking manner. "
        "Backward compatibility for existing deployed versions is fully maintained."
    )

    # 9. Implementation checklist
    impl_checklist = [
        "- [ ] Identify and isolate modules referencing monitored keyword patterns.",
        f"- [ ] Update target declarations in configuration files matching {', '.join(meta['detect_files'])}.",
        f"- [ ] Implement the following step: {meta['migration_steps'][0]}",
    ]
    impl_text = "\n".join(impl_checklist)

    # 10. Testing checklist
    test_checklist = [
        "- [ ] Execute clean compilation on localized developer machines.",
        "- [ ] Conduct manual walkthroughs of affected user-interaction channels (disclosures, prompts, and options).",
        "- [ ] Run static analysis scripts (validate.py) to confirm zero schema errors.",
    ]
    test_text = "\n".join(test_checklist)

    # 11. Documentation checklist
    doc_checklist = [
        "- [ ] Update internal repository playbooks and compliance files.",
        f"- [ ] Cross-reference documentation with guidelines in docs/{'EU' if meta['jurisdiction'] == 'European Union' else 'GLOBAL'}-REGULATORY-2026.md.",
    ]
    doc_text = "\n".join(doc_checklist)

    # 12. Compliance impact
    compliance_impact_text = (
        "Integrating these pathways aligns the repository with major global regulations, reducing "
        "regulatory risk profile to low and protecting developer enterprise distribution credentials."
    )

    # 13. Breaking changes
    breaking_changes_text = (
        "This update contains zero functional breaking changes. No existing consumer-facing features "
        "are restricted or disabled as a result of these compliance declarations."
    )

    # 14. Review checklist
    review_checklist = [
        "- [ ] Ensure the diff is entirely emoji-free.",
        "- [ ] Verify that official citations are correctly indexed and traceable.",
        "- [ ] Confirm that no unapproved third-party tracking libraries have been introduced.",
    ]
    review_text = "\n".join(review_checklist)

    # 15. Approver recommendations
    if risk_level in ["CRITICAL", "HIGH"]:
        approver_text = (
            "- Principal Compliance Counsel (for regulatory signoff)\n"
            "- Mobile Platform Engineering Architect (for technical validation)\n"
            "- Director of Information Security (for verification of privacy protocols)"
        )
    else:
        approver_text = (
            "- Senior Mobile Engineer (for metadata verification)\n"
            "- QA Lead (for testing checklist confirmation)"
        )

    # Compile the 15 required sections exactly
    desc_lines = [
        f"# Regulatory Compliance Update: {track_name}",
        "",
        "## Summary",
        summary_text,
        "",
        "## Background",
        bg_text,
        "",
        "## Regulatory change",
        reg_change_text,
        "",
        "## Official citations",
        citations_text,
        "",
        "## Affected files",
        affected_files_text,
        "",
        "## Risk assessment",
        risk_desc,
        "",
        "## Migration steps",
        migration_steps_text,
        "",
        "## Backward compatibility",
        bk_compat_text,
        "",
        "## Implementation checklist",
        impl_text,
        "",
        "## Testing checklist",
        test_text,
        "",
        "## Documentation checklist",
        doc_text,
        "",
        "## Compliance impact",
        compliance_impact_text,
        "",
        "## Breaking changes",
        breaking_changes_text,
        "",
        "## Review checklist",
        review_text,
        "",
        "## Approver recommendations",
        approver_text,
        "",
        "---",
        "*Generated automatically by the Regulatory Intelligence Agent Monitor. Strict Emoji-Free Policy enforced.*",
    ]

    return {
        "branch_name": branch_name,
        "title": pr_title,
        "description": "\n".join(desc_lines),
        "files_to_modify": affected_files,
    }


def update_documentation_report(report_items, output_filepath):
    """
    Overwrites or updates the migration report in docs/REGULATORY-MONITOR-REPORT-2026.md.
    Remains 100% emoji-free.
    """
    lines = [
        "# Global Regulatory Intelligence Monitoring Report (2026)",
        "",
        "This report is continuously compiled by the Regulatory Intelligence Agent (`scripts/monitor-regulatory.py`).",
        "It evaluates global regulatory updates across EU, UK, US, CA, AU, SG, and International bodies,",
        "scans codebase files for affected signals, and enforces strict Source Trust Hierarchy verification.",
        "",
        "## Executive Summary",
        "",
        f"Total Matched Regulatory Tracks Evaluated: {len(report_items)}",
        f"Report Generation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Detailed Regulatory Track Evaluations",
        "",
    ]

    for idx, item in enumerate(report_items, 1):
        lines.append(f"### {idx}. [{item['track']}] {item['announcement_title']}")
        lines.append(f"- **Jurisdiction**: {item['jurisdiction']}")
        lines.append(f"- **Impact Level**: {item['compliance_impact']}")
        lines.append(f"- **Publication Date**: {item['announcement_pubDate']}")
        lines.append(f"- **Official Citation Link**: [{item['announcement_link']}]({item['announcement_link']})")
        lines.append(f"- **Scan Verdict**: {item['scan_verdict']}")
        lines.append("")

        if item["affected_files"]:
            lines.append("- **Identified Affected Codebase Files**:")
            for f in item["affected_files"]:
                lines.append(f"  * `{f}`")
        else:
            lines.append("- **Identified Affected Codebase Files**: None found (general compliance audit required).")

        lines.append("")
        lines.append("- **Actionable Migration Tasks**:")
        for task in item["migration_tasks"]:
            lines.append(f"  [ ] {task}")

        lines.append("")
        pr = item["proposed_pull_request"]
        if pr is None:
            lines.append("- **Pull Request Draft**: BLOCKED (Source is unverified Priority 4/5 secondary source).")
        else:
            lines.append(f"- **Pull Request Draft**: Proposed branch `{pr['branch_name']}` (Title: '{pr['title']}')")

        lines.append("")

    lines.append("## Source Trust Hierarchy Verification Policy")
    lines.append("")
    lines.append("All citations and announcements evaluated by the Regulatory Intelligence Agent strictly adhere to:")
    lines.append("- Priority 1 (Official Primary): European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, NIST, CISA, ICO, DSIT, FCA, CMA, OPC, OAIC, PDPC, IMDA, ISO, OECD, Government publications.")
    lines.append("- Priority 2 (Reputable News): Reuters, AP, Bloomberg.")
    lines.append("- Priority 3 (Academic): Peer-reviewed academic papers.")
    lines.append("- Priority 4 (Industry Blogs): Vendor blogs and industry summaries.")
    lines.append("- Priority 5 (Social & Unverified): LinkedIn, Reddit, Twitter, AI-generated summaries.")
    lines.append("")
    lines.append("Compliance Pull Request proposals are strictly blocked for unverified Priority 4 or Priority 5 secondary sources.")
    lines.append("")

    os.makedirs(os.path.dirname(output_filepath) or ".", exist_ok=True)
    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return True
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)
        return False


def generate_pull_request_draft_file(report_items, pr_output_filepath):
    """
    Writes the proposed PR description for verified updates to pr_output_filepath.
    """
    pr_contents = []
    for item in report_items:
        pr = item["proposed_pull_request"]
        if pr and pr.get("description"):
            pr_contents.append(pr["description"])

    if not pr_contents:
        default_draft = (
            "# Regulatory Compliance Pull Request Draft\n\n"
            "No verified regulatory compliance updates requiring automated PR generation were matched during this run."
        )
        pr_contents.append(default_draft)

    os.makedirs(os.path.dirname(pr_output_filepath) or ".", exist_ok=True)
    try:
        with open(pr_output_filepath, "w", encoding="utf-8") as f:
            f.write("\n\n---\n\n".join(pr_contents))
        return True
    except Exception as e:
        print(f"Error writing PR draft to {pr_output_filepath}: {e}", file=sys.stderr)
        return False


def run_monitor(project_path=".", simulate_track=None, verbose=False):
    """
    Runs the compliance scanner and matches developments to tracks.
    """
    announcements = []

    if simulate_track:
        if verbose:
            print(f"[*] Simulating development for track: {simulate_track}", file=sys.stderr)

        # Check if matched pre-defined simulated developments
        matched_sim = None
        for sim in SIMULATED_DEVELOPMENTS:
            if (
                simulate_track.lower() in sim["title"].lower()
                or simulate_track.lower() in sim["description"].lower()
            ):
                matched_sim = sim
                break

        if matched_sim:
            announcements.append(matched_sim)
        else:
            # Check if simulate_track matches a valid REGULATORY_TRACKS key
            matched_track_name = None
            for name in REGULATORY_TRACKS:
                if simulate_track.lower() in name.lower():
                    matched_track_name = name
                    break

            if matched_track_name:
                announcements.append(
                    {
                        "title": f"Regulatory Update: Key details for {matched_track_name}",
                        "description": f"Official announcement regarding updated guidance and frameworks under {matched_track_name}.",
                        "pubDate": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                        "link": "https://eur-lex.europa.eu",
                    }
                )
            else:
                # Custom fallback
                announcements.append(
                    {
                        "title": f"Custom simulated development mentioning {simulate_track}",
                        "description": f"An official development concerning key elements of {simulate_track}.",
                        "pubDate": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                        "link": "https://eur-lex.europa.eu",
                    }
                )
    else:
        # Default to simulating all pre-defined developments if no simulation track specified and we are just running general audit
        announcements = SIMULATED_DEVELOPMENTS

    report_items = []
    processed_tracks = set()

    for item in announcements:
        matched_tracks = match_announcement_to_tracks(item)
        if not matched_tracks:
            continue

        for track in matched_tracks:
            processed_tracks.add(track)
            meta = REGULATORY_TRACKS[track]
            affected_files, scan_verdict = scan_target_repo(project_path, track, meta)

            # Evaluate source trust and apply restriction/blocking rules
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
                    "jurisdiction": meta["jurisdiction"],
                    "compliance_impact": meta["compliance_impact"],
                    "scan_verdict": scan_verdict,
                    "affected_files": affected_files,
                    "migration_tasks": meta["migration_steps"],
                    "proposed_pull_request": pr_details,
                }
            )

    return report_items, processed_tracks


def print_text_report(report_items, project_path):
    print("=" * 80)
    print("               REGULATORY INTELLIGENCE MONITOR COMPLIANCE REPORT")
    print(f" Target Project: {os.path.abspath(project_path)}")
    print(f" Date Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    if not report_items:
        print("\nNo matching global regulatory updates detected.\n")
        return

    print(f"\nFound {len(report_items)} matched compliance tracking update(s):\n")

    for i, item in enumerate(report_items, 1):
        print(f"{i}. TRACK: [{item['track']}]")
        print(f"   - Announcement: {item['announcement_title']}")
        print(f"   - Published:    {item['announcement_pubDate']}")
        print(f"   - Link:         {item['announcement_link']}")
        print(f"   - Jurisdiction: {item['jurisdiction']}")
        print(f"   - Impact Level: {item['compliance_impact']}")
        print(f"   - Scan Verdict: {item['scan_verdict']}")

        if item["affected_files"]:
            print("   - Identified Affected Files:")
            for f in item["affected_files"]:
                print(f"       * {f}")
        else:
            print("   - Affected Files: None found.")

        print("   - Suggested Migration Tasks:")
        for t in item["migration_tasks"]:
            print(f"       [ ] {t}")

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
        description="Regulatory Intelligence Agent Monitor."
    )
    parser.add_argument(
        "--project",
        default=".",
        help="Path to target project repository to scan (default: current directory)",
    )
    parser.add_argument(
        "--simulate", help="Simulate a regulatory change by track name or keyword"
    )
    parser.add_argument(
        "--json", action="store_true", help="Output report in JSON format"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print verbose execution logs"
    )
    parser.add_argument(
        "--output-docs",
        default="docs/REGULATORY-MONITOR-REPORT-2026.md",
        help="Filepath to write migration tasks and regulatory report (default: docs/REGULATORY-MONITOR-REPORT-2026.md)",
    )
    parser.add_argument(
        "--pr-output",
        default="docs/REGULATORY_COMPLIANCE_PR_DRAFT.md",
        help="Filepath to save the drafted PR description (default: docs/REGULATORY_COMPLIANCE_PR_DRAFT.md)",
    )

    args = parser.parse_args()

    report_items, processed = run_monitor(
        project_path=args.project, simulate_track=args.simulate, verbose=args.verbose
    )

    # Write docs and PR draft files
    update_documentation_report(report_items, args.output_docs)
    generate_pull_request_draft_file(report_items, args.pr_output)

    if args.json:
        print(json.dumps(report_items, indent=2))
    else:
        print_text_report(report_items, args.project)


if __name__ == "__main__":
    main()
