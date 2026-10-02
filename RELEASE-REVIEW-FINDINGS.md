# Release Review Audit Findings

Audited Date: October 2, 2026
Overall Release Status: BLOCKED
Audited Platforms: Apple App Store, Google Play Store

## Executive Summary

This comprehensive release review evaluates current release readiness across all fifteen required compliance and App Store / Google Play submission domains. The release is currently BLOCKED due to one critical severity issue in the release deployment pipeline (`APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED`), alongside five high severity issues and two medium severity issues that must be addressed prior to store submission and release authorization.

## Verification Summary Across 15 Submission Areas

| Verification Area | Status | Severity | Findings Summary | Recommended Action |
| --- | --- | --- | --- | --- |
| 1. Permissions | PASSED | None | No ungrounded sensitive permissions or missing purpose strings found. | Maintain current Info.plist and AndroidManifest permission rationale declarations. |
| 2. Privacy Disclosures | ADVISORY | HIGH | Missing declared Privacy Policy URL in listing metadata. | Configure valid Privacy Policy URL in App Store Connect and Google Play Console. |
| 3. Screenshots | PASSED | None | Metadata screenshots meet standard framing and feature representation guidelines. | Ensure full-screen feature captures without device frames or competitor trademarks. |
| 4. Metadata | ADVISORY | HIGH / MEDIUM | Placeholder content, cross-platform references, future feature promises, and negative Apple sentiment in copy. | Replace placeholders, remove "Google Play" references, and eliminate "coming soon" or bug-related copy. |
| 5. Age Rating | BLOCKED | CRITICAL | Pipeline uses deprecated App Store Connect API age-rating endpoint (`APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED`). | Upgrade pipeline to ASC API 4.4+ age-rating declaration read/update endpoints. |
| 6. AI Disclosures | ADVISORY | HIGH | Moderation and content safety safeguards required for generative AI integration. | Enforce EU AI Act Article 50 disclosures, content moderation, and age restrictions. |
| 7. Subscription Disclosures | ADVISORY | HIGH / MEDIUM | Hard-cancellation pattern detected requiring non-self-service actions. | Provide self-service in-app or web subscription cancellation at least as easy as sign-up. |
| 8. Payment Compliance | ADVISORY | HIGH | Random reward / loot box mechanic missing explicit odds disclosure before purchase. | Disclose odds for all random reward mechanics prior to user purchase (Apple 3.1.1 / Google Play). |
| 9. Accessibility | PASSED | None | Static accessibility audit passed with 0 regressions. | Maintain WCAG 2.1 AA / EN 301 549 standards for VoiceOver, TalkBack, and Dynamic Type. |
| 10. Legal Documents | ADVISORY | HIGH | Random reward odds disclosure missing from legal documentation. | Update legal terms and in-app purchase overlays with explicit loot box probability disclosures. |
| 11. Support URL | ADVISORY | HIGH | Unreachable or missing support URL check in store metadata. | Declare an active, publicly accessible Support URL in store metadata. |
| 12. Privacy Policy | ADVISORY | HIGH | Privacy policy reference missing in metadata configuration (`BOTH-MISSING-PRIVACY-POLICY`). | Declare reachable Privacy Policy URL in listing metadata and in-app settings. |
| 13. Terms of Service | ADVISORY | HIGH / MEDIUM | Terms of Service / EULA links must be declared for subscription and UGC features. | Ensure linked EULA and ToS on all subscription paywalls and UGC reporting flows. |
| 14. Export Compliance | PASSED | Low | Encryption compliance key required in Info.plist. | Verify `ITSAppUsesNonExemptEncryption` is set to false or properly declared in Info.plist. |
| 15. Encryption Declarations | PASSED | Low | Non-exempt encryption declaration verified. | Confirm French ANSSI declaration if distributing encrypted builds in France. |

---

## Detailed Evaluation by Area

### 1. Permissions
- Status: PASSED
- Risk Level: None
- Analysis: Codebase and manifests were audited for sensitive iOS usage descriptions (`NSCameraUsageDescription`, `NSLocationWhenInUseUsageDescription`, `NSPhotoLibraryUsageDescription`, `NSMicrophoneUsageDescription`) and Android permissions (`ACCESS_BACKGROUND_LOCATION`, `MANAGE_EXTERNAL_STORAGE`, `READ_SMS`, `READ_CALL_LOG`). No ungrounded or vague permission requests were detected.

### 2. Privacy Disclosures
- Status: ADVISORY
- Risk Level: HIGH
- Finding ID: `BOTH-MISSING-PRIVACY-POLICY`
- Description: The store listing metadata configuration lacks a declared Privacy Policy URL.
- Remediation: Publish and set a valid, HTTPS-accessible Privacy Policy URL in App Store Connect and Google Play Console. Confirm that privacy nutrition labels and Google Data Safety declarations reflect all third-party SDK data practices.

### 3. Screenshots
- Status: PASSED
- Risk Level: None
- Analysis: Store listing screenshots show actual app features without login-only screens or splash screen placeholders. Screenshots avoid forbidden Apple device frame overlays (`APPLE-2.3.4-DEVICE-FRAMES-PREVIEW`) and Apple trademark violations (`APPLE-5.2.5-APPLE-DEVICE-IMAGE`).

### 4. Metadata
- Status: ADVISORY
- Risk Level: HIGH / MEDIUM
- Finding IDs: `BOTH-PLACEHOLDER`, `APPLE-2.3-CROSS-PLATFORM-REFERENCE`, `APPLE-2.3-FUTURE-FUNCTIONALITY`, `APPLE-2.3-NEGATIVE-APPLE-SENTIMENT`
- Description:
  - `BOTH-PLACEHOLDER`: Placeholder content (lorem ipsum, example.com) found in repository source/recipes.
  - `APPLE-2.3-CROSS-PLATFORM-REFERENCE`: Cross-platform references ("Google Play", "Android") present in user-facing copy.
  - `APPLE-2.3-FUTURE-FUNCTIONALITY`: Copy mentions future roadmap or beta features ("coming soon").
  - `APPLE-2.3-NEGATIVE-APPLE-SENTIMENT`: Copy includes references to platform bugs or negative sentiment.
- Remediation: Replace all placeholder content with production text. Strip all mentions of competing platforms, future feature promises, and negative platform comments from app descriptions and release notes.

### 5. Age Rating
- Status: BLOCKED
- Risk Level: CRITICAL
- Finding ID: `APPLE-ASCAPI-AGERATING-ENDPOINT-REMOVED`
- Affected Files: `data/detection-recipes.json`
- Description: Release scripts or API integration pipelines invoke a deprecated App Store Connect API age-rating endpoint (`appStoreVersions/{id}/ageRatingDeclaration`).
- Remediation: Update pipeline scripts to use the current age-rating declaration read and update endpoints per App Store Connect API 4.4+ specification. Ensure that the 2026 Apple age rating questionnaire (13+, 16+, 18+) and social media capability questions are answered in App Store Connect.

### 6. AI Disclosures
- Status: ADVISORY
- Risk Level: HIGH
- Finding ID: `BOTH-AI-GENERATED-CONTENT`
- Description: Generative AI features must include appropriate moderation, reporting, and disclosure controls.
- Remediation: Implement content moderation filters, report/block mechanisms for user-generated AI content, EU AI Act Article 50(1) in-app notice prior to user interaction, Article 50(2)/(4) machine-readable markings, and explicit third-party AI data sharing consent modals.

### 7. Subscription Disclosures
- Status: ADVISORY
- Risk Level: HIGH / MEDIUM
- Finding IDs: `BOTH-SUBSCRIPTION-HARD-CANCEL`, `APPLE-3.1.2-MISLEADING-PRICING`
- Description: Subscription terms must provide a simple self-service cancellation path and display full billed pricing as prominently as any calculated monthly rate.
- Remediation: Ensure the app and backend provide an immediate self-service in-app or web cancellation button. Modify paywall UI so that annual billed amounts are at least as prominent as monthly breakdown figures.

### 8. Payment Compliance
- Status: ADVISORY
- Risk Level: HIGH
- Finding IDs: `BOTH-LOOTBOX-ODDS`, `GOOGLE-PLAY-BILLING-V8-REQUIRED`
- Description:
  - `BOTH-LOOTBOX-ODDS`: Random reward / loot box mechanics exist without odds disclosures.
  - `GOOGLE-PLAY-BILLING-V8-REQUIRED`: Google Play Billing Library must be updated to version 8 or higher.
- Remediation: Disclose exact odds for every random item or loot box before purchase. Upgrade Android dependencies to Google Play Billing Library v8+. Confirm StoreKit / Play Billing usage for digital goods and verify Restore Purchases controls.

### 9. Accessibility
- Status: PASSED
- Risk Level: None
- Analysis: Static accessibility scanner executed across iOS, Android, and Web files with zero accessibility regressions detected.
- Verification: Compliance maintained against WCAG 2.1 AA and EN 301 549 standards (VoiceOver labels, Dynamic Type, TalkBack, Font scaling, Color contrast, Reduce Motion).

### 10. Legal Documents
- Status: ADVISORY
- Risk Level: HIGH
- Finding ID: `BOTH-LOOTBOX-ODDS`
- Description: Legal terms must incorporate required statutory disclosures, including random reward probabilities, DSA trader status, and EU AI Act Article 4 AI literacy records.
- Remediation: Add random reward probability disclosures to legal terms and in-app purchase sheets. Verify DSA trader status in App Store Connect.

### 11. Support URL
- Status: ADVISORY
- Risk Level: HIGH
- Finding ID: `BOTH-UNREACHABLE-METADATA-URL`
- Description: Support URL in store metadata must be valid and publicly accessible.
- Remediation: Validate that the support URL configured in metadata is live and returns HTTP 200 without auth gates or broken links.

### 12. Privacy Policy
- Status: ADVISORY
- Risk Level: HIGH
- Finding ID: `BOTH-MISSING-PRIVACY-POLICY`
- Description: Privacy policy URL is omitted from listing configuration metadata.
- Remediation: Set a valid, HTTPS privacy policy URL in App Store Connect and Google Play Console. Confirm that in-app settings link directly to the privacy policy.

### 13. Terms of Service
- Status: ADVISORY
- Risk Level: HIGH / MEDIUM
- Description: Terms of Service / End User License Agreement (EULA) links are required for subscription apps and apps containing user-generated content (UGC).
- Remediation: Ensure EULA / ToS links are present on all paywall screens and account setup flows. Verify 24-hour UGC report, block, and removal capabilities (`APPLE-1.2-UGC-24H-ACTION`).

### 14. Export Compliance
- Status: PASSED
- Risk Level: Low
- Analysis: Export compliance declarations checked for iOS Info.plist configuration.
- Verification: Ensure `ITSAppUsesNonExemptEncryption` is set to `false` (or `true` with appropriate encryption documentation attached in ASC).

### 15. Encryption Declarations
- Status: PASSED
- Risk Level: Low
- Analysis: Encryption status verified for store submission readiness.
- Verification: If distributing non-exempt encryption in France, confirm that the French ANSSI declaration is completed in App Store Connect.

---

## Action Plan for Release Authorization

To unblock and authorize this release:

1. **Resolve Critical Pipeline Issue (Blocker):**
   - Update `data/detection-recipes.json` and deployment scripts to replace deprecated App Store Connect API age-rating endpoints with current API 4.4+ endpoints.

2. **Resolve High Severity Findings:**
   - Add Privacy Policy and Support URLs to metadata configuration.
   - Remove placeholder text and cross-platform references ("Google Play") from app copy and metadata.
   - Provide explicit odds disclosures for random reward / loot box mechanics prior to purchase.
   - Provide a simple self-service subscription cancellation path.

3. **Resolve Medium Severity Findings:**
   - Clean up future feature promises ("coming soon", "beta") and negative platform bug copy from changelogs and descriptions.

4. **Re-run Release Readiness Audit:**
   - Execute `python3 scripts/release-audit.py .` and `bash agent-os/hooks/app-store-compliance-guard.sh .` to confirm all findings are resolved and overall status changes to PASSED / CLEAR TO SUBMIT.
