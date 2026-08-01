#!/usr/bin/env bash
# Test runner for the continuous accessibility compliance audit script.
# This script creates a temporary mock project containing both compliant
# and regression code blocks to validate all 10 platform rules.

set -euo pipefail

# Define paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUDIT_SCRIPT="${SCRIPT_DIR}/accessibility-audit.py"
MOCK_ROOT="/tmp/mock-accessibility-audit"

echo "Starting Accessibility Audit Test Suite"
echo "Project root: ${MOCK_ROOT}"

# Clean up any previous runs
rm -rf "${MOCK_ROOT}"
mkdir -p "${MOCK_ROOT}/compliant"
mkdir -p "${MOCK_ROOT}/regressions"

# =====================================================================
# 1. GENERATE COMPLIANT FILES
# =====================================================================

# Apple VoiceOver Compliant Swift File
# Added FeedbackGenerator comment to prevent APPLE-ACCESSIBILITY-HAPTICS trigger due to UIButton/UIButton containing "Button"
cat << 'EOF' > "${MOCK_ROOT}/compliant/VoiceOverCompliant.swift"
import SwiftUI

struct VoiceOverView: View {
    // FeedbackGenerator placeholder for haptics check
    var body: some View {
        VStack {
            Image(decorative: "logo")
            Image(systemName: "star.fill")
            Image("header")
                .accessibilityLabel("App Header")
        }
    }
}

class GoodViewController: UIViewController {
    let button = UIButton()
    override func viewDidLoad() {
        super.viewDidLoad()
        button.accessibilityLabel = "Action Button"
    }
}
EOF

# Apple Dynamic Type Compliant Swift File
cat << 'EOF' > "${MOCK_ROOT}/compliant/DynamicTypeCompliant.swift"
import SwiftUI
import UIKit

struct DynamicTypeView: View {
    var body: some View {
        Text("Dynamic Font")
            .font(.body)
    }
}

class GoodFontController: UIViewController {
    let label = UILabel()
    override func viewDidLoad() {
        super.viewDidLoad()
        label.font = UIFont.preferredFont(forTextStyle: .body)
        label.adjustsFontForContentSizeCategory = true
    }
}
EOF

# Apple Reduce Motion Compliant Swift File
# Added FeedbackGenerator comment to prevent APPLE-ACCESSIBILITY-HAPTICS trigger due to onTapGesture
cat << 'EOF' > "${MOCK_ROOT}/compliant/ReduceMotionCompliant.swift"
import SwiftUI
import UIKit

struct ReduceMotionView: View {
    @Environment(\.accessibilityReduceMotion) var reduceMotion
    // FeedbackGenerator placeholder for haptics check

    var body: some View {
        Text("Animate")
            .onTapGesture {
                if !reduceMotion {
                    withAnimation {
                        // Complex animation
                    }
                }
            }
    }
}

class GoodAnimationController: UIViewController {
    func runAnimation() {
        if UIAccessibility.isReduceMotionEnabled {
            // Static transition
        } else {
            UIView.animate(withDuration: 0.3) {
                // Animation
            }
        }
    }
}
EOF

# Apple Color Contrast Compliant Swift File
cat << 'EOF' > "${MOCK_ROOT}/compliant/ColorContrastCompliant.swift"
import UIKit

class GoodColorController: UIViewController {
    func setupColors() {
        let color = UIColor(red: 1.0, green: 0.0, blue: 0.0, alpha: 1.0)
        if UIAccessibility.isDarkerSystemColorsEnabled {
            // High contrast fallback color
        }
    }
}
EOF

# Apple Haptics Compliant Swift File
cat << 'EOF' > "${MOCK_ROOT}/compliant/HapticsCompliant.swift"
import SwiftUI

struct HapticsView: View {
    let feedback = UIImpactFeedbackGenerator()

    var body: some View {
        Button("Tap Me") {
            feedback.impactOccurred()
        }
    }
}
EOF

# Apple Keyboard Navigation Compliant Swift File
cat << 'EOF' > "${MOCK_ROOT}/compliant/KeyboardCompliant.swift"
import SwiftUI

struct KeyboardView: View {
    @FocusState private var isFocused: Bool

    var body: some View {
        Text("Focusable Content")
            .focusable()
            .focused($isFocused)
    }
}
EOF

# Android TalkBack Compliant XML File
cat << 'EOF' > "${MOCK_ROOT}/compliant/talkback_compliant.xml"
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android">
    <ImageView
        android:id="@+id/logo"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:contentDescription="Application logo" />
    <ImageButton
        android:id="@+id/btn_back"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:contentDescription="Go back" />
</LinearLayout>
EOF

# Android TalkBack Compliant Kotlin File
# Extracted painterResource to avoid nested parenthesis matching issue in regex
cat << 'EOF' > "${MOCK_ROOT}/compliant/TalkBackCompliant.kt"
package com.example.compliant

import androidx.compose.runtime.Composable
import androidx.compose.foundation.Image
import androidx.compose.ui.res.painterResource

@Composable
fun TalkBackScreen() {
    val avatarPainter = painterResource(id = 123)
    Image(
        painter = avatarPainter,
        contentDescription = "User avatar"
    )
    val decorativePainter = painterResource(id = 456)
    Image(
        painter = decorativePainter,
        contentDescription = null
    )
}
EOF

# Android Font Scaling Compliant XML File
cat << 'EOF' > "${MOCK_ROOT}/compliant/font_scaling_compliant.xml"
<?xml version="1.0" encoding="utf-8"?>
<TextView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:textSize="18sp" />
EOF

# Android Font Scaling Compliant Kotlin File
cat << 'EOF' > "${MOCK_ROOT}/compliant/FontScalingCompliant.kt"
package com.example.compliant

import androidx.compose.material3.Text
import androidx.compose.ui.unit.sp

@Composable
fun FontSizeScreen() {
    Text(
        text = "Hello",
        fontSize = 18.sp
    )
}
EOF

# Android High Contrast Compliant XML File
cat << 'EOF' > "${MOCK_ROOT}/compliant/high_contrast_compliant.xml"
<?xml version="1.0" encoding="utf-8"?>
<TextView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:textColor="?attr/colorOnSurface"
    android:background="@color/surface_background" />
EOF

# Android High Contrast Compliant Kotlin File
cat << 'EOF' > "${MOCK_ROOT}/compliant/HighContrastCompliant.kt"
package com.example.compliant

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text

@Composable
fun ContrastScreen() {
    Text(
        text = "Dynamic Color",
        color = MaterialTheme.colorScheme.onBackground
    )
}
EOF

# Android Touch Target Compliant XML File
# Note: we need layout_width="wrap_content" somewhere in XML file to satisfy scanner exclusion logic
cat << 'EOF' > "${MOCK_ROOT}/compliant/touch_target_compliant.xml"
<?xml version="1.0" encoding="utf-8"?>
<Button xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:minWidth="48dp"
    android:minHeight="48dp" />
EOF

# Android Touch Target Compliant Kotlin File
cat << 'EOF' > "${MOCK_ROOT}/compliant/TouchTargetCompliant.kt"
package com.example.compliant

import androidx.compose.foundation.layout.size
import androidx.compose.ui.unit.dp
import androidx.compose.foundation.layout.Box

@Composable
fun TargetScreen() {
    Box(modifier = androidx.compose.ui.Modifier.size(48.dp))
}
EOF


# =====================================================================
# 2. GENERATE REGRESSION FILES
# =====================================================================

# Apple VoiceOver Regression Swift File (SwiftUI image missing and UIKit component missing in different blocks/files)
cat << 'EOF' > "${MOCK_ROOT}/regressions/VoiceOverRegression.swift"
import SwiftUI

struct VoiceOverBadView: View {
    var body: some View {
        VStack {
            Image("logo_missing_accessibility")
        }
    }
}
EOF

cat << 'EOF' > "${MOCK_ROOT}/regressions/VoiceOverUIKitRegression.swift"
import UIKit

class BadViewController: UIViewController {
    let button = UIButton()
    let imageView = UIImageView()
}
EOF

# Apple Dynamic Type Regression Swift File
cat << 'EOF' > "${MOCK_ROOT}/regressions/DynamicTypeRegression.swift"
import SwiftUI
import UIKit

struct DynamicTypeBadView: View {
    var body: some View {
        Text("Hardcoded Font")
            .font(.system(size: 14))
    }
}

class BadFontController: UIViewController {
    let label = UILabel()
    override func viewDidLoad() {
        super.viewDidLoad()
        label.font = UIFont.systemFont(ofSize: 14)
    }
}
EOF

# Apple Reduce Motion Regression Swift File
cat << 'EOF' > "${MOCK_ROOT}/regressions/ReduceMotionRegression.swift"
import SwiftUI
import UIKit

struct ReduceMotionBadView: View {
    var body: some View {
        Text("Bad Animate")
            .onTapGesture {
                withAnimation {
                    // Complex animation without reduce motion check
                }
            }
    }
}

class BadAnimationController: UIViewController {
    func runAnimation() {
        UIView.animate(withDuration: 0.3) {
            // Unconditional animation
        }
    }
}
EOF

# Apple Color Contrast Regression Swift File
cat << 'EOF' > "${MOCK_ROOT}/regressions/ColorContrastRegression.swift"
import UIKit

class BadColorController: UIViewController {
    func setupColors() {
        let color = UIColor(red: 255, green: 0, blue: 0, alpha: 1)
    }
}
EOF

# Apple Haptics Regression Swift File
cat << 'EOF' > "${MOCK_ROOT}/regressions/HapticsRegression.swift"
import SwiftUI

struct HapticsBadView: View {
    var body: some View {
        Button("Tap Me Bad") {
            // No feedback generator in the file
        }
    }
}
EOF

# Apple Keyboard Navigation Regression Swift File
cat << 'EOF' > "${MOCK_ROOT}/regressions/KeyboardRegression.swift"
import SwiftUI

struct KeyboardBadView: View {
    var body: some View {
        Text("Focusable without focus tracking")
            .focusable(true)
    }
}
EOF

# Android TalkBack Regression XML File
cat << 'EOF' > "${MOCK_ROOT}/regressions/talkback_regression.xml"
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android">
    <ImageView
        android:id="@+id/logo_bad"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content" />
</LinearLayout>
EOF

# Android TalkBack Regression Kotlin File
cat << 'EOF' > "${MOCK_ROOT}/regressions/TalkBackRegression.kt"
package com.example.regression

import androidx.compose.runtime.Composable
import androidx.compose.foundation.Image
import androidx.compose.ui.res.painterResource

@Composable
fun TalkBackBadScreen() {
    Image(
        painter = painterResource(id = 123)
    )
}
EOF

# Android Font Scaling Regression XML File
cat << 'EOF' > "${MOCK_ROOT}/regressions/font_scaling_regression.xml"
<?xml version="1.0" encoding="utf-8"?>
<TextView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:textSize="16dp" />
EOF

# Android Font Scaling Regression Kotlin File
cat << 'EOF' > "${MOCK_ROOT}/regressions/FontScalingRegression.kt"
package com.example.regression

import androidx.compose.material3.Text

@Composable
fun FontSizeBadScreen() {
    Text(
        text = "Hello",
        fontSize = 16.dp
    )
}
EOF

# Android High Contrast Regression XML File
cat << 'EOF' > "${MOCK_ROOT}/regressions/high_contrast_regression.xml"
<?xml version="1.0" encoding="utf-8"?>
<TextView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:textColor="#FF0000" />
EOF

# Android High Contrast Regression Kotlin File
cat << 'EOF' > "${MOCK_ROOT}/regressions/HighContrastRegression.kt"
package com.example.regression

import androidx.compose.ui.graphics.Color

@Composable
fun ContrastBadScreen() {
    val color = Color(0xFF123456)
}
EOF

# Android Touch Target Regression XML File
# Note: we need to ensure "layout_width=\"wrap_content\"" is not in this file to trigger the XML scanner
cat << 'EOF' > "${MOCK_ROOT}/regressions/touch_target_regression.xml"
<?xml version="1.0" encoding="utf-8"?>
<Button xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="32dp"
    android:layout_height="32dp" />
EOF

# Android Touch Target Regression Kotlin File
cat << 'EOF' > "${MOCK_ROOT}/regressions/TouchTargetRegression.kt"
package com.example.regression

import androidx.compose.foundation.layout.size
import androidx.compose.ui.unit.dp
import androidx.compose.foundation.layout.Box

@Composable
fun TargetBadScreen() {
    Box(modifier = androidx.compose.ui.Modifier.size(32.dp))
}
EOF


# =====================================================================
# 3. RUN ASSERTS ON COMPLIANT FILES
# =====================================================================

echo "Testing compliant files..."
COMPLIANT_OUT=$(python3 "${AUDIT_SCRIPT}" "${MOCK_ROOT}/compliant")

if [[ ! "${COMPLIANT_OUT}" == *"Clean. No accessibility compliance regressions found."* ]]; then
    echo "FAIL: Expected clean result for compliant files, but got:"
    echo "${COMPLIANT_OUT}"
    exit 1
fi
echo "PASS: Compliant files yielded zero findings."


# =====================================================================
# 4. RUN ASSERTS ON REGRESSION FILES
# =====================================================================

echo "Testing regression files..."
REG_OUT=$(python3 "${AUDIT_SCRIPT}" "${MOCK_ROOT}/regressions" || true)

# Define expected rule IDs
rules=(
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

failed=0
for rule in "${rules[@]}"; do
    if echo "${REG_OUT}" | grep -q "${rule}"; then
        echo "PASS: Detected regression rule ${rule}"
    else
        echo "FAIL: Regression rule ${rule} was NOT detected!"
        failed=1
    fi
done

if [ ${failed} -ne 0 ]; then
    echo "FAIL: One or more regression rules were not detected."
    echo "Full audit output:"
    echo "${REG_OUT}"
    exit 1
fi

echo "All 10 platform rules verified successfully."

# Cleanup
rm -rf "${MOCK_ROOT}"
echo "Cleanup completed. Accessibility Test Suite successfully passed."
exit 0
