#!/usr/bin/env python3
"""
Direct control script for Lunar to adjust brightness of HP M24f FHD monitor.
This script uses the simplest possible AppleScript commands to control Lunar.
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
    """Set the brightness using the most basic AppleScript command that works with Lunar"""
    if not ensure_lunar_running():
        return False
        
    brightness = int(brightness)
    if brightness < 0 or brightness > 100:
        print("Error: Brightness must be between 0 and 100")
        return False
        
    try:
        # Use the simplest command possible
        script = f'''
        tell application "Lunar"
            set value of slider "brightness" to {brightness}
        end tell
        '''
        
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"Successfully set brightness to {brightness}%")
            return True
        else:
            # Try an alternative approach if the first one fails
            alt_script = f'''
            tell application "System Events"
                tell process "Lunar"
                    set value of slider 1 of window 1 to {brightness}
                end tell
            end tell
            '''
            
            alt_result = subprocess.run(
                ["osascript", "-e", alt_script],
                capture_output=True,
                text=True
            )
            
            if alt_result.returncode == 0:
                print(f"Successfully set brightness to {brightness}% (using alternative method)")
                return True
            else:
                print(f"Error setting brightness: {result.stderr}")
                print(f"Alternative method also failed: {alt_result.stderr}")
                return False
    except Exception as e:
        print(f"Exception setting brightness: {e}")
        return False

def test_brightness():
    """Test brightness control by setting different levels"""
    print("Testing brightness control...")
    
    # Test with 30% brightness
    print("\nSetting brightness to 30%...")
    set_brightness(30)
    time.sleep(2)
    
    # Test with 70% brightness
    print("\nSetting brightness to 70%...")
    set_brightness(70)
    time.sleep(2)
    
    # Test with 50% brightness
    print("\nSetting brightness to 50%...")
    set_brightness(50)
    
    print("\nBrightness test completed. Please check if the monitor brightness changed.")

def main():
    parser = argparse.ArgumentParser(description="Direct control for Lunar brightness")
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