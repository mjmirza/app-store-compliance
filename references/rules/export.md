# Rules. Export and build

1 rules in this category. Generated from data/rejection-patterns.json. Each rule names the guideline, the severity, what triggers it, and the fix.

## APPLE-EXPORT-COMPLIANCE-MISSING

- Title. Missing encryption declaration leaves the build in Missing Compliance
- Platform. apple
- Guideline or policy. Export compliance
- Severity. high
- What triggers it. ITSAppUsesNonExemptEncryption is not set in Info.plist, so each submission stalls in Missing Compliance and never reaches review.
- How to fix it. Set ITSAppUsesNonExemptEncryption in Info.plist. The exempt answer applies to a standard HTTPS only app.
- Present means handled. ITSAppUsesNonExemptEncryption
