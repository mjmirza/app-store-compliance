# Platform and Regulatory Compliance Report

This report evaluates current platform and global regulatory compliance status for Apple App Store (iOS and iPadOS) and Google Play (Android) across fifteen distinct areas. It serves as a comprehensive release review, auditing both the App Store Compliance Playbook itself and general app submission readiness.

As an educational repository, this playbook contains guides, checklists, code templates, and static scanner rules. Automated scans run on this repository will flag simulated/educational findings (such as placeholder strings, cross-platform references, and subscription hard-cancel examples) because these patterns must be documented as educational examples to help developers prevent real-world rejections. These findings are classified as educational false-positives.

---

## 1. Permissions

### Compliance Requirements
Platform-specific frameworks require that any application requesting access to sensitive device resources (such as user location, camera, photo library, microphone, calendar, contacts, Bluetooth, health data, or local network) must declare corresponding usage description strings.
- **Apple App Store:** Guideline 5.1.1 (Privacy - Data Collection and Storage) mandates clear, specific, and non-generic purpose strings in the `Info.plist` (such as `NSLocationWhenInUseUsageDescription`, `NSCameraUsageDescription`, etc.). A vague purpose string (e.g., "This app requires camera access to work") is an automatic rejection.
- **Google Play:** Android permissions require strict declarations. Background location, all files access (`MANAGE_EXTERNAL_STORAGE`), accessibility services (`AccessibilityService`), or SMS/call log access must be justified by a core, user-facing feature. Under Google Play policies, unapproved sensitive permissions lead to immediate removal or rejection.

### Audit and Evaluation
- **Playbook Status:** Verified. No native binary permissions are declared for execution because this repository is an educational playbook and template suite.
- **Automated Scan Analysis:** The static compliance scanner checks `agent-os/hooks/app-store-compliance-guard.sh` and `references/rules/privacy.md` for proper verification procedures of `NSLocationWhenInUseUsageDescription` and others. No real permissions are misconfigured.
- **Developer Action:**
  - Verify that every sensitive permission in `Info.plist` or `AndroidManifest.xml` maps directly to a core user-facing feature.
  - Review all custom purpose strings to ensure they name the specific feature using the permission, avoiding generic text.

---

## 2. Privacy Disclosures

### Compliance Requirements
Regulatory updates and store guidelines require prominent disclosure and explicit user consent before data collection, tracking, or sharing.
- **Apple App Store:** Guideline 5.1.2 (Data Use and Sharing) requires the App Tracking Transparency (ATT) framework for cross-app tracking. Nutrition labels on the App Store must match the app's real-world data collection and SDK behaviors.
- **Google Play:** Google's Data Safety form requires detailed mapping of user data collection, transmission, and encryption. Misalignment between static code analysis of third-party SDKs and the declared Data Safety form is a primary rejection trigger.
- **Regulatory Standards (GDPR, California CPRA):** Mandate a clear "Notice at Collection", explicit opt-in for tracking, and the ability to withdraw consent easily without degrading core, non-reliant app features.

### Audit and Evaluation
- **Playbook Status:** Verified.
- **Automated Scan Analysis:** Static analysis checks for `APPLE-5.1.2-MISSING-ATT` and `GOOGLE-DATASAFETY-MISMATCH`. The rules in `data/rejection-patterns.json` correctly document these triggers to prevent developer oversight.
- **Developer Action:**
  - Cross-reference all imported SDKs with platform data safety schemas.
  - Ensure that the ATT prompt is displayed prior to compiling or sending any advertising identifiers (IDFA).

---

## 3. Screenshots

### Compliance Requirements
Screenshots displayed on app store storefronts must represent the product accurately.
- **Apple App Store:** Guideline 2.3.3 (Accurate Metadata) requires that screenshots show the app in actual use. They must not consist solely of splash screens, marketing art, or login screens. For multi-device compatibility, screenshots must match the correct device aspect ratios and must not display simulated device frames that do not correspond to the targeted hardware.
- **Google Play:** Google Play metadata guidelines require high-quality, non-misleading graphics that demonstrate the primary in-app experience. Using ranking claims (e.g., "Number 1 App"), promotional text, or pricing details in screenshots is strictly prohibited.

### Audit and Evaluation
- **Playbook Status:** Verified. No store metadata assets are submitted for this playbook repository.
- **Automated Scan Analysis:** Checked via metadata-audit scripts.
- **Developer Action:**
  - Provide screenshots capturing the primary workflows (e.g., active dashboard, purchase flow, main utility screens).
  - Exclude any promotional text, ranking claims, emojis, or currency symbols from screenshots.

---

## 4. Metadata

### Compliance Requirements
Store metadata is heavily scrutinized by automated review systems and human reviewers.
- **Apple App Store:** Guidelines 2.3.7 (Names and Keywords) and 2.3.10 (No Other Platforms) prohibit names longer than 30 characters, keyword stuffing, and references to alternative platforms (such as mentioning "Android" or "Google Play" in an iOS description).
- **Google Play:** Google Play metadata policy forbids misleading metadata, ALL CAPS formatting, promotional claims, keywords that do not reflect actual features, or emojis/symbols in the application title or description.

### Audit and Evaluation
- **Playbook Status:** Verified.
- **Automated Scan Analysis:** The static scanner flags `APPLE-2.3-CROSS-PLATFORM-REFERENCE` on file paths, CHANGELOG.md, and documentation within this playbook. This is an expected educational false-positive because the playbook must refer to both platforms to explain cross-platform guidelines and remediation steps.
- **Developer Action:**
  - Run the `scripts/metadata-audit.py` utility on the targeted app store metadata directory to detect platform references, character limits, or promotional keywords.
  - Keep the application name under 30 characters and subtitle/short description highly accurate.

---

## 5. Age Rating

### Compliance Requirements
Accurate age rating answers are required to maintain store visibility and comply with children's safety legislation globally.
- **Apple App Store:** Guideline 2.3.6 (Age Rating) requires developers to answer the age rating questionnaire honestly. Apple's updated questionnaire enforces 13+, 16+, and 18+ tiers. Apps with UGC, video-sharing, or generative AI features must trigger mature age gating.
- **Google Play:** The International Age Rating Coalition (IARC) questionnaire must be answered accurately to receive region-specific age ratings.
- **Regional Laws:** US state App Store Accountability Acts (Louisiana, Utah, Texas, Alabama) mandate using the Declared Age Range API (iOS) and Play Age Signals API (Android) to restrict minor access and profiling.

### Audit and Evaluation
- **Playbook Status:** Verified.
- **Automated Scan Analysis:** Static analysis rules (`APPLE-2.3-AGE-RATING-2026`) are documented in `data/rejection-patterns.json` and monitored.
- **Developer Action:**
  - Update the age rating questionnaire in both developer consoles whenever new user-generated content or interactive features are introduced.
  - Implement robust age gating or age-assurance technologies in jurisdictions like Brazil, Australia, Singapore, and the United Kingdom.

---

## 6. AI Disclosures

### Compliance Requirements
Generative AI integrations must comply with strict safety, disclosure, and ethical rules.
- **Apple App Store:** Guidelines 4.7 and 5.1.2(i) require content moderation safeguards for AI-generated content, appropriate age rating, and a clear consent modal naming any third-party AI provider before sharing personal data.
- **Google Play:** Google Play policies require user-facing disclosures and reporting mechanisms for AI-generated text, audio, and images.
- **Regulatory Standards (EU AI Act):** Article 50(1) (in force August 2026) requires a prominent, in-app disclosure notifying EU users that they are interacting with an AI system. Article 50(2) requires machine-readable and visible marking of AI-generated assets.

### Audit and Evaluation
- **Playbook Status:** Verified. No live generative AI is implemented in this codebase.
- **Automated Scan Analysis:** Rules in `data/rejection-patterns.json` monitor AI compliance requirements.
- **Developer Action:**
  - Display an explicit notice at or before the first user interaction with any in-app AI feature.
  - Provide content filtering and reporting features to let users flag objectionable AI-generated content.

---

## 7. Subscription Disclosures

### Compliance Requirements
Subscription monetization models are subjected to rigorous consumer protection audits.
- **Apple App Store:** Guideline 3.1.2 (Subscriptions) requires prominent display of subscription pricing, billing cycles, auto-renewal terms, and links to the Terms of Service (EULA) and Privacy Policy.
- **Google Play:** Google Play Subscription Policy requires transparent pricing, simple cancellation paths, and a prominent disclosure of free-trial transitions.
- **Regulatory Standards (FTC ROSCA & US State Laws):** The Federal Trade Commission's "Click to Cancel" guidelines require that canceling a subscription must be at least as easy as signing up. Requiring phone calls or mail to cancel is a high-severity compliance violation.

### Audit and Evaluation
- **Playbook Status:** Verified.
- **Automated Scan Analysis:** The static compliance guard flags `BOTH-SUBSCRIPTION-HARD-CANCEL` on payments rules. This is an educational false-positive because the playbook payments rule files must cite these patterns to explain negative-option laws and FTC billing compliance.
- **Developer Action:**
  - Implement a direct, self-service cancellation button within the application settings.
  - Present clear subscription disclosures immediately adjacent to the primary purchase call-to-action button.

---

## 8. Payment Compliance

### Compliance Requirements
Monetization of digital goods and services must comply with store payment terms.
- **Apple App Store:** Guideline 3.1.1 (In-App Purchase) requires the StoreKit framework for all digital purchases, upgrades, or virtual currencies. A Restore Purchases function must be visible to users. Third-party gateways (e.g., Stripe, PayPal) are restricted to physical goods or exempt categories.
- **Google Play:** Google Play Billing Policy requires Google Play Billing Library version 8 or later for in-app digital transactions.
- **Alternative Payments:** Regions like South Korea allow alternative payment providers via a South Korea-specific binary, subject to strict reporting and modal sheet disclosures.

### Audit and Evaluation
- **Playbook Status:** Verified.
- **Automated Scan Analysis:** The static compliance scanner reviews correct StoreKit and Play Billing Library usage patterns documented in the rules database.
- **Developer Action:**
  - Verify that the Restore Purchases action is readily accessible on the primary subscription or paywall interface.
  - Restrict the use of external payment SDKs to strictly non-digital, physical goods or services consumed outside the app.

---

## 9. Accessibility

### Compliance Requirements
Continuous accessibility compliance is legally mandated across global jurisdictions.
- **Regulatory Standards (EAA, EN 301 549, WCAG 2.1 AA):** The European Accessibility Act (in force June 2025) requires digital services, including mobile applications, to satisfy WCAG 2.1 AA criteria and publish a formal accessibility statement.
- **Platform Features:**
  - **iOS:** Support for VoiceOver screen readers, Dynamic Type font scaling, Reduce Motion, High Color Contrast, and full Keyboard Navigation.
  - **Android:** Compatibility with TalkBack, Font Scaling, High Contrast, and proper touch target dimensions.

### Audit and Evaluation
- **Playbook Status:** Verified.
- **Automated Scan Analysis:** The static accessibility scanner `scripts/accessibility-audit.py` successfully validates code files against accessibility violations to prevent regression.
- **Developer Action:**
  - Use semantic accessibility labels and traits for all interactive custom UI elements.
  - Verify that layouts scale gracefully under maximum system text size configurations.

---

## 10. Legal Documents

### Compliance Requirements
A compliant app release must carry all legally required organizational and platform declarations.
- **Digital Services Act (DSA):** Apple and Google require DSA Trader Status verification for apps distributed in the European Union (since February 2025).
- **Children's Privacy (COPPA):** Verifiable parental consent and clear retention policies are required if the target audience includes children.
- **Generative AI (EU AI Act):** Team operations must maintain an AI-literacy record under Article 4.
- **Product Safety (EU GPSR):** Consumer product applications must display the manufacturer's postal/electronic contact details and safety warnings on the online interface.

### Audit and Evaluation
- **Playbook Status:** Verified.
- **Automated Scan Analysis:** Handled by regulatory timeline utilities and checklists.
- **Developer Action:**
  - Complete the DSA trader identification form in App Store Connect.
  - Ensure that the developer contact and corporate legal entity details are current on the app storefront listings.

---

## 11. Support URL

### Compliance Requirements
Storefront listings and in-app menus must provide a functional channel for user assistance.
- **Apple App Store:** Guideline 1.5 (Developer Information) and Guideline 2.1 (App Completeness) mandate a valid, reachable, and active Support URL. The destination web page must provide clear contact options (such as an email, phone number, or support form) and must not return a soft-404 error.
- **Google Play:** Developer contact details must include a functional email address and support link.

### Audit and Evaluation
- **Playbook Status:** Verified.
- **Automated Scan Analysis:** The metadata audit tool scans URLs for reachable endpoints when `--check-urls` is activated.
- **Developer Action:**
  - Periodically run a citation and URL verifier (such as `scripts/verify-citations.py`) to confirm that support landing pages remain reachable and alive.

---

## 12. Privacy Policy

### Compliance Requirements
A comprehensive and legally compliant privacy policy is the single most critical legal document for store submissions.
- **Apple App Store:** Guideline 5.1.1(i) requires a privacy policy URL in App Store Connect and linked directly inside the app. It must detail data collection practices, third-party disclosure, data retention policies, and user data deletion instructions.
- **Google Play:** A clear privacy policy must be linked in the Play Console listing and accessible within the app.
- **Regulatory Frameworks (GDPR, CCPA/CPRA):** Policies must explain user rights (access, deletion, correction, opt-out of sharing) and detail secure transmission.

### Audit and Evaluation
- **Playbook Status:** Verified.
- **Automated Scan Analysis:** The static audit monitors for `BOTH-MISSING-PRIVACY-POLICY`. The playbook rules outline the exact content and placement requirements.
- **Developer Action:**
  - Include an active link to the Privacy Policy directly on the initial account creation or login screen and inside the application settings menu.
  - Review policies annually to ensure alignment with active third-party SDKs.

---

## 13. Terms of Service

### Compliance Requirements
Terms of Service (ToS) or End User License Agreements (EULA) govern the legal relationship between the publisher and the end-user.
- **Apple App Store:** Guideline 1.2 (UGC) and Guideline 3.1.2 (Subscriptions) require that apps with user-generated content or subscription monetization provide a binding EULA. Standard EULA rules must specify that the publisher does not tolerate objectionable content or abusive users, and must outline 24-hour removal/ejection procedures.
- **Google Play:** Users must agree to Terms of Service prior to entering binding monetary or user-generated transactions.

### Audit and Evaluation
- **Playbook Status:** Verified.
- **Automated Scan Analysis:** Scanned via automated metadata-audit rules.
- **Developer Action:**
  - For UGC apps, incorporate a mandatory "I Agree to the Terms" checkbox during the onboarding flow.
  - Explicitly include terms outlining the moderation process, reporting options, and immediate suspension rules for violators.

---

## 14. Export Compliance

### Compliance Requirements
Applications utilizing cryptographic technologies must adhere to national and international export controls.
- **Apple App Store:** If an application incorporates cryptography (such as HTTPS, custom encryption protocols, or secure hashing), developers must answer the encryption selection questionnaire and verify export compliance.
- **French ANSSI:** Submission of an encryption declaration to the French National Agency for the Security of Information Systems (ANSSI) is mandatory if the application uses non-exempt cryptography and is distributed within the French territory.

### Audit and Evaluation
- **Playbook Status:** Verified.
- **Automated Scan Analysis:** The rules in `data/rejection-patterns.json` check for the `APPLE-EXPORT-COMPLIANCE-MISSING` pattern to prevent developer oversights.
- **Developer Action:**
  - Declare export compliance parameters properly in `Info.plist` using the `ITSAppUsesNonExemptEncryption` key.
  - Obtain and upload required French ANSSI declarations to App Store Connect if distributing to France.

---

## 15. Encryption Declarations

### Compliance Requirements
Encryption declarations ensure compliance with US and local cryptologic import/export laws.
- **Apple App Store:** Explicit encryption declarations are verified on every app submission. If the application uses standard encryption (e.g., standard HTTPS, SSL, or basic security APIs) for authentication or data transmission, it may qualify for an exemption, but this must be explicitly declared. If it is not exempt, developers must upload a CCATS (Commodity Classification Automated Tracking System) approval from the US Bureau of Industry and Security (BIS).
- **Google Play:** Security declarations require defining data encryption in transit and outlining secure storage paradigms.

### Audit and Evaluation
- **Playbook Status:** Verified. No custom binary code is shipped in this repository, removing any direct export compliance registration burdens.
- **Automated Scan Analysis:** Automated patterns and guidelines references provide instructions for correct encryption declarations.
- **Developer Action:**
  - Set `<key>ITSAppUsesNonExemptEncryption</key><false/>` in `Info.plist` if the application qualifies for standard encryption exemptions (e.g., standard secure web requests).
  - Track changes in encryption APIs to keep store declarations aligned.

---

## Summary of Findings

1. **Both-Placeholder (High-Severity Finding):** Static analysis detected dummy or placeholder strings in rules and examples.
   - *Status:* Classified as an educational false-positive. The files are text templates and playbook rules, which must include educational examples of bad practices to help developers avoid real-world rejections. No placeholders exist in active code.
2. **Both-Subscription-Hard-Cancel (High-Severity Finding):** Scanners identified references to hard cancellation patterns.
   - *Status:* Classified as an educational false-positive. Citing negative-option billing and difficult cancellation methods is necessary within our compliance documentation to educate developers on ROSCA and FTC laws.
3. **Apple-2.3-Cross-Platform-Reference (High-Severity Finding):** Scanners flagged references to Android and Google Play.
   - *Status:* Classified as an educational false-positive. This repository is a cross-platform playbook, and comparing App Store and Google Play rules within the same documentation is necessary.

## Conclusion and Authorization
This release review verifies that the repository and its integrated tools are structurally compliant, highly detailed, and completely safe to ship. All flagged findings are verified educational false-positives. Release is clear for authorization.
