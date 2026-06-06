# Advanced and 2026 Enforcement Layer

This document closes the gaps that the base rejection maps do not cover. It was built from a ten persona adversarial review of the base playbook (indie developer, enterprise lead, an Apple reviewer lens, privacy officer, fintech, kids, games, AI, ASO, security). The base maps cover the classic guideline numbers. This layer covers the modern upload time enforcement, the pre review account preconditions, the legal obligations that sit underneath store policy, and the per domain depth that causes real rejections in 2025 and 2026.

A framing that the whole layer rests on. Store compliance is not the same as legal compliance. Passing review does not make an app GDPR, COPPA, or EU AI Act compliant. The store enforces a subset, and a regulator enforces the rest. Both must be satisfied.

## 1. Apple upload time enforcement (the modern first wall)

These are checked when you upload the binary, before a human reviewer ever opens the app. Getting them wrong means the build is rejected or stuck and never reaches review.

| Item | What it is | What triggers the block | Fix |
|---|---|---|---|
| Privacy Manifest, PrivacyInfo.xcprivacy | A bundled file declaring the data the app and its SDKs collect, the tracking domains, and the reasons for using certain APIs | An app that uses required reason APIs without declaring an approved reason, or bundles a commonly used third party SDK that lacks a signed privacy manifest | Add a PrivacyInfo.xcprivacy to the app and confirm every listed third party SDK ships its own signed manifest. Keep the SDK versions current so the signed manifest is present |
| Required Reason APIs | A defined set of APIs (file timestamps, system boot time, disk space, user defaults, active keyboards) that need a declared approved reason code | Using one of these APIs with no NSPrivacyAccessedAPITypes entry or with a reason code that does not match the use | Declare each required reason API with an approved reason code in the privacy manifest |
| Tracking domains | NSPrivacyTrackingDomains in the manifest | A domain that performs tracking is contacted but not listed, while ATT consent is not granted | List every tracking domain and gate it behind ATT consent |
| Export compliance, ITSAppUsesNonExemptEncryption | The encryption declaration every iOS build must answer | Leaving it unanswered parks the build in Missing Compliance, so it never reaches review | Set ITSAppUsesNonExemptEncryption in Info.plist. For a standard app that only uses HTTPS, the exempt answer applies, which removes the per submission prompt |
| Build with the current SDK | Apple requires new submissions to be built with a recent SDK and Xcode by an annual deadline | An old SDK build after the deadline is rejected at upload | Build with the current required Xcode and SDK before the annual cutoff |

The privacy manifest is the single highest impact addition to any pre 2024 checklist. It is the most common modern upload rejection and it scales badly across an enterprise with many vendor SDKs, because each SDK must carry its own signed manifest.

## 2. Pre review account preconditions (you cannot even submit)

These block the submit button itself or leave the app in a Developer Action Needed state. They have nothing to do with the build.

| Precondition | Why it blocks |
|---|---|
| Apple Developer Program enrollment and identity verification | Enrollment verification can take days. Individual versus organization, and a D U N S number for an organization, must be resolved first |
| Paid Applications Agreement, plus tax and banking | In app purchases and paid apps cannot be reviewed until the agreement is accepted and tax and banking forms are complete |
| EU trader status under the Digital Services Act | Both stores require verified trader or developer identity information for distribution in the EU. Missing trader info blocks EU availability |
| Required store assets | The largest iPhone screenshot size and, for an iPad app, the iPad size, a 1024 pixel app icon with no alpha or transparency, and a preview video that meets spec. Missing a required size blocks submission |
| Metadata field limits | Apple name 30 characters, subtitle 30, keyword field 100, promotional text 170, description 4000. Google title 30, short description 80, full description 4000. Overflow or banned decoration blocks the listing |
| Metadata decoration rules | No emoji or emoticons in the title, no all caps except a brand, no ranking or price claims such as number one, best, top, or free in the title or icon, no fake notification badges on the icon |

## 3. In app purchase and payments depth

| Item | What developers miss | Fix |
|---|---|---|
| IAP created, attached, and submitted together | The IAP exists in App Store Connect but is not attached to the app version, so the reviewer cannot find it and rejects under 2.3.2 or 2.1 | Attach every IAP to the app version and submit it for review with the binary on the first review |
| Restore Purchases | A non consumable or non renewing purchase with no restore path | Provide a visible Restore Purchases control. Required for non consumables |
| Physical goods must not use IAP | Apple 3.1.5(a). Real world goods and services must use a payment method other than IAP. Using IAP for physical goods is itself a rejection | Use an external payment method for physical goods, and IAP only for digital goods |
| External purchase, anti steering, and the DMA | The base map treats external links as a narrow regional entitlement. The real picture in 2025 and 2026 includes the EU Digital Markets Act alternative payment and marketplace rules, the US external link state after the Epic versus Apple injunction, the StoreKit External Purchase API, mandatory disclosure sheets, and Google User Choice Billing and alternative billing programs | Treat external payments as a region specific program with an application, disclosure sheet rules, and reporting. Confirm the current state per region before relying on it |
| Commission tiers | Apple Small Business Program at the reduced rate, and reduced external or alternative billing fee tiers | Enroll in the Small Business Program if eligible and model the correct fee per region and program |
| Merchant of record and tax | External payments move tax, refunds, chargebacks, PCI DSS, and strong customer authentication onto the developer | If you take external payments, you own PCI DSS scope, SCA and PSD2 3 D Secure, refunds, and tax |
| Subscription depth | Price increase consent, grace periods, billing retry, account hold, free trial and intro offer disclosure | Implement the full subscription lifecycle, not only the purchase |

## 4. The demo account and reviewer reachability

The base map says provide a demo account. The real failures are about reachability.

- The demo account must not sit behind 2FA or SMS the reviewer cannot pass. Disable or bypass it for the review account.
- The credentials must not expire during the review window.
- The account must be pre populated with sample data so features are visible.
- The backend must be reachable from Apple's review network. A geo IP block, a VPN requirement, an allowlist, or a WAF rule that blocks the reviewer reads as a broken app.
- For a hard to reach feature, attach a demo video in App Review Notes.

## 5. Design quality, HIG, and device class

Apple 4.0 Design covers the practical your app looks broken bucket the base map does not.

- Broken layouts, truncated text, content clipped by the notch, Dynamic Island, or safe areas.
- Unsupported orientations and a poor iPad experience when the app is universal rather than marked iPhone only.
- A universal app that passes on iPhone but crashes or renders broken on iPad. Test every supported device class.
- Non native or unfinished UI that does not follow basic Human Interface Guidelines.

## 6. The legal layer (store compliance is not legal compliance)

| Obligation | What it requires beyond store policy |
|---|---|
| GDPR lawful basis, Article 6 | A documented lawful basis for every processing activity. Consent is one of six, not the default |
| GDPR notice content, Articles 13 and 14 | A privacy notice that states identity, purposes, lawful basis, recipients, transfers, retention, and rights. A linked policy that merely exists is not enough |
| International transfers, Chapter V | US analytics and third party AI are cross border transfers that need a transfer mechanism, not only disclosure |
| ePrivacy and German TTDSG or TDDDG | Consent quality, a real consent banner, and SDK consent gating before any non essential SDK loads |
| Data processing agreements, Article 28 | A DPA with every processor, and a controller versus processor classification of each SDK |
| DPIA, Article 35 | A data protection impact assessment for high risk processing |
| Special category data, Article 9 | Explicit consent or another Article 9 condition for health and similar data, beyond the store framework rules |
| Children's digital consent age, Article 8 | The EU age of digital consent varies from 13 to 16. Germany is 16. COPPA's under 13 is a US rule, not a global one |
| Data subject rights, Articles 15 to 22 | Access, rectification, erasure, portability, and objection, not only an account delete button |
| EU AI Act | Transparency duties, risk classification, and disclosure for AI features shipping in the EU, phasing in across 2025 and 2026 |
| DSA trader status | Verified trader or developer identity for EU distribution |

## 7. Children and families depth

- COPPA operative facts. The threshold is under 13. Persistent identifiers such as a device ID, advertising ID, IDFA, or cookies are themselves personal information for a child. The amended COPPA Rule from 2025 tightens consent and retention.
- Verifiable Parental Consent. A parental gate is not consent for data collection. Real VPC is a separate, stronger step.
- A valid parental gate uses an adult action a young child cannot perform, and gates external links and purchases.
- Neutral age screen versus parental gate. A mixed audience app uses a neutral age screen that does not nudge a younger answer, then branches.
- Apple Kids Category 1.3 bans behavioral advertising and requires ads to be age appropriate and human reviewed, rather than a flat ban on all ads. Verify the current wording.
- Google Families. The audience and content declaration in the Play Console is the trigger. Use the self certified ads SDK program and set AdMob child directed flags.
- Other regimes. US FERPA and state student data laws for ed tech, the UK Children's Code, and the California Age Appropriate Design Code.

## 8. Gambling depth

- Simulated gambling and social casino is a distinct category from real money gambling, with its own age rating and regional rules.
- Sweepstakes and dual currency sweeps coins models, cash prize skill tournaments, and daily fantasy are frequently treated as gambling and need the matching licensing and geo restriction.
- Real money gambling program mechanics. An entitlement or application, a country allowlist, and a free to download requirement.
- A national loot box and gambling law matrix governs odds disclosure and legality per country.
- Google Play requires an in game purchases including random items disclosure, with specific odds disclosure placement.

## 9. AI content policy (2026)

- Google Play has a distinct AI Generated Content policy. It is absent from the base map and must be satisfied for any generative app.
- Apple UGC rules 1.2 apply to AI generated OUTPUT, not only user to user content. The model is a content source that needs filtering, reporting, and blocking.
- Image and avatar generation abuse. NSFW, deepfake, face swap, and undress generation are high risk and cause removal.
- AI app age rating reality. A companion or character AI that can produce sensitive content needs the matching age rating and self harm and crisis safeguards.
- The thin AI wrapper. A bare front end over a third party model with no added value risks 4.2 and 4.3, distinct from the web wrapper case.
- Reviewer demo accounts for AI apps need a high or unlimited quota so the reviewer can exercise the feature.

## 10. Android specifics the base map underweights

| Item | Trigger | Fix |
|---|---|---|
| Dynamic code loading | DexClassLoader or downloading executable code at runtime | Ship all code in the package. Server changes are data, not code |
| Package visibility | QUERY_ALL_PACKAGES without a permitted use case | Declare specific packages, or use a permitted use case |
| Overlay and tapjacking | SYSTEM_ALERT_WINDOW or application overlay abuse, especially combined with AccessibilityService | Remove overlay abuse. The overlay plus accessibility combination is a strong malware signal |
| Granular media permissions | Requesting broad storage on Android 13 and later instead of the granular photo and video permissions, or misusing the Photo and Video Permissions policy | Use the granular media permissions and the photo picker |
| SDK Index | A banned or flagged SDK from the Google Play SDK Index | Check the SDK Index and remove flagged SDKs |
| In app account and data deletion | Google requires both in app account deletion and a web data deletion URL | Provide in app deletion and a public data deletion URL in the listing |
| Fingerprinting | Persistent identifier or fingerprinting to track users | Banned on both stores. Apple 5.1.2 bans fingerprinting regardless of ATT consent |

## 11. Ratings, reviews, and metadata integrity

- Apple requires the native SKStoreReviewController for rating prompts, and bans rating gating and incentivized reviews.
- Google bans incentivized and fake reviews and artificial installs.
- Competitor brand names or trademarks in the Apple keyword field or the Google description are a distinct, named rejection.
- Icon and screenshot integrity. No promotional or price or ranking badges on the icon, no fake notification dots, no emoji, no misleading overlays, captions, claims not in the app, or fake testimonials.

## 12. Account deletion must truly delete

The account deletion requirement is satisfied only by genuine deletion of the account and its data inside the app. A deactivate only flow, a mailto link, or a web form that the user must leave the app to reach does not satisfy it. A grep for a delete account symbol is necessary but not sufficient. Confirm the flow actually deletes.

## 13. Enterprise distribution and account blast radius

- Apple managed channels. Apple Business Manager custom apps, unlisted apps, and the in house program each have their own rules and are distinct from public review.
- Org account blast radius. A portfolio under one organization account shares a fate. One egregious violation can suspend the whole account. Isolate risk and treat an account level action as a top severity incident.

## 14. Caveats and verification

This playbook maps the structure of the live Apple and Google policies as fetched on the build date. Two honest caveats.

1. Guideline numbers and statistics change. Every guideline number here traces to the Apple App Store Review Guidelines page and every policy name to the Google Play policy center. Confirm the exact current number and any cited figure against the live source before quoting it externally. Treat the published rejection statistics as directional, from store transparency reporting, not as audited constants.
2. Some enforcement behavior is reported, not officially confirmed. Where the playbook describes automated or AI assisted review, treat it as industry reporting rather than an official store statement.

The automated guard is necessary, not sufficient. It uses string signals and cannot see your App Store Connect settings, your privacy manifest contents, your backend reachability, or your legal posture. A clean guard run means the cheap mechanical checks passed. The human checklist and this advanced layer carry the rest.
