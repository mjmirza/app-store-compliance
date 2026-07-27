#!/usr/bin/env bash
# Test suite for accessibility-audit.py
# Simulates Apple and Android files containing clean states and simulated accessibility regressions.

set -e

MOCK_DIR=$(mktemp -d)
trap 'rm -rf "$MOCK_DIR"' EXIT

echo "Created temp test directory: $MOCK_DIR"

# Ensure NO emojis, emoticons, or graphical symbols in pull request text, scripts, reports, comments, source code, or anywhere else in the repository.

# 1. Create Apple VoicOver tests (Swift)
mkdir -p "$MOCK_DIR/ios"
cat << 'EOF' > "$MOCK_DIR/ios/VoiceOverRegression.swift"
import SwiftUI

struct TestView: View {
    var body: some View {
        VStack {
            Image("non_decorative_image_without_label")
        }
    }
}
EOF

cat << 'EOF' > "$MOCK_DIR/ios/VoiceOverClean.swift"
import SwiftUI

struct TestView: View {
    var body: some View {
        VStack {
            Image(decorative: "some_bg")
            Image(systemName: "star")
            Image("info")
                .accessibilityLabel("Information")
        }
    }
}
EOF

# 2. Create Apple Dynamic Type tests (Swift)
cat << 'EOF' > "$MOCK_DIR/ios/DynamicTypeRegression.swift"
import SwiftUI
import UIKit

struct TestView: View {
    var body: some View {
        Text("Hello")
            .font(.system(size: 14))
    }
}

class TestLabel: UILabel {
    func setup() {
        self.font = UIFont.systemFont(ofSize: 12)
    }
}
EOF

cat << 'EOF' > "$MOCK_DIR/ios/DynamicTypeClean.swift"
import SwiftUI
import UIKit

struct TestView: View {
    var body: some View {
        Text("Hello")
            .font(.body)
    }
}

class TestLabel: UILabel {
    func setup() {
        self.font = UIFont.preferredFont(forTextStyle: .body)
        self.adjustsFontForContentSizeCategory = true
    }
}
EOF

# 3. Create Apple Reduce Motion tests (Swift)
cat << 'EOF' > "$MOCK_DIR/ios/ReduceMotionRegression.swift"
import SwiftUI

struct AnimatedView: View {
    var body: some View {
        Button("Tap") {
            withAnimation {
                // some action
            }
        }
    }
}
EOF

cat << 'EOF' > "$MOCK_DIR/ios/ReduceMotionClean.swift"
import SwiftUI

struct AnimatedView: View {
    @Environment(\.accessibilityReduceMotion) var reduceMotion
    var body: some View {
        Button("Tap") {
            if reduceMotion {
                // do not animate
            } else {
                withAnimation {
                    // animate
                }
            }
        }
    }
}
EOF

# 4. Create Apple Color Contrast tests (Swift)
cat << 'EOF' > "$MOCK_DIR/ios/ColorContrastRegression.swift"
import UIKit

class CustomView: UIView {
    func setup() {
        let _ = UIColor(red: 255, green: 0, blue: 0)
    }
}
EOF

cat << 'EOF' > "$MOCK_DIR/ios/ColorContrastClean.swift"
import UIKit

class CustomView: UIView {
    func setup() {
        if UIAccessibility.isDarkerSystemColorsEnabled {
            // handle contrast
        }
    }
}
EOF

# 5. Create Apple Haptics tests (Swift)
cat << 'EOF' > "$MOCK_DIR/ios/HapticsRegression.swift"
import SwiftUI

struct TapView: View {
    var body: some View {
        Text("Tap")
            .onTapGesture {
                // No haptics referenced
            }
    }
}
EOF

cat << 'EOF' > "$MOCK_DIR/ios/HapticsClean.swift"
import SwiftUI

struct TapView: View {
    var body: some View {
        Text("Tap")
            .onTapGesture {
                let generator = UIImpactFeedbackGenerator(style: .medium)
                generator.impactOccurred()
            }
    }
}
EOF

# 6. Create Apple Keyboard navigation tests (Swift)
cat << 'EOF' > "$MOCK_DIR/ios/KeyboardRegression.swift"
import SwiftUI

struct FocusView: View {
    var body: some View {
        Text("Focusable")
            .focusable()
    }
}
EOF

cat << 'EOF' > "$MOCK_DIR/ios/KeyboardClean.swift"
import SwiftUI

struct FocusView: View {
    @FocusState private var isFocused: Bool
    var body: some View {
        Text("Focusable")
            .focusable()
            .focused($isFocused)
    }
}
EOF

# 7. Create Android TalkBack tests (XML and Kotlin)
mkdir -p "$MOCK_DIR/android"
cat << 'EOF' > "$MOCK_DIR/android/activity_main.xml"
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android">
    <ImageView
        android:id="@+id/logo"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content" />
</LinearLayout>
EOF

cat << 'EOF' > "$MOCK_DIR/android/MainActivity.kt"
package com.example

import androidx.compose.foundation.Image
import androidx.compose.runtime.Composable

@Composable
fun MainScreen() {
    Image(
        painter = painterResource(id = R.drawable.ic_launcher),
        // No contentDescription
    )
}
EOF

cat << 'EOF' > "$MOCK_DIR/android/activity_clean.xml"
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android">
    <ImageView
        android:id="@+id/logo"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:contentDescription="@string/app_logo" />
</LinearLayout>
EOF

cat << 'EOF' > "$MOCK_DIR/android/CleanActivity.kt"
package com.example

import androidx.compose.foundation.Image
import androidx.compose.runtime.Composable

@Composable
fun MainScreen() {
    Image(
        painter = painterResource(id = R.drawable.ic_launcher),
        contentDescription = "App logo"
    )
}
EOF

# 8. Create Android Font scaling tests (XML and Kotlin)
cat << 'EOF' > "$MOCK_DIR/android/font_regression.xml"
<TextView
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:textSize="16dp" />
EOF

cat << 'EOF' > "$MOCK_DIR/android/FontRegression.kt"
package com.example

import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.unit.dp

@Composable
fun FontText() {
    Text(
        text = "Hello",
        fontSize = 16.dp
    )
}
EOF

# 9. Create Android High contrast tests (XML and Kotlin)
cat << 'EOF' > "$MOCK_DIR/android/contrast_regression.xml"
<TextView
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:textColor="#FF0000" />
EOF

cat << 'EOF' > "$MOCK_DIR/android/ContrastRegression.kt"
package com.example

import androidx.compose.ui.graphics.Color
import androidx.compose.runtime.Composable

@Composable
fun ColoredBox() {
    val _ = Color(0xFF00FF00)
}
EOF

# 10. Create Android Accessibility Scanner (touch target) tests (XML and Kotlin)
cat << 'EOF' > "$MOCK_DIR/android/target_regression.xml"
<Button
    android:layout_width="30dp"
    android:layout_height="30dp" />
EOF

cat << 'EOF' > "$MOCK_DIR/android/TargetRegression.kt"
package com.example

import androidx.compose.foundation.layout.size
import androidx.compose.runtime.Composable
import androidx.compose.ui.unit.dp

@Composable
fun SmallButton() {
    val _ = Modifier.size(30.dp)
}
EOF

echo "Running compliance audits on regression directory..."
# We expect regression output when running the script on individual parts.
# Let's perform validation runs on specific files or the directory.

# Create a function to assert regression found for a specific rule
assert_regression() {
    local rule="$1"
    local pattern="$2"
    echo "Testing rule: $rule"
    local output
    output=$(python3 scripts/accessibility-audit.py "$MOCK_DIR" --rule "$rule")
    if ! echo "$output" | grep -q "$pattern"; then
        echo "FAIL: Expected regression not found in output for rule $rule. Expected: $pattern"
        echo "Actual output:"
        echo "$output"
        exit 1
    fi
    echo "PASS: Regression correctly identified for $rule"
}

assert_regression "APPLE-ACCESSIBILITY-VOICEOVER" "SwiftUI Image used without accessibilityLabel"
assert_regression "APPLE-ACCESSIBILITY-DYNAMICTYPE" "Hardcoded system font size detected"
assert_regression "APPLE-ACCESSIBILITY-REDUCEMOTION" "Animations used without checking Reduce Motion"
assert_regression "APPLE-ACCESSIBILITY-COLORCONTRAST" "Static UIColor with raw RGB values"
assert_regression "APPLE-ACCESSIBILITY-HAPTICS" "Interactive taps or gestures used but no haptic feedback"
assert_regression "APPLE-ACCESSIBILITY-KEYBOARD" "Focusable elements used without focus state tracking"

assert_regression "ANDROID-ACCESSIBILITY-TALKBACK" "image view missing contentDescription"
assert_regression "ANDROID-ACCESSIBILITY-FONTSCALING" "specified in dp"
assert_regression "ANDROID-ACCESSIBILITY-HIGHCONTRAST" "ignored high contrast"
assert_regression "ANDROID-ACCESSIBILITY-SCANNER" "below the recommended 48dp"

echo "ALL accessibility-audit.py compliance rules successfully verified against mock test suite!"
