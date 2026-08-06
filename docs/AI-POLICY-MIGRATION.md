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

### Tasks for Apple AI Compliance
- **Regulatory Status**: High priority. Apple App Store compliance gate requirement.
- [ ] **Task 1**: Implement real-time output filters and NSFW/objectionable content classifiers for any interactive AI feature.
- [ ] **Task 2**: Add a prominent in-app consent modal detailing third-party LLM processors (e.g. OpenAI, Anthropic, Gemini) and list specific data types shared with them.
- [ ] **Task 3**: Create an AI content reporting and flagging interface directly inside the chat/generation view allowing 24-hour moderation action.
- [ ] **Task 4**: Recheck and re-answer the age rating questionnaire in App Store Connect to ensure AI content is accounted for.

### Tasks for Google Play AI Compliance
- **Regulatory Status**: High priority. Google Play Developer console requirement.
- [ ] **Task 1**: Implement an in-app prominent disclosure dialog explaining generative AI features and content safety expectations.
- [ ] **Task 2**: Add a simple, one-click content flagging/reporting action next to all AI outputs on Android.
- [ ] **Task 3**: Ensure robust content guards to block synthesis of deepfakes, face-swaps, and non-consensual graphic or sexual media.
- [ ] **Task 4**: Update the Google Play Console Data Safety form to declare any user-generated data processed or uploaded for LLM endpoints.

<!-- AI_POLICY_MONITOR_END -->