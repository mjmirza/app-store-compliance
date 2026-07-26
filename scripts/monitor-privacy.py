#!/usr/bin/env python3
"""
Monitor all mobile and web privacy requirements.
Tracks:
- Privacy Manifest (Apple)
- Required Reason APIs (Apple)
- App Tracking Transparency (Apple)
- Privacy Nutrition Labels (Apple)
- Data Safety (Android/Google Play)
- User Data Policy (Android/Google Play)
- Advertising ID (Android/Google Play)
- Runtime permissions (Android/Google Play)
- Background location (Android/Google Play)
- Health permissions (Android/Google Play)
- GDPR (Web)
- Cookie consent (Web)
- Local storage (Web)
- IndexedDB (Web)
- Session storage (Web)
- Tracking technologies (Web)

For every update, determines repository impact, identifies affected files,
creates migration recommendations, and generates implementation tasks.
"""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json

# Tracked categories
TRACKED_CATEGORIES = [
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
    "Privacy Manifest": ["privacy manifest", "privacymanifest", "privacyinfo.xcprivacy"],
    "Required Reason APIs": ["required reason api", "required reason", "nsprivacyaccessedapitypes", "reason code"],
    "App Tracking Transparency": ["app tracking transparency", "att ", "tracking authorization", "attrackingmanager", "nsusertrackingusagedescription"],
    "Privacy Nutrition Labels": ["privacy nutrition", "privacy label", "privacy report", "nutrition label", "data collection disclosure"],
    "Data Safety": ["data safety", "datasafety", "safety section", "data declaration"],
    "User Data Policy": ["user data policy", "prominent disclosure", "user data disclosure", "sensitive data", "personal info"],
    "Advertising ID": ["advertising id", "gaid", "ad_id", "com.google.android.permission.AD_ID"],
    "Runtime permissions": ["runtime permission", "checkselfpermission", "requestpermissions", "permission model"],
    "Background location": ["background location", "access_background_location", "prominent background disclosure"],
    "Health permissions": ["health permission", "health connect", "health.permission", "health data"],
    "GDPR": ["gdpr", "general data protection regulation", "data protection officer", "right to erasure", "consent withdraw"],
    "Cookie consent": ["cookie consent", "cookie banner", "document.cookie", "cookie preference", "accept cookie", "reject cookie"],
    "Local storage": ["local storage", "localstorage", "window.localstorage", "web storage"],
    "IndexedDB": ["indexeddb", "idbdatabase", "local database", "web sql"],
    "Session storage": ["session storage", "sessionstorage", "window.sessionstorage"],
    "Tracking technologies": ["tracking tech", "tracking script", "tracking pixel", "google tag manager", "google analytics", "facebook pixel", "canvas fingerprint"]
}

# Codebase signals (regex patterns) to find files affected by each of the 16 categories
CATEGORY_SIGNALS = {
    "Privacy Manifest": [r"PrivacyInfo\.xcprivacy", r"NSPrivacyAccessedAPITypes", r"NSPrivacyTrackingDomains"],
    "Required Reason APIs": [r"NSFileManager", r"UserDefaults", r"systemUptime", r"ProcessInfo"],
    "App Tracking Transparency": [r"ATTrackingManager", r"NSUserTrackingUsageDescription", r"requestTrackingAuthorization"],
    "Privacy Nutrition Labels": [r"FirebaseAnalytics", r"GoogleMobileAds", r"Adjust", r"AppsFlyerLib", r"Mixpanel"],
    "Data Safety": [r"firebase-analytics", r"com\.google\.android\.gms\.ads", r"appsflyer", r"adjust", r"com\.facebook"],
    "User Data Policy": [r"READ_CONTACTS", r"WRITE_CONTACTS", r"GET_ACCOUNTS", r"READ_PHONE_STATE"],
    "Advertising ID": [r"com\.google\.android\.gms\.ads\.identifier\.AdvertisingIdClient", r"advertisingId", r"AD_ID"],
    "Runtime permissions": [r"android\.permission\.CAMERA", r"android\.permission\.RECORD_AUDIO", r"android\.permission\.ACCESS_FINE_LOCATION"],
    "Background location": [r"ACCESS_BACKGROUND_LOCATION"],
    "Health permissions": [r"health\.permission", r"HealthConnectClient"],
    "GDPR": [r"gdpr", r"consent", r"opt-out", r"delete", r"clearUserData"],
    "Cookie consent": [r"document\.cookie", r"setCookie", r"cookieConsent", r"cookie-banner", r"CookieConsentBanner", r"acceptCookies"],
    "Local storage": [r"localStorage\.setItem", r"localStorage"],
    "IndexedDB": [r"indexedDB", r"indexedDB\.open", r"IDBDatabase"],
    "Session storage": [r"sessionStorage\.setItem", r"sessionStorage"],
    "Tracking technologies": [r"google-analytics\.com", r"googletagmanager\.com", r"connect\.facebook\.net", r"fbq"]
}

# Rich mock announcements representing policy updates/bulletins for ALL 16 categories
MOCK_ANNOUNCEMENTS = [
    {
        "id": "PRIVACY-MOCK-MANIFEST",
        "category": "Privacy Manifest",
        "title": "Apple App Store Required Privacy Manifest Compliance Guide",
        "description": "Apple mandates a signed Privacy Manifest (PrivacyInfo.xcprivacy) for all new apps and updates. Developers must declare data collection and tracking domains precisely to pass automated publishing validations.",
        "link": "https://developer.apple.com/app-store/review/guidelines/",
        "pubDate": "Fri, 12 Jun 2026 10:00:00 GMT"
    },
    {
        "id": "PRIVACY-MOCK-REASON-APIS",
        "category": "Required Reason APIs",
        "title": "Apple Required Reason APIs Usage and Justification Rule",
        "description": "Any use of APIs like UserDefaults, systemUptime, and NSFileManager requires designated justification reason codes in the app privacy manifest to prevent fingerprinting attempts.",
        "link": "https://developer.apple.com/app-store/review/guidelines/",
        "pubDate": "Mon, 15 Jun 2026 09:00:00 GMT"
    },
    {
        "id": "PRIVACY-MOCK-ATT",
        "category": "App Tracking Transparency",
        "title": "App Tracking Transparency (ATT) Authorization Requirement",
        "description": "Under App Store Review Guideline 5.1.2(i), explicit user authorization via ATTrackingManager is mandatory before tracking users across third-party websites or apps using the IDFA.",
        "link": "https://developer.apple.com/app-store/review/guidelines/",
        "pubDate": "Wed, 17 Jun 2026 11:00:00 GMT"
    },
    {
        "id": "PRIVACY-MOCK-NUTRITION",
        "category": "Privacy Nutrition Labels",
        "title": "Apple Privacy Nutrition Labels Verification and Accuracy Mandate",
        "description": "App Store Connect requires detailed and matching declarations of data collection types. Mismatches between declared practices and active third-party SDK behaviors will trigger immediate submission blocks.",
        "link": "https://developer.apple.com/app-store/review/",
        "pubDate": "Sat, 20 Jun 2026 14:00:00 GMT"
    },
    {
        "id": "PRIVACY-MOCK-DATA-SAFETY",
        "category": "Data Safety",
        "title": "Google Play Store Data Safety Form Verification Rule",
        "description": "Google Play enforces strict scanning to verify Data Safety form declarations. Third-party analytics and ad SDK data collection actions must align perfectly with Play Console declarations.",
        "link": "https://play.google/developer-content-policy/",
        "pubDate": "Tue, 23 Jun 2026 15:00:00 GMT"
    },
    {
        "id": "PRIVACY-MOCK-USER-DATA",
        "category": "User Data Policy",
        "title": "Google Play Prominent Disclosure and User Consent Policy",
        "description": "Accessing personal data like contacts, logs, or SMS requires clear, in-app prominent disclosure and an explicit user opt-in before requesting standard runtime platform permissions.",
        "link": "https://play.google/developer-content-policy/",
        "pubDate": "Fri, 26 Jun 2026 10:00:00 GMT"
    },
    {
        "id": "PRIVACY-MOCK-AD-ID",
        "category": "Advertising ID",
        "title": "Google Play Advertising ID Permission Declaration and Requirements",
        "description": "To target Android 12 (API 31) or higher and retrieve the persistent Google Advertising ID, developers must explicitly declare the com.google.android.permission.AD_ID permission in AndroidManifest.xml.",
        "link": "https://play.google/developer-content-policy/",
        "pubDate": "Mon, 29 Jun 2026 13:00:00 GMT"
    },
    {
        "id": "PRIVACY-MOCK-RUNTIME-PERM",
        "category": "Runtime permissions",
        "title": "Android Runtime Permission Check and Verification Protocol",
        "description": "Apps accessing camera, microphone, or fine location must check and request permissions dynamically at runtime, handling cases where users deny access or revoke permissions gracefully.",
        "link": "https://developer.android.com/guide/topics/permissions/overview",
        "pubDate": "Wed, 01 Jul 2026 09:00:00 GMT"
    },
    {
        "id": "PRIVACY-MOCK-BG-LOCATION",
        "category": "Background location",
        "title": "Google Play Background Location Permission Declaration Mandate",
        "description": "Requesting ACCESS_BACKGROUND_LOCATION is limited to core features and requires a detailed Play Console form declaration, a prominent in-app disclosure, and a video walkthrough submission.",
        "link": "https://support.google.com/googleplay/android-developer/answer/9799150",
        "pubDate": "Fri, 03 Jul 2026 16:00:00 GMT"
    },
    {
        "id": "PRIVACY-MOCK-HEALTH",
        "category": "Health permissions",
        "title": "Google Play Health Connect API Access and Compliance Standard",
        "description": "Apps declaring Health Connect permissions must submit the Google Play health compliance form, maintain strict data safety, and are prohibited from selling or sharing health-related data with brokers.",
        "link": "https://play.google/developer-content-policy/",
        "pubDate": "Mon, 06 Jul 2026 12:00:00 GMT"
    },
    {
        "id": "PRIVACY-MOCK-GDPR",
        "category": "GDPR",
        "title": "European Union GDPR Web Platform User Rights and Compliance Guidance",
        "description": "Under the General Data Protection Regulation, web users must be provided with freely given, unambiguous consent choices, the right to withdraw consent easily, and a direct path to request complete data erasure.",
        "link": "https://eur-lex.europa.eu/eli/reg/2016/679/oj",
        "pubDate": "Thu, 09 Jul 2026 11:00:00 GMT"
    },
    {
        "id": "PRIVACY-MOCK-COOKIE-CONSENT",
        "category": "Cookie consent",
        "title": "Web Platform Cookie Consent Banner and Gating Requirements",
        "description": "Cookie consent policies mandate that cookie banners must allow rejecting non-essential cookies as easily as accepting them, with zero pre-ticked consent options allowed before loading tracking services.",
        "link": "https://eur-lex.europa.eu/eli/reg/2016/679/oj",
        "pubDate": "Sun, 12 Jul 2026 09:00:00 GMT"
    },
    {
        "id": "PRIVACY-MOCK-LOCAL-STORAGE",
        "category": "Local storage",
        "title": "Unsafe Authentication Token Persistency in Web LocalStorage",
        "description": "Privacy regulations and standard web security practices discourage storing sensitive raw JWTs, access secrets, or PII inside browser LocalStorage due to cross-site scripting (XSS) extraction risks.",
        "link": "https://csrc.nist.gov/publications/detail/sp/800-63b/final",
        "pubDate": "Tue, 14 Jul 2026 14:00:00 GMT"
    },
    {
        "id": "PRIVACY-MOCK-INDEXEDDB",
        "category": "IndexedDB",
        "title": "Web Structured Storage Encryption and IndexedDB Security",
        "description": "Any unstructured personal, medical, or transaction-related user data persistent within browser-based IndexedDB stores must utilize AES encryption (e.g., Web Crypto API) to secure local caches.",
        "link": "https://csrc.nist.gov/publications/detail/sp/800-175b/final",
        "pubDate": "Thu, 16 Jul 2026 15:00:00 GMT"
    },
    {
        "id": "PRIVACY-MOCK-SESSION-STORAGE",
        "category": "Session storage",
        "title": "Web Session Storage Lifecycle and User Logout Routines",
        "description": "Session tracking parameters active inside sessionStorage must be explicitly cleared via sessionStorage.clear() upon user logout or session termination to avoid unauthorized cross-tab data access.",
        "link": "https://csrc.nist.gov/publications/detail/sp/800-63b/final",
        "pubDate": "Sat, 18 Jul 2026 10:00:00 GMT"
    },
    {
        "id": "PRIVACY-MOCK-TRACKING",
        "category": "Tracking technologies",
        "title": "Web Tracking Technologies Gating and Fingerprinting Rules",
        "description": "Loading Google Analytics, Tag Manager, or Facebook Pixel prior to explicit user opt-in is prohibited. Device and canvas-based fingerprinting methods are strictly classified as personal data processing.",
        "link": "https://eur-lex.europa.eu/eli/reg/2016/679/oj",
        "pubDate": "Tue, 21 Jul 2026 11:00:00 GMT"
    }
]

def scan_codebase_for_privacy_signals(start_dir="."):
    """
    Scans the codebase for files containing signals related to each of the 16 requirement categories.
    """
    matches = {cat: [] for cat in TRACKED_CATEGORIES}
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
            if not file.endswith(('.swift', '.m', '.h', '.kt', '.java', '.xml', '.gradle', '.kts', '.json', '.js', '.ts', '.md', '.html')):
                continue

            filepath = os.path.join(root, file)
            # Skip monitor scripts to avoid self-referencing matches
            if "monitor-privacy" in file or "monitor-privacy-test" in file:
                continue

            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    for i, line in enumerate(f, 1):
                        for cat, patterns in compiled_signals.items():
                            for pattern in patterns:
                                if pattern.search(line):
                                    matches[cat].append({
                                        "file": filepath,
                                        "line_num": i,
                                        "content": line.strip()[:100],
                                        "matched_pattern": pattern.pattern
                                    })
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
            url,
            headers={'User-Agent': 'Mozilla/5.0 (PrivacyComplianceMonitor/1.0)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)

            def clean_tag(tag):
                return tag.split('}', 1)[1] if '}' in tag else tag

            for elem in root.iter():
                tag = clean_tag(elem.tag)
                if tag in ('item', 'entry'):
                    title = ""
                    desc = ""
                    link = ""
                    pub_date = ""

                    for child in elem:
                        ctag = clean_tag(child.tag)
                        if ctag == 'title':
                            title = child.text or ""
                        elif ctag in ('description', 'summary', 'content'):
                            desc = child.text or ""
                        elif ctag == 'link':
                            link_val = child.get('href')
                            link = link_val if link_val else (child.text or "")
                        elif ctag in ('pubDate', 'published', 'updated'):
                            pub_date = child.text or ""

                    items.append({
                        "title": title.strip(),
                        "description": desc.strip() if desc else "",
                        "link": link.strip(),
                        "pubDate": pub_date.strip()
                    })
    except Exception as e:
        print("Warning: Failed to fetch live feed " + url + ": " + str(e), file=sys.stderr)
    return items

def classify_announcements(announcements, keywords_filter=None):
    """
    Classifies incoming announcements into the 16 requirement categories.
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
                classified_updates.append({
                    "id": ann.get("id", "PRIVACY-UPDATE-" + str(hash(title))[:6]),
                    "category": cat,
                    "title": title,
                    "description": desc,
                    "link": ann.get("link", ""),
                    "pubDate": ann.get("pubDate", "")
                })
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
        citations_list.append("- **" + cat + "**: [" + u['title'] + "](" + u['link'] + ") (Published: " + u['pubDate'] + ")")

        files = scan_results.get(cat, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        if cat == "Privacy Manifest":
            migration_steps.append("- **" + cat + "**: Add a PrivacyInfo.xcprivacy manifest file to the iOS project directory.")
            impl_checklist.append("- [ ] Verify PrivacyInfo.xcprivacy file presence.")
            risk_assessment.append("- *" + cat + "*: Immediate blockage during Apple App Store binary upload.")
        elif cat == "Required Reason APIs":
            migration_steps.append("- **" + cat + "**: Declare approved reason codes in PrivacyInfo.xcprivacy for UserDefaults, NSFileManager, etc.")
            impl_checklist.append("- [ ] Audit UserDefaults and file system API calls in Swift and Objective-C files.")
            risk_assessment.append("- *" + cat + "*: Rejection of app upload by automated App Store Connect verification.")
        elif cat == "App Tracking Transparency":
            migration_steps.append("- **" + cat + "**: Prompt for user tracking authorization via ATTrackingManager and configure NSUserTrackingUsageDescription.")
            impl_checklist.append("- [ ] Prompt for tracking authorization dynamically and set usage description in Info.plist.")
            risk_assessment.append("- *" + cat + "*: Hard App Store rejection for reading IDFA without explicit user consent.")
        elif cat == "Privacy Nutrition Labels":
            migration_steps.append("- **" + cat + "**: Update the App Store Connect Data Use Questionnaire to match analytics and advertising SDK data collection.")
            impl_checklist.append("- [ ] Align App Store Connect privacy questionnaire declarations with current SDK tracking actions.")
            risk_assessment.append("- *" + cat + "*: Potential removal or submission rejection for inaccurate metadata declarations.")
        elif cat == "Data Safety":
            migration_steps.append("- **" + cat + "**: Complete Google Play Data Safety form declaring third-party tracking behavior accurately.")
            impl_checklist.append("- [ ] Re-audit Google Play Console Data Safety selections for all active SDKs.")
            risk_assessment.append("- *" + cat + "*: Play Store listing suspension or warning for Data Safety mismatches.")
        elif cat == "User Data Policy":
            migration_steps.append("- **" + cat + "**: Present prominent in-app disclosure prior to collecting contacts, files, or sensitive identifiers.")
            impl_checklist.append("- [ ] Implement in-app prominent disclosure dialog explaining user data access details.")
            risk_assessment.append("- *" + cat + "*: Automated policy violation rejection under Google Play User Data policies.")
        elif cat == "Advertising ID":
            migration_steps.append("- **" + cat + "**: Declare the com.google.android.permission.AD_ID permission in AndroidManifest.xml when targeting Android 12+.")
            impl_checklist.append("- [ ] Ensure AD_ID permission is set inside the Android manifest configuration.")
            risk_assessment.append("- *" + cat + "*: Replacement of Advertising ID with zeros, causing attribution breakdown.")
        elif cat == "Runtime permissions":
            migration_steps.append("- **" + cat + "**: Verify and request sensitive permissions (camera, location, mic) dynamically at runtime.")
            impl_checklist.append("- [ ] Verify checkSelfPermission and requestPermissions are called correctly at runtime.")
            risk_assessment.append("- *" + cat + "*: Runtime security exceptions or immediate Play Store submission rejection.")
        elif cat == "Background location":
            migration_steps.append("- **" + cat + "**: Complete background location declaration on Play Console and include prominent disclosure.")
            impl_checklist.append("- [ ] Complete the Play Console Background Location Declaration questionnaire and record video demo.")
            risk_assessment.append("- *" + cat + "*: Rejection of application package updates for missing console permissions justification.")
        elif cat == "Health permissions":
            migration_steps.append("- **" + cat + "**: Complete Health Connect declaration form and secure explicit consent before accessing health APIs.")
            impl_checklist.append("- [ ] Fill and submit Play Console Health Connect compatibility form.")
            risk_assessment.append("- *" + cat + "*: Automated removal from Google Play for undeclared sensitive health permission access.")
        elif cat == "GDPR":
            migration_steps.append("- **" + cat + "**: Provide freely given, unambiguous consent options, and add a path for data deletion/withdrawal.")
            impl_checklist.append("- [ ] Review user consent flow to verify unambiguous consent and clear erasure path.")
            risk_assessment.append("- *" + cat + "*: High regulatory fines or enforcement notices from European data protection agencies.")
        elif cat == "Cookie consent":
            migration_steps.append("- **" + cat + "**: Build a cookie consent banner blocking non-essential tracking until user approval is given.")
            impl_checklist.append("- [ ] Add a compliant cookie consent banner blocking non-essential analytics tracking.")
            risk_assessment.append("- *" + cat + "*: Direct violation of the ePrivacy Directive and GDPR, leading to local authority audits.")
        elif cat == "Local storage":
            migration_steps.append("- **" + cat + "**: Avoid placing raw secrets or sensitive JWT tokens in browser LocalStorage.")
            impl_checklist.append("- [ ] Verify raw authentication tokens are not stored inside LocalStorage.")
            risk_assessment.append("- *" + cat + "*: Account compromise or session hijacking through XSS data extraction.")
        elif cat == "IndexedDB":
            migration_steps.append("- **" + cat + "**: Encrypt personal or transaction records persistent within IndexedDB stores.")
            impl_checklist.append("- [ ] Add cryptographically secure encryption layers over IndexedDB caches.")
            risk_assessment.append("- *" + cat + "*: Unauthorized local database data extraction on compromised user hardware.")
        elif cat == "Session storage":
            migration_steps.append("- **" + cat + "**: Call sessionStorage.clear() explicitly during user sign-out or session expiration.")
            impl_checklist.append("- [ ] Explicitly clear sessionStorage parameters in logout routines.")
            risk_assessment.append("- *" + cat + "*: Residual session state leak across shared user browser environments.")
        elif cat == "Tracking technologies":
            migration_steps.append("- **" + cat + "**: Block loading analytical tracking pixels or scripts before explicit user opt-in.")
            impl_checklist.append("- [ ] Implement conditional script injection gating for Google Analytics and Facebook Pixels.")
            risk_assessment.append("- *" + cat + "*: Automatic non-compliance with global consent-first tracking mandates.")
        else:
            migration_steps.append("- **" + cat + "**: Align operations with audited standards for " + cat)
            impl_checklist.append("- [ ] Review monitored updates for " + cat)
            risk_assessment.append("- *" + cat + "*: General compliance risk.")

    citations_str = "\n".join(citations_list)

    if affected_files_set:
        affected_files_str = "\n".join("- `" + f + "`" for f in sorted(list(affected_files_set)))
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps)
    impl_checklist_str = "\n".join(impl_checklist)
    risk_assessment_str = "\n".join(risk_assessment)

    pr_template = """# PULL REQUEST DRAFT: Mobile and Web Privacy Compliance Update

## 1. Summary
This pull request brings the application into complete compliance with all monitored mobile and web privacy regulations and developer requirements. It addresses privacy manifests, required reason APIs, App Tracking Transparency, Android Data Safety, runtime permissions, GDPR compliance, cookie consent, and browser-side data persistency rules.

## 2. Background
Mobile platforms and web standards enforce strict regulatory publishing guidelines regarding user data collection, authorization, and local data persistence. Non-compliance results in publishing blocks, direct store rejections, or high litigation risk under international privacy frameworks.

## 3. Regulatory change
- **Apple & Android Privacy Standards**: Enforcement of Privacy Manifests (PrivacyInfo.xcprivacy), Required Reason API justifications, App Tracking Transparency prompts, Android Data Safety declarations, and dynamic runtime permissions.
- **Web Privacy Standards**: General Data Protection Regulation (GDPR) mandates, cookie consent banners with equivalent accept/reject patterns, and secure local data persistence (LocalStorage, IndexedDB, SessionStorage) guidelines.

## 4. Official citations
""" + citations_str + """

## 5. Affected files
""" + affected_files_str + """

## 6. Risk assessment
""" + risk_assessment_str + """
- **Overall Compliance Standing**: Critical risk of application publishing rejection or data protection regulatory warnings if active gaps are left unmitigated.

## 7. Migration steps
""" + migration_steps_str + """

## 8. Backward compatibility
All implemented privacy enhancements are fully backward-compatible. Dynamic runtime checks are utilized to verify platform capability support on older system versions while enforcing compliance protocols on current environments.

## 9. Implementation checklist
""" + impl_checklist_str + """
- [ ] Run the automated compliance guard checks locally.

## 10. Testing checklist
- [ ] Confirm Apple Privacy Manifest is correctly parsed and accepted during simulated App Store uploads.
- [ ] Verify that Google Play Data Safety form submissions align with all compiled tracking dependencies.
- [ ] Run automated web consent tests verifying tracking scripts are blocked prior to user opt-in.
- [ ] Confirm localStorage and sessionStorage directories contain no unencrypted sensitive user secrets.

## 11. Documentation checklist
- [ ] Update store privacy policies with specific data collection disclosures.
- [ ] Record and save background location verification video walkthroughs.
- [ ] Update docs/PRIVACY-POLICY-MIGRATION.md with completed action logs.

## 12. Compliance impact
- **Store Acceptance**: Secures continuous mobile release submissions by satisfying Apple and Google Play compliance gates.
- **Regulatory Standing**: Mitigates legal exposure under EU GDPR and global data privacy frameworks.
- **User Safety**: Secures local user sessions and database persistence layers against extraction attacks.

## 13. Breaking changes
- None. Accessing restricted APIs and storage layers is structured dynamically with graceful fallbacks.

## 14. Review checklist
- [ ] Code complies with standard platform privacy rules.
- [ ] Cookie consent gating blocks non-essential analytics tracking prior to consent.
- [ ] Local data persistence is secure and encrypted where required.

## 15. Approver recommendations
Verify that updated store-listing declarations are approved in App Store Connect and Google Play Console by appropriate compliance owners. Confirm that third-party SDK dependencies stay updated to retain compatibility with active platform guidelines.
"""
    return pr_template

def update_documentation_report(updates, output_filepath):
    """
    Overwrites or updates the migration report in docs/PRIVACY-POLICY-MIGRATION.md.
    """
    lines = [
        "<!-- PRIVACY_POLICY_MONITOR_START -->",
        "# Mobile and Web Privacy Compliance Migration & Requirements Report",
        "",
        "This report is continuously generated and updated by `scripts/monitor-privacy.py` to track compliance areas.",
        "",
        "## Monitored Requirements Update Log",
        ""
    ]

    for idx, u in enumerate(updates, 1):
        lines.append("### " + str(idx) + ". [" + u['category'] + "] " + u['title'])
        lines.append("- **Published Date**: " + u['pubDate'])
        lines.append("- **Official Resource**: [" + u['link'] + "](" + u['link'] + ")")
        lines.append("- **Description**: " + u['description'])
        lines.append("")

    lines.append("## Automated Migration Recommendations & Implementation Tasks")
    lines.append("")

    for u in updates:
        cat = u["category"]
        lines.append("### Tasks for " + cat)
        lines.append("- **Regulatory Impact**: High priority. Action required to clear compliance gates.")

        if cat == "Privacy Manifest":
            lines.append("- [ ] **Task 1**: Create and configure `PrivacyInfo.xcprivacy` inside the iOS project root.")
            lines.append("- [ ] **Task 2**: Audit third-party SDK dependencies for embedded signed manifests.")
        elif cat == "Required Reason APIs":
            lines.append("- [ ] **Task 1**: Identify Required Reason API calls (UserDefaults, ProcessInfo, etc.).")
            lines.append("- [ ] **Task 2**: Define appropriate NSPrivacyAccessedAPITypes keys in the privacy manifest.")
        elif cat == "App Tracking Transparency":
            lines.append("- [ ] **Task 1**: Implement ATTrackingManager prompt sequence prior to requesting Advertising ID.")
            lines.append("- [ ] **Task 2**: Add NSUserTrackingUsageDescription to Info.plist.")
        elif cat == "Privacy Nutrition Labels":
            lines.append("- [ ] **Task 1**: Match analytics/ad tracking data with App Store privacy questionnaires.")
        elif cat == "Data Safety":
            lines.append("- [ ] **Task 1**: Verify third-party SDK tracking conforms to Google Play Data Safety forms.")
        elif cat == "User Data Policy":
            lines.append("- [ ] **Task 1**: Implement prominent in-app disclosure dialogs for contact or location collection.")
        elif cat == "Advertising ID":
            lines.append("- [ ] **Task 1**: Add com.google.android.permission.AD_ID permission to Android manifest.")
        elif cat == "Runtime permissions":
            lines.append("- [ ] **Task 1**: Confirm dynamic permission checking is active prior to accessing restricted APIs.")
        elif cat == "Background location":
            lines.append("- [ ] **Task 1**: Verify background location permissions are justified with a core application feature.")
        elif cat == "Health permissions":
            lines.append("- [ ] **Task 1**: Complete and submit the Google Play health compatibility declaration.")
        elif cat == "GDPR":
            lines.append("- [ ] **Task 1**: Ensure users possess standard deletion and consent withdrawal options.")
        elif cat == "Cookie consent":
            lines.append("- [ ] **Task 1**: Integrate a compliant cookie preferences consent banner blocking trackers.")
        elif cat == "Local storage":
            lines.append("- [ ] **Task 1**: Ensure no raw credentials or sensitive JWTs are persistent inside LocalStorage.")
        elif cat == "IndexedDB":
            lines.append("- [ ] **Task 1**: Encrypt active structured data caches persistent inside IndexedDB.")
        elif cat == "Session storage":
            lines.append("- [ ] **Task 1**: Implement explicit sessionStorage.clear() logic during user logout routines.")
        elif cat == "Tracking technologies":
            lines.append("- [ ] **Task 1**: Gate analytical and marketing tracking pixels behind cookie consent banner approvals.")
        else:
            lines.append("- [ ] **Task**: Verify compliance parameters for " + cat + ".")
        lines.append("")

    lines.append("<!-- PRIVACY_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        print("Privacy documentation updated successfully at: " + output_filepath)
    except Exception as e:
        print("Error writing documentation to " + output_filepath + ": " + str(e), file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Monitor all Mobile and Web Privacy Requirements")
    parser.add_argument("--live", action="store_true", help="Fetch live mobile/web privacy feeds")
    parser.add_argument("--mock", type=str, help="Path to custom mock announcements JSON file, or 'inline' to use default mock data")
    parser.add_argument("--keywords", type=str, help="Optional comma-separated keywords to filter updates")
    parser.add_argument("--dir", type=str, default=".", help="Codebase directory to scan")
    parser.add_argument("--output-docs", type=str, default="docs/PRIVACY-POLICY-MIGRATION.md", help="Filepath to write migration tasks and logs")
    parser.add_argument("--pr-output", type=str, default="docs/PRIVACY_COMPLIANCE_PR_DRAFT.md", help="Filepath to save the drafted PR (outputs to stdout if omitted)")

    args = parser.parse_args()

    announcements = []

    if args.live:
        print("Fetching live privacy news feeds...")
        announcements.extend(parse_rss_feed("https://edpb.europa.eu/news/news_en.xml"))
        announcements.extend(parse_rss_feed("https://ico.org.uk/about-the-ico/news-and-events/news-and-blogs/rss-feed/"))

    if args.mock or (not args.live and not args.mock) or not announcements:
        print("Using comprehensive mock privacy updates for compliance scanning...")
        if args.mock and args.mock != "inline" and os.path.exists(args.mock):
            try:
                with open(args.mock, 'r') as f:
                    announcements.extend(json.load(f))
            except Exception as e:
                print("Failed to read mock file " + args.mock + ": " + str(e) + ", using default mock dataset instead.", file=sys.stderr)
                announcements.extend(MOCK_ANNOUNCEMENTS)
        else:
            announcements.extend(MOCK_ANNOUNCEMENTS)

    keywords_filter = [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    classified_updates = classify_announcements(announcements, keywords_filter)

    if not classified_updates:
        print("No classified updates matched the current filters.")
        sys.exit(0)

    print("Monitored and classified " + str(len(classified_updates)) + " privacy requirement updates:")
    for idx, u in enumerate(classified_updates, 1):
        print(" " + str(idx) + ". [" + u['category'] + "] " + u['title'])

    print("Scanning codebase under '" + args.dir + "' for privacy integration signals...")
    scan_results = scan_codebase_for_privacy_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    print("Found " + str(total_matches) + " signal matches in code.")

    os.makedirs(os.path.dirname(args.output_docs) or '.', exist_ok=True)
    update_documentation_report(classified_updates, args.output_docs)

    pr_draft = generate_pull_request_draft(classified_updates, scan_results)

    if args.pr_output:
        os.makedirs(os.path.dirname(args.pr_output) or '.', exist_ok=True)
        try:
            with open(args.pr_output, 'w', encoding='utf-8') as f:
                f.write(pr_draft)
            print("PR draft written successfully to: " + args.pr_output)
        except Exception as e:
            print("Failed to write PR draft to " + args.pr_output + ": " + str(e), file=sys.stderr)
    else:
        print("\n=== GENERATED 15-SECTION COMPLIANCE PULL REQUEST DRAFT ===")
        print(pr_draft)
        print("==========================================================")

if __name__ == "__main__":
    main()
