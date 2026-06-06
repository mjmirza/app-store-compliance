# Rules. Metadata and store listing

9 rules in this category. Generated from data/rejection-patterns.json. Each rule names the guideline, the severity, what triggers it, and the fix.

## APPLE-2.3-AGE-RATING-2026

- Title. New 2026 age rating questionnaire not answered
- Platform. apple
- Guideline or policy. 2.3.6
- Severity. high
- What triggers it. Manual check. The updated age rating questions (13 plus, 16 plus, 18 plus) must be answered by 31 January 2026 to submit updates.
- How to fix it. Answer the updated age rating questionnaire in App Store Connect for every app.

## BOTH-UNREACHABLE-METADATA-URL

- Title. Broken support, marketing, or privacy URL in the listing
- Platform. both
- Guideline or policy. Apple 1.5 and 2.1, Google User Data
- Severity. high
- What triggers it. A support URL, marketing URL, or privacy policy URL in the listing does not load. Mirrors the fastlane precheck unreachable_urls rule.
- How to fix it. Confirm every listing URL is public and loads during the entire review window.

## APPLE-5.2.5-APPLE-DEVICE-IMAGE

- Title. Apple device image or Apple trademark in the icon or screenshots
- Platform. apple
- Guideline or policy. 5.2.5
- Severity. high
- What triggers it. Manual metadata check. The app icon or screenshots show an Apple device, the Apple logo, or imply Apple endorsement.
- How to fix it. Remove Apple device images and Apple marks from the icon and screenshots. Source. truongduy2611 apple_trademark rule.

## CHINA-AI-REFERENCES

- Title. External AI service references in a China storefront
- Platform. apple
- Guideline or policy. 5
- Severity. high
- What triggers it. Manual storefront check. References to ChatGPT, Gemini, OpenAI, or similar external AI services in an app distributed on the China storefront can trigger a regional rejection.
- How to fix it. Remove or localize external AI service references for the China storefront. Source. truongduy2611 china_storefront rule.

## APPLE-2.3-CROSS-PLATFORM-REFERENCE

- Title. Reference to other platform or marketplace
- Platform. apple
- Guideline or policy. 2.3.10
- Severity. medium
- What triggers it. Strings such as Android, Google Play, or alternative marketplace names found in app facing copy or metadata.
- How to fix it. Remove references to other platforms and marketplaces from the app and metadata.
- Detection signals. Google Play, available on Android, download on the Play Store

## BOTH-METADATA-DECORATION

- Title. Metadata field overflow or banned decoration
- Platform. both
- Guideline or policy. Apple 2.3.7, Google Store Listing
- Severity. medium
- What triggers it. App name over the limit (Apple 30, Google 30), emoji in the title, all caps, or ranking and price claims such as number one, best, top, or free in the title or icon.
- How to fix it. Keep each metadata field within its limit and remove emoji, all caps, and ranking or price claims from the title and icon.

## APPLE-2.3-FUTURE-FUNCTIONALITY

- Title. Metadata promises features that do not ship in this build
- Platform. apple
- Guideline or policy. 2.3.1
- Severity. medium
- What triggers it. Listing or in app copy uses coming soon, beta, or a promised feature not present in the build. Mirrors the fastlane precheck future_functionality rule.
- How to fix it. Describe only what the build does today. Remove coming soon and future feature promises from the listing.
- Detection signals. coming soon, coming-soon, beta, will be available, in a future update, stay tuned

## APPLE-2.3-NEGATIVE-APPLE-SENTIMENT

- Title. Metadata names an iOS bug or references Apple negatively
- Platform. apple
- Guideline or policy. 2.3.1
- Severity. medium
- What triggers it. Listing copy mentions an iOS bug or makes a negative or insensitive reference to Apple. Mirrors the fastlane precheck negative_apple_sentiment rule.
- How to fix it. Remove negative references to Apple and iOS bugs from the listing copy.
- Detection signals. iOS bug, apple bug, broken on iOS, fix for ios bug

## APPLE-2.3.4-DEVICE-FRAMES-PREVIEW

- Title. Device frames around the app in a preview video
- Platform. apple
- Guideline or policy. 2.3.4
- Severity. medium
- What triggers it. Manual metadata check. The app preview video wraps the app in a device frame instead of showing the app full screen.
- How to fix it. Capture the preview video full screen from the device, without a device frame overlay.
