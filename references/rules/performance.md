# Rules. Performance and completeness

28 rules in this category. Generated from data/rejection-patterns.json. Each rule names the guideline, the severity, what triggers it, and the fix.

## APPLE-2.1-CLOUD-NOT-IN-PRODUCTION

- Title. iCloud or CloudKit schema not deployed to production
- Platform. apple
- Guideline or policy. 2.1
- Severity. critical
- What triggers it. The app uses CloudKit or iCloud but the schema and containers are only in the development environment, so the feature fails for the reviewer on the production build.
- How to fix it. Deploy the CloudKit schema and containers to production before submitting. Source. lukylab checklist.
- Detection signals. CKContainer, CloudKit, NSUbiquitousKeyValueStore, iCloud

How to detect.

```bash
grep -rn 'CKContainer\|CloudKit\|NSUbiquitousKeyValueStore' --include='*.swift' .   # then confirm the CloudKit schema is deployed to production in the CloudKit console
```

## APPLE-2.1-MISSING-DEMO-ACCOUNT

- Title. Account based app without demo credentials
- Platform. apple
- Guideline or policy. 2.1
- Severity. critical
- What triggers it. Login or auth code present (SignInWithApple, OAuth, Auth, login view) but no demo account note found in review metadata or fastlane review_information.
- How to fix it. Add a working demo account and a live test path to the Notes for Review field before submission.
- Detection signals. LoginView, signIn, AuthService, OAuth, Firebase Auth

How to detect.

```bash
grep -rn 'signIn\|LoginView\|OAuth\|FirebaseAuth' --include='*.swift' .   # then confirm a demo account is in the review notes
```

## APPLE-2.1-STAGING-BACKEND

- Title. Backend points at staging or localhost
- Platform. apple
- Guideline or policy. 2.1
- Severity. critical
- What triggers it. API base URL in the release config contains localhost, 127.0.0.1, staging, dev, or ngrok.
- How to fix it. Point the release build at the live production backend and confirm it stays up during review.
- Detection signals. localhost, 127.0.0.1, staging., dev., ngrok, http://

How to detect.

```bash
grep -rn 'localhost\|127.0.0.1\|staging\.\|ngrok\|http://' --include='*.swift' --include='*.plist' . | grep -v https
```

## IONIC-UIWEBVIEW-DEPRECATED

- Title. Deprecated UIWebView symbol statically linked
- Platform. apple
- Guideline or policy. 2.5.1
- Severity. critical
- What triggers it. The literal UIWebView symbol appears anywhere in the built sources, often pulled in transitively by a stale Capacitor or Cordova plugin.
- How to fix it. Apple auto-rejects (ITMS-90809) any binary statically linking UIWebView. Update every plugin to a WKWebView-based version.
- Detection signals. UIWebView

How to detect.

```bash
grep -rn 'UIWebView' --include='*.swift' --include='*.m' . 2>/dev/null
```

## WEB-GDPR-COMPLIANCE

- Title. Processing web personal data without GDPR compliance controls
- Platform. web
- Guideline or policy. GDPR
- Severity. critical
- What triggers it. Collecting or processing personal web data without explicit opt-in controls, privacy policy links, or right to be forgotten (delete) options.
- How to fix it. Integrate standard GDPR compliance gates including explicit opt-in for data processing and a mechanism for data deletion.
- Detection signals. processData, personalData, submitForm, registerWeb, webForm
- Present means handled. GDPR, opt-in, privacyConsent, deletePersonalData, exportData

How to detect.

```bash
grep -rn 'processData\|personalData\|submitForm\|registerWeb\|webForm' --include='*.js' --include='*.ts' --include='*.html' . && ! grep -rn 'GDPR\|opt-in\|privacyConsent\|deletePersonalData\|exportData' .
```

## BOTH-US-ASAA-COMPLIANCE-MISSING

- Title. Missing US State App Store Accountability Act age assurance and parental consent controls
- Platform. both
- Guideline or policy. US State ASAA (Utah SB 142 / Texas SB 2420 / Louisiana HB 570)
- Severity. critical
- What triggers it. Failing to integrate Declared Age Range API or Play Age Signals API and missing parental consent validation for minor users in applicable US states.
- How to fix it. Integrate native age signal APIs (Declared Age Range on iOS, Play Age Signals API on Android), enforce verifiable parental consent for minor accounts, and purge raw age verification data immediately.
- Detection signals. ageCategory, minorUser, parentalConsent, DeclaredAgeRange, com.google.android.play:age-signals
- Present means handled. verifyParentalConsent, deleteAgeVerificationData, handleAgeCategorySignal, rescindConsent

How to detect.

```bash
grep -rni 'DeclaredAgeRange\|age-signals\|parentalConsent\|RESCIND_CONSENT' --include='*.swift' --include='*.kt' --include='*.java' . || echo '  MISSING: No state ASAA age assurance or parental consent signals found'
```

## US-COPPA-AMENDED-RULE-MISSING

- Title. Non-compliance with Amended COPPA Rule requirements
- Platform. both
- Guideline or policy. COPPA 16 CFR Part 312
- Severity. critical
- What triggers it. Collecting childrens data or biometric identifiers without separate opt-in consent for third-party disclosure/targeted ads, or lacking written retention and information security policies.
- How to fix it. Implement separate opt-in consent for third-party sharing/advertising, establish written data retention policies, maintain a written security program, and update verifiable parental consent flows.
- Detection signals. biometricIdentifier, childData, kidProfile, coppaConsent
- Present means handled. separateThirdPartyConsent, coppaWrittenRetentionPolicy, coppaInfoSecurityProgram, verifiableParentalConsent

How to detect.

```bash
grep -rni 'coppaWrittenRetentionPolicy\|coppaInfoSecurityProgram\|separateThirdPartyConsent' --include='*.swift' --include='*.kt' --include='*.md' . || echo '  MISSING: No amended COPPA retention policy or separate consent handles found'
```

## EU-AI-ACT-ART-50-TRANSPARENCY-MISSING

- Title. Missing AI interaction disclosure or synthetic content marking
- Platform. both
- Guideline or policy. EU AI Act Article 50
- Severity. critical
- What triggers it. Providing AI chatbots or generating synthetic text/media without immediate AI-interaction disclosures or machine-readable synthetic content watermarks.
- How to fix it. Display immediate in-app disclosures informing users they are interacting with AI, inject machine-readable provenance watermarks (e.g., C2PA) into synthetic media, and disclose artificial manipulation.
- Detection signals. chatCompletion, generateImage, syntheticMedia, aiChat
- Present means handled. aiInteractionNotice, c2paWatermark, syntheticContentMarker, deepfakeDisclosure

How to detect.

```bash
grep -rni 'aiInteractionNotice\|c2paWatermark\|syntheticContentMarker' --include='*.swift' --include='*.kt' --include='*.js' --include='*.ts' . || echo '  MISSING: No AI Act Article 50 transparency disclosure or C2PA watermarking found'
```

## APPLE-2.1-DEBUG-FEATURES

- Title. Debug or test features shipped in the production build
- Platform. apple
- Guideline or policy. 2.1
- Severity. high
- What triggers it. Debug menus, test logins, or developer backdoors left visible in the release build rather than gated behind a debug only flag.
- How to fix it. Hide debug and test features behind a debug only compile flag so they never ship in production. Source. lukylab checklist.
- Detection signals. debug menu, debugMenu, test login, skip login, bypass auth, DEBUG_BYPASS

How to detect.

```bash
grep -rni 'debug menu\|debugMenu\|skip login\|bypass auth\|DEBUG_BYPASS' --include='*.swift' .
```

## APPLE-2.1-PLACEHOLDER-CONTENT

- Title. Placeholder content in the build
- Platform. apple
- Guideline or policy. 2.1
- Severity. high
- What triggers it. Strings such as lorem ipsum, TODO, FIXME, placeholder, dummy, test data, example.com found in shipped resources.
- How to fix it. Replace all placeholder text and assets with real content before submission.
- Detection signals. lorem ipsum, placeholder, TODO, FIXME, dummy, example.com

How to detect.

```bash
grep -rni 'lorem ipsum\|placeholder\|TODO\|FIXME\|example.com' --include='*.swift' --include='*.strings' .
```

## APPLE-2.1-REVIEW-NOTES-INCOMPLETE

- Title. Review notes missing a required section for a new submission
- Platform. apple
- Guideline or policy. 2.1
- Severity. high
- What triggers it. New submission review notes omit one of the six sections. Screen recording on a physical device, app purpose, access instructions and test credentials, external services list, regional differences, and regulated industry documentation.
- How to fix it. Fill all six review notes sections using templates/REVIEW-NOTES-TEMPLATE.md. Source. truongduy2611 review_notes rules.

How to detect.

```bash
use templates/REVIEW-NOTES-TEMPLATE.md and fill all six sections
```

## APPLE-2.5.1-PRIVATE-API

- Title. Private API or deprecated framework use
- Platform. apple
- Guideline or policy. 2.5.1
- Severity. high
- What triggers it. References to known private API selectors or deprecated frameworks found in the binary or code.
- How to fix it. Use only documented public APIs and current frameworks.
- Detection signals. respondsToSelector private, UIWebView, performSelector hidden

How to detect.

```bash
grep -rn 'UIWebView\|performSelector\|valueForKey' --include='*.swift' --include='*.m' .   # review any reflection or deprecated framework use
```

## BOTH-E-EVIDENCE-COMPLIANCE-MISSING

- Title. Missing legal representative or emergency data-production response procedures for the EU e-Evidence Package
- Platform. both
- Guideline or policy. Regulation (EU) 2023/1543 & Directive (EU) 2023/1544 (EU e-Evidence Package)
- Severity. high
- What triggers it. Apps/services processing user data in the EU that fail to designate a legal representative or lack internal procedures to respond to European Production/Preservation Orders within 10 days (or 8 hours for emergencies).
- How to fix it. Designate an establishment or appoint a legal representative in the EU, notify contact details by August 18, 2026, and establish internal protocols to deliver user data securely within 8 hours in emergency situations.
- Detection signals. e-Evidence, European Production Order, European Preservation Order, emergency data production, law enforcement request, legal representative

How to detect.

```bash
grep -rniE 'e-evidence|european production order|european preservation order|emergency data production' . 2>/dev/null
```

## BOTH-SDK-SUPPLY-CHAIN

- Title. Third party SDK violates policy on the developer's behalf
- Platform. both
- Guideline or policy. SDK responsibility
- Severity. high
- What triggers it. A bundled SDK requests permissions, tracks users, or behaves in ways the app does not declare. The developer is responsible for SDK behavior.
- How to fix it. Vet every SDK, keep them current, and remove any that collect or share data the app does not declare.

## BOTH-SECURE-STORAGE

- Title. Sensitive tokens or credentials stored in insecure unencrypted formats
- Platform. both
- Guideline or policy. Data Security
- Severity. high
- What triggers it. Sensitive session credentials or tokens are saved directly to unencrypted plist, UserDefaults, or SharedPreferences instead of Keychain or Android Keystore / EncryptedSharedPreferences.
- How to fix it. Store all sensitive data and access tokens in iOS Keychain or Android EncryptedSharedPreferences.
- Detection signals. UserDefaults.standard.set, getSharedPreferences

How to detect.

```bash
grep -rn 'UserDefaults.standard.set\|getSharedPreferences' . | grep -i 'token\|password\|credential\|secret\|jwt' && ! grep -rn 'Keychain\|SecItemAdd\|SecItemUpdate\|EncryptedSharedPreferences\|KeyStore\|SQLCipher' .   # matches guard.sh: fires only when a sensitive keyword is present AND a secure-storage API is absent
```

## BOTH-UNSAFE-DEEPLINK

- Title. Unsafe or unvalidated custom deep link URL schemes used for sensitive operations
- Platform. both
- Guideline or policy. Data Security
- Severity. high
- What triggers it. Relying on custom URL schemes for sensitive routing, navigation, or passing tokens, without strict input validation.
- How to fix it. Use Universal Links (iOS) and App Links (Android) for secure domain-validated link routing, and sanitize all deep link parameters.
- Detection signals. CFBundleURLSchemes, android:scheme
- Present means handled. apple-app-site-association, assetlinks.json

How to detect.

```bash
grep -rn 'CFBundleURLSchemes\|android:scheme' . && ! grep -rn 'apple-app-site-association\|assetlinks.json' .
```

## RN-OTA-UNDECLARED

- Title. Undisclosed over-the-air JS bundle updater
- Platform. apple
- Guideline or policy. 3.3.2
- Severity. high
- What triggers it. package.json depends on react-native or expo, and an OTA updater (react-native-code-push, expo-updates, react-native-ota-hot-update, Stallion) is present with no App Review disclosure of bug-fix-only scope.
- How to fix it. Name the OTA mechanism in App Review notes and restrict it to bug fixes that do not change purpose, UI, or features beyond what was reviewed (Apple 3.3.2, 2.5.2).
- Detection signals. react-native-code-push, CodePush., expo-updates, Stallion

How to detect.

```bash
grep -rn 'react-native-code-push\|CodePush\.\|expo-updates' --include='*.ts' --include='*.tsx' --include='*.js' . 2>/dev/null
```

## WEB-INDEXEDDB

- Title. Structured personal data stored in IndexedDB without security controls
- Platform. web
- Guideline or policy. GDPR
- Severity. high
- What triggers it. Storing user records in IndexedDB without user consent, encryption, or proper deletion lifecycles.
- How to fix it. Use encrypted IndexedDB wrappers for structured sensitive records, check user consent, and clear databases upon logout.
- Detection signals. indexedDB.open, indexedDB, createObjectStore
- Present means handled. encryptDatabase, deleteDatabase, consentIndexedDB

How to detect.

```bash
grep -rn 'indexedDB.open\|indexedDB\|createObjectStore' --include='*.js' --include='*.ts' --include='*.html' . && ! grep -rn 'encryptDatabase\|deleteDatabase\|consentIndexedDB' .
```

## WEB-LOCAL-STORAGE

- Title. Unencrypted sensitive personal data stored in localStorage
- Platform. web
- Guideline or policy. GDPR
- Severity. high
- What triggers it. Storing sensitive details or JWT tokens in plain text in localStorage without encryption or user consent check.
- How to fix it. Avoid storing plain sensitive personal info in localStorage, encrypt any stored tokens, and respect storage preferences.
- Detection signals. localStorage.setItem, localStorage
- Present means handled. encryptedStorage, encryptToken, consentLocalStorage, clearLocalStorage

How to detect.

```bash
grep -rn 'localStorage.setItem\|localStorage' --include='*.js' --include='*.ts' --include='*.html' . && ! grep -rn 'encryptedStorage\|encryptToken\|consentLocalStorage\|clearLocalStorage' .
```

## WEB-SESSION-STORAGE

- Title. Sensitive session details stored in sessionStorage without protection
- Platform. web
- Guideline or policy. GDPR
- Severity. high
- What triggers it. Storing raw authentication or session keys in sessionStorage without encryption or clean-up logic.
- How to fix it. Limit and secure the data written to sessionStorage, apply encryption, and ensure data is deleted at session end.
- Detection signals. sessionStorage.setItem, sessionStorage
- Present means handled. encryptedSession, clearSessionStorage

How to detect.

```bash
grep -rn 'sessionStorage.setItem\|sessionStorage' --include='*.js' --include='*.ts' --include='*.html' . && ! grep -rn 'encryptedSession\|clearSessionStorage' .
```

## WEB-TRACKING-TECHNOLOGIES

- Title. Third-party tracking technologies loaded without consent
- Platform. web
- Guideline or policy. GDPR
- Severity. high
- What triggers it. Integrating analytic pixels or tracking scripts (Google Analytics, Facebook Pixel, Hotjar) without consent validation.
- How to fix it. Load third-party tracking scripts and pixels conditionally only after receiving explicit user cookie consent.
- Detection signals. gtag, fbq, google-analytics, trackingPixel, analytics.js, hotjar
- Present means handled. consentTracking, disableTracking, optOutTracking, trackingPreferences

How to detect.

```bash
grep -rn 'gtag\|fbq\|google-analytics\|trackingPixel\|analytics.js\|hotjar' --include='*.js' --include='*.ts' --include='*.html' . && ! grep -rn 'consentTracking\|disableTracking\|optOutTracking\|trackingPreferences' .
```

## EU-AI-ACT-ART-4-LITERACY-MISSING

- Title. Missing AI Literacy Policy and training induction logs for AI system operations
- Platform. both
- Guideline or policy. EU AI Act Article 4
- Severity. high
- What triggers it. Operating or deploying AI models or AI features without maintaining an active AI Literacy Policy, team induction records, and training logs.
- How to fix it. Maintain a written AI Literacy Policy, conduct regular AI safety and privacy inductions, and keep an up-to-date AI literacy training log.
- Detection signals. openai, anthropic, llm, generativeAI, aiAssistant
- Present means handled. aiLiteracyPolicy, AI_LITERACY_LOG, aiTrainingCompleted, aiLiteracyRecord

How to detect.

```bash
grep -rni 'aiLiteracyPolicy\|AI_LITERACY_LOG' --include='*.md' --include='*.swift' --include='*.py' . || echo '  MISSING: No AI literacy policy or training log file found'
```

## APPLE-ACCESSIBILITY-COLORCONTRAST

- Title. Color Contrast and system settings ignored
- Platform. apple
- Guideline or policy. Design - Accessibility
- Severity. medium
- What triggers it. Hardcoded custom colors used without supporting dark/light mode, high-contrast settings, or checking isDarkerSystemColorsEnabled.
- How to fix it. Use dynamic or system colors that automatically adapt, or monitor isDarkerSystemColorsEnabled to adjust contrast dynamically.
- Detection signals. isDarkerSystemColorsEnabled, darkerSystemColors

How to detect.

```bash
python3 scripts/accessibility-audit.py . --rule APPLE-ACCESSIBILITY-COLORCONTRAST
```

## APPLE-ACCESSIBILITY-DYNAMICTYPE

- Title. Dynamic Type support missing or overridden
- Platform. apple
- Guideline or policy. Design - Accessibility
- Severity. medium
- What triggers it. Hardcoded font sizes or styles used without matching scaling or preferredFont APIs, or adjustsFontForContentSizeCategory set to false.
- How to fix it. Use preferredFont(forTextStyle:) in UIKit and system/relative font styles in SwiftUI, ensuring adjustsFontForContentSizeCategory is enabled.
- Detection signals. UIFont.systemFont, preferredFont, adjustsFontForContentSizeCategory

How to detect.

```bash
python3 scripts/accessibility-audit.py . --rule APPLE-ACCESSIBILITY-DYNAMICTYPE
```

## APPLE-ACCESSIBILITY-HAPTICS

- Title. Haptics tactile feedback missing on interactions
- Platform. apple
- Guideline or policy. Design - Accessibility
- Severity. medium
- What triggers it. Interactive elements, buttons, or custom controls lacking feedback generators or CoreHaptics calls.
- How to fix it. Add haptic feedback to buttons, toggles, and swipe actions using UIImpactFeedbackGenerator or selection feedback.
- Detection signals. UIImpactFeedbackGenerator, UINotificationFeedbackGenerator, UISelectionFeedbackGenerator, CHHapticEngine

How to detect.

```bash
python3 scripts/accessibility-audit.py . --rule APPLE-ACCESSIBILITY-HAPTICS
```

## APPLE-ACCESSIBILITY-KEYBOARD

- Title. Keyboard navigation and focus state support missing
- Platform. apple
- Guideline or policy. Design - Accessibility
- Severity. medium
- What triggers it. Custom text editors or complex navigation flows missing keyCommands, focusState, or focusable modifiers.
- How to fix it. Support physical keyboard navigation by utilizing keyCommands in UIKit or focusable() and @FocusState in SwiftUI.
- Detection signals. keyCommands, UIKeyCommand, FocusState, focusable

How to detect.

```bash
python3 scripts/accessibility-audit.py . --rule APPLE-ACCESSIBILITY-KEYBOARD
```

## APPLE-ACCESSIBILITY-REDUCEMOTION

- Title. Reduce Motion accessibility setting ignored
- Platform. apple
- Guideline or policy. Design - Accessibility
- Severity. medium
- What triggers it. Custom animations or transitions without checks for UIAccessibility.isReduceMotionEnabled or environment accessibilityReduceMotion.
- How to fix it. Check the Reduce Motion system status and disable or simplify non-essential animations when requested by the user.
- Detection signals. isReduceMotionEnabled, accessibilityReduceMotion

How to detect.

```bash
python3 scripts/accessibility-audit.py . --rule APPLE-ACCESSIBILITY-REDUCEMOTION
```

## APPLE-ACCESSIBILITY-VOICEOVER

- Title. VoiceOver support missing or incomplete
- Platform. apple
- Guideline or policy. Design - Accessibility
- Severity. medium
- What triggers it. Interactive views or images without accessibilityLabel, accessibilityIdentifier, isAccessibilityElement, or accessibilityElement(children:) properties.
- How to fix it. Ensure all interactive components and decorative or informative images have correct accessibility labels, hints, and traits assigned.
- Detection signals. UIAccessibility, accessibilityLabel, accessibilityIdentifier, isAccessibilityElement

How to detect.

```bash
python3 scripts/accessibility-audit.py . --rule APPLE-ACCESSIBILITY-VOICEOVER
```
