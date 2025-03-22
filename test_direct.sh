#!/bin/bash

# Script to test the direct control approach for Lunar brightness

# Get the absolute path to the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate the virtual environment if it exists
if [ -f "${PROJECT_DIR}/venv/bin/activate" ]; then
    source "${PROJECT_DIR}/venv/bin/activate"
fi

echo "Testing direct control with UI automation..."
python "${PROJECT_DIR}/src/direct_control.py" test

echo
echo "Testing System Events approach (if needed, grant Accessibility permissions)..."
osascript << EOT
tell application "System Events"
    tell process "Lunar"
        set value of slider 1 of window 1 to 40
    end tell
end tell
EOT

echo "Done. Please verify if brightness changes were applied." 