# Rules. Safety and user generated content

4 rules in this category. Generated from data/rejection-patterns.json. Each rule names the guideline, the severity, what triggers it, and the fix.

## APPLE-1.2-UGC-24H-ACTION

- Title. User generated content without the required moderation mechanisms
- Platform. apple
- Guideline or policy. 1.2
- Severity. critical
- What triggers it. UGC present without content filtering, a mechanism to report offensive content with timely responses to concerns, the ability to block abusive users, and published contact information. Verified against the live guideline 2026-08-30, which requires timely responses rather than a fixed 24 hour deadline. Since 8 June 2026 guideline 1.2 states that egregious or repeated behavior is grounds for immediate removal from the App Store and from the Apple Developer Program, and 1.2.1(a) requires creator apps to gate over-rating content on verified or declared age. Since 16 October 2026 guideline 1.2 names the app types it covers, social media, user-generated content platforms, and AI content creation apps, lists nonconsensual intimate imagery among the harms, and states that failing to implement appropriate safeguards or to remediate violations after notice may be a Developer Code of Conduct violation.
- How to fix it. Add a zero tolerance EULA, content filtering, in app reporting, user blocking, published contact information, and a process that acts on reports and Apple notices in a timely way. Remediate every violation Apple identifies, because failing to remediate after notice may breach the Developer Code of Conduct. Source. real Apple Safety 1.2 rejection email, and https://developer.apple.com/news/?id=92th7e5i.
- Detection signals. post, comment, upload, chat, feed, community
- Present means handled. report, block user, EULA, moderation

How to detect.

```bash
grep -rni 'post\|comment\|upload\|feed\|community' --include='*.swift' . && ! grep -rni 'report\|block user\|EULA\|moderation' --include='*.swift' .
```

## APPLE-5-TRAFFICKING-CHILD-EXPLOITATION

- Title. App that facilitates human trafficking or the exploitation of children
- Platform. apple
- Guideline or policy. 5
- Severity. critical
- What triggers it. Since 16 October 2026 the Legal section states that apps found to facilitate human trafficking or the exploitation of children are reported to the authorities, removed from the App Store, and blocked from alternative distribution. The risk sits with marketplaces, classifieds, escort or companion listings, anonymous contact, and any surface where adults reach minors. Checked by hand.
- How to fix it. Moderate listings and messaging for trafficking and child exploitation signals, verify ages where adults can reach minors, report CSAM to NCMEC as US law requires, and keep the reporting path from guideline 1.2. Sources. https://developer.apple.com/news/?id=92th7e5i, https://developer.apple.com/news/?id=vvzx6cul

## BOTH-AI-GENERATED-CONTENT

- Title. Generative AI output without moderation or safeguards
- Platform. both
- Guideline or policy. Apple 1.2, Google AI Generated Content
- Severity. high
- What triggers it. A generative AI or image generation integration is present without content filtering, reporting, blocking, age rating, or abuse safeguards. Apple applies UGC rules to AI output. Google has a dedicated AI Generated Content policy. Since 16 October 2026 Apple 1.2 names AI content creation apps explicitly and requires them to prevent and remove nonconsensual intimate imagery, including AI-generated imagery (https://developer.apple.com/news/?id=vvzx6cul).
- How to fix it. Add moderation, reporting, blocking, an accurate age rating, and abuse safeguards. Prevent NSFW, deepfake, face swap, and undress generation.
- Detection signals. openai, anthropic, stable diffusion, image generation, chat/completions, text-to-image
- Present means handled. moderation, report, block user, content filter

How to detect.

```bash
grep -rni 'api.openai.com\|anthropic\|generativelanguage\|stable diffusion\|text-to-image' . && ! grep -rni 'moderation\|report\|block user\|content filter' .
```

## BOTH-GPSR-COMPLIANCE-MISSING

- Title. Missing EU GPSR manufacturer info or product safety warning disclosures
- Platform. both
- Guideline or policy. Regulation (EU) 2023/988 (EU General Product Safety Regulation)
- Severity. high
- What triggers it. E-commerce or digital product listing present but missing manufacturer email, postal address, or product safety warnings on the interface.
- How to fix it. Provide prominent manufacturer contact details (email and postal address) and any applicable product safety warnings directly on the product listing or online interface for any consumer goods distributed in the EU.
- Detection signals. productListing, buyProduct, checkout, e-commerce, manufacturerInfo, safetyWarning
- Present means handled. manufacturerEmail, manufacturerAddress, safetyLabel, productSafety, responsiblePerson

How to detect.

```bash
grep -rniE 'gpsr|general product safety|product safety|manufacturerInfo|safetyWarning' . 2>/dev/null
```
