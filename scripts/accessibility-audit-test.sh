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
if grep -q "Clean. No accessibility compliance regressions found." <<<"$OUT_COMPLIANT"; then
  ok "Compliant directory produced 0 findings"
else
  bad "Compliant directory produced unexpected findings. Output:"
  echo "$OUT_COMPLIANT"
fi

# Test 2: Run on regression folder. Should detect regressions.
OUT_REGRESSION=$($AUDIT "$REGRESSION_DIR" 2>&1)

# Check Rule 1: APPLE-ACCESSIBILITY-VOICEOVER
if grep -q "APPLE-ACCESSIBILITY-VOICEOVER" <<<"$OUT_REGRESSION"; then
  ok "Flagged APPLE-ACCESSIBILITY-VOICEOVER"
else
  bad "Failed to flag APPLE-ACCESSIBILITY-VOICEOVER"
fi

# Check Rule 2: APPLE-ACCESSIBILITY-DYNAMICTYPE
if grep -q "APPLE-ACCESSIBILITY-DYNAMICTYPE" <<<"$OUT_REGRESSION"; then
  ok "Flagged APPLE-ACCESSIBILITY-DYNAMICTYPE"
else
  bad "Failed to flag APPLE-ACCESSIBILITY-DYNAMICTYPE"
fi

# Check Rule 3: APPLE-ACCESSIBILITY-REDUCEMOTION
if grep -q "APPLE-ACCESSIBILITY-REDUCEMOTION" <<<"$OUT_REGRESSION"; then
  ok "Flagged APPLE-ACCESSIBILITY-REDUCEMOTION"
else
  bad "Failed to flag APPLE-ACCESSIBILITY-REDUCEMOTION"
fi

# Check Rule 4: APPLE-ACCESSIBILITY-COLORCONTRAST
if grep -q "APPLE-ACCESSIBILITY-COLORCONTRAST" <<<"$OUT_REGRESSION"; then
  ok "Flagged APPLE-ACCESSIBILITY-COLORCONTRAST"
else
  bad "Failed to flag APPLE-ACCESSIBILITY-COLORCONTRAST"
fi

# Check Rule 5: APPLE-ACCESSIBILITY-HAPTICS
if grep -q "APPLE-ACCESSIBILITY-HAPTICS" <<<"$OUT_REGRESSION"; then
  ok "Flagged APPLE-ACCESSIBILITY-HAPTICS"
else
  bad "Failed to flag APPLE-ACCESSIBILITY-HAPTICS"
fi

# Check Rule 6: APPLE-ACCESSIBILITY-KEYBOARD
if grep -q "APPLE-ACCESSIBILITY-KEYBOARD" <<<"$OUT_REGRESSION"; then
  ok "Flagged APPLE-ACCESSIBILITY-KEYBOARD"
else
  bad "Failed to flag APPLE-ACCESSIBILITY-KEYBOARD"
fi

# Check Rule 7: ANDROID-ACCESSIBILITY-TALKBACK
if grep -q "ANDROID-ACCESSIBILITY-TALKBACK" <<<"$OUT_REGRESSION"; then
  ok "Flagged ANDROID-ACCESSIBILITY-TALKBACK"
else
  bad "Failed to flag ANDROID-ACCESSIBILITY-TALKBACK"
fi

# Check Rule 8: ANDROID-ACCESSIBILITY-FONTSCALING
if grep -q "ANDROID-ACCESSIBILITY-FONTSCALING" <<<"$OUT_REGRESSION"; then
  ok "Flagged ANDROID-ACCESSIBILITY-FONTSCALING"
else
  bad "Failed to flag ANDROID-ACCESSIBILITY-FONTSCALING"
fi

# Check Rule 9: ANDROID-ACCESSIBILITY-HIGHCONTRAST
if grep -q "ANDROID-ACCESSIBILITY-HIGHCONTRAST" <<<"$OUT_REGRESSION"; then
  ok "Flagged ANDROID-ACCESSIBILITY-HIGHCONTRAST"
else
  bad "Failed to flag ANDROID-ACCESSIBILITY-HIGHCONTRAST"
fi

# Check Rule 10: ANDROID-ACCESSIBILITY-SCANNER
if grep -q "ANDROID-ACCESSIBILITY-SCANNER" <<<"$OUT_REGRESSION"; then
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
if [ "$(echo "$OUT" | grep -c "APPLE-ACCESSIBILITY-VOICEOVER  (")" -eq 2 ] && grep -q "S.swift:19)" <<<"$OUT" && grep -q "S.swift:20)" <<<"$OUT"; then
  ok "#834 titled by a variable, parenthesized, spaced dot, #if block, escaped names, accessibility(label:/hidden:), representation and ((true)) all read, and an escaped Button or a disabled label is still reported"
else
  bad "#834 the round 15 sweep cases changed. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/multi_closure" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if [ "$(echo "$OUT" | grep -c "APPLE-ACCESSIBILITY-VOICEOVER  (")" -eq 1 ] && grep -q "M.swift:7)" <<<"$OUT"; then
  ok "#834 a modifier with several trailing closures does not end the chain before its accessibilityLabel"
else
  bad "#834 a multi-closure modifier hid a later accessibilityLabel, or a real finding was lost. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/qualified" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if [ "$(echo "$OUT" | grep -c "APPLE-ACCESSIBILITY-VOICEOVER  (")" -eq 1 ] && grep -q "Q.swift:4)" <<<"$OUT"; then
  ok "#834 SwiftUI.Button is read as a Button, another module's or a member's Button is not"
else
  bad "#834 a SwiftUI-qualified Button was missed, or an unrelated member Button was flagged. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/regex_esc" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if [ "$(echo "$OUT" | grep -c "APPLE-ACCESSIBILITY-VOICEOVER  (")" -eq 1 ] && grep -q "Esc.swift:6)" <<<"$OUT"; then
  ok "#834 an escaped delimiter inside a #/regex/# literal does not end it early, in code or interpolation"
else
  bad "#834 an escaped regex delimiter ended the literal early or hid the real Button. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/regex_lit" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if [ "$(echo "$OUT" | grep -c "APPLE-ACCESSIBILITY-VOICEOVER  (")" -eq 1 ] && grep -q "Regex.swift:6)" <<<"$OUT"; then
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
if grep -q "R7.swift:4)" <<<"$OUT" && ! grep -q "R7.swift:5)" <<<"$OUT"; then
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
if grep -q "R6.swift:4)" <<<"$OUT" && ! grep -q "R6.swift:5)" <<<"$OUT"; then
  ok "#834 a long comment before label: does not hide an icon label, and (documented limit) an unused local Text counts as a label"
else
  bad "#834 a comment before label: hid an icon label, or whole-label behaviour changed. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/clean_r6" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if grep -q "R6.swift:4)" <<<"$OUT"; then
  ok "#834 (documented limit) an unused local Image in a label is still reported as a possible icon-only Button"
else
  bad "#834 whole-label behaviour changed for an unused local Image. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/deep_interp" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1); RC=$?
if [ "$RC" -eq 0 ] && ! grep -q "Traceback" <<<"$OUT"; then
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
if grep -q "Clean. No accessibility compliance regressions found." <<<"$OUT"; then
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
if grep -q "Clean. No accessibility compliance regressions found." <<<"$OUT"; then
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
if grep -q "Clean. No accessibility compliance regressions found." <<<"$OUT"; then
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
if grep -q "Clean. No accessibility compliance regressions found." <<<"$OUT"; then
  ok "#834 labeled, titled, and Label-based icon buttons are not flagged"
else
  bad "#834 false positive on a labeled icon button. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/clean" 2>&1)
if grep -q "Clean. No accessibility compliance regressions found." <<<"$OUT"; then
  ok "#834 a clean file with no interaction gets no finding (haptics, UIKit)"
else
  bad "#834 clean file produced findings. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/tap" --rule APPLE-ACCESSIBILITY-HAPTICS 2>&1)
if grep -q "\[LOW\] APPLE-ACCESSIBILITY-HAPTICS" <<<"$OUT"; then
  ok "#834 haptics stays an advisory LOW finding on a real tap interaction"
else
  bad "#834 haptics not reported as LOW advisory on a real interaction. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$ISSUE_DIR/clean" --rule APPLE-ACCESSIBILITY-DYNAMIC 2>&1); RC=$?
if [ "$RC" -ne 0 ] && ! grep -q "Clean." <<<"$OUT"; then
  ok "An unknown --rule is an error, never a Clean result"
else
  bad "An unknown --rule reported Clean or exited 0 (rc=$RC). Output:"; echo "$OUT"
fi
rm -rf "$ISSUE_DIR" 2>/dev/null || true

# Issue #1000. Edge cases from the October review.
I1000_DIR=$(mktemp -d "/tmp/access_issue1000_XXXXXX")
mkdir -p "$I1000_DIR/paren_label" "$I1000_DIR/comment_image" "$I1000_DIR/code_image"
cat << 'EOF' > "$I1000_DIR/paren_label/P.swift"
import SwiftUI
struct V: View {
    var body: some View {
        Button(action: {}, label: ({ Image(systemName: "trash") }))
        Button(action: {}, label: (({ Image(systemName: "gear") })))
        Button(action: {}, label: ({ Image(systemName: "star") })).accessibilityLabel("Star")
    }
}
EOF
cat << 'EOF' > "$I1000_DIR/comment_image/C.swift"
import SwiftUI
// Example: Image("logo")
/* Another example, Image("banner") */
struct V: View {
    var body: some View {
        Text("Hello")
    }
}
EOF
cat << 'EOF' > "$I1000_DIR/code_image/D.swift"
import SwiftUI
struct V: View {
    var body: some View {
        Image("logo") // accessibilityLabel is still missing here
    }
}
EOF

OUT=$($AUDIT "$I1000_DIR/paren_label" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if [ "$(echo "$OUT" | grep -c "APPLE-ACCESSIBILITY-VOICEOVER  (")" -eq 2 ]; then
  ok "#1000 a label closure wrapped in parentheses is read, so the icon-only Button is reported"
else
  bad "#1000 a parenthesised label closure was not read. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$I1000_DIR/comment_image" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if grep -q "Clean. No accessibility compliance regressions found." <<<"$OUT"; then
  ok "#1000 an Image inside a comment is not reported as a VoiceOver finding"
else
  bad "#1000 the Image rule read a comment. Output:"; echo "$OUT"
fi

OUT=$($AUDIT "$I1000_DIR/code_image" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if [ "$(echo "$OUT" | grep -c "APPLE-ACCESSIBILITY-VOICEOVER  (")" -eq 1 ] && grep -q 'Image("logo")' <<<"$OUT"; then
  ok "#1000 a real Image in code is still reported even when a comment names accessibilityLabel"
else
  bad "#1000 a real unlabelled Image in code was not reported. Output:"; echo "$OUT"
fi
rm -rf "$I1000_DIR" 2>/dev/null || true

# A Swift bare regex holding a quote never hides the Image after it
R8_DIR="$(mktemp -d)"; mkdir -p "$R8_DIR/app"
printf '%s\n' 'import SwiftUI' 'struct V: View { var body: some View { let regex = /"/; let s = " // "; Image("logo") } }' > "$R8_DIR/app/V.swift"
OUT=$($AUDIT "$R8_DIR/app" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if grep -q 'Image("logo")' <<<"$OUT"; then ok "an Image after a Swift regex holding a quote is still reported"; else bad "an Image after a Swift regex holding a quote was lost. Output:"; echo "$OUT"; fi
rm -rf "$R8_DIR" 2>/dev/null || true

# A closed block comment at the start of a line never hides the code after it
R9_DIR="$(mktemp -d)"; mkdir -p "$R9_DIR/app"
printf '%s\n' 'import SwiftUI' '/* comment */ let r = /"/; let image = Image("hero")' > "$R9_DIR/app/V.swift"
OUT=$($AUDIT "$R9_DIR/app" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if grep -q 'Image("hero")' <<<"$OUT"; then ok "an Image after a closed block comment and a regex is still reported"; else bad "an Image after a closed block comment and a regex was lost. Output:"; echo "$OUT"; fi
rm -rf "$R9_DIR" 2>/dev/null || true
# Code between two block comments on one line is never blanked
R10_DIR="$(mktemp -d)"; mkdir -p "$R10_DIR/app"
printf '%s\n' 'import SwiftUI' '/* comment */ let r = /"/; let image = Image("hero") /* tail */' > "$R10_DIR/app/V.swift"
OUT=$($AUDIT "$R10_DIR/app" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if grep -q 'Image("hero")' <<<"$OUT"; then ok "an Image between two block comments is still reported"; else bad "an Image between two block comments was lost. Output:"; echo "$OUT"; fi
rm -rf "$R10_DIR" 2>/dev/null || true
# A Swift continuation line led by * (multiplication) is code, never a comment line
R16_DIR="$(mktemp -d)"; mkdir -p "$R16_DIR/app"
printf '%s\n' 'import SwiftUI' 'func score(_ p: Regex<Substring>) -> Double { 0.25 }' 'struct Demo: View {' '    var body: some View {' '        Color.red.opacity(2' '            * score(/"/)).overlay(Image("hero"))' '    }' '}' > "$R16_DIR/app/V.swift"
OUT=$($AUDIT "$R16_DIR/app" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if grep -q 'Image("hero")' <<<"$OUT"; then ok "an Image on a line led by * is still reported"; else bad "an Image on a line led by * was lost. Output:"; echo "$OUT"; fi
rm -rf "$R16_DIR" 2>/dev/null || true
# A /* inside a Swift multiline string never blanks the code after the string
R17_DIR="$(mktemp -d)"; mkdir -p "$R17_DIR/app"
printf '%s\n' 'import SwiftUI' 'let example = """' '/*' '"""' 'let regex = /"/; let image = Image("hero")' > "$R17_DIR/app/V.swift"
OUT=$($AUDIT "$R17_DIR/app" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if grep -q 'Image("hero")' <<<"$OUT"; then ok "an Image after a multiline string holding /* is still reported"; else bad "an Image after a multiline string holding /* was lost. Output:"; echo "$OUT"; fi
rm -rf "$R17_DIR" 2>/dev/null || true
# An escaped triple quote inside a Swift multiline string never closes it
R18_DIR="$(mktemp -d)"; mkdir -p "$R18_DIR/app"
printf '%s\n' 'import SwiftUI' 'let example = """' '\"""' '/*' '"""' 'let regex = /"/; let image = Image("hero")' > "$R18_DIR/app/V.swift"
OUT=$($AUDIT "$R18_DIR/app" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if grep -q 'Image("hero")' <<<"$OUT"; then ok "an Image after a string holding an escaped triple quote is still reported"; else bad "an Image after a string holding an escaped triple quote was lost. Output:"; echo "$OUT"; fi
rm -rf "$R18_DIR" 2>/dev/null || true
# A Swift raw multiline string with an escaped delimiter inside never closes early
R20_DIR="$(mktemp -d)"; mkdir -p "$R20_DIR/app"
printf '%s\n' 'import SwiftUI' 'let example = #"""' '\#"""' '/*' '"""#' 'let regex = /"/; let image = Image("hero")' > "$R20_DIR/app/V.swift"
OUT=$($AUDIT "$R20_DIR/app" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if grep -q 'Image("hero")' <<<"$OUT"; then ok "an Image after a raw multiline string is still reported"; else bad "an Image after a raw multiline string was lost. Output:"; echo "$OUT"; fi
rm -rf "$R20_DIR" 2>/dev/null || true
# A triple quote inside a // comment never opens a string
R21_DIR="$(mktemp -d)"; mkdir -p "$R21_DIR/app"
printf '%s\n' 'import SwiftUI' '// """' 'let example = """' '/*' '"""' 'let regex = /"/; let image = Image("hero")' > "$R21_DIR/app/V.swift"
OUT=$($AUDIT "$R21_DIR/app" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if grep -q 'Image("hero")' <<<"$OUT"; then ok "an Image after a comment holding a triple quote is still reported"; else bad "an Image after a comment holding a triple quote was lost. Output:"; echo "$OUT"; fi
rm -rf "$R21_DIR" 2>/dev/null || true
# A triple quote after an inline // comment never opens a string
R22_DIR="$(mktemp -d)"; mkdir -p "$R22_DIR/app"
printf '%s\n' 'import SwiftUI' 'let n = 1 // """' 'let example = """' '/*' '"""' 'let regex = /"/; let image = Image("hero")' > "$R22_DIR/app/V.swift"
OUT=$($AUDIT "$R22_DIR/app" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if grep -q 'Image("hero")' <<<"$OUT"; then ok "an Image after an inline comment holding a triple quote is still reported"; else bad "an Image after an inline comment holding a triple quote was lost. Output:"; echo "$OUT"; fi
rm -rf "$R22_DIR" 2>/dev/null || true
# An interpolated Image inside a multiline string is code, even on a line led by //
R23_DIR="$(mktemp -d)"; mkdir -p "$R23_DIR/app"
printf '%s\n' 'import SwiftUI' 'let q = #"three: """ here"#' 'let text = Text("""' '// \(Image("hero"))' '""")' > "$R23_DIR/app/V.swift"
OUT=$($AUDIT "$R23_DIR/app" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if grep -q 'Image("hero")' <<<"$OUT"; then ok "an interpolated Image inside a string is still reported"; else bad "an interpolated Image inside a string was lost. Output:"; echo "$OUT"; fi
rm -rf "$R23_DIR" 2>/dev/null || true
# A raw-string interpolation such as \#( is code inside a string, even on a line led by //
R24_DIR="$(mktemp -d)"; mkdir -p "$R24_DIR/app"
printf '%s\n' 'import SwiftUI' 'let q = #"three: """ here"#' 'let text = Text(#"""' '// \#(Image("hero"))' '"""#)' > "$R24_DIR/app/V.swift"
OUT=$($AUDIT "$R24_DIR/app" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
if grep -q 'Image("hero")' <<<"$OUT"; then ok "a raw-string interpolated Image is still reported"; else bad "a raw-string interpolated Image was lost. Output:"; echo "$OUT"; fi
rm -rf "$R24_DIR" 2>/dev/null || true
# A wrapped axis has no explicit size, but must not hide any explicit dimension.
WRAP_DIR="$(mktemp -d)"
cat <<'EOF2' > "$WRAP_DIR/mixed_targets.xml"
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content">
    <Button android:layout_width="36dp" android:layout_height="wrap_content" />
    <ImageView android:layout_width="24dp" android:layout_height="24dp" android:clickable="true" />
    <Button android:layout_width="match_parent" android:layout_height="56dp"
        android:minWidth="40dp" />
    <Button android:layout_width="96dp" android:layout_height="56dp" android:minWidth="40dp" />
    <Button android:layout_width="40dp" android:layout_height="48dp" android:minWidth="48dp" />
    <androidx.appcompat.widget.AppCompatCheckBox android:layout_width="24dp" android:layout_height="48dp" />
    <Button android:onClick="@{() -> viewModel.save()}" android:layout_width="32dp" android:layout_height="48dp" />
    <TextView android:layout_width="30dp" android:layout_height="48dp" android:longClickable="true" />
    <Button android:text='Save' android:layout_width="28dp" android:layout_height="48dp" />
    <NumberPicker android:layout_width="26dp" android:layout_height="120dp" />
    <TextView android:onLongClick="@{() -> vm.showMenu()}" android:layout_width="22dp" android:layout_height="48dp" />
    <ImageView android:layout_width="20dp" android:layout_height="20dp" />
    <com.google.android.material.textview.MaterialTextView android:layout_width="match_parent" android:layout_height="19dp" />
    <TextView android:layout_width="match_parent" android:layout_height="40dp" android:autoLink="web" />
    <ImageView android:layout_width="34dp" android:layout_height="48dp" android:clickable="@bool/image_is_clickable" />
    <!-- <Button android:layout_width="18dp" android:layout_height="18dp" /> -->
    <RatingBar android:layout_width="wrap_content" android:layout_height="17dp" android:isIndicator="true" />
    <View android:layout_width="match_parent" android:layout_height="1dp" />
    <View android:layout_width="match_parent" android:layout_height="1dp" android:clickable="false" />
    <Button android:layout_width="16dp" android:layout_height="16dp" android:visibility="gone" />
    <CheckedTextView android:layout_width="match_parent" android:layout_height="15dp" android:checked="true" />
    <CheckBox style="@style/RowCheck" android:layout_width="14dp" android:layout_height="14dp" />
    <Button android:layout_width="48dp" android:layout_height="48dp" />
    <Button android:layout_width="wrap_content" android:layout_height="wrap_content" />
</LinearLayout>
EOF2
printf '<resources><bool name="image_is_clickable">true</bool></resources>\n' > "$WRAP_DIR/bools.xml"
OUT=$($AUDIT "$WRAP_DIR" --rule ANDROID-ACCESSIBILITY-SCANNER 2>&1)
if [ "$(echo "$OUT" | grep -c 'ANDROID-ACCESSIBILITY-SCANNER  (')" -eq 10 ] \
    && grep -q 'context: android:layout_width="36dp"' <<<"$OUT" \
    && grep -q 'context: android:layout_width="24dp"' <<<"$OUT" \
    && grep -q 'context: android:layout_height="24dp"' <<<"$OUT" \
    && grep -q 'context: android:layout_width="40dp"' <<<"$OUT" \
    && grep -q 'context: android:layout_width="32dp"' <<<"$OUT" \
    && grep -q 'context: android:layout_width="30dp"' <<<"$OUT" \
    && grep -q 'context: android:layout_width="28dp"' <<<"$OUT" \
    && grep -q 'context: android:layout_width="26dp"' <<<"$OUT" \
    && grep -q 'context: android:layout_width="22dp"' <<<"$OUT" \
    && ! grep -q 'context: android:layout_height="40dp"' <<<"$OUT" \
    && ! grep -q 'context: android:layout_width="34dp"' <<<"$OUT" \
    && ! grep -q 'context: android:layout_width="16dp"' <<<"$OUT" \
    && ! grep -q 'context: android:layout_height="15dp"' <<<"$OUT" \
    && ! grep -q 'context: android:layout_width="14dp"' <<<"$OUT" \
    && ! grep -q 'context: android:layout_width="18dp"' <<<"$OUT" \
    && ! grep -q 'context: android:layout_height="17dp"' <<<"$OUT" \
    && ! grep -q 'context: android:layout_width="20dp"' <<<"$OUT" \
    && ! grep -q 'context: android:layout_height="19dp"' <<<"$OUT"; then
  ok "wrap_content does not hide an undersized control, and dividers stay silent"
else
  bad "wrap_content does not hide an undersized control, and dividers stay silent"
  echo "$OUT"
fi
rm -rf "$WRAP_DIR"
# A value read from a resource, a link that depends on the text, and an indicator are unknown or inert, so they stay silent.
RES_DIR="$(mktemp -d)"; mkdir -p "$RES_DIR/res/layout" "$RES_DIR/res/values" "$RES_DIR/res/values-sw600dp"
cat <<'EOF4' > "$RES_DIR/res/layout/x.xml"
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent" android:layout_height="wrap_content">
    <Button android:layout_width="32dp" android:layout_height="48dp" android:clickable="@bool/tap" />
    <TextView android:layout_width="match_parent" android:layout_height="24dp" android:autoLink="web" android:linksClickable="@bool/links" />
    <TextView android:layout_width="wrap_content" android:layout_height="23dp" android:autoLink="web" android:linksClickable="@bool/alias" />
    <RatingBar android:layout_width="wrap_content" android:layout_height="22dp" android:isIndicator="@bool/read_only" />
    <RatingBar style="?android:attr/ratingBarStyleSmall" android:layout_width="wrap_content" android:layout_height="21dp" />
    <TextView android:layout_width="wrap_content" android:layout_height="20dp" android:focusable="true" />
    <ImageView android:layout_width="19dp" android:layout_height="48dp" android:clickable="@bool/inert" />
</LinearLayout>
EOF4
printf '<resources><bool name="tap">true</bool><bool name="links">false</bool><bool name="alias">@bool/on</bool><bool name="on">true</bool><bool name="read_only">false</bool><!-- <bool name="inert">true</bool> --><bool name="inert">false</bool></resources>\n' > "$RES_DIR/res/values/b.xml"
printf '<resources><bool name="tap">false</bool><bool name="read_only">true</bool></resources>\n' > "$RES_DIR/res/values-sw600dp/b.xml"
OUT=$($AUDIT "$RES_DIR" --rule ANDROID-ACCESSIBILITY-SCANNER 2>&1)
if [ "$(echo "$OUT" | grep -c 'ANDROID-ACCESSIBILITY-SCANNER  (')" -eq 0 ]; then
  ok "resource-driven, text-dependent and indicator controls stay silent"
else
  bad "resource-driven, text-dependent and indicator controls stay silent"
  echo "$OUT"
fi
rm -rf "$RES_DIR"
# A hidden parent, a weighted size and a Material Slider are unknown or enforced, so they stay silent.
TREE_DIR="$(mktemp -d)"
cat <<'EOF5' > "$TREE_DIR/tree.xml"
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android" android:orientation="horizontal"
    android:layout_width="match_parent" android:layout_height="wrap_content">
    <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:visibility="gone">
        <Button android:layout_width="13dp" android:layout_height="13dp" />
    </LinearLayout>
    <Button android:layout_width="12dp" android:layout_height="48dp" android:layout_weight="1" />
    <com.google.android.material.slider.Slider android:layout_width="match_parent" android:layout_height="11dp" />
    <TextView android:layout_width="10dp" android:layout_height="48dp" android:onClick="@null" />
    <Button android:layout_width="33dp" android:layout_height="48dp" />
</LinearLayout>
EOF5
OUT=$($AUDIT "$TREE_DIR" --rule ANDROID-ACCESSIBILITY-SCANNER 2>&1)
if [ "$(echo "$OUT" | grep -c 'ANDROID-ACCESSIBILITY-SCANNER  (')" -eq 1 ] && grep -q 'context: android:layout_width="33dp"' <<<"$OUT"; then
  ok "a hidden parent, a weighted size, a Material Slider and a null handler stay silent, a sibling is still reported"
else
  bad "a hidden parent, a weighted size, a Material Slider and a null handler stay silent, a sibling is still reported"
  echo "$OUT"
fi
rm -rf "$TREE_DIR"
# Only a LinearLayout or FrameLayout keeps an explicit size final. A weight hides only its own axis.
PARENT_DIR="$(mktemp -d)"
cat <<'EOF6' > "$PARENT_DIR/parents.xml"
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android" xmlns:app="http://schemas.android.com/apk/res-auto"
    android:orientation="vertical" android:layout_width="match_parent" android:layout_height="wrap_content">
    <LinearLayout android:orientation="horizontal" android:layout_width="match_parent" android:layout_height="wrap_content">
        <Button android:layout_width="0dp" android:layout_height="31dp" android:layout_weight="1" />
    </LinearLayout>
    <com.google.android.flexbox.FlexboxLayout android:layout_width="320dp" android:layout_height="wrap_content">
        <Button android:layout_width="12dp" android:layout_height="48dp" app:layout_flexGrow="1" />
    </com.google.android.flexbox.FlexboxLayout>
    <TextView android:layout_width="11dp" android:layout_height="48dp" android:clickable="@{false}" android:onClick="@{() -> vm.save()}" />
    <LinearLayout style="@style/Col" android:layout_width="wrap_content" android:layout_height="160dp">
        <Button android:layout_width="100dp" android:layout_height="29dp" android:layout_weight="1" />
    </LinearLayout>
    <com.google.android.material.floatingactionbutton.FloatingActionButton android:layout_width="28dp" android:layout_height="28dp" app:fabSize="mini" />
    <LinearLayout android:orientation="@integer/stack_orientation" android:layout_width="match_parent" android:layout_height="160dp">
        <Button android:layout_width="wrap_content" android:layout_height="9dp" android:layout_weight="1" />
    </LinearLayout>
    <FrameLayout android:scaleX="2" android:scaleY="2" android:layout_width="match_parent" android:layout_height="wrap_content">
        <ImageButton android:layout_width="8dp" android:layout_height="8dp" />
    </FrameLayout>
</LinearLayout>
EOF6
OUT=$($AUDIT "$PARENT_DIR" --rule ANDROID-ACCESSIBILITY-SCANNER 2>&1)
if [ "$(echo "$OUT" | grep -c 'ANDROID-ACCESSIBILITY-SCANNER  (')" -eq 1 ] && grep -q 'context: android:layout_height="31dp"' <<<"$OUT"; then
  ok "a weight hides only its axis, Flexbox, a disabling binding, a styled orientation and Material stay silent"
else
  bad "a weight hides only its axis, Flexbox, a disabling binding, a styled orientation and Material stay silent"
  echo "$OUT"
fi
rm -rf "$PARENT_DIR"
# A styled section is unknown, the root may be resized by an include, and a plain MaterialTextView is still judged.
MORE_DIR="$(mktemp -d)"
cat <<'EOF7' > "$MORE_DIR/more.xml"
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent" android:layout_height="wrap_content">
    <LinearLayout style="@style/HiddenSection" android:layout_width="match_parent" android:layout_height="wrap_content">
        <Button android:layout_width="27dp" android:layout_height="27dp" />
    </LinearLayout>
    <com.google.android.material.textview.MaterialTextView android:layout_width="48dp" android:layout_height="26dp" android:clickable="true" />
    <ImageButton android:layout_width="24dp" android:layout_height="24dp" android:scaleX="2" android:scaleY="2" />
</FrameLayout>
EOF7
printf '<Button xmlns:android="http://schemas.android.com/apk/res/android" android:layout_width="25dp" android:layout_height="wrap_content" />\n' > "$MORE_DIR/root_button.xml"
OUT=$($AUDIT "$MORE_DIR" --rule ANDROID-ACCESSIBILITY-SCANNER 2>&1)
if [ "$(echo "$OUT" | grep -c 'ANDROID-ACCESSIBILITY-SCANNER  (')" -eq 1 ] && grep -q 'context: android:layout_height="26dp"' <<<"$OUT"; then
  ok "a styled section, a root view and a scaled control stay silent, a clickable MaterialTextView is still reported"
else
  bad "a styled section, a root view and a scaled control stay silent, a clickable MaterialTextView is still reported"
  echo "$OUT"
fi
rm -rf "$MORE_DIR"
# A TouchDelegate in the app can widen a view, so a wrapped file stays silent as before.
TD_DIR="$(mktemp -d)"
printf '<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android" android:layout_width="match_parent" android:layout_height="wrap_content"><ImageButton android:layout_width="24dp" android:layout_height="24dp" /></FrameLayout>\n' > "$TD_DIR/td.xml"
printf 'class A { void f() { parent.setTouchDelegate(new TouchDelegate(rect, button)); } }\n' > "$TD_DIR/A.java"
OUT=$($AUDIT "$TD_DIR" --rule ANDROID-ACCESSIBILITY-SCANNER 2>&1)
if ! grep -q 'context:' <<<"$OUT"; then
  ok "a TouchDelegate in the app keeps a wrapped layout silent"
else
  bad "a TouchDelegate in the app keeps a wrapped layout silent"
  echo "$OUT"
fi
rm -f "$TD_DIR/A.java"
OUT=$($AUDIT "$TD_DIR" --rule ANDROID-ACCESSIBILITY-SCANNER 2>&1)
if [ "$(echo "$OUT" | grep -c 'context:')" -eq 2 ]; then
  ok "without a TouchDelegate the same layout is still reported"
else
  bad "without a TouchDelegate the same layout is still reported"
  echo "$OUT"
fi
rm -rf "$TD_DIR"
AL_DIR="$(mktemp -d)"
printf '<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android" android:layout_width="match_parent" android:layout_height="wrap_content" android:alpha="0"><ImageButton android:layout_width="24dp" android:layout_height="24dp" /></FrameLayout>\n' > "$AL_DIR/al.xml"
OUT=$($AUDIT "$AL_DIR" --rule ANDROID-ACCESSIBILITY-SCANNER 2>&1)
if ! grep -q 'context:' <<<"$OUT"; then
  ok "a control inside an alpha 0 panel stays silent"
else
  bad "a control inside an alpha 0 panel stays silent"
  echo "$OUT"
fi
sed -i.bak 's/android:alpha="0"/android:alpha="0.5"/' "$AL_DIR/al.xml" && rm -f "$AL_DIR/al.xml.bak"
OUT=$($AUDIT "$AL_DIR" --rule ANDROID-ACCESSIBILITY-SCANNER 2>&1)
if [ "$(echo "$OUT" | grep -c 'context:')" -eq 2 ]; then
  ok "a control inside a half-faded panel is still reported"
else
  bad "a control inside a half-faded panel is still reported"
  echo "$OUT"
fi
sed -i.bak 's/android:alpha="0.5"/android:alpha="@dimen\/panel_alpha"/' "$AL_DIR/al.xml" && rm -f "$AL_DIR/al.xml.bak"
OUT=$($AUDIT "$AL_DIR" --rule ANDROID-ACCESSIBILITY-SCANNER 2>&1)
if ! grep -q 'context:' <<<"$OUT"; then
  ok "a resource alpha that may be 0 keeps the panel silent"
else
  bad "a resource alpha that may be 0 keeps the panel silent"
  echo "$OUT"
fi
sed -i.bak 's/android:alpha="@dimen\/panel_alpha"/android:alpha="0.000"/' "$AL_DIR/al.xml" && rm -f "$AL_DIR/al.xml.bak"
OUT=$($AUDIT "$AL_DIR" --rule ANDROID-ACCESSIBILITY-SCANNER 2>&1)
if ! grep -q 'context:' <<<"$OUT"; then
  ok "an alpha written as 0.000 is still zero"
else
  bad "an alpha written as 0.000 is still zero"
  echo "$OUT"
fi
rm -rf "$AL_DIR"
SW_DIR="$(mktemp -d)"
printf '<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android" android:layout_width="match_parent" android:layout_height="wrap_content"><Switch android:layout_width="96dp" android:layout_height="24dp" /><Switch android:layout_width="22dp" android:layout_height="64dp" /><CheckBox android:layout_width="96dp" android:layout_height="23dp" /></FrameLayout>\n' > "$SW_DIR/sw.xml"
OUT=$($AUDIT "$SW_DIR" --rule ANDROID-ACCESSIBILITY-SCANNER 2>&1)
if [ "$(echo "$OUT" | grep -c 'context:')" -eq 2 ] && grep -q 'context: android:layout_height="23dp"' <<<"$OUT" && grep -q 'context: android:layout_width="22dp"' <<<"$OUT"; then
  ok "a switch is judged by its width only, a checkbox by both"
else
  bad "a switch is judged by its width only, a checkbox by both"
  echo "$OUT"
fi
rm -rf "$SW_DIR"
CP_DIR="$(mktemp -d)"
printf '<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android" android:layout_width="match_parent" android:layout_height="wrap_content"><FrameLayout android:layout_width="320dp" android:layout_height="56dp" android:onClick="selectDelivery"><RadioButton android:layout_width="24dp" android:layout_height="24dp" android:onClick="selectDelivery" /></FrameLayout></FrameLayout>\n' > "$CP_DIR/cp.xml"
OUT=$($AUDIT "$CP_DIR" --rule ANDROID-ACCESSIBILITY-SCANNER 2>&1)
if ! grep -q 'context:' <<<"$OUT"; then
  ok "a control inside a clickable row is part of the row target"
else
  bad "a control inside a clickable row is part of the row target"
  echo "$OUT"
fi
printf '<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android" android:layout_width="match_parent" android:layout_height="wrap_content"><FrameLayout android:layout_width="320dp" android:layout_height="56dp" android:onClick="openArticle"><ImageButton android:layout_width="24dp" android:layout_height="24dp" android:onClick="showMenu" /></FrameLayout></FrameLayout>\n' > "$CP_DIR/cp.xml"
OUT=$($AUDIT "$CP_DIR" --rule ANDROID-ACCESSIBILITY-SCANNER 2>&1)
if [ "$(echo "$OUT" | grep -c 'context:')" -eq 2 ]; then
  ok "a control with its own different action inside a clickable row is still reported"
else
  bad "a control with its own different action inside a clickable row is still reported"
  echo "$OUT"
fi
printf '<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android" android:layout_width="match_parent" android:layout_height="wrap_content"><FrameLayout android:layout_width="320dp" android:layout_height="56dp" android:onClick="@{() -> vm.select()}"><RadioButton android:layout_width="24dp" android:layout_height="24dp" android:onClick="@{()->vm.select()}" /></FrameLayout></FrameLayout>\n' > "$CP_DIR/cp.xml"
OUT=$($AUDIT "$CP_DIR" --rule ANDROID-ACCESSIBILITY-SCANNER 2>&1)
if ! grep -q 'context:' <<<"$OUT"; then
  ok "binding callbacks inside a clickable row are not compared as text"
else
  bad "binding callbacks inside a clickable row are not compared as text"
  echo "$OUT"
fi
rm -rf "$CP_DIR"
# A file with no wrapped axis keeps the original behaviour, every small explicit dimension is reported.
PLAIN_DIR="$(mktemp -d)"
cat <<'EOF3' > "$PLAIN_DIR/plain.xml"
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent" android:layout_height="match_parent">
    <ImageView android:layout_width="32dp" android:layout_height="32dp" />
</LinearLayout>
EOF3
OUT=$($AUDIT "$PLAIN_DIR" --rule ANDROID-ACCESSIBILITY-SCANNER 2>&1)
if [ "$(echo "$OUT" | grep -c 'ANDROID-ACCESSIBILITY-SCANNER  (')" -eq 2 ]; then
  ok "a layout with no wrap_content still reports every small dimension"
else
  bad "a layout with no wrap_content still reports every small dimension"
  echo "$OUT"
fi
rm -rf "$PLAIN_DIR"
# Long one-line expressions must not inflate output or hide any controls.
CONTEXT_DIR="$(mktemp -d)"
python3 - "$CONTEXT_DIR/Controls.swift" <<'PYTHON'
import sys
from pathlib import Path

context = "work()" + ' + "long" ' * 500
Path(sys.argv[1]).write_text(
    'Button(action: { ' + context + ' }) { Image(systemName: "trash") }\n'
    'Button(action: {}) { Image(systemName: "gear") }\n'
    'Button(action: {}) { Image(systemName: "star") }.accessibilityLabel("Star")\n'
)
PYTHON
OUT=$($AUDIT "$CONTEXT_DIR" --rule APPLE-ACCESSIBILITY-VOICEOVER 2>&1)
CONTEXT_COUNT=$(echo "$OUT" | grep -c 'APPLE-ACCESSIBILITY-VOICEOVER  (')
if [ "$CONTEXT_COUNT" -eq 2 ] \
    && ! echo "$OUT" | grep '^      context:' | awk 'length($0) > 180 { found = 1 } END { exit !found }' \
    && grep -q 'context: Button(action: {.*\.\.\.$' <<<"$OUT" \
    && grep -Fq 'context: Button(action: {}) { Image(systemName: "gear") }' <<<"$OUT"; then
  ok "reports every icon-only Button with bounded context and keeps short snippets"
else
  bad "reports every icon-only Button with bounded context and keeps short snippets"
fi
rm -rf "$CONTEXT_DIR"

echo ""
echo "Accessibility Compliance test suite complete: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
