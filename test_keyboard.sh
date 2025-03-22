#!/bin/bash

# Script to test the keyboard control approach for Lunar brightness

# Get the absolute path to the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate the virtual environment if it exists
if [ -f "${PROJECT_DIR}/venv/bin/activate" ]; then
    source "${PROJECT_DIR}/venv/bin/activate"
fi

echo "Testing keyboard control approach (this requires accessibility permissions)..."
echo "Make sure Lunar is the active application in the foreground..."
sleep 2

python "${PROJECT_DIR}/src/direct_key_control.py" test

echo
echo "Done. Please verify if brightness changes were applied." 