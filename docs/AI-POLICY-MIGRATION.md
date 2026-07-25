# AI Policy Migration Guide

This document details platform policy updates regarding AI integrations and specifies required migration tasks for compliance.

## Policy Updates Monitored

### Google Play AI safety rules update
- **Source Link**: https://play.google/developer-content-policy/ai-safety
- **Updated Date**: Mon, 15 Jun 2026 00:00:00 GMT
- **Description Summary**: Google Play requires prominent AI generation labels and safety filters.

## Codebase Scan Results

Statically scanned the codebase for AI integration keywords (OpenAI, Anthropic, Gemini, stable diffusion, completions, etc.).

No active AI integrations were detected in source code files. (Note: Platform requirements apply immediately upon introducing generative AI features).

## Required Compliance Migration Tasks

Based on Apple and Google Play AI policy updates, the following tasks must be completed for any active AI features:

### Task 1: User Consent and Disclosure Modal
- **Platform**: Apple (Guideline 5.1.2(i)) and Google Play
- **Requirement**: Prior to transmitting any personal user data to a third-party AI provider or LLM endpoint, present an explicit consent modal. This modal must name the provider (e.g., OpenAI, Anthropic) and declare the precise data types shared.
- **Action**: Design and implement a native consent dialog or sheet and store user preference in secure local storage.

### Task 2: Robust Content Filtering and Moderation
- **Platform**: Both (Apple UGC Guideline 1.2 and Google Play AI Policy)
- **Requirement**: Implement input and output filtering on all prompt flows to block and filter self-harm, hate speech, NSFW content, deepfakes, and other prohibited materials.
- **Action**: Route prompt and response payloads through automated moderation APIs (such as OpenAI Moderation API) before presenting outputs to users.

### Task 3: In-App User Reporting and Blocking Mechanism
- **Platform**: Both (Apple UGC Guideline 1.2 and Google Play AI Policy)
- **Requirement**: Provide clear, accessible UI elements for users to report offensive AI-generated outputs and flag abusive content.
- **Action**: Add a report/flag button adjacent to every AI-generated message or output block, and record reports in the backend for moderator review.

### Task 4: Store Metadata and Age Rating Adjustments
- **Platform**: Both (Apple 2026 age rating rules and Google Play)
- **Requirement**: Adjust the store listing questionnaires. AI-generated content capabilities require higher age ratings and clear disclosure descriptions in the store metadata.
- **Action**: Complete the 2026 age rating questionnaire in App Store Connect and update the Google Play Content Rating Form.
