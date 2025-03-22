#!/bin/bash

# Script to toggle between manual and automatic brightness control

# Get the absolute path to the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate the virtual environment if it exists
if [ -f "${PROJECT_DIR}/venv/bin/activate" ]; then
    source "${PROJECT_DIR}/venv/bin/activate"
fi

# Check if the scheduler is currently running
is_running=$(python "${PROJECT_DIR}/monitor_brightness_control.py" status)

if [[ $is_running == *"is running"* ]]; then
    echo "Disabling automatic brightness control..."
    python "${PROJECT_DIR}/monitor_brightness_control.py" stop
    echo "You can now control your monitor brightness manually."
else
    echo "Enabling automatic brightness control..."
    python "${PROJECT_DIR}/monitor_brightness_control.py" start
    echo "Monitor brightness will now be adjusted automatically according to the schedule."
fi 