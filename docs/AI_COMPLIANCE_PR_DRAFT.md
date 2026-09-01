# PULL REQUEST DRAFT: Platform-Specific AI Policy Compliance Update

## 1. Summary
This pull request brings the application into complete compliance with the latest platform-specific AI policies. It implements robust user disclosure, consent modals, output filtering, and content reporting mechanisms to prevent potential rejections during App Store and Google Play reviews.

## 2. Background
Both Apple and Google Play have tightened their restrictions regarding generative AI features inside mobile apps. Review systems are now actively rejecting applications that send user data to third-party LLM APIs without transparent consent or that display generative content without moderation safeguards.

## 3. Regulatory change
- **Apple (Guidelines 1.2, 5.1.2(i), and 2.3.6)**: Requires clear disclosure of third-party AI data sharing, explicit user consent prior to transmission, content filters for output safety, and reflection of chat assistants in the age rating.
- **Google Play (AI-Generated Content Policy)**: Enforces mandatory user-facing disclosures, user flagging/reporting mechanisms for offensive AI-generated content, and zero-tolerance for deepfakes, face-swapping, or non-consensual graphic outputs.

## 4. Official citations
- [Sample. Apple App Review Guidelines, generative AI section (illustrative)](https://developer.apple.com/app-store/review/guidelines/) (Apple Update, Wed, 01 Apr 2026 10:00:00 PDT)
- [Sample. Google Play generative AI content policy (illustrative)](https://play.google/developer-content-policy/) (Google Play Update, Thu, 02 Apr 2026 09:00:00 PDT)

## 5. Affected files
- `./AGENTS.md`
- `./CHANGELOG.md`
- `./README.md`
- `./agent-os/commands/app-store-audit.md`
- `./data/detection-recipes.json`
- `./data/rejection-patterns.json`
- `./docs/ADVANCED-2026.md`
- `./docs/AI-POLICY-MIGRATION.md`
- `./docs/AI_COMPLIANCE_PR_DRAFT.md`
- `./docs/ANDROID-POLICY-MIGRATION.md`
- `./docs/APPLE.md`
- `./docs/BY-APP-TYPE.md`
- `./docs/COMPETITIVE-GAP-ANALYSIS.md`
- `./docs/EU-REGULATORY-2026.md`
- `./docs/REGULATORY-GAP-REPORT-2026.md`
- `./references/guidelines/by-app-type/ai-and-generative-apps.md`
- `./references/rules/metadata.md`
- `./references/rules/privacy.md`
- `./references/rules/safety.md`
- `./templates/REVIEW-NOTES-TEMPLATE.md`

## 6. Risk assessment
- **Risk Level**: High
- **Consequences of non-compliance**: Immediate rejection of app updates by Apple App Review and potential Google Play suspension or removal under their AI-generated content guidelines.
- **Mitigation plan**: Build interactive user consent, prominent disclosure overlays, content moderation filters, and clear flagging UI.

## 7. Migration steps
1. **Consent Modal**: Add an in-app consent modal detailing that third-party AI/LLM components are used and get explicit consent before sending user personal data.
2. **Output Moderation**: Wire real-time prompt/response filters to detect, flag, and filter out objectionable or NSFW AI content.
3. **Age Rating Update**: Update the age rating questionnaire in App Store Connect to account for interactive AI chat functionality.
4. **Prominent Disclosure**: Implement an in-app disclaimer and user consent sheet for generative content on Android devices.
5. **Content Safety Controls**: Add a prominent 'report content' or 'flag output' UI element directly on all AI output cards.
6. **Terms of Service update**: Declare user safety requirements regarding deepfakes and non-consensual content generation.

## 8. Backward compatibility
All changes are purely additive. Older clients will default to safe local fallback content or receive standard prompts. Data structures, local schema versions, and existing preferences remain fully backward compatible.

## 9. Implementation checklist
- [ ] Create `ConsentModalView` and integrate it into onboarding/settings.
- [ ] Integrate OpenAI/Anthropic moderation API or client-side bad-word list.
- [ ] Add reporting and content flag buttons next to AI-generated messages.
- [ ] Recheck App Store Connect questionnaire for Guideline 1.2 and 2.3.6 updates.
- [ ] Implement a prominent Play Policy disclosure dialog on app launch or AI feature access.
- [ ] Implement one-click reporting next to every AI output block on Android.
- [ ] Prevent face-swap and image generation capabilities if NSFW/deepfake models can be accessed.
- [ ] Update the Google Play Console Data Safety form declarations.
- [ ] Update `docs/ADVANCED-2026.md` and related compliance manuals.

## 10. Testing checklist
- [ ] Verify that the consent modal triggers and blocks data send until approved.
- [ ] Verify that prompt injection attempts and inappropriate topics trigger the moderation filter.
- [ ] Test the content flagging button and verify reports are logged on the server.
- [ ] Test on both iOS and Android emulators/devices for layout adjustments.

## 11. Documentation checklist
- [ ] Update the Privacy Policy URL with third-party AI disclosure details.
- [ ] Update App Store Connect "Notes for Review" with demo credentials and compliance instructions.
- [ ] Update Google Play Console Data Safety questionnaire declarations.
- [ ] Document moderation guidelines in the repository's wiki or `docs/` folder.

## 12. Compliance impact
- **Apple App Store**: Aligns with 2026 guidelines; secures safe passage through human and automated reviews.
- **Google Play**: Safeguards developer account health and retains age-appropriate content standing.
- **EU AI Act**: Fulfills Article 50 transparency requirements for AI-generated interaction.

## 13. Breaking changes
- No breaking database schema migrations.
- UI flow changes include a mandatory, one-time consent prompt when first accessing AI-powered features.

## 14. Review checklist
- [ ] Code complies with all architectural boundaries and secure API storage rules.
- [ ] Consent modal text is clear, localized, and lists the AI sub-processors.
- [ ] Verification tests for the content moderation engine pass.

## 15. Approver recommendations
Ensure that the privacy consent modal explicitly mentions the specific third-party AI processor (e.g., OpenAI, Anthropic, Gemini) as mandated by Apple 5.1.2(i). Confirm that the content reporting UI is functional and triggers 24-hour moderation capabilities.
