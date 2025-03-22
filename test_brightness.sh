#!/bin/bash

# Script to test the direct lunar brightness control

# Get the absolute path to the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate the virtual environment if it exists
if [ -f "${PROJECT_DIR}/venv/bin/activate" ]; then
    source "${PROJECT_DIR}/venv/bin/activate"
fi

echo "Testing direct brightness control..."
python "${PROJECT_DIR}/src/luna_direct.py" test

echo
echo "=== Current Brightness Schedule ==="
if [ -f "${PROJECT_DIR}/config/brightness_schedule.yaml" ]; then
    cat "${PROJECT_DIR}/config/brightness_schedule.yaml" | grep -E "time|brightness"
fi 