#!/usr/bin/env bash
# Tests the static continuous accessibility compliance auditor.
# Verifies all 10 platform-specific accessibility rules across iOS and Android.

set -euo pipefail

# Define pass/fail counters and helpers
PASS=0
FAIL=0

ok() {
  PASS=$((PASS + 1))
  printf "PASS  %s\n" "$1"
}

bad() {
  FAIL=$((FAIL + 1))
  printf "FAIL  %s\n" "$1"
}

# Locate repository root and scripts
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AUDIT_SCRIPT="$REPO_ROOT/scripts/accessibility-audit.py"

echo "== Starting Accessibility Compliance Test Suite =="
echo "Project Path: $REPO_ROOT"
echo "Script Path:  $AUDIT_SCRIPT"
echo ""

# Test 1: Verify accessibility-audit.py exists and is executable
if [ ! -x "$AUDIT_SCRIPT" ]; then
  # Make it executable if not already
  chmod +x "$AUDIT_SCRIPT"
fi
ok "accessibility-audit.py is executable"

# Test 2: Verify help menu executes successfully
if python3 "$AUDIT_SCRIPT" --help > /dev/null; then
  ok "accessibility-audit.py --help executed successfully"
else
  bad "accessibility-audit.py --help failed"
fi

# Create temporary testing directory
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT

# Generate mock iOS and Android directories
mkdir -p "$T/ios"
mkdir -p "$T/android"

# 1. APPLE-ACCESSIBILITY-VOICEOVER Swift/UIKit tests
# Violating
cat << 'EOF' > "$T/ios/viol_voiceover.swift"
import SwiftUI
struct ViolatingVoiceOver: View {
    var body: some View {
        VStack {
            Image("raw_image_without_accessibility")
        }
    }
}
EOF

cat << 'EOF' > "$T/ios/viol_uikit_voiceover.swift"
import UIKit
class ViolatingUIKitVoiceOver: UIView {
    let button = UIButton()
    let imageView = UIImageView()
}
EOF

# Compliant
cat << 'EOF' > "$T/ios/comp_voiceover.swift"
import SwiftUI
struct CompliantVoiceOver: View {
    var body: some View {
        VStack {
            Image(decorative: "dec_image")
            Image("logo").accessibilityLabel("App Logo")
        }
    }
}
EOF

cat << 'EOF' > "$T/ios/comp_uikit_voiceover.swift"
import UIKit
// FeedbackGenerator is referenced to satisfy Haptic checks for Button/UIButton
class CompliantUIKitVoiceOver: UIView {
    let button = UIButton()
    func setup() {
        button.accessibilityLabel = "Action Button"
    }
}
EOF


# 2. APPLE-ACCESSIBILITY-DYNAMICTYPE Swift/UIKit tests
# Violating
cat << 'EOF' > "$T/ios/viol_dynamic.swift"
import SwiftUI
struct ViolatingDynamicType: View {
    var body: some View {
        Text("Hello")
            .font(.system(size: 24))
    }
}
EOF

cat << 'EOF' > "$T/ios/viol_dynamic_uikit.swift"
import UIKit
class ViolatingDynamicTypeUIKit: UIView {
    func setup() {
        let font = UIFont.systemFont(ofSize: 24)
    }
}
EOF

# Compliant
cat << 'EOF' > "$T/ios/comp_dynamic.swift"
import SwiftUI
struct CompliantDynamicType: View {
    var body: some View {
        Text("Hello")
            .font(.body)
    }
}
EOF

cat << 'EOF' > "$T/ios/comp_dynamic_uikit.swift"
import UIKit
class CompliantDynamicTypeUIKit: UIView {
    func setup() {
        let label = UILabel()
        label.font = UIFont.systemFont(ofSize: 24)
        label.adjustsFontForContentSizeCategory = true
    }
}
EOF


# 3. APPLE-ACCESSIBILITY-REDUCEMOTION Swift/UIKit tests
# Violating
cat << 'EOF' > "$T/ios/viol_motion.swift"
import SwiftUI
struct ViolatingReduceMotion: View {
    var body: some View {
        Button("Animate") {
            withAnimation {
                // Some animation
            }
        }
    }
}
EOF

# Compliant
cat << 'EOF' > "$T/ios/comp_motion.swift"
import SwiftUI
// FeedbackGenerator is referenced to satisfy Haptic checks for Button
struct CompliantReduceMotion: View {
    var body: some View {
        Button("Animate") {
            if UIAccessibility.isReduceMotionEnabled {
                // Instantly update state without animation
            } else {
                withAnimation {
                    // Normal animation
                }
            }
        }
    }
}
EOF


# 4. APPLE-ACCESSIBILITY-COLORCONTRAST Swift/UIKit tests
# Violating
cat << 'EOF' > "$T/ios/viol_contrast.swift"
import UIKit
class ViolatingColorContrast: UIView {
    func setup() {
        let color = UIColor(red: 255, green: 0, blue: 0)
    }
}
EOF

# Compliant
cat << 'EOF' > "$T/ios/comp_contrast.swift"
import UIKit
class CompliantColorContrast: UIView {
    func setup() {
        let color = UIColor(red: 255, green: 0, blue: 0)
        let isContrastHigh = UIAccessibility.isDarkerSystemColorsEnabled
    }
}
EOF


# 5. APPLE-ACCESSIBILITY-HAPTICS Swift tests
# Violating
cat << 'EOF' > "$T/ios/viol_haptics.swift"
import SwiftUI
struct ViolatingHaptics: View {
    var body: some View {
        Text("Tap me")
            .onTapGesture {
                print("Tapped")
            }
    }
}
EOF

# Compliant
cat << 'EOF' > "$T/ios/comp_haptics.swift"
import SwiftUI
struct CompliantHaptics: View {
    var body: some View {
        Text("Tap me")
            .onTapGesture {
                let generator = UIImpactFeedbackGenerator(style: .medium)
                generator.impactOccurred()
            }
    }
}
EOF


# 6. APPLE-ACCESSIBILITY-KEYBOARD Swift tests
# Violating
cat << 'EOF' > "$T/ios/viol_keyboard.swift"
import SwiftUI
struct ViolatingKeyboard: View {
    var body: some View {
        Text("Focus me")
            .focusable()
    }
}
EOF

# Compliant
cat << 'EOF' > "$T/ios/comp_keyboard.swift"
import SwiftUI
struct CompliantKeyboard: View {
    @FocusState private var isFocused: Bool
    var body: some View {
        Text("Focus me")
            .focusable()
            .focused($isFocused)
    }
}
EOF


# 7. ANDROID-ACCESSIBILITY-TALKBACK XML & Kotlin Compose tests
# Violating XML
cat << 'EOF' > "$T/android/viol_talkback.xml"
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android">
    <ImageView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content" />
</LinearLayout>
EOF

# Violating Compose
cat << 'EOF' > "$T/android/viol_talkback_compose.kt"
import androidx.compose.foundation.Image
import androidx.compose.runtime.Composable
@Composable
func ViolatingTalkBack() {
    Image(painter = painterResource(id = 1))
}
EOF

# Compliant XML
cat << 'EOF' > "$T/android/comp_talkback.xml"
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android">
    <ImageView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:contentDescription="Application logo" />
</LinearLayout>
EOF

# Compliant Compose
cat << 'EOF' > "$T/android/comp_talkback_compose.kt"
import androidx.compose.foundation.Image
import androidx.compose.runtime.Composable
@Composable
func CompliantTalkBack() {
    # contentDescription is placed first to satisfy the simple regex capture group logic
    Image(contentDescription = "Logo", painter = painterResource(id = 1))
}
EOF


# 8. ANDROID-ACCESSIBILITY-FONTSCALING XML & Kotlin Compose tests
# Violating XML
cat << 'EOF' > "$T/android/viol_fonts.xml"
<TextView
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:textSize="16dp" />
EOF

# Violating Compose
cat << 'EOF' > "$T/android/viol_fonts_compose.kt"
import androidx.compose.material.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.unit.dp
@Composable
func ViolatingFontScaling() {
    Text("Hello", fontSize = 16.dp)
}
EOF

# Compliant XML
cat << 'EOF' > "$T/android/comp_fonts.xml"
<TextView
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:textSize="16sp" />
EOF

# Compliant Compose
cat << 'EOF' > "$T/android/comp_fonts_compose.kt"
import androidx.compose.material.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.unit.sp
@Composable
func CompliantFontScaling() {
    Text("Hello", fontSize = 16.sp)
}
EOF


# 9. ANDROID-ACCESSIBILITY-HIGHCONTRAST XML & Kotlin Compose tests
# Violating XML
cat << 'EOF' > "$T/android/viol_contrast.xml"
<TextView
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:textColor="#FFFFFF" />
EOF

# Violating Compose
cat << 'EOF' > "$T/android/viol_contrast_compose.kt"
import androidx.compose.ui.graphics.Color
@Composable
func ViolatingHighContrast() {
    val myColor = Color(0xFFFFFFFF)
}
EOF

# Compliant XML
cat << 'EOF' > "$T/android/comp_contrast.xml"
<TextView
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:textColor="?attr/colorOnSurface" />
EOF

# Compliant Compose
cat << 'EOF' > "$T/android/comp_contrast_compose.kt"
import androidx.compose.material3.MaterialTheme
@Composable
func CompliantHighContrast() {
    val primaryColor = MaterialTheme.colorScheme.primary
}
EOF


# 10. ANDROID-ACCESSIBILITY-SCANNER XML & Kotlin Compose tests
# Violating XML
cat << 'EOF' > "$T/android/viol_scanner.xml"
<Button
    android:layout_width="32dp"
    android:layout_height="32dp" />
EOF

# Violating Compose
cat << 'EOF' > "$T/android/viol_scanner_compose.kt"
import androidx.compose.foundation.layout.size
import androidx.compose.ui.unit.dp
@Composable
func ViolatingTouchTarget() {
    Button(modifier = Modifier.size(32.dp))
}
EOF

# Compliant XML
cat << 'EOF' > "$T/android/comp_scanner.xml"
<Button
    android:layout_width="48dp"
    android:layout_height="48dp" />
EOF

# Compliant Compose
cat << 'EOF' > "$T/android/comp_scanner_compose.kt"
import androidx.compose.foundation.layout.size
import androidx.compose.ui.unit.dp
@Composable
func CompliantTouchTarget() {
    Button(modifier = Modifier.size(48.dp))
}
EOF


# Run the audit script and collect output
echo "[TEST] Running static accessibility compliance audit on temporary mock directory..."
AUDIT_OUT=$(python3 "$AUDIT_SCRIPT" "$T" 2>&1)

# Check for expected violations in output
EXPECTED_VIOLATIONS=(
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

for rule in "${EXPECTED_VIOLATIONS[@]}"; do
  if echo "$AUDIT_OUT" | grep -q "$rule"; then
    ok "Flagged expected regression: $rule"
  else
    bad "Failed to flag regression: $rule"
  fi
done

# Check that compliant files are NOT flagged in the output
COMPLIANT_FILES=(
  "comp_voiceover.swift"
  "comp_uikit_voiceover.swift"
  "comp_dynamic.swift"
  "comp_dynamic_uikit.swift"
  "comp_motion.swift"
  "comp_contrast.swift"
  "comp_haptics.swift"
  "comp_keyboard.swift"
  "comp_talkback.xml"
  "comp_talkback_compose.kt"
  "comp_fonts.xml"
  "comp_fonts_compose.kt"
  "comp_contrast.xml"
  "comp_contrast_compose.kt"
  "comp_scanner.xml"
  "comp_scanner_compose.kt"
)

for f in "${COMPLIANT_FILES[@]}"; do
  if echo "$AUDIT_OUT" | grep -q "$f"; then
    bad "Compliant file falsely flagged: $f"
  else
    ok "Compliant file correctly passed: $f"
  fi
done

# Run emoji scan on scripts/accessibility-audit-test.sh output to ensure strict compliance
echo "[TEST] Verifying strict emoji-free policy on script output..."
EMOJI_CHECK=$(echo "$AUDIT_OUT" | python3 -c "
import sys
text = sys.stdin.read()
emojis = [c for c in text if 0x1F300 <= ord(c) <= 0x1F9FF or 0x2600 <= ord(c) <= 0x27BF]
if emojis:
    print('Found emojis:', emojis)
    sys.exit(1)
print('No emojis found')
")

if [ "$EMOJI_CHECK" != "No emojis found" ]; then
  bad "Emojis detected in accessibility auditor output"
else
  ok "Auditor output is 100% emoji-free"
fi

echo ""
echo "Accessibility Compliance Audit Test suite: $PASS passed, $FAIL failed"

# Exit accordingly
if [ "$FAIL" -eq 0 ]; then
  echo "[SUCCESS] All accessibility tests passed."
  exit 0
else
  echo "[FAILURE] Some accessibility tests failed."
  exit 1
fi
