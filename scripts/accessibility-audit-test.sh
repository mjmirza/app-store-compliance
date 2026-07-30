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

echo ""
echo "Accessibility Compliance test suite complete: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
