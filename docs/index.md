---
title: App Store and Google Play rejection playbook
description: How to stop App Store and Google Play rejections. Rejection maps, a pre-submission checklist, privacy manifest and Data safety checks, app regulation deadlines, and a guard that runs before you submit.
---

# App Store and Google Play rejection playbook

**The short answer.** Most rejections come from a few causes. A demo account that does not work, a privacy declaration that does not match what the app and its SDKs really collect, missing in-app account deletion, digital goods sold outside in-app purchase, and an incomplete or placeholder build. This playbook maps every common rejection to the rule behind it and the fix, and ships a guard that checks your project before you submit.

- **117 rejection patterns** with the guideline, how to detect it in your code, and the fix.
- **95 regulatory deadlines** across 28 jurisdictions, including the EU AI Act, the Digital Services Act, COPPA and US state age laws.
- **A pre-submission guard** that runs locally or inside AI coding tools like Claude Code, Codex and Cursor.
- Free to read. Source on [GitHub](https://github.com/mjmirza/app-store-compliance).

## Start here

| You are | Read this |
|---|---|
| About to submit | [Pre-submission checklist](PRE-SUBMISSION-CHECKLIST.md) |
| Rejected on the App Store | [Apple rejection map](APPLE.md) |
| Rejected on Google Play | [Google Play rejection map](GOOGLE-PLAY.md) |
| Want to appeal | [Root causes and the appeal playbook](MISTAKE-PATTERNS.md) |
| Building a specific kind of app | [Rejection map by app type](BY-APP-TYPE.md) |
| Using Expo, React Native or Flutter | [Cross-platform frameworks](CROSS-PLATFORM-FRAMEWORKS.md) |

## Laws and deadlines

- [EU rules for apps in 2026](EU-REGULATORY-2026.md). EU AI Act, Digital Services Act trader status, European Accessibility Act, DMA.
- [USA and worldwide rules](GLOBAL-REGULATORY-2026.md). COPPA, state app store accountability acts, UK, Australia, Brazil and more.
- [Regulatory timeline](REGULATORY-TIMELINE.md) and [ruling register](RULING-REGISTER.md).
- [Platform mechanics](PLATFORM-MECHANICS-2026.md). Notarization, Android developer verification, target API level, Play Billing.

## Privacy, security and payments

- [Mobile privacy guide](MOBILE-PRIVACY-MONITOR-2026.md). Privacy manifests, App Tracking Transparency, Google Data safety.
- [Mobile security requirements](MOBILE-SECURITY-2026.md).
- [Loot boxes and gambling by country](GAMBLING-MATRIX.md).
- [Other app stores](OTHER-STORES.md).

## Frequently asked questions

**Why was my app rejected under Apple guideline 2.1?** The reviewer could not fully use the app. Usually a broken demo account, a backend that was down, placeholder content or an in-app purchase that did not load.

**Do I need a privacy manifest?** Yes, for iOS apps that call required-reason APIs, and every third-party SDK must ship its own signed manifest. A missing declaration triggers ITMS-91053 on upload.

**Do I need in-app account deletion?** Yes. Any app that creates accounts must let users delete the account from inside the app, on both stores.

**Can I use Stripe instead of in-app purchase?** Not for digital goods used in the app. Stripe is fine for physical goods and real-world services. US link-out rules changed in 2025.

**How many testers does a new Google Play account need?** New personal developer accounts need a closed test with at least 12 testers for 14 days before production access.

**Does the EU AI Act affect my app?** If an AI feature talks to EU users or generates content, transparency duties apply from 2 August 2026.

More answers in the [Q&A discussions](https://github.com/mjmirza/app-store-compliance/discussions/categories/q-a).

## Run the guard

```bash
git clone https://github.com/mjmirza/app-store-compliance ~/repositories/app-store-compliance
bash ~/repositories/app-store-compliance/scripts/install.sh install
```

Maintained by [Mirza Iqbal](https://github.com/mjmirza). Not affiliated with Apple or Google. App Store is a trademark of Apple Inc. Google Play is a trademark of Google LLC.

<script type="application/ld+json">
{"@context":"https://schema.org","@type":"SoftwareSourceCode","name":"App Store Compliance Playbook","description":"Open playbook and pre-submission guard to stop App Store and Google Play rejections.","codeRepository":"https://github.com/mjmirza/app-store-compliance","programmingLanguage":["Shell","Python"],"author":{"@type":"Person","name":"Mirza Iqbal","url":"https://github.com/mjmirza","sameAs":["https://twitter.com/MirzaJhanzaib","https://next8n.com"]},"keywords":"App Store rejection, Google Play rejection, app review guidelines, privacy manifest, Data safety, account deletion, EU AI Act, COPPA"}
</script>
