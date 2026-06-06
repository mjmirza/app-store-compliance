# Apple App Store Review Guidelines. Rejection Map

Source. Apple App Store Review Guidelines (developer.apple.com/app-store/review/guidelines). Empirical ranking from Apple's 2024 App Store Transparency Report and 2025 enforcement reporting.

Apple groups every rule into five sections. Safety, Performance, Business, Design, Legal. The tables below list every rejection causing guideline, what it requires, the exact behavior that triggers a rejection, and how to avoid it. Severity reflects how often the rule causes a real rejection and how hard it is to recover from.

## Ranked reality (where rejections actually come from)

| Rank | Area | Guideline | Why it tops the list |
|---|---|---|---|
| 1 | Privacy noncompliance | 5.1.1, 5.1.2 | Single biggest cause of update and new app rejection. Missing privacy policy, vague purpose strings, no account deletion, undisclosed data sharing |
| 2 | App completeness | 2.1 | Crashes, broken links, placeholder content, missing demo account, backend not live during review. Over 1.2 million performance rejections in 2024 |
| 3 | Inaccurate metadata | 2.3 | Hidden features, misleading screenshots, undocumented functionality, keyword stuffing |
| 4 | In app purchase | 3.1.1 | Trying to sell digital goods outside Apple's in app purchase, missing restore, undisclosed odds |
| 5 | Minimum functionality and spam | 4.2, 4.3 | Repackaged websites, thin apps, duplicate bundle IDs, template apps, saturated category clones |
| 6 | Design and login | 4.8 | Third party login present without an equal privacy preserving alternative |

About one in four submissions is rejected. A large share fail on privacy and stability as Apple tightens enforcement and, per industry reporting, increasingly automates parts of review. Treat the figures here as directional, from store transparency reporting, and confirm current numbers against the source before quoting them.

## Section 1. Safety

| Guideline | Requires | Triggers rejection | Avoid by |
|---|---|---|---|
| 1.1 Objectionable content | No defamatory, discriminatory, violent, sexual, or inflammatory content | Mean spirited content, realistic depictions of harm, pornography, hookup or prostitution promotion, fake or trick functionality. An entertainment disclaimer does not excuse it | Ship genuine, non objectionable functionality and remove joke or fake utility features |
| 1.2 User generated content | Filtering, reporting, blocking, and published contact info for any app with UGC | No content filter, no report mechanism, no way to block abusive users, anonymous or objectionable chat | Build moderation, in app reporting, user blocking, and a contact method before submission |
| 1.2.1 Creator content | Age restriction so minors cannot reach age inappropriate creator content | Creator app with no age gating mechanism | Add an age restriction based on verified or declared age |
| 1.3 Kids category | No external links, no purchases, no IDFA, no third party ads or analytics collecting child data, all behind a parental gate | Links out, purchase opportunities, third party analytics or ads, children privacy law noncompliance | Gate every exit and purchase, strip third party SDKs that collect child data |
| 1.4 Physical harm | Accurate medical data, validated health claims, no encouragement of harm | Unvalidated health measurement claims, drug dosage calculators without approval, DUI checkpoint data not from law enforcement, dangerous challenges | Validate claims, cite approvals, remove harm encouraging features |
| 1.5 Developer information | An easy contact method in app or a support URL | Missing or outdated contact info | Add a working support URL and in app contact |
| 1.6 Data security | Appropriate security for user information | Unauthorized access, disclosure, or weak protection | Encrypt in transit and at rest, scope third party access |
| 1.7 Reporting criminal activity | Local law enforcement involvement where active | Reporting crime features without law enforcement involvement | Restrict to regions with active law enforcement partnership |

## Section 2. Performance

| Guideline | Requires | Triggers rejection | Avoid by |
|---|---|---|---|
| 2.1 App completeness | A finished, stable, fully reviewable build | Crashes, bugs, broken links, placeholder or temporary content, untested code, missing demo account or demo mode for account features, backend not live during review, in app purchases incomplete or invisible, undocumented non obvious features | Test on device, ship a live backend, provide demo credentials, explain every non obvious feature and every in app purchase in App Review Notes |
| 2.2 Beta testing | No demos, betas, or trials on the App Store | Submitting a trial or beta directly instead of using TestFlight | Use TestFlight for any pre release build |
| 2.3.1 Accurate metadata | No hidden, dormant, or undocumented features, no misleading marketing | Hidden functionality, false claims, generic Notes for Review, unvalidated claims such as an iOS virus scanner | Document everything, make claims you can prove |
| 2.3.2 IAP in metadata | In app purchases clearly indicated, correct purchase handling | IAP not indicated in description or screenshots, broken purchase completion | Show IAP in metadata, implement transaction completion correctly |
| 2.3.3 Screenshots | Screenshots show the app in use | Screenshots of only title art, a login page, or a splash screen | Capture real in app screens |
| 2.3.6 Age rating | Accurate age rating and content warnings | Inaccurate rating, missing warnings for films, music, games | Answer the age rating questionnaire honestly |
| 2.3.7 Names and keywords | App name 30 characters or fewer, clean keywords | Name too long, metadata packed with trademarks, app names, prices, or unrelated keywords | Keep the name short, keywords relevant and owned |
| 2.3.10 No other platforms | No references to other platforms or marketplaces | Naming Android, Google Play, or alternative marketplaces in app or metadata | Remove cross platform references |
| 2.4.2 Resource use | No excessive battery, heat, or background abuse | Rapid drain, excessive heat, unrelated background work such as crypto mining | Profile resource use, remove unrelated background tasks |
| 2.5.1 Software requirements | Public APIs only, current OS, no deprecated tech | Private API use, deprecated frameworks, APIs used for unintended purposes | Use only documented public APIs |
| 2.5.2 No executable code download | No downloading code that changes app features | Downloading or installing code that alters functionality | Ship all functionality in the binary, gate changes server side as data not code |
| 2.5.4 Background modes | Background services used only for declared purposes | Misusing VoIP, audio, or location background modes | Declare only the background modes you actually use |
| 2.5.18 Ad behavior | Age appropriate, non deceptive ads with a visible close control | Deceptive interstitials, ads on sensitive data, ads without a close button, ads in kids apps | Use compliant ad placements, never on health, school, or kids data |

## Section 3. Business

| Guideline | Requires | Triggers rejection | Avoid by |
|---|---|---|---|
| 3.1.1 In app purchase | Apple's in app purchase for all digital goods, services, and paid content access | Selling digital access with license keys, QR codes, crypto, or any non IAP method, loot boxes without disclosed odds, digital gift cards outside IAP, external buttons or links to purchase NFTs (the ban is global, not US only) | Route every digital purchase through StoreKit in app purchase, disclose loot box odds before purchase |
| 3.1.1(a) External link entitlements | StoreKit external purchase link entitlements used only in approved regions | Using external purchase links outside approved storefronts, misleading entitlement marketing | Apply for the correct entitlement, restrict to approved regions |
| 3.1.2 Subscriptions | Ongoing value, periods of 7 days or more, clear terms, available across devices | Subscriptions with no ongoing value, hidden terms, removing paid functionality to force a subscription, subscription scams | Provide continuous value, disclose terms, never remove what existing users already bought |
| 3.1.3 Other purchase methods | External payment only for the specific exempt categories such as reader, multiplatform, enterprise, and person to person services | A non exempt app using external payment for in app consumed goods | Use IAP unless the app is a documented exempt category |
| 3.2.2 Unacceptable business practices | No store like interface for third party apps, no artificial ad inflation, no manipulating other services, no usurious lending | Building an app store inside the app, fake ad impressions, personal loans over 36 percent APR or under 60 day terms, forcing rate or download actions | Remove these mechanics entirely |

## Section 4. Design

| Guideline | Requires | Triggers rejection | Avoid by |
|---|---|---|---|
| 4.1 Copycats | Original app, no impersonation, no third party brand in icon or name | Copying a popular app with minor changes, impersonating a service, using another brand's icon or name without permission | Build an original experience and own your brand assets |
| 4.2 Minimum functionality | Real features, content, and UI beyond a repackaged website | Repackaged website, thin web clip, marketing only app, content aggregator or link collection with no utility | Add native value, lasting utility, or entertainment |
| 4.2.3 Standalone and disclosed downloads | Works on its own, discloses on launch download size | Requiring another app to function, hidden large downloads | Make the app self sufficient, prompt before large downloads |
| 4.2.6 Templates | Template or generated apps submitted directly by the content provider | A reseller submitting many near identical template apps | The content owner submits, or use a single aggregated picker app |
| 4.3(a) Spam, duplicate bundles | One app, variations via in app purchase, not separate bundle IDs | Multiple bundle IDs of the same app for cities, teams, or schools | Consolidate into one app with in app content selection |
| 4.3(b) Spam, saturated categories | A unique high quality experience in crowded categories | A low effort clone in a saturated category, repeated store spam | Provide genuine differentiation or do not ship the clone |
| 4.4 Extensions | Extensions follow the extension guidelines, are disclosed, carry no ads or IAP | Non functional or undisclosed keyboard, Safari, or share extensions | Build functional extensions, disclose them, keep ads out |
| 4.7 Mini apps and chatbots | Hosted software follows privacy 5.1, moderation, and in app purchase rules, with an index and age controls | Hosted mini apps, chatbots, or plug ins that skip moderation, privacy, or IAP, or expose native APIs | Apply the full guidelines to every piece of hosted software |
| 4.8 Login services | An equal alternative login that limits data to name and email and allows a private email, whenever third party social login is offered | Offering only Facebook, Google, or similar social login with no privacy preserving alternative | Add Sign in with Apple or an equivalent that keeps email private and does not track for ads |
| 4.9 Apple Pay | All required purchase terms disclosed before sale, correct Apple Pay UI | Missing recurring terms, improper Apple Pay branding | Disclose renewal term, charges, and cancellation |
| 4.10 Monetizing built in capabilities | No monetizing native hardware or Apple services | Charging for camera, push, gyroscope, Apple Music access, or iCloud | Do not gate native capabilities behind payment |

## Section 5. Legal

| Guideline | Requires | Triggers rejection | Avoid by |
|---|---|---|---|
| 5.1.1(i) Privacy policy | A privacy policy linked in App Store Connect and inside the app, describing data collected, third party protection, retention, and deletion | Missing, inaccessible, or vague privacy policy, undisclosed third party sharing | Publish a complete, accessible privacy policy and keep it accurate |
| 5.1.1(ii) Consent and purpose strings | Consent before collection, paid features not gated by data access, clear purpose strings, easy consent withdrawal | No consent, paid features blocked behind a permission, vague purpose strings, no way to withdraw | Request consent, write specific purpose strings, never gate purchases behind data access |
| 5.1.1(iii) Data minimization | Only data relevant to core functionality | Excessive or irrelevant data collection | Collect the minimum, use the system picker or share sheet instead of full access |
| 5.1.1(v) Account sign in and deletion | Account deletion inside any app that supports account creation, login optional for non core features, no off device storage of social credentials | Account creation with no in app deletion, mandatory personal data for non core features, social tokens stored off device | Add in app account deletion, make login optional where possible, never store social credentials off device |
| 5.1.1(ix) Regulated fields | Banking, healthcare, gambling, cannabis, air travel, and crypto apps submitted by the legal entity, with geo restriction where required | An individual developer submitting a regulated app, cannabis app not geo restricted | Submit under the regulated legal entity and geo restrict |
| 5.1.2(i) Data use and sharing | Permission and ATT consent before tracking, disclosed third party and third party AI sharing, no required system access or payment to use the app | Tracking without App Tracking Transparency consent, undisclosed sharing, requiring push, location, or tracking to use the app, paying users for data | Implement the ATT prompt, disclose every recipient including AI providers, never gate the app on tracking |
| 5.1.2(vi) Sensitive frameworks | HealthKit, HomeKit, ClassKit, and similar data never used for advertising, marketing, or data mining | Using health, home, or education data for ads or analytics | Keep sensitive framework data out of marketing entirely |
| 5.1.3 Health and research | Health data not used for ads, informed consent and an ethics board for research apps | Health data sold or mined, research without consent or ethics approval | Restrict health data use, obtain consent and ethics review |
| 5.1.4 Kids privacy | COPPA, GDPR, and local law compliance, no third party analytics or ads in kids apps, privacy policy for any app handling minor data | Child data noncompliance, third party SDKs in kids apps, For Kids language outside the Kids category | Comply with child privacy law, strip third party child data SDKs |
| 5.1.5 Location services | Location only when relevant, with notice and consent and a clear purpose | Irrelevant location collection, no consent, undisclosed use | Use location only for real features, explain and ask first |
| 5.2 Intellectual property | Own or license all trademarks, copyrights, and content, no copycat metadata | Unauthorized brand, content, or media use, copycat names, downloading from YouTube or streaming services without authorization | Use only owned or licensed IP, never enable unauthorized media downloads |
| 5.3 Gaming and gambling | Licensed and geo restricted real money gaming, free to download, with official rules and no Apple sponsorship implied | Unlicensed real money gaming, paid gambling app, IAP funded real money credit, illegal gambling aids | License, geo restrict, make it free, never fund real money gaming via IAP |
| 5.4 VPN apps | NEVPNManager API, organization enrollment, declared data use, no selling or sharing data | Non standard VPN implementation, individual developer, data sold or shared | Enroll as an organization, use the official API, never sell VPN data |
| 5.5 Mobile device management | MDM capability granted by Apple, only for enterprise, education, or government | Unauthorized MDM use by an individual or non approved entity | Request the capability and restrict to approved entity types |
| 5.6 Developer code of conduct | Honest behavior, no impersonation, no review manipulation | Impersonating another app or service, manipulating ratings | Act honestly, build original apps |

## 2026 changes you must act on

| Change | Deadline or status | Action |
|---|---|---|
| New age rating system remaps the old bands into 4 plus, 9 plus, 13 plus, 16 plus, 18 plus (the old 12 plus and 17 plus are replaced, not kept alongside) | Respond to the updated age rating questions by the Apple stated deadline (reported as 31 January 2026, verify in App Store Connect) to avoid blocked update submissions | Answer the new age rating questionnaire for every app before submitting an update |
| AI assistant and chatbot content counts toward the rating | Active | Factor all AI generated content into the age rating, add an age restriction where the model can produce sensitive content |
| Third party AI data sharing disclosure under 5.1.2(i) | Active | Add a consent modal naming the AI provider and the data types shared before any personal data leaves the app |
| Creator content age identification under 1.2.1 | Active | Let users identify content that exceeds the app's rating and restrict by verified or declared age |
| AI assisted review and tighter spam and privacy enforcement | Ongoing | Expect deeper automated inspection of stability, privacy strings, and duplicate or AI slop apps |

## The Notes for Review field is a tool, not a formality

Most 2.1 and 2.3 rejections are recoverable in one cycle when the Notes for Review field carries a working demo account, a one line explanation of every non obvious feature, an explanation of every in app purchase, and any regional licensing detail. A reviewer who cannot reach a feature rejects it. Make every feature reachable and explained.
