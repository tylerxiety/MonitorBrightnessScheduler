#!/usr/bin/env python3
"""
Direct control of monitor brightness using macOS built-in functions.

This uses the 'brightness' command line tool which is part of some macOS systems.
If not available, it will fail gracefully.
"""

import subprocess
import sys
import os
import time
import argparse

def check_brightness_tool():
    """Check if the brightness tool is available"""
    try:
        result = subprocess.run(
            ["which", "brightness"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception:
        return False

def set_brightness(brightness):
    """Set the brightness using the brightness command"""
    # Convert percentage to decimal (0.0 - 1.0)
    brightness_value = float(brightness) / 100.0
    
    # Make sure it's in valid range
    if brightness_value < 0:
        brightness_value = 0
    elif brightness_value > 1:
        brightness_value = 1
        
    # First try using the brightness command
    try:
        # For external displays, we'll use a different approach with AppleScript
        script = f'''
        tell application "System Events"
            tell process "SystemUIServer"
                try
                    key code 144 -- F15 key (brightness control)
                    delay 0.2
                    
                    -- First set to minimum
                    repeat 16 times
                        key code 145 -- F14 key (decrease brightness)
                        delay 0.05
                    end repeat
                    
                    -- Then increase to desired level
                    repeat {int(brightness_value * 16)} times
                        key code 144 -- F15 key (increase brightness)
                        delay 0.05
                    end repeat
                    
                    return true
                on error
                    return false
                end try
            end tell
        end tell
        '''
        
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and "true" in result.stdout.strip().lower():
            print(f"Successfully set brightness to approximately {brightness}%")
            return True
        else:
            print(f"AppleScript brightness control failed, trying direct approach")
            
            # Try the brightness command if available
            if check_brightness_tool():
                cmd_result = subprocess.run(
                    ["brightness", str(brightness_value)],
                    capture_output=True,
                    text=True
                )
                
                if cmd_result.returncode == 0:
                    print(f"Successfully set brightness to {brightness}% using brightness command")
                    return True
            
            # Try one more approach - using a simple AppleScript that simulates keyboard shortcuts
            simple_script = f'''
            tell application "System Preferences"
                reveal anchor "displaysDisplayTab" of pane "com.apple.preference.displays"
            end tell
            delay 1
            tell application "System Events" to tell process "System Preferences"
                set value of slider 1 of group 1 of tab group 1 of window 1 to {brightness_value}
            end tell
            delay 0.5
            tell application "System Preferences" to quit
            '''
            
            simple_result = subprocess.run(
                ["osascript", "-e", simple_script],
                capture_output=True,
                text=True
            )
            
            if simple_result.returncode == 0:
                print(f"Successfully set brightness to {brightness}% using System Preferences")
                return True
            else:
                print(f"Failed to set brightness using all methods")
                return False
    except Exception as e:
        print(f"Error setting brightness: {e}")
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
    parser = argparse.ArgumentParser(description="Control monitor brightness using macOS functions")
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