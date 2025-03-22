#!/bin/bash

# Script to display information about connected monitors using Lunar and AppleScript

# Check if Lunar app is installed
if [ ! -d "/Applications/Lunar.app" ]; then
    echo "Error: Lunar app is not installed."
    echo "Please install Lunar from https://lunar.fyi/ or via Homebrew: brew install --cask lunar"
    exit 1
fi

# Get the absolute path to the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate the virtual environment if it exists
if [ -f "${PROJECT_DIR}/venv/bin/activate" ]; then
    source "${PROJECT_DIR}/venv/bin/activate"
fi

# Start Lunar if not running
if ! pgrep -x "Lunar" > /dev/null; then
    echo "Starting Lunar app..."
    open -a Lunar
    sleep 2
fi

echo "=== Connected Monitors ==="
osascript -e 'tell application "Lunar" to get name of every display'

echo 
echo "=== Testing Monitor Info Python Script ==="
python "${PROJECT_DIR}/src/lunar_brightness.py" info

echo
echo "=== Current Schedule ==="
if [ -f "${PROJECT_DIR}/config/brightness_schedule.yaml" ]; then
    cat "${PROJECT_DIR}/config/brightness_schedule.yaml"
else
    echo "No schedule file found."
fi

echo
echo "=== Scheduler Status ==="
python "${PROJECT_DIR}/monitor_brightness_control.py" status 