#!/usr/bin/env python3
import bisect
import os
import sys
import re
import argparse

# List of directory names to ignore during scan
IGNORE_DIRS = {
    "node_modules", "Pods", ".git", "build", "DerivedData", "vendor",
    ".dart_tool", "Carthage", "androidTest", "__tests__"
}

# Mapping of rule IDs to their detail
RULE_META = {
    "APPLE-ACCESSIBILITY-VOICEOVER": {
        "platform": "apple",
        "severity": "medium",
        "title": "VoiceOver support missing or incomplete",
        "fix": "Ensure all interactive components and decorative or informative images have correct accessibility labels, hints, and traits assigned."
    },
    "APPLE-ACCESSIBILITY-DYNAMICTYPE": {
        "platform": "apple",
        "severity": "medium",
        "title": "Dynamic Type support missing or overridden",
        "fix": "Use preferredFont(forTextStyle:) in UIKit and system/relative font styles in SwiftUI, ensuring adjustsFontForContentSizeCategory is enabled."
    },
    "APPLE-ACCESSIBILITY-REDUCEMOTION": {
        "platform": "apple",
        "severity": "medium",
        "title": "Reduce Motion accessibility setting ignored",
        "fix": "Check the Reduce Motion system status and disable or simplify non-essential animations when requested by the user."
    },
    "APPLE-ACCESSIBILITY-COLORCONTRAST": {
        "platform": "apple",
        "severity": "medium",
        "title": "Color Contrast and system settings ignored",
        "fix": "Use dynamic or system colors that automatically adapt, or monitor isDarkerSystemColorsEnabled to adjust contrast dynamically."
    },
    "APPLE-ACCESSIBILITY-HAPTICS": {
        "platform": "apple",
        "severity": "low",
        "title": "Haptic feedback absent on interactions (advisory, not required by WCAG 2.2 or EN 301 549)",
        "fix": "Add haptic feedback to buttons, toggles, and swipe actions using UIImpactFeedbackGenerator or selection feedback."
    },
    "APPLE-ACCESSIBILITY-KEYBOARD": {
        "platform": "apple",
        "severity": "medium",
        "title": "Keyboard navigation and focus state support missing",
        "fix": "Support physical keyboard navigation by utilizing keyCommands in UIKit or focusable() and @FocusState in SwiftUI."
    },
    "ANDROID-ACCESSIBILITY-TALKBACK": {
        "platform": "google",
        "severity": "medium",
        "title": "TalkBack support missing or disabled",
        "fix": "Provide meaningful contentDescription values for all informative images and interactive views, and ensure importantForAccessibility is set correctly."
    },
    "ANDROID-ACCESSIBILITY-FONTSCALING": {
        "platform": "google",
        "severity": "medium",
        "title": "Font scaling disabled due to dp text sizing",
        "fix": "Always define text sizes in sp (scale-independent pixels) rather than dp to allow the system font scaling to work correctly."
    },
    "ANDROID-ACCESSIBILITY-HIGHCONTRAST": {
        "platform": "google",
        "severity": "medium",
        "title": "Hardcoded colors ignoring high contrast settings",
        "fix": "Reference semantic colors or color resources so the app automatically respects high contrast themes."
    },
    "ANDROID-ACCESSIBILITY-SCANNER": {
        "platform": "google",
        "severity": "medium",
        "title": "Touch target sizes below 48dp",
        "fix": "Ensure all interactive elements have a minimum touch target area of 48dp x 48dp by using padding, minWidth, and minHeight."
    }
}

def scan_files(directory):
    ios_files = []
    android_files = []
    for root, dirs, files in os.walk(directory):
        # In-place directory filtering to ignore unwanted folders
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.endswith("Tests")]
        for file in files:
            path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            if ext in {".swift", ".m", ".h", ".plist", ".storyboard", ".xib"}:
                ios_files.append(path)
            elif ext in {".kt", ".java", ".xml"}:
                android_files.append(path)
    return ios_files, android_files


def _string_frame(content, q, hashes):
    multi = content.startswith('"""', q)
    return ("s", multi, ('"""' if multi else '"') + "#" * hashes, "\\" + "#" * hashes)


def _skip_string(content, q, hashes):
    """For the string opening at q, return (body start, body end, offset after it).
    An explicit stack walks nested strings and interpolations, so no depth can overflow."""
    n = len(content)
    body_start = q + (3 if content.startswith('"""', q) else 1)
    stack, j = [_string_frame(content, q, hashes)], body_start
    while j < n:
        frame = stack[-1]
        if frame[0] == "s":
            _, multi, close, esc = frame
            if content.startswith(esc, j):
                k = j + len(esc)
                if k < n and content[k] == "(":
                    stack.append(["i", 0])
                    j = k
                else:
                    j = k + 1
                continue
            if not multi and content[j] == "\n":
                stack.pop()  # an unterminated single-line string ends at the newline
                if not stack:
                    return body_start, j, j
                continue
            if content.startswith(close, j):
                stack.pop()
                if not stack:
                    return body_start, j, j + len(close)
                j += len(close)
                continue
            j += 1
            continue
        c = content[j]
        if content.startswith("//", j):
            nl = content.find("\n", j)
            j = n if nl == -1 else nl
            continue
        if content.startswith("/*", j):
            level, j = 1, j + 2
            while j < n and level:
                if content.startswith("/*", j):
                    level, j = level + 1, j + 2
                elif content.startswith("*/", j):
                    level, j = level - 1, j + 2
                else:
                    j += 1
            continue
        if c == '"' or c == "#":
            h = 0
            while j + h < n and content[j + h] == "#":
                h += 1
            if j + h < n and content[j + h] == '"':
                inner = _string_frame(content, j + h, h)
                stack.append(inner)
                j = j + h + (3 if inner[1] else 1)
                continue
            if h and j + h < n and content[j + h] == "/":
                end = _regex_close(content, j + h + 1, h)
                j = min(n, end + 1 + h)
                continue
            j += max(h, 1)
            continue
        if c == "(":
            frame[1] += 1
        elif c == ")":
            frame[1] -= 1
            if frame[1] == 0:
                stack.pop()
        j += 1
    return body_start, n, n


def _regex_close(content, start, hashes):
    """Offset of the closing slash of a #/.../# literal, skipping backslash escapes, or len(content)."""
    close = "/" + "#" * hashes
    n, j = len(content), start
    while j < n:
        if content[j] == "\\":
            j += 2
        elif content.startswith(close, j):
            return j
        else:
            j += 1
    return n


def swift_code_lines(content):
    """Only whole comment lines blanked, with no string state, so a misread quote never hides any code.
    Offsets and newlines are kept."""
    out = []
    in_block = False
    in_text = False
    for line in content.split("\n"):
        t = line.lstrip(" \t")
        if re.search(chr(92) * 2 + "#*" + chr(92) + "(", line):
            out.append(line)
            continue
        if not in_block and not in_text and t.startswith("//"):
            # a comment line is blanked before its quotes are counted, so a quote in a comment never opens a string
            out.append(" " * len(line))
            continue
        code = re.sub(chr(92) * 2 + '#*"', "", line)
        cut = code.find("//")
        if cut != -1 and code[:cut].count('"') % 2 == 0:
            code = code[:cut]  # quotes after an inline // comment never open a string
        quotes = code.count('"""')
        if not in_block and (in_text or quotes % 2):
            # a multiline string line is kept as is, so a /* or // inside one never blanks the code after it
            if quotes % 2:
                in_text = not in_text
            out.append(line)
            continue
        if not in_block and t.startswith("//"):
            out.append(" " * len(line))
            continue
        if in_block and not (t.startswith("*") or "*/" in line):
            # a block comment goes on only through lines that look like comment lines, any other line is code
            in_block = False
            out.append(line)
            continue
        if in_block or t.startswith("/*"):
            # only a block comment opened at a line start is blanked, a line led by * outside one is code
            end = line.find("*/", len(line) - len(t) + (0 if in_block else 2))
            if end == -1:
                in_block = True
                out.append(" " * len(line))
            else:
                in_block = False
                out.append(" " * (end + 2) + line[end + 2:])
            continue
        out.append(line)
    return "\n".join(out)


def swift_code_only(content):
    """Blank comments (nested too) and string contents, keeping quotes, newlines and offsets.
    What is left is code, so a Button inside a comment or a string is never read as a control."""
    out = list(content)
    n = len(content)
    i = 0

    def blank(a, b):
        for k in range(a, b):
            if out[k] != "\n":
                out[k] = " "

    while i < n:
        c = content[i]
        if content.startswith("//", i):
            j = content.find("\n", i)
            j = n if j == -1 else j
            blank(i, j)
            i = j
        elif content.startswith("/*", i):
            depth, j = 1, i + 2
            while j < n and depth:
                if content.startswith("/*", j):
                    depth, j = depth + 1, j + 2
                elif content.startswith("*/", j):
                    depth, j = depth - 1, j + 2
                else:
                    j += 1
            blank(i, j)
            i = j
        elif c == "#" or c == '"':
            hashes = 0
            while i + hashes < n and content[i + hashes] == "#":
                hashes += 1
            q = i + hashes
            if hashes and q < n and content[q] == "/":
                end = _regex_close(content, q + 1, hashes)
                blank(q + 1, end)
                i = min(n, end + 1 + hashes)
                continue
            if q >= n or content[q] != '"':
                i += max(hashes, 1)
                continue
            body_start, body_end, after = _skip_string(content, q, hashes)
            blank(body_start, body_end)
            i = after
        else:
            i += 1
    return "".join(out)


def _bracket_pairs(code):
    """Map each opening bracket to the offset just past its match, per bracket type, in one pass."""
    pairs, stacks = {}, {"(": [], "[": [], "{": []}
    opener = {")": "(", "]": "[", "}": "{"}
    for i, ch in enumerate(code):
        if ch in stacks:
            stacks[ch].append(i)
        elif ch in opener and stacks[opener[ch]]:
            pairs[stacks[opener[ch]].pop()] = i + 1
    return pairs


def _skip_ws(text, i):
    while i < len(text) and text[i].isspace():
        i += 1
    return i


def _top_level_args(code, start, end, pairs):
    """(start, end) offsets of each comma-separated argument at depth 0 between start and end.
    Nested brackets are jumped over through pairs, so enclosing calls never rescan them."""
    parts, depth, a, k = [], 0, start, start
    while k < end:
        ch = code[k]
        if ch in "([{":
            close = pairs.get(k, -1)
            if depth == 0 and 0 < close <= end:
                k = close
                continue
            depth += 1
        elif ch in ")]}":
            depth -= 1
        elif ch == "," and depth == 0:
            parts.append((a, k))
            a = k + 1
        k += 1
    parts.append((a, end))
    return parts


DIRECTIVE = re.compile(r"#(?:if|elseif|else|endif)\b")
LABELED_CLOSURE = re.compile(r"\s*[A-Za-z_][A-Za-z0-9_]*\s*:\s*\{")


def _modifier_chain(code, i, pairs):
    """Read the .modifier(...) chain that follows offset i. Returns (names with args, end offset)."""
    mods = []
    n = len(code)
    while True:
        j = _skip_ws(code, i)
        if DIRECTIVE.match(code, j):  # #if / #else / #endif lines between modifiers
            eol = code.find("\n", j)
            i = n if eol == -1 else eol
            continue
        d = _skip_ws(code, j + 1) if j < n and code[j] == "." else n
        if d >= n or not (code[d].isalpha() or code[d] == "_"):
            return mods, i
        k = d
        while k < n and (code[k].isalnum() or code[k] == "_"):
            k += 1
        name, args = code[d:k], None
        k2 = _skip_ws(code, k)
        if k2 < n and code[k2] == "(":
            end = pairs.get(k2, -1)
            if end == -1:
                return mods, i
            args, k = (k2, end), end
            k2 = _skip_ws(code, k)
        while k2 < n and code[k2] == "{":  # one trailing closure, then any labeled ones
            end = pairs.get(k2, -1)
            if end == -1:
                return mods, i
            k = end
            m = LABELED_CLOSURE.match(code, k)
            k2 = m.end() - 1 if m else n
        mods.append((name, args))
        i = k


IMAGE_SYMBOL = re.compile(r"\bImage\s*\(\s*systemName\s*:")
NAMED_CONTENT = re.compile(r"\b(Text|Label)\s*\(|\baccessibilityLabel\b")
TITLED_ARG = re.compile(r"\s*(#*\"|title\s*:)")
LABEL_ARG = re.compile(r"\s*label\s*:")
LABEL_CLOSURE = re.compile(r"\s*label\s*:\s*(?:[(]\s*)*\{")  # label: ({ ... }) reads too
HIDDEN_TRUE = re.compile(r"\((?:\s*\()*\s*true\s*(?:\)\s*)*\)")
ACC_HIDDEN = re.compile(r"\bhidden\s*:\s*(?:\(\s*)*true\b")
ACC_LABEL = re.compile(r"\blabel\s*:")
LABEL_OFF = re.compile(r"\bisEnabled\s*:\s*false\b")
UNLABELED_ARG = re.compile(r"\s*(?![A-Za-z_][A-Za-z0-9_]*\s*:)[^\s{]")


def _labels_button(code, name, args):
    """True when a modifier gives the Button a spoken label or hides it from VoiceOver."""
    if name == "accessibilityLabel":
        return not (args and LABEL_OFF.search(code, *args))
    if name == "accessibilityRepresentation":
        return True
    if name == "accessibilityHidden":
        return bool(args and HIDDEN_TRUE.fullmatch(code, *args))
    if name == "accessibility" and args:
        return bool(ACC_LABEL.search(code, *args) or ACC_HIDDEN.search(code, *args))
    return False


def _any_in(hits, a, b):
    k = bisect.bisect_left(hits, a)
    return k < len(hits) and hits[k] < b


def _label_closure_after(code, k, pairs):
    """(start, end) of a label: { ... } closure beginning at or after k, or None."""
    lab = LABEL_CLOSURE.match(code, k)
    if not lab:
        return None
    start = lab.end() - 1
    end = pairs.get(start, -1)
    return None if end == -1 else (start, end)


def _line_end(text, start, end):
    nl = text.find("\n", start, end)
    return end if nl == -1 else nl


def find_icon_only_buttons(code):
    """Yield (offset, end) for SwiftUI Buttons whose only label is an Image(systemName:)
    with no accessibilityLabel on the label or on the Button's own modifier chain."""
    code = code.replace("`", " ")  # escaped identifiers read as plain names, offsets kept
    pairs = _bracket_pairs(code)
    closer = {end - 1: start for start, end in pairs.items() if code[start] == "("}
    img_hits = [m.start() for m in IMAGE_SYMBOL.finditer(code)]
    named_hits = [m.start() for m in NAMED_CONTENT.finditer(code)]
    for m in re.finditer(r"(?<![\w.])(?:SwiftUI\s*\.\s*)?Button\b", code):
        k = m.start() - 1
        while k >= 0 and code[k].isspace():
            k -= 1
        if k >= 0 and code[k] == ".":
            continue  # a member of something else, such as MyKit . SwiftUI.Button
        i = _skip_ws(code, m.end())
        label = None
        if i < len(code) and code[i] == "(":
            end = pairs.get(i, -1)
            if end == -1:
                continue
            parts = _top_level_args(code, i + 1, end - 1, pairs)
            if any(
                TITLED_ARG.match(code, a, b) or UNLABELED_ARG.match(code, a, b) for a, b in parts
            ):
                continue  # a titled button reads its title, literal or not
            label_part = next(
                ((a, b) for a, b in parts if LABEL_ARG.match(code, a, b)), None
            )
            if label_part:
                label = _label_closure_after(code, label_part[0], pairs)
                if not label or label[1] > label_part[1]:
                    continue  # a label view passed by name cannot be read here
            i = end
            j = _skip_ws(code, i)
            if label is None and j < len(code) and code[j] == "{":
                lend = pairs.get(j, -1)
                if lend == -1:
                    continue
                label, i = (j, lend), lend
                after = _label_closure_after(code, i, pairs)
                if after:  # the trailing closure was the action, the label follows it
                    label, i = after, after[1]
        elif i < len(code) and code[i] == "{":
            end = pairs.get(i, -1)
            if end == -1:
                continue
            label = _label_closure_after(code, end, pairs)
            if not label:
                continue
            i = label[1]
        if not label:
            continue
        if not _any_in(img_hits, label[0], label[1]) or _any_in(named_hits, label[0], label[1]):
            continue  # the whole label counts, see the documented limit in README.md
        mods, end = _modifier_chain(code, i, pairs)
        start = m.start()
        while True:  # ((Button { ... })).modifier reads through every wrapping parenthesis
            j = _skip_ws(code, end)
            o = closer.get(j)
            if o is None or code[o + 1 : start].strip():
                break
            start = o
            more, end = _modifier_chain(code, j + 1, pairs)
            mods += more
        if any(_labels_button(code, name, args) for name, args in mods):
            continue
        yield m.start(), i
def run_rule_scan(rule_id, ios_files, android_files):
    findings = []

    if rule_id == "APPLE-ACCESSIBILITY-VOICEOVER":
        # SwiftUI Image without accessibility modifiers, or UIKit views without accessibility attributes
        # Scan SwiftUI Images: e.g. Image("name") or Image(systemName: "...")
        for f in ios_files:
            if not f.endswith(".swift"):
                continue
            try:
                content = open(f, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue

            # Find SwiftUI Image usages in code only, so a commented example is never read
            # The lexer view is precise and the line view never loses code to a misread quote. Both are read.
            seen = set()
            code = swift_code_only(content)
            for view in (code, swift_code_lines(content)):
              for match in re.finditer(r"\bImage\s*\(([^)]+)\)", view):
                if match.start() in seen:
                    continue
                seen.add(match.start())
                expr = match.group(1)
                # Ignore images explicitly defined as decorative or having system accessibility labels/hidden
                if "decorative:" in expr or "systemName:" in expr:
                    continue
                # Simple parsing check: does the immediate context (within 5 lines) have accessibility modifiers?
                start_idx = match.start()
                context = code[start_idx:start_idx + 300]
                if not any(kw in context for kw in ["accessibilityLabel", "accessibilityIdentifier", "accessibilityHidden", "accessibilityElement"]):
                    line_no = content.count("\n", 0, start_idx) + 1
                    findings.append({
                        "file": f,
                        "line": line_no,
                        "rule_id": rule_id,
                        "match": content[match.start() : match.end()],
                        "message": "SwiftUI Image used without accessibilityLabel or decorative initialization.",
                        "fix": "Initialize decorative images as Image(decorative: ...) or add an explicit .accessibilityLabel(...) modifier."
                    })

            newlines = [k for k, ch in enumerate(code) if ch == "\n"]
            for offset, end in find_icon_only_buttons(code):
                findings.append(
                    {
                        "file": f,
                        "line": bisect.bisect_right(newlines, offset) + 1,
                        "rule_id": rule_id,
                        "match": content[offset : _line_end(content, offset, end)].strip(),
                        "message": "Possible icon-only Button. Its label shows an Image(systemName:) with no Text, Label or accessibilityLabel, so VoiceOver may read the symbol name.",
                        "fix": 'Add .accessibilityLabel("...") to the Button, or use Label("Title", systemImage: ...) / Button("Title", systemImage: ...).',
                    }
                )

            # Look for UIButton / UIImageView declarations in UIKit swift without accessibility properties
            if re.search(r"\bUI(Button|ImageView)\b", code):
                if not any(kw in content for kw in ["accessibilityLabel", "accessibilityIdentifier", "isAccessibilityElement"]):
                    findings.append({
                        "file": f,
                        "line": 1,
                        "rule_id": rule_id,
                        "match": "UIButton / UIImageView declaration",
                        "message": "UIKit components found but no accessibility attributes (accessibilityLabel, isAccessibilityElement) are references in the file.",
                        "fix": "Assign meaningful accessibilityLabel properties to interactive UIKit components."
                    })

    elif rule_id == "APPLE-ACCESSIBILITY-DYNAMICTYPE":
        # Check SwiftUI hardcoded system fonts, e.g. .font(.system(size: ...))
        # Or UIKit Font declarations like UIFont.systemFont(ofSize: ...)
        for f in ios_files:
            if not (f.endswith(".swift") or f.endswith(".m") or f.endswith(".h")):
                continue
            try:
                content = open(f, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue

            for match in re.finditer(r"\.system\(size:\s*\d+", content):
                start_idx = match.start()
                line_no = content.count("\n", 0, start_idx) + 1
                findings.append({
                    "file": f,
                    "line": line_no,
                    "rule_id": rule_id,
                    "match": match.group(0),
                    "message": "Hardcoded system font size detected which prevents Dynamic Type scaling.",
                    "fix": "Use SwiftUI relative text styles like .font(.body) or wrap custom font sizes in dynamic-type scaled modifiers."
                })

            for match in re.finditer(r"UIFont\.systemFont\(ofSize:\s*\d+", content):
                start_idx = match.start()
                line_no = content.count("\n", 0, start_idx) + 1
                # Check if adjustsFontForContentSizeCategory is present in the file
                if "adjustsFontForContentSizeCategory" not in content:
                    findings.append({
                        "file": f,
                        "line": line_no,
                        "rule_id": rule_id,
                        "match": match.group(0),
                        "message": "Hardcoded UIFont used without adjusting for content size category.",
                        "fix": "Use UIFont.preferredFont(forTextStyle:) and set adjustsFontForContentSizeCategory = true on your labels."
                    })

    elif rule_id == "APPLE-ACCESSIBILITY-REDUCEMOTION":
        # Find transition, withAnimation or UIView.animate without checking reduce motion
        for f in ios_files:
            if not (f.endswith(".swift") or f.endswith(".m")):
                continue
            try:
                content = open(f, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue

            if "withAnimation" in content or "UIView.animate" in content:
                if "isReduceMotionEnabled" not in content and "accessibilityReduceMotion" not in content:
                    findings.append({
                        "file": f,
                        "line": 1,
                        "rule_id": rule_id,
                        "match": "Animation usage",
                        "message": "Animations used without checking Reduce Motion state.",
                        "fix": "Check UIAccessibility.isReduceMotionEnabled or SwiftUI's accessibilityReduceMotion environment variable to disable or simplify animations."
                    })

    elif rule_id == "APPLE-ACCESSIBILITY-COLORCONTRAST":
        # Find hardcoded UIColors or SwiftUI Colors without dynamic adaptivity or isDarkerSystemColorsEnabled
        for f in ios_files:
            if not (f.endswith(".swift") or f.endswith(".m")):
                continue
            try:
                content = open(f, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue

            # Flag static CGColors or UIColors using hardcoded color specs without dynamic checking
            for match in re.finditer(r"UIColor\s*\(\s*red:\s*\d+", content):
                if "isDarkerSystemColorsEnabled" not in content and "darkerSystemColors" not in content:
                    start_idx = match.start()
                    line_no = content.count("\n", 0, start_idx) + 1
                    findings.append({
                        "file": f,
                        "line": line_no,
                        "rule_id": rule_id,
                        "match": match.group(0),
                        "message": "Static UIColor with raw RGB values does not support custom high-contrast modes.",
                        "fix": "Utilize asset-catalog named dynamic colors or respect UIAccessibility.isDarkerSystemColorsEnabled."
                    })

    elif rule_id == "APPLE-ACCESSIBILITY-HAPTICS":
        # Scan for interactive actions/handlers without feedback generator references
        for f in ios_files:
            if not f.endswith(".swift"):
                continue
            try:
                content = open(f, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue

            code = swift_code_only(content)
            if re.search(r"\.onTapGesture\b|(?<![A-Za-z0-9_])Button\s*[({]", code):
                if not any(kw in content for kw in ["FeedbackGenerator", "CoreHaptics", "CHHapticEngine"]):
                    findings.append({
                        "file": f,
                        "line": 1,
                        "rule_id": rule_id,
                        "match": "Interactive controls without haptics",
                        "message": "Interactive taps or gestures used but no haptic feedback generator referenced.",
                        "fix": "Incorporate UIImpactFeedbackGenerator or UISelectionFeedbackGenerator for interactive feedback."
                    })

    elif rule_id == "APPLE-ACCESSIBILITY-KEYBOARD":
        # Scan for customized controls or keyboard handling missing proper focus or keyCommands
        for f in ios_files:
            if not f.endswith(".swift"):
                continue
            try:
                content = open(f, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue

            if "focusable" in content and "FocusState" not in content and "focused" not in content:
                findings.append({
                    "file": f,
                    "line": 1,
                    "rule_id": rule_id,
                    "match": "focusable",
                    "message": "Focusable elements used without focus state tracking.",
                    "fix": "Use @FocusState to track and programmatically move keyboard focus for accessibility keyboard users."
                })

    elif rule_id == "ANDROID-ACCESSIBILITY-TALKBACK":
        # Look for XML layout elements or Compose Image without contentDescription
        for f in android_files:
            if f.endswith(".xml"):
                try:
                    content = open(f, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                # Find ImageView or ImageButton
                for match in re.finditer(r"<ImageView\b|<ImageButton\b", content):
                    start_idx = match.start()
                    line_no = content.count("\n", 0, start_idx) + 1
                    # Check if this element block (up to next >) has contentDescription
                    elem_block = content[start_idx:content.find(">", start_idx) + 1]
                    if "contentDescription" not in elem_block:
                        findings.append({
                            "file": f,
                            "line": line_no,
                            "rule_id": rule_id,
                            "match": elem_block.split("\n")[0],
                            "message": "XML image view missing contentDescription attribute.",
                            "fix": "Add an android:contentDescription attribute with descriptive text, or set android:importantForAccessibility=\"no\" if decorative."
                        })
            elif f.endswith(".kt"):
                try:
                    content = open(f, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                # Find Jetpack Compose Image usages
                for match in re.finditer(r"\bImage\s*\(([^)]+)\)", content):
                    expr = match.group(1)
                    if "contentDescription" not in expr:
                        start_idx = match.start()
                        line_no = content.count("\n", 0, start_idx) + 1
                        findings.append({
                            "file": f,
                            "line": line_no,
                            "rule_id": rule_id,
                            "match": match.group(0),
                            "message": "Compose Image element missing contentDescription parameter.",
                            "fix": "Provide a descriptive contentDescription or pass null explicitly if decorative."
                        })

    elif rule_id == "ANDROID-ACCESSIBILITY-FONTSCALING":
        # Search for XML textSize with dp units, or Compose fontSize with dp units
        for f in android_files:
            if f.endswith(".xml"):
                try:
                    content = open(f, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                for match in re.finditer(r"android:textSize\s*=\s*\"(\d+dp)\"", content):
                    start_idx = match.start()
                    line_no = content.count("\n", 0, start_idx) + 1
                    findings.append({
                        "file": f,
                        "line": line_no,
                        "rule_id": rule_id,
                        "match": match.group(0),
                        "message": f"Text size specified in dp ({match.group(1)}) instead of sp.",
                        "fix": "Change text size unit from dp to sp (scale-independent pixels) so font scaling is supported."
                    })
            elif f.endswith(".kt"):
                try:
                    content = open(f, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                for match in re.finditer(r"fontSize\s*=\s*(\d+)\.dp", content):
                    start_idx = match.start()
                    line_no = content.count("\n", 0, start_idx) + 1
                    findings.append({
                        "file": f,
                        "line": line_no,
                        "rule_id": rule_id,
                        "match": match.group(0),
                        "message": "Compose text fontSize specified in dp instead of sp.",
                        "fix": "Change Jetpack Compose text font size unit to sp (e.g. 16.sp)."
                    })

    elif rule_id == "ANDROID-ACCESSIBILITY-HIGHCONTRAST":
        # Scan for hardcoded background or text colors using hex code values directly in XML or Compose
        for f in android_files:
            if f.endswith(".xml"):
                try:
                    content = open(f, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                for match in re.finditer(r"android:(textColor|background)\s*=\s*\"(#[0-9A-Fa-f]{6,8})\"", content):
                    start_idx = match.start()
                    line_no = content.count("\n", 0, start_idx) + 1
                    findings.append({
                        "file": f,
                        "line": line_no,
                        "rule_id": rule_id,
                        "match": match.group(0),
                        "message": f"Hardcoded hex color value ({match.group(2)}) ignored high contrast theme settings.",
                        "fix": "Use semantic theme references or color resources (e.g. ?attr/colorOnSurface) rather than static hex strings."
                    })
            elif f.endswith(".kt"):
                try:
                    content = open(f, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                for match in re.finditer(r"Color\s*\(\s*0xFF[0-9A-Fa-f]{6}\s*\)", content):
                    start_idx = match.start()
                    line_no = content.count("\n", 0, start_idx) + 1
                    findings.append({
                        "file": f,
                        "line": line_no,
                        "rule_id": rule_id,
                        "match": match.group(0),
                        "message": "Compose Color declared with hardcoded hex code.",
                        "fix": "Reference semantic colors from your app Theme material colors scheme instead of hardcoded values."
                    })

    elif rule_id == "ANDROID-ACCESSIBILITY-SCANNER":
        # Scan XML and Compose layouts for touch target dimensions or paddings under 48dp
        for f in android_files:
            if f.endswith(".xml"):
                try:
                    content = open(f, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                # Match layout_width or layout_height with dimensions below 48dp (e.g. 10dp to 47dp)
                # Let's match layout_width or layout_height or minWidth or minHeight under 48dp
                for match in re.finditer(r"android:(layout_width|layout_height|minWidth|minHeight)\s*=\s*\"([1-3][0-9]|4[0-7]|[1-9])dp\"", content):
                    if "layout_width=\"wrap_content\"" not in content and "layout_height=\"wrap_content\"" not in content:
                        start_idx = match.start()
                        line_no = content.count("\n", 0, start_idx) + 1
                        findings.append({
                            "file": f,
                            "line": line_no,
                            "rule_id": rule_id,
                            "match": match.group(0),
                            "message": f"Component dimension ({match.group(0)}) is below the recommended 48dp touch target threshold.",
                            "fix": "Increase interactive component width and height to at least 48dp or add layout padding."
                        })
            elif f.endswith(".kt"):
                try:
                    content = open(f, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                # Match clickable elements that may be too small
                for match in re.finditer(r"\.size\s*\(\s*([1-3][0-9]|4[0-7]|[1-9])\.dp\s*\)", content):
                    start_idx = match.start()
                    line_no = content.count("\n", 0, start_idx) + 1
                    findings.append({
                        "file": f,
                        "line": line_no,
                        "rule_id": rule_id,
                        "match": match.group(0),
                        "message": "Compose view size is below the recommended 48dp touch target threshold.",
                        "fix": "Enlarge the touch target size of the clickable control to at least 48dp x 48dp."
                    })

    return findings

def main():
    parser = argparse.ArgumentParser(description="Static continuous accessibility compliance auditor.")
    parser.add_argument("directory", nargs="?", default=".", help="Root directory of the project to scan.")
    parser.add_argument("--rule", help="Scan only a specific accessibility rule ID.")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Directory not found: {args.directory}")
        return 0

    ios_files, android_files = scan_files(args.directory)

    if args.rule and args.rule not in RULE_META:
        print(
            f"Unknown rule: {args.rule}. Known rules. {', '.join(RULE_META)}",
            file=sys.stderr,
        )
        return 2

    rules_to_scan = [args.rule] if args.rule else list(RULE_META.keys())

    all_findings = []
    for rule in rules_to_scan:
        if rule not in RULE_META:
            continue
        findings = run_rule_scan(rule, ios_files, android_files)
        all_findings.extend(findings)

    # Sort findings by rule ID and file path
    all_findings.sort(key=lambda x: (x["rule_id"], x["file"], x["line"]))

    print("== Accessibility Compliance Audit ==")
    print(f"Audited directory. {args.directory}")
    print(f"Scanned files. iOS={len(ios_files)} Android={len(android_files)}")
    print("")

    if not all_findings:
        print("Clean. No accessibility compliance regressions found.")
        print("")
        print("Summary. critical=0 high=0 medium=0 low=0")
        return 0

    # Print detailed findings
    crit = 0
    high = 0
    med = 0
    low = 0

    for f in all_findings:
        meta = RULE_META[f["rule_id"]]
        sev = meta["severity"]
        if sev == "critical":
            crit += 1
        elif sev == "high":
            high += 1
        elif sev == "medium":
            med += 1
        else:
            low += 1

        print(f"  [{sev.upper()}] {f['rule_id']}  ({f['file']}:{f['line']})")
        print(f"      context: {f['match']}")
        print(f"      reason:  {f['message']}")
        print(f"      fix:     {f['fix']}")
        print("")

    print(f"Summary. critical={crit} high={high} medium={med} low={low}")
    print("Reference. docs/EU-REGULATORY-2026.md and docs/PLATFORM-MECHANICS-2026.md")

    # Exit with 0 on advisory findings since accessibility represents medium store risk
    return 0

if __name__ == "__main__":
    sys.exit(main())
