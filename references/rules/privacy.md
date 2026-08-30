# Rules. Privacy and data

17 rules in this category. Generated from data/rejection-patterns.json. Each rule names the guideline, the severity, what triggers it, and the fix.

## APPLE-5.1.1-MISSING-PRIVACY-POLICY

- Title. Missing privacy policy
- Platform. apple
- Guideline or policy. 5.1.1(i)
- Severity. critical
- What triggers it. No privacy policy URL in App Store Connect metadata and no in app privacy link reference in the codebase.
- How to fix it. Publish a privacy policy, link it in App Store Connect, and reach it from inside the app.
- Detection signals. privacyPolicy, privacy-policy, PrivacyPolicyURL

How to detect.

```bash
grep -rn 'privacyPolicy\|privacy-policy\|PrivacyPolicy' --include='*.swift' . || echo 'no privacy policy reference found'
```

## APPLE-5.1.1-MISSING-USAGE-DESCRIPTION

- Title. Sensitive framework linked without a usage description
- Platform. apple
- Guideline or policy. 5.1.1(ii)
- Severity. critical
- What triggers it. A sensitive framework or API is referenced in code but the matching NSxUsageDescription key is absent from Info.plist.
- How to fix it. Add the matching usage description key with a specific reason for every sensitive framework used.
- Detection signals. AVCaptureDevice, CLLocationManager, PHPhotoLibrary, CNContactStore, HKHealthStore

How to detect.

```bash
for k in NSCameraUsageDescription NSLocationWhenInUseUsageDescription NSPhotoLibraryUsageDescription NSContactsUsageDescription NSMicrophoneUsageDescription; do echo "$k"; plutil -extract "$k" raw */Info.plist 2>/dev/null || echo '  MISSING or empty'; done
```

## APPLE-5.1.1-NO-ACCOUNT-DELETION

- Title. Account creation without in app account deletion
- Platform. apple
- Guideline or policy. 5.1.1(v)
- Severity. critical
- What triggers it. Account creation or sign up code present but no delete account flow found.
- How to fix it. Add an in app account deletion flow for any app that supports account creation.
- Detection signals. signUp, createAccount, register
- Present means handled. deleteAccount, delete_account, account deletion

How to detect.

```bash
grep -rn 'createAccount\|signUp\|register' --include='*.swift' . && ! grep -rn 'deleteAccount\|delete_account\|account deletion' --include='*.swift' .
```

## APPLE-PRIVACY-MANIFEST-MISSING

- Title. Required reason APIs or third party SDKs without a privacy manifest
- Platform. apple
- Guideline or policy. Privacy Manifest
- Severity. critical
- What triggers it. Required reason API usage or a commonly used third party SDK is present but no PrivacyInfo.xcprivacy is bundled, or an SDK lacks its signed manifest. Enforced by Apple at upload since 2024.
- How to fix it. Add a PrivacyInfo.xcprivacy with NSPrivacyAccessedAPITypes and approved reason codes, list NSPrivacyTrackingDomains, and confirm every third party SDK ships its signed manifest.
- Detection signals. NSFileManager, UserDefaults, systemUptime, ProcessInfo, Firebase, Alamofire
- Present means handled. PrivacyInfo.xcprivacy, NSPrivacyAccessedAPITypes

How to detect.

```bash
find . -name 'PrivacyInfo.xcprivacy' | grep -q . || echo 'MISSING PrivacyInfo.xcprivacy'; find . -path '*/*.framework/*' -name 'PrivacyInfo.xcprivacy'   # each bundled SDK should ship one
```

## FLUTTER-PRIVACY-MANIFEST-MISSING

- Title. Flutter plugin touches required-reason APIs with no PrivacyInfo.xcprivacy
- Platform. apple
- Guideline or policy. 5.1.1
- Severity. critical
- What triggers it. pubspec.yaml present, a plugin known to touch required-reason APIs (permission_handler, image_picker, geolocator, device_info_plus, package_info_plus, shared_preferences, sqflite, firebase_*) is a dependency, and no PrivacyInfo.xcprivacy exists anywhere in the project.
- How to fix it. Add an app-level PrivacyInfo.xcprivacy and confirm each Flutter plugin ships its own (Flutter 3.19+ plugins mostly do). A missing plugin-level manifest is invisible to Apple unless the app manifest also declares that plugin reason code.
- Detection signals. pubspec.yaml, permission_handler, image_picker, firebase_

How to detect.

```bash
grep -q 'permission_handler\|image_picker\|geolocator\|firebase_' pubspec.yaml 2>/dev/null && ! find . -name 'PrivacyInfo.xcprivacy' | grep -q .
```

## GOOGLE-MISSING-PRIVACY-POLICY

- Title. Missing privacy policy
- Platform. google
- Guideline or policy. User Data
- Severity. critical
- What triggers it. No privacy policy URL set in the Play Console store listing while the app collects user data.
- How to fix it. Publish a privacy policy and set its URL in the Play Console store listing.
- Detection signals. privacyPolicy, privacy-policy

How to detect.

```bash
grep -rn 'privacyPolicy\|privacy-policy' . || echo 'set a privacy policy URL in the Play listing'
```

## RN-PRIVACY-MANIFEST-MISSING

- Title. React Native native module touches required-reason APIs with no PrivacyInfo.xcprivacy
- Platform. apple
- Guideline or policy. 5.1.1
- Severity. critical
- What triggers it. package.json depends on react-native or expo, native modules with required-reason API usage are present (Firebase, AsyncStorage, expo-file-system), and no PrivacyInfo.xcprivacy exists.
- How to fix it. Add an app-level PrivacyInfo.xcprivacy. Native modules bundled transitively via JS deps each need their own manifest aggregated in the final IPA.
- Detection signals. @react-native-firebase, AsyncStorage, expo-file-system

How to detect.

```bash
grep -qE '"react-native"|"expo"' package.json 2>/dev/null && grep -rn 'Firebase\|AsyncStorage\|expo-file-system' --include='*.ts' --include='*.tsx' . 2>/dev/null && ! find . -name 'PrivacyInfo.xcprivacy' | grep -q .
```

## WEB-COOKIE-CONSENT

- Title. Setting non-essential cookies without prior cookie consent
- Platform. web
- Guideline or policy. ePrivacy Directive
- Severity. critical
- What triggers it. Writing to document.cookie or cookieStore without checking if the user accepted cookies via a cookie consent banner.
- How to fix it. Implement a compliant Cookie Consent banner that blocks non-essential cookies until the user gives explicit consent.
- Detection signals. document.cookie, setCookie, cookieStore, js-cookie, cookieConsent
- Present means handled. cookieBanner, cookieConsentBanner, acceptCookies, cookiePreferences

How to detect.

```bash
grep -rn 'document.cookie\|setCookie\|cookieStore\|js-cookie\|cookieConsent' --include='*.js' --include='*.ts' --include='*.html' . && ! grep -rn 'cookieBanner\|cookieConsentBanner\|acceptCookies\|cookiePreferences' .
```

## ANDROID-ACCOUNT-DELETION-URL

- Title. Account creation without in app deletion and a data deletion URL
- Platform. google
- Guideline or policy. User Data
- Severity. high
- What triggers it. Account creation present but no in app delete path and no web data deletion URL.
- How to fix it. Provide in app account deletion and set a public data deletion URL in the Play Console listing.
- Detection signals. signUp, createAccount, register
- Present means handled. deleteAccount, delete_account, account deletion

How to detect.

```bash
grep -rn 'createAccount\|signUp\|register' --include='*.kt' --include='*.java' . && ! grep -rn 'deleteAccount\|delete_account' .   # also set a data deletion URL in the Play listing
```

## APPLE-5.1.1-UNNECESSARY-DATA

- Title. Requiring personal data not relevant to core functionality
- Platform. apple
- Guideline or policy. 5.1.1
- Severity. high
- What triggers it. A registration or onboarding form requires phone number, gender, marital status, date of birth, or home address when it is not essential to the core feature. Relevance is contextual.
- How to fix it. Make non essential personal fields optional. Require only data directly relevant to the core feature. Source. truongduy2611 unnecessary_data rule.
- Detection signals. phone, gender, marital, date of birth, birthdate, address

How to detect.

```bash
grep -rni 'phone\|gender\|marital\|date.of.birth\|birthdate\|address' --include='*.swift' . | grep -i 'required\|validator\|isRequired'
```

## APPLE-5.1.1-VAGUE-PURPOSE-STRING

- Title. Generic or empty permission purpose string
- Platform. apple
- Guideline or policy. 5.1.1(ii)
- Severity. high
- What triggers it. An NSxUsageDescription key in Info.plist is empty or carries a generic value such as needs access or required.
- How to fix it. Write a specific purpose string naming the real feature that uses each permission.
- Detection signals. NSCameraUsageDescription, NSLocationWhenInUseUsageDescription, NSPhotoLibraryUsageDescription, NSMicrophoneUsageDescription, NSContactsUsageDescription

How to detect.

```bash
for k in NSCameraUsageDescription NSLocationWhenInUseUsageDescription NSPhotoLibraryUsageDescription NSContactsUsageDescription; do v=$(plutil -extract "$k" raw */Info.plist 2>/dev/null); echo "$k = $v"; done   # flag empty or generic values like 'required'
```

## APPLE-5.1.2-AI-NO-CONSENT-MODAL

- Title. Personal data shared with third party AI without consent modal
- Platform. apple
- Guideline or policy. 5.1.2(i)
- Severity. high
- What triggers it. A third party AI or LLM SDK is present and personal data may be sent without a consent modal naming the provider.
- How to fix it. Show a consent modal naming the AI provider and data types before any personal data leaves the app.
- Detection signals. OpenAI, anthropic, gemini, completion, chat/completions
- Present means handled. consent, data sharing modal

How to detect.

```bash
grep -rni 'api.openai.com\|anthropic\|generativelanguage\|chat/completions' . && ! grep -rni 'consent' .
```

## APPLE-5.1.2-MISSING-ATT

- Title. Tracking SDK without App Tracking Transparency
- Platform. apple
- Guideline or policy. 5.1.2(i)
- Severity. high
- What triggers it. A tracking or advertising SDK is present but ATTrackingManager request is not called and NSUserTrackingUsageDescription is absent.
- How to fix it. Call the ATT prompt before any cross app tracking and add the tracking usage description.
- Detection signals. AppsFlyer, Adjust, Branch, FacebookSDK, IDFA, ASIdentifierManager
- Present means handled. ATTrackingManager, NSUserTrackingUsageDescription

How to detect.

```bash
grep -rn 'AppsFlyer\|Adjust\|FBSDK\|advertisingIdentifier\|ASIdentifierManager' --include='*.swift' . && ! grep -rn 'ATTrackingManager\|NSUserTrackingUsageDescription' .
```

## APPLE-ACCOUNT-DELETION-WEAK

- Title. Account deletion is a mailto or deactivate only flow
- Platform. apple
- Guideline or policy. 5.1.1(v)
- Severity. high
- What triggers it. The only account removal path is a mailto link, a web form the user must leave the app to reach, or a deactivate that does not delete.
- How to fix it. Provide genuine in app deletion of the account and its data, not a deactivate or an external form.
- Detection signals. mailto:, deactivate, contact us to delete

How to detect.

```bash
grep -rn 'deleteAccount\|delete account' --include='*.swift' . && grep -rn 'mailto:\|deactivate' --include='*.swift' .   # deletion must truly delete, not mailto or deactivate
```

## APPLE-PRIVACY-NUTRITION-LABELS

- Title. Missing Privacy Nutrition Labels data type declarations
- Platform. apple
- Guideline or policy. 5.1.1
- Severity. high
- What triggers it. Collecting sensitive user data (e.g. email, phone, name, coordinates) but missing the privacyNutritionLabels declaration or proper nutrition disclosure references.
- How to fix it. Update the app privacy manifest (PrivacyInfo.xcprivacy) with NSPrivacyCollectedDataTypes and complete corresponding Nutrition Labels in App Store Connect.
- Detection signals. email, phoneNumber, userName, location, coordinates
- Present means handled. NSPrivacyCollectedDataTypes, privacyNutritionLabels, privacy-nutrition-labels

How to detect.

```bash
grep -rn 'email\|phoneNumber\|userName\|location\|coordinates' --include='*.swift' . && ! grep -rn 'NSPrivacyCollectedDataTypes\|privacyNutritionLabels\|privacy-nutrition-labels' .
```

## BOTH-FINGERPRINTING

- Title. Device fingerprinting to track users
- Platform. both
- Guideline or policy. Apple 5.1.2, Google Device and Network Abuse
- Severity. high
- What triggers it. Building a persistent device fingerprint from hardware or settings to identify users. Apple bans this regardless of ATT consent.
- How to fix it. Do not fingerprint. Use the platform advertising identifier with consent where tracking is genuinely needed.
- Detection signals. fingerprint, deviceFingerprint, canvas fingerprint, identifierForVendor cross app

How to detect.

```bash
grep -rni 'fingerprint\|deviceFingerprint\|canvas fingerprint' .
```

## IONIC-PRIVACY-MANIFEST-MISSING

- Title. Capacitor/Cordova plugin wrapping a native SDK with no PrivacyInfo.xcprivacy
- Platform. apple
- Guideline or policy. 5.1.1
- Severity. high
- What triggers it. Capacitor/Cordova plugins are present and no PrivacyInfo.xcprivacy exists anywhere in the project.
- How to fix it. Capacitor plugin manifest support is less standardized than Flutter's. Verify each plugin wrapping a native SDK (camera, geolocation, ads) ships PrivacyInfo.xcprivacy, and add the app-level one.
- Detection signals. @capacitor/, Capacitor.

How to detect.

```bash
grep -rq '@capacitor/\|Capacitor\.' --include='*.ts' . 2>/dev/null && ! find . -name 'PrivacyInfo.xcprivacy' | grep -q .
```
