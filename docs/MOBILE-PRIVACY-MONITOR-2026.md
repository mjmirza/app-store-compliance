# Mobile and Web Privacy Compliance Monitor Guide (2026)

This reference manual provides a comprehensive analysis of mobile and web privacy regulations, mandatory store compliance policies, and automated auditing patterns for Apple App Store, Google Play, and Web application deployment.

## Part 1. Apple App Store Privacy Requirements

### 1. Privacy Manifest (PrivacyInfo.xcprivacy)
Apple enforces mandatory Privacy Manifests for any app or third-party SDK that accesses designated Required Reason APIs.
- Official Citation: Apple Developer Documentation - Describing data use in privacy manifests.
- Compliance Mandate: Any usage of APIs in key areas (such as UserDefaults, systemUptime, ProcessInfo, or NSFileManager) must be declared with an approved reason code in `PrivacyInfo.xcprivacy`.
- Implementation Check: The manifest must contain the key `NSPrivacyAccessedAPITypes` declaring the specific APIs and the precise, valid reason keys specified by Apple.
- Critical Rejection Risk: Submissions containing third-party SDKs or direct code that call these APIs without a matching declaration are blocked at the upload stage.

### 2. Required Reason APIs
Required Reason APIs are divided into several categories:
- File Timestamp APIs: Accessing file creation/modification dates.
- System Boot Time APIs: Accessing system uptime/boot-related metrics.
- Disk Space APIs: Querying free disk space.
- Active Keyboard APIs: Detecting active input methods.
- User Defaults APIs: Reading or writing user preferences.
Each category requires one or more approved, specific reasons (e.g., storing user preferences locally via UserDefaults). General-purpose logging or tracking is not a permitted reason.

### 3. App Tracking Transparency (ATT)
Under App Store Review Guideline 5.1.2(i), any cross-app tracking requires explicit user consent via the App Tracking Transparency framework.
- Compliance Mandate: You must request permission using the `ATTrackingManager.requestTrackingAuthorization(completionHandler:)` API before reading the Advertising Identifier (IDFA).
- Purpose String: A localized purpose string must be present in the `Info.plist` file under `NSUserTrackingUsageDescription`.
- Rejection Risk: Accessing IDFA or other tracking SDKs (e.g., Adjust, AppsFlyer, Facebook SDK) without showing the ATT prompt leads to immediate rejection.

### 4. Privacy Nutrition Labels
Developers must accurately declare data collection practices in App Store Connect.
- Compliance Mandate: Declare if data is linked to the user's identity or used for tracking.
- Implementation Gaps: Rejections occur when there is a mismatch between what an imported SDK does (e.g., Firebase collecting device identifiers for analytics) and what the developer has disclosed in the App Store Connect Privacy Questionnaire.

---

## Part 2. Google Play Privacy Requirements

### 1. Data Safety
Google Play requires developers to complete a comprehensive Data Safety form.
- Official Citation: Google Play Developer Policy Center - Data Safety Section.
- Compliance Mandate: You must disclose the collection, sharing, and security practices of the app, including data type (location, personal info, financial info, identifiers, etc.) and purpose (analytics, advertising, functionality).
- Rejection Risk: Automatic or manual detection of analytics or advertising SDKs (such as Firebase Analytics or AdMob) that collect data not declared in the Data Safety form triggers immediate policy enforcement.

### 2. User Data Policy
Google Play's User Data policy mandates clear, prominent disclosures and explicit consent for personal and sensitive data.
- Compliance Mandate: If the app accesses or uploads personal data (e.g., contacts, personal files, SMS), it must present a prominent in-app disclosure before the access occurs.
- Disclosure Standards: The disclosure must be shown in the normal usage flow of the app, explain exactly what is being collected, how it will be used, and require explicit user action (e.g., tapping an "Accept" button).

### 3. Advertising ID
To safeguard user privacy, Google Play restricts the use of the Advertising ID.
- Compliance Mandate: For apps targeting Android 12 (API level 31) or higher, developers must declare the `com.google.android.permission.AD_ID` permission in their `AndroidManifest.xml` to access the Advertising ID.
- Rejection Risk: If the permission is omitted, the Advertising ID is replaced with zeros. If an Ad SDK is present but the permission is missing, or if the permission is declared for an app targetting children, it is flagged as non-compliant.

### 4. Runtime Permissions
Sensitive system capabilities must be requested dynamically at runtime.
- Compliance Mandate: Check permissions using `checkSelfPermission` and request them dynamically via `requestPermissions` or the modern Activity Result APIs.
- Core Principle: Apps must not access sensitive APIs (such as Camera, Microphone, or Location) without verifying that the permission has been granted by the user at runtime.

### 5. Background Location
ACCESS_BACKGROUND_LOCATION is treated as a highly sensitive permission under Google Play policy.
- Compliance Mandate: Background location must be essential to the core functionality of the app.
- Review Requirement: Developers must submit a detailed declaration form, include a prominent disclosure inside the app, and provide a video demonstration showing how the feature works in the background.

### 6. Health Permissions
Accessing health or physical activity data requires specialized compliance.
- Compliance Mandate: Apps accessing health, fitness, or wellness data (including Google Fit or Health Connect APIs) must declare the corresponding permissions and submit the Health Connect compliance form.
- Core Rule: Data accessed via Health Connect must never be sold or transferred to data brokers or advertising platforms.

---

## Part 3. Web Privacy Requirements

### 1. GDPR (General Data Protection Regulation)
The EU GDPR enforces strict rules on the processing of personal data on the web.
- Official Citation: Regulation (EU) 2016/679 (General Data Protection Regulation).
- Compliance Mandates:
  - Valid user consent must be freely given, specific, informed, and unambiguous.
  - Users must have the right to withdraw consent easily at any time.
  - Apps must provide easy methods for users to request data access or account/data deletion (Right to Erasure).

### 2. Cookie Consent
Websites must obtain prior, explicit consent before storing or accessing non-essential cookies.
- Compliance Mandates:
  - Cookie banners must not have pre-ticked consent boxes.
  - Users must be able to "Reject All" non-essential cookies as easily as they can "Accept All".
  - Strictly necessary cookies required for core site functionality do not require prior consent but must still be disclosed.

### 3. Local Storage
Web LocalStorage (`window.localStorage`) persists data across browser sessions.
- Compliance Mandates:
  - Do not store sensitive authentication tokens (e.g., raw JWTs), passwords, or personally identifiable information (PII) in LocalStorage.
  - LocalStorage is vulnerable to Cross-Site Scripting (XSS) attacks. If XSS occurs, an attacker can extract all LocalStorage tokens.
  - For sensitive session-related identifiers, use secure, HttpOnly, and SameSite cookies instead.

### 4. IndexedDB
IndexedDB is a transactional database system for storing structured data locally.
- Compliance Mandates:
  - Any health, financial, or highly personal user data stored in IndexedDB must be encrypted.
  - Use cryptographically secure algorithms (e.g., Web Crypto API with AES-GCM) to encrypt database stores.

### 5. Session Storage
Web SessionStorage (`window.sessionStorage`) persists data for the duration of the page session.
- Compliance Mandates:
  - Ensure sessionStorage is explicitly cleared upon user sign-out or session termination (`sessionStorage.clear()`).
  - Do not leak session data or leave sensitive information lingering in the browser state after logout.

### 6. Tracking Technologies
Tracking pixels, scripts, and fingerprinting technologies must be tightly regulated.
- Compliance Mandates:
  - Do not load tracking scripts (such as Google Tag Manager, Google Analytics, or Facebook Pixel) until the user has explicitly consented via the cookie/privacy consent banner.
  - Do not use canvas fingerprinting or hardware-based fingerprinting techniques to track users across websites, as modern privacy regulations (GDPR, CCPA) treat fingerprints as personal data.

---

## Part 4. Automated Compliance Auditing

This project includes automated checks in `agent-os/hooks/app-store-compliance-guard.sh` to statically scan codebases for privacy-related non-compliance.

### Static Verification Recipes:
- Apple Privacy Manifest: Scans for the presence of `PrivacyInfo.xcprivacy` when required SDKs or APIs are found.
- Google Play Data Safety: Matches the presence of analytics or tracking packages (e.g., AdMob, Firebase) against data disclosures.
- Android Advertising ID: Flags apps targeting API 31+ that use advertising services without declaring `com.google.android.permission.AD_ID`.
- Web GDPR & Cookie Consent: Analyzes web files (`.html`, `.js`, `.ts`) for the use of tracking technologies, cookies, or storage APIs, checking for corresponding consent and clearing controls.
- Web Secure Storage: Detects the storage of items in `localStorage` or `sessionStorage` and flags potential exposures if secure options or encryption hooks are absent.
