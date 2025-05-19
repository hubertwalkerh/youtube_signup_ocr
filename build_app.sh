#!/bin/bash

APP_NAME="YouTubeSignUpApp"
APP_DIR=~/Desktop/${APP_NAME}.app
EXECUTABLE_NAME=${APP_NAME}

# Thư mục dự án của bạn
PROJECT_DIR="/Users/huytran/Downloads/youtube_signup_ocr"
VENV_ACTIVATE="${PROJECT_DIR}/venv/bin/activate"
SCRIPT_NAME="multi_device_runner.py"

echo "Tạo app ${APP_NAME} tại Desktop..."

# Tạo cấu trúc thư mục .app
mkdir -p "${APP_DIR}/Contents/MacOS"

# Tạo file thực thi trong Contents/MacOS
cat > "${APP_DIR}/Contents/MacOS/${EXECUTABLE_NAME}" <<EOF
#!/bin/bash
cd "${PROJECT_DIR}"
source "${VENV_ACTIVATE}"
python3 "${SCRIPT_NAME}"
EOF

chmod +x "${APP_DIR}/Contents/MacOS/${EXECUTABLE_NAME}"

# Tạo file Info.plist tối giản (bắt buộc để macOS nhận diện .app)
cat > "${APP_DIR}/Contents/Info.plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>${APP_NAME}</string>
    <key>CFBundleExecutable</key>
    <string>${EXECUTABLE_NAME}</string>
    <key>CFBundleIdentifier</key>
    <string>com.yourdomain.${APP_NAME,,}</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
</dict>
</plist>
EOF

echo "Hoàn tất! Bạn đã có app tại: ${APP_DIR}"

