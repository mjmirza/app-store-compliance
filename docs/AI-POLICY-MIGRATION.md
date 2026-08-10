<!-- AI_POLICY_MONITOR_START -->
# AI Policy Monitoring & Compliance Report

This report is continuously generated and updated by `scripts/monitor-ai-policy.py` to keep track of platform policy changes.

## Latest Monitored Policy Changes

### Sample. Apple App Review Guidelines, generative AI section (illustrative) (Apple)
- **Published**: Wed, 01 Apr 2026 10:00:00 PDT
- **Official Link**: [https://developer.apple.com/app-store/review/guidelines/](https://developer.apple.com/app-store/review/guidelines/)
- **Key Topics**: AI-generated content requirements, App Review AI guidance, Safety expectations
- **Details**: Illustrative example only. Apps with generative AI features are expected to implement input/output moderation and user-reporting, disclose data shared with third-party LLM providers, and reflect AI-generated content in the age rating questionnaire. Verify the current wording at the linked guidelines page before citing it as fact.

### Sample. Google Play generative AI content policy (illustrative) (Google Play)
- **Published**: Thu, 02 Apr 2026 09:00:00 PDT
- **Official Link**: [https://play.google/developer-content-policy/](https://play.google/developer-content-policy/)
- **Key Topics**: Google Play AI policies
- **Details**: Illustrative example only. Apps featuring generative AI are expected to disclose AI-generated content, let users flag or report harmful output, and prevent deepfakes, face-swaps, and non-consensual sexual content. Verify the current wording at the linked developer policy center before citing it as fact.

## Automated Migration Recommendations & Implementation Tasks

### Tasks for AI-generated content requirements
- **Recommendation**: Ensure that generative outputs are moderated to prevent inappropriate content.
- [ ] Implement prompt-level filtering for offensive language and inappropriate requests.
- [ ] Use model-based moderation endpoints (e.g. OpenAI Moderation API) before presenting outputs to users.

### Tasks for App Review AI guidance
- **Recommendation**: Ensure compliance with Guideline 4.2 (Minimum Functionality) and Guideline 4.3 (Spam). Do not publish a thin AI wrapper.
- [ ] Review app features to ensure significant unique value-add beyond standard API responses.
- [ ] Document custom templates, UI controls, or workflow integrations in review notes.

### Tasks for Google Play AI policies
- **Recommendation**: Ensure compliance with overall Google Play Developer Policies on AI-generated content.
- [ ] Review Google Play Console declarations regarding AI features.
- [ ] Update developer terms to reflect Google Play rules for generative outputs.

### Tasks for Safety expectations
- **Recommendation**: Provide robust safety filters and reporting mechanisms.
- [ ] Implement a 1-click 'Flag Content' or 'Report Output' button next to all AI-generated texts or images.
- [ ] Establish a 24-hour response SLA for reviewed user reports on generated content.

<!-- AI_POLICY_MONITOR_END -->