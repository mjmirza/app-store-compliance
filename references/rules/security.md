# Rules. Security and mobile hardening

3 rules in this category. Generated from data/rejection-patterns.json. Each rule names the guideline, the severity, what triggers it, and the fix.

## BOTH-SECURE-STORAGE

- Title. Unencrypted or insecure local storage for sensitive data
- Platform. both
- Guideline or policy. Security
- Severity. critical
- What triggers it. Use of insecure local storage (such as UserDefaults, SharedPreferences, localStorage, or AsyncStorage) to persist credentials, auth tokens, or private keys without encryption.
- How to fix it. Store sensitive credentials exclusively in platform secure storage mechanisms (iOS Keychain, Android Keystore, or EncryptedSharedPreferences).
- Detection signals. UserDefaults, SharedPreferences, localStorage, AsyncStorage, getSharedPreferences
- Present means handled. Keychain, Keystore, SecureStore, KeychainSwift, EncryptedSharedPreferences, keychain-access, flutter_secure_storage

How to detect.

```bash
grep -rn 'UserDefaults\|SharedPreferences\|localStorage\|AsyncStorage' . && ! grep -rn 'Keychain\|Keystore\|SecureStore\|EncryptedSharedPreferences' .
```

## ANDROID-INSECURE-BACKUP

- Title. Insecure backup configuration allows credential extraction
- Platform. google
- Guideline or policy. Security
- Severity. high
- What triggers it. android:allowBackup is set to true in AndroidManifest.xml without any data extraction rules, allowing local app database and token extraction via ADB.
- How to fix it. Set android:allowBackup to false in the AndroidManifest.xml or declare a restrictive backup rules XML configuration.
- Detection signals. allowBackup="true", android:allowBackup="true"
- Present means handled. allowBackup="false", android:allowBackup="false", android:dataExtractionRules, android:fullBackupContent

How to detect.

```bash
grep -rn 'allowBackup="true"' --include='AndroidManifest.xml' . && ! grep -rn 'allowBackup="false"\|dataExtractionRules\|fullBackupContent' --include='AndroidManifest.xml' .
```

## BOTH-UNSAFE-DEEPLINK

- Title. Unsafe deep link intent handling without validation
- Platform. both
- Guideline or policy. Security
- Severity. high
- What triggers it. Custom URL scheme or intent filter registered but actions executed on incoming data without any verification or sanitization.
- How to fix it. Use verified links (Universal Links or App Links) for sensitive entry points, and strictly sanitize all incoming URL query parameters.
- Detection signals. intent-filter, CFBundleURLTypes, URL Schemes
- Present means handled. Associated Domains, assetlinks.json, apple-app-site-association, autoVerify="true"

How to detect.

```bash
grep -rn 'intent-filter\|CFBundleURLTypes\|URL Schemes' . && ! grep -rn 'assetlinks.json\|apple-app-site-association' .
```
