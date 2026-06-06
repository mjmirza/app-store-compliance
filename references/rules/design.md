# Rules. Design and login

3 rules in this category. Generated from data/rejection-patterns.json. Each rule names the guideline, the severity, what triggers it, and the fix.

## APPLE-4.8-SOCIAL-LOGIN-ONLY

- Title. Third party social login without an equal alternative
- Platform. apple
- Guideline or policy. 4.8
- Severity. high
- What triggers it. Facebook, Google, or similar social login is present without Sign in with Apple or an equal privacy preserving option.
- How to fix it. Add Sign in with Apple or an equal login that limits data to name and email and allows a private email.
- Detection signals. FacebookLogin, GoogleSignIn, GIDSignIn, LoginWithFacebook
- Present means handled. SignInWithApple, ASAuthorizationAppleIDProvider

## APPLE-4.2-WEB-WRAPPER

- Title. Thin web wrapper with no added value
- Platform. apple
- Guideline or policy. 4.2
- Severity. high
- What triggers it. The app is mostly a single web view loading a website with little native code.
- How to fix it. Add native capability, offline value, device integration, or content the web version lacks.
- Detection signals. WKWebView loadRequest, single WebView, Capacitor, Cordova

## APPLE-4.0-SIWA-UX

- Title. Sign in with Apple UX violation
- Platform. apple
- Guideline or policy. 4.0
- Severity. high
- What triggers it. Asking for name or email again after Sign in with Apple already provided them, a non standard SIWA button, hiding SIWA below other social logins, or rejecting a private relay email.
- How to fix it. Use the name and email from the Apple credential, do not re ask, use the standard SIWA button, keep SIWA at least as prominent as other logins, and accept private relay emails. Source. truongduy2611 sign_in_with_apple rule.
- Detection signals. ASAuthorizationAppleIDProvider, SignInWithApple
- Present means handled. ASAuthorizationAppleIDButton, privaterelay.appleid.com
