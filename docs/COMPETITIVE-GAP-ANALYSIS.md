# Competitive Gap Analysis. What Other Repositories Publish and What We Adopted

This document is the result of surveying the open source repositories that already publish App Store and Google Play compliance knowledge, studying why each one exists and what it captures, finding the gaps against this playbook, and folding the missing patterns back in. It is maintained so this playbook stays the most complete open reference, not a snapshot.

Method. Each repository was read in full through the GitHub API, its structure and unique content extracted, then compared field by field against this playbook. The gaps it surfaced are listed, and the ones we adopted are marked.

## The repositories surveyed

| Repository | Stars | What it publishes | Why it exists |
|---|---|---|---|
| truongduy2611/app-store-preflight-skills | about 1,224 | An AI agent skill that scans an iOS or macOS project, pulls App Store Connect metadata through the asc CLI, and checks it against a full index of 100 plus guidelines organized into 10 app type checklists | The most popular comparable. Built so an agent catches rejections before submission, the same goal as this playbook |
| lukylab/appstore-submission-checklist | about 17 | Two practical checklists, one for new app submissions and one for app updates, from an indie developer with 10 plus live apps | New apps and updates fail review for different reasons, so it splits the two |
| andrewmcwattersandco/app-store-rejections | about 14 | A community collection of real, named App Store rejection stories with links | To warn developers of marketplace risk and encourage self publishing |
| jaywcjlove/app-rejection-fixes | small | Rejection reasons paired with the fix that cleared each | A working developer logging the rejections they hit and resolved |
| hnxyzhw/AppStoreReviewsAndRejected | small | The actual Apple rejection email texts, by guideline, with the Chinese translation and the fix | Captures the exact reviewer wording, which is the most concrete signal of what triggers a rejection |
| aashishtamsya/Appstore-Review-Guidelines | about 90 | An older curated guideline list by category | An early community attempt at a pre submission reference |

## Gaps these repositories surfaced, and what we adopted

### 1. App type specific checklists. ADOPTED

The most popular repository organizes its checks into ten app types, because a games app and a finance app fail for very different reasons. Our playbook was flat. We adopted this as a new doc, `BY-APP-TYPE.md`, mapping each app type to the critical guidelines that hit it. This is the single biggest structural improvement from the survey.

### 2. macOS as a first class target. ADOPTED

The leader covers macOS and the Mac App Store as a distinct checklist. Our playbook covered iOS and Android. macOS has its own rules, sandboxing, notarization, no non App Store update mechanism, and the 2.4.5 Mac specific set. We added a macOS section to the by app type doc.

### 3. Pulling real App Store Connect metadata. ADOPTED as guidance

The leader integrates the asc CLI to pull the live listing metadata and inspect it, rather than only scanning source. Our guard scans source. We added guidance to the skill that the strongest audit pulls the real App Store Connect metadata, with the asc CLI or the App Store Connect API, and checks the words in the live listing, because a large share of rejections are metadata, not code.

### 4. Specific metadata rejection rules. ADOPTED into the taxonomy

The leader and the Chinese rejection email collection name precise triggers we did not have as patterns.

- Apple device images or the Apple trademark in the app icon or screenshots, guideline 5.2.5.
- Device frames around the app in preview videos, guideline 2.3.4.
- Subscription pricing that shows the monthly price more prominently than the actual billed amount, guideline 3.1.2.
- Missing Terms of Use or EULA and Privacy Policy links for a subscription, guideline 3.1.2.
- In a China storefront, references to external AI services such as ChatGPT or Gemini can trigger a regional rejection.
- Review notes for a new submission that omit a screen recording, the app purpose, test credentials, external service details, regional information, or regulatory documents, guideline 2.1.

### 5. The user generated content 24 hour rule. ADOPTED

The real Safety 1.2 rejection email in the Chinese collection states the exact requirement. The developer must act on an objectionable content report within 24 hours by removing the content and ejecting the user. Our 1.2 coverage named filtering, reporting, and blocking, but not the 24 hour action window and the EULA with zero tolerance. Both are now captured.

### 6. Financial apps require a company developer account. ADOPTED

The PLA 1.2 rejection email shows that a financial app submitted under an individual account is rejected. This reinforces our 5.1.1(ix) regulated fields rule, now stated plainly for finance.

### 7. New app versus update split. ADOPTED into the checklist

An update fails for different reasons than a first submission. Our checklist is now framed so the first submission items, demo account, review notes, and metadata, are clearly the heavy ones, and the update items focus on what changed.

### 8. Real rejection case studies. ADOPTED into the mistake patterns

The community collections hold named, real rejections that teach more than an abstract rule. The Halide camera app rejected for not explaining why it uses the camera, the iDOS emulator takedown, and the pattern of a long lived app pulled for not being updated. These are now examples in the mistake patterns doc.

### 9. A guideline history reference. ADOPTED as a reference

The checklist repository points at the App Store Review Guidelines History site, which tracks how the guidelines changed over time. Useful when a rejection cites a rule that was recently reworded.

## What we already had that they did not

This survey also confirmed where this playbook is ahead.

- Google Play depth. Most comparable repositories are iOS only. This playbook carries the full Google Play policy map, the four level enforcement ladder, the 12 tester rule, and Data Safety.
- The legal layer. None of the surveyed repositories cover GDPR lawful basis, the EU AI Act, the DSA, or COPPA depth. This playbook does, with the explicit framing that store compliance is not legal compliance.
- Cross store coverage. Huawei, the Chinese stores, Samsung, Amazon, Microsoft, and RuStore, in `OTHER-STORES.md`.
- A working automated guard with a test suite, not only a written checklist.

## The standing process

This analysis is repeatable. When a new comparable repository appears, read it through the API, extract its structure and unique rules, diff against this playbook, and fold in the net new patterns. Contributions that bring a pattern from another open source list are welcome, with a link to the source.
