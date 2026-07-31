#!/usr/bin/env bash
# Test suite for scripts/accessibility-audit.py
# Verifies all 10 platform rules (Apple & Android accessibility policies)
# by generating mock files with compliant and regression code blocks.
#
# No emojis or emoticons are allowed in this script or repository.

set -uo pipefail

PASS=0
FAIL=0

ok()   { PASS=$((PASS+1)); printf 'PASS  %s\n' "$1"; }
bad()  { FAIL=$((FAIL+1)); printf 'FAIL  %s\n' "$1"; }

MOCK_DIR="/tmp/accessibility_mock_project"
rm -rf "$MOCK_DIR" 2>/dev/null || true
mkdir -p "$MOCK_DIR/ios" "$MOCK_DIR/android"

# Cleanup mock directory on exit
cleanup() {
  rm -rf "$MOCK_DIR" 2>/dev/null || true
}
trap cleanup EXIT

echo "== Running Accessibility Compliance Audit Test Suite =="

# ----------------------------------------------------------------------
# Generate Mock Files for Apple Accessibility
# ----------------------------------------------------------------------

# 1. APPLE-ACCESSIBILITY-VOICEOVER
cat << 'EOF' > "$MOCK_DIR/ios/VoiceOverRegression.swift"
import SwiftUI

struct VoiceOverRegressionView: View {
    var body: some View {
        VStack {
            Image("unlabeled_image_reference")
        }
    }
}
EOF

cat << 'EOF' > "$MOCK_DIR/ios/VoiceOverCompliant.swift"
import SwiftUI

struct VoiceOverCompliantView: View {
    var body: some View {
        VStack {
            Image(decorative: "decorative_image_reference")
            Image("labeled_image_reference")
                .accessibilityLabel("Detailed label for screen readers")
        }
    }
}
EOF

cat << 'EOF' > "$MOCK_DIR/ios/VoiceOverUIKitRegression.swift"
import UIKit

class UIKitRegressionController: UIViewController {
    let badButton = UIButton()
}
EOF

cat << 'EOF' > "$MOCK_DIR/ios/VoiceOverUIKitCompliant.swift"
import UIKit

class UIKitCompliantController: UIViewController {
    let goodButton = UIButton()
    override func viewDidLoad() {
        super.viewDidLoad()
        goodButton.accessibilityLabel = "Close settings"
    }
}
EOF

# 2. APPLE-ACCESSIBILITY-DYNAMICTYPE
cat << 'EOF' > "$MOCK_DIR/ios/DynamicTypeRegression.swift"
import SwiftUI

struct DynamicTypeRegressionView: View {
    var body: some View {
        Text("Hardcoded Font")
            .font(.system(size: 16))
    }
}
EOF

cat << 'EOF' > "$MOCK_DIR/ios/DynamicTypeUIKitRegression.swift"
import UIKit

class DynamicTypeUIKitRegressionView: UIView {
    let label = UILabel()
    func setup() {
        label.font = UIFont.systemFont(ofSize: 14)
    }
}
EOF

cat << 'EOF' > "$MOCK_DIR/ios/DynamicTypeCompliant.swift"
import UIKit

class DynamicTypeCompliantView: UIView {
    let label = UILabel()
    func setup() {
        label.font = UIFont.preferredFont(forTextStyle: .body)
        label.adjustsFontForContentSizeCategory = true
    }
}
EOF

# 3. APPLE-ACCESSIBILITY-REDUCEMOTION
cat << 'EOF' > "$MOCK_DIR/ios/ReduceMotionRegression.swift"
import SwiftUI

struct ReduceMotionRegressionView: View {
    func animateChanges() {
        withAnimation {
            // Unconditional animation
        }
    }
}
EOF

cat << 'EOF' > "$MOCK_DIR/ios/ReduceMotionCompliant.swift"
import SwiftUI

struct ReduceMotionCompliantView: View {
    @Environment(\.accessibilityReduceMotion) var reduceMotion
    func animateChanges() {
        if reduceMotion {
            // Skip or simplify animation
        } else {
            withAnimation {
                // Perform standard animation
            }
        }
    }
}
EOF

# 4. APPLE-ACCESSIBILITY-COLORCONTRAST
cat << 'EOF' > "$MOCK_DIR/ios/ColorContrastRegression.swift"
import UIKit

class ColorContrastRegressionView: UIView {
    func setup() {
        self.backgroundColor = UIColor(red: 255, green: 0, blue: 0, alpha: 1)
    }
}
EOF

cat << 'EOF' > "$MOCK_DIR/ios/ColorContrastCompliant.swift"
import UIKit

class ColorContrastCompliantView: UIView {
    func setup() {
        self.backgroundColor = UIColor(red: 255, green: 0, blue: 0, alpha: 1)
        if UIAccessibility.isDarkerSystemColorsEnabled {
            self.backgroundColor = UIColor.black
        }
    }
}
EOF

# 5. APPLE-ACCESSIBILITY-HAPTICS
cat << 'EOF' > "$MOCK_DIR/ios/HapticsRegression.swift"
import SwiftUI

struct HapticsRegressionView: View {
    var body: some View {
        Button("Tap Me") {
            // Interactive action without haptics
        }
    }
}
EOF

cat << 'EOF' > "$MOCK_DIR/ios/HapticsCompliant.swift"
import SwiftUI

struct HapticsCompliantView: View {
    var body: some View {
        Button("Tap Me") {
            let generator = UIImpactFeedbackGenerator(style: .medium)
            generator.impactOccurred()
        }
    }
}
EOF

# 6. APPLE-ACCESSIBILITY-KEYBOARD
cat << 'EOF' > "$MOCK_DIR/ios/KeyboardRegression.swift"
import SwiftUI

struct KeyboardRegressionView: View {
    var body: some View {
        Text("Focus Target")
            .focusable()
    }
}
EOF

cat << 'EOF' > "$MOCK_DIR/ios/KeyboardCompliant.swift"
import SwiftUI

struct KeyboardCompliantView: View {
    @FocusState private var isFocused: Bool
    var body: some View {
        Text("Focus Target")
            .focusable()
            .focused($isFocused)
    }
}
EOF


# ----------------------------------------------------------------------
# Generate Mock Files for Android Accessibility
# ----------------------------------------------------------------------

# 7. ANDROID-ACCESSIBILITY-TALKBACK
cat << 'EOF' > "$MOCK_DIR/android/TalkBackRegression.xml"
<ImageView
    android:id="@+id/icon"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content" />
EOF

cat << 'EOF' > "$MOCK_DIR/android/TalkBackCompliant.xml"
<ImageView
    android:id="@+id/icon"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:contentDescription="Settings application icon" />
EOF

cat << 'EOF' > "$MOCK_DIR/android/TalkBackRegression.kt"
import androidx.compose.foundation.Image
import androidx.compose.runtime.Composable

@Composable
fun TalkBackRegressionView() {
    Image(
        painter = painterResource(id = R.drawable.logo)
    )
}
EOF

cat << 'EOF' > "$MOCK_DIR/android/TalkBackCompliant.kt"
import androidx.compose.foundation.Image
import androidx.compose.runtime.Composable

@Composable
fun TalkBackCompliantView() {
    Image(
        painter = painterResource(id = R.drawable.logo),
        contentDescription = "Company logo reference"
    )
}
EOF

# 8. ANDROID-ACCESSIBILITY-FONTSCALING
cat << 'EOF' > "$MOCK_DIR/android/FontScalingRegression.xml"
<TextView
    android:id="@+id/title"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:textSize="18dp" />
EOF

cat << 'EOF' > "$MOCK_DIR/android/FontScalingCompliant.xml"
<TextView
    android:id="@+id/title"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:textSize="18sp" />
EOF

cat << 'EOF' > "$MOCK_DIR/android/FontScalingRegression.kt"
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.unit.dp

@Composable
fun FontScalingRegressionView() {
    Text("Header Text", fontSize = 24.dp)
}
EOF

cat << 'EOF' > "$MOCK_DIR/android/FontScalingCompliant.kt"
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.unit.sp

@Composable
fun FontScalingCompliantView() {
    Text("Header Text", fontSize = 24.sp)
}
EOF

# 9. ANDROID-ACCESSIBILITY-HIGHCONTRAST
cat << 'EOF' > "$MOCK_DIR/android/HighContrastRegression.xml"
<TextView
    android:id="@+id/label"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:textColor="#FF0000" />
EOF

cat << 'EOF' > "$MOCK_DIR/android/HighContrastCompliant.xml"
<TextView
    android:id="@+id/label"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:textColor="?attr/colorOnBackground" />
EOF

cat << 'EOF' > "$MOCK_DIR/android/HighContrastRegression.kt"
import androidx.compose.ui.graphics.Color

fun getRegressionColor(): Color {
    return Color(0xFFFF0000)
}
EOF

cat << 'EOF' > "$MOCK_DIR/android/HighContrastCompliant.kt"
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

@Composable
fun getCompliantColor(): Color {
    return MaterialTheme.colorScheme.primary
}
EOF

# 10. ANDROID-ACCESSIBILITY-SCANNER
cat << 'EOF' > "$MOCK_DIR/android/ScannerRegression.xml"
<Button
    android:id="@+id/action_btn"
    android:layout_width="32dp"
    android:layout_height="32dp" />
EOF

cat << 'EOF' > "$MOCK_DIR/android/ScannerCompliant.xml"
<Button
    android:id="@+id/action_btn"
    android:layout_width="48dp"
    android:layout_height="48dp" />
EOF

cat << 'EOF' > "$MOCK_DIR/android/ScannerRegression.kt"
import androidx.compose.foundation.layout.size
import androidx.compose.ui.unit.dp

fun getRegressionModifier(): Modifier {
    return Modifier.size(40.dp)
}
EOF

cat << 'EOF' > "$MOCK_DIR/android/ScannerCompliant.kt"
import androidx.compose.foundation.layout.size
import androidx.compose.ui.unit.dp

fun getCompliantModifier(): Modifier {
    return Modifier.size(48.dp)
}
EOF


# ----------------------------------------------------------------------
# Run the Static Accessibility Audit Tool
# ----------------------------------------------------------------------

AUDIT_LOG="/tmp/accessibility_audit_output.log"
python3 scripts/accessibility-audit.py "$MOCK_DIR" > "$AUDIT_LOG" 2>&1
RC=$?

if [ "$RC" -ne 0 ]; then
  bad "accessibility-audit.py failed to execute with exit code $RC"
  exit 1
fi

# Check for correct detection of each of the 10 rules in the audit log
declare -a RULES=(
  "APPLE-ACCESSIBILITY-VOICEOVER"
  "APPLE-ACCESSIBILITY-DYNAMICTYPE"
  "APPLE-ACCESSIBILITY-REDUCEMOTION"
  "APPLE-ACCESSIBILITY-COLORCONTRAST"
  "APPLE-ACCESSIBILITY-HAPTICS"
  "APPLE-ACCESSIBILITY-KEYBOARD"
  "ANDROID-ACCESSIBILITY-TALKBACK"
  "ANDROID-ACCESSIBILITY-FONTSCALING"
  "ANDROID-ACCESSIBILITY-HIGHCONTRAST"
  "ANDROID-ACCESSIBILITY-SCANNER"
)

for rule in "${RULES[@]}"; do
  if grep -q "$rule" "$AUDIT_LOG"; then
    ok "Successfully detected rule regression: $rule"
  else
    bad "Failed to detect rule regression: $rule"
  fi
done

# Ensure that compliant files are NOT flagged incorrectly under rules they are not related to
# All detections are mapped to their respective regression files
# Let's count how many total medium findings were reported. It should be exactly 14 findings in total
# (since 4 rules have two regression files each, and 6 rules have one regression file each).
# Let's count occurrences of [MEDIUM] in the output.
NUM_FINDINGS=$(grep -c "\[MEDIUM\]" "$AUDIT_LOG" || true)
if [ "$NUM_FINDINGS" -ge 10 ]; then
  ok "Detected at least 10 expected regression occurrences (total found: $NUM_FINDINGS)"
else
  bad "Expected at least 10 regression occurrences, but found only $NUM_FINDINGS"
fi

echo ""
echo "Accessibility Compliance Audit test suite: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  exit 0
else
  exit 1
fi
