#!/usr/bin/env python3
"""
Mobile and Web Privacy Requirements Monitor: tracks 16 Apple, Android, and Web
privacy requirements against live/mock feeds and scans the codebase for impact.
"""

import os
import sys
import re
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import json
from datetime import datetime

# 16 distinct privacy requirements
TRACKED_REQUIREMENTS = [
    # Apple
    "Privacy Manifest",
    "Required Reason APIs",
    "App Tracking Transparency",
    "Privacy Nutrition Labels",
    # Android
    "Data Safety",
    "User Data Policy",
    "Advertising ID",
    "Runtime permissions",
    "Background location",
    "Health permissions",
    # Web
    "GDPR",
    "Cookie consent",
    "Local storage",
    "IndexedDB",
    "Session storage",
    "Tracking technologies",
]

# Keywords used to classify incoming policy announcements/articles into the 16 categories
CATEGORY_KEYWORDS = {
    "Privacy Manifest": [
        "privacy manifest",
        "xcprivacy",
        "privacyinfo",
        "privacy manifest requirement",
    ],
    "Required Reason APIs": [
        "required reason api",
        "accessed api",
        "reasons for api",
        "userdefaults",
        "systemuptime",
        "nsfilemanager",
    ],
    "App Tracking Transparency": [
        "app tracking transparency",
        "att prompt",
        "idfa tracking",
        "requesttrackingauthorization",
        "user tracking",
    ],
    "Privacy Nutrition Labels": [
        "privacy nutrition label",
        "nutrition label",
        "privacy label",
        "nsprivacycollecteddatatypes",
    ],
    "Data Safety": [
        "data safety",
        "google play safety section",
        "data safety form",
        "data collection and sharing",
    ],
    "User Data Policy": [
        "user data policy",
        "prominent disclosure",
        "personal data sharing",
        "account deletion flow",
    ],
    "Advertising ID": [
        "advertising id",
        "ad id permission",
        "google advertising id",
        "com.google.android.gms.permission.AD_ID",
    ],
    "Runtime permissions": [
        "runtime permission",
        "permission request",
        "requestpermissions",
        "shouldshowrequestpermissionrationale",
    ],
    "Background location": [
        "background location",
        "access_background_location",
        "persistent location",
    ],
    "Health permissions": [
        "health permissions",
        "health connect",
        "health data access",
        "read_steps",
        "read_heart_rate",
    ],
    "GDPR": [
        "gdpr",
        "general data protection regulation",
        "opt-in consent",
        "right to be forgotten",
    ],
    "Cookie consent": [
        "cookie consent",
        "cookie banner",
        "eprivacy directive",
        "document.cookie",
    ],
    "Local storage": [
        "local storage",
        "localstorage",
        "localstorage.setitem",
    ],
    "IndexedDB": [
        "indexeddb",
        "indexeddb.open",
        "structured storage",
    ],
    "Session storage": [
        "session storage",
        "sessionstorage",
        "sessionstorage.setitem",
    ],
    "Tracking technologies": [
        "tracking technologies",
        "google analytics",
        "tracking pixels",
        "third-party trackers",
        "gtag",
        "fbq",
        "hotjar",
    ],
}

# Codebase signals (regex patterns) to find files affected by each of the 16 categories
CATEGORY_SIGNALS = {
    "Privacy Manifest": [
        r"PrivacyInfo\.xcprivacy",
        r"NSPrivacyAccessedAPITypes",
        r"NSPrivacyCollectedDataTypes",
    ],
    "Required Reason APIs": [
        r"UserDefaults",
        r"NSFileManager",
        r"systemUptime",
        r"ProcessInfo",
        r"stat\s*\(",
    ],
    "App Tracking Transparency": [
        r"ATTrackingManager",
        r"NSUserTrackingUsageDescription",
        r"ASIdentifierManager",
        r"advertisingIdentifier",
    ],
    "Privacy Nutrition Labels": [
        r"NSPrivacyCollectedDataTypes",
        r"privacyNutritionLabels",
        r"privacy-nutrition-labels",
    ],
    "Data Safety": [
        r"firebase-analytics",
        r"com\.google\.android\.gms\.ads",
        r"facebook",
        r"appsflyer",
        r"adjust",
    ],
    "User Data Policy": [
        r"privacyPolicy",
        r"privacy-policy",
        r"privacy_policy",
        r"User Data",
        r"deleteAccount",
        r"delete_account",
    ],
    "Advertising ID": [
        r"com\.google\.android\.gms\.permission\.AD_ID",
        r"AD_ID",
        r"getAdvertisingIdInfo",
    ],
    "Runtime permissions": [
        r"requestPermissions",
        r"checkSelfPermission",
        r"shouldShowRequestPermissionRationale",
    ],
    "Background location": [
        r"ACCESS_BACKGROUND_LOCATION",
    ],
    "Health permissions": [
        r"HealthConnectClient",
        r"com\.google\.android\.gms\.permission\.HealthConnect",
        r"READ_STEPS",
        r"READ_HEART_RATE",
    ],
    "GDPR": [
        r"processData",
        r"personalData",
        r"submitForm",
        r"registerWeb",
        r"webForm",
    ],
    "Cookie consent": [
        r"document\.cookie",
        r"setCookie",
        r"cookieStore",
        r"js-cookie",
        r"cookieConsent",
    ],
    "Local storage": [
        r"localStorage\.setItem",
        r"localStorage",
    ],
    "IndexedDB": [
        r"indexedDB\.open",
        r"indexedDB",
        r"createObjectStore",
    ],
    "Session storage": [
        r"sessionStorage\.setItem",
        r"sessionStorage",
    ],
    "Tracking technologies": [
        r"gtag",
        r"fbq",
        r"google-analytics",
        r"trackingPixel",
        r"analytics\.js",
        r"hotjar",
    ],
}

# Mock updates representing announcements for all 16 categories
MOCK_ANNOUNCEMENTS = [
    {
        "id": "PRIV-MOCK-APPLE-MANIFEST",
        "category": "Privacy Manifest",
        "title": "Apple Mandatory Privacy Manifest Framework Implementation Deadline",
        "description": "Apple announces strict validation rules for third-party SDK bundles. All binary uploads must contain a valid signed PrivacyInfo.xcprivacy detailing tracking domains and collected data types.",
        "link": "https://developer.apple.com/news/?id=privacy-manifest-mandate",
        "pubDate": "Wed, 10 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "PRIV-MOCK-APPLE-REASON",
        "category": "Required Reason APIs",
        "title": "Strict Rejection Gate for Declared Reason API Violations",
        "description": "Apple is initiating automated rejections for builds invoking system APIs like systemUptime, ProcessInfo, or UserDefaults without specific and valid reason codes mapped in the app bundle manifest.",
        "link": "https://developer.apple.com/news/?id=required-reason-apis",
        "pubDate": "Thu, 11 Jun 2026 11:00:00 GMT",
    },
    {
        "id": "PRIV-MOCK-APPLE-ATT",
        "category": "App Tracking Transparency",
        "title": "App Tracking Transparency Opt-In Enforcement Clarification",
        "description": "App Review clarifies that accessing the Advertising Identifier (IDFA) or sharing device fingerprints requires prior user opt-in via the ATTrackingManager prompt. Failing to present the prompt leads to an automatic rejection.",
        "link": "https://developer.apple.com/news/?id=att-enforcement",
        "pubDate": "Fri, 12 Jun 2026 12:00:00 GMT",
    },
    {
        "id": "PRIV-MOCK-APPLE-NUTRITION",
        "category": "Privacy Nutrition Labels",
        "title": "Storefront Validation of Privacy Nutrition Labels Mismatch",
        "description": "Apple requires all self-reported privacy labels in App Store Connect to be kept accurate. Discrepancies between compiled code transmission behavior and declared data safety labels will trigger review delays.",
        "link": "https://developer.apple.com/news/?id=privacy-nutrition-labels",
        "pubDate": "Sat, 13 Jun 2026 13:00:00 GMT",
    },
    {
        "id": "PRIV-MOCK-ANDROID-SAFETY",
        "category": "Data Safety",
        "title": "Google Play Store Data Safety Form Compliance Verification",
        "description": "Google Play increases automated static verification of app binaries to identify undeclared analytics and tracking SDK usage. Discrepancies in the Data Safety declaration will lead to update blockages.",
        "link": "https://support.google.com/googleplay/android-developer/answer/10787469",
        "pubDate": "Sun, 14 Jun 2026 14:00:00 GMT",
    },
    {
        "id": "PRIV-MOCK-ANDROID-USERDATA",
        "category": "User Data Policy",
        "title": "Google Play User Data and Explicit Prominent Disclosure Policy",
        "description": "Apps collecting sensitive user credentials, contacts, or device files must display a prominent, clear modal explaining what data is collected, followed by explicit user consent before any ingestion occurs.",
        "link": "https://support.google.com/googleplay/android-developer/answer/User-Data-Policy",
        "pubDate": "Mon, 15 Jun 2026 15:00:00 GMT",
    },
    {
        "id": "PRIV-MOCK-ANDROID-ADID",
        "category": "Advertising ID",
        "title": "Google Play Services Advertising ID Policy and Opt-Out Requirements",
        "description": "Apps declaring the AD_ID permission must support user opt-out and provide pathways to delete or reset the advertising identifier within the application interface or linked privacy statement.",
        "link": "https://support.google.com/googleplay/android-developer/answer/9899234",
        "pubDate": "Tue, 16 Jun 2026 16:00:00 GMT",
    },
    {
        "id": "PRIV-MOCK-ANDROID-PERMS",
        "category": "Runtime permissions",
        "title": "Mandatory Runtime Permission Flow and UX Validation",
        "description": "Google Play restricts broad access to system cameras, directories, and background resources. Apps must dynamically query permissions at runtime and supply clear rationales when users previously denied requests.",
        "link": "https://developer.android.com/guide/topics/permissions/overview",
        "pubDate": "Wed, 17 Jun 2026 17:00:00 GMT",
    },
    {
        "id": "PRIV-MOCK-ANDROID-LOCATION",
        "category": "Background location",
        "title": "Strict Review for ACCESS_BACKGROUND_LOCATION Permissions",
        "description": "Google Play strictly limits background location access. Developers must submit extensive core use-case justifications and prominently display persistent disclosures to clear the publishing gate.",
        "link": "https://developer.android.com/about/versions/14/changes/schedule-exact-alarms",
        "pubDate": "Thu, 18 Jun 2026 18:00:00 GMT",
    },
    {
        "id": "PRIV-MOCK-ANDROID-HEALTH",
        "category": "Health permissions",
        "title": "Health Connect and Health Permissions Compliance Mandate",
        "description": "Accessing Health Connect APIs requires completed console questionnaires and a dedicated, in-app health privacy statement explaining step or heart-rate tracking purposes.",
        "link": "https://developer.android.com/guide/topics/permissions/overview",
        "pubDate": "Fri, 19 Jun 2026 19:00:00 GMT",
    },
    {
        "id": "PRIV-MOCK-WEB-GDPR",
        "category": "GDPR",
        "title": "GDPR Compliance and Right to be Forgotten Controls on Web Interfaces",
        "description": "Web interfaces processing data from EU residents must provide strict opt-in checkboxes and accessible self-service data deletion and extraction features in compliance with data minimization.",
        "link": "https://eur-lex.europa.eu/eli/reg/2016/679/oj",
        "pubDate": "Sat, 20 Jun 2026 20:00:00 GMT",
    },
    {
        "id": "PRIV-MOCK-WEB-COOKIE",
        "category": "Cookie consent",
        "title": "ePrivacy Directive Cookie Consent Banner Mandatory Implementation",
        "description": "Non-essential tracking cookies and local variables must not be saved on initial load before the user explicitly registers cookie acceptance on the consent banner.",
        "link": "https://eur-lex.europa.eu/eli/dir/2002/58/oj",
        "pubDate": "Sun, 21 Jun 2026 21:00:00 GMT",
    },
    {
        "id": "PRIV-MOCK-WEB-LOCAL",
        "category": "Local storage",
        "title": "Secure Encryption for Sensitive Variables in localStorage",
        "description": "Storing plaintext authentication credentials or personal identifiers in localStorage is prohibited due to cross-site scripting risks. Store secrets securely and encrypt stored items.",
        "link": "https://eur-lex.europa.eu/eli/reg/2016/679/oj",
        "pubDate": "Mon, 22 Jun 2026 22:00:00 GMT",
    },
    {
        "id": "PRIV-MOCK-WEB-INDEXEDDB",
        "category": "IndexedDB",
        "title": "IndexedDB Data Retention and Cleanup Regulations",
        "description": "Databases holding offline records must respect user tracking consent preferences and execute complete cleanup routines when users logout or invoke deletion rights.",
        "link": "https://eur-lex.europa.eu/eli/reg/2016/679/oj",
        "pubDate": "Tue, 23 Jun 2026 23:00:00 GMT",
    },
    {
        "id": "PRIV-MOCK-WEB-SESSION",
        "category": "Session storage",
        "title": "Temporary Session Variable Safety and Clean State Execution",
        "description": "Session identifiers and tokens must be limited, shielded from un-authorized scripts, and terminated immediately upon browser window or tab closure.",
        "link": "https://eur-lex.europa.eu/eli/reg/2016/679/oj",
        "pubDate": "Wed, 24 Jun 2026 10:00:00 GMT",
    },
    {
        "id": "PRIV-MOCK-WEB-TRACKING",
        "category": "Tracking technologies",
        "title": "Third-Party Tracking Scripts and Marketing Pixel Management",
        "description": "Third-party pixels and analytics tags must remain inactive until explicit cookie preferences are registered. Unmanaged, silent script injection violates web compliance laws.",
        "link": "https://eur-lex.europa.eu/eli/dir/2002/58/oj",
        "pubDate": "Thu, 25 Jun 2026 11:00:00 GMT",
    },
]


def scan_codebase_for_privacy_signals(start_dir="."):
    """
    Scans the codebase for files containing signals related to each of the 16 requirements.
    """
    matches = {req: [] for req in TRACKED_REQUIREMENTS}
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
        req: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        for req, patterns in CATEGORY_SIGNALS.items()
    }

    for root, dirs, files in os.walk(start_dir):
        # Prune excluded directories in-place
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.endswith("Tests")]

        for file in files:
            # Check applicable file types
            if not file.endswith(
                (
                    ".kt",
                    ".java",
                    ".xml",
                    ".gradle",
                    ".kts",
                    ".json",
                    ".js",
                    ".ts",
                    ".md",
                    ".swift",
                    ".plist",
                    ".html",
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
                        for req, patterns in compiled_signals.items():
                            for pattern in patterns:
                                if pattern.search(line):
                                    matches[req].append(
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
    Classifies incoming announcements into the 16 privacy categories.
    """
    classified_updates = []

    for ann in announcements:
        title = ann.get("title", "")
        desc = ann.get("description", "")
        text_to_search = (title + " " + desc).lower()

        if keywords_filter:
            if not any(k.lower() in text_to_search for k in keywords_filter):
                continue

        # Match against categories
        matched_categories = []
        for req, keywords in CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in text_to_search:
                    matched_categories.append(req)
                    break

        if not matched_categories and ann.get("category"):
            matched_categories.append(ann["category"])

        if matched_categories:
            for req in matched_categories:
                classified_updates.append(
                    {
                        "id": ann.get("id", "PRIVACY-UPDATE-" + str(hash(title))[:6]),
                        "category": req,
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
        req = u["category"]
        citations_list.append(
            f"- **{req}**: [{u['title']}]({u['link']}) (Published: {u['pubDate']})"
        )

        files = scan_results.get(req, [])
        if files:
            for f in files:
                affected_files_set.add(f["file"])

        # Category-specific details
        if req == "Privacy Manifest":
            migration_steps.append(
                f"- **{req}**: Generate root PrivacyInfo.xcprivacy with tracking domains and data declarations."
            )
            impl_checklist.append(
                "- [ ] Add a root PrivacyInfo.xcprivacy to the Xcode project and check third-party SDK manifests."
            )
            risk_assessment.append(
                f"- *{req}*: Apple automatic upload rejection on build submission if PrivacyInfo.xcprivacy is missing or invalid."
            )
        elif req == "Required Reason APIs":
            migration_steps.append(
                f"- **{req}**: Declare correct reason codes for accesses to system APIs such as UserDefaults or active keyboard."
            )
            impl_checklist.append(
                "- [ ] Audit calls to system APIs like UserDefaults and add required reason codes inside PrivacyInfo.xcprivacy."
            )
            risk_assessment.append(
                f"- *{req}*: Automatic rejection from Apple App Store Connect for undeclared API category usage."
            )
        elif req == "App Tracking Transparency":
            migration_steps.append(
                f"- **{req}**: Trigger ATTrackingManager prompt before launching any tracking code or third-party ad frameworks."
            )
            impl_checklist.append(
                "- [ ] Configure NSUserTrackingUsageDescription in Info.plist and verify dynamic consent request calls."
            )
            risk_assessment.append(
                f"- *{req}*: Store rejection if cross-app tracing SDKs are activated before prompt acceptance."
            )
        elif req == "Privacy Nutrition Labels":
            migration_steps.append(
                f"- **{req}**: Align self-reported App Store privacy nutrition questions with actual runtime data transmissions."
            )
            impl_checklist.append(
                "- [ ] Audit email, phone, location, and device ID variables and populate data categories in App Store Connect."
            )
            risk_assessment.append(
                f"- *{req}*: Discrepancy between declared nutrition forms and codebase will trigger review blocks."
            )
        elif req == "Data Safety":
            migration_steps.append(
                f"- **{req}**: Keep Google Play Console Data Safety statements fully synchronized with integrated analytics and marketing SDK behaviors."
            )
            impl_checklist.append(
                "- [ ] Ensure firebase-analytics, AppsFlyer, or Facebook SDK usage matches Google Play declarations."
            )
            risk_assessment.append(
                f"- *{req}*: Google Play policy rejection due to mismatch between binary scans and Data Safety forms."
            )
        elif req == "User Data Policy":
            migration_steps.append(
                f"- **{req}**: Supply prominent in-app disclosure dialogs before collecting sensitive personal attributes."
            )
            impl_checklist.append(
                "- [ ] Add a modal with an accept/consent button prior to registration or ingestion of user credentials."
            )
            risk_assessment.append(
                f"- *{req}*: App removal or suspension on Google Play for silent, un-disclosed user-data processing."
            )
        elif req == "Advertising ID":
            migration_steps.append(
                f"- **{req}**: Declare com.google.android.gms.permission.AD_ID in the manifest and ensure opt-out pathways are implemented."
            )
            impl_checklist.append(
                "- [ ] Declare AD_ID permission and add an in-app toggle for advertising ID reset/deletion requests."
            )
            risk_assessment.append(
                f"- *{req}*: Automated release blocking if targeting Android 12+ and using advertising libraries without declarations."
            )
        elif req == "Runtime permissions":
            migration_steps.append(
                f"- **{req}**: Verify runtime permissions dynamically before initializing camera, microphone, or file accesses."
            )
            impl_checklist.append(
                "- [ ] Wrap hardware triggers with checkSelfPermission and display rationales on denial."
            )
            risk_assessment.append(
                f"- *{req}*: App crashes or storefront flags for requesting sensitive access blocks without rationales."
            )
        elif req == "Background location":
            migration_steps.append(
                f"- **{req}**: Limit background location access. Provide persistent disclosures if ACCESS_BACKGROUND_LOCATION is required."
            )
            impl_checklist.append(
                "- [ ] Verify that ACCESS_BACKGROUND_LOCATION is only declared if strictly required for core operations."
            )
            risk_assessment.append(
                f"- *{req}*: Instant publishing blockages on Google Play if background location is not essential and justified."
            )
        elif req == "Health permissions":
            migration_steps.append(
                f"- **{req}**: Maintain a separate health-specific privacy link if reading health indices from Health Connect."
            )
            impl_checklist.append(
                "- [ ] Implement HealthConnectClient authorization gates and reference dedicated health privacy policies."
            )
            risk_assessment.append(
                f"- *{req}*: Immediate console rejections if health APIs are imported without dedicated health privacy policies."
            )
        elif req == "GDPR":
            migration_steps.append(
                f"- **{req}**: Integrate strict opt-in checkboxes and self-service delete pathways for EU web users."
            )
            impl_checklist.append(
                "- [ ] Build user-facing GDPR forms and functional account deletion triggers to satisfy data minimization."
            )
            risk_assessment.append(
                f"- *{req}*: Serious non-compliance risk under GDPR, potentially triggering heavy regulatory fines."
            )
        elif req == "Cookie consent":
            migration_steps.append(
                f"- **{req}**: Construct cookie consent gates that block third-party analytics cookies from being written before opt-in."
            )
            impl_checklist.append(
                "- [ ] Integrate a Cookie Consent Banner and check user preferences before updating document.cookie."
            )
            risk_assessment.append(
                f"- *{req}*: Direct violation of the ePrivacy Directive if tracking tags load automatically without user consent."
            )
        elif req == "Local storage":
            migration_steps.append(
                f"- **{req}**: Avoid storing plaintext user credentials, JWTs, or session keys inside localStorage."
            )
            impl_checklist.append(
                "- [ ] Implement encryption wrappers for critical localStorage variables or migrate them to secure cookies."
            )
            risk_assessment.append(
                f"- *{req}*: Vulnerability to cross-site scripting (XSS) attacks leading to account hijacking."
            )
        elif req == "IndexedDB":
            migration_steps.append(
                f"- **{req}**: Clean database rows on user logout or deletion to preserve clean state rules."
            )
            impl_checklist.append(
                "- [ ] Add indexedDB database wipe logic on user sign-out or account removal."
            )
            risk_assessment.append(
                f"- *{req}*: Persistent user tracking records left on shared browsers, violating right to erase rules."
            )
        elif req == "Session storage":
            migration_steps.append(
                f"- **{req}**: Clear temporary session data promptly when tab closure is detected."
            )
            impl_checklist.append(
                "- [ ] Ensure sensitive temporary identifiers in sessionStorage are cleared or encrypted."
            )
            risk_assessment.append(
                f"- *{req}*: Session token persistence risks if sensitive values are left un-monitored in sessionStorage."
            )
        elif req == "Tracking technologies":
            migration_steps.append(
                f"- **{req}**: Block third-party tracking pixels (Google Analytics, Hotjar) from initiating until cookie preferences are accepted."
            )
            impl_checklist.append(
                "- [ ] Block silent injection of gtag or fbq scripts before consent validation."
            )
            risk_assessment.append(
                f"- *{req}*: Serious regulatory warning notifications for silent tracking of users before consent."
            )
        else:
            migration_steps.append(
                f"- **{req}**: Run comprehensive audits for {req} to ensure compliance."
            )
            impl_checklist.append(
                f"- [ ] Audit files matching {req} and update configuration variables."
            )
            risk_assessment.append(f"- *{req}*: General regulatory compliance risk.")

    citations_str = "\n".join(citations_list)

    if affected_files_set:
        affected_files_str = "\n".join(
            f"- `{f}`" for f in sorted(list(affected_files_set))
        )
    else:
        affected_files_str = "- *No specific files containing matching category patterns were automatically detected. (Perform manual review of configuration variables).* "

    migration_steps_str = "\n".join(migration_steps)
    impl_checklist_str = "\n".join(impl_checklist)
    risk_assessment_str = "\n".join(risk_assessment)

    pr_template = f"""# PULL REQUEST DRAFT: Mobile and Web Privacy Requirements Compliance Update

## 1. Summary
This pull request brings the application into complete compliance with all monitored global mobile and web privacy requirements. It addresses Privacy Manifests, Required Reason APIs, App Tracking Transparency, Data Safety, GDPR, Cookie Consent, and other sensitive storage structures to satisfy modern platform publishing gates.

## 2. Background
Storefront operators (Apple and Google Play) and regional regulators enforce strict privacy rules regarding user consent, runtime permissions, secure local storage, and accurate declarations. Non-compliance results in build rejections, account suspension, or heavy fines.

## 3. Regulatory change
- **Apple Storefront**: Mandatory root Privacy Manifest configuration, Required Reason API declarations, and accurate Nutrition Labels.
- **Android Storefront**: Strict Data Safety declarations, prominent sensitive disclosures, background location limits, and Health Connect approvals.
- **Web Applications**: GDPR data minimization and right to be forgotten rights, ePrivacy Directive cookie consent controls, and secure local/session/indexedDB handling.

## 4. Official citations
{citations_str}

## 5. Affected files
{affected_files_str}

## 6. Risk assessment
{risk_assessment_str}
- **Overall Standing**: High risk of update blockage, storefront rejection, or compliance complaints if these updates are not actively merged.

## 7. Migration steps
{migration_steps_str}

## 8. Backward compatibility
All configuration and declarative adjustments are fully backward-compatible. No breaking API updates or customer-facing flow restrictions are introduced. Core legacy components continue operating normally.

## 9. Implementation checklist
{impl_checklist_str}
- [ ] Run the automated compliance checks locally to verify validation.

## 10. Testing checklist
- [ ] Confirm Xcode build compiles and bundles the PrivacyInfo.xcprivacy correctly.
- [ ] Verify that Google Play data declarations align with integrated SDK analytics.
- [ ] Run browser diagnostics to ensure third-party pixels are blocked prior to Cookie Banner opt-in.
- [ ] Validate account deletion triggers wipe associated localStorage and indexedDB files.

## 11. Documentation checklist
- [ ] Update internal compliance playbooks with completed tasks.
- [ ] Connect the revised privacy statement URL inside the store console dashboards.
- [ ] Update `docs/PRIVACY-POLICY-MIGRATION.md` with resolved log entries.

## 12. Compliance impact
- **Submission Security**: Eliminates upload-time blocks, review delays, and automatic rejections on Apple and Google Play.
- **Regulatory Safety**: Insulates the brand against GDPR and ePrivacy complaints, reinforcing data protection.
- **Consumer Trust**: Increases transparency through clear, prominent disclosures and explicit consent gates.

## 13. Breaking changes
No structural breaking changes or functional restrictions are introduced.

## 14. Review checklist
- [ ] Code changes and PR text are completely emoji-free.
- [ ] Core configuration variables are securely mapped without placeholder records.
- [ ] Consent prompts and prominent disclosures match required styling guidelines.

## 15. Approver recommendations
Ensure that compliance counsel registers the updated privacy statements on the live portal before merging. Double-check that compiled third-party SDK dependencies ship with signed privacy manifests prior to final release bundling.
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
        "## Monitored Privacy Requirements Update Log",
        "",
    ]

    for idx, u in enumerate(updates, 1):
        lines.append(f"### {idx}. [{u['category']}] {u['title']}")
        lines.append(f"- **Published Date**: {u['pubDate']}")
        lines.append(f"- **Official Resource**: [{u['link']}]({u['link']})")
        lines.append(f"- **Description**: {u['description']}")
        lines.append("")

    lines.append("## Automated Migration Recommendations & Implementation Tasks")
    lines.append("")

    for u in updates:
        req = u["category"]
        lines.append(f"### Tasks for {req}")
        lines.append(
            "- **Regulatory Impact**: High priority. Complete steps to satisfy storefront/regulatory audits."
        )

        if req == "Privacy Manifest":
            lines.append(
                "- [ ] **Task 1**: Integrate `PrivacyInfo.xcprivacy` at Xcode project root."
            )
            lines.append(
                "- [ ] **Task 2**: Cross-reference third-party SDK dependencies for signed manifests."
            )
        elif req == "Required Reason APIs":
            lines.append(
                "- [ ] **Task 1**: Audit references to file timestamps, system boot time, or `UserDefaults`."
            )
            lines.append(
                "- [ ] **Task 2**: Supply valid reasons inside the `NSPrivacyAccessedAPITypes` manifest block."
            )
        elif req == "App Tracking Transparency":
            lines.append(
                "- [ ] **Task 1**: Wire `ATTrackingManager.requestTrackingAuthorization` prior to tracker initialization."
            )
            lines.append(
                "- [ ] **Task 2**: Populate `NSUserTrackingUsageDescription` in Info.plist."
            )
        elif req == "Data Safety":
            lines.append(
                "- [ ] **Task 1**: Audit runtime tracking dependencies (Firebase, AppsFlyer) and update declarations."
            )
            lines.append(
                "- [ ] **Task 2**: Synchronize Google Play Console Data Safety form inputs."
            )
        elif req == "Cookie consent":
            lines.append(
                "- [ ] **Task 1**: Configure Cookie Consent Banner to block tracking scripts before opt-in."
            )
            lines.append(
                "- [ ] **Task 2**: Provide granular cookies preferences selectors."
            )
        elif req == "GDPR":
            lines.append(
                "- [ ] **Task 1**: Supply user-accessible account deletion button in-app/on-web."
            )
            lines.append(
                "- [ ] **Task 2**: Ensure user data purging covers linked third-party analytics storage."
            )
        else:
            lines.append(
                f"- [ ] **Task**: Review, implement, and verify all compliance criteria for {req}."
            )
        lines.append("")

    lines.append("<!-- PRIVACY_POLICY_MONITOR_END -->")

    try:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"Privacy documentation updated successfully at: {output_filepath}")
    except Exception as e:
        print(f"Error writing documentation to {output_filepath}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor all Mobile and Web Privacy Requirements"
    )
    parser.add_argument(
        "--live", action="store_true", help="Fetch live Google Play & Apple policy feeds"
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
        help="Filepath to save the drafted PR",
    )

    args = parser.parse_args()

    announcements = []

    if args.live:
        print("Fetching live developer RSS feeds...")
        announcements.extend(
            parse_rss_feed(
                "https://android-developers.googleblog.com/feeds/posts/default"
            )
        )
        announcements.extend(
            parse_rss_feed("https://developer.apple.com/news/rss/news.rss")
        )

    if args.mock or (not args.live and not args.mock) or not announcements:
        print(
            "Using comprehensive mock Privacy updates for compliance scanning..."
        )
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

    print(
        f"Monitored and classified {len(classified_updates)} policy/requirement updates:"
    )
    for idx, u in enumerate(classified_updates, 1):
        print(f" {idx}. [{u['category']}] {u['title']}")

    print(f"Scanning codebase under '{args.dir}' for privacy integration signals...")
    scan_results = scan_codebase_for_privacy_signals(args.dir)

    total_matches = sum(len(matches) for matches in scan_results.values())
    print(f"Found {total_matches} signal matches in code.")

    os.makedirs(os.path.dirname(args.output_docs) or ".", exist_ok=True)
    update_documentation_report(classified_updates, args.output_docs)

    pr_draft = generate_pull_request_draft(classified_updates, scan_results)

    os.makedirs(os.path.dirname(args.pr_output) or ".", exist_ok=True)
    try:
        with open(args.pr_output, "w", encoding="utf-8") as f:
            f.write(pr_draft)
        print(f"PR draft written successfully to: {args.pr_output}")
    except Exception as e:
        print(f"Failed to write PR draft to {args.pr_output}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
