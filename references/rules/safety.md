# Rules. Safety and user generated content

3 rules in this category. Generated from data/rejection-patterns.json. Each rule names the guideline, the severity, what triggers it, and the fix.

## APPLE-1.2-UGC-24H-ACTION

- Title. User generated content without the required moderation mechanisms
- Platform. apple
- Guideline or policy. 1.2
- Severity. critical
- What triggers it. UGC present without content filtering, a mechanism to report offensive content with timely responses to concerns, the ability to block abusive users, and published contact information. Verified against the live guideline 2026-08-30, which requires timely responses rather than a fixed 24 hour deadline. Since 8 June 2026 guideline 1.2 states that egregious or repeated behavior is grounds for immediate removal from the App Store and from the Apple Developer Program, and 1.2.1(a) requires creator apps to gate over-rating content on verified or declared age.
- How to fix it. Add a zero tolerance EULA, content filtering, in app reporting, user blocking, and a process to act on reports within 24 hours. Source. real Apple Safety 1.2 rejection email.
- Detection signals. post, comment, upload, chat, feed, community
- Present means handled. report, block user, EULA, moderation

How to detect.

```bash
grep -rni 'post\|comment\|upload\|feed\|community' --include='*.swift' . && ! grep -rni 'report\|block user\|EULA\|moderation' --include='*.swift' .
```

## BOTH-AI-GENERATED-CONTENT

- Title. Generative AI output without moderation or safeguards
- Platform. both
- Guideline or policy. Apple 1.2, Google AI Generated Content
- Severity. high
- What triggers it. A generative AI or image generation integration is present without content filtering, reporting, blocking, age rating, or abuse safeguards. Apple applies UGC rules to AI output. Google has a dedicated AI Generated Content policy.
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
