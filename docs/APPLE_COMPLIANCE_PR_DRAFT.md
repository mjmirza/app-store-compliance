# Compliance Update: Integrating HealthKit and Human Interface Guidelines for iOS 18

## Summary
This pull request drafts the necessary repository adjustments to address Apple's recent policy update: "Integrating HealthKit and Human Interface Guidelines for iOS 18". This update has been classified with a Release Impact of High.

## Background
Apple regularly updates its requirements, guidelines, and agreements to maintain user privacy, enhance platform stability, and respond to regulatory shifts. This background context details the operational motivation behind the policy "Integrating HealthKit and Human Interface Guidelines for iOS 18" and its intersection with developers' obligations.

## Regulatory change
The core change involves the following updated Apple developer program requirements:
Human Interface Guidelines, HealthKit policies, Minimum SDK versions

Specifically, Apple has modified policy thresholds or introduced new validation mandates which developers must satisfy to avoid service disruption or review failures.

## Official citations
According to the official announcement published by Apple Developer News:
Citation Link: https://developer.apple.com/news/?id=healthkit-hig-ios18
Publication Date: 2026-05-01
" New design layouts in the Human Interface Guidelines (HIG) introduce specific standards for fitness apps. Developers integrating HealthKit must comply with clinical health records sharing policies and use Apple-approved layouts. "

## Affected files
The following repository locations are identified as affected or relevant to this compliance update:
- README.md: This file matches keywords of the updated requirements.
- agent-os/hooks/app-store-compliance-guard.sh: This file matches keywords of the updated requirements.
- agent-os/skill/SKILL.md: This file matches keywords of the updated requirements.
- data/detection-recipes.json: This file matches keywords of the updated requirements.
- data/rejection-patterns.json: This file matches keywords of the updated requirements.
- docs/ADVANCED-2026.md: This file matches keywords of the updated requirements.
- docs/APPLE.md: This file matches keywords of the updated requirements.
- docs/APPLE_COMPLIANCE_PR_DRAFT.md: This file matches keywords of the updated requirements.
- docs/BY-APP-TYPE.md: This file matches keywords of the updated requirements.
- docs/EU-REGULATORY-2026.md: This file matches keywords of the updated requirements.
- docs/GLOBAL-REGULATORY-2026.md: This file matches keywords of the updated requirements.
- docs/OPEN-SOURCE-PATTERNS.md: This file matches keywords of the updated requirements.
- docs/PLATFORM-MECHANICS-2026.md: This file matches keywords of the updated requirements.
- docs/PRE-SUBMISSION-CHECKLIST.md: This file matches keywords of the updated requirements.
- docs/apple_pr_draft_alternative_payment_options_and_dma_compliance_in_the_european_union.md: This file matches keywords of the updated requirements.
- docs/apple_pr_draft_app_review_guidelines_updated_for_ai_generated_content_and_safety.md: This file matches keywords of the updated requirements.
- docs/apple_pr_draft_app_store_submissions_now_require_xcode_17_and_swift_6.md: This file matches keywords of the updated requirements.
- docs/apple_pr_draft_apple_developer_program_license_agreement_update_and_app_store_connect_enhancements.md: This file matches keywords of the updated requirements.
- docs/apple_pr_draft_enforcing_privacy_manifests_and_required_reason_apis.md: This file matches keywords of the updated requirements.
- docs/apple_pr_draft_new_accessibility_mandates_under_european_accessibility_act.md: This file matches keywords of the updated requirements.
- docs/apple_pr_draft_privacy_updates_for_location__camera__microphone__and_app_tracking_transparency.md: This file matches keywords of the updated requirements.
- docs/apple_pr_draft_security_enhancements__push_notifications__and_background_execution_policies.md: This file matches keywords of the updated requirements.
- references/guidelines/by-app-type/ai-and-generative-apps.md: This file matches keywords of the updated requirements.
- references/guidelines/by-app-type/health-fitness-and-medical.md: This file matches keywords of the updated requirements.
- references/rules/android.md: This file matches keywords of the updated requirements.
- references/rules/design.md: This file matches keywords of the updated requirements.
- references/rules/entitlements.md: This file matches keywords of the updated requirements.
- references/rules/export.md: This file matches keywords of the updated requirements.
- references/rules/metadata.md: This file matches keywords of the updated requirements.
- references/rules/payments.md: This file matches keywords of the updated requirements.
- references/rules/performance.md: This file matches keywords of the updated requirements.
- references/rules/privacy.md: This file matches keywords of the updated requirements.
- references/rules/safety.md: This file matches keywords of the updated requirements.
- scripts/generate-references.py: This file matches keywords of the updated requirements.
- scripts/metadata-audit-test.sh: This file matches keywords of the updated requirements.
- scripts/metadata-audit.py: This file matches keywords of the updated requirements.
- scripts/monitor-apple-test.sh: This file matches keywords of the updated requirements.
- scripts/monitor-apple.py: This file matches keywords of the updated requirements.
- scripts/validate.py: This file matches keywords of the updated requirements.

## Risk assessment
Failure to address this update carries the following technical and operational risks:
- Severity level: High
- Primary risk: The update involves regulatory, legal, or review guidelines changes that could result in rejection during human review.
- Direct consequences include automated binary upload rejections, review delays, app suspension, or potential developer account flags.

## Migration steps
To achieve full compliance, perform the following step-by-step migration:
1. Review the official announcement details at the cited URL.
2. Inspect the identified affected files and locate relevant configurations.
3. Apply the specific code or configuration adjustments listed in the implementation checklist.
4. Regenerate local build configurations and verify local compilation.
5. Run automated compliance lints or pre-submission guard checks.

## Backward compatibility
This compliance change has been analyzed for backward compatibility:
- Support for older iOS/macOS client versions remains stable unless specifically noted otherwise.
- Configuration adjustments (such as adding key-value entries to plist files or manifests) are safe and do not degrade functionality on older runtimes.

## Implementation checklist
Complete the following implementation items:
- [ ] Audit layout and interaction design against HIG recommendations
- [ ] Add NSHealthShareUsageDescription and NSHealthUpdateUsageDescription in Info.plist
- [ ] Ensure clinical health data usage conforms to privacy policies
- [ ] Verify deployment target is set correctly in build configurations
- [ ] Update minimum supported iOS version in CI/CD pipeline definitions
- [ ] Verify compliance version numbers match Apple minimum specifications
- [ ] Clean up any legacy or deprecated API endpoints in conflict with this update

## Testing checklist
Execute the following verification and validation steps:
- [ ] Build the application locally with target SDKs
- [ ] Run automated compliance scripts such as scripts/validate.py
- [ ] Perform a clean build and upload to TestFlight to verify submission pipelines
- [ ] Test the affected features on a physical device running the target OS version

## Documentation checklist
Update the following documentation assets:
- [ ] Record compliance changes in docs/APPLE-POLICY-MIGRATION.md
- [ ] Update inline code comments to explain compliance-driven configurations
- [ ] Revise the relevant sections of references/ or playbooks if guidelines have altered

## Compliance impact
This update relates to broader compliance domains:
- Jurisdictional alignment: Ensures the application complies with regional requirements, data privacy principles, and global consumer trust frameworks.

## Breaking changes
No structural breaking changes to public APIs are expected from this update unless specified in the announcement. Existing user databases, credentials, and app states are preserved.

## Review checklist
Reviewers must confirm the following before approval:
- [ ] All 15 required sections of this pull request are comprehensive and complete.
- [ ] Code adjustments align strictly with Priority 1 official sources.
- [ ] No emojis or graphical symbols have been introduced in the PR, documentation, or code.

## Approver recommendations
The following roles are recommended to sign off and approve this compliance pull request:
- Lead iOS Development Engineer: To verify build, runtime, and SDK configuration safety.
- Compliance and Privacy Officer: To verify compliance with global policies and official standards.
- QA Technical Lead: To confirm successful testing on target physical devices.
