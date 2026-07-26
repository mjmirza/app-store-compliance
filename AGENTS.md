# App Store and Google Play Compliance Instructions for Agents

This file contains strict guidelines and instructions that every agent operating in this repository must adhere to. Every release of an iOS or Android application in this repository must be thoroughly reviewed as if it were about to be submitted to the Apple App Store and Google Play.

All findings and issues must be reported to the developers before any release is finalized.

## Required Release Review Checks

Before any release, the agent must verify the following fifteen critical areas of compliance and platform requirements.

### 1. Permissions
Verify that the app requests only the minimum necessary permissions required for its functionality.
- For iOS: Verify that all requested permissions have explicit, specific, and clear NSCameraUsageDescription, NSLocationWhenInUseUsageDescription, NSPhotoLibraryUsageDescription, NSMicrophoneUsageDescription, and NSContactsUsageDescription keys in Info.plist.
- For Android: Verify that background permissions (such as ACCESS_BACKGROUND_LOCATION, MANAGE_EXTERNAL_STORAGE, SMS, and Call Log permissions) have corresponding core feature justifications and required declarations, or are removed.
- Verify that standard permission purpose strings are descriptive, explain why the permission is needed, and are never vague or empty.

### 2. Privacy Disclosures
Verify that all data collection practices are transparent and properly disclosed.
- Verify that every runtime data collection has user consent before it happens.
- Ensure that for any tracking or advertising SDK (like AppsFlyer, Adjust, Branch, Facebook SDK, or IDFA), the App Tracking Transparency (ATT) prompt is implemented and NSUserTrackingUsageDescription is defined.
- On Android, verify that the Google Play Data Safety declaration matches actual runtime and SDK data collection behavior.

### 3. Screenshots
Verify that app store screenshots comply with platform requirements.
- Ensure screenshots depict the actual application in use, rather than mere splash, logo, or login screens.
- Do not include device frame wrappers around the app in preview videos.
- Verify that screenshots are truthful and represent the actual app features.

### 4. Metadata
Verify that all store metadata fields comply with rules and limits.
- Confirm that the app name and subtitle are each within the 30-character limit.
- Ensure keywords do not exceed the 100-character limit.
- Verify that keywords use commas with no spaces and do not duplicate words already in the name or subtitle.
- Ensure metadata fields contain no banned decoration (e.g., emojis, all-caps words, or ranking and pricing claims like "#1", "top app", "best app", or "free").
- Verify that there are no references to other platforms (such as "Android" or "Google Play" references on iOS, and vice versa).
- Verify that there is no future functionality language (such as "coming soon" or "will be available in a future update").
- Ensure no placeholder text, test data, or curse words exist in any metadata fields.

### 5. Age Rating
Verify the age rating and content questionnaire details.
- Verify that the App Store and Google Play age or content rating questionnaires are answered honestly.
- For iOS, ensure the updated age rating questionnaire (13 plus, 16 plus, 18 plus) is completed.
- Ensure any generative AI or user-generated content features carry appropriate age restrictions.

### 6. AI Disclosures
Verify compliance with platform artificial intelligence policies.
- If personal data is shared with a third-party AI or LLM (e.g., OpenAI, Anthropic, Gemini), a consent modal naming the provider and the data types must be shown to the user before transmission.
- For EU users, show a clear in-app notice that the user is interacting with AI.
- Ensure that any AI-generated content (audio, image, video, text) carries machine-readable and visible markings.
- Ensure that generative AI integrations have content filtering, reporting, blocking, and abuse safeguards.
- For the China storefront, remove any references to external AI services (like ChatGPT or OpenAI) to avoid regional rejections.

### 7. Subscription Disclosures
Verify that subscriptions and in-app pricing disclosures are clear and non-misleading.
- Ensure subscription terms, renewal, charges, and cancellation flows are fully disclosed before purchase.
- The actual amount billed must be shown at least as prominently as any calculated per-month rate (e.g., on annual subscriptions).
- Ensure a visible and functional "Restore Purchases" button is present for all non-consumable purchases and non-renewing subscriptions.

### 8. Payment Compliance
Verify that payments are routed correctly.
- Digital goods, services, and content sold in the app must use the official store billing APIs (StoreKit for iOS, Play Billing for Android).
- External payment SDKs (like Stripe or PayPal) are prohibited for digital goods unless the app qualifies for a documented exempt category.
- Confirm that any random reward mechanic (loot box, gacha, etc.) discloses the exact odds before purchase.

### 9. Accessibility
Verify compliance with platform and legal accessibility standards.
- Static accessibility checks must enforce compatibility with screen readers (VoiceOver on iOS, TalkBack on Android).
- Ensure support for Dynamic Type (font scaling), Reduce Motion, color contrast, haptic feedback, and keyboard navigation.
- The app must meet WCAG 2.1 AA and EN 301 549 standards.

### 10. Legal Documents
Verify that necessary legal agreements are linked and visible.
- Ensure that the app's Terms of Service and Privacy Policy links are visible in the app description, on the paywall screen, and within the app's settings.
- Ensure DSA (Digital Services Act) trader status is declared and verified in App Store Connect where required.

### 11. Support URL
Verify that the support link in the store listing is valid and reachable.
- Ensure the support URL loads correctly and points to a functioning contact path for users during the entire review process.

### 12. Privacy Policy
Verify the privacy policy is accessible and accurate.
- A functional privacy policy URL must be linked in the store listing and reachable from within the app.
- Ensure the privacy policy accurately describes all data collection, sharing, and retention practices, including those of third-party SDKs.

### 13. Terms of Service
Verify the terms of service are accessible and accurate.
- Ensure a terms of service or EULA link is accessible to the user prior to registration or making any in-app purchase.

### 14. Export Compliance
Verify export compliance configurations.
- Ensure that export compliance is properly declared.
- For iOS, set the ITSAppUsesNonExemptEncryption key in Info.plist to prevent the build from stalling in the "Missing Compliance" state.

### 15. Encryption Declarations
Verify encryption compliance.
- Upload any required encryption declarations (such as the France ANSSI encryption declaration) in the platform console if the app uses non-exempt encryption.

## Rules on Tone and Content of Deliverables

- Do not use any emojis, emoticons, or graphical symbols in pull request text, scripts, reports, comments, source code, or anywhere else in the repository. Keep all text plain and professional.
- Report all findings and issues in a clean markdown table or list, detailing the violation, the severity (Critical, High, Medium, Low), the specific file or field, and the exact remediation required.
