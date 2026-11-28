# Rejection Map by App Type

A games app and a finance app fail review for very different reasons. This doc routes each app type to the guidelines that actually hit it, so you check the right things instead of all things. Adopted from the structure of the most popular open source preflight skill. Run the universal set for every app, then the set that matches your app type.

## Universal. Every app

- Stability. No crashes, broken links, or placeholder content. Apple 2.1, Google spam and minimum functionality.
- Demo account and live backend. A working demo account, no 2FA the reviewer cannot pass, a backend that stays up. Apple 2.1.
- Review notes. A screen recording or path for every non obvious feature, the app purpose, test credentials, external services, regional notes, and any regulatory document. Apple 2.1.
- Privacy policy. Published, reachable in the app, accurate. Apple 5.1.1, Google User Data.
- Permissions. Each sensitive permission traces to a visible core feature with a specific reason string. Apple 5.1.1, Google permissions policy.
- Privacy manifest. iOS PrivacyInfo.xcprivacy with approved reason codes, and every SDK ships its signed manifest. Apple upload enforcement.
- Data declaration. Apple privacy labels and Google Data Safety match real runtime behavior including SDKs.
- Metadata. Accurate name, screenshots of the app in use, no other platform mentions, no Apple device images in the icon, no device frames in the preview video. Apple 2.3, 5.2.5.
- Account deletion. Genuine in app deletion for any account creating app, not a deactivate or a web form. Apple 5.1.1(v), Google account deletion.
- Export compliance. ITSAppUsesNonExemptEncryption set so the build does not stall.

## Subscriptions and in app purchase

- All digital goods through Apple in app purchase and Google Play Billing. Apple 3.1.1.
- Subscriptions show real ongoing value, clear terms, and the actual billed amount at least as prominent as the per month figure. Apple 3.1.2.
- Terms of Use or EULA and Privacy Policy links present in the app and the metadata. Apple 3.1.2.
- Restore Purchases control for non consumables. Apple 3.1.1.
- Loot boxes and random rewards disclose odds before purchase. Apple 3.1.1, Google random items disclosure.
- Physical goods use external payment, not in app purchase. Apple 3.1.5(a).

## Social and user generated content

- A EULA with zero tolerance for objectionable content, that users must agree to.
- Content filtering, a report mechanism, and the ability to block abusive users.
- The developer acts on an objectionable content report within 24 hours by removing the content and ejecting the user. Apple 1.2.
- Published contact information.
- For AI generated output, the same moderation applies. The model is a content source. Apple 1.2 and Google AI Generated Content.
- China mainland App Store. An app that enables end-to-end encrypted instant messaging there answers the Security Assessment declaration on App Compliance, including No when that feature is absent, disabled, or geoblocked. The evidence, the failure mode, and the 31 January 2027 date for existing apps are in the AI and generative apps section and in docs/GLOBAL-REGULATORY-2026.md section 3.9.

## Kids category and families

- COPPA, GDPR, and local child law. Under 13 is the COPPA threshold. Persistent identifiers are personal information for a child.
- No third party analytics or behavioral ads. Use only a self certified ads SDK in the families program.
- A valid parental gate for links and purchases, and a neutral age screen for a mixed audience.
- Verifiable Parental Consent where data is collected, which is more than a parental gate. Apple 5.1.4, Google Families.

## Health, fitness, and medical

- Validated health claims only. No unproven measurement from device sensors. Apple 1.4.1.
- Health data never used for advertising, marketing, or data mining. Apple 5.1.2(vi), 5.1.3.
- Informed consent and an ethics review for research apps.
- Special category data under GDPR Article 9 needs explicit consent.
- A medical or regulated entity submits, not an individual. Apple 5.1.1(ix).

## Games

- In app purchase for all digital goods and currency. No external funding of real money play. Apple 3.1.
- Loot boxes and gacha disclose odds before purchase. Google requires a random items disclosure.
- Real money gaming is licensed, geo restricted, free to download, with official rules. Apple 5.3.
- Simulated gambling and social casino is a separate category with its own rating.
- Accurate age rating for the content and any chance mechanics.
- For the per country loot box and gambling rules, see docs/GAMBLING-MATRIX.md.

## macOS and the Mac App Store

- Proper sandboxing and the macOS file system rules. Apple 2.4.5(i).
- Packaged with Xcode, self contained, no third party installer. Apple 2.4.5(ii).
- No auto launch, no Dock icon added without consent, no desktop shortcut left behind. Apple 2.4.5(iii).
- No downloading standalone apps, kexts, or code that adds features. Apple 2.4.5(iv).
- No root escalation or setuid. No custom license key or copy protection screen. No non App Store update mechanism. Apple 2.4.5(v) through (vii).
- Runs on the current shipping OS. Apple 2.4.5(viii).

## AI and generative apps

- AI generated content counts toward the age rating, and a model that can produce sensitive content needs an age restriction. Apple 2026 rules.
- EU AI Act Article 111(4). A system that generates synthetic audio, image, video or text and was placed on the market before 2 August 2026 complies with Article 50(2) machine-readable marking by 2 December 2026.
- EU AI Act Article 5(1)(ba), (bb), (1a) and (1b), from 2 December 2026. Placing on the market or putting into service is prohibited only where generation or manipulation of non-consensual intimate material, or of child sexual abuse material or performance within Directive 2011/93/EU Article 2(c) and (e), is the intended purpose, or is a reasonably foreseeable and reproducible outcome and the system lacks reasonable and adequate safeguards to reliably prevent it and to correct observed or reported misuse. Use is prohibited only where the deployer uses the system for that purpose. A change that does not increase the exposure of depicted intimate parts or alter the nature of depicted sexually explicit activities is not manipulation under point (ba).
- EU AI Act Article 4, replaced 27 July 2026. Providers and deployers take measures to support the development of AI literacy of the people who operate or use the system on their behalf. The duty does not require guaranteeing any specific level of AI literacy of any individual.
- A consent modal naming the AI provider and the data types before any personal data is sent to a third party AI. Apple 5.1.2, enforced since late 2025.
- Moderation, reporting, and blocking on AI output, the same as user content. No NSFW, deepfake, face swap, or undress generation.
- Self harm and crisis safeguards for a companion or character AI.
- Not a thin wrapper over a third party model with no added value. Apple 4.2 and 4.3.
- In a China storefront, references to external AI services such as ChatGPT or Gemini can trigger a regional rejection.
- China mainland App Store. Every app on that storefront answers both App Compliance declarations, including an app that selects No because the feature is absent, disabled, or geoblocked there. The role is Account Holder or Admin, under General. AI-Generated or Synthetic Content covers services such as AI chatbots, image or video generation, and voice and face alteration. A Yes answer needs the approved filing number and registered filing name. If someone else's technology powers the feature, the authorization or usage agreement names the registered foundation model or algorithm and its filing number, names you or your organization as the authorized party, and names an authorizing entity that matches the Cyberspace Administration of China approval registry. Security Assessment covers features such as distributing that content or end-to-end encrypted instant messaging. A Yes answer needs a National Internet Security Management Service Platform screenshot showing the app name, the provider name, and pass or passed review, plus the report with the app name, the provider name, and the company seal or chop. Statuses are Missing Info, Pending Verification, Verification Failed, and Active. If verification fails, the app ships in other selected regions and stays off the China mainland store until a corrected declaration is reviewed with the next version and accepted. Existing apps must be completed and verified by 31 January 2027 to stay available. Source. [Apple, China mainland compliance](https://developer.apple.com/help/app-store-connect/manage-compliance-information/view-china-mainland-compliance-information/).
- A reviewer demo account needs a high or unlimited quota so the feature can be exercised.

## Crypto, finance, and trading

- A finance app is submitted by the company legal entity, not an individual account. Apple 5.1.1(ix) and PLA 1.2.
- Licensing where required, and geo restriction to licensed regions.
- No personal loans over 36 percent APR or under 60 day terms. Apple 3.2.2(ix).
- No binary options, and CFD or FOREX needs proper licensing. Apple 3.2.2(viii).
- NFT purchases through in app purchase, no external buttons or links to buy NFTs.
- Crypto exchange apps come from a licensed exchange in the regions offered.

### Google Play

Read on 27 November 2026 from [Understanding Google Play's Cryptocurrency Exchanges and Software Wallets Policy](https://support.google.com/googleplay/android-developer/answer/16329703?hl=en). The October 2026 change log on that page says the article was updated to accept the Virtual Asset Trading Platform (VATP) license for Hong Kong, to accept a license from the Capital Market Authority (CMA) for the United Arab Emirates, and to add an "Additional Options" section for apps qualifying for local regulatory exemptions. The [policy announcement of 29 October 2026](https://support.google.com/googleplay/android-developer/answer/18100766) lists this under clarifications, and the sentence is: "Cryptocurrency: Expanded Hong Kong licensing requirements to include the Virtual Asset Trading Platform license, and introduced an "Additional Options" section for apps qualifying for local regulatory exemptions." The heading on that list says enforcement standards and practices remain the same. The Capital Market Authority change is stated on the policy page change log.

Declare the app under App Content, in the Financial Features Declaration, as a cryptocurrency exchange and/or software wallet. The page says: "If you don't have the required registration or licensing information for certain locations and none of the additional options apply to you, remove the relevant locations from your app's distribution countries/regions." It also says: "If your distribution country/region is not on the list, you may continue to make your cryptocurrency exchange and software wallet apps available there." Developers are still expected to obtain any additional licensure required per local laws, and Google Play may ask for further information on a jurisdiction that is not listed.

The table is the country list on that page on the read date. Where the software wallet cell says "Same as exchanges", the page uses one cell across both columns, so the exchange wording applies to software wallets as well. Hong Kong and Thailand are the rows with their own software wallet cell, and both say "Not required".

| Country or region | Cryptocurrency exchanges | Cryptocurrency software wallets |
|---|---|---|
| Bahrain | The developer must hold the appropriate Crypto-Asset Services licence from the Central Bank of Bahrain (CBB). | Same as exchanges |
| Canada | The developer must be registered with FINTRAC (CANAFE) as a money services business. | Same as exchanges |
| Hong Kong | The developer must be licensed by the Securities and Futures Commission (SFC) of Hong Kong and obtain one or both of the following, subject to the token classifications on the exchange: (1) a type 1 (dealing in securities) licence and type 7 licence (providing automated trading services), (2) a formal Virtual Asset Trading Platform (VATP) licence. The developer must only offer tokens permitted by the license(s). | Not required |
| Indonesia | The developer must hold the appropriate license from the Otoritas Jasa Keuangan (OJK) as a Digital Financial Asset Trading Provider. | Same as exchanges |
| Israel | The developer must be either (a) licensed by the CMISA (רשות שוק ההון, ביטוח וחיסכון) as a Financial Services Provider or (b) licensed by the Bank of Israel (בנק ישראל) as a banking corporation. | Same as exchanges |
| Japan | The developer must be duly registered as a crypto asset exchange service provider with the Financial Services Agency (金融庁) of Japan. | Same as exchanges |
| Philippines | The developer must have obtained a certificate of authority as a Money Services Business from the Philippine Central Bank (BSP). | Same as exchanges |
| South Africa | The developer must be registered with the Financial Sector Conduct Authority (FSCA). | Same as exchanges |
| South Korea | The developer must have successfully filed a virtual asset service providers (VASP) Report with the Commissioner of the Korea Financial Intelligence Unit (KoFIU). | Same as exchanges |
| Thailand | The developer must have obtained the relevant Digital Asset Business licence from the Securities and Exchange Commission (SEC) of Thailand. | Not required |
| United Arab Emirates | The developer must be licensed by (a) the Financial Services Regulatory Authority (FSRA), (b) the Virtual Asset Regulatory Authority (VARA) or (c) the Dubai Financial Services Authority (DFSA), (d) Capital Market Authority (CMA). | Same as exchanges |
| United Kingdom | The developer must be registered with the Financial Conduct Authority (FCA). | Same as exchanges |
| United States | The developer must be either (a) registered with FinCEN as a Money Services Business and with a state as a money transmitter or (b) a federal or state chartered bank entity. | Same as exchanges |
| European Union. Austria, Belgium, Bulgaria, Croatia, Cyprus, Czechia, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Ireland, Italy, Latvia, Lithuania, Luxemburg, Malta, Netherlands, Poland, Portugal, Romania, Slovakia, Slovenia, Spain, and Sweden. Starting July 2026: Liechtenstein, Iceland, and Norway | The developer must be authorized as a crypto-asset service provider (CASP) under the markets in crypto-assets (MiCA) regulation by a relevant national competent authority. Any other local legal requirements, including any national-level restrictions or requirements beyond MiCA, must also be complied with. Developers from Liechtenstein, Iceland, and Norway. Starting July 2026, developers authorized as a crypto-asset service provider (CASP) under the markets in crypto-assets (MiCA) regulation by a relevant national competent authority from Liechtenstein, Iceland, and Norway, may also distribute to the European Union Member States. | Same as exchanges |

Additional Options. If you do not hold the required local license or registration, and one of the following options applies to your app, select the corresponding option in the Financial Features Declaration. You are responsible for maintaining all relevant supporting documentation and adhering to any additional requirements. The page's preview of those options is:

- I confirm that my app is a non-custodial software wallet.
- I confirm that my app does not offer the purchase, holding, or exchange of cryptocurrencies in this country/region and I have applied the necessary geo-restriction measures.
- I confirm that the availability of my app in this country/region does not require a local license or registration, or is permitted under a valid statutory exemption under applicable local law. I hold supporting documentation and agree to provide this to Google upon request. The app also meets Google Play's mandatory safety requirements: the Full Description for that country includes a disclosure clarifying the entity providing the service and its regulatory status, and at least one of the following is true. 2.1, a valid cryptocurrency exchange or software wallet license in at least one other listed jurisdiction, and/or 2.2, the cryptocurrency services are offered by a publicly traded entity listed on a recognized stock exchange, with the ISIN (International Securities Identification Number) entered. Fulfilling those safety requirements does not impact the app's legal status in that country, and does not substitute any required license, registration, or statutory exemption. The developer has verified compliance with local law and made any necessary adjustments or feature restrictions.

If the regulatory exemption option is selected, acceptable documentation is a formal letter, email, or communication from the local competent regulatory authority confirming the exemption and expressly stating the allowed scope of cryptocurrency exchange and/or software wallet activities, or a legal memorandum or opinion from qualified counsel in that country confirming eligibility for an exemption. Google Play may ask to review it. If the exemption relies on passive availability, the page says not every country recognizes that claim, and the country can be deselected in Play Console.

## VPN and networking

- The NEVPNManager API, and the developer enrolled as an organization. Apple 5.4.
- Declared data use, and no selling or sharing of any data.
- License information in the review notes where a territory requires it.
- Android, no misuse of the VPN service for tracking or ad injection.
