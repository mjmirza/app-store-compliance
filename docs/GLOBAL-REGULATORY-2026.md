# Global Regulatory Hard Rules (2026). USA and Worldwide

This document is the non-EU legal layer for App Store and Google Play compliance. It is the companion to [EU-REGULATORY-2026.md](EU-REGULATORY-2026.md). The same framing holds. Store compliance is not the same as legal compliance. Passing App Review does not make an app compliant with US federal or state law, or with the laws of the UK, Australia, Brazil, Canada, South Korea, India, Singapore, Japan, or China. The store enforces a subset, a regulator enforces the rest, and for an app that reaches users in a market both must be satisfied.

Every item is a HARD rule for any app that reaches users in the named market. Each carries a date and a source. Apple-backed items cite developer.apple.com so the reference stays Apple-anchored. Many US and global dates are under active litigation or legislative delay, so treat each effective date as the statutory date subject to injunction or amendment, and re-verify against the cited source before relying on it. Items that could not be confirmed against a primary source are labelled unverified in the last section.

## 1. Apple's cross-region age-assurance spine (Apple-backed, check this first)

Several national and US-state laws are operated through Apple's own age-assurance machinery, so an audit checks this layer first.

- Declared Age Range API. It returns a user's age band, not a birthdate, plus a signal for how age was confirmed (`governmentIDChecked`, `paymentChecked`, `selfDeclared`, `guardianDeclared`). The entitlement is `com.apple.developer.declared-age-range`. Version map. iOS and iPadOS 26 add the base self-declared and guardian-declared range. 26.2 adds verification methods and PermissionKit. 26.4 adds regulatory-requirement signals and a parental-acknowledgement sheet for a major app update. Full features build against the iOS 26.2 SDK with Xcode 26.2 or later. The API is available worldwide. Sources. [Apple age assurance](https://developer.apple.com/support/age-assurance/), [Apple Declared Age Range](https://developer.apple.com/documentation/declaredagerange/).
- Apple names no specific law on the age-assurance page. it says "in certain regions, where legally required" and "consult your legal counsel". The country and state list lives in Apple's dated news posts, not the evergreen page. An audit must not read the region list off the support page.
- The developer owns the restriction and the consent handling. Until a parent consents, the child is prevented from accessing the gated update or feature. Consent withdrawal arrives through App Store Server Notifications as the `RESCIND_CONSENT` value, and a major app change re-requests consent through PermissionKit (`SignificantAppUpdateTopic`). Source. [Apple age assurance](https://developer.apple.com/support/age-assurance/).
- 18-plus download block. from 24 February 2026 Apple blocks users in Brazil, Australia, and Singapore from downloading apps rated 18-plus unless they are confirmed to be adults through reasonable methods. Apple states developers may have separate obligations to independently confirm adulthood. Source. [Apple region age requirements](https://developer.apple.com/news/?id=f5zj08ey).

Per-region storefront dates Apple has published.

| Region | Apple date | Mechanic | Law Apple names |
|---|---|---|---|
| Texas | 4 June 2026 (after an injunction was stayed) | Age assurance plus parent consent for under-18 on downloads, purchases, and major changes. bands under 13, 13 to 15, 16 to 17, over 18 | SB 2420 |
| Utah | 6 May 2026 (new Apple Accounts) | Age category via Declared Age Range API, consent and revocation | not named |
| Louisiana | 1 July 2026 (new Apple Accounts) | Same tool set as Utah | not named |
| Brazil | 24 February 2026 | 18-plus download block. loot-box apps auto-rated 18-plus | not named |
| Australia | 24 February 2026 | 18-plus download block | not named |
| Singapore | 24 February 2026 | 18-plus download block | not named |

Sources. [Apple region age requirements](https://developer.apple.com/news/?id=f5zj08ey), [Apple Texas SB 2420](https://developer.apple.com/news/?id=btkirlj8).

## 2. United States

### 2.1 COPPA and the amended COPPA Rule (FTC)

- COPPA covers operators of services directed to children under 13, and general-audience services with actual knowledge they collect data from an under-13 child. Asking date of birth and receiving an under-13 answer is actual knowledge. Anchor is 16 CFR Part 312. Source. [FTC COPPA FAQ](https://www.ftc.gov/business-guidance/resources/complying-coppa-frequently-asked-questions).
- The amended Rule. Federal Register 22 April 2025, citation 90 FR 16918, effective 23 June 2025, general compliance date 22 April 2026. Source. [Federal Register 2025-05904](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule).
- What changed, each a testable duty.
  - Personal information now adds biometric identifiers (fingerprint, retina or iris, genetic or DNA, voiceprint, gait, facial template) and government identifiers beyond the SSN.
  - Separate opt-in consent for third-party disclosure and targeted advertising, and access cannot be conditioned on it.
  - Data-retention limits with a written retention policy, no indefinite retention (312.10).
  - A written information-security program with a coordinator and an annual risk assessment (312.8).
  - New verifiable parental consent methods including knowledge-based authentication and a face-match to a government photo ID.
  - Penalty up to 53,088 dollars per violation (2025 inflation-adjusted).
  Sources. [FTC final COPPA changes](https://www.ftc.gov/news-events/news/press-releases/2025/01/ftc-finalizes-changes-childrens-privacy-rule-limiting-companies-ability-monetize-kids-data), [Gibson Dunn COPPA analysis](https://www.gibsondunn.com/ftc-updates-to-coppa-rule-impose-new-compliance-obligations-for-online-services-that-collect-data-from-children/).
- Apple hook. Guideline 5.1.4 names COPPA, and Guideline 1.3 gates Kids-Category apps behind a parental gate with no third-party PII sharing. Source. [Apple App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/).

### 2.2 US state App Store Accountability Acts (ASAA)

These put duties on both the store and the developer, separate from broader social-media minor laws. Four states as of mid-2026, all under active litigation or delay.

| State | Bill | Signed | Effective (subject to litigation) |
|---|---|---|---|
| Utah | SB 142 | 26 March 2025 | store and developer duties from 6 May 2026, some operational parts delayed to 6 May 2027, private right of action from 31 December 2026 |
| Texas | SB 2420 | 2025 | statutory 1 January 2026, enjoined 23 December 2025, injunction stayed 28 May 2026 so now in effect while litigation continues |
| Louisiana | HB 570 | 30 June 2025 | delayed one year to 1 July 2027 |
| Alabama | HB 161 | 9 March 2026 | 2027, exact date unverified |

Common developer duties. request and receive an age category from the store. confirm whether verifiable parental consent exists for a minor account before use. assign an accurate age and suitability rating. re-request consent on a major change. limit use of age and consent data to compliance and delete it after verification (Texas is explicit on deletion). Sources. [Utah SB 142](https://le.utah.gov/~2025/bills/static/SB0142.html), [FPF comparison of the ASAAs](https://fpf.org/blog/comparing-enacted-app-store-accountability-acts/), [Wiley ASAA developments](https://www.wiley.law/alert-Key-Developments-With-State-App-Store-Accountability-Acts-as-Texas-Act-Takes-Effect).

Apple discrepancy to flag. Apple's storefront date for Louisiana is 1 July 2026, while the statute was delayed to 1 July 2027. An audit flags the gap rather than assuming either date. Sources. [Apple region age requirements](https://developer.apple.com/news/?id=f5zj08ey), [Alston on the Louisiana delay](https://www.alstonprivacy.com/louisiana-delays-app-store-accountability-effective-date-to-july-2027/).

Note. Texas HB 18 (the SCOPE Act, effective 1 September 2024) is a separate Texas law that regulates digital service providers directly, distinct from the ASAA.

### 2.3 US external purchase links and anti-steering (Epic v. Apple)

- 30 April 2025. the court found Apple in civil contempt and enjoined it from charging a commission on out-of-app purchases or restricting the design of external links. 11 December 2025. the Ninth Circuit upheld the contempt finding but narrowed the remedy. Apple may charge only costs genuinely necessary to coordinate the hand-off, not a flat percentage. The Supreme Court granted cert in mid-2026 with argument scheduled October 2026, so the exact US commission is unsettled. Sources. [Ninth Circuit opinion](https://cdn.ca9.uscourts.gov/datastore/opinions/2025/12/11/25-2935.pdf), [SCOTUS cert reporting](https://9to5mac.com/2026/06/30/supreme-court-agrees-to-hear-apple-appeal-over-epic-games-ruling/).
- Apple-backed rule. from 1 May 2025 Apple updated Guidelines 3.1.1, 3.1.1(a), 3.1.3, and 3.1.3(a) for the US decision. On the US storefront an app may include external-purchase links or buttons to the developer's own website, with no entitlement and no mandatory disclosure sheet. It does not permit alternative in-app payment. the transaction happens on the web. Outside the US the prohibition still applies and the external-purchase-link entitlement is still required. Sources. [Apple guideline update 1 May 2025](https://developer.apple.com/news/?id=9txfddzf), [Apple App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/).
- An audit treats the US commission question as unresolved, not as a fixed zero.

### 2.4 California (CCPA and CPRA, CPPA 2026 regulations, AADC)

- CCPA and CPRA apply to a for-profit business doing business in California over a revenue or volume threshold. Duties. a privacy policy and a notice at collection, rights to know, delete, and correct, an opt-out of sale and sharing through a "Do Not Sell or Share" mechanism that honors Global Privacy Control, a "Limit the Use of My Sensitive Personal Information" control, and non-discrimination. Source. [California AG CCPA](https://oag.ca.gov/privacy/ccpa).
- The CPPA finalised 2026 regulations, effective 1 January 2026. Automated-decision-making duties for high-impact decisions begin 1 April 2027, and cybersecurity audits phase in from 1 April 2028 by revenue tier. Source. [CPPA regulations](https://cppa.ca.gov/regulations/ccpa_updates.html).
- The California Age-Appropriate Design Code (AB 2273) is only partly enforceable. On 12 March 2026 the Ninth Circuit narrowed the injunction. age-estimation and coverage parts may proceed, but the data-use restriction and the DPIA requirement stay enjoined. Treat the vague data-use and DPIA duties as not required for now. Source. [Ninth Circuit AADC opinion](https://cdn.ca9.uscourts.gov/datastore/opinions/2026/03/12/25-2366.pdf).
- California SB 976 (social-media addiction) applies only to social-feed apps for minors, not a general app. its age-verification part starts 1 January 2027. Source. [California AG SB 976](https://oag.ca.gov/sb976).

### 2.5 Other US state privacy laws and Global Privacy Control

Broad state privacy laws in effect or arriving through 2025 and 2026.

| State | Law | Effective | Honor GPC |
|---|---|---|---|
| Virginia | VCDPA | 1 Jan 2023 | no |
| Colorado | CPA | 1 Jul 2023 | yes |
| Connecticut | CTDPA | 1 Jul 2023 | yes |
| Texas | TDPSA | 1 Jul 2024 (GPC from 1 Jan 2025) | yes |
| Oregon | OCPA | 1 Jul 2024 (opt-out signal 1 Jan 2026) | yes |
| Delaware | DPDPA | 1 Jan 2025 | yes |
| New Jersey | SB 332 | 15 Jan 2025 | yes |
| Minnesota | MCDPA | 31 Jul 2025 | yes |
| Maryland | MODPA | 1 Oct 2025 (processing after 1 Apr 2026) | yes |
| Indiana | ICDPA | 1 Jan 2026 | no |
| Kentucky | KCDPA | 1 Jan 2026 | no |
| Rhode Island | RIDTPPA | 1 Jan 2026 | no |

Common app duties. a privacy notice, an opt-out of targeted advertising, sale, and profiling, opt-in consent for sensitive data in the Virginia-model states, and a data protection assessment for high-risk processing. Maryland is stricter. data minimisation to what is reasonably necessary, and no sale of sensitive data at all. Global Privacy Control arrives in an embedded webview as the `Sec-GPC` header. a native app has no browser signal, so it offers an equivalent in-app opt-out and honors any platform-level signal, suppressing sale and targeted-ad data flows. Roughly a dozen states require honoring it. Sources. [IAPP US state privacy tracker](https://iapp.org/resources/article/us-state-privacy-legislation-tracker), [Global Privacy Control](https://globalprivacycontrol.org/).

### 2.6 US health data and biometric law

- Most direct-to-consumer health apps are not covered by HIPAA. HIPAA applies only when the developer is a covered entity or a business associate under a BAA. Otherwise the FTC Health Breach Notification Rule applies. the 2024 final rule covers non-HIPAA health apps, treats an unauthorized disclosure (for example sharing health data with an ad vendor) as a breach, and requires notice within 60 days. Penalty up to 53,088 dollars per violation. Sources. [HHS health apps](https://www.hhs.gov/hipaa/for-professionals/special-topics/health-apps/index.html), [FTC Health Breach Notification Rule](https://www.ftc.gov/news-events/news/press-releases/2024/04/ftc-finalizes-changes-health-breach-notification-rule).
- Illinois BIPA. written notice and a written release before collecting a biometric identifier, a public retention schedule, destruction within 3 years, no sale, and a private right of action with statutory damages of 1,000 dollars per negligent and 5,000 dollars per intentional violation. SB 2979 (effective 2 August 2024) made repeated collection of the same biometric a single violation. Texas CUBI and Washington My Health My Data Act add further consent and destruction duties. Sources. [BIPA overview](https://www.recordinglaw.com/us-laws/data-privacy-laws/bipa/), [Washington MHMDA](https://app.leg.wa.gov/RCW/default.aspx?cite=19.373&full=true).

## 3. Other global markets

### 3.1 United Kingdom

- Online Safety Act 2023. age-assurance duties in force from 25 July 2025, enforced by Ofcom. Highly Effective Age Assurance methods include facial age estimation, open banking, digital ID, and credit-card checks. self-declaration alone is not highly effective. Penalty up to 18 million pounds or 10 percent of global turnover, plus blocking orders. As of early 2026 Ofcom had opened investigations into more than 90 services. Sources. [Ofcom age checks](https://www.ofcom.org.uk/online-safety/protecting-children/age-checks-to-protect-children-online).
- ICO Age Appropriate Design Code (Children's Code), in force since September 2021. it applies to any service likely to be accessed by a UK child under 18, even a general-audience one. Checkable defaults. high privacy by default, data minimisation, geolocation off by default, profiling off by default, and a DPIA. Source. [ICO Children's Code](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/introduction-to-the-childrens-code/).

### 3.2 Australia

- Online Safety Amendment (Social Media Minimum Age) Act 2024, in force 10 December 2025. an age-restricted social media platform takes reasonable steps to stop under-16s holding an account. Named platforms include Facebook, Instagram, Snapchat, TikTok, X, YouTube, Reddit. The eSafety guidance expects a waterfall of methods, and self-declaration cannot be the sole method. Age-assurance data is ringfenced and destroyed after use. Penalty up to 49.5 million Australian dollars. Sources. [eSafety social media age restrictions](https://www.esafety.gov.au/about-us/industry-regulation/social-media-age-restrictions).
- Apple blocks 18-plus downloads in Australia from 24 February 2026.

### 3.3 Brazil

- Digital ECA (Law 15,211/2025), enforceable from 17 March 2026, on top of the LGPD and enforced by the ANPD. Accepted age-verification methods include document verification, facial age estimation, facial matching, and a CPF database check. a self-declaration checkbox no longer counts. The ANPD 2026 enforcement plan prioritises app stores and operating systems as gatekeepers. Penalty up to 50 million reais per violation or 10 percent of Brazilian revenue. Sources. [Digital ECA timeline](https://inplp.com/latest-news/article/the-digital-eca-brazils-new-age-verification-framework-and-enforcement-timeline/).
- Apple blocks 18-plus downloads in Brazil from 24 February 2026, and loot-box apps auto-rate 18-plus on the Brazil storefront.

### 3.4 Canada

- PIPEDA is the federal baseline. informed consent, purpose limitation, and breach reporting. Quebec Law 25 is stricter. explicit opt-in consent for tracking and profiling, a named privacy officer, privacy impact assessments, and breach notification. Penalty up to the greater of 25 million Canadian dollars or 4 percent of global turnover. Sources. [Quebec Law 25](https://www.cookieyes.com/blog/quebec-law-25/).

### 3.5 South Korea

- PIPA is the baseline. a rewrite reported to take effect in 2026 raises the maximum penalty toward 10 percent of turnover and adds CEO accountability. exact date unverified.
- The Telecommunications Business Act mandates alternative in-app payment. Apple's implementation is Apple-backed and specific. a 26 percent commission on the price the user pays, gross of VAT, approved payment providers only (KCP, Inicis, Toss, NICE), the entitlement `com.apple.developer.storekit.external-purchase` with `SKExternalPurchase = "KR"`, a Korea-only binary, no co-mingling with Apple in-app purchase, a native (non-webview) payment, an external-purchase modal sheet shown first, monthly sales reporting within 15 days, and remittance within 45 days. Source. [Apple StoreKit external entitlement Korea](https://developer.apple.com/support/storekit-external-entitlement-kr/).

### 3.6 India

- Digital Personal Data Protection Act 2023 with the DPDP Rules 2025 notified 13 November 2025. the consent and children's rules are enforceable from 13 May 2027. Everyone under 18 is a child, so verifiable parental consent through a government-backed system such as DigiLocker is required before processing any under-18 data, and behavioral tracking and targeted advertising to children are prohibited. Source. [India DPDP Rules 2025](https://www.bassberry.com/news/indias-data-privacy-rules-what-your-business-needs-to-know/).

### 3.7 Singapore

- PDPA is the baseline. a data protection officer, breach notification within 3 days, and consent. The IMDA Code of Practice for Online Safety for App Distribution Services required app-store age assurance from 1 April 2026. app stores screen and stop users estimated under 18 from downloading age-inappropriate apps, and age-assurance data is not retained after the purpose is met. Source. [IMDA app-store age assurance](https://www.twobirds.com/en/insights/2026/singapore/app-stores-in-singapore-required-to-implement-age-assurance-measures).
- Apple blocks 18-plus downloads in Singapore from 24 February 2026.

### 3.8 Japan

- APPI is the baseline. an amendment bill was submitted to the Diet in 2026, with full effect expected by 2028. A consent-based cross-border transfer discloses the recipient country, that country's data-protection regime, and the recipient's protection measures, and the law reaches foreign operators serving people in Japan. Source. [DLA Piper Japan transfer](https://www.dlapiperdataprotection.com/?t=transfer&c=JP).

### 3.9 China

- Mobile App Filing with the MIIT (an extension of ICP filing) is mandatory. new apps since 1 September 2023, existing apps by 31 March 2024, or removal. Only a Chinese entity can file, so a foreign developer partners with a local company. PIPL privacy, data localisation, real-name verification, content moderation, and a Banhao license for games also apply. Sources. [China app filing guide](https://appinchina.co/blog/the-complete-guide-to-chinas-mobile-app-filing/).

## 4. Alternative app stores (distinct requirements only)

- Huawei AppGallery and Samsung Galaxy Store. for the Singapore age-assurance rule from 1 April 2026 both use credit-card data as the method. Huawei mainland-China distribution needs ICP filing, a local entity, and simplified-Chinese metadata. Source. [App store age-assurance methods](https://www.biometricupdate.com/202604/app-stores-reveal-age-verification-estimation-methods-to-meet-singapore-requirements).
- Amazon Appstore for Android was discontinued on 20 August 2025, so it is no longer a distribution target for new Android work. Source. [Amazon Appstore discontinued](https://www.forasoft.com/blog/article/distribute-android-apps-beyond-google-play).

## 5. Consolidated global audit checklist (HARD gates)

- COPPA. a child-directed app or one where a DOB reveals under-13 uses verifiable parental consent before collection, a separate opt-in for third-party or ad disclosure, a written retention policy, a written security program, and lists biometric identifiers in its data inventory. Compliance date 22 April 2026.
- US state ASAA. the app requests an age category from the store, confirms parental consent for a minor account, re-requests consent on a major change, and deletes age data after verification. wired through the Declared Age Range API for the flagged states.
- Age rating. set to 4-plus, 9-plus, 13-plus, 16-plus, or 18-plus, never Unrated, questionnaire re-answered under the new bands by 31 January 2026.
- US external purchase. US-storefront external links are allowed with no entitlement and no disclosure sheet, no in-app alternative payment, and the commission question is treated as unsettled.
- Account deletion (Guideline 5.1.1(v)) present, `PrivacyInfo.xcprivacy` and SDK manifests present, App Privacy details match runtime.
- California and state privacy. a privacy policy, notice at collection, know, delete, correct, "Do Not Sell or Share", "Limit Use of Sensitive PI", and honoring Global Privacy Control (`Sec-GPC` in a webview, an equivalent native opt-out).
- Biometric. written or e-signed consent before capture, a public retention and destruction schedule (BIPA 3 years, CUBI 1 year), and no sale.
- Health app. the HIPAA gate, else the FTC Health Breach Notification Rule with a 60-day breach notice, plus a distinct Washington MHMDA policy and consent where it applies.
- 18-plus gating. handled for Brazil, Australia, and Singapore for the 24 February 2026 Apple block.
- UK. Highly Effective Age Assurance for harmful content, a Children's-Code DPIA, and high-privacy, geolocation-off, profiling-off defaults for a likely-child service.
- Australia. a waterfall age assurance for an age-restricted social media platform, with ringfenced and destroyed age data.
- Brazil, India. document, biometric, or government-database age verification (not a checkbox), and verifiable parental consent for a minor.
- South Korea. a Korea-only binary with an approved payment provider, no co-mingled in-app purchase, the modal sheet, and the 26 percent reporting, if alternative billing is used.
- China. MIIT app filing and a local entity, plus PIPL, real-name, and a Banhao license for a game.

## 6. Sources and verification note

Apple facts cite developer.apple.com and apple.com. US federal dates cite the Federal Register and the FTC. state and global facts cite the legislature, the regulator, or a reputable law-firm source, cross-checked where a government page could not be machine-read.

Marked unverified, confirm against the primary source before relying on a figure. the South Korea PIPA effective date and the CEO-liability and 10-percent-turnover specifics. the Alabama HB 161 exact effective date. the exact Declared Age Range enum brackets (the Apple doc page renders as a client-side app that resisted an automated read, so the bands rest on Apple's Texas worked example). the California AADC partial-enforcement start date. the exact per-state Global Privacy Control required list and the 2026 penalty figures. the Australia Children's Online Privacy Code date. the Canada federal reform bill status. and the Google Android developer-verification rollout scope.

The genuinely unsettled areas an audit treats as moving targets. the current US external-purchase commission (pending the Supreme Court, argument October 2026), the ASAA effective dates (all under litigation or delay), the California AADC scope, and the per-state Global Privacy Control list. Treat this document as HARD on the existence and direction of each obligation, and advisory on any specific number or date until re-verified against the cited source.
