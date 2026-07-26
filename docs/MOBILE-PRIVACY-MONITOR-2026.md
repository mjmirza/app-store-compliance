# Mobile and Web Privacy Compliance Guide (2026)

This playbook establishes the reference and automated validation framework to ensure compliance with modern privacy requirements across iOS, Android, and Web platforms. Use this guide to identify missing disclosures and implementation gaps before submitting your applications to their respective app stores or deploying to production.

---

## 1. Apple Privacy Compliance

Apple enforces highly strict, programmatic checks at build upload and review times. Failure to comply with any of these rules results in an automatic binary rejection or review block.

### 1.1 Privacy Manifest (PrivacyInfo.xcprivacy)
- **Rule:** Every app and third-party SDK must bundle a `PrivacyInfo.xcprivacy` manifest file detailing the types of data collected, tracking practices, and any usage of Required Reason APIs.
- **Implementation Gap:** Missing the manifest entirely or failing to include declarations for embedded third-party SDKs that collect data or perform tracking. Each bundled framework or library must ship with its own signed privacy manifest.
- **Verification:** Search for `PrivacyInfo.xcprivacy` files in the app bundle and verify that all collected data types are mapped correctly.

### 1.2 Required Reason APIs
- **Rule:** Apple designates specific APIs as Required Reason APIs, including system uptime, file timestamps, active keyboards, user defaults, and disk space. If your code or an embedded SDK calls these, you must declare the approved reason code in your privacy manifest.
- **Implementation Gap:** Declaring an API without specifying an approved reason code, or using an unapproved API category, which triggers automatic App Store Connect build rejection.
- **Verification:** Scan the codebase for symbols like `NSFileManager`, `UserDefaults`, `systemUptime`, or `ProcessInfo` and cross-reference with the `NSPrivacyAccessedAPITypes` array in your privacy manifest.

### 1.3 App Tracking Transparency (ATT)
- **Rule:** Before accessing the advertising identifier (IDFA) or tracking users across other apps/websites, you must show the App Tracking Transparency prompt and request permission.
- **Implementation Gap:** Presenting third-party tracking or advertising SDKs (such as Facebook, AppsFlyer, Adjust, or Branch) without calling the ATT prompt or omitting `NSUserTrackingUsageDescription` from `Info.plist`.
- **Verification:** Run static analysis to detect tracking SDK references and verify that `ATTrackingManager.requestTrackingAuthorization` is called before initialization.

### 1.4 Privacy Nutrition Labels
- **Rule:** Developers must complete the self-reported Privacy Nutrition Labels questionnaire in App Store Connect. The declared labels must align with actual data collection and tracking observed at runtime.
- **Implementation Gap:** Failing to declare data collection types such as email address, phone number, location, or purchase history in the App Store Connect portal while the codebase actively transmits this information.
- **Verification:** Audit all outgoing API request payloads and ensure that any personally identifiable information (PII) corresponds directly with the submitted nutrition labels.

---

## 2. Android Privacy Compliance

Google Play enforces a multi-tiered compliance policy, backed by automated static scanning and human verification, focusing heavily on user consent and runtime capability access.

### 2.1 Data Safety
- **Rule:** The Google Play Data Safety form requires developers to provide clear, granular declarations regarding what user data is collected, shared, and how it is secured (e.g., encryption in transit).
- **Implementation Gap:** A discrepancy between the declared Data Safety form and actual runtime behavior, specifically around bundled analytics, advertising, or attribution SDKs that collect data silently.
- **Verification:** Scan dependencies for known tracking or marketing libraries and verify that their collection practices match the Google Play Console declarations.

### 2.2 User Data Policy
- **Rule:** Personal and sensitive user data must be handled securely and require a prominent, explicit in-app disclosure followed by user consent before collection.
- **Implementation Gap:** Accessing or transferring contacts, SMS, device accounts, or file systems without a prominent disclosure or before the user explicitly clicks an consent button.
- **Verification:** Audit onboarding and authentication flows to confirm that privacy policies and disclosures are displayed prior to data collection.

### 2.3 Advertising ID
- **Rule:** Apps targeting Android 12 (API level 31) or higher that use the Google Play Services Advertising ID must declare the `com.google.android.gms.permission.AD_ID` permission in the manifest.
- **Implementation Gap:** Declaring the advertising ID permission without providing a mechanism inside the app or the privacy policy to opt out of interest-based ads or request advertising ID reset/deletion.
- **Verification:** Search for the `AD_ID` permission in `AndroidManifest.xml` and confirm that opt-out preferences are fully supported.

### 2.4 Runtime Permissions
- **Rule:** Sensitive permissions must be requested dynamically at runtime rather than assuming access is granted. The app should check, request, and gracefully handle permission denial.
- **Implementation Gap:** Invoking system features (e.g., camera or contacts) without checking for permission, or failing to present an in-app rationale prior to the system dialog when requested a second time.
- **Verification:** Trace calls to permission-checking methods and verify that rationales are shown when `shouldShowRequestPermissionRationale` returns true.

### 2.5 Background Location
- **Rule:** Google Play strictly restricts the use of `ACCESS_BACKGROUND_LOCATION`. It is permitted only if background location is essential to the core functionality of the application.
- **Implementation Gap:** Requesting background location for features that could be accomplished with foreground access, or failing to present a highly visible, persistent prominent disclosure.
- **Verification:** Ensure `ACCESS_BACKGROUND_LOCATION` is absent unless fully justified by a core use case, and verify the prominent disclosure UX.

### 2.6 Health Permissions
- **Rule:** Access to health, fitness, or wellness data (including APIs like Health Connect) requires extensive developer declarations, a prominent disclosure, and explicit user consent.
- **Implementation Gap:** Integrating Health Connect SDKs or querying health permissions (such as steps or heart rate) without completing the Health Connect integration questionnaire in Google Play Console.
- **Verification:** Locate health-related permissions in the manifest and ensure a specialized health privacy policy is accessible inside the app.

---

## 3. Web Privacy Compliance

Web applications must adhere to international regulations like the General Data Protection Regulation (GDPR) and ePrivacy Directive. Static analysis of local storage, session storage, databases, cookies, and tracking tags is necessary to prevent compliance failures.

### 3.1 GDPR
- **Rule:** Under GDPR, processing personal data of EU residents requires a legal basis, most commonly explicit, freely-given opt-in consent. Users must also be provided with the "Right to be Forgotten" (data deletion) and data portability.
- **Implementation Gap:** Processing or storing IP addresses, names, emails, or device identifiers without obtaining prior opt-in consent or lacking a functional data deletion request mechanism.
- **Verification:** Confirm that GDPR consent gates are active for all data ingestion pipelines and that an explicit deletion request option is available to users.

### 3.2 Cookie Consent
- **Rule:** Non-essential cookies (such as analytics, tracking, or marketing cookies) must not be written or accessed before the user has given explicit consent via a Cookie Consent banner.
- **Implementation Gap:** Injecting tracking cookies on initial page load before the user interacts with the consent banner, or failing to provide a preference manager.
- **Verification:** Check that all analytical or marketing script tags are delayed or conditionally executed only after consent is recorded.

### 3.3 Local Storage
- **Rule:** Sensitive personal data, session tokens, or authentication credentials should not be stored in unencrypted plain text within `localStorage`, as it is vulnerable to Cross-Site Scripting (XSS) attacks.
- **Implementation Gap:** Writing JWT tokens, passwords, or user profile information directly to `localStorage` without encryption or proper lifecycle management.
- **Verification:** Scan for `localStorage.setItem` calls and verify that sensitive keys are encrypted or moved to secure cookies (HttpOnly, Secure, SameSite).

### 3.4 IndexedDB
- **Rule:** Structured offline client-side data stored in `indexedDB` must respect user consent preferences, apply secure encryption for sensitive files, and provide absolute cleanup mechanisms.
- **Implementation Gap:** Creating object stores containing personal health, financial, or tracking data without validation of consent, or leaving databases orphaned after user logout.
- **Verification:** Review `indexedDB.open` calls and verify that database instances are wiped during account deletion or logout.

### 3.5 Session Storage
- **Rule:** Temporary sensitive details stored in `sessionStorage` must be limited, protected against unauthorized script access, and cleared immediately when the tab or window is closed.
- **Implementation Gap:** Leaving exposed active session data in `sessionStorage` without security controls or validation, leading to potential session hijacking.
- **Verification:** Scan for `sessionStorage.setItem` and ensure no highly sensitive data is left plain.

### 3.6 Tracking Technologies
- **Rule:** Third-party tracking scripts, tracking pixels, and analytics tags (e.g., Google Analytics, Facebook Pixel, Hotjar) must be explicitly managed, declared in the privacy policy, and disabled by default until consent is obtained.
- **Implementation Gap:** Loading tracking scripts dynamically or statically via script tags on page load without checking the user's consent status.
- **Verification:** Verify that analytics and pixel scripts are loaded conditionally based on cookie preferences.

---

## 4. Identifying Gaps and Verifying Compliance

To integrate these requirements into your release workflows, the App Store Compliance Guard automatically scans source code for known privacy violation patterns. Every check maps to the strict guidelines established above, preventing costly rejections before your build leaves the developer machine.
