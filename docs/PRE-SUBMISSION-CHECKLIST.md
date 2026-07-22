# Pre Submission Checklist

Treat every unchecked box as a release blocker. Run this before any upload to App Store Connect or the Play Console. Each item is phrased as a verifiable check.

## Shared (both stores)

### Stability and completeness
- [ ] The app launches and runs without a crash on a real device, on the oldest supported OS and the newest.
- [ ] No placeholder text, lorem ipsum, dummy images, or temporary content anywhere in the build.
- [ ] Every link, button, and navigation path works. No dead ends, no broken URLs.
- [ ] The production backend is live and reachable for the entire review window.
- [ ] A working demo account is provided, or a demo mode exists, for any feature behind login.
- [ ] All in app purchases are live, visible, and complete a real transaction in the review build.

### Privacy and data
- [ ] A privacy policy is published, reachable from inside the app, and accurate.
- [ ] Every data collection has user consent before it happens.
- [ ] Every permission has a specific reason string that names the real feature using it.
- [ ] Account creating apps offer in app account deletion.
- [ ] Users can withdraw consent and the app still works for non core features.
- [ ] Every third party SDK and its data behavior is known and declared.

### Mobile Security and Best Practices
For a deep-dive reference across platform best practices, see `docs/MOBILE-SECURITY-2026.md`.
- [ ] **Secure Storage:** Sensitive items (session tokens, passwords, keys) are stored securely (iOS Keychain or Android EncryptedSharedPreferences/Keystore) and never in plaintext files, plain SharedPreferences, or unencrypted local databases.
- [ ] **Biometrics:** Biometric login (FaceID, TouchID, BiometricPrompt) is crypto-backed, requiring biometric validation to unlock a secure cryptographic key rather than just returning a bypassable boolean.
- [ ] **Jailbreak and Root Detection:** Device environment check is implemented locally (and backed by Google Play Integrity on Android) to block or gracefully degrade app features when run on compromised/rooted/jailbroken devices.
- [ ] **Certificate Pinning and SSL:** SSL/TLS cleartext traffic is completely disabled. Public key pinning (SPKI hashes) is implemented on critical endpoints with valid backup pins configured.
- [ ] **Backup Exclusion:** Sensitive private directory files (database files, token preferences) are explicitly excluded from automatic iOS iCloud/iTunes backups and Android ADB/Google Drive backups.
- [ ] **Deep Link and URL Schemes Verification:** Inputs from deep links, Universal Links, and App Links are treated as untrusted, sanitized, and thoroughly validated. Secure Universal Links (iOS) and verified App Links (Android) are used instead of easily hijackable custom schemes.
- [ ] **Secure Auth and Session Flows:** Standard modern flows like OAuth 2.1 or OIDC with PKCE are used without hardcoded client secrets. Session timeouts are enforced, and all local tokens, databases, and caches are thoroughly destroyed on logout or session expiration.

### Metadata and listing
- [ ] The app name, description, and screenshots match what the app actually does.
- [ ] Screenshots show the app in use, not a splash or login screen.
- [ ] No keyword stuffing in the name, subtitle, or description.
- [ ] The age or content rating questionnaire is answered honestly.
- [ ] No references to the other platform or to alternative marketplaces.

### Monetization
- [ ] Digital goods use the official store billing.
- [ ] Subscription terms, renewal, charges, and cancellation are disclosed before purchase.
- [ ] Loot boxes or random rewards disclose odds before purchase.

## Apple specific

- [ ] Notes for Review explains every non obvious feature and every in app purchase.
- [ ] Privacy nutrition labels match the app's real data collection and the SDKs.
- [ ] App Tracking Transparency prompt is implemented before any cross app tracking.
- [ ] Third party social login is paired with an equal privacy preserving alternative such as Sign in with Apple.
- [ ] No private APIs, no deprecated frameworks, current OS support.
- [ ] No downloaded code that changes app features. Server side changes are data, not code.
- [ ] Background modes declared match what the app actually does.
- [ ] The new age rating questionnaire (13 plus, 16 plus, 18 plus) is answered for every app.
- [ ] Any AI feature that can produce sensitive content has an age restriction.
- [ ] Any personal data shared with a third party AI has a consent modal naming the provider and data types.
- [ ] Regulated category apps are submitted under the legal entity and geo restricted where required.
- [ ] App name is 30 characters or fewer.

## Google Play specific

- [ ] The Data Safety form matches the app's real runtime data behavior, including every SDK. This is the top rejection cause.
- [ ] Every sensitive permission has a qualifying core use case and the required declaration.
- [ ] Background location, all files access, SMS, call log, and AccessibilityService each map to a visible core feature, or are removed.
- [ ] The app targets the current required Android API level.
- [ ] For a new personal developer account, the closed test of at least 12 testers over 14 consecutive days is complete.
- [ ] Play Billing is used for in app digital goods.
- [ ] The IARC content rating questionnaire is complete.
- [ ] The listing makes no claim the app cannot deliver.
- [ ] Apps for children follow the Families policy and use only Families certified ad SDKs.

## EU specific (legal layer, if the app reaches EU users)

Passing App Review does not make an app EU-legal. The full hard rules and sources are in docs/EU-REGULATORY-2026.md.

- [ ] DSA trader status is declared and verified in App Store Connect. A missing declaration removes the app from the EU App Store (Apple enforced 17 February 2025).
- [ ] Any AI feature reaching EU users shows an in-app notice that the user is interacting with AI, at or before first interaction (EU AI Act Article 50(1), in force 2 August 2026).
- [ ] AI-generated audio, image, video, or text carries a machine-readable and visible AI-generated marking (Article 50(2) and 50(4)).
- [ ] A short AI-literacy record exists for the team building or operating the AI feature (Article 4, live since 2 February 2025).
- [ ] No prohibited AI practice ships (manipulation, banned emotion inference, biometric categorisation) (Article 5, live since 2 February 2025).
- [ ] Personal data shared with a third-party AI has a consent modal naming the provider and data types, shown before data leaves the device (Apple Guideline 5.1.2(i), 13 November 2025).
- [ ] The app meets EN 301 549 and WCAG 2.1 AA and publishes an accessibility statement (European Accessibility Act, in force 28 June 2025). VoiceOver labels, Dynamic Type, contrast, and Reduce Motion are covered.
- [ ] If the app promotes external offers in the EU, the external-purchase entitlement is declared, every external link calls the disclosure sheet, IAP and external offers are not mixed on one storefront, and reporting is wired (DMA).

## Global specific (USA and other markets, if the app reaches those users)

The full hard rules and sources are in docs/GLOBAL-REGULATORY-2026.md. This is legal, on top of App Review. Several dates are under active litigation, so re-verify each against the cited source.

- [ ] Child-directed or under-13 data. COPPA verifiable parental consent, a separate opt-in for ad or third-party disclosure, a written retention policy and a written security program (general compliance date 22 April 2026).
- [ ] US state App Store Accountability Acts (Utah, Texas, Louisiana, Alabama). the app requests an age category from the store, confirms parental consent for a minor, and re-requests on a major change, wired through the Declared Age Range API.
- [ ] Age rating set to 4-plus, 9-plus, 13-plus, 16-plus, or 18-plus, never Unrated, questionnaire re-answered by 31 January 2026.
- [ ] US storefront external links are allowed with no entitlement and no disclosure sheet, no in-app alternative payment, and the commission question is treated as unsettled.
- [ ] California and US state privacy. a privacy policy, notice at collection, know, delete, correct, "Do Not Sell or Share", "Limit Use of Sensitive PI", and honoring Global Privacy Control.
- [ ] Biometric. written consent before capture, a public retention and destruction schedule, and no sale (Illinois BIPA, Texas CUBI).
- [ ] Health app. the HIPAA gate, else the FTC Health Breach Notification Rule with a 60-day breach notice.
- [ ] 18-plus download gating handled for Brazil, Australia, and Singapore for the Apple block of 24 February 2026.
- [ ] UK Online Safety Act Highly Effective Age Assurance and the Children's-Code defaults for a likely-child service.
- [ ] Australia under-16 age assurance for an age-restricted social media platform.
- [ ] South Korea Korea-only binary with an approved payment provider if alternative billing is used.
- [ ] China MIIT app filing with a local entity, plus PIPL and a Banhao license for a game.

## Platform mechanics gate (both stores, if the item applies)

The full detail with dated sources is in `PLATFORM-MECHANICS-2026.md`. These are current, common, blocking causes the base maps did not carry.

Apple.

- [ ] macOS app distributed outside the Mac App Store is Developer ID signed with the hardened runtime, notarized with `notarytool`, and stapled with `stapler`.
- [ ] Not a thin wrapper (Guideline 4.2) and not a duplicate, clone, or un-differentiated saturated-category app (Guideline 4.3, tightened June 2026).
- [ ] Reader app using the External Link Account Entitlement meets every 3.1.3(a) condition and link rule, and offers no in-app purchase while the entitlement is used.
- [ ] France ANSSI encryption declaration uploaded in App Store Connect if the app uses non-exempt encryption and ships on the French App Store.
- [ ] App Store Connect content-rights question answered, with proof of rights available for any third-party content.
- [ ] visionOS App Motion declared, and watchOS and tvOS built with the platform-26 SDK and Xcode 26 by 28 April 2026.

Android.

- [ ] Developer identity verified before 30 September 2026 if the app is distributed to Brazil, Indonesia, Singapore, or Thailand.
- [ ] Every foreground service declares `foregroundServiceType` in the manifest with the matching permission, and each type is declared in the Play Console with a demo video.
- [ ] No SafetyNet Attestation. attestation uses the Play Integrity API, verified server-side.
- [ ] Play Billing Library at version 8 or later before 31 August 2026, and digital goods route through Play Billing.
- [ ] `targetSdkVersion` at least 35 today, planned for at least 36 by the 2026 deadline.
- [ ] No unexpected launch-time or mid-task full-screen interstitial, and every interstitial is closable by 15 seconds.
- [ ] Health app has the Health Apps Declaration, a core-function justification per Health Connect permission, the migrated Organization Account, and the correct medical-device label or disclaimer.

Cross-cutting.

- [ ] A US-facing UGC app has a documented NCMEC CyberTipline report path on actual knowledge and a 1-year preservation policy.
- [ ] A UGC or social app has a content filter, in-app report and block, published contact, and 24-hour remove-and-eject (Apple 1.2), plus the Google Play Child Safety Standards items for the Social and Dating categories.
- [ ] Account-creating app has both an in-app account-and-data deletion flow and a publicly reachable web deletion URL, declared.
- [ ] Not on the OFAC SDN list, and country availability excludes the embargoed territories.
- [ ] Non-store card payments for real goods implement PSD2 SCA and 3D Secure in the EU or UK, store no card number, and identify the correct PCI SAQ.

## The two checks that prevent the most rejections

Two checks stop the majority of rejections across both stores. A working demo account with a live backend, and a privacy declaration that matches actual runtime behavior including SDKs. If you verify nothing else, verify these two.
