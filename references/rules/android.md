# Rules. Google Play specific

12 rules in this category. Generated from data/rejection-patterns.json. Each rule names the guideline, the severity, what triggers it, and the fix.

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
