# Pull Request: US Subscription Cancellation Negative Option Compliance Updates

## Summary
This Pull Request introduces comprehensive configuration, documentation, static auditing, and pre-submission guard updates to support US subscription cancellation (negative option rule) compliance. It ensures that the repository identifies and blocks subscription flows that are easy to start but hard to cancel, complying with the Restore Online Shoppers' Confidence Act (ROSCA), FTC Act Section 5, and state-level negative-option statutes in California, New York, and Massachusetts.

## Background
Negative option marketing—where a consumer's silence or failure to take an affirmative action to reject an offer is interpreted as agreement—has become a major target of regulatory enforcement. While the FTC's federal "Click to Cancel" rule was vacated in July 2025 by the Eighth Circuit, the underlying statutory obligations under ROSCA and FTC Act Section 5 remain in full force. Furthermore, states like California, New York, and Massachusetts enforce their own strict negative-option statutes. A flow requiring a phone call or physical mailing to cancel while allowing online or one-tap signup is a direct violation under these state laws and FTC enforcement guidelines.

## Regulatory change
The legal framework mandates that online subscription services provide a simple, self-service mechanism for consumers to cancel recurring charges. The mechanism must be at least as easy to use as the consent/signup flow (the "click to cancel" or "easy cancel" standard). Specifically:
- Self-service cancellation must be available through the same medium used to sign up (e.g., online/in-app).
- It is unlawful to force customers to make a phone call, mail a physical letter, or visit a physical retail location to cancel when sign-up was completed with a simple online form or in-app tap.

## Official citations
- Priority 1 (Official Sources):
  - Federal Trade Commission (FTC) Act Section 5, 15 U.S.C. Section 45 (Unfair or Deceptive Acts or Practices).
  - Restore Online Shoppers' Confidence Act (ROSCA), 15 U.S.C. Sections 8401-8405.
  - California Automatic Renewal Law (ARL), Cal. Bus. & Prof. Code Sections 17600-17606 (as amended).
  - New York Automatic Renewal Law, N.Y. Gen. Bus. Law Section 527-a.
  - Massachusetts Automatic Renewal Law, Mass. Gen. Laws ch. 93A.
  - FTC Rulemaking: Advanced Notice of Proposed Rulemaking (ANPRM) on Negative Option Rule, 91 FR 10022 (March 11, 2026).
  - Judicial Precedent: Eighth Circuit Court of Appeals Vacatur of 2024 FTC Rule (July 8, 2025).
- Priority 2 (Reputable News):
  - Reuters Legal Regulatory Watch Feed (2025/2026 reports on negative-option enforcement).
  - Bloomberg Law Reports on Automatic Renewal Statutes.

## Affected files
The following files in the repository have been updated to support this compliance tracking:
- `docs/GLOBAL-REGULATORY-2026.md`: Added Section 2.7 detail explaining the negative-option rule, state statutes, and operational scopes, plus Section 5 checklist update.
- `data/rejection-patterns.json`: Added pattern `BOTH-SUBSCRIPTION-HARD-CANCEL` with a high-severity rating, detection signals, and specific fixes under Guideline 3.1.2 / ROSCA.
- `data/detection-recipes.json`: Added corresponding regex-based grep detection recipe for `BOTH-SUBSCRIPTION-HARD-CANCEL` to identify violating cancellation phrases.
- `agent-os/hooks/app-store-compliance-guard.sh`: Wired pattern `BOTH-SUBSCRIPTION-HARD-CANCEL` check into the pre-submission guard script to inspect local directories for violating phrases.
- `agent-os/hooks/app-store-compliance-guard-test.sh`: Integrated explicit unit tests verifying that a directory with a violating subscription cancellation screen (e.g. "call to cancel") is correctly blocked, whereas a clean self-service directory is permitted.

## Risk assessment
- Compliance Risk Level: High
- Risk Description: Submitting or deploying an application containing a subscription billed outside the app store (e.g. via Stripe, PayPal, or custom web portal) that requires a manual phone call, physical mailing, or in-person visit to cancel represents an immediate violation under California, New York, and Massachusetts laws, as well as an FTC ROSCA target. This can lead to class-action litigation, state attorney general enforcement, significant administrative fines, and automatic storefront rejection if detected during Apple/Google platform review.

## Migration steps
To update external subscription funnels to comply with these rules:
1. Identify all subscription products billed outside Apple In-App Purchase or Google Play Billing (e.g., companion web account, Stripe integration).
2. Inspect the user-facing cancellation pathways for these products.
3. Replace any phrases requiring manual intervention, such as:
   - "call us to cancel"
   - "call to cancel"
   - "cancel your subscription by calling"
   - "mail a letter to cancel"
   - "write to cancel"
   - "cancel in person"
   - "visit a store to cancel"
4. Implement a fully self-service "Cancel Subscription" button or accessible self-service settings panel in the app/portal that cancels the recurring payment immediately with no manual verification required.
5. Run `bash agent-os/hooks/app-store-compliance-guard.sh <path-to-project>` on target project to verify no violating phrases remain.

## Backward compatibility
These compliance rules represent purely additive static checks and documentation guidelines. No existing functional APIs, database models, or core interface contracts are broken. All previously valid pre-submission hooks remain compatible, as the script behaves transparently and fail-safe on non-matching project paths.

## Implementation checklist
- [x] Document the regulatory environment and specific state negative-option statutes in `docs/GLOBAL-REGULATORY-2026.md`.
- [x] Define a machine-readable pattern `BOTH-SUBSCRIPTION-HARD-CANCEL` in `data/rejection-patterns.json`.
- [x] Wire the detection recipe into `data/detection-recipes.json`.
- [x] Implement the static grep scanner logic for `BOTH-SUBSCRIPTION-HARD-CANCEL` in `agent-os/hooks/app-store-compliance-guard.sh`.
- [x] Run `python3 scripts/validate.py` to verify pattern database integrity.

## Testing checklist
- [x] Verify that `agent-os/hooks/app-store-compliance-guard-test.sh` contains explicit test cases for `BOTH-SUBSCRIPTION-HARD-CANCEL`.
- [x] Run `bash agent-os/hooks/app-store-compliance-guard-test.sh` and ensure all 17 test cases pass cleanly.
- [x] Test the pre-submission guard against a mock project directory containing violating subscription phrases and confirm that the build is blocked with Exit Code 2.
- [x] Test the pre-submission guard against a clean project directory with self-service cancel flows and confirm it passes with Exit Code 0.

## Documentation checklist
- [x] Document the state automatic renewal laws and FTC Act Section 5/ROSCA guidelines in `docs/GLOBAL-REGULATORY-2026.md`.
- [x] Update the consolidated pre-submission checklist to include the self-service cancellation requirement.
- [x] Ensure `references/rules/payments.md` is regenerated using `python3 scripts/generate-references.py` to include the new pattern.

## Compliance impact
Integrating this compliance check ensures the playbook repository acts as an up-to-date, airtight reference for mobile and cross-platform apps. It mitigates the risk of costly class-action lawsuits, state attorney general investigations, and platform review rejections by proactively catching negative-option violations before submission.

## Breaking changes
There are no breaking changes introduced in this pull request. Existing workflows, CI/CD pipelines, and script arguments remain fully compatible and unaffected.

## Review checklist
- [x] Ensure all documentation and code modifications are completely emoji-free (no emoticons or graphical symbols).
- [x] Confirm that no external non-official blogs or unverified Priority 5 social media rumors were cited for legal/regulatory claims.
- [x] Verify that the static scanner in the guard script is accurate and does not trigger false positives on standard code.
- [x] Check that all JSON files parse successfully and are valid according to `scripts/validate.py`.

## Approver recommendations
- Principal Compliance Counsel: To sign off on automatic renewal laws, ROSCA, and state negative-option statutory alignment.
- Senior Mobile Platform Architect: To verify the accuracy of the regex signatures in the pre-submission guard script.
- Release Quality Assurance Lead: To confirm that the CI/CD guard hook blocks invalid builds correctly without interrupting standard deployment.
