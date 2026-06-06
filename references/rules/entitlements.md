# Rules. Entitlements

1 rules in this category. Generated from data/rejection-patterns.json. Each rule names the guideline, the severity, what triggers it, and the fix.

## APPLE-2.4.5-UNUSED-ENTITLEMENTS

- Title. Entitlements declared but not used
- Platform. apple
- Guideline or policy. 2.4.5(i)
- Severity. high
- What triggers it. An entitlements file declares a capability the app does not use. Apple requests justification for any entitlement with no matching functionality, which blocks review. Temporary exception entitlements draw extra scrutiny.
- How to fix it. Remove any entitlement the app does not actively use. Cross check each entitlement against real code usage. Source. truongduy2611 unused_entitlements rule.
- Detection signals. com.apple.security.temporary-exception, .entitlements

How to detect.

```bash
for e in $(find . -name '*.entitlements'); do echo "== $e"; plutil -p "$e"; done   # then grep the codebase to confirm each capability is actually used
```
