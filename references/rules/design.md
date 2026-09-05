# Rules. Design and login

6 rules in this category. Generated from data/rejection-patterns.json. Each rule names the guideline, the severity, what triggers it, and the fix.

## APPLE-4.0-SIWA-RELAY-DOMAIN

- Title. Sign in with Apple relay addresses on private.icloud.com rejected by email validation
- Platform. apple
- Guideline or policy. 4.0 Design and Sign in with Apple. Hide My Email relay domain change (Apple Developer news 1ptvdtcm, 15 June 2026, corrected 24 August 2026)
- Severity. critical
- What triggers it. The account system, email validation, or allowlist accepts only privaterelay.appleid.com. Apple now issues Hide My Email relay addresses on private.icloud.com as well. Sign-ups with the new domain fail silently and the app is rejected under 4.0 or 4.8 for a broken Sign in with Apple flow.
- How to fix it. Accept both privaterelay.appleid.com and private.icloud.com everywhere email addresses are validated, allowlisted, or matched, server and client.
- Detection signals. privaterelay.appleid.com
- Present means handled. private.icloud.com

How to detect.

```bash
grep -rn 'privaterelay\.appleid\.com' . && ! grep -rqn 'private\.icloud\.com' .
```

## APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED

- Title. CI pipeline calls a removed App Store Connect API age-rating endpoint
- Platform. apple
- Guideline or policy. App Store Connect API 4.3 and 4.4 release notes
- Severity. critical
- What triggers it. The App Store Connect API removed GET /v1/appStoreVersions/{id}/relationships/ageRatingDeclaration and GET /v1/appStoreVersions/{id}/ageRatingDeclaration. A fastlane, script, or CI step that still calls them fails and the release pipeline stops. The replacement is the read age-rating declaration endpoint, which also carries the new socialMedia and socialMediaAgeRestricted attributes.
- How to fix it. Switch to the current age-rating declaration read and update endpoints, and set socialMedia and socialMediaAgeRestricted where the app has social features. Re-run the pipeline against a TestFlight build before the next release.
- Detection signals. appStoreVersions/, /ageRatingDeclaration, relationships/ageRatingDeclaration
- Present means handled. ageRatingDeclarations/

How to detect.

```bash
grep -rn 'appStoreVersions/[^ ]*/ageRatingDeclaration\|relationships/ageRatingDeclaration' --include='*.rb' --include='*.sh' --include='*.py' --include='*.js' --include='*.ts' --include='*.yml' --include='*.yaml' .
```

## APPLE-4.0-SIWA-UX

- Title. Sign in with Apple UX violation
- Platform. apple
- Guideline or policy. 4.0
- Severity. high
- What triggers it. Asking for name or email again after Sign in with Apple already provided them, a non standard SIWA button, hiding SIWA below other social logins, or rejecting a private relay email.
- How to fix it. Use the name and email from the Apple credential, do not re ask, use the standard SIWA button, keep SIWA at least as prominent as other logins, and accept private relay emails. Source. truongduy2611 sign_in_with_apple rule.
- Detection signals. ASAuthorizationAppleIDProvider, SignInWithApple
- Present means handled. ASAuthorizationAppleIDButton, privaterelay.appleid.com

How to detect.

```bash
grep -rn 'ASAuthorizationAppleIDProvider' --include='*.swift' . && grep -rn 'completeProfile\|askForName\|nameTextField\|emailTextField' --include='*.swift' .   # asking for name or email after SIWA is a violation
```

## APPLE-4.2-WEB-WRAPPER

- Title. Thin web wrapper with no added value
- Platform. apple
- Guideline or policy. 4.2
- Severity. high
- What triggers it. The app is mostly a single web view loading a website with little native code.
- How to fix it. Add native capability, offline value, device integration, or content the web version lacks.
- Detection signals. WKWebView loadRequest, single WebView, Capacitor, Cordova

How to detect.

```bash
grep -rn 'WKWebView\|loadRequest\|Capacitor\|Cordova' --include='*.swift' . | wc -l   # a high count with little native code is a thin wrapper
```

## APPLE-4.8-SOCIAL-LOGIN-ONLY

- Title. Third party social login without an equal alternative
- Platform. apple
- Guideline or policy. 4.8
- Severity. high
- What triggers it. Facebook, Google, or similar social login is present without Sign in with Apple or an equal privacy preserving option.
- How to fix it. Add Sign in with Apple or an equal login that limits data to name and email and allows a private email.
- Detection signals. FacebookLogin, GoogleSignIn, GIDSignIn, LoginWithFacebook
- Present means handled. SignInWithApple, ASAuthorizationAppleIDProvider

How to detect.

```bash
grep -rn 'FacebookLogin\|GoogleSignIn\|GIDSignIn' --include='*.swift' . && ! grep -rn 'SignInWithApple\|ASAuthorizationAppleIDProvider' --include='*.swift' .
```

## IONIC-4.2-THIN-WRAPPER

- Title. Thin WebView wrapper with insufficient native functionality
- Platform. apple
- Guideline or policy. 4.2
- Severity. high
- What triggers it. A Capacitor/Cordova/WKWebView marker is present alongside fewer than 2 distinct native-feel plugins (status bar, splash screen, push notifications, haptics, share, camera, local notifications). This is a heuristic proxy for the real Apple 4.2 test (features/content/UI beyond a repackaged website), reviewed manually before treating as a blocker.
- How to fix it. Apple 4.2 Minimum Functionality is the single most common Ionic rejection. Add native Capacitor/Cordova plugins for status bar, splash transition, push, and haptics, or ship as an installable PWA to skip App Review.
- Detection signals. WKWebView, Capacitor, Cordova

How to detect.

```bash
grep -rlE 'WKWebView|loadRequest|Capacitor|Cordova' --include='*.ts' --include='*.js' --include='*.swift' . 2>/dev/null | wc -l   # then count distinct @capacitor/(status-bar|splash-screen|push-notifications|haptics) markers, fewer than 2 is a thin wrapper
```
