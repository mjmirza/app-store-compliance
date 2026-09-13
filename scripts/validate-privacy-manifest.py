#!/usr/bin/env python3
"""Validate the internals of an app's PrivacyInfo.xcprivacy.

The nutrition-label check in the guard only asks whether
NSPrivacyCollectedDataTypes exists. Apple additionally validates the manifest's
internal consistency at upload and rejects the build by email (ITMS-91xxx)
after processing, so a binary can install from TestFlight and still be barred
from review.

Usage:  validate-privacy-manifest.py <path-to-PrivacyInfo.xcprivacy> [...]
Exit:   0 clean, 1 findings, 2 could not read a file.
Prints  SEVERITY<TAB>ID<TAB>message  per finding.
"""
import plistlib
import sys

VALID_PURPOSES = {
    "NSPrivacyCollectedDataTypePurposeThirdPartyAdvertising",
    "NSPrivacyCollectedDataTypePurposeDeveloperAdvertising",
    "NSPrivacyCollectedDataTypePurposeAnalytics",
    "NSPrivacyCollectedDataTypePurposeProductPersonalization",
    "NSPrivacyCollectedDataTypePurposeAppFunctionality",
    "NSPrivacyCollectedDataTypePurposeOther",
}

REQUIRED_ON_TYPE = (
    "NSPrivacyCollectedDataType",
    "NSPrivacyCollectedDataTypeLinked",
    "NSPrivacyCollectedDataTypeTracking",
    "NSPrivacyCollectedDataTypePurposes",
)


def check(path):
    out = []
    try:
        with open(path, "rb") as fh:
            d = plistlib.load(fh)
    except Exception as exc:  # unreadable or malformed
        return [("critical", "APPLE-MANIFEST-UNREADABLE",
                 f"{path}: cannot parse privacy manifest ({exc})")], True

    tracking = d.get("NSPrivacyTracking", False)
    domains = d.get("NSPrivacyTrackingDomains", []) or []

    # ITMS-91064. Apple states the converse in the rejection email, but an
    # empty domain list alongside NSPrivacyTracking true is what fails.
    if tracking and not domains:
        out.append(("critical", "APPLE-ITMS-91064-TRACKING-NO-DOMAINS",
                    f"{path}: NSPrivacyTracking is true but NSPrivacyTrackingDomains is empty. "
                    "List every domain the app or its SDKs contact for tracking "
                    "(an MMP such as AppsFlyer declares its own in the pod's manifest)."))
    if domains and not tracking:
        out.append(("critical", "APPLE-ITMS-91064-DOMAINS-NO-TRACKING",
                    f"{path}: NSPrivacyTrackingDomains is non-empty but NSPrivacyTracking is false. "
                    "Set NSPrivacyTracking to true, or remove the domains."))

    types = d.get("NSPrivacyCollectedDataTypes", [])
    for i, entry in enumerate(types):
        label = entry.get("NSPrivacyCollectedDataType", f"entry {i}")
        for key in REQUIRED_ON_TYPE:
            if key not in entry:
                out.append(("high", "APPLE-MANIFEST-TYPE-INCOMPLETE",
                            f"{path}: collected data type {label} is missing {key}."))
        for purpose in entry.get("NSPrivacyCollectedDataTypePurposes", []):
            if purpose not in VALID_PURPOSES:
                out.append(("high", "APPLE-MANIFEST-BAD-PURPOSE",
                            f"{path}: {label} declares unknown purpose {purpose}."))
        if not entry.get("NSPrivacyCollectedDataTypePurposes", []):
            out.append(("high", "APPLE-MANIFEST-NO-PURPOSE",
                        f"{path}: {label} declares no purposes; at least one is required."))
        # Internally contradictory, but not a documented upload rejection, so it surfaces without blocking.
        if entry.get("NSPrivacyCollectedDataTypeTracking") and not tracking:
            out.append(("high", "APPLE-MANIFEST-TRACKING-CONTRADICTION",
                        f"{path}: {label} is marked used for tracking but NSPrivacyTracking is false."))

    for api in d.get("NSPrivacyAccessedAPITypes", []):
        if not api.get("NSPrivacyAccessedAPITypeReasons"):
            out.append(("high", "APPLE-MANIFEST-API-NO-REASON",
                        f"{path}: accessed API {api.get('NSPrivacyAccessedAPIType', '?')} "
                        "declares no reason codes."))

    return out, False


def main(argv):
    if len(argv) < 2:
        print("usage: validate-privacy-manifest.py <PrivacyInfo.xcprivacy> [...]", file=sys.stderr)
        return 2
    findings, unreadable = [], False
    for path in argv[1:]:
        got, bad = check(path)
        findings.extend(got)
        unreadable = unreadable or bad
    for sev, ident, msg in findings:
        print(f"{sev}\t{ident}\t{msg}")
    if unreadable:
        return 2
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
