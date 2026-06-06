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
- A consent modal naming the AI provider and the data types before any personal data is sent to a third party AI. Apple 5.1.2, enforced since late 2025.
- Moderation, reporting, and blocking on AI output, the same as user content. No NSFW, deepfake, face swap, or undress generation.
- Self harm and crisis safeguards for a companion or character AI.
- Not a thin wrapper over a third party model with no added value. Apple 4.2 and 4.3.
- In a China storefront, references to external AI services such as ChatGPT or Gemini can trigger a regional rejection.
- A reviewer demo account needs a high or unlimited quota so the feature can be exercised.

## Crypto, finance, and trading

- A finance app is submitted by the company legal entity, not an individual account. Apple 5.1.1(ix) and PLA 1.2.
- Licensing where required, and geo restriction to licensed regions.
- No personal loans over 36 percent APR or under 60 day terms. Apple 3.2.2(ix).
- No binary options, and CFD or FOREX needs proper licensing. Apple 3.2.2(viii).
- NFT purchases through in app purchase, no external buttons or links to buy NFTs.
- Crypto exchange apps come from a licensed exchange in the regions offered.

## VPN and networking

- The NEVPNManager API, and the developer enrolled as an organization. Apple 5.4.
- Declared data use, and no selling or sharing of any data.
- License information in the review notes where a territory requires it.
- Android, no misuse of the VPN service for tracking or ad injection.
