# Rules. Google Play specific

22 rules in this category. Generated from data/rejection-patterns.json. Each rule names the guideline, the severity, what triggers it, and the fix.

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

## GOOGLE-PERM-SMS-CALLLOG

- Title. SMS or Call Log without an approved core use case
- Platform. google
- Guideline or policy. Permissions and APIs
- Severity. critical
- What triggers it. READ_SMS, SEND_SMS, RECEIVE_SMS, READ_CALL_LOG, or WRITE_CALL_LOG declared without an approved use case.
- How to fix it. Use the permissions declaration form for an approved core use case, or drop the permission.
- Detection signals. READ_SMS, SEND_SMS, RECEIVE_SMS, READ_CALL_LOG, WRITE_CALL_LOG

How to detect.

```bash
grep -rnE 'permission.(READ_SMS|SEND_SMS|RECEIVE_SMS|READ_CALL_LOG|WRITE_CALL_LOG)' --include='AndroidManifest.xml' .
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

## GOOGLE-TARGET-API

- Title. App does not target the current required API level
- Platform. google
- Guideline or policy. Target API level
- Severity. high
- What triggers it. targetSdkVersion in build.gradle is below the current Google Play requirement. From 31 August 2026, new apps and updates must target Android 16, API level 36, or higher.
- How to fix it. Build against the current required Android target API level. From 31 August 2026 that is API 36 or higher. Submissions below the threshold are rejected automatically.
- Detection signals. targetSdkVersion, targetSdk

How to detect.

```bash
grep -rnE 'targetSdk(Version)?[ =]+[0-9]+' --include='*.gradle' --include='*.kts' .   # must be 36 or higher from 31 Aug 2026
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

## ANDROID-DYNAMIC-CODE-LOADING

- Title. Dynamic code loading at runtime
- Platform. google
- Guideline or policy. Device and Network Abuse
- Severity. high
- What triggers it. DexClassLoader, PathClassLoader from a downloaded file, or downloading and executing code at runtime.
- How to fix it. Ship all code in the package. Server side changes must be data, not executable code.
- Detection signals. DexClassLoader, PathClassLoader, loadDex, createPackageContext

How to detect.

```bash
grep -rn 'DexClassLoader\|PathClassLoader\|loadDex\|createPackageContext' --include='*.kt' --include='*.java' .
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
