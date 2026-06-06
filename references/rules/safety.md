# Rules. Safety and user generated content

2 rules in this category. Generated from data/rejection-patterns.json. Each rule names the guideline, the severity, what triggers it, and the fix.

## APPLE-1.2-UGC-24H-ACTION

- Title. User generated content without the 24 hour action mechanism
- Platform. apple
- Guideline or policy. 1.2
- Severity. critical
- What triggers it. UGC present without a EULA with zero tolerance for objectionable content, content filtering, a flag mechanism, user blocking, and the ability to act on a report within 24 hours by removing content and ejecting the user.
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
