# Rules. Google Play specific

34 rules in this category. Generated from data/rejection-patterns.json. Each rule names the guideline, the severity, what triggers it, and the fix.

## ANDROID-HEALTH-PERMISSIONS

- Title. Health or fitness data access without Health Connect declaration
- Platform. google
- Guideline or policy. Permissions and APIs
- Severity. critical
- What triggers it. Accessing Health Connect client or querying health permissions (e.g. steps, heart rate) without proper declaration or dedicated health privacy policy.
- How to fix it. Declare Health Connect permissions, complete the console Health Connect form, and maintain a dedicated health privacy policy.
- Detection signals. HealthConnectClient, com.google.android.gms.permission.HealthConnect, READ_STEPS, READ_HEART_RATE
- Present means handled. healthConnectConsent, healthPrivacyPolicy, Health Connect

How to detect.

```bash
grep -rn 'HealthConnectClient\|com.google.android.gms.permission.HealthConnect\|READ_STEPS\|READ_HEART_RATE' --include='*.kt' --include='*.java' --include='AndroidManifest.xml' . && ! grep -rn 'healthConnectConsent\|healthPrivacyPolicy\|Health Connect' .
```

## ANDROID-USER-DATA-DISCLOSURE

- Title. Missing prominent disclosure for sensitive user data
- Platform. google
- Guideline or policy. User Data
- Severity. critical
- What triggers it. Collecting personal user data (e.g. contacts, SMS, device accounts, files) without a prominent disclosure and explicit user consent block.
- How to fix it. Provide a prominent in-app disclosure before collecting sensitive personal data, and obtain explicit user consent.
- Detection signals. contacts, SMS, device accounts, files, personalData
- Present means handled. prominent disclosure, user consent, privacy consent, accept policy

How to detect.

```bash
grep -rn 'contacts\|SMS\|device accounts\|files\|personalData' --include='*.kt' --include='*.java' --include='*.xml' . && ! grep -rn 'prominent disclosure\|user consent\|privacy consent\|accept policy' .
```

## GOOGLE-DATASAFETY-MISMATCH

- Title. Data Safety form does not match runtime behavior
- Platform. google
- Guideline or policy. Data Safety
- Severity. critical
- What triggers it. Analytics, ads, or tracking SDKs are present that collect or share data not declared in the Data Safety section. This is the number one Google rejection cause.
- How to fix it. Audit every SDK and runtime data flow and declare every collection, sharing, and security practice accurately in the Data Safety form.
- Detection signals. firebase-analytics, com.google.android.gms.ads, facebook, appsflyer, adjust

How to detect.

```bash
grep -rn 'firebase-analytics\|com.google.android.gms.ads\|appsflyer\|adjust\|com.facebook' --include='*.gradle' --include='*.kts' .   # every SDK that collects or shares data must be declared in Data Safety
```

## GOOGLE-FAMILIES-AD-SDK

- Title. Non compliant ad SDK in a child targeted app
- Platform. google
- Guideline or policy. Families
- Severity. critical
- What triggers it. An app declared for children uses an ad SDK that is not Families certified, or shows behavioral ads to minors.
- How to fix it. Use only Families certified ad SDKs and remove behavioral advertising to minors.
- Detection signals. children, Designed for Families, kids

How to detect.

```bash
grep -rn 'com.google.android.gms.ads\|applovin\|unity.*ads\|ironsource' --include='*.gradle' . && grep -rni 'children\|families\|kids' --include='AndroidManifest.xml' .
```

## GOOGLE-PERM-ACCESSIBILITY-MISUSE

- Title. AccessibilityService used for non accessibility purposes
- Platform. google
- Guideline or policy. Permissions and APIs
- Severity. critical
- What triggers it. BIND_ACCESSIBILITY_SERVICE declared in an app that is not an accessibility tool.
- How to fix it. Use accessibility APIs only for genuine accessibility features and declare the use, or remove the service.
- Detection signals. BIND_ACCESSIBILITY_SERVICE, AccessibilityService

How to detect.

```bash
grep -rn 'BIND_ACCESSIBILITY_SERVICE\|AccessibilityService' --include='AndroidManifest.xml' --include='*.kt' --include='*.java' .
```

## GOOGLE-PERM-ALL-FILES

- Title. All files access without a qualifying use case
- Platform. google
- Guideline or policy. Permissions and APIs
- Severity. critical
- What triggers it. MANAGE_EXTERNAL_STORAGE declared in AndroidManifest.
- How to fix it. Use scoped storage. Request all files access only for a qualifying use case with the required declaration.
- Detection signals. MANAGE_EXTERNAL_STORAGE

How to detect.

```bash
grep -rn 'MANAGE_EXTERNAL_STORAGE' --include='AndroidManifest.xml' .
```

## GOOGLE-PERM-BACKGROUND-LOCATION

- Title. Background location without a qualifying core feature
- Platform. google
- Guideline or policy. Permissions and APIs
- Severity. critical
- What triggers it. ACCESS_BACKGROUND_LOCATION declared in AndroidManifest with no clear core feature or prominent disclosure.
- How to fix it. Use foreground location where possible, or justify background use with a core feature and a prominent disclosure and the permission declaration.
- Detection signals. ACCESS_BACKGROUND_LOCATION

How to detect.

```bash
grep -rn 'ACCESS_BACKGROUND_LOCATION' --include='AndroidManifest.xml' .
```

## GOOGLE-PERM-SMS-CALLLOG

- Title. SMS or Call Log without an approved core use case
- Platform. google
- Guideline or policy. Permissions and APIs
- Severity. critical
- What triggers it. READ_SMS, SEND_SMS, RECEIVE_SMS, READ_CALL_LOG, or WRITE_CALL_LOG declared without an approved use case. From 26 August 2026 account verification via phone call is no longer a permitted use case for READ_CALL_LOG. Use the Digital Credentials API or the SMS Retriever API instead.
- How to fix it. Use the permissions declaration form for an approved core use case, or drop the permission.
- Detection signals. READ_SMS, SEND_SMS, RECEIVE_SMS, READ_CALL_LOG, WRITE_CALL_LOG

How to detect.

```bash
grep -rnE 'permission.(READ_SMS|SEND_SMS|RECEIVE_SMS|READ_CALL_LOG|WRITE_CALL_LOG)' --include='AndroidManifest.xml' .
```

## GOOGLE-PLAY-AGE-SIGNALS-MISUSE

- Title. Misuse of Play Age Signals API
- Platform. google
- Guideline or policy. User Data
- Severity. critical
- What triggers it. Usage of the Play Age Signals API (com.google.android.play:age-signals) in conjunction with advertising, marketing, user profiling, or analytics libraries, which violates Google Play's strict Terms of Service.
- How to fix it. Ensure that information from the Play Age Signals API is solely used to provide age-appropriate content and experiences in compliance with laws. Do not use the API or its returned signals for advertising, marketing, user profiling, or analytics.
- Detection signals. com.google.android.play:age-signals, AgeSignalsManager, AgeSignalsRequest

How to detect.

```bash
grep -rn 'com.google.android.play:age-signals\|AgeSignalsManager\|AgeSignalsRequest' --include='*.gradle' --include='*.kts' --include='*.kt' --include='*.java' .   # if present, confirm age signals are never passed to ad, marketing, profiling, or analytics SDKs
```

## GOOGLE-ORG-REGISTRATION-REQUIRED

- Title. Regulated-category app published from a personal developer account
- Platform. google
- Guideline or policy. Play Console requirements. organization account for regulated categories (Play Console Help answers 10788890 and 17125096)
- Severity. critical
- What triggers it. From 30 September 2026 financial products and services (banking, loans, trading, investment funds, crypto wallets and exchanges), health apps (medical, human subjects research), apps approved to use VpnService, and government apps must be published from an organization account with a D-U-N-S number consistent with the Dun and Bradstreet profile. Detection is heuristic on VpnService, Health Connect, and finance signals.
- How to fix it. Convert or create an organization developer account, obtain a D-U-N-S number, keep the account details identical to the Dun and Bradstreet profile, and transfer the app through the official Transfer ownership workflow before 30 September 2026.
- Detection signals. VpnService, HealthConnect, health.connect, BankAccount, loan, cryptocurrency, wallet

How to detect.

```bash
grep -rn 'VpnService\|HealthConnect\|health\.connect\|BankAccount\|cryptocurrency' {A} .   # then verify the Play Console account type is Organization with a D-U-N-S number
```

## GOOGLE-PLAY-APP-REGISTRATION-MISSING

- Title. Play app package name not registered for developer verification
- Platform. google
- Guideline or policy. Android developer verification, Play leg (Play Console Help answers 17125096 and 17134731)
- Severity. critical
- What triggers it. Every Play app package name must be registered in Play Console for Android developer verification by 30 September 2026. This leg is global. Unregistered apps risk global removal from Google Play. Detection is manual in Play Console. Development-build package names that are never distributed do not need registration.
- How to fix it. Open Play Console, complete developer verification, register every distributed package name, and re-check after adding a new applicationId or product flavor.
- Detection signals. applicationId

How to detect.

```bash
grep -rhoE 'applicationId[[:space:]=]+"[^"]+"' --include='*.gradle' --include='*.kts' .   # then confirm each distributed package name is registered in Play Console developer verification
```

## GOOGLE-GENAI-NCII-CONTROLS

- Title. Generative image or video app without NCII safeguards and a full-access test account
- Platform. google
- Guideline or policy. Generative AI policy enforcement, non-consensual intimate content (Android Developers Blog, 25 August 2026)
- Severity. critical
- What triggers it. Apps that generate or edit images or video of people must integrate customized input and output moderation, document the safety prompts and edge cases tested, and give the reviewer a test account with full unpaywalled access to every AI feature. Suspended apps are blocked from monetization and advertising across Google platforms.
- How to fix it. Add input and output moderation for intimate and deepfake content, keep a written test record of safety prompts and edge cases, and provide a full-access test account in the Play Console review notes.
- Detection signals. generateImage, imageGeneration, text-to-image, faceSwap, face swap, undress, stable-diffusion
- Present means handled. moderation, safetyClassifier, contentFilter

How to detect.

```bash
grep -rqn 'generateImage\|imageGeneration\|text-to-image\|faceSwap\|stable-diffusion' --include='*.kt' --include='*.java' --include='*.xml' --include='*.gradle' --include='*.kts' --include='*.dart' --include='*.ts' . && ! grep -rqi 'moderation\|safetyClassifier\|contentFilter' .
```

## GOOGLE-ANON-CHAT-MINOR-BLOCK

- Title. Random or anonymous chat app without minor blocking and child-safety standards
- Platform. google
- Guideline or policy. Age-Restricted Content, Families, and Child Safety Standards policies (Play Console Help answers 17036597, 17122218, 14747720, effective 26 August 2026)
- Severity. critical
- What triggers it. Apps whose core function is randomly connecting users to strangers, or anonymous communication with hidden identities, must use Play Console functionality to block minors, may not target children, and are in scope of the Child Safety Standards policy (published CSAE standards, in-app reporting, CSAM removal, child-safety contact).
- How to fix it. Enable the Play Console minor-blocking tools, set the age rating and target audience to exclude children, publish CSAE standards, add in-app reporting, and designate a child-safety contact.
- Detection signals. random chat, anonymous chat, chat with strangers, Omegle, stranger
- Present means handled. ageGate, minorBlock, csae

How to detect.

```bash
grep -rqi 'random chat\|anonymous chat\|chat with strangers\|Omegle' . && ! grep -rqi 'ageGate\|minorBlock\|csae' .
```

## ANDROID-ADVERTISING-ID

- Title. Google Play Advertising ID usage without disclosure or opt-out
- Platform. google
- Guideline or policy. User Data
- Severity. high
- What triggers it. Using com.google.android.gms.permission.AD_ID permission or querying GAID but lacking opt-out support or user deletion pathways in code/privacy policy.
- How to fix it. Declare the AD_ID permission in AndroidManifest.xml and handle user opt-out or deletion requests in full compliance with Google Play policy.
- Detection signals. com.google.android.gms.permission.AD_ID, AD_ID, getAdvertisingIdInfo
- Present means handled. opt-out, reset AD_ID, advertisingIdConsent, delete AD_ID

How to detect.

```bash
grep -rn 'com.google.android.gms.permission.AD_ID\|AD_ID\|getAdvertisingIdInfo' --include='AndroidManifest.xml' --include='*.kt' --include='*.java' . && ! grep -rn 'opt-out\|reset AD_ID\|advertisingIdConsent\|delete AD_ID' .
```

## ANDROID-DYNAMIC-CODE-LOADING

- Title. Dynamic code loading at runtime
- Platform. google
- Guideline or policy. Device and Network Abuse
- Severity. high
- What triggers it. DexClassLoader, PathClassLoader from a downloaded file, or downloading and executing code at runtime. For apps targeting API 37, every native library loaded with System.load() must be read-only or the system throws UnsatisfiedLinkError.
- How to fix it. Ship all code in the package. Server side changes must be data, not executable code.
- Detection signals. DexClassLoader, PathClassLoader, loadDex, createPackageContext

How to detect.

```bash
grep -rn 'DexClassLoader\|PathClassLoader\|loadDex\|createPackageContext' --include='*.kt' --include='*.java' .
```

## ANDROID-INSECURE-BACKUP

- Title. Android backup is enabled without filtering sensitive data
- Platform. google
- Guideline or policy. Device and Network Abuse
- Severity. high
- What triggers it. android:allowBackup is set to true in AndroidManifest.xml without setting data extraction rules to exclude credentials/databases.
- How to fix it. Disable backups with allowBackup="false", or configure dataExtractionRules / fullBackupContent to exclude sensitive credentials and SQLite databases.
- Detection signals. allowBackup="true"
- Present means handled. dataExtractionRules, fullBackupContent, allowBackup="false"

How to detect.

```bash
grep -rn 'allowBackup="true"' . && ! grep -rn 'dataExtractionRules\|fullBackupContent\|allowBackup="false"' .
```

## ANDROID-OVERLAY-TAPJACKING

- Title. System overlay permission, a tapjacking and malware signal
- Platform. google
- Guideline or policy. Permissions and APIs
- Severity. high
- What triggers it. SYSTEM_ALERT_WINDOW or application overlay declared, especially combined with AccessibilityService.
- How to fix it. Remove overlay abuse. The overlay plus accessibility combination is a strong malware signal Google enforces against.
- Detection signals. SYSTEM_ALERT_WINDOW, TYPE_APPLICATION_OVERLAY

How to detect.

```bash
grep -rn 'SYSTEM_ALERT_WINDOW\|TYPE_APPLICATION_OVERLAY' --include='AndroidManifest.xml' --include='*.kt' --include='*.java' .
```

## ANDROID-QUERY-ALL-PACKAGES

- Title. QUERY_ALL_PACKAGES without a permitted use case
- Platform. google
- Guideline or policy. Package visibility
- Severity. high
- What triggers it. QUERY_ALL_PACKAGES declared in AndroidManifest.
- How to fix it. Declare specific packages with a queries element, or qualify for a permitted use case.
- Detection signals. QUERY_ALL_PACKAGES

How to detect.

```bash
grep -rn 'QUERY_ALL_PACKAGES' --include='AndroidManifest.xml' .
```

## ANDROID-RUNTIME-PERMISSIONS

- Title. Sensitive runtime permissions requested without validation
- Platform. google
- Guideline or policy. Permissions and APIs
- Severity. high
- What triggers it. Requesting critical permissions (camera, contacts, storage) without dynamic checks or explicit explanation/rationale to the user.
- How to fix it. Check permissions dynamically at runtime, show a clear rationale if denied, and handle denials gracefully.
- Detection signals. requestPermissions, checkSelfPermission, shouldShowRequestPermissionRationale
- Present means handled. permission explanation, showPermissionRationale, explainPermission

How to detect.

```bash
grep -rn 'requestPermissions\|checkSelfPermission\|shouldShowRequestPermissionRationale' --include='*.kt' --include='*.java' . && ! grep -rn 'permission explanation\|showPermissionRationale\|explainPermission' .
```

## GOOGLE-12-TESTER-RULE

- Title. New personal account without the closed test
- Platform. google
- Guideline or policy. Closed testing requirement
- Severity. high
- What triggers it. Manual check. New personal developer accounts need at least 12 testers for 14 consecutive days of closed testing before production.
- How to fix it. Run the closed test with at least 12 testers over 14 consecutive days, or use an organization account where appropriate.

## GOOGLE-MISLEADING-LISTING

- Title. Listing claims a feature the app lacks
- Platform. google
- Guideline or policy. Store Listing and Promotion
- Severity. high
- What triggers it. Manual check. The store listing, screenshots, and description must match the app's actual functionality.
- How to fix it. Make the listing match the build exactly, with screenshots of real in app screens.

## GOOGLE-TARGET-API

- Title. App does not target the current required API level
- Platform. google
- Guideline or policy. Target API level
- Severity. high
- What triggers it. targetSdkVersion in build.gradle is below the current Google Play requirement. From 31 August 2026, new apps and updates must target Android 16, API level 36, or higher. A Play Console extension to 1 November 2026 is available. Wear OS and Automotive OS must target API 35 or higher, TV and XR API 34 or higher.
- How to fix it. Build against the current required Android target API level. From 31 August 2026 that is API 36 or higher. Submissions below the threshold are rejected automatically.
- Detection signals. targetSdkVersion, targetSdk

How to detect.

```bash
grep -rnE 'targetSdk(Version)?[ =]+[0-9]+' --include='*.gradle' --include='*.kts' .   # must be 36 or higher from 31 Aug 2026
```

## GOOGLE-PAYMENTS-DONATION-LINK

- Title. In-app donation link to a payment page outside Play billing
- Platform. google
- Guideline or policy. Payments policy (support.google.com/googleplay/android-developer/answer/9992660). Donations outside Play billing are permitted only as tax-exempt donations
- Severity. high
- What triggers it. An in-app link or button routes to Open Collective, Ko-fi, Patreon, Buy Me a Coffee, GitHub Sponsors, Liberapay, or a PayPal donate page. Google enforces the Payments policy exception literally. only donations to a tax-exempt charity (a 501(c)(3)-class body, not a 501(c)(6) trade association or an unincorporated project) may bypass Play billing. Everything else is treated as a digital-goods payment. Open-source apps are the most common casualty (AnkiDroid, August 2026, Hacker News 921 points).
- How to fix it. Either remove the donation entry point from the Play build (a build flavor is enough), route it through Play billing as a one-time product, or, if the recipient is a tax-exempt charity, keep proof of that status in the review notes. Do not argue the case in the appeal, Google has already stated 501(c)(6) does not qualify.
- Detection signals. opencollective.com, ko-fi.com, patreon.com, buymeacoffee.com, github.com/sponsors, liberapay.com, paypal.com/donate, Donate
- Present means handled. BillingClient, com.android.billingclient, 501(c)(3)

How to detect.

```bash
grep -rn 'opencollective.com\|ko-fi.com\|patreon.com\|buymeacoffee.com\|github.com/sponsors\|liberapay.com\|paypal.com/donate' --include='*.kt' --include='*.java' --include='*.xml' --include='*.dart' --include='*.ts' --include='*.tsx' --include='*.js' .
```

## GOOGLE-CONTACTS-PICKER-REQUIRED

- Title. READ_CONTACTS requested where the Contact Picker is sufficient
- Platform. google
- Guideline or policy. Contacts Permissions policy for apps targeting Android 17, API level 37 (Play Console Help answer 16909972)
- Severity. high
- What triggers it. Apps targeting API 37 or later may only request READ_CONTACTS when the Android Contact Picker is not sufficient for core functionality, and must complete the Play Console declaration. Enforcement 27 January 2027, pre-review checks from 27 October 2026.
- How to fix it. Replace READ_CONTACTS with the Contact Picker for one-off selection. Keep the permission only for a genuine core use (a dialer, a contacts manager) and file the declaration.
- Detection signals. READ_CONTACTS, targetSdk 37, targetSdkVersion 37
- Present means handled. ContactsContract.Intents.Insert, ACTION_PICK, ContactPicker

How to detect.

```bash
grep -rqn 'READ_CONTACTS' --include='*.kt' --include='*.java' --include='*.xml' --include='*.gradle' --include='*.kts' . && grep -rqE 'targetSdk(Version)?[[:space:]=]+3[7-9]' --include='*.gradle' --include='*.kts' . && ! grep -rqn 'ACTION_PICK\|ContactPicker' --include='*.kt' --include='*.java' --include='*.xml' --include='*.gradle' --include='*.kts' .
```

## GOOGLE-LOCATION-BUTTON-SCOPE

- Title. Location requested without the Android location button scope
- Platform. google
- Guideline or policy. Location Permissions policy for apps targeting API 37 (Play Console Help answer 16909972)
- Severity. high
- What triggers it. Apps targeting API 37 or later must implement the Android location button using the onlyForLocationButton permission flag in the manifest when location is only needed at a user-triggered moment. A blanket ACCESS_FINE_LOCATION request for a tap-to-locate feature is a policy violation from 27 January 2027.
- How to fix it. Scope one-shot location use to the location button with the onlyForLocationButton flag and keep the broad permission only for continuous features that justify it.
- Detection signals. ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, targetSdk 37
- Present means handled. onlyForLocationButton

How to detect.

```bash
grep -rqn 'ACCESS_FINE_LOCATION\|ACCESS_COARSE_LOCATION' --include='*.kt' --include='*.java' --include='*.xml' --include='*.gradle' --include='*.kts' . && grep -rqE 'targetSdk(Version)?[[:space:]=]+3[7-9]' --include='*.gradle' --include='*.kts' . && ! grep -rqn 'onlyForLocationButton' --include='*.kt' --include='*.java' --include='*.xml' --include='*.gradle' --include='*.kts' .
```

## GOOGLE-FGS-GEOFENCE-REMOVED

- Title. Foreground service used for geofencing
- Platform. google
- Guideline or policy. Foreground service requirements for apps targeting API 37 (Play Console Help answer 16965181)
- Severity. high
- What triggers it. Geofencing is removed as an approved foreground service use case for apps targeting API 37. An app declaring FOREGROUND_SERVICE_LOCATION whose only location use is geofencing is rejected from 27 January 2027.
- How to fix it. Move to the Geofence API (GeofencingClient) and drop FOREGROUND_SERVICE_LOCATION if geofencing was its only use.
- Detection signals. FOREGROUND_SERVICE_LOCATION, geofence, Geofence
- Present means handled. GeofencingClient, addGeofences

How to detect.

```bash
grep -rqn 'FOREGROUND_SERVICE_LOCATION' --include='*.kt' --include='*.java' --include='*.xml' --include='*.gradle' --include='*.kts' . && grep -rqi 'geofenc' --include='*.kt' --include='*.java' --include='*.xml' --include='*.gradle' --include='*.kts' .
```

## ANDROID-LOCAL-NETWORK-PERMISSION

- Title. Local network access without the ACCESS_LOCAL_NETWORK runtime permission
- Platform. google
- Guideline or policy. Android 17 behavior changes for apps targeting API 37 (developer.android.com/about/versions/17/behavior-changes-17)
- Severity. high
- What triggers it. From Android 17 enforcement is mandatory for apps targeting API 37 or later. mDNS, NSD discovery, multicast, and direct LAN connections fail with a security exception unless the app declares and requests ACCESS_LOCAL_NETWORK.
- How to fix it. Declare android.permission.ACCESS_LOCAL_NETWORK, request it at runtime before any LAN discovery or connection, and degrade gracefully when denied.
- Detection signals. NsdManager, MulticastSocket, _tcp.local, mDNS, 192.168.
- Present means handled. ACCESS_LOCAL_NETWORK

How to detect.

```bash
grep -rqn 'NsdManager\|MulticastSocket\|_tcp\.local\|mDNS' {A} . && ! grep -rqn 'ACCESS_LOCAL_NETWORK' {A} .
```

## ANDROID-R8-OPTIMIZATION-MISSING

- Title. Release build not optimized, shrunk, or obfuscated
- Platform. google
- Guideline or policy. Play Console technical quality requirements, DEX optimization (Play Console Help answer 17492799)
- Severity. high
- What triggers it. From February 2027 apps must be optimized with a minimum of 25 percent coverage across optimization, shrinking, and obfuscation using a tool such as R8. A release build with minifyEnabled false, or with no minifyEnabled at all, falls below the bar and loses visibility and publishing capabilities.
- How to fix it. Enable R8 in the release build type (isMinifyEnabled = true, isShrinkResources = true), fix keep rules, and verify the Play Console optimization report before February 2027.
- Detection signals. minifyEnabled false, isMinifyEnabled = false
- Present means handled. minifyEnabled true, isMinifyEnabled = true

How to detect.

```bash
! grep -rqE '(isMinifyEnabled|minifyEnabled)[[:space:]=]+true' --include='*.gradle' --include='*.kts' .
```

## GOOGLE-UNRATED-APP-BANNED

- Title. App published or updated with no content rating
- Platform. google
- Guideline or policy. Content Ratings policy clarification (Play Console Help answer 17134731, 26 August 2026)
- Severity. high
- What triggers it. Google clarified that unrated apps are not allowed on Google Play. An incomplete or expired IARC content rating questionnaire blocks publishing. Detection is manual in Play Console.
- How to fix it. Complete the content rating questionnaire for every app and re-answer it when features change (chat, UGC, gambling, AI generation).
- Detection signals. contentRating

How to detect.

```bash
echo 'manual. open Play Console, App content, Content rating, and confirm the questionnaire is complete and current'
```

## ANDROID-ACCESSIBILITY-FONTSCALING

- Title. Font scaling disabled due to dp text sizing
- Platform. google
- Guideline or policy. User Experience - Accessibility
- Severity. medium
- What triggers it. Hardcoded text sizes specified in dp instead of sp in Android XML layouts or Jetpack Compose files.
- How to fix it. Always define text sizes in sp (scale-independent pixels) rather than dp to allow the system font scaling to work correctly.
- Detection signals. textSize, dp

How to detect.

```bash
python3 scripts/accessibility-audit.py . --rule ANDROID-ACCESSIBILITY-FONTSCALING
```

## ANDROID-ACCESSIBILITY-HIGHCONTRAST

- Title. Hardcoded colors ignoring high contrast settings
- Platform. google
- Guideline or policy. User Experience - Accessibility
- Severity. medium
- What triggers it. Hardcoded hex color strings in layout files or hardcoded Color objects in Compose without using theme attributes.
- How to fix it. Reference semantic colors or color resources so the app automatically respects high contrast themes.
- Detection signals. color, textColor, Color(0xFF

How to detect.

```bash
python3 scripts/accessibility-audit.py . --rule ANDROID-ACCESSIBILITY-HIGHCONTRAST
```

## ANDROID-ACCESSIBILITY-SCANNER

- Title. Touch target sizes below 48dp
- Platform. google
- Guideline or policy. User Experience - Accessibility
- Severity. medium
- What triggers it. Clickable items or buttons defined with layout_width, layout_height, or padding that results in touch targets smaller than 48dp.
- How to fix it. Ensure all interactive elements have a minimum touch target area of 48dp x 48dp by using padding, minWidth, and minHeight.
- Detection signals. clickable, onClick, 48dp, 48.dp

How to detect.

```bash
python3 scripts/accessibility-audit.py . --rule ANDROID-ACCESSIBILITY-SCANNER
```

## ANDROID-ACCESSIBILITY-TALKBACK

- Title. TalkBack support missing or disabled
- Platform. google
- Guideline or policy. User Experience - Accessibility
- Severity. medium
- What triggers it. Views or graphic components missing contentDescription or setting importantForAccessibility inappropriately.
- How to fix it. Provide meaningful contentDescription values for all informative images and interactive views, and ensure importantForAccessibility is set correctly.
- Detection signals. contentDescription, importantForAccessibility

How to detect.

```bash
python3 scripts/accessibility-audit.py . --rule ANDROID-ACCESSIBILITY-TALKBACK
```

## GOOGLE-PLAY-CHARGEBACK-LIABILITY

- Title. Play billing without chargeback dispute handling (developer now bears the cost)
- Platform. google
- Guideline or policy. Play Console. Updates to refund protection and chargeback cost responsibility (support.google.com/googleplay/android-developer/answer/17068375)
- Severity. medium
- What triggers it. For orders placed after 3 August 2026 Google Play no longer absorbs chargebacks. the developer bears the purchase price less the service fee plus the card-network chargeback fee (typically USD 15 to 25 per dispute). An app uses Play billing but never handles the PendingRefundReviewNotification real-time developer notification or calls the Review Refund API, so every fraudulent dispute is lost by default. Not a rejection cause, a revenue-and-fraud exposure that lands on the developer's account.
- How to fix it. Subscribe to real-time developer notifications, handle PendingRefundReviewNotification, and call the Review Refund API within 24 hours with the refund preference and purchase-usage evidence so Google Play can contest illegitimate chargebacks. Reconcile chargeback fees in your revenue model.
- Detection signals. BillingClient, com.android.billingclient, purchases.subscriptions, purchases.products
- Present means handled. PendingRefundReviewNotification, ReviewRefund, reviewrefund, pendingRefundReviewNotification

How to detect.

```bash
grep -rq 'BillingClient\|com.android.billingclient' --include='*.kt' --include='*.java' --include='*.gradle' --include='*.kts' . && ! grep -rqi 'PendingRefundReviewNotification\|reviewrefund' .
```
