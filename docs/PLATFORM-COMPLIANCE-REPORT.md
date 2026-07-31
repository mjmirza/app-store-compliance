# Platform and Regulatory Compliance Report

This report evaluates and documents the current global regulatory and platform compliance status for Apple App Store (iOS and iPadOS) and Google Play (Android) distribution.

## 1. Summary
This compliance report provides an exhaustive, multi-regional review of current and upcoming mobile platform policy gates and regulatory requirements for iOS and Android distribution. By executing continuous monitor audits and evaluating regional compliance databases, we establish a structured, proactive mitigation strategy to address major regulatory updates, including the EU AI Act transparency rules, Google Play Target SDK requirements, and mandatory Play Billing version updates, ensuring that all submissions proceed without storefront rejections or developer account penalties.

## 2. Background
Mobile application marketplaces have pivoted from basic editorial reviews to rigorous, legally-mandated compliance validation systems. In 2026, regulatory authorities globally (including the European Commission, the US Federal Trade Commission, and state-level legislatures) have deputized platform operators (Apple and Google) to enforce statutory requirements under penalty of app removal or account termination. Maintaining high alignment with these platform-enforced rules is essential to ensure continuous service availability and brand integrity across all target markets.

## 3. Regulatory change
Recent legislative and platform-level shifts have introduced critical updates that demand active codebase and operational synchronization:
- **European Union (EU AI Act - Regulation (EU) 2024/1689)**: Article 50 mandates that any user interacting with generative AI features must receive immediate, clear disclosure. Synthetic content (audio, video, image, or text) must carry machine-readable and visible markings.
- **US State App Store Accountability Acts (Utah, Texas, Louisiana)**: These statutes mandate the collection of verified user age categories and parental consent for minors, which must be declared programmatically via Apple's Declared Age Range API or Android's Play Age Signals API.
- **Google Play Target SDK 36 Update**: Effective August 31, 2026, all new apps and updates must target API level 36 (Android 16), raising runtime requirements and tightening background execution limits.
- **Google Play Billing v8.0 Mandatory Migration**: Legacy BillingClient libraries must be migrated to version 8.0 or later to maintain in-app purchasing capabilities.
- **Android Scoped Storage and Permissions Model**: Tighter scanning on broad media access permissions (READ_MEDIA_IMAGES and READ_MEDIA_VIDEO) requires a full transition to the system-provided Photo Picker API.

## 4. Official citations
The following Priority 1 official sources and documents have been prioritized to compile this compliance report:
- **European Union**: Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act).
- **European Commission**: Directive (EU) 2019/882 on the accessibility requirements for products and services (European Accessibility Act).
- **US Federal Trade Commission**: 16 CFR Part 312, Children's Online Privacy Protection Act (COPPA) Rules and 2026 amendments.
- **Apple Developer News**: Official updates regarding Privacy Manifests, Required Reason APIs, and Xcode 26 SDK requirements.
- **Google Play Policy Center**: Google Play Developer Program Policies, target API schedule, and Google Play Billing Library migration guidelines.
- **United Kingdom Government**: Online Safety Act 2023, Part 3 obligations for services likely to be accessed by children.

## 5. Affected files
Codebase files identified as potentially affected or containing matching signals requiring audit:
- `data/rejection-patterns.json`: Contains structured patterns for detecting standard Apple/Android policy violations.
- `data/regulatory-deadlines.json`: Contains regional, national, and platform regulatory timelines.
- `docs/EU-REGULATORY-2026.md`: Documents legal rules for European market distribution.
- `docs/GLOBAL-REGULATORY-2026.md`: Documents global legal boundaries (COPPA, US state laws, etc.).
- `docs/PLATFORM-MECHANICS-2026.md`: Details platform-specific API and version target rules.
- `docs/PRE-SUBMISSION-CHECKLIST.md`: Comprehensive manual pre-launch checks for release audits.
- `scripts/monitor.py`: Core Apple requirements scanner.
- `scripts/monitor-android.py`: Core Android requirements scanner.

## 6. Risk assessment
- **Critical Risk (Blocked Submissions)**: Operating with a target SDK level below API 35 or utilizing billing libraries below v8.0 will trigger an automatic gatekeeper rejection in the developer console.
- **High Risk (Regulatory Non-Compliance)**: Failure to implement user-facing AI interaction disclosures or proper age rating declarations increases exposure to regional data protection fines and potential App Store removal in the EU.
- **Medium Risk (Administrative Delay)**: Missing developer identity verification or broken in-app account deletion links can lead to temporary listing suspensions.

## 7. Migration steps
To secure publishing approval, developers and administrators must execute the following sequence:
- **Update Target SDK Configurations**: Modify the targetSdkVersion to API 36 inside build.gradle configurations and verify runtime compatibility.
- **Integrate Platform Age Signals**: Implement the native Declared Age Range API for iOS and the Play Age Signals API for Android to correctly sync storefront age rating questionnaires.
- **Deploy AI Interaction Disclosures**: Inject a modal notification or persistent visual label for any feature powered by generative models, aligning with the EU AI Act.
- **Transition Storage Permissions**: Replace broad READ_MEDIA_IMAGES declarations with the modern Photo Picker framework to eliminate manual permission review delays.
- **Upgrade Billing Client Libraries**: Migrate dependencies from BillingClient v7 or below to BillingClient v8.0+.

## 8. Backward compatibility
All changes detailed in this update are backwards-compatible:
- **Fallback APIs**: Use conditional checks (e.g., if-Build-VERSION) to utilize the native Photo Picker on newer Android OS versions while maintaining standard selectors on older versions.
- **State Preservation**: Existing subscription models and local secure databases remain completely unaffected. No breaking schema modifications are introduced.

## 9. Implementation checklist
- [ ] Upgrade targetSdkVersion and compileSdkVersion to 36 in Android build files.
- [ ] Upgrade minSdkVersion to 23 to officially deprecate legacy API 21/22 devices.
- [ ] Add NSPrivacyAccessedAPITypes declarations to iOS PrivacyInfo.xcprivacy.
- [ ] Incorporate in-app account deletion buttons that route directly to deletion APIs.
- [ ] Wire user-facing AI transparency disclaimers onto interactive LLM screens.

## 10. Testing checklist
- [ ] Execute clean local and CI compilation across both iOS and Android target builds.
- [ ] Perform functional tests of user consent withdrawal and account deletion UX.
- [ ] Run the repository validator script to verify pattern file structures.
- [ ] Conduct layout verification of Dynamic Type rendering and WCAG 2.1 contrast compliance.

## 11. Documentation checklist
- [ ] Ensure that store metadata listings do not mention competing platforms or unapproved keywords.
- [ ] Verify that a valid, responsive privacy policy URL is embedded in-app and on the store listing page.
- [ ] Document specific test account credentials in the Notes for Review field.
- [ ] Update the internal compliance deadline tracker with the latest confirmed grace periods.

## 12. Compliance impact
- **Submission Security**: Lowers general App Review rejection rates, avoiding critical release bottlenecks.
- **Legal Safeguards**: Mitigates compliance liabilities under the GDPR, the EU AI Act, and COPPA.
- **User Trust**: Clear data usage declarations and accessible deletion mechanisms increase user retention and store ratings.

## 13. Breaking changes
- Raising the minSdkVersion to 23 terminates update support for legacy devices running Android 5.0 and 5.1 (API 21/22).
- Enforcing strict target SDK 36 behavior may result in background task throttling for unoptimized tasks.

## 14. Review checklist
- [ ] Verify that the codebase is completely emoji-free and contains no graphical symbols.
- [ ] Confirm that all official citations are traceably matched to official Priority 1 publications.
- [ ] Double-check that no private APIs are utilized in the iOS build.

## 15. Approver recommendations
- **Mobile Engineering Lead**: Validate that the target SDK 36 and Billing Library v8 migrations compile without warnings.
- **Data Protection Officer / Legal Counsel**: Confirm that the privacy policy accurately discloses third-party AI data sharing behaviors.
- **Release Manager**: Check that personal/organization developer account verifications are completed before the September deadline.
