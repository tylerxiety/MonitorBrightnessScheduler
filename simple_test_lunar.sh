#!/bin/bash

# A simple script to test Lunar AppleScript control

# Start Lunar if not running
if ! pgrep -x "Lunar" > /dev/null; then
    echo "Starting Lunar app..."
    open -a Lunar
    sleep 2
fi

echo "Testing simple AppleScript commands with Lunar"

echo "1. Getting display list:"
osascript -e 'tell application "Lunar" to return display'

echo "2. Getting current brightness:"
osascript -e 'tell application "Lunar" to return brightness'

echo "3. Setting brightness to 60%:"
osascript -e 'tell application "Lunar" to set brightness to 60'
echo "Done. Please check if the monitor brightness changed."

echo "4. Setting brightness to 80%:"
osascript -e 'tell application "Lunar" to set brightness to 80'
echo "Done. Please check if the monitor brightness changed."

echo "5. Getting all monitor names:"
osascript << EOT
tell application "Lunar"
    try
        -- Try to get all display names
        set displayNames to get name of displays
        return displayNames
    on error errMsg
        return "Error: " & errMsg
    end try
end tell
EOT

echo "Test completed. Please verify if brightness changes were applied." 