# EU Regulatory Hard Rules (2026)

This document is the EU legal layer for App Store and Google Play compliance. It sits on top of the base rejection maps and the Advanced 2026 layer. The framing holds. Store compliance is not the same as legal compliance. Passing App Review does not make an app compliant with the EU AI Act, the Digital Markets Act, the Digital Services Act, or the European Accessibility Act. The store enforces a subset, a regulator enforces the rest, and for an app that reaches users in the EU both must be satisfied.

Every item in this document is a HARD rule for any app distributed to, or reaching, users in the EU or EEA. Each carries the date it takes effect and a source. Regulatory dates and fee numbers move, so re-verify against the cited source before quoting a figure externally. Items that could not be confirmed against a primary source are labelled unverified in section 9.

## 1. EU AI Act, Regulation (EU) 2024/1689

Scope. Any app whose AI feature reaches EU users is in scope, wherever the developer is based. A typical consumer app with an AI chatbot, assistant, or generation feature sits in the limited-risk transparency tier, not high-risk and not prohibited.

**MUST for every EU-facing AI app.** Sections 1.1 to 1.7 are a requirement, not a recommendation. An app with an AI feature that reaches EU users is not compliant, and must not be shipped to those users, until every HARD item in this section is satisfied. Treat this as a release blocker, the same weight as a working demo account or a matching privacy declaration.

### 1.1 Timeline (HARD dates)

| Date | What applies | Status mid-2026 |
|---|---|---|
| 1 Aug 2024 | Entry into force, no obligations yet | past |
| 2 Feb 2025 | Article 5 prohibited practices, Article 4 AI literacy | live now |
| 2 Aug 2025 | GPAI-model obligations, governance, penalties (Articles 99 and 100) | live now |
| 2 Aug 2026 | Article 50 transparency, and most remaining provisions | in force from this date |
| 2 Dec 2027 | Article 6(1) / Annex III High-risk AI systems (as deferred by the AI Omnibus, in force 27 July 2026) | future |
| 2 Aug 2028 | Annex I High-risk AI embedded in physical products (as deferred by the AI Omnibus, in force 27 July 2026) | future |

The Digital Omnibus simplification package (the AI Omnibus) was finalised in mid-2026 (Parliament 16 June 2026, Council final green light 29 June 2026, and entered into force on 27 July 2026). It postpones high-risk compliance deadlines (Annex III high-risk moved to 2 December 2027, Annex I physical high-risk moved to 2 August 2028), but **Article 50 transparency HOLDS at 2 August 2026**. Do not assume the transparency date moved. Sources. [artificialintelligenceact.eu timeline](https://artificialintelligenceact.eu/implementation-timeline/), [EUR-Lex 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng), [Council 29 June 2026](https://www.consilium.europa.eu/en/press/press-releases/2026/06/29/artificial-intelligence-council-gives-final-green-light-to-simplify-and-streamline-rules/), [EU Commission AI Omnibus Enters into Force 27 July 2026](https://digital-strategy.ec.europa.eu/en/news/ai-omnibus-enters-force).

### 1.2 Article 50 transparency (HARD, from 2 Aug 2026)

An app with an AI feature reaching EU users MUST do all of the following.

- AI-interaction disclosure, Article 50(1). If the app has a chatbot or assistant that interacts directly with a person, the person is told they are interacting with an AI system, unless it is obvious to a reasonably informed person. A plain in-app line such as "You are chatting with an AI assistant" satisfies this.
- Synthetic-content marking, Article 50(2). If the app generates synthetic audio, image, video, or text, the output is marked in a machine-readable format and detectable as artificially generated or manipulated, using state-of-the-art techniques. C2PA content provenance is a common implementation choice, but the Act does not name C2PA. It requires machine-readable and state-of-the-art, not a specific vendor.
- Deepfake disclosure, Article 50(4). If the app produces a deepfake, the deployer discloses that the content has been artificially generated or manipulated, even without intent to deceive.
- Timing and accessibility, Article 50(5). The information is given in a clear and distinguishable manner at the latest at the time of the first interaction or exposure, and it conforms to accessibility requirements (which ties this rule to the European Accessibility Act in section 4).

The Commission published draft Article 50 implementation guidelines on 8 May 2026, intended to apply from 2 Aug 2026. Sources. [Article 50 text](https://artificialintelligenceact.eu/article/50/), [Commission draft Article 50 guidelines](https://digital-strategy.ec.europa.eu/en/library/draft-guidelines-implementation-transparency-obligations-certain-ai-systems-under-article-50-ai-act).

### 1.3 Article 4 AI literacy (HARD, live since 2 Feb 2025)

Every provider and deployer makes sure the people who build or operate the AI feature have a sufficient level of AI literacy. There is no headcount carve-out, so a solo team is bound too. only the scale of "sufficient" scales down. For a small team the pragmatic evidence is a short written policy, an induction, a refresh schedule, and a completion log. Source. [Article 4](https://artificialintelligenceact.eu/article/4/).

### 1.4 Article 5 prohibited practices (HARD, live since 2 Feb 2025)

Never ship an AI feature that does any of the following. subliminal, manipulative, or deceptive techniques causing serious harm. exploiting vulnerabilities of children, disabled, or socio-economically disadvantaged people. social scoring. purely profiling-based crime prediction. untargeted facial-image scraping. emotion inference in the workplace or education (outside medical or safety). biometric categorisation inferring sensitive traits such as race, religion, or sexual orientation. real-time remote biometric identification in public for law enforcement. Source. [Article 5](https://artificialintelligenceact.eu/article/5/).

### 1.5 Provider versus deployer (scope the obligation correctly)

A developer building an AI feature on a third-party model (OpenAI, Anthropic, Google) through an API is a DEPLOYER by default. The heavy GPAI-model obligations (training-data summaries, model documentation, copyright, systemic risk) fall on the model vendor, not the app. The app becomes a PROVIDER under Article 25 only if it puts its own name or trademark on the system, makes a substantial modification, or puts it into service for a new intended purpose. Because a consumer app is usually the provider of its own assistant UI and the deployer of the model, it carries the visible disclosure duties of Article 50 regardless. Do not over-scope the developer into the model-vendor obligations. Source. [Commission GPAI guidance](https://digital-strategy.ec.europa.eu/en/policies/guidelines-gpai-providers).

### 1.6 Penalties, Article 99

| Violation | Maximum fine, whichever is higher |
|---|---|
| Prohibited practices (Article 5) | 35,000,000 euro or 7 percent of total worldwide annual turnover |
| Other obligations including transparency (Article 50) | 15,000,000 euro or 3 percent of worldwide annual turnover |
| Supplying incorrect or misleading information to authorities | 7,500,000 euro or 1 percent of worldwide annual turnover |

For SMEs and start-ups each fine is capped at the LOWER of the euro amount or the percentage, the reverse of the default. So the penalty anchor for a transparency miss by a small developer is the lower of 15,000,000 euro or 3 percent. Source. [Article 99](https://artificialintelligenceact.eu/article/99/).

### 1.7 The Apple and Google rules that overlap the AI Act

- Apple Guideline 5.1.2(i), effective 13 November 2025. If an app shares personal data with a third-party AI (OpenAI, Anthropic, Gemini, ElevenLabs, and the like), it must clearly disclose the third party, name the AI provider and the data types, and obtain explicit opt-in consent before any transmission. On-device AI (the Apple Foundation Models framework, Core ML) does not trigger this, because data never leaves the device. Sources. [TechCrunch 13 Nov 2025](https://techcrunch.com/2025/11/13/apples-new-app-review-guidelines-clamp-down-on-apps-sharing-personal-data-with-third-party-ai/), [Apple guideline update](https://developer.apple.com/news/?id=ey6d8onl).
- Google Play AI-generated content policy (2025). Developers must clearly inform users when content is AI-generated, and must prevent the generation of offensive or harmful content up front, not only react to reports. Source. [Google Play policy analysis](https://chatboq.com/blogs/google-play-ai-content-policy).

Neither Apple nor Google states "you must comply with the AI Act". Both shipped AI-disclosure and consent policies that a compliant Article 50 implementation largely satisfies, and the reverse. Do not assert that Apple or Google requires AI Act compliance. they do not say that.

## 2. EU Digital Markets Act (DMA)

Applies to apps distributed to users in the EU (NFC rules apply in the EEA). Apps outside the EU keep the standard worldwide App Store terms. On 8 July 2026 the EU General Court upheld Apple's DMA gatekeeper designation for the App Store and iOS.

### 2.1 Distribution channels and notarization (HARD)

There are three EU distribution channels, all still involving Apple. the App Store, Web Distribution (the developer hosts signed binaries on its own registered domain, iOS 17.5 or later), and Alternative App Marketplaces (via the Alternative App Marketplace Entitlement and the MarketplaceKit framework). Notarization is mandatory for every iOS and iPadOS app regardless of channel. Apple runs automated and human notarization checks for accuracy, functionality, safety, security, and privacy, and can revoke an app if malware is found after install. Sources. [Apple DMA and apps in the EU](https://developer.apple.com/support/dma-and-apps-in-the-eu/), [Apple alternative marketplace](https://developer.apple.com/support/alternative-app-marketplace-in-the-eu/).

### 2.2 External purchase links and alternative payments (HARD)

- In June 2025 Apple consolidated the non-IAP options into a single "communication and promotion of offers" entitlement. The entitlement identifier is `com.apple.developer.storekit.external-purchase-link`, and the developer signs the StoreKit External Purchase Link Entitlement Addendum for EU Apps.
- Every external link the user can tap, click, or scan MUST call the `ExternalPurchaseCustomLink` API to show a system-provided disclosure sheet stating the user will transact with the developer and not Apple.
- No mixing on the same storefront. An app cannot offer In-App Purchase and promote external offers within the same app on the same App Store storefront and platform.
- Reporting. external-purchase transactions are reported through the External Purchase Server API monthly, within 15 calendar days of Apple's fiscal-month end.
- Lost capabilities for external purchases. no Report-a-Problem, no Family Sharing, no Ask-to-Buy, no Apple purchase history or subscription management.

Source. [Apple communication and promotion of offers in the EU](https://developer.apple.com/support/communication-and-promotion-of-offers-on-the-app-store-in-the-eu/).

### 2.3 The EU fee model (advisory, re-verify before encoding numbers)

Two fee regimes coexisted as of mid-2026 (the promised single business model announced for 1 January 2026 had NOT been implemented, and Apple remained in discussion with the Commission, so treat all numbers as advisory and re-check Apple's live page).

- Core Technology Fee (CTF). 0.50 euro per first annual install per year above a 1,000,000 first-annual-installs per year threshold, for developers on the Alternative Terms Addendum. Apple estimates fewer than 1 percent of developers pay it. Exemptions include under 1,000,000 installs per year, a small-developer 3-year on-ramp under 10,000,000 euro global revenue, and nonprofit or education or government waivers.
- Core Technology Commission (CTC). 5 percent on digital goods sold through promoted external offers, effective 26 June 2025.
- External Purchase Link fee stack (June 2025 model). an Initial Acquisition Fee of 2 percent, Store Services of 5 percent (Tier 1) or 13 percent (Tier 2), plus the 5 percent Core Technology Commission, totalling roughly 12 percent to 20 percent.

Rule for a compliance tool. warn about the fee model, do not hardcode fee numbers, because the model was unresolved in mid-2026. Sources. [Apple Core Technology Fee](https://developer.apple.com/support/core-technology-fee/), [Apple DMA and apps in the EU](https://developer.apple.com/support/dma-and-apps-in-the-eu/), [RevenueCat June 2025 analysis](https://www.revenuecat.com/blog/growth/apple-eu-dma-update-june-2025/).

### 2.4 Browser engine, NFC, interoperability

Alternative browser engines (non-WebKit) are allowed in the EU via the Alternative Browser Engine Entitlement. A browser choice screen is shown on first Safari launch for EU users on iOS 17.4 or later. Contactless via Host Card Emulation is allowed in the EEA via the HCE entitlement on iOS 17.4 or later, and a third-party contactless app can be set as default over Apple Pay. All DMA entitlements are scoped to EU or EEA storefronts only. Source. [Apple DMA and apps in the EU](https://developer.apple.com/support/dma-and-apps-in-the-eu/).

### 2.5 The enforcement backdrop

The European Commission fined Apple 500,000,000 euro on 23 April 2025 for breaching the DMA anti-steering obligation (Article 5(4)). Apple's June 2025 EU fee and entitlement restructuring was its direct response. Apple appealed on 7 July 2025 and the appeal is pending. Sources. [Commission decision](https://digital-strategy.ec.europa.eu/en/news/commission-finds-apple-and-meta-breach-digital-markets-act), [CNBC appeal](https://www.cnbc.com/2025/07/07/apple-appeal-eu-fine-app-store.html).

### 2.6 What a compliance tool must CHECK for an EU app using DMA entitlements

- The external-purchase entitlement identifier is declared when the app uses external offers.
- Every external link the user can tap, click, or scan calls the `ExternalPurchaseCustomLink` disclosure sheet.
- The app does NOT ship both StoreKit IAP and external-offer links on the same EU storefront.
- External Purchase Server API reporting is wired (monthly, 15-day window).
- Any non-App-Store build passed notarization.
- A marketplace app uses MarketplaceKit, installs only from its own domain, and runs moderation, anti-fraud, and refund handling.
- Entitlement-using code is gated to the minimum OS (iOS and iPadOS 17.4, macOS 14.4, visionOS 1.2, watchOS 10.4).
- Browser-engine and HCE features carry their entitlements and are region-gated to EU or EEA.

## 3. EU Digital Services Act, trader status (HARD)

The DSA (Articles 30 and 31) requires the App Store and Google Play to verify and display trader contact and identity information for traders distributing apps in the EU.

- Apple enforced this from 17 February 2025. apps whose developers had not provided and verified trader status were removed from the EU App Store on that date. Every developer must declare a status even when not distributing in the EU.
- What a trader submits (App Store Connect, Business, then Digital Services Act). for an organization, the address (from D-U-N-S), phone number, and email. for an individual, an address or P.O. box, phone number, and email. all traders also provide payment-account details and certify EU-law compliance. Verification is two-factor (email plus phone SMS) with documentation upload.
- Publication. once verified, Apple publishes the trader's address, phone, and email on the App Store product page across all 27 EU territories.
- Non-trader declaration. if the developer declares "not a trader", EU consumers are notified that consumer-protection law does not apply to contracts with the developer. Confirm that is intended.
- Google Play carries the same DSA obligation. Google historically enforced with reduced discoverability rather than immediate removal. the exact Google hard deadline is unverified against a canonical Google page.

What a compliance tool must CHECK. trader versus non-trader declaration completed and verified before EU distribution. address, phone, email present and 2FA-verified. a missing declaration flagged as an EU-storefront removal risk. Sources. [Apple manage DSA trader requirements](https://developer.apple.com/help/app-store-connect/manage-compliance-information/manage-european-union-digital-services-act-trader-requirements/), [Apple upcoming requirement 02172025a](https://developer.apple.com/news/upcoming-requirements/?id=02172025a).

## 4. European Accessibility Act (EAA), Directive (EU) 2019/882 (HARD, NEW gap)

The EAA became applicable on 28 June 2025. This is the largest gap the base playbook did not cover.

### 4.1 Scope

In scope are consumer products and services delivered through websites AND mobile apps, including e-commerce, banking and financial services, e-books and e-readers, transport and travel booking, telecom services, and audiovisual media access. Any organization based in the EU, or offering these apps or services to EU consumers, is covered, so the reach is extraterritorial. Sources. [European Commission EAA](https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/disability/union-equality-strategy-rights-persons-disabilities-2021-2030/european-accessibility-act_en), [Level Access EAA](https://www.levelaccess.com/blog/eu-accessibility-requirements-and-eaa-compliance/).

### 4.2 Microenterprise exemption

A microenterprise with fewer than 10 employees AND annual turnover or balance-sheet total not exceeding 2,000,000 euro is exempt, but the exemption applies to services only, not products, has no grace period once thresholds are crossed, and does not apply if the business received accessibility funding. Source. [Greenberg Traurig EAA](https://www.gtlaw.com/en/insights/2025/7/european-accessibility-act-compliance-what-businesses-in-the-eu-market-need-to-know).

### 4.3 The technical bar for apps

- The EAA is met through the harmonised standard EN 301 549. WCAG is the underlying guidelines set.
- EN 301 549 version 3.2.1 is built on WCAG 2.1 Level AA and adds roughly 64 requirements beyond WCAG, in particular Chapter 11 for non-web software and mobile apps. A WCAG-only audit does NOT satisfy EN 301 549 Chapter 11.
- EN 301 549 version 4.1.1, expected in 2026, moves to WCAG 2.2.
- An accessibility statement is required (EN 301 549 Annex B and C). A missing or inaccurate statement can be a separate penalty in some Member States.

Sources. [Deque EN 301 549](https://www.deque.com/en-301-549-compliance/), [EN 301 549 Chapter 11 for mobile apps](https://auditsu.com/resources/en-301-549-chapter-11-mobile-apps).

### 4.4 Penalties

Penalties are set per Member State. Germany, administrative fines up to 100,000 euro plus corrective measures or market withdrawal (verified, law-firm source). Other national figures cited by accessibility vendors (France around 25,000 euro per year for a missing statement, Ireland around 60,000 euro, Sweden around 900,000 euro) are unverified against national statutes and are marked so in section 9.

### 4.5 What a compliance tool must CHECK for an EU app (maps to Apple accessibility)

- VoiceOver labels and traits on every interactive element (accessibilityLabel, accessibilityTraits, accessibilityHint). every feature operable with VoiceOver, an external keyboard, and switch control.
- Dynamic Type. system font scaling supported, no fixed layout that breaks at larger text.
- Color contrast at WCAG 2.1 AA (4.5 to 1 for text, 3 to 1 for large text and UI), no information carried by color alone.
- Reduce Motion honored, logical focus order, adequate touch-target size.
- An accessibility statement published and reachable.
- A flag that WCAG-only coverage leaves an EN 301 549 Chapter 11 gap.

These map onto the Apple accessibility discipline the setup already carries (Dynamic Type, VoiceOver, contrast, Reduce Motion). The difference the EAA adds is that this is now a legal requirement with fines, not only a quality bar.

## 5. Adjacent EU rules to track (dates, so the audit stays current)

- EU Data Act, Regulation (EU) 2023/2854. core obligations from 12 September 2025, access-by-design from 12 September 2026. Relevant when an app interacts with a connected product (wearables, smart devices).
- Cyber Resilience Act, Regulation (EU) 2024/2847. reporting obligations from 11 September 2026, main obligations from 11 December 2027. Relevant when the app ships as a standalone product with digital elements (security-by-design, vulnerability handling).
- DSA protection of minors and age verification. Commission Guidelines on Protection of Minors published 14 July 2025. an EU age-verification blueprint became feature-ready 15 April 2026, with Member States urged to roll out by 31 December 2026.
- GDPR children's data. EDPB Statement 1/2025 on age assurance (adopted 11 February 2025) sets ten principles, and age assurance must still respect data minimisation and purpose limitation.

### 5.1 EU e-Evidence Package (Regulation (EU) 2023/1543 & Directive (EU) 2023/1544) (HARD, NEW)

The EU e-Evidence Package fundamentally reshapes cross-border law enforcement access to electronic data by allowing judicial authorities of one Member State to directly compel service providers in another Member State to preserve or produce data, bypassing traditional mutual legal assistance frameworks.

- **Scope:** Applies to electronic communications service providers (instant messaging, VoIP, email), internet domain registries, and other information society services that facilitate intra-user communication (such as online marketplaces) or store/process data on behalf of users (such as cloud hosting and SaaS applications). This applies to any provider offering services in the EU, regardless of where they are headquartered.
- **Key Obligations:**
  - **Designation/Appointment of Addressees:** Under Directive (EU) 2023/1544, EU-established service providers must designate an establishment, and non-EU-established service providers must appoint a legal representative in the EU, to receive and execute European Production and Preservation Orders.
  - **Notification Requirement:** Providers must notify the designated central authority of their representative's details and languages. The notification deadline is **18 August 2026**, or within six months of commencing services in the EU.
  - **European Production Order Execution:** Compels providers to produce electronic evidence. The default compliance window is **10 days**, but in critical emergency situations, providers MUST produce the requested data within **8 hours**.
  - **European Preservation Order Execution:** Compels providers to preserve electronic evidence for **60 days** to prevent deletion.
- **Penalties:** Joint and several liability applies to the provider and their designated legal representative. Non-compliance can result in administrative fines of up to **2% of the provider's total annual global turnover** under national implementing legislation.
- **Sources:** [Regulation (EU) 2023/1543 (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2023/1543/oj), [Directive (EU) 2023/1544 (EUR-Lex)](https://eur-lex.europa.eu/eli/dir/2023/1544/oj), [Bird & Bird EU e-Evidence Package Guide](https://www.twobirds.com/en/insights/2026/germany/e-evidence-richtlinie-umsetzungsfrist-abgelaufen--implementierungsstatus-und-handlungsbedarf).

### 5.2 EU Contract Withdrawal Button (Distance Marketing of Financial Services Directive (EU) 2023/2673) (HARD, NEW)

The Distance Marketing of Financial Services Directive introduces amendments to the Consumer Rights Directive (Directive 2011/83/EU), ensuring that consumers can easily exercise their statutory right of withdrawal from online contracts.

- **Scope:** Applies to all distance contracts concluded via an online user interface, including websites and mobile applications, that offer retail financial services or other consumer contracts and subscriptions.
- **Key Obligations:**
  - **Withdrawal Button/Function:** Service providers must ensure that where a contract is concluded online, consumers can withdraw from it via a prominent, dedicated, and easily accessible "withdrawal button" or "withdrawal function" on the online interface.
  - **Frictionless Experience:** The cancellation/withdrawal path must be direct and cannot be buried behind multiple steps, contact forms, phone calls, or administrative obstacles. It must be at least as simple as the contract sign-up/subscription process.
  - **Information Requirements:** The interface must clearly state the 14-day statutory withdrawal period and outline the consequences of withdrawal.
- **Timelines:** Member States are expected to transpose and implement these requirements by **19 June 2026**.
- **Sources:** [Directive (EU) 2023/2673 (EUR-Lex)](https://eur-lex.europa.eu/eli/dir/2023/2673/oj), [Reed Smith 2026 EU Regulations Overview](https://www.reedsmith.com/our-insights/blogs/viewpoints/102lyiv/2026-update-eu-regulations-for-tech-and-online-businesses/).

Sources. [Morgan Lewis Data Act](https://www.morganlewis.com/blogs/sourcingatmorganlewis/2025/09/eu-data-act-begins-september-12-impacting-cloud-services-connected-products-and-other-data-industries), [Commission Cyber Resilience Act](https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act), [Commission age verification](https://digital-strategy.ec.europa.eu/en/policies/eu-age-verification).

## 6. Apple platform changes 2025 and 2026 (beyond the base map)

These are Apple App Review and App Store Connect changes, layered on top of the EU legal rules.

- New age-rating system, HARD deadline 31 January 2026. Apple added 13 plus, 16 plus, and 18 plus tiers on top of 4 plus and 9 plus. Every app must answer the updated age-rating questionnaire by 31 January 2026 or be blocked from submitting updates. New questionnaire items cover user-generated content, messaging and chat, friend or follower systems, livestreaming, content-creation tools, and the presence of advertising, plus safeguards such as moderation, filtering, reporting, and parental controls. The declared capabilities must match real app behaviour. Sources. [Apple updated age ratings](https://developer.apple.com/news/?id=ks775ehf), [Apple upcoming requirement 07242025a](https://developer.apple.com/news/upcoming-requirements/?id=07242025a).
- Declared Age Range API, new in iOS 26. a privacy-preserving age-band API returning bands (under 13, 13 to 15, 16 to 17, over 18), not a birthdate, plus whether parental controls are on. Rolled out globally in February 2026 to meet child-safety laws in regions including Brazil, Australia, Singapore, Utah, Louisiana, and Texas. Sources. [Apple Declared Age Range](https://developer.apple.com/documentation/declaredagerange/), [Apple age assurance](https://developer.apple.com/support/age-assurance/).
- Guideline 5.1.2(i), third-party-AI data-sharing consent (13 November 2025). see section 1.7.
- Guideline 1.2.1(a), creator apps. must let users flag content exceeding the app's age rating and use a verified or declared-age mechanism to limit underage access.
- Guideline 4.7 and 4.7.2 and 4.7.4 and 4.7.5, HTML5 and JavaScript mini apps and mini games. now fully in scope. cannot expose native APIs without permission, must provide a verified or declared-age restriction, and must provide a full index of all mini apps with metadata.
- Guideline 4.1(c), anti-clone. cannot use another developer's icon, brand, or product name in your icon or name without approval.
- Guideline 5.1.1(ix), crypto exchanges added to highly regulated fields (need licensing and geo-restriction).
- Guideline 5.1.1(v), account deletion. unchanged since 30 June 2022 but still a top rejection cause. genuine in-app deletion, not deactivation or a web form.
- Xcode 26 and iOS 26 SDK, HARD deadline 28 April 2026. new uploads must be built with Xcode 26 and the iOS 26 (and matching platform 26) SDK.
- App Tracking Transparency. the rule is unchanged, but France's competition authority fined Apple 150,000,000 euro in March 2025 over the ATT implementation, so the ATT prompt and the tracking-domain declaration remain a live audit item. Sources. [Apple updated App Review Guidelines 13 Nov 2025](https://developer.apple.com/news/?id=ey6d8onl), [Apple upcoming requirements](https://developer.apple.com/news/upcoming-requirements/).

## 7. Consolidated audit checklist (HARD gates for an EU app)

| Gate | Verify | Effective |
|---|---|---|
| AI interaction disclosure | An in-app "you are talking to AI" notice at or before first interaction | 2 Aug 2026 |
| AI content marking | Machine-readable plus visible label on generated media and text | 2 Aug 2026 |
| AI literacy record | A short written policy, induction, and completion log | live since 2 Feb 2025 |
| No prohibited AI practice | No manipulation, no banned emotion inference, no biometric categorisation | live since 2 Feb 2025 |
| Third-party-AI consent (Apple 5.1.2(i)) | A consent modal naming the AI provider and data types, shown before data leaves the device | live since 13 Nov 2025 |
| DSA trader status | Trader or non-trader declared and verified before EU distribution | live since 17 Feb 2025 |
| Age-rating questionnaire | Answered for every app, capabilities match behaviour | deadline 31 Jan 2026 |
| European Accessibility Act | EN 301 549 and WCAG 2.1 AA met, accessibility statement published | live since 28 Jun 2025 |
| DMA external purchase | Entitlement declared, disclosure sheet wired, no IAP mix, reporting wired | live |
| Notarization | Any non-App-Store build notarized | live |
| Xcode 26 SDK | Build with Xcode 26 and the iOS 26 SDK | deadline 28 Apr 2026 |
| EU e-Evidence Package | Legal representative designated and 8-hour emergency response protocol established | 18 Aug 2026 |
| EU Contract Withdrawal | Prominent, Frictionless contract withdrawal button on user interface | 19 Jun 2026 |

## 8. Sources

The inline links above are the primary and secondary sources. The authoritative pages to re-check for currency are the Apple developer support pages (DMA, external offers, Core Technology Fee, DSA trader, age ratings, upcoming requirements), the EU Commission digital-strategy pages, EUR-Lex for the regulation texts, and artificialintelligenceact.eu for the AI Act article texts.

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

## 9. Verification and honesty note

Confidence is high on the core dates and the sourced facts. Confirmed against primary or law-firm sources. the AI Act timeline and Article 50 and Article 99 figures, the DMA 500,000,000 euro fine dated 23 April 2025, Apple's DSA trader fields and the 17 February 2025 removal, the EAA date of 28 June 2025 and EN 301 549 and WCAG 2.1 AA, and the Apple 2025-2026 guideline and deadline dates.

Marked unverified, confirm before quoting externally. the per-Member-State EAA penalty figures for France, Ireland, and Sweden (vendor-blog summaries, not national statutes). Google Play's exact DSA trader hard deadline. the exact post-January-2026 Apple EU fee percentages (the single-business-model unification announced for 1 January 2026 was not implemented as of mid-2026, so all fee numbers here are the June 2025 model and are advisory). the reported 60-day compliance window on the 500,000,000 euro ruling. and the reported 22 July 2026 signatory deadline for the AI-generated-content Code of Practice (conflicting sources). C2PA is an implementation convention for Article 50 marking, not a legal mandate.

Because these dates and figures move, an audit tool should treat this document as advisory on numbers and HARD on the existence and direction of each obligation, and re-verify any figure against the cited primary source before quoting it externally.
