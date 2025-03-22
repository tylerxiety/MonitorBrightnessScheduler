#!/bin/bash

# Script to test the OS X brightness control approach

# Get the absolute path to the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate the virtual environment if it exists
if [ -f "${PROJECT_DIR}/venv/bin/activate" ]; then
    source "${PROJECT_DIR}/venv/bin/activate"
fi

echo "Testing OS X brightness control approach..."
echo "This may require accessibility permissions for Terminal..."
sleep 1

python "${PROJECT_DIR}/src/osx_brightness.py" test

echo
echo "Done. Please verify if brightness changes were applied." 