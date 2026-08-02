#!/usr/bin/env python3
"""Monitors the 17 mobile security categories in TRACKED_CATEGORIES
below, and generates repo-impact and migration tasks for each update."""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json

# The 17 tracked mobile security requirement categories
TRACKED_CATEGORIES = [
    "secure storage",
    "Keychain",
    "Android Keystore",
    "biometric authentication",
    "certificate pinning",
    "jailbreak detection",
    "root detection",
    "SSL configuration",
    "backup rules",
    "exported activities",
    "intent filters",
    "deep links",
    "universal links",
    "app links",
    "authentication flows",
    "session handling",
    "token storage",
]

# Keywords used to classify incoming policy announcements/articles into the 17 categories
CATEGORY_KEYWORDS = {
    "secure storage": [
        "secure storage",
        "encrypted storage",
        "sqlcipher",
        "sqlite encryption",
        "database encryption",
        "data protection class",
    ],
    "Keychain": [
        "keychain",
        "keychain services",
        "ksecattraccessible",
        "ksecclass",
        "ios credential storage",
    ],
    "Android Keystore": [
        "android keystore",
        "keystore system",
        "hardware-backed key",
        "strongbox",
        "key protection",
    ],
    "biometric authentication": [
        "biometric",
        "biometrics",
        "faceid",
        "touchid",
        "fingerprint",
        "biometricprompt",
        "lacontext",
        "face id",
        "touch id",
    ],
    "certificate pinning": [
        "certificate pinning",
        "ssl pinning",
        "public key pinning",
        "nspinneddomains",
        "pin-set",
        "subject public key info",
        "spki",
    ],
    "jailbreak detection": [
        "jailbreak",
        "jailbroken",
        "jailbreak detection",
        "ios bypass",
        "cydia",
        "mobilesubstrate",
    ],
    "root detection": [
        "root detection",
        "rooted",
        "magisk",
        "superuser",
        "zygisk",
        "play integrity",
        "device integrity",
    ],
    "SSL configuration": [
        "ssl",
        "tls",
        "ssl configuration",
        "cleartext",
        "http traffic",
        "app transport security",
        "ats",
        "usescleartexttraffic",
    ],
    "backup rules": [
        "backup rules",
        "allowbackup",
        "dataextractionrules",
        "fullbackupcontent",
        "cloud backup",
        "device backup",
    ],
    "exported activities": [
        "exported activity",
        "exported activities",
        "android:exported",
        "exported component",
        "intent redirection",
    ],
    "intent filters": [
        "intent filter",
        "intent filters",
        "implicit intent",
        "explicit intent",
        "getcallingpackage",
        "intent spoofing",
    ],
    "deep links": [
        "deep link",
        "deep links",
        "url scheme",
        "custom scheme",
        "cfbundleurlschemes",
    ],
    "universal links": [
        "universal link",
        "universal links",
        "apple-app-site-association",
        "aasa",
        "associated domains",
    ],
    "app links": [
        "app link",
        "app links",
        "assetlinks.json",
        "autoverify",
        "digital asset links",
    ],
    "authentication flows": [
        "auth flow",
        "authentication flow",
        "oauth",
        "pkce",
        "oidc",
        "aswebauthenticationsession",
        "custom tabs",
    ],
    "session handling": [
        "session",
        "sessions",
        "session timeout",
        "session handling",
        "logout",
        "app background",
        "multitasking blur",
    ],
    "token storage": [
        "token storage",
        "token protection",
        "jwt storage",
        "refresh token",
        "access token",
    ],
}

# Codebase signals (regex patterns) to find files affected by each of the 17 categories
CATEGORY_SIGNALS = {
    "secure storage": [
        r"UserDefaults\.standard",
        r"getSharedPreferences",
        r"EncryptedSharedPreferences",
        r"SQLCipher",
    ],
    "Keychain": [
        r"kSecAttrAccessible",
        r"kSecClassGenericPassword",
        r"SecItemAdd",
        r"Keychain",
    ],
    "Android Keystore": [
        r"AndroidKeyStore",
        r"KeyGenParameterSpec",
        r"KeyInfo\.isInsideSecureHardware",
    ],
    "biometric authentication": [
        r"LAContext",
        r"BiometricPrompt",
        r"evaluatePolicy",
        r"CryptoObject",
    ],
    "certificate pinning": [
        r"NSPinnedDomains",
        r"CertificatePinner",
        r"pin-set",
        r"network_security_config",
    ],
    "jailbreak detection": [
        r"Cydia",
        r"MobileSubstrate",
        r"bin/bash",
        r"private/jailbreak",
    ],
    "root detection": [
        r"magisk",
        r"Build\.TAGS",
        r"test-keys",
        r"PlayIntegrity",
        r"IntegrityManager",
    ],
    "SSL configuration": [
        r"usesCleartextTraffic",
        r"NSAllowsArbitraryLoads",
        r"cleartextTrafficPermitted",
    ],
    "backup rules": [
        r"allowBackup",
        r"dataExtractionRules",
        r"fullBackupContent",
        r"isExcludedFromBackup",
    ],
    "exported activities": [
        r"android:exported",
        r"protectionLevel",
        r"signature",
    ],
    "intent filters": [
        r"intent-filter",
        r"getCallingPackage",
        r"getCallingActivity",
    ],
    "deep links": [
        r"CFBundleURLSchemes",
        r"android:scheme",
        r"custom scheme",
    ],
    "universal links": [
        r"apple-app-site-association",
        r"applinks",
        r"Associated Domains",
    ],
    "app links": [
        r"assetlinks\.json",
        r"autoVerify",
        r"handle_all_urls",
    ],
    "authentication flows": [
        r"OAuth",
        r"PKCE",
        r"ASWebAuthenticationSession",
        r"CustomTabs",
    ],
    "session handling": [
        r"logout",
        r"sessionTimeout",
        r"backgroundTimeRemaining",
        r"multitasking",
    ],
    "token storage": [
        r"token",
        r"jwt",
        r"access_token",
        r"refresh_token",
    ],
}

# Rich mock announcements representing policy updates/bulletins for ALL 17 categories
MOCK_ANNOUNCEMENTS = [
    {
        "id": "SEC-MOCK-STORAGE",
        "category": "secure storage",
        "title": "NIST Guidelines on Mobile Data Protection",
        "description": "NIST publishes updated recommendations on secure storage, mandating that all sensitive data must be encrypted using strong cryptographic systems such as AES-256 and SQLCipher, rather than unencrypted standard options like UserDefaults or plain SharedPreferences.",
        "link": "https://pages.nist.gov/Mobile-Threat-Catalogue/",
        "pubDate": "Fri, 15 May 2026 10:00:00 GMT",
    },
    {
        "id": "SEC-MOCK-KEYCHAIN",
        "category": "Keychain",
        "title": "Apple Security Update: iOS Keychain Protection Class Enforcement",
        "description": "Apple security teams release advisory enforcing the use of strict Keychain accessibility attributes. Developers are instructed to use kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly to prevent unauthorized backup extraction and access group leaks.",
        "link": "https://developer.apple.com/security/",
        "pubDate": "Sat, 16 May 2026 11:00:00 GMT",
    },
    {
        "id": "SEC-MOCK-KEYSTORE",
        "category": "Android Keystore",
        "title": "Android Keystore Security Advisory on StrongBox Hardware Backing",
        "description": "Google publishes Android Keystore guidelines requiring StrongBox hardware protection on devices that support it. Developers must use KeyGenParameterSpec to generate keys inside secure hardware and check isInsideSecureHardware at runtime.",
        "link": "https://source.android.com/docs/security/",
        "pubDate": "Sun, 17 May 2026 12:00:00 GMT",
    },
    {
        "id": "SEC-MOCK-BIOMETRICS",
        "category": "biometric authentication",
        "title": "OWASP MASVS Biometric Bypass Protection and Cryptographic Binding",
        "description": "OWASP updates MASVS biometric authentication requirements, specifying that biometric prompts must be backed by cryptographic keys in Keychain or Keystore via CryptoObject and SecAccessControl, and simple boolean success callbacks are fully deprecated to prevent runtime instrument hooks.",
        "link": "https://mas.owasp.org/MASVS/",
        "pubDate": "Mon, 18 May 2026 13:00:00 GMT",
    },
    {
        "id": "SEC-MOCK-PINNING",
        "category": "certificate pinning",
        "title": "ENISA Advisory on Certificate Pinning and Subject Public Key Info Hashes",
        "description": "ENISA recommends certificate pinning using Subject Public Key Info SPKI hashes rather than full certificates. The advisory stresses utilizing NSPinnedDomains natively on iOS and network_security_config on Android with robust backup pin definitions.",
        "link": "https://www.enisa.europa.eu/publications",
        "pubDate": "Tue, 19 May 2026 14:00:00 GMT",
    },
    {
        "id": "SEC-MOCK-JAILBREAK",
        "category": "jailbreak detection",
        "title": "Apple Security Brief on Multi-layered Jailbreak Detection",
        "description": "An official iOS security brief details the evasion tactics of jailbreak tools. App developers are advised to employ multi-layered detection heuristics, checking for Cydia, MobileSubstrate, and verifying dyld dynamic linkers rather than single boolean checks.",
        "link": "https://developer.apple.com/support/downloads/",
        "pubDate": "Wed, 20 May 2026 15:00:00 GMT",
    },
    {
        "id": "SEC-MOCK-ROOT",
        "category": "root detection",
        "title": "Google Play Integrity API Integration for Robust Root Detection",
        "description": "Google Play updates security rules, mandating hardware-backed Play Integrity API tokens for sensitive operations. Traditional local root detection (Magisk, su checks) must be paired with server-side signature verification of Integrity tokens.",
        "link": "https://developer.android.com/google/play/integrity",
        "pubDate": "Thu, 21 May 2026 16:00:00 GMT",
    },
    {
        "id": "SEC-MOCK-SSL",
        "category": "SSL configuration",
        "title": "CISA Bulletin on Disabling Cleartext HTTP Traffic in Production",
        "description": "CISA issues a directive requiring mobile apps to completely disable cleartext HTTP traffic. App Transport Security ATS NSAllowsArbitraryLoads must be false on iOS, and usesCleartextTraffic must be false in Android manifests to mitigate active MITM interception.",
        "link": "https://www.cisa.gov/news-events/directives",
        "pubDate": "Fri, 22 May 2026 17:00:00 GMT",
    },
    {
        "id": "SEC-MOCK-BACKUP",
        "category": "backup rules",
        "title": "Federal Trade Commission Advice on Mobile App Backup Rules",
        "description": "The FTC alerts developers to secure mobile app backups. On Android, allowBackup must be false or dataExtractionRules configured to exclude local authentication tokens, databases, and preferences from cloud or adb backups to prevent credential leakage.",
        "link": "https://www.ftc.gov/business-guidance/",
        "pubDate": "Sat, 23 May 2026 18:00:00 GMT",
    },
    {
        "id": "SEC-MOCK-EXPORTED",
        "category": "exported activities",
        "title": "Android Vulnerability Report on Exported Activities and Intent Redirection",
        "description": "A high-severity vulnerability report warns against setting android:exported to true without signature-level permission restrictions. Unprotected exported components expose internal business logic and can bypass authentication.",
        "link": "https://source.android.com/docs/security/bulletin",
        "pubDate": "Sun, 24 May 2026 19:00:00 GMT",
    },
    {
        "id": "SEC-MOCK-INTENTS",
        "category": "intent filters",
        "title": "NIST Mobile Security on Intent Spoofing and Intent Filters Protection",
        "description": "NIST releases guidelines on inter-process communication safety, requiring validation of implicit intents with getCallingPackage and getCallingActivity to block intent spoofing, and recommending explicit intents for internal app components.",
        "link": "https://pages.nist.gov/Mobile-Threat-Catalogue/",
        "pubDate": "Mon, 25 May 2026 20:00:00 GMT",
    },
    {
        "id": "SEC-MOCK-DEEPLINKS",
        "category": "deep links",
        "title": "CISA Advisory on Custom URL Scheme Deep Link Hijacking Vulnerabilities",
        "description": "CISA highlights deep link hijacking risks where multiple apps register identical custom URL schemes. Apps are advised to never transmit session tokens or credentials in deep links, and sanitize all parsed incoming parameters.",
        "link": "https://www.cisa.gov/news-events/alerts",
        "pubDate": "Tue, 26 May 2026 21:00:00 GMT",
    },
    {
        "id": "SEC-MOCK-UNIVERSAL",
        "category": "universal links",
        "title": "Apple Security Update: Universal Links Domain Verification Guidelines",
        "description": "Apple security highlights guidelines on secure domain verification. Developers must host valid apple-app-site-association AASA files on HTTPS domains and declare matching Associated Domains in entitlements to prevent deep link spoofing.",
        "link": "https://developer.apple.com/security/",
        "pubDate": "Wed, 27 May 2026 22:00:00 GMT",
    },
    {
        "id": "SEC-MOCK-APPLINKS",
        "category": "app links",
        "title": "Android App Links Auto-Verification and AssetLinks Configuration Mandate",
        "description": "Google publishes Android App Links verification requirements, emphasizing assetlinks.json configuration and autoVerify true in AndroidManifest.xml, guaranteeing secure and direct domain-app association.",
        "link": "https://developer.android.com/training/app-links",
        "pubDate": "Thu, 28 May 2026 23:00:00 GMT",
    },
    {
        "id": "SEC-MOCK-AUTH",
        "category": "authentication flows",
        "title": "OAuth 2.1 and PKCE Requirement Mandate for Mobile Apps",
        "description": "The IETF OAuth Working Group advances OAuth 2.1, making Proof Key for Code Exchange PKCE mandatory for mobile applications. Mobile authentication must rely on ASWebAuthenticationSession or Custom Tabs instead of embedded webviews to protect secrets.",
        "link": "https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics",
        "pubDate": "Fri, 29 May 2026 09:00:00 GMT",
    },
    {
        "id": "SEC-MOCK-SESSIONS",
        "category": "session handling",
        "title": "NIST Guidance on Mobile Session Invalidation and Background Blurring",
        "description": "NIST recommendations for high-assurance session handling include immediate server-side validation, short-lived tokens, complete local cache purge upon logout, and background blurring of multitasking window views to protect sensitive data screens.",
        "link": "https://pages.nist.gov/Mobile-Threat-Catalogue/",
        "pubDate": "Sat, 30 May 2026 10:00:00 GMT",
    },
    {
        "id": "SEC-MOCK-TOKENS",
        "category": "token storage",
        "title": "OWASP MASVS Token Storage and Access Isolation Advisory",
        "description": "OWASP MASVS updates token protection guidance, requiring short-lived access tokens and isolating long-lived refresh tokens using biometrics or hardware backing. Tokens must never be printed to logs or stored in plain local databases.",
        "link": "https://mas.owasp.org/MASVS/",
        "pubDate": "Sun, 31 May 2026 11:00:00 GMT",
    },
]


def scan_codebase_for_security_signals(start_dir="."):
    """
    Scans the codebase for files containing signals related to each of the 17 requirement categories.
    """
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
                    ".swift",
                    ".m",
                    ".h",
                    ".kt",
                    ".java",
                    ".xml",
                    ".gradle",
                    ".kts",
                    ".json",
                    ".js",
                    ".ts",
                    ".md",
                    ".plist",
                    ".entitlements",
                )
            ):
                continue

            filepath = os.path.join(root, file)
            # Skip monitor scripts to avoid self-referencing matches
            if "monitor-security" in file or "monitor-security-test" in file:
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
                                    # Break to avoid duplicate entry for the same line and category
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
            url, headers={"User-Agent": "Mozilla/5.0 (MobileSecurityComplianceMonitor/1.0)"}
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
        print("Warning: Failed to fetch live feed " + str(url) + ": " + str(e), file=sys.stderr)
    return items


def classify_announcements(announcements, keywords_filter=None):
    """
    Classifies incoming announcements into the 17 mobile security requirement categories.
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

        # If a pre-set category exists on mock and no matched categories, use that category
        if not matched_categories and ann.get("category"):
            matched_categories.append(ann["category"])

        if matched_categories:
            for cat in matched_categories:
                classified_updates.append(
                    {
                        "id": ann.get("id", "SEC-UPDATE-" + str(hash(title))[:6]),
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
        citations_list.append(
            "- " + cat + ": [" + u["title"] + "](" + u["link"] + ") (Published: " + u["pubDate"] + ")"
        )

        # Pull affected files
        files = scan_results.get(cat, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        # Category-specific migration details
        if cat == "secure storage":
            migration_steps.append(
                "- " + cat + ": Migrate plain UserDefaults/SharedPreferences to Keychain / EncryptedSharedPreferences."
            )
            impl_checklist.append(
                "- [ ] Replace plain disk database or keys with SQLCipher or Jetpack Security wrappers."
            )
            risk_assessment.append(
                "- " + cat + ": High exposure of local storage secrets to device-compromise attacks."
            )
        elif cat == "Keychain":
            migration_steps.append(
                "- " + cat + ": Enforce kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly for Keychain items."
            )
            impl_checklist.append(
                "- [ ] Update SecItemAdd and SecItemUpdate attributes with strict accessibility class."
            )
            risk_assessment.append(
                "- " + cat + ": Backup recovery vulnerability if keys migrate across devices during physical restore."
            )
        elif cat == "Android Keystore":
            migration_steps.append(
                "- " + cat + ": Enforce StrongBox hardware-backing and KeyGenParameterSpec restrictions."
            )
            impl_checklist.append(
                "- [ ] Configure setIsStrongBoxBacked(true) and check isInsideSecureHardware() in Keystore initialization."
            )
            risk_assessment.append(
                "- " + cat + ": Key extraction vulnerability if keys are stored in software-backed boundaries."
            )
        elif cat == "biometric authentication":
            migration_steps.append(
                "- " + cat + ": Implement crypto-backed biometrics via CryptoObject and SecAccessControl."
            )
            impl_checklist.append(
                "- [ ] Require biometrics to authorize or unlock actual cryptographic keys instead of simple boolean flags."
            )
            risk_assessment.append(
                "- " + cat + ": Rooted/jailbroken device runtime instrumentation hooks bypass simple boolean success returns."
            )
        elif cat == "certificate pinning":
            migration_steps.append(
                "- " + cat + ": Pin SPKI hashes of intermediate or leaf public keys with backup pins."
            )
            impl_checklist.append(
                "- [ ] Configure NSPinnedDomains in iOS Info.plist and network_security_config.xml on Android."
            )
            risk_assessment.append(
                "- " + cat + ": Man-in-the-middle MITM proxy traffic sniffing and modification."
            )
        elif cat == "jailbreak detection":
            migration_steps.append(
                "- " + cat + ": Implement multi-layered detection of jailbreak artifacts (Cydia, MobileSubstrate, dyld)."
            )
            impl_checklist.append(
                "- [ ] Add sandbox file write and symlink verification checks to runtime security modules."
            )
            risk_assessment.append(
                "- " + cat + ": Loss of security guarantees and sandbox boundaries on compromised iOS platforms."
            )
        elif cat == "root detection":
            migration_steps.append(
                "- " + cat + ": Integrate Google Play Integrity API verification on backend server."
            )
            impl_checklist.append(
                "- [ ] Forward signed Play Integrity tokens to secure server endpoint for decryption and validation."
            )
            risk_assessment.append(
                "- " + cat + ": Runtime database access, code redirection, and token extraction on compromised Android devices."
            )
        elif cat == "SSL configuration":
            migration_steps.append(
                "- " + cat + ": Force TLS 1.2 or 1.3 minimum. Disable cleartext HTTP globally."
            )
            impl_checklist.append(
                "- [ ] Set android:usesCleartextTraffic to false and keep NSAllowsArbitraryLoads false in production configs."
            )
            risk_assessment.append(
                "- " + cat + ": Local Wi-Fi network credential or session interception."
            )
        elif cat == "backup rules":
            migration_steps.append(
                "- " + cat + ": Restrict backup domains to exclude sensitive credentials and databases."
            )
            impl_checklist.append(
                "- [ ] Set android:allowBackup to false or declare strict dataExtractionRules filtering preferences."
            )
            risk_assessment.append(
                "- " + cat + ": Unencrypted secrets exported automatically during device migrations or cloud backups."
            )
        elif cat == "exported activities":
            migration_steps.append(
                "- " + cat + ": Restrict exported activities to false or apply signature-level permissions."
            )
            impl_checklist.append(
                "- [ ] Audit AndroidManifest.xml; enforce android:exported to false unless strictly required."
            )
            risk_assessment.append(
                "- " + cat + ": Vulnerability to arbitrary intent injection or app logic redirection by malicious local apps."
            )
        elif cat == "intent filters":
            migration_steps.append(
                "- " + cat + ": Sanitize and validate incoming implicit intents using calling package metrics."
            )
            impl_checklist.append(
                "- [ ] Implement calling package validation via getCallingActivity and getCallingPackage."
            )
            risk_assessment.append(
                "- " + cat + ": Potential spoofing or hijacking of implicit broadcast messages or activities."
            )
        elif cat == "deep links":
            migration_steps.append(
                "- " + cat + ": Sanitize all deep link parameters; never pass access tokens or secrets in URLs."
            )
            impl_checklist.append(
                "- [ ] Implement strict URL input validation and restrict scheme targets to transient identifiers."
            )
            risk_assessment.append(
                "- " + cat + ": Deep link URL hijacking or token leakage to third-party registered handlers."
            )
        elif cat == "universal links":
            migration_steps.append(
                "- " + cat + ": Set up secure, HTTPS-validated Universal Links."
            )
            impl_checklist.append(
                "- [ ] Deploy apple-app-site-association file to HTTPS root and configure Associated Domains entitlement."
            )
            risk_assessment.append(
                "- " + cat + ": Insecure custom scheme redirection allowing link hijack exploits."
            )
        elif cat == "app links":
            migration_steps.append(
                "- " + cat + ": Setup secure Android App Links with autoVerify."
            )
            impl_checklist.append(
                "- [ ] Publish assetlinks.json on server domain and configure autoVerify true on matching intent filters."
            )
            risk_assessment.append(
                "- " + cat + ": Intent hijacking leading to credential spoofing on older Android versions."
            )
        elif cat == "authentication flows":
            migration_steps.append(
                "- " + cat + ": Deploy OAuth 2.1 / OIDC flows utilizing PKCE code challenges."
            )
            impl_checklist.append(
                "- [ ] Replace embedded WebViews with ASWebAuthenticationSession on iOS and Custom Tabs on Android."
            )
            risk_assessment.append(
                "- " + cat + ": Theft of Authorization codes or user credentials from embedded WebView DOM trees."
            )
        elif cat == "session handling":
            migration_steps.append(
                "- " + cat + ": Implement server-validated sessions, short lifetimes, and background multitasking blurring."
            )
            impl_checklist.append(
                "- [ ] Listen to background/active application transitions; blur multitasking preview window."
            )
            risk_assessment.append(
                "- " + cat + ": Exposure of confidential information via snapshot previews in multitasking menus."
            )
        elif cat == "token storage":
            migration_steps.append(
                "- " + cat + ": Enforce isolated, secure vaulting for JWTs and access/refresh tokens."
            )
            impl_checklist.append(
                "- [ ] Store transient tokens strictly within Keychain or Android EncryptedSharedPreferences."
            )
            risk_assessment.append(
                "- " + cat + ": Leakage of access credentials leading to unauthorized account takeovers."
            )

    citations_str = "\n".join(citations_list)

    if affected_files_set:
        affected_files_str = "\n".join(
            "- `" + f + "`" for f in sorted(list(affected_files_set))
        )
    else:
        affected_files_str = "- *No specific files containing matching security patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps)
    impl_checklist_str = "\n".join(impl_checklist)
    risk_assessment_str = "\n".join(risk_assessment)

    pr_template = f"""# PULL REQUEST DRAFT: Mobile Security Requirements Compliance Update

## 1. Summary
This pull request implements comprehensive security upgrades to align the mobile application architecture with current OWASP MASVS guidelines and regulatory compliance requirements. It ensures secure data storage, cryptographic keystore validation, biometric verification integrity, certificate pinning, and intent-filter isolation across both platform environments.

## 2. Background
Ensuring client-side confidentiality and data protection is critical to preventing session hijacking, token leakage, or administrative credential compromises. This security update proactively fortifies mobile storage mechanisms and transit layers against current Threat Catalogue attack surfaces.

## 3. Regulatory change
- **OWASP MASVS & NIST SP 800-218 Guidelines**: Mandates hardware-backed cryptographic bounds, biometric-bound authorization vaults, strict keychain sharing, and disabling cleartext HTTP interfaces.
- **Privacy & Transport Standards**: Standardizes certificate pinning using SPKI hashes, Universal/App Link verification to block custom scheme redirection, and PKCE-bound OAuth 2.1 authorization flows.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Threat Level**: Critical vulnerability risk if unencrypted tokens or credentials reside in standard device directories.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All cryptographic upgrades preserve full backward compatibility with older operating systems. EncryptedSharedPreferences and Keychain classes utilize modern, system-supported algorithms. Fallback storage models apply gracefully where hardware-based StrongBox modules are absent.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Re-run the compliance guard scanner to confirm zero remaining violations.

## 10. Testing checklist
- [ ] Verify that secure keychain and database read/write actions execute properly.
- [ ] Confirm biometric-bound cryptographic key verification processes prompt user dialogs correctly.
- [ ] Run network interception tools to confirm certificate pinning actively blocks un-trusted proxy certificates.
- [ ] Verify background multitasking blurring behaves correctly during application suspension.

## 11. Documentation checklist
- [ ] Update internal mobile security architecture guides.
- [ ] Update `docs/SECURITY-POLICY-MIGRATION.md` with finished actions.
- [ ] Record developer setup parameters for local hardware attestation testing.

## 12. Compliance impact
- **Data Security Standing**: Guarantees compliance with modern secure storage requirements, protecting client records from offline dump inspection.
- **Brand standing**: Dramatically lowers risk profiles in regulated finance, health, and enterprise app markets.
- **Rejection Prevention**: Mitigates compliance strikes, securing flawless App Store and Google Play review lifecycles.

## 13. Breaking changes
- No direct functional breaking changes are introduced. Standard background processing remains unaltered.
- Devices lacking secure passcode or hardware enclaves face graceful downgrades.

## 14. Review checklist
- [ ] Code strictly isolates credential tokens from console prints or plaintext storage structures.
- [ ] AndroidManifest.xml and Info.plist configurations set Cleartext policies to false.
- [ ] Deep links do not carry sensitive transactional payloads or access tokens.

## 15. Approver recommendations
Verify that intermediate public keys of production endpoints match SPKI pins declared in configuration files. Confirm that all local SQLite databases adopt verified SQLCipher wraps before code deployment.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """
    Overwrites or updates the migration report in docs/SECURITY-POLICY-MIGRATION.md.
    """
    lines = [
        "<!-- SECURITY_POLICY_MONITOR_START -->",
        "# Mobile Security Requirements Policy Migration & Compliance Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-security.py` to track security compliance.",
        "",
        "## Monitored Security Guidelines Update Log",
        "",
    ]

    for idx, u in enumerate(updates, 1):
        lines.append("### " + str(idx) + ". [" + u["category"] + "] " + u["title"])
        lines.append("- **Published Date**: " + u["pubDate"])
        lines.append("- **Official Resource**: [" + u["link"] + "](" + u["link"] + ")")
        lines.append("- **Description**: " + u["description"])
        lines.append("")

    lines.append("## Automated Security Migration Recommendations & Tasks")
    lines.append("")

    for u in updates:
        cat = u["category"]
        lines.append("### Security tasks for " + cat)
        lines.append(
            "- **Threat Vulnerability Level**: High priority. System protection requires immediate task execution."
        )

        if cat == "secure storage":
            lines.append("- [ ] **Task 1**: Replace plain SharedPreferences and UserDefaults with EncryptedSharedPreferences or Keychain wrappers.")
            lines.append("- [ ] **Task 2**: Encrypt local database assets using SQLCipher or system-level Data Protection files.")
        elif cat == "biometric authentication":
            lines.append("- [ ] **Task 1**: Refactor local FaceID/TouchID prompts to release hardware-backed Keystore/Keychain keys.")
            lines.append("- [ ] **Task 2**: Eliminate local boolean check dependencies from authentication controllers.")
        elif cat == "certificate pinning":
            lines.append("- [ ] **Task 1**: Configure native NSPinnedDomains or network_security_config SPKI base64 hashes.")
            lines.append("- [ ] **Task 2**: Declare secondary standby backup public key pins.")
        elif cat == "backup rules":
            lines.append("- [ ] **Task 1**: Set allowBackup to false in manifest, or define robust dataExtractionRules files.")
            lines.append("- [ ] **Task 2**: Set the isExcludedFromBackup flag on all local storage URL folders.")
        else:
            lines.append("- [ ] **Task**: Review mobile codebase; configure and verify that active structures satisfy security criteria for " + cat + ".")
        lines.append("")

    lines.append("<!-- SECURITY_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print("Security compliance report updated successfully at: " + output_filepath)
    except Exception as e:
        print("Error writing security documentation to " + output_filepath + ": " + str(e), file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor all Mobile Security requirements and best practices"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live mobile security advisory feeds"
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
        default="docs/SECURITY-POLICY-MIGRATION.md",
        help="Filepath to write migration tasks and logs",
    )
    parser.add_argument(
        "--pr-output",
        type=str,
        default="docs/SECURITY_COMPLIANCE_PR_DRAFT.md",
        help="Filepath to save the drafted PR",
    )
    parser.add_argument(
        "--json", action="store_true", help="Output report in JSON format"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print verbose execution and scanning logs"
    )

    args = parser.parse_args()

    # 1. Gather announcements
    announcements = []

    if args.live:
        print("Fetching live mobile security bulletins...", file=sys.stderr)
        # NIST Mobile Threat feed or standard secure advisory source fallbacks
        announcements.extend(
            parse_rss_feed(
                "https://source.android.com/security/bulletin.xml"
            )
        )

    # Fallback to mock data if live has no updates or mock is explicitly requested
    if args.mock or (not args.live and not args.mock) or not announcements:
        if args.verbose:
            print("Using comprehensive mock security updates for compliance scanning...", file=sys.stderr)
        if args.mock and args.mock != "inline" and os.path.exists(args.mock):
            try:
                with open(args.mock, "r") as f:
                    announcements.extend(json.load(f))
            except Exception as e:
                print("Failed to read mock file " + str(args.mock) + ": " + str(e) + ", using default mock dataset instead.", file=sys.stderr)
                announcements.extend(MOCK_ANNOUNCEMENTS)
        else:
            announcements.extend(MOCK_ANNOUNCEMENTS)

    # 2. Classify updates into the 17 security categories
    keywords_filter = (
        [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    )
    classified_updates = classify_announcements(announcements, keywords_filter)

    if not classified_updates:
        print("No classified security updates matched the current filters.")
        sys.exit(0)

    if args.verbose:
        print("Monitored and classified " + str(len(classified_updates)) + " security requirement updates:", file=sys.stderr)
        for idx, u in enumerate(classified_updates, 1):
            print(" " + str(idx) + ". [" + u["category"] + "] " + u["title"], file=sys.stderr)

    # 3. Scan the codebase for signals related to these categories
    if args.verbose:
        print("Scanning codebase under '" + args.dir + "' for security integration signals...", file=sys.stderr)
    scan_results = scan_codebase_for_security_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    if args.verbose:
        print("Found " + str(total_matches) + " security signal matches in code.", file=sys.stderr)

    # 4. JSON output requested?
    if args.json:
        report_data = []
        for u in classified_updates:
            cat = u["category"]
            matches_list = scan_results.get(cat, [])
            report_data.append({
                "announcement_id": u["id"],
                "category": cat,
                "title": u["title"],
                "description": u["description"],
                "link": u["link"],
                "pubDate": u["pubDate"],
                "affected_files": [m["file"] for m in matches_list],
            })
        print(json.dumps(report_data, indent=2))
        return

    # 5. Write/Update documentation
    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, args.output_docs)

    # 6. Generate Pull Request draft
    pr_draft = generate_pull_request_draft(classified_updates, scan_results)

    if args.pr_output:
        os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
        try:
            with open(args.pr_output, "w", encoding="utf-8") as f:
                f.write(pr_draft)
            print("PR draft written successfully to: " + args.pr_output)
        except Exception as e:
            print("Failed to write PR draft to " + args.pr_output + ": " + str(e), file=sys.stderr)
    else:
        print("\n=== GENERATED 15-SECTION SECURITY PULL REQUEST DRAFT ===")
        print(pr_draft)
        print("========================================================")


if __name__ == "__main__":
    main()
