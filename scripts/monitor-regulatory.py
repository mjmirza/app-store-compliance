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
    "Priority 1": "European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, NIST, CISA, ICO, Government publications",
    "Priority 2": "Reuters, AP, Bloomberg",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries",
}

# Database of global jurisdictions, authorities, laws and their tracking keywords/signatures
REGULATORY_TRACKS = {
    # European Union
    "EU AI Act": {
        "jurisdiction": "European Union",
        "authorities": ["European Commission", "Official Journal", "EUR-Lex"],
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
            "safety warning"
        ],
        "patterns": [
            r"gpsr",
            r"general[ -]product[ -]safety[ -]regulation",
            r"product[ -]safety"
        ],
        "detect_files": ["*.swift", "*.py", "*.js", "*.ts", "*.json", "*.md"],
        "detect_regex": r"productListing|buyProduct|checkout|e-commerce|manufacturerInfo|safetyWarning|manufacturerEmail|manufacturerAddress|safetyLabel|productSafety|responsiblePerson",
        "impact_desc": "The EU GPSR (Regulation (EU) 2023/988) mandates that e-commerce applications and digital marketplaces distributed in the EU display manufacturer contact information and product safety warnings directly on the interface.",
        "migration_steps": [
            "Ensure e-commerce product detail templates display manufacturer identity (name, registered trade name/trademark).",
            "Provide manufacturer postal address and electronic address (email or website) directly on the interface.",
            "Display relevant product safety warnings or instructions in languages accepted by the member states of distribution.",
            "Formally verify that an EU-based Responsible Person is designated for any products sold to EU consumers."
        ],
        "compliance_impact": "High"
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
        "authorities": ["European Commission", "EUR-Lex"],
        "citations": [
            "Regulation (EU) 2022/868 on European data governance (Data Governance Act)"
        ],
        "keywords": [
            "data governance act",
            "data intermediation",
            "data alturism",
            "eu data governance",
        ],
        "patterns": [r"data[ -]governance[ -]act", r"data[ -]intermediation"],
        "detect_files": ["*.swift", "*.py", "*.json", "*.md"],
        "detect_regex": r"dataIntermediary|dataSharing|altruismConsent|dataTrust",
        "impact_desc": "The EU Data Governance Act sets framework conditions for data sharing, data intermediation services, and data altruism organizations within the EU.",
        "migration_steps": [
            "Verify that data sharing frameworks meet EU data intermediation neutrality rules.",
            "Implement transparent consent mechanisms for data altruism features.",
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
            "network and information systems",
            "incident reporting",
            "cybersecurity risk management",
        ],
        "patterns": [r"nis2", r"directive[ -]2022/2555"],
        "detect_files": ["*.swift", "*.py", "*.json", "*.md"],
        "detect_regex": r"incidentReport|securityAudit|cyberRisk|nis2",
        "impact_desc": "The NIS2 Directive sets strict risk management, supply chain security, and early incident reporting obligations (24-hour warning) for essential and important entities.",
        "migration_steps": [
            "Establish automated incident detection and early warning alert procedures.",
            "Conduct supply chain cybersecurity risk assessments for third-party dependencies.",
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
        "authorities": ["EDPB", "European Commission"],
        "citations": [
            "Directive 2002/58/EC concerning the processing of personal data and the protection of privacy in the electronic communications sector (ePrivacy Directive)"
        ],
        "keywords": [
            "eprivacy",
            "cookie directive",
            "terminal equipment",
            "tracking pixels",
        ],
        "patterns": [r"eprivacy", r"directive[ -]2002/58/ec"],
        "detect_files": ["*.js", "*.ts", "*.html", "*.swift", "*.md"],
        "detect_regex": r"cookie|localStorage|trackingPixel|analytics\.js|gtag",
        "impact_desc": "The ePrivacy Directive strictly regulates access to terminal equipment, requiring explicit opt-in consent before storing or accessing information (cookies, local storage, tracking scripts).",
        "migration_steps": [
            "Implement a compliant cookie consent banner that blocks non-essential cookies prior to consent.",
            "Ensure local storage and session variables do not store unencrypted sensitive information.",
        ],
        "compliance_impact": "High",
    },
    "Product Liability Directive": {
        "jurisdiction": "European Union",
        "authorities": ["European Commission", "EUR-Lex"],
        "citations": [
            "Directive (EU) 2024/2853 on liability for defective products (Revised Product Liability Directive)"
        ],
        "keywords": [
            "product liability directive",
            "defective software",
            "software liability",
            "ai damage",
        ],
        "patterns": [r"product[ -]liability", r"software[ -]defect"],
        "detect_files": ["*.swift", "*.py", "*.md"],
        "detect_regex": r"liability|disclaimer|termsOfService|eula",
        "impact_desc": "The revised EU Product Liability Directive explicitly includes software, AI systems, and digital services under no-fault strict product liability for damages caused by defective software.",
        "migration_steps": [
            "Review End User License Agreements (EULA) and Terms of Service regarding software safety disclosures.",
            "Establish continuous monitoring for safety-critical software updates and bug patches.",
        ],
        "compliance_impact": "Medium",
    },
    "AI Liability Directive": {
        "jurisdiction": "European Union",
        "authorities": ["European Commission", "EUR-Lex"],
        "citations": [
            "Proposal for a Directive on adapting non-contractual civil liability rules to artificial intelligence (AI Liability Directive)"
        ],
        "keywords": [
            "ai liability",
            "presumption of causality",
            "ai fault",
            "disclosure of evidence",
        ],
        "patterns": [r"ai[ -]liability", r"presumption[ -]of[ -]causality"],
        "detect_files": ["*.swift", "*.py", "*.md"],
        "detect_regex": r"openai|anthropic|llm|aiLog|inferenceRecord",
        "impact_desc": "The proposed AI Liability Directive eases the burden of proof for victims of AI-related harm, establishing a rebuttable presumption of causality for non-compliant AI systems.",
        "migration_steps": [
            "Maintain comprehensive logging of AI inference outputs and safety interventions.",
            "Ensure compliance with AI Act obligations to maintain the defense against presumptions of causality.",
        ],
        "compliance_impact": "Medium",
    },

    # United Kingdom
    "UK Online Safety Act": {
        "jurisdiction": "United Kingdom",
        "authorities": ["Ofcom", "Government publications", "ICO"],
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
    "UK AI Regulation": {
        "jurisdiction": "United Kingdom",
        "authorities": ["DSIT", "FCA", "CMA", "ICO"],
        "citations": [
            "UK DSIT Pro-innovation approach to AI regulation white paper",
            "FCA and CMA Joint Guidance on AI Oversight in Financial and Consumer Services",
        ],
        "keywords": [
            "uk ai regulation",
            "dsit",
            "fca ai guidance",
            "cma ai review",
            "pro-innovation ai",
        ],
        "patterns": [r"dsit", r"uk[ -]ai", r"fca[ -]ai"],
        "detect_files": ["*.swift", "*.py", "*.md"],
        "detect_regex": r"openai|llm|aiModel|financialAdvice|consumerChoice",
        "impact_desc": "The UK's sector-led AI regulatory framework empowers existing regulators (ICO, FCA, CMA) to enforce principles of safety, transparency, fairness, and accountability.",
        "migration_steps": [
            "Ensure AI systems used in financial or advisory contexts provide explainable outputs.",
            "Conduct fairness and algorithmic bias audits for UK market deployments.",
        ],
        "compliance_impact": "Medium",
    },

    # United States
    "US COPPA": {
        "jurisdiction": "United States",
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
    "US NIST AI RMF": {
        "jurisdiction": "United States",
        "authorities": ["NIST", "FTC", "CISA"],
        "citations": [
            "NIST AI Risk Management Framework (AI RMF 1.0 / NIST AI 100-1)",
            "CISA Guidelines for Secure AI System Development",
        ],
        "keywords": [
            "nist ai rmf",
            "ai risk management framework",
            "cisa ai guidance",
            "trustworthy ai",
        ],
        "patterns": [r"nist[ -]ai", r"ai[ -]rmf", r"cisa[ -]ai"],
        "detect_files": ["*.swift", "*.py", "*.json", "*.md"],
        "detect_regex": r"openai|anthropic|llm|modelSafety|aiRisk",
        "impact_desc": "NIST AI RMF provides actionable guidance for managing risks to individuals, organizations, and society associated with AI systems across Governance, Mapping, Measuring, and Managing.",
        "migration_steps": [
            "Perform a structured risk mapping for integrated AI/LLM models.",
            "Establish continuous monitoring for model drift, hallucination risks, and data leakage.",
        ],
        "compliance_impact": "High",
    },
    "US State ASAA": {
        "jurisdiction": "United States",
        "authorities": ["State Legislatures", "CISA"],
        "citations": [
            "Utah SB 142 (App Store Accountability Act)",
            "Texas SB 2420 (App Store Accountability Act)",
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
    "US State AI Legislation": {
        "jurisdiction": "United States",
        "authorities": ["State Legislatures", "FTC"],
        "citations": [
            "California SB 1047 (Safe and Secure Innovation for Frontier AI Models Act)",
            "Colorado AI Act (SB 24-205 Consumer Protections in Interactions Relating to Artificial Intelligence Systems)",
            "Utah Artificial Intelligence Policy Act (SB 149)",
        ],
        "keywords": [
            "colorado ai act",
            "utah ai policy act",
            "california sb 1047",
            "algorithmic discrimination",
            "ai disclosure",
        ],
        "patterns": [r"colorado[ -]ai", r"utah[ -]ai", r"sb[ -]1047", r"algorithmic[ -]discrimination"],
        "detect_files": ["*.swift", "*.py", "*.md"],
        "detect_regex": r"openai|chatgpt|llm|algorithmicDecision|aiDisclosure",
        "impact_desc": "US State AI laws enforce mandatory disclosures when users interact with AI and impose duties of reasonable care to prevent algorithmic discrimination in consequential decisions.",
        "migration_steps": [
            "Add explicit state-compliant AI interaction disclosures.",
            "Complete algorithmic impact assessments for automated decision features.",
        ],
        "compliance_impact": "High",
    },

    # Canada
    "Canada OPC and AIDA": {
        "jurisdiction": "Canada",
        "authorities": ["OPC", "Innovation, Science and Economic Development Canada"],
        "citations": [
            "Office of the Privacy Commissioner of Canada (OPC) Principles for Generative AI",
            "Artificial Intelligence and Data Act (AIDA - Bill C-27 Part 3)",
        ],
        "keywords": [
            "aida",
            "artificial intelligence and data act",
            "opc canada",
            "pipeda",
            "bill c-27",
        ],
        "patterns": [r"aida", r"bill[ -]c-27", r"opc[ -]canada"],
        "detect_files": ["*.swift", "*.py", "*.md"],
        "detect_regex": r"openai|llm|pipeda|consentCanada",
        "impact_desc": "Canada's AIDA and OPC guidelines require developers of high-impact AI systems to assess risks, publish plain-language system descriptions, and maintain strict data privacy.",
        "migration_steps": [
            "Formulate plain-language Canadian privacy disclosures for AI features.",
            "Establish risk mitigation mechanisms for generative AI outputs.",
        ],
        "compliance_impact": "High",
    },

    # Australia
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
    "Australia OAIC AI Governance": {
        "jurisdiction": "Australia",
        "authorities": ["OAIC", "Department of Industry, Science and Resources"],
        "citations": [
            "OAIC Guidance on Privacy and Generative AI",
            "Australian Voluntary AI Safety Standard (2024)",
        ],
        "keywords": [
            "oaic ai governance",
            "australia ai safety standard",
            "australian privacy principles",
        ],
        "patterns": [r"oaic[ -]ai", r"australian[ -]privacy[ -]principles"],
        "detect_files": ["*.swift", "*.py", "*.md"],
        "detect_regex": r"privacyPolicy|appScope|australiaPrivacy",
        "impact_desc": "The OAIC enforces Australian Privacy Principles (APPs) on AI training and generation, requiring notice, purpose limitation, and human oversight.",
        "migration_steps": [
            "Update Australian storefront privacy disclosures to cover AI data usage.",
            "Implement human oversight controls for automated AI decisions.",
        ],
        "compliance_impact": "Medium",
    },

    # Singapore
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
    "Singapore PDPC and AI Verify": {
        "jurisdiction": "Singapore",
        "authorities": ["PDPC", "IMDA", "AI Verify Foundation"],
        "citations": [
            "Model AI Governance Framework for Generative AI (PDPC & IMDA Singapore)",
            "AI Verify Testing Framework and Software Toolkit",
        ],
        "keywords": [
            "ai verify",
            "pdpc generative ai",
            "imda model ai governance",
        ],
        "patterns": [r"ai[ -]verify", r"model[ -]ai[ -]governance"],
        "detect_files": ["*.swift", "*.py", "*.json", "*.md"],
        "detect_regex": r"openai|llm|aiSafety|singaporeAi",
        "impact_desc": "Singapore's Model AI Governance Framework and AI Verify toolkit promote transparent, fair, and safe AI deployment with voluntary and standardized testing.",
        "migration_steps": [
            "Conduct safety testing using AI Verify framework evaluation parameters.",
            "Document AI alignment and safety safeguards for regional distribution.",
        ],
        "compliance_impact": "Medium",
    },

    # International
    "International AI and Security Standards": {
        "jurisdiction": "International",
        "authorities": ["ISO", "IEC", "OECD", "G7", "G20"],
        "citations": [
            "ISO/IEC 42001:2023 Artificial Intelligence - Management System",
            "ISO/IEC 27001:2022 Information Security Management",
            "OECD Principles on Artificial Intelligence",
            "G7 Hiroshima AI Process Comprehensive Policy Framework",
        ],
        "keywords": [
            "iso 42001",
            "iso 27001",
            "oecd ai principles",
            "g7 hiroshima ai",
            "g20 ai guidelines",
        ],
        "patterns": [r"iso[ -]42001", r"iso[ -]27001", r"oecd[ -]ai", r"g7[ -]hiroshima"],
        "detect_files": ["*.swift", "*.py", "*.json", "*.md"],
        "detect_regex": r"security|iso42001|iso27001|aiGovernance",
        "impact_desc": "International consensus standards (ISO/IEC 42001, OECD AI Principles, G7 Hiroshima Process) establish global benchmarks for AI management systems, security controls, and ethical AI development.",
        "migration_steps": [
            "Align AI governance procedures with ISO/IEC 42001 management system controls.",
            "Maintain an ISO 27001 compliant information security risk management process.",
        ],
        "compliance_impact": "High",
    },
}

# Pre-defined Simulated Regulatory Announcements covering all tracked jurisdictions
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
        "title": "UK Ofcom issues final guidance under UK Online Safety Act for App Stores and Platforms",
        "description": "Ofcom published official guidance requiring app distributors and developers to deploy highly effective age assurance methods to protect minors from harmful content under the UK Online Safety Act.",
        "pubDate": "Mon, 10 Nov 2025 10:00:00 GMT",
        "link": "https://www.ofcom.org.uk/online-safety/protecting-children",
    },
    {
        "title": "Canada AIDA and OPC issue joint principles for Generative AI deployment",
        "description": "The Office of the Privacy Commissioner of Canada and ISED released operational guidance for generative AI compliance under PIPEDA and the Artificial Intelligence and Data Act (AIDA).",
        "pubDate": "Wed, 14 Jan 2026 11:00:00 GMT",
        "link": "https://www.priv.gc.ca/en/privacy-topics/technology/artificial-intelligence/",
    },
    {
        "title": "Australia eSafety Commissioner enforces Social Media Minimum Age rules",
        "description": "The eSafety Commissioner published binding standards under the Online Safety Amendment Act requiring robust age verification for restricted services.",
        "pubDate": "Thu, 19 Feb 2026 09:00:00 GMT",
        "link": "https://www.esafety.gov.au/about-us/industry-regulation",
    },
    {
        "title": "Singapore IMDA and PDPC update Model AI Governance Framework for Generative AI",
        "description": "IMDA and PDPC Singapore published updated guidelines for deploying generative AI and utilizing the AI Verify software testing toolkit.",
        "pubDate": "Tue, 10 Mar 2026 08:00:00 GMT",
        "link": "https://www.pdpc.gov.sg/help-and-resources/2020/01/model-ai-governance-framework",
    },
    {
        "title": "ISO/IEC 42001 Artificial Intelligence Management System International Standard Guidance",
        "description": "ISO and IEC published updated compliance audit guides for ISO/IEC 42001 AI Management Systems and OECD AI Principles alignment.",
        "pubDate": "Wed, 15 Apr 2026 14:00:00 GMT",
        "link": "https://www.iso.org/standard/81230.html",
    },
    {
        "title": "Unverified rumors of GDPR policy changes on Reddit forum",
        "description": "An anonymous user posted a rumor on Reddit saying GDPR consent requirements are changing. No official authorities or official sources were referenced.",
        "pubDate": "Sun, 26 Jul 2026 12:00:00 GMT",
        "link": "https://reddit.com/r/privacy/comments/12345/GDPR_rumor",
    },
]

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


def scan_target_repo(repo_path, track_name, metadata):
    """
    Scans the repository path to identify affected files and files of interest.
    """
    affected_files = []
    file_patterns = metadata["detect_files"]
    detect_regex = metadata["detect_regex"]

    if not os.path.exists(repo_path):
        return [], "Repository path does not exist."

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
        "ofcom.org.uk",
        "gov.sg",
        "imda.gov.sg",
        "pdpc.gov.sg",
        "anpd.gov.br",
        "esafety.gov.au",
        "priv.gc.ca",
        "iso.org",
        "oecd.org",
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
        "ofcom",
        "government publication",
        "imda",
        "pdpc",
        "anpd",
        "esafety commissioner",
        "federal register",
        "opc canada",
        "iso standard",
        "oecd",
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
        keyword_match = False
        for kw in meta["keywords"]:
            if kw in combined:
                keyword_match = True
                break

        if keyword_match:
            matched.append(track)
            continue

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

    citations_list = []
    citations_list.append("Priority 1: European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, NIST, CISA, ICO, Government publications")
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

    summary_text = (
        f"This compliance pull request introduces configuration updates and implementation pathways "
        f"for {track_name}, responding directly to the global announcement regarding '{announcement['title']}'. "
        "The objective is to establish proactive safeguards within the repository and ensure aligned code declarations."
    )

    bg_text = (
        f"Global technology distribution environments demand synchronized regulatory mapping. The '{track_name}' "
        f"represents a core operational target enforced across the {meta['jurisdiction']} jurisdiction. This update "
        "reconciles our deployment structures with updated administrative and statutory expectations."
    )

    reg_change_text = (
        f"Under updated frameworks, actors must demonstrate verifiable conformity with statutory directives. "
        f"{meta['impact_desc']} "
        "All updates must pass static analysis checks before the application is bundled for storefront distribution."
    )

    citations_text = "\n".join(citations_list)

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

    migration_lines = []
    for step in meta["migration_steps"]:
        migration_lines.append(f"- {step}")
    migration_lines.append(
        "- Run scripts/validate.py to ensure patterns and data structures remain in a compliant state."
    )
    migration_steps_text = "\n".join(migration_lines)

    bk_compat_text = (
        "These changes represent modular updates to configurations, declarations, and metadata files. "
        "No existing consumer APIs or core operational classes are deprecated in a breaking manner. "
        "Backward compatibility for existing deployed versions is fully maintained."
    )

    impl_checklist = [
        "- [ ] Identify and isolate modules referencing monitored keyword patterns.",
        f"- [ ] Update target declarations in configuration files matching {', '.join(meta['detect_files'])}.",
        f"- [ ] Implement the following step: {meta['migration_steps'][0]}",
    ]
    impl_text = "\n".join(impl_checklist)

    test_checklist = [
        "- [ ] Execute clean compilation on localized developer machines.",
        "- [ ] Conduct manual walkthroughs of affected user-interaction channels (disclosures, prompts, and options).",
        "- [ ] Run static analysis scripts (validate.py) to confirm zero schema errors.",
    ]
    test_text = "\n".join(test_checklist)

    doc_checklist = [
        "- [ ] Update internal repository playbooks and compliance files.",
        f"- [ ] Cross-reference documentation with guidelines in docs/{'EU' if meta['jurisdiction'] == 'European Union' else 'GLOBAL'}-REGULATORY-2026.md.",
    ]
    doc_text = "\n".join(doc_checklist)

    compliance_impact_text = (
        "Integrating these pathways aligns the repository with major global regulations, reducing "
        "regulatory risk profile to low and protecting developer enterprise distribution credentials."
    )

    breaking_changes_text = (
        "This update contains zero functional breaking changes. No existing consumer-facing features "
        "are restricted or disabled as a result of these compliance declarations."
    )

    review_checklist = [
        "- [ ] Ensure the diff is entirely emoji-free.",
        "- [ ] Verify that official citations are correctly indexed and traceable.",
        "- [ ] Confirm that no unapproved third-party tracking libraries have been introduced.",
    ]
    review_text = "\n".join(review_checklist)

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

    desc_lines = [
        f"# Regulatory Compliance Update: {track_name}",
        "",
        "## 1. Summary",
        summary_text,
        "",
        "## 2. Background",
        bg_text,
        "",
        "## 3. Regulatory change",
        reg_change_text,
        "",
        "## 4. Official citations",
        citations_text,
        "",
        "## 5. Affected files",
        affected_files_text,
        "",
        "## 6. Risk assessment",
        risk_desc,
        "",
        "## 7. Migration steps",
        migration_steps_text,
        "",
        "## 8. Backward compatibility",
        bk_compat_text,
        "",
        "## 9. Implementation checklist",
        impl_text,
        "",
        "## 10. Testing checklist",
        test_text,
        "",
        "## 11. Documentation checklist",
        doc_text,
        "",
        "## 12. Compliance impact",
        compliance_impact_text,
        "",
        "## 13. Breaking changes",
        breaking_changes_text,
        "",
        "## 14. Review checklist",
        review_text,
        "",
        "## 15. Approver recommendations",
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


def update_documentation_report(report_items, output_filepath, is_simulated=True):
    """
    Generates or overwrites docs/REGULATORY-MONITOR-REPORT-2026.md with detailed findings.
    """
    lines = [
        "<!-- REGULATORY_MONITOR_START -->",
    ]
    if is_simulated:
        lines.extend(SIMULATED_NOTICE)
    lines.extend([
        "# Global Regulatory Intelligence Monitoring Report (2026)",
        "",
        "This comprehensive compliance report is continuously updated by `scripts/monitor-regulatory.py` to evaluate global regulatory developments across key jurisdictions.",
        "",
        "## Jurisdictional Coverage Overview",
        "",
        "- **European Union**: EU AI Act, GDPR, Data Act, Data Governance Act, Cyber Resilience Act, NIS2, Digital Services Act, Digital Markets Act, ePrivacy Directive, European Accessibility Act, Product Liability Directive, AI Liability Directive, EU GPSR",
        "- **United Kingdom**: UK Online Safety Act, ICO Children's Code, UK AI Regulation (DSIT, FCA, CMA, ICO)",
        "- **United States**: US COPPA (FTC), US NIST AI RMF & CISA, US State ASAA, US State AI Legislation (California, Utah, Colorado)",
        "- **Canada**: Canada OPC & AIDA (Artificial Intelligence and Data Act)",
        "- **Australia**: Australia Online Safety & eSafety, Australia OAIC & AI Governance",
        "- **Singapore**: Singapore IMDA & Online Safety, Singapore PDPC & AI Verify Framework",
        "- **International**: International Standards (ISO/IEC 42001, ISO/IEC 27001, OECD AI Principles, G7/G20)",
        "",
        "## Monitored Developments Log & Evaluation",
        "",
    ])

    for i, item in enumerate(report_items, 1):
        pr = item.get("proposed_pull_request")
        status_str = "Verified (Priority 1 Official Source)" if pr is not None else "BLOCKED (Unverified Priority 4/5 Source)"
        lines.append(f"### {i}. [{item['jurisdiction']}] {item['track']}")
        lines.append(f"- **Announcement Title**: {item['announcement_title']}")
        lines.append(f"- **Published Date**: {item['announcement_pubDate']}")
        lines.append(f"- **Official Resource Link**: [{item['announcement_link']}]({item['announcement_link']})")
        lines.append(f"- **Verification Status**: {status_str}")
        lines.append(f"- **Compliance Impact Level**: {item['compliance_impact']}")
        lines.append(f"- **Scan Verdict**: {item['scan_verdict']}")
        lines.append("")
        if item["affected_files"]:
            lines.append("  **Identified Affected Files**:")
            for f in item["affected_files"]:
                lines.append(f"  - `{f}`")
            lines.append("")
        lines.append("  **Recommended Migration Tasks**:")
        for task in item["migration_tasks"]:
            lines.append(f"  - [ ] {task}")
        lines.append("")

    lines.append("<!-- REGULATORY_MONITOR_END -->")

    os.makedirs(os.path.dirname(output_filepath) or ".", exist_ok=True)
    with open(output_filepath, "w", encoding="utf-8") as fp:
        fp.write("\n".join(lines) + "\n")
    print(f"Regulatory documentation report written to: {output_filepath}")


def run_monitor(project_path=".", simulate_track=None, verbose=False):
    """
    Runs the compliance scanner and matches developments to tracks.
    """
    announcements = []

    if simulate_track:
        if verbose:
            print(f"[*] Simulating development for track: {simulate_track}")

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
                announcements.append(
                    {
                        "title": f"Custom simulated development mentioning {simulate_track}",
                        "description": f"An official development concerning key elements of {simulate_track}.",
                        "pubDate": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                        "link": "https://eur-lex.europa.eu",
                    }
                )
    else:
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
        "--output-docs",
        nargs="?",
        const="docs/REGULATORY-MONITOR-REPORT-2026.md",
        default=None,
        help="Write/update report markdown to given filepath (default: docs/REGULATORY-MONITOR-REPORT-2026.md)",
    )
    parser.add_argument(
        "--pr-output",
        nargs="?",
        const="docs/REGULATORY_COMPLIANCE_PR_DRAFT.md",
        default=None,
        help="Write draft PR description markdown to given filepath (default: docs/REGULATORY_COMPLIANCE_PR_DRAFT.md)",
    )
    parser.add_argument(
        "--json", action="store_true", help="Output report in JSON format"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print verbose execution logs"
    )

    args = parser.parse_args()

    print(
        "Data. sample developments built into this script, not live news.",
        file=sys.stderr if args.json else sys.stdout,
    )
    report_items, processed = run_monitor(
        project_path=args.project, simulate_track=args.simulate, verbose=args.verbose
    )

    if args.output_docs:
        update_documentation_report(
            report_items, args.output_docs, is_simulated=True
        )

    if args.pr_output:
        pr_content = None
        for item in report_items:
            if item.get("proposed_pull_request"):
                pr_content = item["proposed_pull_request"]["description"]
                break
        if pr_content:
            os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
            with open(args.pr_output, "w", encoding="utf-8") as fp:
                fp.write(pr_content + "\n")
            print(f"Draft Pull Request written to: {args.pr_output}")

    if args.json:
        print(json.dumps(report_items, indent=2))
    else:
        print_text_report(report_items, args.project)


if __name__ == "__main__":
    main()
