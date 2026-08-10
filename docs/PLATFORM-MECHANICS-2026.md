# Platform Mechanics Hard Rules (2026). Apple and Android

This document covers the platform-mechanics and newer-policy gaps that sit alongside the legal layer ([EU-REGULATORY-2026.md](EU-REGULATORY-2026.md), [GLOBAL-REGULATORY-2026.md](GLOBAL-REGULATORY-2026.md)) and the base rejection maps. These are current, common, and blocking causes that the base playbook did not carry. Every item is dated and sourced. Several dates and versions move, so re-verify against the cited source before relying on a figure. Items that could not be confirmed against a primary source are labelled unverified in the last section.

## 1. Apple platform mechanics

### 1.1 macOS notarization for distribution outside the Mac App Store (HARD)

An app distributed with a Developer ID (not through the Mac App Store) must be notarized or Gatekeeper blocks it. The four steps. build with every executable and dylib signed. sign with a Developer ID certificate plus a secure timestamp and the hardened runtime. submit with `xcrun notarytool` and wait for the ticket. staple with `xcrun stapler`. A bare executable cannot be notarized. it is wrapped in a ZIP, DMG, or PKG container first.

- Hardened runtime is a notarization prerequisite (enable the capability and declare the needed entitlements).
- The signing form is `codesign --options runtime --timestamp -s "Developer ID Application: NAME (TEAMID)" <App>` (the `--options runtime` flag is the hardened runtime, `--timestamp` is the secure timestamp).
- Submit `xcrun notarytool submit <container> --apple-id ... --team-id TEAMID --password <app-specific-password> --wait`, then `xcrun stapler staple <App>`.
- What breaks. an app that is not stapled fails to launch on an offline Mac, because Gatekeeper cannot fetch the ticket. an app that is not notarized at all shows the "Apple cannot check it for malicious software" or "app is damaged" dialog and is blocked on stricter policies.

Sources. [Apple notarizing macOS software](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution), [Apple Developer ID](https://developer.apple.com/developer-id/), [Apple customizing the notarization workflow](https://developer.apple.com/documentation/security/customizing-the-notarization-workflow).

### 1.2 Guideline 4.2 minimum functionality and 4.3 spam or duplicate (HARD, top rejection bucket)

- 4.2 Minimum Functionality. an app includes features, content, and UI that lift it beyond a repackaged website. a thin web view or wrapper is rejected. web tech (WebView, React Native) is allowed only when the result feels native and has lasting value. Placeholder or incomplete content that reads as unfinished is rejected.
- 4.3(a) Spam or duplicate. apps that provide the same feature set as other apps and only vary in content or language are treated as spam. Submitting multiple similar apps, or repackaging one app many times, triggers this.
- 4.3(b) Copycat. cloning or imitating another developer's app.
- June 2026 tightening. Apple strengthened 4.3 and named saturated categories (dating, flashlight, sound effects, wallpaper, simple timers, fortune telling). New submissions in these categories are not accepted unless they offer a materially different or improved experience, and Apple may remove existing apps in these categories that are not updated, improved, or attracting customers.

Sources. [Apple App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/), [Apple 2026 guideline update](https://developer.apple.com/news/?id=d75yllv4), [MacRumors on the 4.3 saturation tightening](https://www.macrumors.com/2026/06/09/app-store-guidelines-low-quality-apps/).

### 1.3 Reader apps, the External Link Account Entitlement (Guideline 3.1.3(a))

A reader app provides magazines, newspapers, books, audio, music, or video as its primary function. The optional External Link Account Entitlement lets it include one informational link to a developer-owned site to create or manage an account. Conditions to qualify. the eligible content is the primary function. sign-in to an externally-created account. access to previously purchased content when signed in. NO in-app purchase offered while the entitlement is used. no real-time person-to-person services (tutoring, medical, fitness). Link rules, all required. links to a site you own. opens the default browser in a new window, not a web view. https scheme with no query or extra URL parameters. no redirects. defined statically in Info.plist before submission. shown once per page with standard HTML styling. Entitlement identifier `com.apple.developer.storekit.external-link.account` (iOS 16 or later). earlier OS uses Apple's exact modal sheet.

Source. [Apple reader apps](https://developer.apple.com/support/reader-apps/).

### 1.4 France ANSSI encryption declaration (beyond ITSAppUsesNonExemptEncryption)

Apple's export-compliance documentation matrix.

| Encryption in use | Documentation required |
|---|---|
| Apple OS crypto only | none in App Store Connect |
| An industry-standard algorithm not provided by Apple's OS | upload a French encryption declaration in App Store Connect, if distributing in France |
| A proprietary algorithm not accepted by IEEE, IETF, or ITU | upload both a US CCATS and the French encryption declaration |

The French declaration is required only when distributing on the French App Store, uploaded in App Store Connect, and the authority is ANSSI. Banking and Medical apps are exempt. `ITSAppUsesNonExemptEncryption` in Info.plist avoids re-answering the encryption question each submission. Note. the US annual self-classification report to BIS is an EAR obligation, not an App Store Connect field, so it is an external legal item to track, not a store check.

Source. [Apple export compliance documentation for encryption](https://developer.apple.com/help/app-store-connect/reference/export-compliance-documentation-for-encryption/).

### 1.5 Content-rights declaration in App Store Connect (maps to Guideline 5.2)

App Store Connect asks, before each submission, whether the app contains, shows, or accesses third-party content. If yes, the developer must hold the rights under the laws of each country the app is available in, and must be able to provide proof of rights to Apple (attach supporting documents in App Review notes). Source. [Apple App Information reference](https://developer.apple.com/help/app-store-connect/reference/app-information/app-information/).

### 1.6 visionOS, watchOS, and tvOS submission specifics

- visionOS App Motion. if the app contains movement such as quick turns or sudden camera changes, indicate it in App Store Connect. the product page then shows a motion badge for motion-sensitive users.
- visionOS Developer Capture. screenshots and previews use the Developer Capture feature in Reality Composer Pro, not a Control Center screen recording (which is foveated and low resolution).
- SDK minimums, effective 28 April 2026. watchOS apps build with the watchOS 26 SDK, tvOS apps with the tvOS 26 SDK, all with Xcode 26, the same deadline as iOS 26 and visionOS 26.
- App completeness (Guideline 2.1) and the privacy declarations apply to every platform, including watchOS and tvOS. Pull the exact per-device screenshot and asset dimensions live from the App Store Connect screenshot-spec page, as they change per device.

Sources. [Apple submit visionOS apps](https://developer.apple.com/visionos/submit/), [Apple SDK minimums 28 April 2026](https://developer.apple.com/news/upcoming-requirements/?id=02032026a).

### 1.7 In-App Events, Custom Product Pages, and the submission-concurrency limit

- In-App Events. up to 10 live at a time, up to 15 approved per app, each reviewed as a submission item against the guidelines.
- Custom Product Pages. up to 70 additional product-page versions, metadata reviewed independently of an app update and still bound by the guidelines.
- Submission concurrency. a platform can have at most two submissions under review at once, one with an app version and one with items (events or custom product pages) that carry no version.
- StoreKit External Purchase entitlements are region-gated. the `allowed-regions` entitlement array must match the entitlement Apple granted (EU, and South Korea for external purchase, plus the separate US external-link path). Check the presence and configuration of the entitlement, not the fee math, which is fluid.

Sources. [Apple In-App Events](https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/submit-an-in-app-event/), [Apple Custom Product Pages](https://developer.apple.com/app-store/custom-product-pages/), [Apple StoreKit external purchase](https://developer.apple.com/documentation/storekit/external-purchase).

## 2. Google Play and Android mechanics

### 2.1 Android developer verification (identity, all Android apps including sideloaded)

A device-level service checks whether an installed app is registered to a verified developer identity, for all Android apps on certified devices, including sideloaded and alternative-store apps, not only Play Store apps. Timeline. verification opened to all developers in March 2026. the verifier service began auto-installing on devices in June 2026. registration by a verified developer becomes required to install or update apps on certified devices in Brazil, Indonesia, Singapore, and Thailand from 30 September 2026, with participating stores including Google Play, Samsung, Xiaomi, and others. global rollout follows in 2027. A student or hobbyist can use a limited distribution account to share to up to 20 devices without a government ID or fee. Consequence. after the deadline in a participating country, an app from an unverified developer cannot be installed or updated on certified devices through participating stores.

Sources. [Android developer verification](https://android-developers.googleblog.com/2026/06/android-developer-verification.html), [Android verification rolling out to all developers](https://android-developers.googleblog.com/2026/03/android-developer-verification-rolling-out-to-all-developers.html).

### 2.2 Foreground Service types, Android 14 (API 34) and later (HARD)

An app targeting API 34 or later that runs a foreground service must declare `android:foregroundServiceType` in the manifest AND hold the matching `FOREGROUND_SERVICE_*` permission. a missing permission throws a runtime exception and the service cannot start. Separately, the Play Console requires a foreground-service-types declaration on the App content page for each type, including a description, the user impact if deferred, a demo video, and a mapped use case. a missing Play declaration is an update rejection under the Device and Network Abuse policy. Related. `USE_FULL_SCREEN_INTENT` on API 34 or later is auto-granted only for alarm and calling apps. all others declare it in Play Console or request it at runtime and degrade gracefully.

Sources. [Android FGS types required](https://developer.android.com/about/versions/14/changes/fgs-types-required), [Play Console FGS declaration](https://support.google.com/googleplay/android-developer/answer/13392821?hl=en).

### 2.3 Play Integrity API and the SafetyNet retirement (HARD)

SafetyNet Attestation is fully shut down (turndown completed 31 January 2025). all attestation and anti-abuse checks must use the Play Integrity API. An app that still calls `com.google.android.gms:play-services-safetynet` is calling a dead service. Verify the server checks the Play Integrity verdict with `requestHash` request-binding. Source. [Play Integrity API](https://en.wikipedia.org/wiki/Play_Integrity_API).

### 2.4 Play Billing Library minimum version (HARD)

By 31 August 2026, all new apps and updates to existing apps must use Play Billing Library version 8 or later (an extension is available on request until 1 November 2026). This is a publishing gate, not a runtime kill switch. an already-published version-7 binary keeps transacting, but no new release, including a security patch, can ship on version 7 after the gate. Version 9 shipped in May 2026, and there is no direct version-7-to-9 jump, so migrate to version 8 first. Verify the `com.android.billingclient:billing` dependency is at least version 8 before the deadline, and that an app selling digital goods actually uses Play Billing rather than a side payment flow. Source. [Android Play Billing deprecation FAQ](https://developer.android.com/google/play/billing/deprecation-faq).

### 2.5 Target API level (annual bump, HARD)

New apps and updates must target Android 15 (API 35) or later. existing apps must target API 34 or later to stay visible to new users on newer devices (Wear OS, Android TV, and Automotive target API 34 or later), effective 31 August 2025 with an extension window. The 2026 bump to API 36 (Android 16) for new apps and updates, reported for 31 August 2026 with a version-35 minimum for existing apps, is consistent with Google's yearly release pattern but should be verified live on the target-sdk page before it is written as a fixed date. Verify `targetSdkVersion` is at least 35 today and plan for at least 36 by the 2026 deadline.

Sources. [Android target SDK requirement](https://developer.android.com/google/play/requirements/target-sdk), [Play Console target API help](https://support.google.com/googleplay/android-developer/answer/11926878?hl=en).

### 2.6 Disruptive ads and unexpected full-screen interstitials (HARD)

The Better Ads Experiences policy bans full-screen interstitials that appear unexpectedly (for example when a user is about to read an article or is mid-task), ads at the start of a content segment or before the app's loading screen, and full-screen interstitials that cannot be closed after 15 seconds (opt-in and rewarded ads excepted). Allowed. interstitials at a natural transition point (end of a game level or chapter), non-full-screen ads, and genuine opt-in or rewarded ads. Verify no interstitial fires at app launch or mid-task, every interstitial has a close control that works by 15 seconds, and ads do not overlay system controls or the app's own UI.

Sources. [Play Console ads policy](https://support.google.com/googleplay/android-developer/answer/9857753?hl=en), [Play Better Ads Experiences](https://support.google.com/googleplay/android-developer/answer/12271244?hl=en).

### 2.7 Health Connect and health-apps data policy

A health app completes the Health Apps Declaration (the Health Connect declaration form enforcement began in March 2025). A January 2026 tightening added a medical-device labeling system, stricter Health Connect data justifications, and a ban on using age-restricted signals for health profiling. requesting sensitive Health Connect read permissions requires proving the data is necessary to the app's primary function. Existing health apps migrate to a verified Organization Account by 28 January 2026. an app without regulatory clearance shows the disclaimer that it is not a medical device. Verify the declaration is complete, each Health Connect permission has a core-function justification, the Organization Account is migrated, and the label or disclaimer is correct.

Sources. [Play Console Health content and services](https://support.google.com/googleplay/android-developer/answer/16679511?hl=en), [Play Console Health Connect permissions](https://support.google.com/googleplay/android-developer/answer/12991134?hl=en).

### 2.8 Real-money games and Brazilian betting license (HARD)

- **Google Real-Money Games**: Google historically allowed real-money games only where a government licensing regime exists. a 2024 pilot opened a program for real-money games not covered by an existing regime (first in India, Mexico, Brazil), then Google paused the expansion of new types citing the absence of a central approval authority in some regions. India moved toward a developer self-declaration model in mid-2025, status evolving. Verify a real-money-game app is in a supported country with an accepted license or a valid self-declaration, with the real-money-game declarations, age-gating, geo-restriction, and the correct service-fee model in place.
- **Apple Brazilian Betting License (May 8, 2026)**: Following changes to Brazil's fixed-odds betting regulation, apps with fixed-odds betting (gambling) features can only be distributed on the App Store in Brazil with a valid fixed-odds betting license from the **Secretariat of Prizes and Bets (SPA)**.
  - Answering "Yes" to the gambling question in the age rating questionnaire in App Store Connect will automatically set the app's Brazil age rating to **A18**.
  - To trigger the license verification process, **a new app version must be submitted** for review; simply updating the App Review Information section in App Store Connect alone is insufficient and will not start the verification review.
  - License information must be explicitly provided in the App Review Information section during the submission of the new version.

Sources. [Google real-money games approach](https://android-developers.googleblog.com/2024/01/a-new-approach-to-real-money-games-on-google-play.html), [Google pauses RMG expansion (NEXT.io)](https://next.io/news/regulation/google-halts-rmg-expansion-on-play-store/), Apple Developer News, "Brazilian betting license requirement for App Store availability" (May 8, 2026).

### 2.9 Media permissions, exact alarm, package visibility, and account-deletion URL

- Photo and Video permissions. only an app with a genuine broad-access need keeps `READ_MEDIA_IMAGES` or `READ_MEDIA_VIDEO`. one-time or limited use uses the Android Photo Picker. full compliance was mandatory from 28 May 2025, and a non-compliant app is subject to removal.
- Account deletion. an app that allows in-app account creation provides both an in-app deletion path and a web-based deletion URL, both declared in the Data safety form. an unreachable deletion URL is a frequent rejection.
- `QUERY_ALL_PACKAGES` (package visibility) and `SCHEDULE_EXACT_ALARM` or `USE_EXACT_ALARM` remain declaration-gated permissions that require a justification against an approved use case.

Sources. [Play Console Photo and Video permissions](https://support.google.com/googleplay/android-developer/answer/14115180?hl=en), [Play Console account deletion](https://support.google.com/googleplay/android-developer/answer/13327111?hl=en).

## 3. Cross-cutting (both platforms)

### 3.1 CSAM reporting for UGC apps (LEGAL)

- US, 18 U.S.C. 2258A. a provider that gains actual knowledge of an apparent child-sexual-abuse violation must report to the NCMEC CyberTipline as soon as reasonably possible. the provider is not required to affirmatively search, but must report on knowledge. The REPORT Act (signed 7 May 2024) raised penalties (first offense 600,000 to 850,000 dollars, pattern up to 1,000,000 dollars, scaling with provider size), expanded reportable conduct to child sex trafficking and enticement, and extended evidence preservation from 90 days to 1 year.
- UK, the Online Safety Act 2023. in-scope user-to-user and search services carry illegal-harm duties including child sexual exploitation and abuse. the first illegal-content Codes took effect 17 March 2025, and the children's-access duties from 25 July 2025. penalty up to 18 million pounds or 10 percent of global revenue.
- EU, the CSA Regulation is not yet a final permanent instrument (the mandatory-scanning push was dropped for voluntary detection, trilogues ongoing). the temporary derogation that permits voluntary scanning was reinstated to run to 2028. Do not hard-code an EU mandatory-scanning duty yet. track it as pending.

Verify, for a US-facing UGC app. a documented escalation path to file a NCMEC report on actual knowledge, a 1-year preservation policy for the reported content, and a reporting mechanism. Sources. [18 U.S.C. 2258A](https://www.law.cornell.edu/uscode/text/18/2258A), [Ofcom illegal harms](https://www.ofcom.org.uk/online-safety/illegal-and-harmful-content/), [Council CSA Regulation position](https://www.consilium.europa.eu/en/press/press-releases/2025/11/26/child-sexual-abuse-council-reaches-position-on-law-protecting-children-from-online-abuse/).

### 3.2 UGC minimum requirements and Child Safety Standards (STORE)

- Apple Guideline 1.2. a UGC or social app has all four. a content filter, an in-app report mechanism with timely responses, the ability to block abusive users, and published developer contact info. Apps must remove reported content and eject the offending user within 24 hours of a report. a 6 February 2026 update states that random or anonymous chat apps are explicitly subject to 1.2.
- Google Play UGC policy. an app with UGC requires terms acceptance before posting, defines and prohibits objectionable content, provides an in-app system to report and block objectionable content and users, and acts on reports.
- Google Play Child Safety Standards, effective 19 March 2025 for the Social and Dating categories. five requirements. published CSAE standards on a globally reachable web page that names the app and developer with the link entered in Play Console, an in-app feedback mechanism, a CSAM response protocol, a named child-safety point of contact, and compliance with in-jurisdiction child-safety law. this applies regardless of whether the app actually has child users, and is a removal cause for the Social and Dating categories.

Sources. [Apple App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/), [Google Play Child Safety Standards](https://support.google.com/googleplay/android-developer/answer/14747720?hl=en).

### 3.3 Accessibility as a store-review dimension

Neither store hard-rejects for failing WCAG, so this is a medium store risk and a high legal risk (see 3.6 and the European Accessibility Act in the EU doc).

### 3.4 EU Packaging and Packaging Waste Regulation (PPWR), Regulation (EU) 2025/40 (HARD, NEW)

The Packaging and Packaging Waste Regulation (PPWR) applies across all 27 EU Member States from **12 August 2026**, establishing a harmonised regulatory framework for packaging compliance to replace the legacy directive (94/62/EC).

- **Scope:** Applies directly to all economic operators present on the EU market or trading with the EU involved in manufacturing, importing, or distributing packaged products. Compliance with PPWR is a precondition for legally placing any packaged product on the EU market.
- **Key Obligations:**
  - **Compliance Documentation:** Companies must compile and maintain Technical Documentation and hold a valid EU Declaration of Conformity.
  - **Substance Limits:** Operators must ensure and document that packaging conforms to substance restriction thresholds (such as PFAS and heavy metal limits).
- **Sources:** [ETL Global PPWR 2026 Rules](https://www.etl-global.com/eu-sustainability-rules-2026-esg/), [EUR-Lex PPWR Text](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32025R0040).

### 3.5 Accessibility labels (STORE)

- Apple Accessibility Nutrition Labels, introduced 2025, appear on the product page and cover 9 features (VoiceOver, Voice Control, Larger Text, Dark Interface, Differentiate Without Color Alone, Sufficient Contrast, Reduced Motion, Captions, Audio Descriptions). they are voluntary now, and Apple states they will become required to submit over time. a claimed feature must let users complete all common tasks with it, and a misleading label is contacted under Guideline 2.3 (accurate metadata), which is the enforceable accessibility hook today.
- Google Play provides tooling, not a gate. the Accessibility Scanner and TalkBack. checkable criteria include touch targets of at least 48dp, content descriptions on all interactive and graphical elements, and TalkBack-navigable controls.

Verify. Apple Accessibility Nutrition Labels populated and not over-claimed, UIAccessibility labels and traits present, and on Android the 48dp targets, content descriptions, and a clean Accessibility Scanner run. Sources. [Apple Accessibility Nutrition Labels](https://developer.apple.com/help/app-store-connect/manage-app-accessibility/overview-of-accessibility-nutrition-labels/), [Android accessibility testing](https://developer.android.com/guide/topics/ui/accessibility/testing).

### 3.6 Account and data deletion, the web URL (STORE, commonly missed)

- Apple Guideline 5.1.1(v). an account-creating app lets users start account and associated-data deletion in-app (in force since 30 June 2022). a public web deletion or privacy-choices page is provided through the optional Privacy Choices URL in App Store Connect.
- Google Play. an account-creating app provides both an in-app deletion path and a web-link resource for account and data deletion that works even after uninstall, both declared in the Data safety form. an invalid or unreachable deletion URL is a frequent rejection.

Verify the in-app delete flow deletes data (not deactivate), and that a publicly reachable web deletion URL (returns 200, no login wall) is declared. Sources. [Apple offering account deletion](https://developer.apple.com/support/offering-account-deletion-in-your-app/), [Google Play account deletion](https://support.google.com/googleplay/android-developer/answer/13327111?hl=en).

### 3.7 OFAC sanctions and embargoed-territory availability (LEGAL)

US sanctions prohibit providing goods or services to blocked persons and embargoed territories. Apple itself settled with OFAC for 466,912 dollars in 2019 for hosting a blocked developer's apps, and 2025 reporting found sanctioned-linked apps slipping into both stores, so the developer's own compliance still matters. Verify the developer or entity is not on the OFAC SDN list, and the app's country availability in App Store Connect and Play Console excludes the embargoed territories (Cuba, Iran, North Korea, Syria, and the sanctioned regions of Ukraine). Source. [TTP on sanctioned apps in the stores](https://www.techtransparencyproject.org/articles/u.s.-sanctioned-firms-find-opening-in-apple-and-google-app-stores).

### 3.8 ADA Title III accessibility litigation (LEGAL, US)

Federal Title III web-accessibility suits rose about 27 percent in 2025, and mobile-app suits are a growing share, with WCAG 2.1 AA as the de facto court standard, though there is no DOJ Title III technical rule for private businesses. the DOJ Title II final rule (2024) requires state and local government apps to meet WCAG 2.1 AA by 2026 or 2027 by population. Flag WCAG 2.1 AA as a legal risk-mitigation item for US consumer apps, and a hard deadline for government or public-entity apps. Source. [ABA on Title III digital accessibility](https://businesslawtoday.org/2025/08/digital-accessibility-under-title-iii-of-the-ada/).

### 3.9 PSD2 SCA and PCI DSS for card payments outside store billing (LEGAL and contractual)

These apply only to legitimate non-store card payments for real-world goods and services. digital goods and subscriptions must still route through Apple in-app purchase or Google Play Billing.

- PSD2 Strong Customer Authentication. an EU or UK remote card payment for real goods needs two of three factors (knowledge, possession, inherence), usually 3D Secure, with limited exemptions (low value, transaction-risk analysis). PSD3 is expected around 2026 to 2027, so monitor.
- PCI DSS version 4.0.1 is the current standard, with all future-dated requirements mandatory from 31 March 2025. tokenization or Apple Pay or Google Pay keeps the app off the card number and reduces scope to roughly SAQ A. handling raw card data pulls in far heavier requirements.

Verify. if the app takes EU or UK card payments for real goods, SCA and 3D Secure are implemented. if the app handles cards, no card number is stored, logged, or cached, entry goes to a tokenizing processor or a wallet, and the correct SAQ is identified. Sources. [Stripe SCA guide](https://stripe.com/guides/strong-customer-authentication), [PCI SSC SAQ bulletin for v4.0.1](https://www.pcisecuritystandards.org/wp-content/uploads/2024/10/SAQs_for_PCI_DSS_v4.0.1_Bulletin.pdf).

## 4. Consolidated audit checklist (HARD gates)

| Gate | Verify | Platform |
|---|---|---|
| macOS notarization | Developer ID signed, hardened runtime, notarytool submitted, stapled | Apple (non-store macOS) |
| 4.2 / 4.3 | Not a thin wrapper, not a duplicate or clone, not an un-differentiated saturated-category app | Apple |
| Reader app entitlement | 3.1.3(a) conditions and link rules met, no IAP while used | Apple |
| France encryption | French ANSSI declaration uploaded if non-exempt crypto and distributed in France | Apple |
| Content rights | ASC third-party-content question answered, proof available | Apple |
| visionOS App Motion | Declared, Developer Capture screenshots | Apple |
| SDK 26 (all platforms) | Built with Xcode 26 and the platform-26 SDK by 28 April 2026 | Apple |
| Developer verification | Verified before 30 Sep 2026 if distributing to Brazil, Indonesia, Singapore, Thailand | Android |
| Foreground service types | Manifest type + matching permission + Play Console declaration with demo video | Android |
| Play Integrity | No SafetyNet Attestation, verdict verified server-side | Android |
| Play Billing v8+ | Billing Library at least version 8 before 31 Aug 2026 | Android |
| Target API | targetSdkVersion at least 35 now, plan for 36 by Aug 2026 | Android |
| Disruptive ads | No launch or mid-task interstitial, closable by 15 seconds | Android |
| Health Connect | Declaration, core-function justification, org account, correct label | Android |
| UGC controls | Report, block, filter, published contact, 24-hour remove-and-eject (Apple 1.2) | Both |
| Child Safety Standards | Published CSAE URL, in-app report, response protocol, named contact (Social and Dating) | Google Play |
| CSAM reporting | NCMEC CyberTipline path and 1-year preservation for a US UGC app | Legal |
| Account and data deletion | In-app deletion plus a reachable web deletion URL, declared | Both |
| Sanctions | Entity not SDN-listed, availability excludes embargoed territories | Legal |
| Card payments | SCA and 3D Secure on EU or UK real-goods card flows, no PAN stored, correct PCI SAQ | Legal |
| Accessibility labels | Apple Accessibility Nutrition Labels populated and not over-claimed | Apple |
| Packaging Reform (PPWR) | Confirm packaging compliance via EU Declaration of Conformity and Technical Documentation | Both |

## 5. Sources and verification note

Apple facts cite developer.apple.com. Android and Google Play facts cite developer.android.com and the Play Console help. legal facts cite the statute, the regulator, or the standards body. Where a government or Apple page rendered as a client-side app that resisted an automated read, the fact was cross-checked across reputable sources and is flagged here.

### Source Trust Hierarchy

All sources used for establishing regulatory requirements must adhere to the following priority guidelines:

- Priority 1 (Primary Official): European Commission, EUR-Lex, Official Journal of the European Union, ENISA, EDPB, FTC, NIST, CISA, ICO, and official government publications.
- Priority 2 (Highly Reputable News): Reuters, AP (Associated Press), Bloomberg.
- Priority 3 (Academic): Academic papers and peer-reviewed journals.
- Priority 4 (Industry): Industry blogs and vendor publications.
- Priority 5 (Social & Unverified): LinkedIn, Reddit, Twitter, and AI generated summaries.

### Compliance Pull Request Rules

- Never trust secondary sources before official sources.
- Never create compliance pull requests using Priority 4 or Priority 5 sources unless verified by a Priority 1 source. Any citation or claim sourced from Priority 4 or 5 must be traceably corroborated by an official publication from Priority 1.

Marked unverified, confirm against the primary source before relying on a figure. the 2026 Android target API 36 date (widely reported, consistent with the annual release pattern, but the official target-sdk page still showed the 2025 text at fetch time). the exact `codesign`, `notarytool`, and `stapler` command strings (corroborated across sources, not copied from a rendered Apple page). the exact visionOS, watchOS, and tvOS per-device screenshot pixel dimensions (pull live from the App Store Connect screenshot page). the exact date Apple's Accessibility Nutrition Labels become mandatory (Apple says over time, no date published). the Google real-money-games India final rollout status. the EU CSA Regulation final form (in trilogue). the US BIS annual self-classification report specifics. and the PSD3 timing.

Treat this document as HARD on the existence and direction of each obligation, and advisory on any specific number, version, or date until re-verified against the cited source.
