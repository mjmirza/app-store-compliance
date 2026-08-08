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

### Apple AI Policy Migration Checklist
The latest Apple platform policy updates require the following compliance actions:

- **AI-generated content requirements**:
  - [ ] Implement robust output watermarking or metadata tags indicating synthetic media creation.
  - [ ] Perform regular red-teaming and prompt-filtering evaluations of the underlying LLM.
- **App Review AI guidance**:
  - [ ] Add explicit developer notes in App Store Connect explaining the generative features and providing a demo account.
  - [ ] Verify that the app's interactive features do not violate copyright, IP, or Trademark guidelines.
- **Safety expectations**:
  - [ ] Implement mandatory, real-time client or server-side input and output moderation.
  - [ ] Include one-click user reporting/flagging buttons directly adjacent to all AI-generated content blocks.
  - [ ] Provide 24-hour moderation response channels to address user flags or abuse.
- **User disclosure requirements**:
  - [ ] Integrate a prominent in-app consent modal detailing third-party LLM data sharing prior to transmission.
  - [ ] Clearly display a disclosure indicating when the user is interacting with an AI (e.g., EU AI Act compliance).

### Google Play AI Policy Migration Checklist
The latest Google Play platform policy updates require the following compliance actions:

- **Google Play AI policies**:
  - [ ] Ensure that the app does not generate deepfakes, face-swaps, or non-consensual graphic sexual content.
  - [ ] Review Google Play Console Data Safety questionnaires and declare any AI-related data collection/sharing.
- **AI-generated content disclosures**:
  - [ ] Display an explicit, prominent in-app disclosure overlay indicating generative AI outputs are synthetic.
  - [ ] Provide a dedicated link explaining data processing and user privacy policies for the generative models.
- **User safety requirements**:
  - [ ] Provide one-click content flagging/reporting controls on all AI output screens on Android.
  - [ ] Implement automated blocking for malicious or abusive inputs (anti-abuse prompt filtering).

<!-- AI_POLICY_MONITOR_END -->