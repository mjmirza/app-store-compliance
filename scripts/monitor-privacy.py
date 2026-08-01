#!/usr/bin/env python3
"""
Mobile and Web Privacy Compliance Requirements Monitor.
Tracks 16 distinct Apple, Android, and Web privacy requirements.
Statically scans the codebase, updates/generates docs/PRIVACY-POLICY-MIGRATION.md,
and drafts docs/PRIVACY_COMPLIANCE_PR_DRAFT.md with exactly 15 non-vague sections.
Strict Emoji-Free Policy is enforced.
"""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json
from datetime import datetime

# 16 tracked privacy requirements
PRIVACY_REQUIREMENTS = {
    # Apple Privacy Requirements (4)
    "Privacy Manifest": {
        "platform": "apple",
        "severity": "critical",
        "keywords": ["privacy manifest", "xcprivacy", "privacyinfo"],
        "detect_files": ["PrivacyInfo.xcprivacy", "*.swift", "*.plist", "*.m", "*.h"],
        "detect_regex": r"NSPrivacyAccessedAPITypes|NSPrivacyCollectedDataTypes|PrivacyInfo\.xcprivacy",
        "citations": [
            "Apple Developer Documentation: Privacy Manifest Files",
            "App Store Review Guidelines 5.1.1"
        ],
        "impact_desc": "Mandatory privacy manifest requirement (PrivacyInfo.xcprivacy) for third-party SDKs and Required Reason APIs.",
        "migration_steps": [
            "Audit third-party SDKs for presence of their signed PrivacyInfo.xcprivacy.",
            "Generate or update a root PrivacyInfo.xcprivacy with correct tracking domains and data collection declarations."
        ]
    },
    "Required Reason APIs": {
        "platform": "apple",
        "severity": "critical",
        "keywords": ["required reason api", "accessed api", "reasons for api", "userdefaults", "systemuptime"],
        "detect_files": ["*.swift", "*.m", "*.h", "*.plist", "PrivacyInfo.xcprivacy"],
        "detect_regex": r"UserDefaults|NSFileManager|systemUptime|ProcessInfo|stat\s*\(",
        "citations": [
            "Apple Developer Documentation: Describing data use with privacy manifests",
            "App Store Review Guidelines 5.1.1"
        ],
        "impact_desc": "Stricter declaration rules for accessing specific Apple system APIs (UserDefaults, systemUptime, system boot time, file timestamps).",
        "migration_steps": [
            "Identify any use of file timestamps, system boot time, disk space, active keyboard, or user defaults.",
            "Declare valid reason codes in PrivacyInfo.xcprivacy under NSPrivacyAccessedAPITypes."
        ]
    },
    "App Tracking Transparency": {
        "platform": "apple",
        "severity": "high",
        "keywords": ["app tracking transparency", "att", "idfa", "user tracking"],
        "detect_files": ["Info.plist", "*.swift", "*.m", "*.h"],
        "detect_regex": r"ATTrackingManager|NSUserTrackingUsageDescription|ASIdentifierManager|advertisingIdentifier",
        "citations": [
            "Apple Developer Documentation: User Tracking and Data Privacy",
            "App Store Review Guidelines 5.1.2"
        ],
        "impact_desc": "Tracking consent rules and IDFA access restrictions require explicit user consent prompts.",
        "migration_steps": [
            "Verify ATTrackingManager.requestTrackingAuthorization is called before starting any tracking.",
            "Add NSUserTrackingUsageDescription with a clear reason explaining why tracking is used."
        ]
    },
    "Privacy Nutrition Labels": {
        "platform": "apple",
        "severity": "high",
        "keywords": ["privacy nutrition label", "nutrition label", "privacy label", "collected data types"],
        "detect_files": ["*.swift", "*.m", "*.h", "Info.plist"],
        "detect_regex": r"NSPrivacyCollectedDataTypes|privacyNutritionLabels|privacy-nutrition-labels",
        "citations": [
            "Apple Developer Documentation: App privacy details on the App Store",
            "App Store Review Guidelines 5.1.1"
        ],
        "impact_desc": "Self-reported App Store Privacy Nutrition Labels must align with actual codebase data collection.",
        "migration_steps": [
            "Conduct a data inventory to locate all points of user PII collection.",
            "Verify that NSPrivacyCollectedDataTypes maps correctly to App Store Connect labels."
        ]
    },

    # Android Privacy Requirements (6)
    "Data Safety": {
        "platform": "android",
        "severity": "critical",
        "keywords": ["data safety", "datasafety", "safety section", "data declaration"],
        "detect_files": ["*.kt", "*.java", "*.xml", "*.gradle", "*.kts"],
        "detect_regex": r"Data Safety|firebase-analytics|appsflyer|adjust|com\.facebook",
        "citations": [
            "Google Play Console Help: Provide app privacy and security information for Google Play's Data Safety section",
            "Google Play Developer Distribution Agreement"
        ],
        "impact_desc": "Google Play Data Safety declarations must match the runtime activities and compiled SDK inclusions.",
        "migration_steps": [
            "Audit all network endpoints and third-party SDKs for data collection activities.",
            "Update the Play Console Data Safety questionnaire declarations to match the current state."
        ]
    },
    "User Data Policy": {
        "platform": "android",
        "severity": "critical",
        "keywords": ["user data policy", "prominent disclosure", "personal data", "user data"],
        "detect_files": ["*.kt", "*.java", "*.xml", "*.gradle"],
        "detect_regex": r"privacyPolicy|privacy-policy|privacy_policy|User Data|deleteAccount|delete_account",
        "citations": [
            "Google Play Developer Policy Center: User Data",
            "Google Play Developer Program Policies"
        ],
        "impact_desc": "Accessing or transferring contacts, accounts, SMS, or files requires prominent disclosures and consent.",
        "migration_steps": [
            "Build explicit prominent disclosure dialogues shown before permission prompts or data ingestion.",
            "Verify that in-app and web account deletion links are correctly active."
        ]
    },
    "Advertising ID": {
        "platform": "android",
        "severity": "high",
        "keywords": ["advertising id", "ad_id", "google play services advertising id", "com.google.android.gms.permission.AD_ID"],
        "detect_files": ["AndroidManifest.xml", "*.kt", "*.java", "build.gradle"],
        "detect_regex": r"com\.google\.android\.gms\.permission\.AD_ID|AD_ID|com\.google\.android\.gms\.ads\.identifier",
        "citations": [
            "Google Play Console Help: Advertising ID",
            "Google Play Developer Program Policies: Play Console requirements"
        ],
        "impact_desc": "Apps targeting modern API levels using Advertising ID must declare the permission and support user opt-outs.",
        "migration_steps": [
            "Declare com.google.android.gms.permission.AD_ID in the manifest if using tracking features.",
            "Ensure opt-out capability is supported by gracefully handling zeroed out identifiers."
        ]
    },
    "Runtime permissions": {
        "platform": "android",
        "severity": "critical",
        "keywords": ["runtime permission", "request permission", "check permission", "dynamic permission"],
        "detect_files": ["*.kt", "*.java", "AndroidManifest.xml"],
        "detect_regex": r"requestPermissions|checkSelfPermission|Manifest\.permission|uses-permission",
        "citations": [
            "Android Developer Documentation: Request app permissions",
            "Google Play Developer Program Policies: Permissions"
        ],
        "impact_desc": "Sensitive capabilities must be requested dynamically at runtime with context and checking.",
        "migration_steps": [
            "Verify dynamic checks are present before accessing system hardware or personal data.",
            "Test fallback paths to ensure graceful degradation if permissions are rejected."
        ]
    },
    "Background location": {
        "platform": "android",
        "severity": "critical",
        "keywords": ["background location", "access_background_location", "background location permission"],
        "detect_files": ["AndroidManifest.xml", "*.kt", "*.java"],
        "detect_regex": r"ACCESS_BACKGROUND_LOCATION",
        "citations": [
            "Google Play Console Help: Requesting background location permission",
            "Google Play Developer Program Policies: Location Permissions"
        ],
        "impact_desc": "Strict constraints are placed on accessing background location, which must be essential and disclosed prominently.",
        "migration_steps": [
            "Verify ACCESS_BACKGROUND_LOCATION is necessary, otherwise restrict location to foreground.",
            "Implement a highly visible prominent disclosure detailing location usage in the background."
        ]
    },
    "Health permissions": {
        "platform": "android",
        "severity": "high",
        "keywords": ["health connect", "health permission", "health data", "fitness data"],
        "detect_files": ["AndroidManifest.xml", "*.kt", "*.java"],
        "detect_regex": r"HealthConnect|health|step|heart|HKHealthStore|HealthKit",
        "citations": [
            "Android Developer Documentation: Health Connect",
            "Google Play Developer Program Policies: Health Connect Policy"
        ],
        "impact_desc": "Accessing health or wellness data requires special developer declarations and a distinct health privacy policy.",
        "migration_steps": [
            "Complete the Health Connect declaration form in the Google Play Console.",
            "Provide an in-app link to a specialized privacy policy covering sensitive health data."
        ]
    },

    # Web Privacy Requirements (6)
    "GDPR": {
        "platform": "web",
        "severity": "critical",
        "keywords": ["gdpr", "general data protection regulation", "consent modal", "right to be forgotten"],
        "detect_files": ["*.html", "*.js", "*.ts", "*.vue", "*.jsx", "*.tsx"],
        "detect_regex": r"gdpr|userConsent|personalData|deleteAccount|dataDelet|rightToEras",
        "citations": [
            "Regulation (EU) 2016/679 (General Data Protection Regulation)",
            "EDPB Guidelines on Consent and Data Subject Rights"
        ],
        "impact_desc": "GDPR mandates strict, freely given user consent and comprehensive right to erasure / data deletion pathways.",
        "migration_steps": [
            "Validate that no personal data or tracking is initiated before consent is granted.",
            "Offer a straightforward way for web users to request deletion of all collected personal data."
        ]
    },
    "Cookie consent": {
        "platform": "web",
        "severity": "critical",
        "keywords": ["cookie consent", "cookie banner", "eprivacy", "eprivacy directive"],
        "detect_files": ["*.html", "*.js", "*.ts", "*.vue", "*.jsx", "*.tsx"],
        "detect_regex": r"document\.cookie|setCookie|cookieStore|js-cookie|cookieConsent|cookieBanner|cookieConsentBanner|acceptCookies|cookiePreferences",
        "citations": [
            "Directive 2002/58/EC (ePrivacy Directive)",
            "EDPB Guidelines on Cookie Consent Banners"
        ],
        "impact_desc": "Non-essential cookies must remain disabled by default until explicit consent is recorded.",
        "migration_steps": [
            "Implement or integrate a compliant cookie preference manager banner.",
            "Audit all active scripts and delay analytical or marketing cookies until user opts in."
        ]
    },
    "Local storage": {
        "platform": "web",
        "severity": "high",
        "keywords": ["local storage", "localstorage", "setitem"],
        "detect_files": ["*.html", "*.js", "*.ts", "*.vue", "*.jsx", "*.tsx"],
        "detect_regex": r"localStorage\.setItem|localStorage\[",
        "citations": [
            "Regulation (EU) 2016/679 (General Data Protection Regulation)",
            "OWASP Web Security Testing Guide: Client-Side Storage"
        ],
        "impact_desc": "Avoid storing unencrypted sensitive user information, credentials, or session tokens in plain text.",
        "migration_steps": [
            "Audit localStorage for occurrences of JWTs, credentials, or personal profiles.",
            "Migrate sensitive session tokens to secure, HttpOnly, SameSite cookies."
        ]
    },
    "IndexedDB": {
        "platform": "web",
        "severity": "medium",
        "keywords": ["indexeddb", "indexeddb.open"],
        "detect_files": ["*.html", "*.js", "*.ts", "*.vue", "*.jsx", "*.tsx"],
        "detect_regex": r"indexedDB\.open",
        "citations": [
            "Regulation (EU) 2016/679 (General Data Protection Regulation)",
            "OWASP Client-Side Storage Security Guidelines"
        ],
        "impact_desc": "Client-side structured databases must respect user privacy consent and support reliable cleanup/deletion on logout.",
        "migration_steps": [
            "Implement complete IndexedDB instance purge flows upon user logout or deletion request.",
            "Apply cryptographic shielding where sensitive files are cached locally."
        ]
    },
    "Session storage": {
        "platform": "web",
        "severity": "medium",
        "keywords": ["session storage", "sessionstorage", "sessionstorage.setitem"],
        "detect_files": ["*.html", "*.js", "*.ts", "*.vue", "*.jsx", "*.tsx"],
        "detect_regex": r"sessionStorage\.setItem|sessionStorage\[",
        "citations": [
            "Regulation (EU) 2016/679 (General Data Protection Regulation)",
            "OWASP Session Management Guidelines"
        ],
        "impact_desc": "Temporary session parameters must be restricted from script access where sensitive data is loaded.",
        "migration_steps": [
            "Enforce strict clearing of sessionStorage details immediately when tabs are destroyed.",
            "Verify that no highly sensitive access key is kept unmitigated in sessionStorage."
        ]
    },
    "Tracking technologies": {
        "platform": "web",
        "severity": "high",
        "keywords": ["tracking pixel", "google analytics", "facebook pixel", "hotjar", "analytics tag"],
        "detect_files": ["*.html", "*.js", "*.ts", "*.vue", "*.jsx", "*.tsx"],
        "detect_regex": r"google-analytics|ga\(|fbq\(|facebook-pixel|hotjar|gtag",
        "citations": [
            "Directive 2002/58/EC (ePrivacy Directive)",
            "EDPB Guidelines on Tracking Technologies"
        ],
        "impact_desc": "Analytical, promotional, or telemetry trackers must not initialize until explicit consent is given.",
        "migration_steps": [
            "Map all active pixel tags and script inclusions.",
            "Enforce conditional loading based on the active state of the user's consent preferences."
        ]
    }
}

# 16 Built-in Mock Privacy Policy updates representing monitored feeds
MOCK_PRIVACY_UPDATES = [
    {
        "id": "PRIV-MOCK-APPLE-MANIFEST",
        "requirement": "Privacy Manifest",
        "title": "Apple App Store Upload Enforcement for Privacy Manifests",
        "description": "Apple announced final enforcement of Privacy Manifest files. Submissions containing unrecognized or missing PrivacyInfo.xcprivacy configurations will be immediately rejected at the App Store Connect upload-time gate.",
        "link": "https://developer.apple.com/news/?id=privacy-manifest-enforce",
        "pubDate": "Mon, 18 May 2026 10:00:00 GMT"
    },
    {
        "id": "PRIV-MOCK-APPLE-REQUIRED-REASON",
        "requirement": "Required Reason APIs",
        "title": "Stricter Verification on Required Reason APIs",
        "description": "Apple is initiating rigorous automated checking for system uptime, file timestamp, and user default API calls. Developers must match each call to an approved reason code in their bundled manifest.",
        "link": "https://developer.apple.com/news/?id=required-reason-apis",
        "pubDate": "Tue, 19 May 2026 11:00:00 GMT"
    },
    {
        "id": "PRIV-MOCK-APPLE-ATT",
        "requirement": "App Tracking Transparency",
        "title": "Enhanced ATT Enforcement in Saturated Markets",
        "description": "The App Store Review team will reject applications accessing third-party tracking, analytics, or attribution services without exhibiting the App Tracking Transparency consent dialogue first.",
        "link": "https://developer.apple.com/news/?id=att-enforce",
        "pubDate": "Wed, 20 May 2026 12:00:00 GMT"
    },
    {
        "id": "PRIV-MOCK-APPLE-NUTRITION",
        "requirement": "Privacy Nutrition Labels",
        "title": "App Store Privacy Nutrition Label Discrepancy Audits",
        "description": "Apple is updating review systems to audit network traffic of submitted apps, cross-referencing findings against declared Nutrition Labels. Discrepancies lead to immediate rejection.",
        "link": "https://developer.apple.com/news/?id=nutrition-label-audits",
        "pubDate": "Thu, 21 May 2026 13:00:00 GMT"
    },
    {
        "id": "PRIV-MOCK-ANDROID-SAFETY",
        "requirement": "Data Safety",
        "title": "Google Play Store Data Safety Questionnaire Compliance",
        "description": "Google Play is updating Data Safety expectations. Apps sharing user data with external attribution or push notification services must declare these actions granularly to avoid account suspensions.",
        "link": "https://support.google.com/googleplay/android-developer/answer/datasafety",
        "pubDate": "Fri, 22 May 2026 14:00:00 GMT"
    },
    {
        "id": "PRIV-MOCK-ANDROID-USERDATA",
        "requirement": "User Data Policy",
        "title": "Stricter Account Deletion and Personal Data Policy Requirements",
        "description": "Google Play reminds developers that apps permitting account creation must support in-app account deletion and must supply a valid, responsive web-based data deletion URL in the listing details.",
        "link": "https://support.google.com/googleplay/android-developer/answer/userdata",
        "pubDate": "Sat, 23 May 2026 15:00:00 GMT"
    },
    {
        "id": "PRIV-MOCK-ANDROID-ADID",
        "requirement": "Advertising ID",
        "title": "Google Play Advertising ID Permission and Deletion Policy",
        "description": "Under Android 12+, developers targeting higher API levels who access the Advertising ID must explicitly declare the AD_ID permission in their manifest and provide opt-out preferences.",
        "link": "https://support.google.com/googleplay/android-developer/answer/adid-perm",
        "pubDate": "Sun, 24 May 2026 16:00:00 GMT"
    },
    {
        "id": "PRIV-MOCK-ANDROID-RUNTIME-PERM",
        "requirement": "Runtime permissions",
        "title": "Sensitive Scope Audits of Android Runtime Permissions",
        "description": "Google Play static analysis scans will flag apps declaring sensitive permissions in their AndroidManifest.xml if they bypass dynamic verification prompts or logical explanations.",
        "link": "https://developer.android.com/guide/topics/permissions",
        "pubDate": "Mon, 25 May 2026 10:00:00 GMT"
    },
    {
        "id": "PRIV-MOCK-ANDROID-BG-LOC",
        "requirement": "Background location",
        "title": "Enforcement Actions on ACCESS_BACKGROUND_LOCATION Declarations",
        "description": "Google is executing a strict sweep of background location access. Only highly essential user-facing features will be granted permission; all others must restrict location to foreground actions.",
        "link": "https://support.google.com/googleplay/android-developer/answer/bg-location",
        "pubDate": "Tue, 26 May 2026 11:00:00 GMT"
    },
    {
        "id": "PRIV-MOCK-ANDROID-HEALTH",
        "requirement": "Health permissions",
        "title": "Google Play Health Connect Data Permission Declarations",
        "description": "Apps interacting with Health Connect APIs must complete the dedicated health declaration form and must show a specialized in-app privacy policy prior to querying permissions.",
        "link": "https://support.google.com/googleplay/android-developer/answer/health-connect",
        "pubDate": "Wed, 27 May 2026 12:00:00 GMT"
    },
    {
        "id": "PRIV-MOCK-WEB-GDPR",
        "requirement": "GDPR",
        "title": "EDPB Updates Guidelines on Cookie Consent and GDPR Data Erasure",
        "description": "The European Data Protection Board finalized consent rules. Web entities are required to support clear consent revoke paths and ensure absolute right-to-erase triggers purge all analytical copies.",
        "link": "https://edpb.europa.eu/our-work-tools/general-guidance",
        "pubDate": "Thu, 28 May 2026 13:00:00 GMT"
    },
    {
        "id": "PRIV-MOCK-WEB-COOKIE",
        "requirement": "Cookie consent",
        "title": "European Union ePrivacy Compliance Sweep for Tracker Placement",
        "description": "ePrivacy updates mandate strict opt-in cookie banners. Non-essential cookies, analytics tools, or marketing pixels placed prior to explicit opt-in are subjected to direct regulatory prosecution.",
        "link": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex:32002L0058",
        "pubDate": "Fri, 29 May 2026 14:00:00 GMT"
    },
    {
        "id": "PRIV-MOCK-WEB-LOCALSTORAGE",
        "requirement": "Local storage",
        "title": "OWASP Guidance on Client-Side Local Storage Security",
        "description": "New OWASP security releases highlight threats regarding unencrypted JWTs, access credentials, or PII cached in localStorage. Developers are urged to shift sensitive secrets to secure HTTP-only cookies.",
        "link": "https://owasp.org/www-project-web-security-testing-guide",
        "pubDate": "Sat, 30 May 2026 15:00:00 GMT"
    },
    {
        "id": "PRIV-MOCK-WEB-INDEXEDDB",
        "requirement": "IndexedDB",
        "title": "Structured Storage Security and Deletion Best Practices",
        "description": "GDPR requirements mandate complete structured database cleanup. Ensure all tables and client objects created via IndexedDB are securely wiped during deletion flows or user account logout.",
        "link": "https://owasp.org/www-project-web-security-testing-guide",
        "pubDate": "Sun, 31 May 2026 16:00:00 GMT"
    },
    {
        "id": "PRIV-MOCK-WEB-SESSIONSTORAGE",
        "requirement": "Session storage",
        "title": "Session Hijacking Mitigation and Storage Restrictions",
        "description": "Security advisories emphasize locking sessionStorage objects during active browser cycles. Temporary secrets must be mitigated and cleared immediately upon session window termination.",
        "link": "https://owasp.org/www-project-web-security-testing-guide",
        "pubDate": "Mon, 01 Jun 2026 10:00:00 GMT"
    },
    {
        "id": "PRIV-MOCK-WEB-TRACKING",
        "requirement": "Tracking technologies",
        "title": "Directive Requirements on Third-Party Tracking Pixels",
        "description": "Under regional guidelines, tracking pixels (Facebook, Google Analytics, Hotjar) cannot load or fetch telemetry metadata dynamically on page loading before obtaining consent.",
        "link": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex:32002L0058",
        "pubDate": "Tue, 02 Jun 2026 11:00:00 GMT"
    }
]


def scan_codebase_for_privacy_signals(start_dir="."):
    """
    Scans the repository codebase for file patterns and regex signals
    matching the 16 requirements. Skipping exclude folders.
    """
    matches = {req: [] for req in PRIVACY_REQUIREMENTS}
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
        "assets"
    }

    # Compile patterns and regex
    compiled_requirements = {}
    for req_name, info in PRIVACY_REQUIREMENTS.items():
        file_pats = info["detect_files"]
        regex_str = info["detect_regex"]
        compiled_pats = []
        for p in file_pats:
            if p.startswith("*."):
                compiled_pats.append(re.compile(r".*\." + re.escape(p[2:]) + "$", re.IGNORECASE))
            else:
                compiled_pats.append(re.compile(r".*" + re.escape(p) + "$", re.IGNORECASE))
        compiled_requirements[req_name] = {
            "patterns": compiled_pats,
            "regex": re.compile(regex_str, re.IGNORECASE)
        }

    for root, dirs, files in os.walk(start_dir):
        # Prune excluded directories in-place
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.endswith("Tests") and not d.endswith("test")]

        for file in files:
            filepath = os.path.join(root, file)
            # Skip monitor scripts to avoid self-referencing matches
            if "monitor-privacy" in file or "monitor-privacy-test" in file:
                continue

            for req_name, compiled in compiled_requirements.items():
                # Check if file name matches file patterns
                is_file_match = False
                for pat in compiled["patterns"]:
                    if pat.match(file) or pat.match(filepath):
                        is_file_match = True
                        break

                if is_file_match:
                    try:
                        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                            for i, line in enumerate(f, 1):
                                if compiled["regex"].search(line):
                                    matches[req_name].append({
                                        "file": filepath,
                                        "line_num": i,
                                        "content": line.strip()[:100],
                                        "matched_pattern": compiled["regex"].pattern
                                    })
                                    # Break to avoid duplicating lines for the same requirement
                                    break
                    except Exception:
                        pass
    return matches


def parse_rss_feed(url):
    """
    Fetches and parses RSS/Atom feeds from a live endpoint.
    """
    items = []
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (PrivacyComplianceMonitor/1.0)"}
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

                    items.append({
                        "title": title.strip(),
                        "description": desc.strip() if desc else "",
                        "link": link.strip(),
                        "pubDate": pub_date.strip(),
                    })
    except Exception as e:
        print(f"Warning: Failed to fetch live feed {url}: {e}", file=sys.stderr)
    return items


def classify_announcements(announcements, keywords_filter=None):
    """
    Classifies incoming RSS or custom announcements into the 16 requirements.
    """
    classified_updates = []

    for ann in announcements:
        title = ann.get("title", "")
        desc = ann.get("description", "")
        text_to_search = (title + " " + desc).lower()

        if keywords_filter:
            if not any(k.lower() in text_to_search for k in keywords_filter):
                continue

        # Check matched requirements
        matched_reqs = []
        for req_name, info in PRIVACY_REQUIREMENTS.items():
            for kw in info["keywords"]:
                if kw.lower() in text_to_search:
                    matched_reqs.append(req_name)
                    break

        if not matched_reqs and ann.get("requirement"):
            matched_reqs.append(ann["requirement"])

        if matched_reqs:
            for req in matched_reqs:
                classified_updates.append({
                    "id": ann.get("id", "PRIV-UPDATE-" + str(hash(title))[:6]),
                    "requirement": req,
                    "title": title,
                    "description": desc,
                    "link": ann.get("link", ""),
                    "pubDate": ann.get("pubDate", "")
                })
    return classified_updates


def generate_pull_request_draft(updates, scan_results):
    """
    Generates a draft of a Pull Request containing EXACTLY 15 required non-vague sections.
    Ensures that it is entirely emoji-free.
    """
    citations_list = []
    affected_files_set = set()
    risk_assessment_list = []
    migration_steps_list = []
    impl_checklist_list = []
    test_checklist_list = []
    breaking_changes_list = []

    for idx, u in enumerate(updates, 1):
        req_name = u["requirement"]
        info = PRIVACY_REQUIREMENTS[req_name]
        citations_list.append(f"Official Citations for {req_name}:")
        for cit in info["citations"]:
            citations_list.append(f"- Priority 1 (Official Reference): {cit}")
        citations_list.append(f"- Announcement Context: {u['title']} ({u['link']})")

        # Affected files
        files = scan_results.get(req_name, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        # Risk level and analysis
        risk_lvl = info["severity"].upper()
        risk_assessment_list.append(
            f"- **{req_name} ({risk_lvl} Risk)**: Failure to comply will lead to storefront rejection or regulatory audit."
        )

        # Migration steps
        migration_steps_list.append(f"- **{req_name} Migration**:")
        for step in info["migration_steps"]:
            migration_steps_list.append(f"  * {step}")

        # Checklists
        impl_checklist_list.append(f"- [ ] Implement compliance declarations for {req_name}.")
        impl_checklist_list.append(f"  * Verify that `{info['detect_regex']}` occurrences are correctly handled.")

        # Test items
        test_checklist_list.append(f"- [ ] Verify {req_name} behavior against standard test specifications.")

    citations_str = "\n".join(citations_list)

    if affected_files_set:
        affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set)))
    else:
        affected_files_str = "- No specific files containing matching requirement signals were automatically detected. Perform manual review of configuration declarations."

    risk_str = "\n".join(risk_assessment_list)
    migration_str = "\n".join(migration_steps_list)
    impl_str = "\n".join(impl_checklist_list)
    test_str = "\n".join(test_checklist_list)

    pr_template = f"""# PULL REQUEST DRAFT: Mobile and Web Privacy Compliance Synchronization

## 1. Summary
This pull request introduces critical configuration parameters and code adaptations to ensure complete alignment with 16 distinct Apple, Android, and Web privacy requirements. It remediates identified gaps and ensures compliance with global privacy regulations and developer policies.

## 2. Background
Ensuring user privacy and security is a primary release gate across Apple, Android, and Web platforms. This sync aligns current repository files with global mandates, preventing build rejections or administrative account sanctions during storefront distribution.

## 3. Regulatory change
Platform policies and international regulations enforce strict transparency obligations, cookie controls, data safety declarations, and manifest files. These updates implement the necessary technical structures to meet these evolving security-by-design and privacy-by-design standards.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_str}
- Overall Risk Standing: High priority compliance sync. Missing declarations will cause direct build or publication rejection during storefront submission.

## 7. Migration steps
{migration_str}

## 8. Backward compatibility
All modifications are fully backward-compatible. Configured keys and metadata updates do not alter existing application logic or deprecate public-facing interface components in a breaking manner.

## 9. Implementation checklist
{impl_str}
- [ ] Perform a full static scan using the automated compliance guard scripts.

## 10. Testing checklist
{test_str}
- [ ] Confirm clean compilation across development and production configurations.
- [ ] Audit cookie placement and verify local client-side storage boundaries manually in browser devtools.

## 11. Documentation checklist
- [ ] Document all completed compliance updates in docs/PRIVACY-POLICY-MIGRATION.md.
- [ ] Ensure that privacy policy links are live and reachable across all storefront listings.

## 12. Compliance impact
- Guarantees continuous build validation and uninterrupted storefront delivery.
- Aligns product storage boundaries with global data minimisation requirements, shielding the product from regulatory scrutiny.

## 13. Breaking changes
- There are no structural breaking changes introduced by these metadata alignment activities.

## 14. Review checklist
- [ ] Confirm that all required keys are correctly registered and mapped in configuration folders.
- [ ] Ensure the entire pull request is 100 percent emoji-free.

## 15. Approver recommendations
Ensure that the technical and legal teams review the compiled Data Safety and Privacy Nutrition Label mapping prior to production distribution. It is recommended to perform continuous regression checks using the local test harness before build sign-off.
"""
    return pr_template


def update_documentation_report(updates, output_filepath):
    """
    Generates and updates docs/PRIVACY-POLICY-MIGRATION.md.
    Ensures that it is entirely emoji-free.
    """
    lines = [
        "<!-- PRIVACY_POLICY_MONITOR_START -->",
        "# Mobile and Web Privacy Compliance Migration & Requirements Report",
        "",
        "This report is continuously generated and updated by scripts/monitor-privacy.py to track active privacy compliance gaps.",
        "",
        "## Monitored Requirements Update Log",
        "",
    ]

    for idx, u in enumerate(updates, 1):
        req_name = u["requirement"]
        lines.append(f"### {idx}. [{req_name}] {u['title']}")
        lines.append(f"- **Published Date**: {u['pubDate']}")
        lines.append(f"- **Official Resource**: [{u['link']}]({u['link']})")
        lines.append(f"- **Description**: {u['description']}")
        lines.append("")

    lines.append("## Automated Migration Recommendations & Implementation Tasks")
    lines.append("")

    for req_name, info in PRIVACY_REQUIREMENTS.items():
        lines.append(f"### Tasks for {req_name} ({info['platform'].capitalize()} Platform)")
        lines.append(f"- **Severity Level**: {info['severity'].upper()}")
        for idx, step in enumerate(info["migration_steps"], 1):
            lines.append(f"- [ ] **Task {idx}**: {step}")
        lines.append("")

    lines.append("<!-- PRIVACY_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"Privacy documentation report updated successfully at: {output_filepath}")
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor Mobile and Web Privacy Compliance Requirements"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live developer and regulatory feeds"
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
        default="docs/PRIVACY-POLICY-MIGRATION.md",
        help="Filepath to write migration tasks and logs",
    )
    parser.add_argument(
        "--pr-output",
        type=str,
        default="docs/PRIVACY_COMPLIANCE_PR_DRAFT.md",
        help="Filepath to save the drafted compliance PR",
    )
    parser.add_argument(
        "--json", action="store_true", help="Output report in JSON format to stdout"
    )
    parser.add_argument(
        "--simulate",
        type=str,
        help="Simulate an update by requirement name (e.g., 'GDPR') or 'all' to simulate all 16 requirements",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print verbose execution details"
    )

    args = parser.parse_args()

    # Determine announcements
    announcements = []

    if args.simulate:
        if args.simulate.lower() == "all":
            for m in MOCK_PRIVACY_UPDATES:
                announcements.append(m)
        else:
            matched_req = None
            for req_name in PRIVACY_REQUIREMENTS:
                if args.simulate.lower() in req_name.lower():
                    matched_req = req_name
                    break
            if matched_req:
                for m in MOCK_PRIVACY_UPDATES:
                    if m["requirement"] == matched_req:
                        announcements.append(m)
            else:
                # Custom simulation fallback
                announcements.append({
                    "id": "PRIV-SIM-" + str(hash(args.simulate))[:6],
                    "requirement": "GDPR",
                    "title": f"Simulated Policy update for {args.simulate}",
                    "description": f"This is a simulated announcement representing privacy updates for {args.simulate}.",
                    "link": "https://edpb.europa.eu",
                    "pubDate": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
                })
    elif args.live:
        print("Fetching live privacy developer and regulatory RSS feeds...")
        announcements.extend(parse_rss_feed("https://android-developers.googleblog.com/feeds/posts/default"))
        announcements.extend(parse_rss_feed("https://developer.apple.com/news/rss/news.rss"))

    # Fallback to default mock updates if needed
    if not announcements or args.mock or (not args.live and not args.simulate):
        if args.mock and args.mock != "inline" and os.path.exists(args.mock):
            try:
                with open(args.mock, "r") as f:
                    announcements.extend(json.load(f))
            except Exception as e:
                print(f"Warning: Failed to load custom mock file {args.mock}: {e}", file=sys.stderr)
                announcements.extend(MOCK_PRIVACY_UPDATES)
        else:
            announcements.extend(MOCK_PRIVACY_UPDATES)

    # Classify updates
    keywords_filter = [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    classified_updates = classify_announcements(announcements, keywords_filter)

    if not classified_updates:
        print("No classified updates matched the active filters.")
        sys.exit(0)

    if args.verbose:
        print(f"Monitored and classified {len(classified_updates)} privacy updates.")

    # Codebase scan
    scan_results = scan_codebase_for_privacy_signals(args.dir)

    # Output to stdout or files
    if args.json:
        report = []
        for u in classified_updates:
            req = u["requirement"]
            report.append({
                "announcement_title": u["title"],
                "announcement_pubDate": u["pubDate"],
                "announcement_link": u["link"],
                "requirement": req,
                "platform": PRIVACY_REQUIREMENTS[req]["platform"],
                "severity": PRIVACY_REQUIREMENTS[req]["severity"],
                "affected_files": [f["file"] for f in scan_results.get(req, [])],
                "migration_tasks": PRIVACY_REQUIREMENTS[req]["migration_steps"]
            })
        print(json.dumps(report, indent=2))
    else:
        # File generation
        os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
        update_documentation_report(classified_updates, args.output_docs)

        os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
        pr_draft = generate_pull_request_draft(classified_updates, scan_results)
        try:
            with open(args.pr_output, "w", encoding="utf-8") as f:
                f.write(pr_draft)
            print(f"Privacy PR draft written successfully to: {args.pr_output}")
        except Exception as e:
            print(f"Error writing PR draft to {args.pr_output}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
