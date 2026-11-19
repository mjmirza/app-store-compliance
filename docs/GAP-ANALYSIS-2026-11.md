# Gap analysis, November 2026

<!-- freshness: 60d -->

What changed on the platforms and in law between 5 September and 14 November 2026, what this playbook added in response, and what could not be read from a primary source. It repeats the method of [GAP-ANALYSIS-2026-09.md](GAP-ANALYSIS-2026-09.md). Every item encoded below was read on its primary source on 14 November 2026. Anything that could not be read there is listed under Unverified, not folded into a rule. The next sweep is due by 13 January 2027.

## 1. Method

- Apple. every Apple Developer news post from 5 September to 14 November 2026 (21 posts, none between 5 and 8 September) and the Upcoming Requirements page.
- Google. the Play policy announcements in the window (one batch, 29 October 2026), the Play Policy Deadlines table, the Android Developers Blog, and the target API, Billing deprecation, and developer verification pages.
- Regulation. four regional passes (EU and UK, United States, Asia-Pacific, and Canada, Australia, Brazil), each returning only dated items with a quoted sentence from the instrument. gov.ca.gov, ofcom.org.uk, and esafety.gov.au refused or timed out on scripted fetches, so their items are listed as unverified rather than encoded.
- Repo. every finding was searched for across `docs/`, `data/`, and `references/` before anything was written, so items the October review had already added (the 16 October guideline revision, the EU ATT prompt, the DSA trader status) were not added twice.
- Every finding a research pass returned was re-read on its primary page before it changed the data. Two claims that contradicted existing entries (the social media 13+ rule, the iPhone Duo SDK scope) were checked this way and turned out to be wrong, so the entries stand.

## 2. Apple, verified deltas

| Change | Source | Repo action |
|---|---|---|
| New age rating descriptors, Shared Location and Dating and Relationships, in the questionnaire from 16 November 2026, every app answered by 12 January 2027, Dating sets an 18+ minimum | [yxkh08us](https://developer.apple.com/news/?id=yxkh08us) | APPLE-AGE-RATING-LOCATION-DATING-2027, APPLE.md |
| Original Developer ID Sub-CA expires 1 February 2027, re-sign installer packages from the G2 authority | [w4atic4c](https://developer.apple.com/news/?id=w4atic4c) | APPLE-DEVELOPER-ID-SUBCA-EXPIRY-2027, PLATFORM-MECHANICS section 1.1 |
| Developer Program License Agreement updated 13 October 2026, acceptance needed | [17mwd36z](https://developer.apple.com/news/?id=17mwd36z) | APPLE.md |
| Taiwan standard commission 30 to 26 percent from 31 October 2026 | [w9mxlhek](https://developer.apple.com/news/?id=w9mxlhek) | APPLE.md |
| App Review Guidelines revised 16 October 2026 (2.3.14, 2.5.19, 1.2 NCII) and EU ATT alternative prompt from iOS 27.2 | [92th7e5i](https://developer.apple.com/news/?id=92th7e5i), [idsft9ai](https://developer.apple.com/news/?id=idsft9ai) | Already in the repo from the October review, no change |

Checked and month-only, placeholders kept. the social media declaration (September 2026), the minimum SDK for uploads and the iPhone Duo screenshot rule (both April 2027).

## 3. Google Play and Android, verified deltas

All from the policy announcement of 29 October 2026 and the Play Policy Deadlines table.

| Deadline | Change | Repo action |
|---|---|---|
| 1 December 2026 | Japan payments authorization, or payments held globally | GOOGLE-JAPAN-PAYMENTS-AUTHORIZATION-2026 |
| 27 January 2027 | Eligibility-based subscription discounts disclose criteria, verification, and post-eligibility pricing | GOOGLE-SUBSCRIPTION-ELIGIBILITY-DISCOUNTS-2027 |
| 14 April 2027 | AppFunctions API policy | GOOGLE-APPFUNCTIONS-POLICY-2027 |
| 25 August 2027 | Local Network and Manage Contacts permission declarations | GOOGLE-LOCAL-NETWORK-MANAGE-CONTACTS-2027 |

The same announcement says trader status must be declared in Play Console starting November 2026, which the repo already covers. Android developer verification still names 2027 for the global step with no day. The target API and Billing pages are unchanged.

## 4. Regulation, verified deltas

- European Union. Cyber Resilience Act vulnerability and incident reporting applies from 11 September 2026, already encoded. The Commission proposed the Digital Fairness Act on 11 November 2026 (COM(2026) 1100), which would apply 12 months after entry into force, so it creates no obligation yet. The EDPB finalised its DSA and GDPR interplay guidelines and consulted on fines guidelines until 13 November 2026.
- United Kingdom. The draft Consumer Subscription Contracts (Cancellation and Information) Regulations 2026 name 1 January 2027 and had not been made on 14 November 2026.
- United States. New York S.9051B/A.10379C (signed 28 October 2026) bars unsafe AI chatbot features for minors and requires age verification with a non-ID option, with no effective date published. The FTC opened an advance notice of proposed rulemaking on impersonation scams on 1 October 2026 (comments to 30 November 2026). Louisiana Act 502 takes effect 1 January 2027. The DOJ ADA Title II rule is still the interim final rule and the FTC AI accuracy statement is still proposed.

## 5. Asia-Pacific, Canada, Australia, Brazil, verified deltas

The regional pass for Asia-Pacific, Canada, Australia, and Brazil was still running when this sweep merged. Its findings landed in a follow-up change on 15 November 2026 after each item was read on its primary source. Korea's AI development reuse rule (Act No. 21910, from 9 March 2027), Indonesia's PP TUNAS self-assessment deadline (31 December 2026), and China's CAC filing window for platforms with a large minor audience (closing around 16 November 2026). Items already confirmed in [#659](https://github.com/mjmirza/app-store-compliance/issues/659) on 14 November 2026. Korea's mandatory privacy certification from 1 July 2027, Japan's APPI amendment as Act No. 56 of 2026, and the India DPDP rule 4 Consent Manager date.

## 6. Unverified, deliberately not encoded

- California bills signed in September 2026 (AB 1709 social media for under-16s, SB 1119 companion chatbots, AB 1856 age signals, AB 2246 replacing the Age-Appropriate Design Code, SB 1000 and AB 2713 AI transparency). A research pass read the Governor's releases, but gov.ca.gov refused every fetch from this check, and none of the releases states an effective date. Read the chaptered text on leginfo before encoding.
- Ofcom's amended Illegal Content Codes of Practice (issued 12 October 2026, in force 2 November 2026) and its categorised-services risk assessment dates. ofcom.org.uk answers scripted reads with a browser challenge, so the wording was seen only through a search index.
- The UK under-16 social media regulations, reported to be laid in December 2026 for spring 2027. Secondary only.
- The Alabama App Store Accountability Act challenge (CCIA, reported 28 October 2026). No docket found.
- Korea MyData expansion dates and the Australia App Distribution Services Code on the live eSafety register, carried over from [#659](https://github.com/mjmirza/app-store-compliance/issues/659).

## 7. Follow-up, 15 November 2026

A second pass read the App Store Connect release notes and the Upcoming Requirements page line by line, which the first pass had only skimmed.

| Change | Source | Repo action |
|---|---|---|
| From early 2027 App Store Connect will no longer accept uploads containing On-Demand Resources from new apps or apps that have never used the feature (release notes, 12 November 2026) | [release notes](https://developer.apple.com/help/app-store-connect/release-notes/) | APPLE-ODR-UPLOAD-BLOCK-2027, APPLE-ODR-DEPRECATED-27 expanded |
| iOS and iPadOS apps uploaded to App Store Connect must target iOS 13 or later | [Upcoming Requirements](https://developer.apple.com/news/upcoming-requirements/) | APPLE-MIN-DEPLOYMENT-TARGET-IOS13, new guard check |

Checked and not encoded. The INSTALLS analytics report deprecation in App Store Connect API 4.6 affects reporting, not review. The Republic of Korea consent schedule for converting subscription offers to standard paid subscriptions (30 September 2026) is tracked for the next sweep, because its detail page failed to load on the first read.

## 8. Follow-up, 19 November 2026

The 29 October 2026 announcement says trader status must be declared in Play Console starting in November 2026. Section 3 above treated that line as already covered. The linked Play Console page (answer 17594752), read on 19 November 2026, states two dates the announcement does not. Existing accounts must declare trader or non-trader status by 1 February 2027, and the EEA and UK online marketplace display starts 1 March 2027. Those are `GOOGLE-PLAY-TRADER-STATUS-2027` and `GOOGLE-PLAY-MARKETPLACE-DISPLAY-2027`. They are not the February 2027 technical quality deadline (`GOOGLE-TECH-QUALITY-FEB-2027`) and not Apple's DSA trader duty (`EU-DSA-TRADER-STATUS`).
