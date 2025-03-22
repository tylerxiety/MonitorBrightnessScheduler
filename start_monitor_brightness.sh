#!/bin/bash

# Path to the project directory - modify this to match your installation path
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate the virtual environment and start the scheduler
source "${PROJECT_DIR}/venv/bin/activate"
python "${PROJECT_DIR}/monitor_brightness_control.py" start

# Optional: Log start time
echo "Monitor brightness scheduler started at $(date)" >> "${PROJECT_DIR}/scheduler.log" 