#!/bin/bash

# Script to install the monitor brightness scheduler as a LaunchAgent

# Get the absolute path to the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="$PROJECT_DIR/start_monitor_brightness.sh"

# Set execute permissions on the startup script
chmod +x "$SCRIPT_PATH"

# Create LaunchAgent plist file
PLIST_PATH="$HOME/Library/LaunchAgents/com.user.monitorbrightness.plist"
PLIST_CONTENT="<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">
<plist version=\"1.0\">
<dict>
    <key>Label</key>
    <string>com.user.monitorbrightness</string>
    <key>ProgramArguments</key>
    <array>
        <string>$SCRIPT_PATH</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
    <key>StandardErrorPath</key>
    <string>$PROJECT_DIR/error.log</string>
    <key>StandardOutPath</key>
    <string>$PROJECT_DIR/output.log</string>
</dict>
</plist>"

# Write the plist file
echo "$PLIST_CONTENT" > "$PLIST_PATH"

# Load the LaunchAgent
launchctl load "$PLIST_PATH"

echo "Monitor brightness scheduler has been installed as a LaunchAgent"
echo "It will start automatically when you log in"
echo "To start it immediately, run: launchctl start com.user.monitorbrightness"
echo "To uninstall, run: launchctl unload $PLIST_PATH && rm $PLIST_PATH" 