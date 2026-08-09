#!/usr/bin/env python3
"""
Mobile and Web Privacy Compliance Requirements Monitoring Utility.
Tracks 16 distinct Apple, Android, and Web privacy requirements.
"""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json

# The 16 tracked privacy requirement categories
CATEGORIES = [
    "Privacy Manifest",
    "Required Reason APIs",
    "App Tracking Transparency",
    "Privacy Nutrition Labels",
    "Data Safety",
    "User Data Policy",
    "Advertising ID",
    "Runtime permissions",
    "Background location",
    "Health permissions",
    "GDPR",
    "Cookie consent",
    "Local storage",
    "IndexedDB",
    "Session storage",
    "Tracking technologies"
]

# Keywords used to classify incoming policy announcements/articles into the 16 categories
CATEGORY_KEYWORDS = {
    "Privacy Manifest": ["privacy manifest", "privacyinfo.xcprivacy", "xcprivacy", "manifest"],
    "Required Reason APIs": ["required reason api", "required reason", "userdefaults", "nsfilemanager", "systemuptime", "processinfo"],
    "App Tracking Transparency": ["app tracking transparency", "att", "idfa", "tracking authorization", "tracking usage description"],
    "Privacy Nutrition Labels": ["privacy nutrition label", "nutrition label", "privacy label", "app store connect privacy"],
    "Data Safety": ["data safety", "datasafety", "google play data safety"],
    "User Data Policy": ["user data policy", "prominent disclosure", "data deletion", "account deletion", "personal data collection"],
    "Advertising ID": ["advertising id", "advertising_id", "ad_id", "gaid", "google play services advertising id"],
    "Runtime permissions": ["runtime permission", "requestpermissions", "checkselfpermission", "shouldshowrequestpermissionrationale"],
    "Background location": ["background location", "access_background_location"],
    "Health permissions": ["health permission", "health connect", "healthconnect", "body_sensors", "read_steps", "read_heart_rate"],
    "GDPR": ["gdpr", "general data protection regulation", "opt-in consent", "right to be forgotten", "european data protection board", "edpb"],
    "Cookie consent": ["cookie consent", "cookie banner", "cookie preference", "eprivacy"],
    "Local storage": ["local storage", "localstorage", "setitem", "web storage"],
    "IndexedDB": ["indexeddb", "indexed database", "createobjectstore"],
    "Session storage": ["session storage", "sessionstorage"],
    "Tracking technologies": ["tracking technology", "tracking script", "google analytics", "facebook pixel", "hotjar", "tracking pixel", "analytic pixel"]
}

# Codebase signals (regex patterns) to find files affected by each of the 16 categories
CATEGORY_SIGNALS = {
    "Privacy Manifest": [
        r"PrivacyInfo\.xcprivacy",
        r"NSPrivacyAccessedAPITypes",
        r"NSPrivacyTracking",
        r"NSPrivacyTrackingDomains"
    ],
    "Required Reason APIs": [
        r"UserDefaults",
        r"NSFileManager",
        r"systemUptime",
        r"ProcessInfo",
        r"stat"
    ],
    "App Tracking Transparency": [
        r"ATTrackingManager",
        r"requestTrackingAuthorization",
        r"NSUserTrackingUsageDescription"
    ],
    "Privacy Nutrition Labels": [
        r"privacyNutritionLabels",
        r"privacy-nutrition-labels",
        r"NSPrivacyCollectedDataTypes"
    ],
    "Data Safety": [
        r"firebase-analytics",
        r"appsflyer",
        r"adjust",
        r"com\.facebook",
        r"Data Safety"
    ],
    "User Data Policy": [
        r"personalData",
        r"deleteAccount",
        r"delete_account",
        r"User Data Policy"
    ],
    "Advertising ID": [
        r"com\.google\.android\.gms\.permission\.AD_ID",
        r"AD_ID",
        r"getAdvertisingIdInfo"
    ],
    "Runtime permissions": [
        r"requestPermissions",
        r"checkSelfPermission",
        r"shouldShowRequestPermissionRationale"
    ],
    "Background location": [
        r"ACCESS_BACKGROUND_LOCATION",
        r"BackgroundLocation"
    ],
    "Health permissions": [
        r"HealthConnectClient",
        r"com\.google\.android\.gms\.permission\.HealthConnect",
        r"READ_STEPS",
        r"READ_HEART_RATE"
    ],
    "GDPR": [
        r"GDPR",
        r"opt-in",
        r"privacyConsent",
        r"deletePersonalData"
    ],
    "Cookie consent": [
        r"document\.cookie",
        r"cookieStore",
        r"cookieConsent",
        r"cookieBanner",
        r"cookieConsentBanner"
    ],
    "Local storage": [
        r"localStorage\.setItem",
        r"localStorage"
    ],
    "IndexedDB": [
        r"indexedDB\.open",
        r"indexedDB",
        r"createObjectStore"
    ],
    "Session storage": [
        r"sessionStorage\.setItem",
        r"sessionStorage"
    ],
    "Tracking technologies": [
        r"gtag",
        r"fbq",
        r"google-analytics",
        r"trackingPixel",
        r"analytics\.js",
        r"hotjar"
    ]
}

# Source trust domains and keywords for verification
TRUST_HIERARCHY = {
    "Priority 1": "Official sources (European Commission, EUR-Lex, Official Journal, ENISA, EDPB, FTC, NIST, CISA, ICO, Government publications, Apple Developer, Android Developer)",
    "Priority 2": "Reputable news (Reuters, AP, Bloomberg)",
    "Priority 3": "Academic papers",
    "Priority 4": "Industry blogs",
    "Priority 5": "LinkedIn, Reddit, Twitter, AI generated summaries"
}

# 16 Comprehensive Mock Announcements for all 16 categories
MOCK_ANNOUNCEMENTS = [
    {
        "id": "PRIV-MOCK-APPLE-MANIFEST",
        "category": "Privacy Manifest",
        "title": "Apple Mandatory Privacy Manifest Requirements for App Store Submissions",
        "description": "Apple enforces mandatory Privacy Manifests (PrivacyInfo.xcprivacy) for all newly submitted apps and third-party SDK updates. The manifest must accurately declare data collection, tracking domains, and required reason API usage.",
        "link": "https://developer.apple.com/support/privacy-manifest-files",
        "pubDate": "Mon, 15 Jun 2026 10:00:00 PDT"
    },
    {
        "id": "PRIV-MOCK-APPLE-REQUIRED-REASON",
        "category": "Required Reason APIs",
        "title": "Apple Stricter Required Reason API Usage Guidelines",
        "description": "To prevent fingerprinting, Apple requires developers to specify approved reason codes in their Privacy Manifest if they access designated Required Reason APIs, such as UserDefaults, file timestamps, system uptime, and disk space.",
        "link": "https://developer.apple.com/documentation/bundleresources/privacy_manifest_files/describing_use_of_required_reason_api",
        "pubDate": "Tue, 16 Jun 2026 11:00:00 PDT"
    },
    {
        "id": "PRIV-MOCK-APPLE-ATT",
        "category": "App Tracking Transparency",
        "title": "App Tracking Transparency Framework Reinforcement",
        "description": "Developers must display the App Tracking Transparency (ATT) prompt via ATTrackingManager and obtain user permission before collecting the advertising identifier (IDFA) or tracking users across other apps or websites.",
        "link": "https://developer.apple.com/app-store/user-privacy-and-data-use",
        "pubDate": "Wed, 17 Jun 2026 12:00:00 PDT"
    },
    {
        "id": "PRIV-MOCK-APPLE-NUTRITION",
        "category": "Privacy Nutrition Labels",
        "title": "Apple App Store Privacy Nutrition Labels Questionnaire Update",
        "description": "Apple requires developers to complete the self-reported Privacy Nutrition Labels in App Store Connect. All declared data collection and usage practices must match actual in-app behaviors.",
        "link": "https://developer.apple.com/app-store/app-privacy-details",
        "pubDate": "Thu, 18 Jun 2026 13:00:00 PDT"
    },
    {
        "id": "PRIV-MOCK-ANDROID-SAFETY",
        "category": "Data Safety",
        "title": "Google Play Store Data Safety Form Compliance Verification",
        "description": "Google Play enforces strict validation of the Data Safety section. Submissions are dynamically scanned for compiled libraries and network activities to verify they align with the declared Data Safety form.",
        "link": "https://support.google.com/googleplay/android-developer/answer/10787469",
        "pubDate": "Fri, 19 Jun 2026 14:00:00 PDT"
    },
    {
        "id": "PRIV-MOCK-ANDROID-USERDATA",
        "category": "User Data Policy",
        "title": "Google Play User Data Protection and Deletion Policy",
        "description": "Google Play User Data policy requires prominent disclosures and explicit user consent before collecting any personal or sensitive data. Apps with in-app account creation must offer an in-app and web account deletion option.",
        "link": "https://support.google.com/googleplay/android-developer/answer/9899234",
        "pubDate": "Sat, 20 Jun 2026 15:00:00 PDT"
    },
    {
        "id": "PRIV-MOCK-ANDROID-ADID",
        "category": "Advertising ID",
        "title": "Google Play Advertising ID Policy and com.google.android.gms.permission.AD_ID",
        "description": "Apps targeting Android 12 or higher that use the Google Play Services Advertising ID must declare the AD_ID permission in their manifest and provide user options to reset or delete the ID.",
        "link": "https://support.google.com/googleplay/android-developer/answer/6048248",
        "pubDate": "Sun, 21 Jun 2026 16:00:00 PDT"
    },
    {
        "id": "PRIV-MOCK-ANDROID-PERM",
        "category": "Runtime permissions",
        "title": "Android Runtime Permission Model and Dynamic Checks",
        "description": "Android runtime permissions must be requested dynamically when the app accesses sensitive capabilities like camera, contacts, or storage. Rationale must be explained before requesting the permission.",
        "link": "https://developer.android.com/guide/topics/permissions/overview",
        "pubDate": "Mon, 22 Jun 2026 17:00:00 PDT"
    },
    {
        "id": "PRIV-MOCK-ANDROID-LOCATION",
        "category": "Background location",
        "title": "Google Play Restriction on ACCESS_BACKGROUND_LOCATION Permission",
        "description": "Google Play strictly limits background location access. Developers must justify that background location is crucial to the app's core feature, and provide a clear prominent disclosure to the user.",
        "link": "https://support.google.com/googleplay/android-developer/answer/9799150",
        "pubDate": "Tue, 23 Jun 2026 18:00:00 PDT"
    },
    {
        "id": "PRIV-MOCK-ANDROID-HEALTH",
        "category": "Health permissions",
        "title": "Google Play Health Connect Integration and Fitness Permissions",
        "description": "Accessing health or fitness data via Health Connect requires specialized developer declarations in the Play Console, a detailed health privacy policy, and prominent in-app disclosures.",
        "link": "https://support.google.com/googleplay/android-developer/answer/12253906",
        "pubDate": "Wed, 24 Jun 2026 19:00:00 PDT"
    },
    {
        "id": "PRIV-MOCK-WEB-GDPR",
        "category": "GDPR",
        "title": "European Union General Data Protection Regulation Enforcement Guidelines",
        "description": "The EDPB issues guidance on valid GDPR consent. Processing EU residents' personal data requires explicit opt-in, clear information, data portability, and a functional right to be forgotten (data erasure).",
        "link": "https://www.edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en",
        "pubDate": "Thu, 25 Jun 2026 20:00:00 PDT"
    },
    {
        "id": "PRIV-MOCK-WEB-COOKIE",
        "category": "Cookie consent",
        "title": "ePrivacy Directive Cookie Consent Banner Requirements",
        "description": "Websites targeting EU users must present a compliant Cookie Consent banner that blocks non-essential cookies (such as marketing or analytics) until explicit, active consent is granted.",
        "link": "https://commission.europa.eu/cookies_en",
        "pubDate": "Fri, 26 Jun 2026 21:00:00 PDT"
    },
    {
        "id": "PRIV-MOCK-WEB-LOCAL",
        "category": "Local storage",
        "title": "Secure Client-Side Local Storage Guidelines under GDPR",
        "description": "Stashing unencrypted sensitive information, JWT tokens, or credentials in local web storage (localStorage) is highly discouraged. Stored data must respect user consent and remain protected from cross-site scripting (XSS) extraction.",
        "link": "https://commission.europa.eu/law/law-topic/data-protection_en",
        "pubDate": "Sat, 27 Jun 2026 22:00:00 PDT"
    },
    {
        "id": "PRIV-MOCK-WEB-INDEXED",
        "category": "IndexedDB",
        "title": "IndexedDB Structured Client-Side Databases and User Consent Control",
        "description": "Large-scale offline or structured data stored locally in browser IndexedDB instances must follow user privacy preferences, use encryption where sensitive data is involved, and perform cleanups upon logout.",
        "link": "https://commission.europa.eu/law/law-topic/data-protection_en",
        "pubDate": "Sun, 28 Jun 2026 23:00:00 PDT"
    },
    {
        "id": "PRIV-MOCK-WEB-SESSION",
        "category": "Session storage",
        "title": "Temporary Browser Session Storage Security Recommendations",
        "description": "Data kept in sessionStorage must be handled securely, ensuring sensitive credentials are not exposed to untrusted scripts, and are thoroughly purged once the user closes the tab or logs out.",
        "link": "https://commission.europa.eu/law/law-topic/data-protection_en",
        "pubDate": "Mon, 29 Jun 2026 09:00:00 PDT"
    },
    {
        "id": "PRIV-MOCK-WEB-TRACKING",
        "category": "Tracking technologies",
        "title": "Tracking Technologies, Scripts, and Invisible Pixels Consent Management",
        "description": "Third-party analytical scripts (Google Analytics, Facebook Pixel, Hotjar) must be explicitly controlled and completely disabled by default until the user accepts cookie or tracking preferences.",
        "link": "https://www.edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en",
        "pubDate": "Tue, 30 Jun 2026 10:00:00 PDT"
    },
    # Unverified announcements to test blocking
    {
        "id": "PRIV-MOCK-UNVERIFIED-BLOG",
        "category": "GDPR",
        "title": "Unverified Industry Blog Rumors on GDPR Fines",
        "description": "A random industry blog claims GDPR rules are being changed next week to fine all websites without an immediate dark mode. This is an unverified blog post.",
        "link": "https://randomblogsite.com/gdpr-rumor",
        "pubDate": "Wed, 01 Jul 2026 11:00:00 PDT"
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
        "europa.eu", "eur-lex.europa.eu", "enisa.europa.eu", "edpb.europa.eu",
        "ftc.gov", "nist.gov", "cisa.gov", "ico.org.uk", "gov.uk", "gov.sg",
        "imda.gov.sg", "pdpc.gov.sg", "anpd.gov.br", "esafety.gov.au",
        "apple.com", "developer.apple.com", "android.com", "developer.android.com", "support.google.com"
    ]
    p1_keywords = [
        "european commission", "eur-lex", "official journal", "enisa", "edpb",
        "ftc", "nist", "cisa", "ico", "government publication", "imda", "pdpc",
        "anpd", "esafety commissioner", "federal register", "apple developer", "android developer"
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
                    common_terms = {"privacy", "gdpr", "consent", "android", "apple", "cookie"}
                    overlap = words.intersection(other_words).intersection(common_terms)
                    if overlap:
                        is_verified = True
                        break

    return priority, is_verified


def scan_codebase_for_privacy_signals(start_dir="."):
    """
    Scans the codebase for files containing signals related to each of the 16 privacy categories.
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
            if "monitor-privacy" in file:
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
    Classifies incoming announcements into the 16 Apple, Android, and Web privacy categories.
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
                        "id": ann.get("id", "PRIV-UPDATE-" + str(hash(title))[:6]),
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

        # Pull affected files
        files = scan_results.get(cat, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        # Category-specific details
        if cat == "Privacy Manifest":
            migration_steps.append(
                f"- **{cat}**: Add or update the PrivacyInfo.xcprivacy file in the iOS app bundle to declare tracking and data collection."
            )
            impl_checklist.append("- [ ] Create/Update PrivacyInfo.xcprivacy in iOS App Bundle.")
            risk_assessment.append(f"- *{cat}*: Immediate App Store Connect build rejection if Privacy Manifest is missing or incomplete.")
        elif cat == "Required Reason APIs":
            migration_steps.append(
                f"- **{cat}**: Declare active usage of designated Required Reason APIs (UserDefaults, NSFileManager, etc.) with valid, approved reason codes in the privacy manifest."
            )
            impl_checklist.append("- [ ] Map Required Reason APIs to approved codes in PrivacyInfo.xcprivacy.")
            risk_assessment.append(f"- *{cat}*: Direct App Store submission failure on detection of undeclared required reason API calls.")
        elif cat == "App Tracking Transparency":
            migration_steps.append(
                f"- **{cat}**: Request explicit tracking consent before invoking any marketing, profiling, or tracking SDKs."
            )
            impl_checklist.append("- [ ] Call ATTrackingManager.requestTrackingAuthorization prior to tracking SDK initialization.")
            risk_assessment.append(f"- *{cat}*: Binary rejection by Apple App Review if cross-app tracking occurs without ATT consent.")
        elif cat == "Privacy Nutrition Labels":
            migration_steps.append(
                f"- **{cat}**: Ensure declared App Store Connect privacy questionnaire labels are completely aligned with actual runtime data transmission."
            )
            impl_checklist.append("- [ ] Update App Store Connect Privacy Questionnaire to reflect all active tracking and collected user details.")
            risk_assessment.append(f"- *{cat}*: Metadata or review rejection due to discrepancy in self-reported labels and dynamic review traffic.")
        elif cat == "Data Safety":
            migration_steps.append(
                f"- **{cat}**: Align the Google Play Store Data Safety declarations with compiled SDKs and actual runtime network endpoints."
            )
            impl_checklist.append("- [ ] Review compiled libraries and ensure Play Console Data Safety form declarations match perfectly.")
            risk_assessment.append(f"- *{cat}*: Critical Google Play rejection due to silent or undeclared SDK data sharing.")
        elif cat == "User Data Policy":
            migration_steps.append(
                f"- **{cat}**: Build clear, prominent in-app disclosures and offer a reliable web and in-app account/data deletion portal."
            )
            impl_checklist.append("- [ ] Complete the Google Play Account Deletion section and publish a data deletion URL.")
            risk_assessment.append(f"- *{cat}*: Policy non-compliance leading to warnings and potential account suspension by Google Play.")
        elif cat == "Advertising ID":
            migration_steps.append(
                f"- **{cat}**: Declare com.google.android.gms.permission.AD_ID permission only with valid opt-out handles."
            )
            impl_checklist.append("- [ ] Configure AD_ID permission in AndroidManifest and verify opt-out flows.")
            risk_assessment.append(f"- *{cat}*: Google Play policy rejection if AD_ID permission is present without opt-out validation.")
        elif cat == "Runtime permissions":
            migration_steps.append(
                f"- **{cat}**: Implement dynamic runtime permission requests with prior user-facing rationale checks."
            )
            impl_checklist.append("- [ ] Verify checks for requestPermissions and handle permission denials gracefully.")
            risk_assessment.append(f"- *{cat}*: High crash rate or Play Store rejection on immediate, un-rationalized permission requests.")
        elif cat == "Background location":
            migration_steps.append(
                f"- **{cat}**: Restrict usage of ACCESS_BACKGROUND_LOCATION to vital features with prominent in-app disclosures."
            )
            impl_checklist.append("- [ ] Remove ACCESS_BACKGROUND_LOCATION unless essential and supported by a prominent disclosure view.")
            risk_assessment.append(f"- *{cat}*: Strict Google Play publishing blocks for unjustified background location permissions.")
        elif cat == "Health permissions":
            migration_steps.append(
                f"- **{cat}**: Formulate specialized health privacy statements and declare fitness/Health Connect permission usage."
            )
            impl_checklist.append("- [ ] Deploy a dedicated health data privacy statement and register Health Connect permissions.")
            risk_assessment.append(f"- *{cat}*: Account suspension and removal under Google Play Health Connect and medical policy rules.")
        elif cat == "GDPR":
            migration_steps.append(
                f"- **{cat}**: Deliver robust opt-in controls, data portability pathways, and right-to-be-forgotten buttons for EU users."
            )
            impl_checklist.append("- [ ] Integrate explicit opt-in forms and user-accessible data purge buttons for EU regions.")
            risk_assessment.append(f"- *{cat}*: Heavy fines and legal non-compliance risks under EU GDPR guidelines.")
        elif cat == "Cookie consent":
            migration_steps.append(
                f"- **{cat}**: Block writing or accessing non-essential cookies until active consent is recorded."
            )
            impl_checklist.append("- [ ] Integrate a Cookie Consent banner blocking non-essential cookie writes until approved.")
            risk_assessment.append(f"- *{cat}*: Regulatory fines by European national authorities for unlawful tracking cookie storage.")
        elif cat == "Local storage":
            migration_steps.append(
                f"- **{cat}**: Purge plain text sensitive data and encrypt JWT tokens stored in browser localStorage."
            )
            impl_checklist.append("- [ ] Encrypt all credentials or tokens prior to calling localStorage.setItem.")
            risk_assessment.append(f"- *{cat}*: High susceptibility to XSS token extraction and subsequent session hijacking.")
        elif cat == "IndexedDB":
            migration_steps.append(
                f"- **{cat}**: Sanitize, encrypt, and properly close/delete client-side IndexedDB databases on user logout."
            )
            impl_checklist.append("- [ ] Verify database purging functions run correctly upon account logout or deletion.")
            risk_assessment.append(f"- *{cat}*: Exposed offline user data on shared computer browser instances.")
        elif cat == "Session storage":
            migration_steps.append(
                f"- **{cat}**: Restrict sensitive data stored in sessionStorage and execute absolute purges on window close."
            )
            impl_checklist.append("- [ ] Verify that sensitive keys in sessionStorage are cleared upon user session logout.")
            risk_assessment.append(f"- *{cat}*: Unsecured temporary data exposed to cross-tab script execution.")
        elif cat == "Tracking technologies":
            migration_steps.append(
                f"- **{cat}**: Hold third-party tracking pixels and analytic script loads until user consent is validated."
            )
            impl_checklist.append("- [ ] Implement conditional script loading for third-party tags based on cookies acceptance.")
            risk_assessment.append(f"- *{cat}*: Direct non-compliance with the ePrivacy directive and subsequent cookie tracking blocks.")

    citations_str = "\n".join(citations_list) if citations_list else "- *No updates cited.*"

    if affected_files_set:
        affected_files_str = "\n".join(f"- `{f}`" for f in sorted(list(affected_files_set)))
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps) if migration_steps else "- *No migration steps identified.*"
    impl_checklist_str = "\n".join(impl_checklist) if impl_checklist else "- [ ] Perform generic verification of the privacy policy."
    risk_assessment_str = "\n".join(risk_assessment) if risk_assessment else "- *Low identified risk.*"

    pr_template = f"""# PULL REQUEST DRAFT: Mobile and Web Privacy Requirements Compliance Update

## 1. Summary
This pull request introduces critical configuration, structural, and code modifications to bring the mobile and web platforms into complete compliance with modern privacy policies. It addresses Apple, Android, and Web-specific regulations to pass automated storefront checks and human compliance reviews.

## 2. Background
Global application ecosystems enforce absolute transparency regarding data practices, tracking consents, local storages, and permissions. Mobile storefronts utilize automated scanning systems at build upload, and web validators scan for compliant cookie consents and GDPR opt-in flows. This PR proactively clears identified implementation gaps.

## 3. Regulatory change
- **Apple Requirements**: Full enforcement of signed Privacy Manifests, explicit required reason API mapping, App Tracking Transparency prompts, and aligned Nutrition Labels.
- **Android Requirements**: Precise Data Safety declarations, user deletion portals, AD_ID opt-outs, background location disclosures, and Health Connect verification.
- **Web Requirements**: Compliant GDPR opt-in consent banners, secure non-essential cookie writes, encrypted client-side local storages, and conditional tracking pixel activation.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High risk of application update blockages or storefront listing removals if these privacy gates are not cleared.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All changes are fully backward-compatible. Minimum SDK levels are maintained, and web components utilize robust feature checks to fall back gracefully on older devices and legacy browser configurations.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run the repository-wide automated compliance guard.

## 10. Testing checklist
- [ ] Verify that PrivacyInfo.xcprivacy exists in the final iOS bundle output.
- [ ] Verify that Google Play console Data Safety fields match the compiled libraries.
- [ ] Validate that non-essential cookie scripts are blocked prior to clicking accept on the consent banner.
- [ ] Perform a full account deletion walkthrough and verify all local storages are wiped.

## 11. Documentation checklist
- [ ] Update the Privacy Policy URL with standard tracking disclosures.
- [ ] Update `docs/PRIVACY-POLICY-MIGRATION.md` with the completed actions.
- [ ] Confirm App Store and Google Play console privacy sections reflect actual data transmissions.

## 12. Compliance impact
- **Storefront Reviews**: Eliminates high-frequency Apple and Android privacy rejections, securing clean publishing passages.
- **Regulatory Penalties**: Mitigates compliance risks under EU GDPR, ePrivacy Directive, and regional privacy rules.
- **Consumer Trust**: Increases user trust by providing explicit tracking permissions and transparent data control mechanisms.

## 13. Breaking changes
- No functional breaking changes are introduced. User tracking features are conditionally deferred until active permission is granted.

## 14. Review checklist
- [ ] Verify that the diff is completely emoji-free.
- [ ] Verify that all official sources cited are correct and verified.
- [ ] Verify that sensitive local credentials are fully encrypted.

## 15. Approver recommendations
Verify that the published web-based data deletion URL functions correctly before submitting the Android update, and ensure that the third-party frameworks embedded in the iOS workspace have their signed privacy manifests.
"""
    return pr_template


def update_documentation_report(updates, output_filepath, quiet=False):
    """
    Overwrites or updates the migration report in docs/PRIVACY-POLICY-MIGRATION.md.
    """
    lines = [
        "<!-- PRIVACY_POLICY_MONITOR_START -->",
        "# Mobile and Web Privacy Requirements Migration & Requirements Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-privacy.py` to track privacy compliance areas.",
        "",
        "## Monitored Requirements Update Log",
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
            lines.append("- **Regulatory Status**: Suspended. Source is an unverified Priority 4/5 secondary source.")
            lines.append("")
            continue

        lines.append(f"### Tasks for {cat}")
        lines.append("- **Regulatory Impact**: High priority compliance area.")

        if cat == "Privacy Manifest":
            lines.append("- [ ] **Task 1**: Create a PrivacyInfo.xcprivacy manifest at the root of the iOS target.")
            lines.append("- [ ] **Task 2**: List all collected data types and tracking practices in the manifest.")
        elif cat == "Required Reason APIs":
            lines.append("- [ ] **Task 1**: Identify all required reason API references (e.g. UserDefaults).")
            lines.append("- [ ] **Task 2**: Map reason codes under NSPrivacyAccessedAPITypes.")
        elif cat == "App Tracking Transparency":
            lines.append("- [ ] **Task 1**: Prompt users via ATTrackingManager before fetching advertising IDs.")
            lines.append("- [ ] **Task 2**: Fill out NSUserTrackingUsageDescription in Info.plist.")
        elif cat == "Privacy Nutrition Labels":
            lines.append("- [ ] **Task 1**: Verify App Store Connect nutrition disclosures against codebase PII transmission.")
        elif cat == "Data Safety":
            lines.append("- [ ] **Task 1**: Conduct a dependency audit for Google Play Data Safety alignment.")
        elif cat == "User Data Policy":
            lines.append("- [ ] **Task 1**: Build clear in-app data deletion controls and set a public web deletion URL.")
        elif cat == "Advertising ID":
            lines.append("- [ ] **Task 1**: Configure the AD_ID permission in AndroidManifest and handle user opt-outs.")
        elif cat == "Runtime permissions":
            lines.append("- [ ] **Task 1**: Ensure permissions are dynamically verified with clear user explanations.")
        elif cat == "Background location":
            lines.append("- [ ] **Task 1**: Ensure background location is backed by a prominent in-app disclosure view.")
        elif cat == "Health permissions":
            lines.append("- [ ] **Task 1**: Complete specialized fitness declarations and publish health statements.")
        elif cat == "GDPR":
            lines.append("- [ ] **Task 1**: Provide opt-in controls and account deletion pathways for EU users.")
        elif cat == "Cookie consent":
            lines.append("- [ ] **Task 1**: Deploy a cookie banner that halts non-essential cookie writes by default.")
        elif cat == "Local storage":
            lines.append("- [ ] **Task 1**: Encrypt any JWT tokens or user details kept in localStorage.")
        elif cat == "IndexedDB":
            lines.append("- [ ] **Task 1**: Safely wipe local database object stores upon user logout.")
        elif cat == "Session storage":
            lines.append("- [ ] **Task 1**: Secure temporary session tokens and clear session variables upon closing tabs.")
        elif cat == "Tracking technologies":
            lines.append("- [ ] **Task 1**: Defer Google Analytics or Facebook Pixel scripts until consent is given.")
        else:
            lines.append(f"- [ ] **Task**: Verify that all platform criteria for {cat} are checked and handled.")
        lines.append("")

    lines.append("<!-- PRIVACY_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        if not quiet:
            print(f"Privacy documentation report updated successfully at: {output_filepath}")
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor all Mobile and Web Privacy Requirements"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live mobile and web privacy RSS feeds"
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
        default="docs/PRIVACY-POLICY-MIGRATION.md",
        help="Filepath to write migration tasks and logs",
    )
    parser.add_argument(
        "--pr-output",
        type=str,
        default="docs/PRIVACY_COMPLIANCE_PR_DRAFT.md",
        help="Filepath to save the drafted PR",
    )
    parser.add_argument(
        "--json", action="store_true", help="Output JSON report to stdout"
    )

    args = parser.parse_args()

    # 1. Gather announcements
    announcements = []

    if args.live:
        if not args.json:
            print("Fetching live privacy regulatory RSS feeds...")
        announcements.extend(parse_rss_feed("https://developer.apple.com/news/rss/news.rss"))
        announcements.extend(parse_rss_feed("https://android-developers.googleblog.com/feeds/posts/default"))
        announcements.extend(parse_rss_feed("https://edpb.europa.eu/news/news/feed_en"))

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

    # 2. Classify updates into the 16 required categories
    keywords_filter = (
        [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    )
    classified_updates = classify_announcements(announcements, keywords_filter)

    if not classified_updates:
        print("No classified updates matched the current filters.")
        sys.exit(0)

    # Sort classified updates to keep them structured
    classified_updates = sorted(classified_updates, key=lambda x: x["category"])

    # Filter out announcements with unverified sources for PR generation
    verified_updates = []
    blocked_updates_count = 0
    for u in classified_updates:
        priority, is_verified = classify_source_and_verify(u)
        if priority in (4, 5) and not is_verified:
            blocked_updates_count += 1
        else:
            verified_updates.append(u)

    if not args.json:
        print(f"Monitored and classified {len(classified_updates)} policy/requirement updates ({blocked_updates_count} blocked due to source trust validation):")
        for idx, u in enumerate(classified_updates, 1):
            priority, is_verified = classify_source_and_verify(u)
            status_str = f"Priority {priority} " + ("(Verified)" if is_verified else "(Unverified)")
            print(f" {idx}. [{u['category']}] {u['title']} - {status_str}")

    # 3. Scan the codebase for signals related to these categories
    if not args.json:
        print(f"Scanning codebase under '{args.dir}' for privacy integration signals...")
    scan_results = scan_codebase_for_privacy_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    if not args.json:
        print(f"Found {total_matches} signal matches in code.")

    # 4. Write/Update documentation
    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, args.output_docs, quiet=args.json)

    # 5. Generate Pull Request draft using verified updates
    pr_draft = generate_pull_request_draft(verified_updates, scan_results)

    # Save drafted PR
    os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
    try:
        with open(args.pr_output, "w", encoding="utf-8") as f:
            f.write(pr_draft)
        if not args.json:
            print(f"PR draft written successfully to: {args.pr_output}")
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
