# Global Regulatory Hard Rules (2026). USA and Worldwide

This document is the non-EU legal layer for App Store and Google Play compliance. It is the companion to [EU-REGULATORY-2026.md](EU-REGULATORY-2026.md). The same framing holds. Store compliance is not the same as legal compliance. Passing App Review does not make an app compliant with US federal or state law, or with the laws of the UK, Australia, Brazil, Canada, South Korea, India, Singapore, Japan, or China. The store enforces a subset, a regulator enforces the rest, and for an app that reaches users in a market both must be satisfied.

Every item is a HARD rule for any app that reaches users in the named market. Each carries a date and a source. Apple-backed items cite developer.apple.com so the reference stays Apple-anchored. Many US and global dates are under active litigation or legislative delay, so treat each effective date as the statutory date subject to injunction or amendment, and re-verify against the cited source before relying on it. Items that could not be confirmed against a primary source are labelled unverified in the last section.

## 1. Storefront-backed age-assurance spines (Apple and Google-backed)

Several national and US-state laws are operated through storefront-specific age-assurance machinery, so an audit checks this layer first.

### 1.1 Apple's cross-region age-assurance spine

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

### 1.2 Google Play Age Signals API (v3 / beta)

To help developers meet compliance obligations under age verification laws in jurisdictions such as Texas, Utah, Louisiana, and Brazil, Google Play provides a runtime client-side age signal interface.

- **Purpose and Scope**: The Play Age Signals API retrieves age-related signals for users, notifies Google Play of significant app changes requiring parental approval, and receives notifications about revoked approvals. It only returns data for users based in regions where Play is required by law to provide age category data.
- **Terms of Service (ToS)**: Usage is heavily restricted. Developers may only use information from the Play Age Signals API to provide age-appropriate content and experiences in compliance with laws. You **MUST NOT** use the API for any other purpose including, but not limited to, advertising, marketing, user profiling, or analytics. Misuse will result in the termination of API access and immediate app suspension or takedown.
- **Integration & Dependency**: Integrate using `com.google.android.play:age-signals:0.0.3` (or subsequent versions). Supported on Android 6.0 (API level 23) and higher.
- **Bands**: Default returned categories are 0-12, 13-15, 16-17, and 18+ (custom age ranges can also be received). Cached age signals are updated by Play within 2 to 8 weeks after the user's birthday.
- **Data Safety**: No user data is collected, stored, or shared by the client-side library itself. Google Play's background services handle data governed by the Google Play ToS.
- **Rollout Timeline**:
  - **Brazil**: Started rolling out on March 17, 2026, to meet requirements under Brazil's Digital ECA.
  - **Texas**: Started returning signals on May 28, 2026, for users who created accounts after that date to comply with Texas SB2420.
  - Ongoing updates are provided for other US states (Utah, Louisiana).

Sources. [Google Play Age Signals overview](https://developer.android.com/google/play/age-signals/v3/overview), [Use Play Age Signals API (beta)](https://developer.android.com/google/play/age-signals/v3/use-age-signals-api), [Google Play Developer Help](https://support.google.com/googleplay/android-developer/answer/16569691).

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

- FTC Enforcement Policy Statement on age-verification technology, 25 February 2026, in force until final COPPA amendments are published. A general or mixed-audience app that collects age data for age verification is outside COPPA enforcement only if it uses the data solely for age determination, minimises retention, vets third parties, gives notice, and secures the data. Correction to earlier drafts of this doc. the section 312.11 carve-outs are earlier dates and bind FTC-approved Safe Harbor programs, not developers. Bill status on 5 September 2026 (govinfo BILLSTATUS). COPPA 2.0 (S.836) passed the Senate on 5 March 2026 and sits at the House desk, the KIDS Act (H.R.7757) passed the House on 29 June 2026 and sits in Senate Commerce, KOSA (S.1748) was ordered reported on 5 August 2026, and the App Store Accountability Act (H.R.3149) is at full committee. None is law. Sources. [FTC policy statement](https://www.ftc.gov/news-events/news/press-releases/2026/02/ftc-issues-coppa-policy-statement-incentivize-use-age-verification-technologies-protect-children), [COPPA final rule, 90 FR 16918](https://www.govinfo.gov/content/pkg/FR-2025-04-22/html/2025-05904.htm), [BILLSTATUS bulk data](https://www.govinfo.gov/bulkdata/BILLSTATUS/119).

### 2.2 US state App Store Accountability Acts (ASAA)

These put duties on both the store and the developer, separate from broader social-media minor laws. Four states as of mid-2026, all under active litigation or delay.

| State | Bill | Signed | Effective (subject to litigation) |
|---|---|---|---|
| Utah | SB 142 | 26 March 2025 | store and developer duties from 6 May 2026, some operational parts delayed to 6 May 2027, private right of action from 31 December 2026 |
| Texas | SB 2420 | 2025 | statutory 1 January 2026, enjoined 23 December 2025, injunction stayed 28 May 2026 so now in effect while litigation continues |
| Louisiana | HB 570 | 30 June 2025 | delayed one year to 1 July 2027 |
| Alabama | HB 161 | 9 March 2026 | 2027, exact date unverified |

Common developer duties. request and receive an age category from the store. confirm whether verifiable parental consent exists for a minor account before use. assign an accurate age and suitability rating. re-request consent on a major change. limit use of age and consent data to compliance and delete it after verification (Texas is explicit on deletion). For Android apps, Google Play supports this via the Play Age Signals API, which began returning signals for eligible Texas accounts created after May 28, 2026. Sources. [Utah SB 142](https://le.utah.gov/~2025/bills/static/SB0142.html), [FPF comparison of the ASAAs](https://fpf.org/blog/comparing-enacted-app-store-accountability-acts/), [Wiley ASAA developments](https://www.wiley.law/alert-Key-Developments-With-State-App-Store-Accountability-Acts-as-Texas-Act-Takes-Effect).

Apple discrepancy to flag. Apple's storefront date for Louisiana is 1 July 2026, while the statute was delayed to 1 July 2027. An audit flags the gap rather than assuming either date. Sources. [Apple region age requirements](https://developer.apple.com/news/?id=f5zj08ey), [Alston on the Louisiana delay](https://www.alstonprivacy.com/louisiana-delays-app-store-accountability-effective-date-to-july-2027/).

Note. Texas HB 18 (the SCOPE Act, effective 1 September 2024) is a separate Texas law that regulates digital service providers directly, distinct from the ASAA.

- Status on 5 September 2026, verified on the enrolled texts and court dockets. Texas SB 2420 is in force since 1 January 2026. the Fifth Circuit stayed the preliminary injunctions on 4 June 2026 and the Supreme Court declined to vacate the stay on 6 July 2026, merits appeal pending. Utah SB 142 was amended by HB 498 (2026). every substantive duty now begins 6 May 2027, pre-installed apps are in scope, and enforcement is a private right of action only, so the CCIA challenge was dismissed on 21 April 2026. Louisiana HB 570 (Act 481 of 2025) never takes effect. HB 977 (Act 185 of 2026) re-enacts the regime effective 1 July 2027. Alabama HB 161 is confirmed effective 1 January 2027 with legacy accounts age-verified by 1 October 2027. Sources. [Fifth Circuit stay order, Nos. 25-51073 and 26-50001](https://www.ca5.uscourts.gov/), [Utah HB 498 enrolled](https://le.utah.gov/Session/2026/bills/enrolled/HB0498.pdf), [Louisiana HB 977](https://legis.la.gov/), [Alabama HB 161](https://alison.legislature.state.al.us/).

### 2.3 US external purchase links and anti-steering (Epic v. Apple)

- 30 April 2025. the court found Apple in civil contempt and enjoined it from charging a commission on out-of-app purchases or restricting the design of external links. 11 December 2025. the Ninth Circuit upheld the contempt finding but narrowed the remedy. Apple may charge only costs genuinely necessary to coordinate the hand-off, not a flat percentage. The Supreme Court granted cert in mid-2026 with argument scheduled October 2026, so the exact US commission is unsettled. Sources. [Ninth Circuit opinion](https://cdn.ca9.uscourts.gov/datastore/opinions/2025/12/11/25-2935.pdf), [SCOTUS cert reporting](https://9to5mac.com/2026/06/30/supreme-court-agrees-to-hear-apple-appeal-over-epic-games-ruling/).
- Apple-backed rule. from 1 May 2025 Apple updated Guidelines 3.1.1, 3.1.1(a), 3.1.3, and 3.1.3(a) for the US decision. On the US storefront an app may include external-purchase links or buttons to the developer's own website, with no entitlement and no mandatory disclosure sheet. It does not permit alternative in-app payment. the transaction happens on the web. Outside the US the prohibition still applies and the external-purchase-link entitlement is still required. Sources. [Apple guideline update 1 May 2025](https://developer.apple.com/news/?id=9txfddzf), [Apple App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/).
- An audit treats the US commission question as unresolved, not as a fixed zero.

### 2.4 California (CCPA and CPRA, CPPA 2026 regulations, AADC)

- CCPA and CPRA apply to a for-profit business doing business in California over a revenue or volume threshold. Duties. a privacy policy and a notice at collection, rights to know, delete, and correct, an opt-out of sale and sharing through a "Do Not Sell or Share" mechanism that honors Global Privacy Control, a "Limit the Use of My Sensitive Personal Information" control, and non-discrimination. Source. [California AG CCPA](https://oag.ca.gov/privacy/ccpa).
- The CPPA finalised 2026 regulations, effective 1 January 2026. Automated-decision-making duties for high-impact decisions begin 1 April 2027, and cybersecurity audits phase in from 1 April 2028 by revenue tier. Source. [CPPA regulations](https://cppa.ca.gov/regulations/ccpa_updates.html).
- The California Age-Appropriate Design Code (AB 2273) is only partly enforceable. On 12 March 2026 the Ninth Circuit narrowed the injunction. age-estimation and coverage parts may proceed, but the data-use restriction and the DPIA requirement stay enjoined. Treat the vague data-use and DPIA duties as not required for now. Source. [Ninth Circuit AADC opinion](https://cdn.ca9.uscourts.gov/datastore/opinions/2026/03/12/25-2366.pdf).
- California SB 976 (social-media addiction) applies only to social-feed apps for minors, not a general app. its age-verification part starts 1 January 2027. Source. [California AG SB 976](https://oag.ca.gov/sb976).

- 2027 California dates, verified on leginfo and the CPPA text. AB 1043 (Digital Age Assurance Act) is operative 1 January 2027. operating systems and app stores collect age at setup and expose an age-bracket signal by API, developers request and use it. SB 976 from 1 January 2027 treats every user as a minor unless age assurance reasonably determines otherwise before an addictive feed or a night-time notification, with AG age-assurance regulations due the same day. AB 56 requires the Surgeon General warning label on social media daily, after three cumulative hours, then hourly, from 1 January 2027. SB 243 companion chatbot operators report annually to the Office of Suicide Prevention from 1 July 2027. CPPA regulations. automated decision-making notice, opt-out, and access by 1 January 2027, risk assessments for pre-2026 processing by 31 December 2027 and submitted by 1 April 2028, cybersecurity audit certifications from 1 April 2028 by revenue tier. The Delete Act DROP platform obligated data brokers from 1 August 2026. Sources. [AB 1043](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260AB1043), [SB 976](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240SB976), [CPPA regulations](https://cppa.ca.gov/regulations/), [DROP](https://privacy.ca.gov/drop-for-data-brokers/).

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

- 2027 and 2028 state dates added September 2026. New York SAFE for Kids Act final rules were published 29 July 2026 and take effect 25 January 2027 (addictive feeds and night-time notifications for minors need verifiable parental consent, certified age assurance). Vermont Age-Appropriate Design Code effective 1 January 2027, rulemaking comments due 2 October 2026. Washington HB 2225 companion chatbot duties effective 1 January 2027. Oklahoma Consumer Data Privacy Act effective 1 January 2027. Colorado SB26-051 device age attestation effective 1 July 2028 (existing devices by 1 January 2029), and SB26-189 replaces the Colorado AI Act with a transparency-based automated decision-making regime from 1 January 2027. Connecticut SB 1295 minors' targeted-advertising ban (1 July 2026), Alabama Personal Data Protection Act (1 May 2027), Nebraska design code enforcement (1 July 2026), and Illinois HB 5511 (signed 31 July 2026, 2028 effective date) are reported by secondary sources only and are not encoded as deadlines. Sources. [NY AG SAFE for Kids](https://ag.ny.gov/), [Vermont AG rulemaking](https://ago.vermont.gov/vermont-age-appropriate-design-code-rulemaking), [Washington HB 2225](https://app.leg.wa.gov/billsummary?BillNumber=2225&Year=2026), [Colorado SB26-051](https://leg.colorado.gov/bills/sb26-051), [Oklahoma SB 546](https://okhouse.gov/posts/news-20260323_2).

### 2.6 US health data and biometric law

- Most direct-to-consumer health apps are not covered by HIPAA. HIPAA applies only when the developer is a covered entity or a business associate under a BAA. Otherwise the FTC Health Breach Notification Rule applies. the 2024 final rule covers non-HIPAA health apps, treats an unauthorized disclosure (for example sharing health data with an ad vendor) as a breach, and requires notice within 60 days. Penalty up to 53,088 dollars per violation. Sources. [HHS health apps](https://www.hhs.gov/hipaa/for-professionals/special-topics/health-apps/index.html), [FTC Health Breach Notification Rule](https://www.ftc.gov/news-events/news/press-releases/2024/04/ftc-finalizes-changes-health-breach-notification-rule).
- Illinois BIPA. written notice and a written release before collecting a biometric identifier, a public retention schedule, destruction within 3 years, no sale, and a private right of action with statutory damages of 1,000 dollars per negligent and 5,000 dollars per intentional violation. SB 2979 (effective 2 August 2024) made repeated collection of the same biometric a single violation. Texas CUBI and Washington My Health My Data Act add further consent and destruction duties. Sources. [BIPA overview](https://www.recordinglaw.com/us-laws/data-privacy-laws/bipa/), [Washington MHMDA](https://app.leg.wa.gov/RCW/default.aspx?cite=19.373&full=true).

- TAKE IT DOWN Act (Pub. L. 119-12). FTC enforcement of the non-consensual intimate imagery notice-and-removal duty began 19 May 2026. A covered platform removes reported content, with known identical copies, within 48 hours. Source. [FTC business blog, May 2026](https://www.ftc.gov/business-guidance/blog/2026/05/take-it-down-act-enforcement-starts-now-what-know-about-ftc-tida).

### 2.7 US subscription cancellation (negative option rule)

- The FTC's federal "click to cancel" rule (the Negative Option Rule amendment) was VACATED IN FULL by the Eighth Circuit on 8 July 2025, six days before its most demanding provisions were due to take effect on 14 July 2025, for a procedural failure. the FTC skipped the required preliminary regulatory analysis before finalizing it. The federal rule is not currently in force. Source. [WilmerHale, Eighth Circuit vacates the FTC's click-to-cancel rule](https://www.wilmerhale.com/en/insights/client-alerts/20250801-eighth-circuit-vacates-the-ftcs-click-to-cancel-rule-but-federal-and-state-regulators-likely-to-remain-active).
- The FTC reopened rulemaking. it submitted an Advance Notice of Proposed Rulemaking to OIRA on 30 January 2026 and published it on 11 March 2026, seeking comment (closed 13 April 2026) on whether to amend or supplement the rule. No final rule is in force as of this writing. Source. [FTC ANPRM press release](https://www.ftc.gov/news-events/news/press-releases/2026/03/ftc-seeks-public-comment-response-advance-notice-proposed-rulemaking-regarding-negative-option).
- The federal vacatur does not remove the underlying duty. the FTC retains authority to bring cases against a subscription that is easy to start and hard to cancel under Section 5 of the FTC Act (unfair or deceptive acts) and ROSCA (the Restore Online Shoppers' Confidence Act, which independently requires clear disclosure, informed consent, and a simple cancellation mechanism for any negative-option feature sold online). Chair Ferguson signaled continued vigorous enforcement of exactly this pattern through existing law. Source. [WilmerHale, as above].
- California, New York, and Massachusetts have their own negative-option statutes in force independent of the federal rule, generally requiring cancellation to be at least as easy as sign-up, and roughly 30 US jurisdictions have some comparable requirement. A subscription flow that requires a phone call, a mailed letter, or an in-person visit to cancel, while sign-up is a single tap, is the classic violation pattern regardless of which specific law applies. Sources. [WilmerHale, as above], [Dickinson Wright, click-to-cancel is click-to-gone](https://www.dickinson-wright.com/news-alerts/rule-interrupted-click-to-cancel-is-click-to-gone).
- This applies to a subscription's own customer-facing cancellation flow (a web or account-settings surface for a cross-platform or web-billed subscription), not to a digital good billed through Apple in-app purchase or Google Play Billing, where the platform's own subscription-management surface already satisfies an easy-cancel path. It becomes a real rejection-adjacent and legal risk for any app whose subscription is billed outside the app stores (a web signup funnel, a companion account) and directs the person to call, email, or mail to cancel.

### 2.8 US accessibility rules that reach apps through the contract chain (added September 2026)

Neither rule is a general developer duty. Both bind the entity that provides the app, and they reach a commercial developer through a contract, licence, or other arrangement, which the HHS rule names expressly. Both 2024 compliance dates were extended by interim final rules in 2026.

- DOJ ADA Title II, 28 CFR Part 35 Subpart H. A mobile app provided or made available by a state or local government entity must conform to WCAG 2.1 Level AA by 26 April 2027 (population 50,000 or more) or 26 April 2028 (under 50,000, and every special district government). The extension is verbatim from 24 April 2026 to 26 April 2027. No final rule had been published as of 5 September 2026. Sources. [Interim final rule, FR Doc. 2026-07663](https://www.govinfo.gov/content/pkg/FR-2026-04-20/html/2026-07663.htm), [ADA.gov web rule fact sheet](https://www.ada.gov/resources/2024-03-08-web-rule/).
- HHS Section 504, 45 CFR 84.84(b). A mobile app provided directly or through a contractual, licensing, or other arrangement by a recipient of HHS federal financial assistance must conform to WCAG 2.1 Level AA by 11 May 2027 (15 or more employees) or 10 May 2028 (fewer than 15). Sources. [Interim final rule, 91 FR 25496](https://www.govinfo.gov/content/pkg/FR-2026-05-11/html/2026-09266.htm), [HHS OCR press release](https://www.hhs.gov/press-room/hhs-extends-mobile-and-web-accessibility-deadline.html).
- Checked and carrying no new dated app obligation. EO 14365 and EO 14409 on AI, the FTC AI-accuracy policy statement (comments closed 31 July 2026, not finalised), surveillance pricing and dark patterns (FTC Act section 5 enforcement only), the TikTok divestiture (completed January 2026), BIS connected-vehicle rules (vehicle systems only), the voluntary FCC Cyber Trust Mark, Section 508 (still WCAG 2.0), and the FDA clinical decision support final guidance (non-binding).

## 3. Other global markets

### 3.1 United Kingdom

- Online Safety Act 2023. age-assurance duties in force from 25 July 2025, enforced by Ofcom. Highly Effective Age Assurance methods include facial age estimation, open banking, digital ID, and credit-card checks. self-declaration alone is not highly effective. Penalty up to 18 million pounds or 10 percent of global turnover, plus blocking orders. As of early 2026 Ofcom had opened investigations into more than 90 services. Sources. [Ofcom age checks](https://www.ofcom.org.uk/online-safety/protecting-children/age-checks-to-protect-children-online).
- ICO Age Appropriate Design Code (Children's Code), in force since September 2021. it applies to any service likely to be accessed by a UK child under 18, even a general-audience one. Checkable defaults. high privacy by default, data minimisation, geolocation off by default, profiling off by default, and a DPIA. Source. [ICO Children's Code](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/introduction-to-the-childrens-code/).

- Data (Use and Access) Act 2025. Commenced 5 February 2026 (SI 2026/82) with new lawful bases, automated decision-making rules, Schedule A1 cookie exemptions, and the PECR penalty uplift to 17.5 million pounds or 4 percent of turnover. The section 103 complaints process commenced 19 June 2026. acknowledge a data subject complaint within 30 days. The Information Commission itself (sections 117 to 119) has no commencement date yet. Sources. [SI 2026/82](https://www.legislation.gov.uk/uksi/2026/82/made), [DPA 2018 section 157](https://www.legislation.gov.uk/ukpga/2018/12/section/157).
- ICO final Guidance on Storage and Access Technologies, published 29 April 2026. Re-audit every SDK, tracking pixel, and device-fingerprinting call, not only cookies. The statutory AI and automated decision-making code of practice is required by SI 2026/425 (in force 12 May 2026) but has no publication date. Source. [ICO announcement](https://ico.org.uk/about-the-ico/media-centre/news-and-blogs/2026/04/final-storage-and-access-technologies-guidance-published/).
- Online Safety Act 2023, 2026 milestones. Ofcom published the register of categorised services on 30 June 2026 (Apple iMessage is Category 2B). CSEA reporting to the NCA portal is a live duty for user-to-user services since 7 April 2026 (SI 2026/268). Category 1 and 2A services deliver updated risk-assessment records by October 2026 and publish summaries by November 2026. Ofcom's statutory report on children's use of app stores is due by January 2027 and feeds the decision on bringing app stores into scope. Sources. [Ofcom roadmap to regulation](https://www.ofcom.org.uk/online-safety/illegal-and-harmful-content/roadmap-to-regulation), [SI 2026/268](https://www.legislation.gov.uk/uksi/2026/268/made).
- Under-16 social media ban, announced 15 June 2026 under the Children's Wellbeing and Schools Act. Regulations laid before the end of 2026, implementation in spring 2027. Under-16 accounts blocked on user-to-user social platforms (Snapchat, TikTok, YouTube, Instagram, Facebook, X named. WhatsApp and Signal out). For 16 and 17 year olds livestreaming and stranger contact are off by default, notifications are off from midnight to 6am, autoplay and personalised feeds are off by default, and AI romantic companion chatbots must enforce a minimum age of 18. Sources. [gov.uk announcement, 15 June 2026](https://www.gov.uk/government/collections/growing-up-in-the-online-world).
- Digital Markets, Competition and Consumers Act 2024. Subscription contracts regime (pre-contract information, renewal reminders, two cooling-off periods, easy cancellation, refunds) commences January 2027 per the 9 August 2026 announcement, superseding the spring 2027 estimate. Unfair commercial practices enforcement (drip pricing, fake urgency, default opt-ins) is live since 6 April 2025 with fines up to 10 percent of global turnover decided by the CMA directly. Apple and Google hold strategic market status since 22 October 2025. the proposed Steering conduct requirements (consultation closed 28 July 2026) have no decision date. Sources. [gov.uk, 9 August 2026](https://www.gov.uk/government/news/pm-starts-roll-out-of-everyday-fixes-on-the-cost-of-living-ending-rip-off-discounts-and-subscription-traps), [CMA mobile platforms programme](https://www.gov.uk/guidance/the-cmas-programme-of-work-across-mobile-platforms).

### 3.2 Australia

- Online Safety Amendment (Social Media Minimum Age) Act 2024, in force 10 December 2025. an age-restricted social media platform takes reasonable steps to stop under-16s holding an account. Named platforms include Facebook, Instagram, Snapchat, TikTok, X, YouTube, Reddit. The eSafety guidance expects a waterfall of methods, and self-declaration cannot be the sole method. Age-assurance data is ringfenced and destroyed after use. Penalty up to 49.5 million Australian dollars. Sources. [eSafety social media age restrictions](https://www.esafety.gov.au/about-us/industry-regulation/social-media-age-restrictions).
- Apple blocks 18-plus downloads in Australia from 24 February 2026.

- Apple, 18 June 2026. The 15+ age rating is no longer available on the App Store in Australia. Apps rated 15+ with the affected content descriptors moved to 16+. Re-check the storefront rating after the change. Source. [Apple, age rating updates for Australia and Vietnam, 21 May 2026](https://developer.apple.com/news/?id=yrrb45pw).

- App Distribution Services Online Safety Code (Schedule 7 of the Consolidated Industry Codes, registered 9 September 2025). Six months after commencement, on 9 September 2026, app stores must apply age assurance and access controls before permitting the download or purchase of adult apps, the Head Terms working-towards grace period ends, and the initial risk assessment is due. The Equipment Code (Schedule 8) is in force since 9 March 2026 with child-account and restricted-profile defaults, first compliance report no earlier than 9 March 2027. These pages were read from a Wayback capture of eSafety content last updated 19 May 2026 because esafety.gov.au was unreachable. re-confirm on the live register before acting. Source. [eSafety industry codes, unreachable from this environment, read from a Wayback capture](https://web.archive.org/web/2026/https://www.esafety.gov.au/industry/codes).
- Privacy Act. From 10 December 2026 the privacy policy must disclose the kinds of personal information used by, and decisions made by, automated decision-making that significantly affects rights or interests (APP 1.7 to 1.9). The Children's Online Privacy Code must be registered by 10 December 2026. The Online Safety (Age-Restricted Social Media Platforms) Amendment Rules 2026 (F2026L00370, 25 March 2026) amended the platform criteria, re-run the self-assessment. Sources. [OAIC APP guidelines](https://www.oaic.gov.au/privacy/australian-privacy-principles/australian-privacy-principles-guidelines), [OAIC children's code (page unreachable from this environment, dates from the OAIC timeline)](https://www.oaic.gov.au/privacy/privacy-legislation), [F2026L00370](https://www.legislation.gov.au/F2026L00370/asmade/text).

### 3.3 Brazil

- Digital ECA (Law 15,211/2025), enforceable from 17 March 2026, on top of the LGPD and enforced by the ANPD. Accepted age-verification methods include document verification, facial age estimation, facial matching, and a CPF database check. a self-declaration checkbox no longer counts. The ANPD 2026 enforcement plan prioritises app stores and operating systems as gatekeepers. Penalty up to 50 million reais per violation or 10 percent of Brazilian revenue. Sources. [Digital ECA timeline](https://inplp.com/latest-news/article/the-digital-eca-brazils-new-age-verification-framework-and-enforcement-timeline/).
- Apple blocks 18-plus downloads in Brazil from 24 February 2026, and loot-box apps auto-rate 18-plus on the Brazil storefront.
- Google Play rolled out support for the Digital ECA on March 17, 2026, returning age signals for eligible Brazilian users through the Play Age Signals API.

- Brazil alternative distribution (CADE). Beginning with iOS 26.5, developers can distribute apps on alternative app marketplaces, operate alternative marketplaces, and process payments for digital goods and services outside Apple In-App Purchase in Brazil. Every Apple Developer Program member had to accept the updated ADPLA (Attachment 12) by 6 July 2026. An unaccepted agreement blocks submissions. The Brazil fixed-odds betting licence check requires a NEW app version to start verification, editing App Review Information alone does not (8 May 2026). Sources. [Apple, changes to iOS in Brazil, 18 June 2026](https://developer.apple.com/news/?id=dhwadr2x), [Apple, ADPLA update deadline](https://developer.apple.com/news/?id=umq9wxmm), [Apple, Brazil betting licence verification](https://developer.apple.com/news/?id=x4eyetnp).

- Decreto n. 12.880 of 18 March 2026 regulates the Digital ECA. App stores and operating systems supply a free age signal, request age at account creation, verify it by an ANPD-approved method, allow contestation, seek guardian authorisation, and show the age rating before download (Article 25). Stores must block gambling and lottery apps and any app lacking an age-verification solution (Article 21). Lei n. 15.352 of 25 February 2026 makes the ANPD a full agency and hard-codes the 17 March 2026 date. ANPD publishes age-assurance parameters from August 2026 with adaptation through November 2026, and enforcement starts January 2027. The STF Tema 987 platform-liability ruling became final on 17 June 2026. The AI bill PL 2338/2023 is not enacted. Sources. [Decreto 12.880](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/decreto/D12880.htm), [ANPD ECA Digital](https://www.gov.br/anpd/pt-br/assuntos/eca-digital).

### 3.4 Canada

- PIPEDA is the federal baseline. informed consent, purpose limitation, and breach reporting. Quebec Law 25 is stricter. explicit opt-in consent for tracking and profiling, a named privacy officer, privacy impact assessments, and breach notification. Penalty up to the greater of 25 million Canadian dollars or 4 percent of global turnover. Sources. [Quebec Law 25](https://www.cookieyes.com/blog/quebec-law-25/).

- Checked 5 September 2026. No AI statute exists (no government AI bill in the 45th Parliament), Bill C-36 (privacy) is at first reading, Bill S-209 (age verification) passed the Senate on 15 April 2026 and is at House first reading, and the Online Harms bill was reintroduced as C-34 at second reading. Bill C-8 (cyber security, Royal Assent 15 June 2026) binds vital-services operators, not consumer apps. No new dated app obligation. Source. [LEGISinfo](https://www.parl.ca/legisinfo/).

### 3.5 South Korea

- PIPA is the baseline. a rewrite reported to take effect in 2026 raises the maximum penalty toward 10 percent of turnover and adds CEO accountability. exact date unverified.
- The Telecommunications Business Act mandates alternative in-app payment. Apple's implementation is Apple-backed and specific. a 26 percent commission on the price the user pays, gross of VAT, approved payment providers only (KCP, Inicis, Toss, NICE), the entitlement `com.apple.developer.storekit.external-purchase` with `SKExternalPurchase = "KR"`, a Korea-only binary, no co-mingling with Apple in-app purchase, a native (non-webview) payment, an external-purchase modal sheet shown first, monthly sales reporting within 15 days, and remittance within 45 days. Source. [Apple StoreKit external entitlement Korea](https://developer.apple.com/support/storekit-external-entitlement-kr/).

- Apple, October 2026. Two content descriptors move from an age rating of All to 12+ on the App Store in Korea, alongside the GRAC rating-certificate (RCN) override announced 12 August 2026. Source. [Apple, age rating updates for Korea](https://developer.apple.com/news/?id=oj3r9pvw).

- Personal Information Protection Act amendment (Act No. 21445), effective 11 September 2026. The CEO and representative are the final accountable parties, a board-approved chief privacy officer is required at qualifying scale, punitive surcharges and widened breach notification apply. A further Telecommunications Business Act and Network Act amendment passed on 12 March 2026 with an unconfirmed effective date. Source. [law.go.kr PIPA amendment history](https://law.go.kr/LSW/lsRvsRsnListP.do?chrClsCd=010102&lsId=011357).

### 3.6 India

- Digital Personal Data Protection Act 2023 with the DPDP Rules 2025 notified 13 November 2025. the consent and children's rules are enforceable from 13 May 2027. Everyone under 18 is a child, so verifiable parental consent through a government-backed system such as DigiLocker is required before processing any under-18 data, and behavioral tracking and targeted advertising to children are prohibited. Source. [India DPDP Rules 2025](https://www.bassberry.com/news/indias-data-privacy-rules-what-your-business-needs-to-know/).

- Digital Personal Data Protection Rules 2025 (G.S.R. 846(E), 13 November 2025) commence in three tranches. rules 1, 2, and 17 to 21 immediately, rule 4 (registered Consent Managers) on 13 November 2026, and rules 3, 5 to 16, 22, and 23 (consent notice, security safeguards, breach reporting, verifiable parental consent, data principal rights) on 13 May 2027. The IT Rules amendment of 10 February 2026 adds synthetic-content labelling with 3-hour and 2-hour takedown windows from 20 February 2026. Primary Gazette hosts returned 403 during verification, the text was confirmed from a mirror.

### 3.7 Singapore

- PDPA is the baseline. a data protection officer, breach notification within 3 days, and consent. The IMDA Code of Practice for Online Safety for App Distribution Services required app-store age assurance from 1 April 2026. app stores screen and stop users estimated under 18 from downloading age-inappropriate apps, and age-assurance data is not retained after the purpose is met. Source. [IMDA app-store age assurance](https://www.twobirds.com/en/insights/2026/singapore/app-stores-in-singapore-required-to-implement-age-assurance-measures).
- Apple blocks 18-plus downloads in Singapore from 24 February 2026.

- Online Safety (Relief and Accountability) Act 2025, partially commenced 29 June 2026 with the Online Safety Commission as regulator and five priority harms in scope. Further harm categories follow progressively with no published date. The IMDA age-assurance duty on app distribution services (screen and stop users under 18 from age-inappropriate downloads) bit on 1 April 2026, while the Code itself commenced 31 March 2025. Source. [MDDI announcement](https://www.mddi.gov.sg/newsroom/online-safety-commission-and-online-safety--relief-and-accountability--act-2025-to-start-on-29-june-2026/).

### 3.8 Japan

- APPI is the baseline. an amendment bill was submitted to the Diet in 2026, with full effect expected by 2028. A consent-based cross-border transfer discloses the recipient country, that country's data-protection regime, and the recipient's protection measures, and the law reaches foreign operators serving people in Japan. Source. [DLA Piper Japan transfer](https://www.dlapiperdataprotection.com/?t=transfer&c=JP).

- Act on the Protection of Personal Information amendment, passed 10 July 2026 and promulgated 17 July 2026. Effective within two years (by 16 July 2028, exact day by cabinet order). New under-16 threshold where the legal representative is the party for consent, notice, and use-stop requests, plus a surcharge regime. The Mobile Software Competition Act is in full effect since 18 December 2025, and designated providers (Apple, iTunes KK, Google) publish annual compliance reports (latest 27 July 2026). Sources. [PPC amendment page](https://www.ppc.go.jp/personalinfo/legal/r8kaiseihogohou/), [JFTC MSCA](https://www.jftc.go.jp/msca/).

### 3.9 China

- Mobile App Filing with the MIIT (an extension of ICP filing) is mandatory. new apps since 1 September 2023, existing apps by 31 March 2024, or removal. Only a Chinese entity can file, so a foreign developer partners with a local company. PIPL privacy, data localisation, real-name verification, content moderation, and a Banhao license for games also apply. Sources. [China app filing guide](https://appinchina.co/blog/the-complete-guide-to-chinas-mobile-app-filing/).

- Interim Measures for AI Anthropomorphic Interactive Services (CAC Order No. 21), effective 15 July 2026. Identify minor users, switch them into minors mode automatically, obtain guardian consent under 14, and never offer virtual companion or virtual kin services to a minor. Any chat, companion, or roleplay app in China is in scope. The minors online-content classification measures (effective 1 March 2026) ban surfacing harmful content on the home screen, pop-ups, hot searches, rankings, and recommendations, and ban algorithmic push to minors. The personal-information compliance audit measures (effective 1 May 2025) require handlers above 10 million people to complete a first audit within the first two-year cycle (by 30 April 2027, derived) and repeat at least every two years. Sources. [CAC, AI anthropomorphic services measures](https://www.cac.gov.cn/2026-04/10/c_1777558395078289.htm), [CAC minors content classification](https://www.cac.gov.cn/2026-01/23/c_1770728781060093.htm), [CAC compliance audit measures](https://www.cac.gov.cn/2025-02/14/c_1741233507681519.htm).

### 3.10 Vietnam

- Decree 147, Article 38. From 18 June 2026 apps available on the App Store in Vietnam require a region-specific age rating. App Store Connect exposes a 00+ value (ZERO_ZERO in the App Store Connect API) for the Vietnam classification. Source. [Apple, age rating updates for Australia and Vietnam, 21 May 2026](https://developer.apple.com/news/?id=yrrb45pw), [App Store Connect API 4.4 release notes](https://developer.apple.com/documentation/appstoreconnectapi/app-store-connect-api-4-4-release-notes).

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
- US subscription cancellation. any web or account-settings cancellation path for a subscription billed outside Apple in-app purchase or Google Play Billing is at least as easy as sign-up, never a phone call, a mailed letter, or an in-person visit, per ROSCA and the active state negative-option statutes (California, New York, Massachusetts) regardless of the vacated federal rule's status.

## 6. Sources and verification note

Apple facts cite developer.apple.com and apple.com. US federal dates cite the Federal Register and the FTC. state and global facts cite the legislature, the regulator, or a reputable law-firm source, cross-checked where a government page could not be machine-read.

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

Marked unverified, confirm against the primary source before relying on a figure. the South Korea PIPA effective date and the CEO-liability and 10-percent-turnover specifics. the Alabama HB 161 exact effective date. the exact Declared Age Range enum brackets (the Apple doc page renders as a client-side app that resisted an automated read, so the bands rest on Apple's Texas worked example). the California AADC partial-enforcement start date. the exact per-state Global Privacy Control required list and the 2026 penalty figures. the Australia Children's Online Privacy Code date. the Canada federal reform bill status. and the Google Android developer-verification rollout scope.

The genuinely unsettled areas an audit treats as moving targets. the current US external-purchase commission (pending the Supreme Court, argument October 2026), the ASAA effective dates (all under litigation or delay), the California AADC scope, and the per-state Global Privacy Control list. Treat this document as HARD on the existence and direction of each obligation, and advisory on any specific number or date until re-verified against the cited source.
