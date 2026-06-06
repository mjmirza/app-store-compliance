# Why Apps Get Rejected. Root Cause Taxonomy and Appeal Playbook

Rejection is rarely caused by a lack of knowledge about the rules. It is caused by process gaps that let a known rule slip through. This document names the recurring mistake patterns, the human root cause behind each, and the discipline that prevents it. Then it gives the appeal playbook for when a rejection still lands.

## The meta lesson

The store reviewer is an adversarial integration test that runs once, on a real device, with no access to your intentions and no patience for setup. Every developer who is surprised by a rejection made the same error. They optimized for building the app and treated submission as a final formality, when submission is itself a test with its own preconditions. The fix is to move the review criteria to the front of the process and treat each one as a release blocker, not a last mile checklist.

## The eight root cause patterns

### 1. The invisible feature
Root cause. The reviewer could not reach a feature, so they rejected what they could not see. A login wall with no demo account, a backend that was paused to save cost during review, a feature behind a paywall the reviewer did not buy, a region locked flow.

The discipline. Provide a working demo account and a live backend at submission. Walk the Notes for Review field through every non obvious path. If the reviewer cannot reach it, it does not exist.

### 2. The declaration mismatch
Root cause. What the app does at runtime does not match what was declared. Apple privacy labels or Google Data Safety say one thing while an SDK does another. A purpose string is generic. The listing promises a feature the build lacks.

The discipline. Audit actual runtime data flows, including every third party SDK, against every declaration. The declaration is a contract. Make the app honor it exactly.

### 3. The payment shortcut
Root cause. Trying to avoid the store commission on digital goods by routing payment outside the official billing. License keys, external checkout, crypto, or a web link for in app digital content.

The discipline. Use Apple in app purchase and Google Play Billing for all digital goods unless the app is a documented exempt category. Treat the commission as a cost of distribution, not a bug to route around.

### 4. The thin wrapper
Root cause. Shipping a website in a native shell with no added value. The app is a web view, a marketing page, or a link collection. Apple 4.2 and Google minimum functionality both reject this.

The discipline. Add genuine native capability, offline value, device integration, or content the web version does not have. If the app does nothing beyond the website, it is not ready.

### 5. The spam signature
Root cause. Submitting many near identical apps, duplicate bundle IDs for variations, template or generated apps from a reseller, or a low effort clone in a saturated category. Apple 4.3 and Google spam policy both catch this, and both escalate to account level action.

The discipline. One app per concept, with variations handled as in app content. If a content owner has many properties, the owner submits or uses a single picker app.

### 6. The permission grab
Root cause. Requesting sensitive permissions with no matching core feature. Background location, all files access, SMS or call log, AccessibilityService used for data collection. Google rejects the permission without a qualifying use case, Apple rejects the vague purpose string.

The discipline. Request the minimum. Every sensitive permission must trace to a visible core feature, carry a specific reason string, and use the platform declaration form where required.

### 7. The missing exit
Root cause. The app collects data or creates accounts but gives users no way out. No account deletion inside an app that supports account creation, no consent withdrawal, no privacy policy, social tokens stored off device.

The discipline. Every account creating app needs in app account deletion. Every data collection needs consent and a withdrawal path. The privacy policy must be present, accessible, and accurate.

### 8. The compounding resubmit
Root cause. Treating a rejection as a coin flip and resubmitting the same build hoping for a different reviewer. On Google this is the fastest path from rejection to suspension to account termination.

The discipline. Never resubmit without addressing the cited guideline. Read the exact rule, fix the cause, and reply in the Resolution Center or the Play appeal with what changed.

## Top mistakes to never make

1. Submitting without a working demo account for an account based app.
2. Letting the backend go down or stay in staging during review.
3. A privacy nutrition label or Data Safety form that does not match the SDKs.
4. Generic permission purpose strings that do not name a real reason.
5. No in app account deletion in an app that creates accounts.
6. Selling digital goods outside in app purchase or Play Billing.
7. Loot boxes or random rewards without disclosed odds.
8. Screenshots of a splash or login screen instead of the app in use.
9. Keyword stuffing the name, subtitle, or description.
10. Third party social login with no privacy preserving alternative on Apple.
11. Background location or all files access with no qualifying core feature.
12. Shipping a web wrapper with no added value.
13. Duplicate bundle IDs or many near identical template apps.
14. Skipping the Google closed test of 12 testers over 14 days on a new personal account.
15. Not targeting the current required Android API level.
16. AI features that produce sensitive content without an age restriction.
17. Sharing personal data with a third party AI without a consent modal naming the provider.
18. Not answering Apple's new age rating questionnaire before a 2026 update.
19. References to other platforms or marketplaces inside the app or metadata.
20. Resubmitting an unchanged build after a rejection.

## The appeal playbook

A rejection is recoverable. A bad appeal turns one rejection into a strike.

### Apple. Resolution Center

1. Read the exact guideline number Apple cited. The rejection names it.
2. If it is a misunderstanding, reply in the Resolution Center with a precise explanation, a screenshot or screen recording, and the demo path. Be factual and specific.
3. If it is a real issue, fix it, then in the reply state exactly what changed and where.
4. If you believe the reviewer is wrong on the rules, you can escalate to the App Review Board. Use this sparingly and only with evidence.
5. Never argue the spirit of the rule. Address the cited guideline directly.

### Google. Play Console appeal

1. The enforcement email names the policy and includes appeal instructions. Use that link.
2. State precisely what the app does, why it complies, and what you changed if anything.
3. Fix the declaration mismatch first. Most Google reversals come from correcting the Data Safety form or removing the offending SDK or permission, not from arguing.
4. Do not resubmit the same rejected build in parallel. That compounds strikes.
5. For an account level action, the appeal is the only channel. Be complete and honest, because a second wrong move can be terminal.

### The universal rule of appeals

Address the cited rule, show evidence, change the build if needed, and reply once with everything. Speed comes from precision, not from volume.

## How to operationalize this

Put the pre submission checklist into the definition of done for every release. Run the automated guard before every upload. Keep this taxonomy in code review so a reviewer can name the pattern a change risks. The goal is that no rejection reason in this document can reach submission without a human or a hook catching it first.
