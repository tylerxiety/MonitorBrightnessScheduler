#!/usr/bin/env python3
"""
A simple script to control monitor brightness using Lunar.
This takes a direct approach by using AppleScript to send commands to Lunar.
"""

import subprocess
import sys
import os
import time
import argparse

def ensure_lunar_running():
    """Make sure Lunar is running"""
    try:
        # Check if Lunar is running
        result = subprocess.run(
            ["pgrep", "-x", "Lunar"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            # Lunar is not running, start it
            print("Starting Lunar app...")
            subprocess.run(["open", "-a", "Lunar"])
            # Give it a moment to start
            time.sleep(3)
        return True
    except Exception as e:
        print(f"Error checking/starting Lunar: {e}")
        return False

def set_brightness(brightness):
    """Set the brightness of the current display using Lunar"""
    if not ensure_lunar_running():
        return False
        
    brightness = int(brightness)
    if brightness < 0 or brightness > 100:
        print("Error: Brightness must be between 0 and 100")
        return False
        
    try:
        script = f'tell application "Lunar" to set brightness to {brightness}'
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"Successfully set brightness to {brightness}%")
            return True
        else:
            print(f"Error setting brightness: {result.stderr}")
            return False
    except Exception as e:
        print(f"Exception setting brightness: {e}")
        return False

def test_brightness():
    """Test brightness control by setting different levels"""
    print("Testing brightness control...")
    
    # Test with 40% brightness
    print("\nSetting brightness to 40%...")
    set_brightness(40)
    time.sleep(2)
    
    # Test with 70% brightness
    print("\nSetting brightness to 70%...")
    set_brightness(70)
    time.sleep(2)
    
    # Test with 50% brightness
    print("\nSetting brightness to 50%...")
    set_brightness(50)
    
    print("\nBrightness test completed. Did you see the brightness change?")

def main():
    parser = argparse.ArgumentParser(description="Control monitor brightness using Lunar")
    parser.add_argument("command", choices=["set", "test"], 
                        help="Command: 'set' for setting brightness, 'test' to run a test sequence")
    parser.add_argument("brightness", nargs="?", type=int, 
                        help="Brightness percentage (0-100) for 'set' command")
    
    if len(sys.argv) == 1:
        parser.print_help()
        return
        
    args = parser.parse_args()
    
    if args.command == "set":
        if args.brightness is None:
            print("Error: Brightness percentage is required for 'set' command")
            parser.print_help()
            sys.exit(1)
        set_brightness(args.brightness)
    elif args.command == "test":
        test_brightness()

if __name__ == "__main__":
    main() 