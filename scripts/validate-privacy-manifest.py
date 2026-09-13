#!/usr/bin/env python3
"""Validate the internals of an app's PrivacyInfo.xcprivacy.

The nutrition-label check in the guard only asks whether
NSPrivacyCollectedDataTypes exists. Apple additionally validates the manifest's
internal consistency at upload and rejects the build by email (ITMS-91xxx)
after processing, so a binary can install from TestFlight and still be barred
from review.

Usage:  validate-privacy-manifest.py <path-to-PrivacyInfo.xcprivacy> [...]
Exit:   0 clean, 1 findings, 2 could not read a file.
Rules:  Apple TN3181 (invalid privacy manifest) and the privacy manifest reference. Reason codes per
        category are not validated here; App Store Connect still checks those.
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


def _rec(path, sev, ident, msg):
    # one record per line, so a newline in a path or value can never split a finding for the bash reader
    return (sev, ident, f"{path}: {msg}".replace("\n", " ").replace("\t", " "))


def _validate(d, path, out):
    tracking = d.get("NSPrivacyTracking", False)
    if not isinstance(tracking, bool):
        out.append(_rec(path, "critical", "APPLE-MANIFEST-BAD-VALUE",
                        "NSPrivacyTracking must be a Boolean (TN3181)."))
        tracking = bool(tracking)
    domains = d.get("NSPrivacyTrackingDomains", [])
    if not isinstance(domains, list) or any(not isinstance(x, str) for x in domains):
        out.append(_rec(path, "critical", "APPLE-MANIFEST-BAD-VALUE",
                        "NSPrivacyTrackingDomains must be an array of strings (TN3181)."))
        domains = [x for x in domains if isinstance(x, str)] if isinstance(domains, list) else []

    # ITMS-91064, both directions are documented as invalid (TN3181 and the privacy manifest reference)
    if tracking and not domains:
        out.append(_rec(path, "critical", "APPLE-ITMS-91064-TRACKING-NO-DOMAINS",
                        "NSPrivacyTracking is true but NSPrivacyTrackingDomains is empty. "
                        "List every domain the app or its SDKs contact for tracking "
                        "(an MMP such as AppsFlyer declares its own in the pod's manifest)."))
    if domains and not tracking:
        out.append(_rec(path, "critical", "APPLE-ITMS-91064-DOMAINS-NO-TRACKING",
                        "NSPrivacyTrackingDomains is non-empty but NSPrivacyTracking is false. "
                        "Set NSPrivacyTracking to true, or remove the domains."))

    types = d.get("NSPrivacyCollectedDataTypes", [])
    if not isinstance(types, list):
        out.append(_rec(path, "critical", "APPLE-MANIFEST-BAD-VALUE",
                        "NSPrivacyCollectedDataTypes must be an array of dictionaries."))
        types = []
    for i, entry in enumerate(types):
        if not isinstance(entry, dict):
            out.append(_rec(path, "critical", "APPLE-MANIFEST-BAD-VALUE",
                            f"NSPrivacyCollectedDataTypes entry {i} is not a dictionary."))
            continue
        label = entry.get("NSPrivacyCollectedDataType", f"entry {i}")
        # every key is required per collected type (privacy manifest reference), an invalid manifest blocks upload
        for key in REQUIRED_ON_TYPE:
            if key not in entry:
                out.append(_rec(path, "critical", "APPLE-MANIFEST-TYPE-INCOMPLETE",
                                f"collected data type {label} is missing {key}."))
        purposes = entry.get("NSPrivacyCollectedDataTypePurposes", [])
        if not isinstance(purposes, list):
            out.append(_rec(path, "critical", "APPLE-MANIFEST-BAD-VALUE",
                            f"{label} NSPrivacyCollectedDataTypePurposes must be an array of strings."))
            purposes = []
        for purpose in purposes:
            if purpose not in VALID_PURPOSES:
                out.append(_rec(path, "critical", "APPLE-MANIFEST-BAD-PURPOSE",
                                f"{label} declares unknown purpose {purpose}."))
        if not purposes:
            out.append(_rec(path, "critical", "APPLE-MANIFEST-NO-PURPOSE",
                            f"{label} declares no purposes; at least one is required."))
        # internally contradictory, but not a documented upload rejection, so it surfaces without blocking
        if entry.get("NSPrivacyCollectedDataTypeTracking") and not tracking:
            out.append(_rec(path, "high", "APPLE-MANIFEST-TRACKING-CONTRADICTION",
                            f"{label} is marked used for tracking but NSPrivacyTracking is false."))

    if "NSPrivacyAccessedAPITypes" in d:
        apis = d["NSPrivacyAccessedAPITypes"]
        if not isinstance(apis, list):
            out.append(_rec(path, "critical", "APPLE-MANIFEST-BAD-VALUE",
                            "NSPrivacyAccessedAPITypes must be an array of dictionaries (TN3181)."))
            apis = []
        elif not apis:
            # TN3181. an empty array is invalid, remove the key when no required reason API is used
            out.append(_rec(path, "critical", "APPLE-MANIFEST-API-TYPES-EMPTY",
                            "NSPrivacyAccessedAPITypes is an empty array. Remove the key, or list each required reason API the app uses."))
        for i, api in enumerate(apis):
            if not isinstance(api, dict):
                out.append(_rec(path, "critical", "APPLE-MANIFEST-BAD-VALUE",
                                f"NSPrivacyAccessedAPITypes entry {i} is not a dictionary."))
                continue
            api_type = api.get("NSPrivacyAccessedAPIType")
            if not isinstance(api_type, str) or not api_type:
                out.append(_rec(path, "critical", "APPLE-MANIFEST-API-TYPE-MISSING",
                                f"NSPrivacyAccessedAPITypes entry {i} has no NSPrivacyAccessedAPIType category string (TN3181)."))
                api_type = api_type or "?"
            reasons = api.get("NSPrivacyAccessedAPITypeReasons")
            # TN3181. a missing key or an empty array is an invalid manifest, the upload is rejected by email
            if not isinstance(reasons, list) or not reasons:
                out.append(_rec(path, "critical", "APPLE-MANIFEST-API-NO-REASON",
                                f"accessed API {api_type} declares no reason codes."))


def check(path):
    out = []
    try:
        with open(path, "rb") as fh:
            d = plistlib.load(fh)
        if not isinstance(d, dict):
            raise ValueError("root is not a dictionary")
        _validate(d, path, out)
    except Exception as exc:  # unreadable, malformed, or an unexpected shape. never a silent pass
        return [_rec(path, "critical", "APPLE-MANIFEST-UNREADABLE",
                     f"cannot parse privacy manifest ({exc})")], True
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
