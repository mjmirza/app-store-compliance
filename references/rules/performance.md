# Rules. Performance and completeness

15 rules in this category. Generated from data/rejection-patterns.json. Each rule names the guideline, the severity, what triggers it, and the fix.

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

## BOTH-SDK-SUPPLY-CHAIN

- Title. Third party SDK violates policy on the developer's behalf
- Platform. both
- Guideline or policy. SDK responsibility
- Severity. high
- What triggers it. A bundled SDK requests permissions, tracks users, or behaves in ways the app does not declare. The developer is responsible for SDK behavior.
- How to fix it. Vet every SDK, keep them current, and remove any that collect or share data the app does not declare.

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
