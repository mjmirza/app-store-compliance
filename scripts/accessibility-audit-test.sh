#!/usr/bin/env bash
# Test suite for scripts/accessibility-audit.py
# Verifies all 10 platform accessibility rules on compliant and non-compliant codeblocks.
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
AUDIT="python3 $HERE/accessibility-audit.py"
PASS=0
FAIL=0

ok() {
  PASS=$((PASS+1))
  printf 'PASS: %s\n' "$1"
}

bad() {
  FAIL=$((FAIL+1))
  printf 'FAIL: %s\n' "$1"
}

# Create mock folders
COMPLIANT_DIR=$(mktemp -d "/tmp/access_compliant_XXXXXX")
REGRESSION_DIR=$(mktemp -d "/tmp/access_regression_XXXXXX")

cleanup() {
  rm -rf "$COMPLIANT_DIR" "$REGRESSION_DIR" 2>/dev/null || true
}
trap cleanup EXIT

# --- Populate Compliant (Clean) Cases ---

# Rule 1: APPLE-ACCESSIBILITY-VOICEOVER Compliant SwiftUI and UIKit
cat << 'EOF' > "$COMPLIANT_DIR/VoiceOver_SwiftUI_Compliant.swift"
import SwiftUI
struct MyView: View {
    var body: some View {
        Image(decorative: "logo")
        Image(systemName: "star")
        Image("logo")
            .accessibilityLabel("Logo")
    }
}
EOF

cat << 'EOF' > "$COMPLIANT_DIR/VoiceOver_UIKit_Compliant.swift"
import UIKit
// FeedbackGenerator reference to prevent false-positive APPLE-ACCESSIBILITY-HAPTICS on UIButton
class MyController: UIViewController {
    let button = UIButton()
    func setup() {
        button.accessibilityLabel = "Click me"
    }
}
EOF

# Rule 2: APPLE-ACCESSIBILITY-DYNAMICTYPE Compliant SwiftUI and UIKit
cat << 'EOF' > "$COMPLIANT_DIR/DynamicType_SwiftUI_Compliant.swift"
import SwiftUI
struct MyView: View {
    var body: some View {
        Text("Hello").font(.body)
    }
}
EOF

cat << 'EOF' > "$COMPLIANT_DIR/DynamicType_UIKit_Compliant.swift"
import UIKit
class MyController: UIViewController {
    func setup() {
        let label = UILabel()
        label.font = UIFont.systemFont(ofSize: 14)
        label.adjustsFontForContentSizeCategory = true
    }
}
EOF

# Rule 3: APPLE-ACCESSIBILITY-REDUCEMOTION Compliant SwiftUI and UIKit
cat << 'EOF' > "$COMPLIANT_DIR/ReduceMotion_Compliant.swift"
import SwiftUI
// FeedbackGenerator reference to prevent false-positive APPLE-ACCESSIBILITY-HAPTICS on Button
struct MyView: View {
    var body: some View {
        Button("Animate") {
            if UIAccessibility.isReduceMotionEnabled {
                // static behavior
            } else {
                withAnimation {
                    // Do animation
                }
            }
        }
    }
}
EOF

# Rule 4: APPLE-ACCESSIBILITY-COLORCONTRAST Compliant SwiftUI and UIKit
cat << 'EOF' > "$COMPLIANT_DIR/ColorContrast_Compliant.swift"
import UIKit
class MyController: UIViewController {
    func setup() {
        if UIAccessibility.isDarkerSystemColorsEnabled {
            let color = UIColor.black
        } else {
            let color = UIColor(red: 255, green: 0, blue: 0, alpha: 1)
        }
    }
}
EOF

# Rule 5: APPLE-ACCESSIBILITY-HAPTICS Compliant
cat << 'EOF' > "$COMPLIANT_DIR/Haptics_Compliant.swift"
import SwiftUI
struct MyView: View {
    var body: some View {
        Button("Tap me") {
            let generator = UIImpactFeedbackGenerator()
            generator.impactOccurred()
        }
    }
}
EOF

# Rule 6: APPLE-ACCESSIBILITY-KEYBOARD Compliant
cat << 'EOF' > "$COMPLIANT_DIR/Keyboard_Compliant.swift"
import SwiftUI
struct MyView: View {
    @FocusState private var isFocused: Bool
    var body: some View {
        Text("Hello")
            .focusable()
            .focused($isFocused)
    }
}
EOF

# Rule 7: ANDROID-ACCESSIBILITY-TALKBACK Compliant XML and Compose
cat << 'EOF' > "$COMPLIANT_DIR/talkback_compliant.xml"
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent">
    <ImageView
        android:id="@+id/logo"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:contentDescription="App Logo" />
</LinearLayout>
EOF

cat << 'EOF' > "$COMPLIANT_DIR/TalkBack_Compliant.kt"
import androidx.compose.foundation.Image
import androidx.compose.runtime.Composable
@Composable
fun MyScreen() {
    val myPainter = painterResource
    Image(
        painter = myPainter,
        contentDescription = "App Logo"
    )
}
EOF

# Rule 8: ANDROID-ACCESSIBILITY-FONTSCALING Compliant XML and Compose
cat << 'EOF' > "$COMPLIANT_DIR/fontscaling_compliant.xml"
<?xml version="1.0" encoding="utf-8"?>
<TextView xmlns:android="http://schemas.android.com/apk/res/android"
    android:textSize="16sp" />
EOF

cat << 'EOF' > "$COMPLIANT_DIR/FontScaling_Compliant.kt"
import androidx.compose.material.Text
import androidx.compose.runtime.Composable
@Composable
fun MyText() {
    Text("Hello", fontSize = 16.sp)
}
EOF

# Rule 9: ANDROID-ACCESSIBILITY-HIGHCONTRAST Compliant XML and Compose
cat << 'EOF' > "$COMPLIANT_DIR/highcontrast_compliant.xml"
<?xml version="1.0" encoding="utf-8"?>
<TextView xmlns:android="http://schemas.android.com/apk/res/android"
    android:textColor="?attr/colorOnSurface" />
EOF

cat << 'EOF' > "$COMPLIANT_DIR/HighContrast_Compliant.kt"
import androidx.compose.material3.MaterialTheme
val myColor = MaterialTheme.colorScheme.primary
EOF

# Rule 10: ANDROID-ACCESSIBILITY-SCANNER Compliant XML and Compose
cat << 'EOF' > "$COMPLIANT_DIR/scanner_compliant.xml"
<?xml version="1.0" encoding="utf-8"?>
<Button xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content" />
EOF

cat << 'EOF' > "$COMPLIANT_DIR/Scanner_Compliant.kt"
import androidx.compose.ui.Modifier
val mod = Modifier.size(48.dp)
EOF


# --- Populate Regression (Non-Compliant) Cases ---

# Rule 1: APPLE-ACCESSIBILITY-VOICEOVER Non-Compliant SwiftUI
cat << 'EOF' > "$REGRESSION_DIR/VoiceOver_SwiftUI_NonCompliant.swift"
import SwiftUI
struct MyView: View {
    var body: some View {
        Image("logo")
    }
}
EOF

# Rule 1: APPLE-ACCESSIBILITY-VOICEOVER Non-Compliant UIKit
cat << 'EOF' > "$REGRESSION_DIR/VoiceOver_UIKit_NonCompliant.swift"
import UIKit
class MyController: UIViewController {
    let button = UIButton()
}
EOF

# Rule 2: APPLE-ACCESSIBILITY-DYNAMICTYPE Non-Compliant SwiftUI
cat << 'EOF' > "$REGRESSION_DIR/DynamicType_SwiftUI_NonCompliant.swift"
import SwiftUI
struct MyView: View {
    var body: some View {
        Text("Hello").font(.system(size: 14))
    }
}
EOF

# Rule 2: APPLE-ACCESSIBILITY-DYNAMICTYPE Non-Compliant UIKit
cat << 'EOF' > "$REGRESSION_DIR/DynamicType_UIKit_NonCompliant.swift"
import UIKit
class MyController: UIViewController {
    func setup() {
        let font = UIFont.systemFont(ofSize: 14)
    }
}
EOF

# Rule 3: APPLE-ACCESSIBILITY-REDUCEMOTION Non-Compliant
cat << 'EOF' > "$REGRESSION_DIR/ReduceMotion_NonCompliant.swift"
import SwiftUI
struct MyView: View {
    var body: some View {
        Button("Animate") {
            withAnimation {
                // Do animation
            }
        }
    }
}
EOF

# Rule 4: APPLE-ACCESSIBILITY-COLORCONTRAST Non-Compliant
cat << 'EOF' > "$REGRESSION_DIR/ColorContrast_NonCompliant.swift"
import UIKit
class MyController: UIViewController {
    func setup() {
        let color = UIColor(red: 255, green: 0, blue: 0, alpha: 1)
    }
}
EOF

# Rule 5: APPLE-ACCESSIBILITY-HAPTICS Non-Compliant
cat << 'EOF' > "$REGRESSION_DIR/Haptics_NonCompliant.swift"
import SwiftUI
struct MyView: View {
    var body: some View {
        Button("Tap me") {
            print("Tapped")
        }
    }
}
EOF

# Rule 6: APPLE-ACCESSIBILITY-KEYBOARD Non-Compliant
cat << 'EOF' > "$REGRESSION_DIR/Keyboard_NonCompliant.swift"
import SwiftUI
struct MyView: View {
    var body: some View {
        Text("Hello")
            .focusable()
    }
}
EOF

# Rule 7: ANDROID-ACCESSIBILITY-TALKBACK Non-Compliant XML
cat << 'EOF' > "$REGRESSION_DIR/talkback_noncompliant.xml"
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent">
    <ImageView
        android:id="@+id/logo"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content" />
</LinearLayout>
EOF

# Rule 7: ANDROID-ACCESSIBILITY-TALKBACK Non-Compliant Compose
cat << 'EOF' > "$REGRESSION_DIR/TalkBack_NonCompliant.kt"
import androidx.compose.foundation.Image
import androidx.compose.runtime.Composable
@Composable
fun MyScreen() {
    Image(
        painter = painterResource
    )
}
EOF

# Rule 8: ANDROID-ACCESSIBILITY-FONTSCALING Non-Compliant XML
cat << 'EOF' > "$REGRESSION_DIR/fontscaling_noncompliant.xml"
<?xml version="1.0" encoding="utf-8"?>
<TextView xmlns:android="http://schemas.android.com/apk/res/android"
    android:textSize="16dp" />
EOF

# Rule 8: ANDROID-ACCESSIBILITY-FONTSCALING Non-Compliant Compose
cat << 'EOF' > "$REGRESSION_DIR/FontScaling_NonCompliant.kt"
import androidx.compose.material.Text
import androidx.compose.runtime.Composable
@Composable
fun MyText() {
    Text("Hello", fontSize = 16.dp)
}
EOF

# Rule 9: ANDROID-ACCESSIBILITY-HIGHCONTRAST Non-Compliant XML
cat << 'EOF' > "$REGRESSION_DIR/highcontrast_noncompliant.xml"
<?xml version="1.0" encoding="utf-8"?>
<TextView xmlns:android="http://schemas.android.com/apk/res/android"
    android:textColor="#FF0000" />
EOF

# Rule 9: ANDROID-ACCESSIBILITY-HIGHCONTRAST Non-Compliant Compose
cat << 'EOF' > "$REGRESSION_DIR/HighContrast_NonCompliant.kt"
import androidx.compose.ui.graphics.Color
val myColor = Color(0xFFFF0000)
EOF

# Rule 10: ANDROID-ACCESSIBILITY-SCANNER Non-Compliant XML
cat << 'EOF' > "$REGRESSION_DIR/scanner_noncompliant.xml"
<?xml version="1.0" encoding="utf-8"?>
<Button xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:minWidth="40dp" />
EOF

# Rule 10: ANDROID-ACCESSIBILITY-SCANNER Non-Compliant Compose
cat << 'EOF' > "$REGRESSION_DIR/Scanner_NonCompliant.kt"
import androidx.compose.ui.Modifier
val mod = Modifier.size(40.dp)
EOF


echo "== Running Accessibility Compliance Test Suite =="

# Test 1: Run on compliant folder. Should have NO findings.
OUT_COMPLIANT=$($AUDIT "$COMPLIANT_DIR" 2>&1)
if echo "$OUT_COMPLIANT" | grep -q "Clean. No accessibility compliance regressions found."; then
  ok "Compliant directory produced 0 findings"
else
  bad "Compliant directory produced unexpected findings. Output:"
  echo "$OUT_COMPLIANT"
fi

# Test 2: Run on regression folder. Should detect regressions.
OUT_REGRESSION=$($AUDIT "$REGRESSION_DIR" 2>&1)

# Check Rule 1: APPLE-ACCESSIBILITY-VOICEOVER
if echo "$OUT_REGRESSION" | grep -q "APPLE-ACCESSIBILITY-VOICEOVER"; then
  ok "Flagged APPLE-ACCESSIBILITY-VOICEOVER"
else
  bad "Failed to flag APPLE-ACCESSIBILITY-VOICEOVER"
fi

# Check Rule 2: APPLE-ACCESSIBILITY-DYNAMICTYPE
if echo "$OUT_REGRESSION" | grep -q "APPLE-ACCESSIBILITY-DYNAMICTYPE"; then
  ok "Flagged APPLE-ACCESSIBILITY-DYNAMICTYPE"
else
  bad "Failed to flag APPLE-ACCESSIBILITY-DYNAMICTYPE"
fi

# Check Rule 3: APPLE-ACCESSIBILITY-REDUCEMOTION
if echo "$OUT_REGRESSION" | grep -q "APPLE-ACCESSIBILITY-REDUCEMOTION"; then
  ok "Flagged APPLE-ACCESSIBILITY-REDUCEMOTION"
else
  bad "Failed to flag APPLE-ACCESSIBILITY-REDUCEMOTION"
fi

# Check Rule 4: APPLE-ACCESSIBILITY-COLORCONTRAST
if echo "$OUT_REGRESSION" | grep -q "APPLE-ACCESSIBILITY-COLORCONTRAST"; then
  ok "Flagged APPLE-ACCESSIBILITY-COLORCONTRAST"
else
  bad "Failed to flag APPLE-ACCESSIBILITY-COLORCONTRAST"
fi

# Check Rule 5: APPLE-ACCESSIBILITY-HAPTICS
if echo "$OUT_REGRESSION" | grep -q "APPLE-ACCESSIBILITY-HAPTICS"; then
  ok "Flagged APPLE-ACCESSIBILITY-HAPTICS"
else
  bad "Failed to flag APPLE-ACCESSIBILITY-HAPTICS"
fi

# Check Rule 6: APPLE-ACCESSIBILITY-KEYBOARD
if echo "$OUT_REGRESSION" | grep -q "APPLE-ACCESSIBILITY-KEYBOARD"; then
  ok "Flagged APPLE-ACCESSIBILITY-KEYBOARD"
else
  bad "Failed to flag APPLE-ACCESSIBILITY-KEYBOARD"
fi

# Check Rule 7: ANDROID-ACCESSIBILITY-TALKBACK
if echo "$OUT_REGRESSION" | grep -q "ANDROID-ACCESSIBILITY-TALKBACK"; then
  ok "Flagged ANDROID-ACCESSIBILITY-TALKBACK"
else
  bad "Failed to flag ANDROID-ACCESSIBILITY-TALKBACK"
fi

# Check Rule 8: ANDROID-ACCESSIBILITY-FONTSCALING
if echo "$OUT_REGRESSION" | grep -q "ANDROID-ACCESSIBILITY-FONTSCALING"; then
  ok "Flagged ANDROID-ACCESSIBILITY-FONTSCALING"
else
  bad "Failed to flag ANDROID-ACCESSIBILITY-FONTSCALING"
fi

# Check Rule 9: ANDROID-ACCESSIBILITY-HIGHCONTRAST
if echo "$OUT_REGRESSION" | grep -q "ANDROID-ACCESSIBILITY-HIGHCONTRAST"; then
  ok "Flagged ANDROID-ACCESSIBILITY-HIGHCONTRAST"
else
  bad "Failed to flag ANDROID-ACCESSIBILITY-HIGHCONTRAST"
fi

# Check Rule 10: ANDROID-ACCESSIBILITY-SCANNER
if echo "$OUT_REGRESSION" | grep -q "ANDROID-ACCESSIBILITY-SCANNER"; then
  ok "Flagged ANDROID-ACCESSIBILITY-SCANNER"
else
  bad "Failed to flag ANDROID-ACCESSIBILITY-SCANNER"
fi

# --- Issue #834 and --rule regression cases ---
ISSUE_DIR=$(mktemp -d "/tmp/access_issue834_XXXXXX")
mkdir -p "$ISSUE_DIR/icon_bad" "$ISSUE_DIR/icon_good" "$ISSUE_DIR/clean" "$ISSUE_DIR/tap"

cat << 'EOF' > "$ISSUE_DIR/icon_bad/IconButton.swift"
import SwiftUI
struct V: View {
    var body: some View {
        Button { delete() } label: { Image(systemName: "trash") }
        Button(action: edit) {
            Image(systemName: "pencil")
        }
    }
}
EOF

cat << 'EOF' > "$ISSUE_DIR/icon_good/IconButtonLabeled.swift"
import SwiftUI
struct V: View {
    var body: some View {
        Button { delete() } label: { Image(systemName: "trash") }
            .accessibilityLabel("Delete")
        Button("Save", systemImage: "square.and.arrow.down") { save() }
        Button { go() } label: { Label("Go", systemImage: "arrow.right") }
        Image(systemName: "star")
    }
}
EOF

cat << 'EOF' > "$ISSUE_DIR/clean/Clean.swift"
import SwiftUI
// Mentions of UIButton and Button in a comment are not interactions.
struct V: View {
    var body: some View {
        Text("Hello").font(.body)
    }
}
EOF

cat << 'EOF' > "$ISSUE_DIR/tap/Tap.swift"
import SwiftUI
struct V: View {
    var body: some View {
        Text("Hello").onTapGesture { open() }
    }
}
EOF

mkdir -p "$ISSUE_DIR/icon_bad2" "$ISSUE_DIR/lexer_clean" "$ISSUE_DIR/big"
cat << 'EOF' > "$ISSUE_DIR/icon_bad2/Inline.swift"
import SwiftUI
struct V: View {
    var body: some View {
        Button(action: {}, label: { Image(systemName: "trash") })
        Button(action: edit) { Image (systemName: "gear") }
        HStack {
            Button(action: {}) { Image(systemName: "xmark") }.padding(); Text("Other").accessibilityLabel("Other")
        }
    }
}
EOF

cat << 'EOF' > "$ISSUE_DIR/lexer_clean/Strings.swift"
import SwiftUI
/* outer /* nested Button { } label: { Image(systemName: "a") } */ still a comment Button(action: x) { Image(systemName: "b") } */
let raw = #"Button(action: x) { Image(systemName: "c") } and "quotes" inside"#
let multi = """
Button(action: y) { Image(systemName: "d") }
see https://docs.example/a // not a comment
"""
struct V: View {
    var body: some View { Text(multi).font(.body) }
}
EOF

mkdir -p "$ISSUE_DIR/regex_lit" "$ISSUE_DIR/chain_perf" "$ISSUE_DIR/mod_perf"
mkdir -p "$ISSUE_DIR/sweep15"
cat << 'EOF' > "$ISSUE_DIR/sweep15/S.swift"
import SwiftUI
struct V: View {
    let title = "Pause"
    var body: some View {
        Button(title) { icon = Image(systemName: "pause") }
        ((Button(action: {}) { Image(systemName: "trash") })).accessibilityLabel("Delete")
        Button(action: {}) { Image(systemName: "a") } . accessibilityLabel("A")
        Button(action: {}) { Image(systemName: "b") }
        #if DEBUG
            .padding()
        #endif
            .accessibilityLabel("B")
        Button(action: {}) { Image(systemName: "c") }.`accessibilityLabel`("C")
        Button(action: {}) { Image(systemName: "d"); `Text`("D") }
        Button(action: {}) { Image(systemName: "e") }.accessibility(label: Text("E"))
        Button(action: {}) { Image(systemName: "f") }.accessibility(hidden: true)
        Button(action: {}) { Image(systemName: "g") }.accessibilityRepresentation { Text("G") }
        Button(action: {}) { Image(systemName: "h") }.accessibilityHidden((true))
        `Button`(action: {}) { Image(systemName: "i") }
        Button(action: {}) { Image(systemName: "j") }.accessibilityLabel("J", isEnabled: false)
    }
}
EOF
mkdir -p "$ISSUE_DIR/multi_closure"
cat << 'EOF' > "$ISSUE_DIR/multi_closure/M.swift"
import SwiftUI
struct V: View {
    var body: some View {
        Button(action: {}) { Image(systemName: "trash") }
            .contextMenu { Text("Menu") } preview: { Text("Preview") }
            .accessibilityLabel("Delete")
        Button(action: {}) { Image(systemName: "gear") }
            .contextMenu { Text("Menu") } preview: { Text("Preview") }
    }
}
EOF
mkdir -p "$ISSUE_DIR/qualified"
cat << 'EOF' > "$ISSUE_DIR/qualified/Q.swift"
import SwiftUI
struct V: View {
    var body: some View {
        SwiftUI.Button(action: {}) { Image(systemName: "gear") }
        MyKit.Button(action: {}) { Image(systemName: "trash") }
        let b = self.Button(action: {}) { Image(systemName: "star") }
        let c = MyKit . SwiftUI.Button(action: {}) { Image(systemName: "bell") }
        let d = ΩSwiftUI.Button(action: {}) { Image(systemName: "flag") }
        let e = obj . Button(action: {}) { Image(systemName: "pin") }
    }
}
EOF
mkdir -p "$ISSUE_DIR/regex_esc"
cat << 'EOF' > "$ISSUE_DIR/regex_esc/Esc.swift"
import SwiftUI
let re = #/foo\/#[/*]/#
let s = "x \(#/a\/#b/#) y"
struct V: View {
    var body: some View {
        Button(action: {}) { Image(systemName: "gear") }
    }
}
EOF
cat << 'EOF' > "$ISSUE_DIR/regex_lit/Regex.swift"
import SwiftUI
let re = #/[Button(action: {}) { Image(systemName: "trash") }]/#
let s = "count \(#/ // ) " /#.description)"
struct V: View {
    var body: some View {
        Button(action: {}) { Image(systemName: "gear") }
    }
}
EOF
python3 - "$ISSUE_DIR" << 'PY'
import os, sys
d = sys.argv[1]
q = chr(34); nl = chr(10)
chain = "let v0 = Image(systemName: " + q + "trash" + q + ")" + nl + "".join("let v%d = v%d" % (k, k - 1) + nl for k in range(1, 3200))
with open(os.path.join(d, "chain_perf", "Chain.swift"), "w") as fh:
    fh.write("Button(action: {}) {" + nl + chain + "return v3199" + nl + "}" + nl)
n = 32000
with open(os.path.join(d, "mod_perf", "Mods.swift"), "w") as fh:
    fh.write(("Button(action: {}) { Image(systemName: " + q + "trash" + q + ") }.overlay(") * n + "EmptyView()" + ")" * n + nl)
PY

mkdir -p "$ISSUE_DIR/icon_r7" "$ISSUE_DIR/nested_labels"
cat << 'EOF' > "$ISSUE_DIR/icon_r7/R7.swift"
import SwiftUI
struct V: View {
    var body: some View {
        Button(action: {}) { let icon = Image(systemName: "trash"); return icon }
        Button(action: {}) { return Image(systemName: "gear"); Text("Unused") }
    }
}
EOF
python3 - "$ISSUE_DIR" << 'PY'
import os, sys
q = chr(34)
n = 16000
with open(os.path.join(sys.argv[1], "nested_labels", "Labels.swift"), "w") as fh:
    fh.write(("Button(action: {}) {" + chr(10)) * n + "Image(systemName: " + q + "trash" + q + ")" + (chr(10) + "}") * n + chr(10))
PY

mkdir -p "$ISSUE_DIR/icon_r6" "$ISSUE_DIR/clean_r6" "$ISSUE_DIR/deep_interp" "$ISSUE_DIR/nested_perf"
cat << 'EOF' > "$ISSUE_DIR/icon_r6/R6.swift"
import SwiftUI
struct V: View {
    var body: some View {
        Button(role: .destructive) { delete() } label: /* explanation explanation explanation explanation explanation explanation explanation */ { Image(systemName: "trash") }
        Button { go() } label: { let discarded = Text("Delete"); return Image(systemName: "gear") }
    }
}
EOF
cat << 'EOF' > "$ISSUE_DIR/clean_r6/R6.swift"
import SwiftUI
struct V: View {
    var body: some View {
        Button { go() } label: { let discarded = Image(systemName: "trash"); return EmptyView() }
    }
}
EOF
python3 - "$ISSUE_DIR" << 'PY'
import os, sys
d = sys.argv[1]
q = chr(34); bs = chr(92)
with open(os.path.join(d, "deep_interp", "Deep.swift"), "w") as fh:
    fh.write("let text = " + (q + bs + "(") * 3000 + q + "x" + q + (")" + q) * 3000 + "\n")
n = 3000
with open(os.path.join(d, "nested_perf", "Nested.swift"), "w") as fh:
    fh.write("Button(action: {" * n + "work()" + ("}) { Image(systemName: " + q + "trash" + q + ") }") * n + "\n")
PY

mkdir -p "$ISSUE_DIR/icon_role" "$ISSUE_DIR/role_clean"
cat << 'EOF' > "$ISSUE_DIR/icon_role/Role.swift"
import SwiftUI
struct V: View {
    var body: some View {
        Button(role: .destructive) { delete() } label: { Image(systemName: "trash") }
    }
}
EOF
cat << 'EOF' > "$ISSUE_DIR/role_clean/Role.swift"
import SwiftUI
struct V: View {
    var body: some View {
        Button(role: .destructive) { let i = Image(systemName: "trash"); use(i) } label: { Text("Delete") }
    }
}
EOF

mkdir -p "$ISSUE_DIR/icon_bad4"
cat << 'EOF' > "$ISSUE_DIR/icon_bad4/InterpComment.swift"
import SwiftUI
func f(_ n: Int) -> Int { n }
let a = "Value \(f(/* ( " */ 1))"
struct V: View {
    var body: some View {
        Button(action: {}) { Image(systemName: "trash") }
    }
}
EOF

mkdir -p "$ISSUE_DIR/icon_bad3" "$ISSUE_DIR/lexer_clean2"
cat << 'EOF' > "$ISSUE_DIR/icon_bad3/Nested.swift"
import SwiftUI
struct V: View {
    var body: some View {
        Button(action: { confirm(title: "Delete?") }) {
            Image(systemName: "trash")
        }
        Button(action: { log(label: { Text("log") }) }) { Image(systemName: "gear") }
        Button(action: {}) { Image(systemName: "xmark") }.accessibilityHidden(isLoading == true)
    }
}
EOF

cat << 'EOF' > "$ISSUE_DIR/lexer_clean2/Interp.swift"
import SwiftUI
let a = "Value \(f("Button(action: {}) { Image(systemName: icon) }"))"
let b = #"before \#"# Button(action: {}) { Image(systemName: "trash") } after"#
struct V: View {
    var body: some View { Text(a + b).font(.body) }
}
EOF

python3 - "$ISSUE_DIR/big/Big.swift" << 'PY'
import sys
block = 'struct V%d: View {\n    var body: some View {\n        Button(action: {}) { Image(systemName: "trash") }\n    }\n}\n'
with open(sys.argv[1], "w") as f:
    for i in range(16000):
        f.write(block % i)
PY

OUT=$($AUDIT "$ISSUE_DIR/sweep15" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if [ "$(echo "$OUT" | grep -c "APPLE-ACCESSIBILITY-VOICEOVER  (")" -eq 2 ] && echo "$OUT" | grep -q "S.swift:19)" && echo "$OUT" | grep -q "S.swift:20)"; then
  ok "#834 titled by a variable, parenthesized, spaced dot, #if block, escaped names, accessibility(label:/hidden:), representation and ((true)) all read, and an escaped Button or a disabled label is still reported"
else
  bad "#834 the round 15 sweep cases changed. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/multi_closure" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if [ "$(echo "$OUT" | grep -c "APPLE-ACCESSIBILITY-VOICEOVER  (")" -eq 1 ] && echo "$OUT" | grep -q "M.swift:7)"; then
  ok "#834 a modifier with several trailing closures does not end the chain before its accessibilityLabel"
else
  bad "#834 a multi-closure modifier hid a later accessibilityLabel, or a real finding was lost. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/qualified" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if [ "$(echo "$OUT" | grep -c "APPLE-ACCESSIBILITY-VOICEOVER  (")" -eq 1 ] && echo "$OUT" | grep -q "Q.swift:4)"; then
  ok "#834 SwiftUI.Button is read as a Button, another module's or a member's Button is not"
else
  bad "#834 a SwiftUI-qualified Button was missed, or an unrelated member Button was flagged. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/regex_esc" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if [ "$(echo "$OUT" | grep -c "APPLE-ACCESSIBILITY-VOICEOVER  (")" -eq 1 ] && echo "$OUT" | grep -q "Esc.swift:6)"; then
  ok "#834 an escaped delimiter inside a #/regex/# literal does not end it early, in code or interpolation"
else
  bad "#834 an escaped regex delimiter ended the literal early or hid the real Button. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/regex_lit" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if [ "$(echo "$OUT" | grep -c "APPLE-ACCESSIBILITY-VOICEOVER  (")" -eq 1 ] && echo "$OUT" | grep -q "Regex.swift:6)"; then
  ok "#834 a Button inside a #/regex/# literal is ignored, inside interpolation too, and the real Button after it is found"
else
  bad "#834 a regex literal was read as code, or hid the real Button. Output:"; echo "$OUT"
fi

for CASE in chain_perf:1:"3200 chained local bindings" mod_perf:32000:"32000 Buttons nested in modifiers"; do
  DIRN="${CASE%%:*}"; REST="${CASE#*:}"; WANT="${REST%%:*}"; NAME="${REST#*:}"
  START=$(python3 -c 'import time; print(time.time())')
  OUT=$($AUDIT "$ISSUE_DIR/$DIRN" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1); RC=$?
  ELAPSED=$(python3 -c "import time; print(round(time.time() - $START, 2))")
  COUNT=$(echo "$OUT" | grep -c "APPLE-ACCESSIBILITY-VOICEOVER  (")
  if [ "$RC" -eq 0 ] && [ "$COUNT" -eq "$WANT" ] && python3 -c "import sys; sys.exit(0 if $ELAPSED < 5 else 1)"; then
    ok "#834 $NAME report $WANT finding(s) in under 5s (${ELAPSED}s)"
  else
    bad "#834 $NAME were slow or miscounted (rc=$RC count=$COUNT want=$WANT ${ELAPSED}s)"
  fi
done

OUT=$($AUDIT "$ISSUE_DIR/icon_r7" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if echo "$OUT" | grep -q "R7.swift:4)" && ! echo "$OUT" | grep -q "R7.swift:5)"; then
  ok "#834 a returned local icon is flagged, and (documented limit) a Text anywhere in the label counts, even after a return"
else
  bad "#834 whole-label behaviour changed for a returned local or a Text after return. Output:"; echo "$OUT"
fi

START=$(python3 -c 'import time; print(time.time())')
OUT=$($AUDIT "$ISSUE_DIR/nested_labels" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1); RC=$?
ELAPSED=$(python3 -c "import time; print(round(time.time() - $START, 2))")
if [ "$RC" -eq 0 ] && python3 -c "import sys; sys.exit(0 if $ELAPSED < 3 else 1)"; then
  ok "#834 16000 nested Button labels scan in under 3s (${ELAPSED}s)"
else
  bad "#834 nested labels were slow (rc=$RC ${ELAPSED}s)"
fi

OUT=$($AUDIT "$ISSUE_DIR/icon_r6" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if echo "$OUT" | grep -q "R6.swift:4)" && ! echo "$OUT" | grep -q "R6.swift:5)"; then
  ok "#834 a long comment before label: does not hide an icon label, and (documented limit) an unused local Text counts as a label"
else
  bad "#834 a comment before label: hid an icon label, or whole-label behaviour changed. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/clean_r6" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if echo "$OUT" | grep -q "R6.swift:4)"; then
  ok "#834 (documented limit) an unused local Image in a label is still reported as a possible icon-only Button"
else
  bad "#834 whole-label behaviour changed for an unused local Image. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/deep_interp" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1); RC=$?
if [ "$RC" -eq 0 ] && ! echo "$OUT" | grep -q "Traceback"; then
  ok "#834 3000 levels of string interpolation scan without a crash"
else
  bad "#834 deep interpolation crashed the audit (rc=$RC). Output:"; echo "$OUT" | tail -3
fi

START=$(python3 -c 'import time; print(time.time())')
OUT=$($AUDIT "$ISSUE_DIR/nested_perf" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1); RC=$?
ELAPSED=$(python3 -c "import time; print(round(time.time() - $START, 2))")
COUNT=$(echo "$OUT" | grep -c "APPLE-ACCESSIBILITY-VOICEOVER  (")
if [ "$RC" -eq 0 ] && [ "$COUNT" -eq 3000 ] && python3 -c "import sys; sys.exit(0 if $ELAPSED < 3 else 1)"; then
  ok "#834 3000 nested Buttons report all 3000 in under 3s (${ELAPSED}s)"
else
  bad "#834 nested Buttons were slow or miscounted (rc=$RC count=$COUNT ${ELAPSED}s)"
fi

OUT=$($AUDIT "$ISSUE_DIR/icon_role" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if [ "$(echo "$OUT" | grep -c "APPLE-ACCESSIBILITY-VOICEOVER  (")" -eq 1 ]; then
  ok "#834 a role Button reads its label: closure, not its action"
else
  bad "#834 a role Button with an icon label was missed. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/role_clean" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if echo "$OUT" | grep -q "Clean. No accessibility compliance regressions found."; then
  ok "#834 an Image inside the action does not flag a Button with a Text label"
else
  bad "#834 an Image in the action flagged a Text-labelled Button. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/icon_bad4" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if [ "$(echo "$OUT" | grep -c "APPLE-ACCESSIBILITY-VOICEOVER  (")" -eq 1 ]; then
  ok "#834 a comment inside string interpolation does not hide the code after it"
else
  bad "#834 a comment inside interpolation swallowed the rest of the file. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/icon_bad3" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if [ "$(echo "$OUT" | grep -c "APPLE-ACCESSIBILITY-VOICEOVER  (")" -eq 3 ]; then
  ok "#834 a title or label inside the action, or conditional hiding, does not hide an icon button"
else
  bad "#834 an action argument or conditional hiding suppressed an icon button. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/lexer_clean2" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if echo "$OUT" | grep -q "Clean. No accessibility compliance regressions found."; then
  ok "#834 buttons inside string interpolation and escaped raw strings are not flagged"
else
  bad "#834 flagged a button inside interpolation or an escaped raw string. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/icon_bad2" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if [ "$(echo "$OUT" | grep -c "APPLE-ACCESSIBILITY-VOICEOVER  (")" -eq 3 ]; then
  ok "#834 inline label closure, spaced Image (, and a sibling label on the same line are all flagged"
else
  bad "#834 missed an inline, spaced, or sibling-shadowed icon button. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/lexer_clean" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if echo "$OUT" | grep -q "Clean. No accessibility compliance regressions found."; then
  ok "#834 buttons inside nested comments, raw strings, and multiline strings are not flagged"
else
  bad "#834 flagged a button that only exists in a comment or string. Output:"; echo "$OUT"
fi

BUDGET="${A11Y_PERF_BUDGET:-10}"
START=$(python3 -c 'import time; print(time.time())')
BIG_OUT=$($AUDIT "$ISSUE_DIR/big" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1); BIG_RC=$?
ELAPSED=$(python3 -c "import time; print(round(time.time() - $START, 2))")
BIG_COUNT=$(echo "$BIG_OUT" | grep -c "APPLE-ACCESSIBILITY-VOICEOVER  (")
if [ "$BIG_RC" -eq 0 ] && [ "$BIG_COUNT" -eq 16000 ] && python3 -c "import sys; sys.exit(0 if $ELAPSED < $BUDGET else 1)"; then
  ok "#834 a 1.5 MB Swift file reports all 16000 buttons in under ${BUDGET}s (${ELAPSED}s)"
else
  bad "#834 large file scan failed, missed buttons, or ran over ${BUDGET}s (rc=$BIG_RC count=$BIG_COUNT ${ELAPSED}s)"
fi

OUT=$($AUDIT "$ISSUE_DIR/icon_bad" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if [ "$(echo "$OUT" | grep -c "APPLE-ACCESSIBILITY-VOICEOVER  (")" -eq 2 ]; then
  ok "#834 flagged both icon-only systemName buttons without accessibilityLabel"
else
  bad "#834 missed an icon-only systemName button. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/icon_good" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if echo "$OUT" | grep -q "Clean. No accessibility compliance regressions found."; then
  ok "#834 labeled, titled, and Label-based icon buttons are not flagged"
else
  bad "#834 false positive on a labeled icon button. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/clean" 2>&1)
if echo "$OUT" | grep -q "Clean. No accessibility compliance regressions found."; then
  ok "#834 a clean file with no interaction gets no finding (haptics, UIKit)"
else
  bad "#834 clean file produced findings. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/tap" --rule APPLE-ACCESSIBILITY-HAPTICS 2>&1)
if echo "$OUT" | grep -q "\[LOW\] APPLE-ACCESSIBILITY-HAPTICS"; then
  ok "#834 haptics stays an advisory LOW finding on a real tap interaction"
else
  bad "#834 haptics not reported as LOW advisory on a real interaction. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/clean" --rule APPLE-ACCESSIBILITY-DYNAMIC 2>&1); RC=$?
if [ "$RC" -ne 0 ] && ! echo "$OUT" | grep -q "Clean."; then
  ok "An unknown --rule is an error, never a Clean result"
else
  bad "An unknown --rule reported Clean or exited 0 (rc=$RC). Output:"; echo "$OUT"
fi
rm -rf "$ISSUE_DIR" 2>/dev/null || true

echo ""
echo "Accessibility Compliance test suite complete: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
