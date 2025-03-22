#!/usr/bin/env python3
import subprocess
import sys
import os
import argparse
import json
import time

class LunarBrightnessController:
    def __init__(self):
        self.lunar_app = "/Applications/Lunar.app"
        # Check if Lunar is installed
        if not os.path.exists(self.lunar_app):
            print("Error: Lunar is not installed in the default location.")
            print("Please install Lunar from https://lunar.fyi/ or via Homebrew: brew install --cask lunar")
            sys.exit(1)
        
        # Ensure Lunar is running
        self._ensure_lunar_running()

    def _ensure_lunar_running(self):
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
        except Exception as e:
            print(f"Error checking/starting Lunar: {e}")

    def _run_applescript(self, script):
        """Run AppleScript and return the result"""
        try:
            proc = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                text=True
            )
            if proc.returncode != 0:
                print(f"AppleScript error: {proc.stderr}")
                return None
            return proc.stdout.strip()
        except Exception as e:
            print(f"Error running AppleScript: {e}")
            return None

    def list_displays(self):
        """List all connected displays using AppleScript"""
        script = '''
        tell application "Lunar"
            set allDisplays to get name of every display
            return allDisplays
        end tell
        '''
        return self._run_applescript(script)

    def get_display_info(self):
        """Get information about connected displays using AppleScript"""
        # First get display names
        names_script = '''
        tell application "Lunar"
            set displayNames to get name of every display
            return displayNames
        end tell
        '''
        display_names = self._run_applescript(names_script)
        if not display_names:
            return None
            
        # Parse the display names - they come as a comma-separated list
        names = [name.strip() for name in display_names.split(",")]
        
        # Create a dictionary of display information
        displays = {}
        for i, name in enumerate(names):
            displays[str(i+1)] = {"name": name, "id": str(i+1)}
            
        return displays

    def set_brightness(self, display_id, brightness_percent):
        """Set brightness for a specific display using AppleScript"""
        brightness = int(brightness_percent)
        if brightness < 0 or brightness > 100:
            print("Error: Brightness must be between 0 and 100")
            return False
        
        # Get display info to find the name
        displays = self.get_display_info()
        if not displays or display_id not in displays:
            print(f"Error: Display ID {display_id} not found")
            return False
            
        display_name = displays[display_id]["name"]
        
        # Set brightness using AppleScript
        script = f'''
        tell application "Lunar"
            set brightness of display "{display_name}" to {brightness}
            return "Success"
        end tell
        '''
        
        result = self._run_applescript(script)
        if result and "Success" in result:
            print(f"Successfully set brightness to {brightness}% for display {display_name}")
            return True
        else:
            print(f"Failed to set brightness for display {display_name}")
            return False

    def set_hp_monitor_brightness(self, brightness_percent):
        """Set brightness specifically for HP monitor"""
        displays = self.get_display_info()
        if not displays:
            return False
            
        hp_monitor = None
        for display_id, display_info in displays.items():
            # Look for an HP monitor in the connected displays, specifically targeting the M24f model
            display_name = display_info.get("name", "")
            if "HP" in display_name:
                # Check if it's specifically the M24f model
                if "M24f" in display_name:
                    hp_monitor = {
                        "id": display_id,
                        "name": display_name
                    }
                    break
                # Otherwise keep the first HP monitor found
                elif not hp_monitor:
                    hp_monitor = {
                        "id": display_id,
                        "name": display_name
                    }
                
        if not hp_monitor:
            print("No HP monitor found among connected displays")
            print("Connected displays:")
            print(self.list_displays())
            return False
            
        print(f"Found HP monitor: {hp_monitor['name']}")
        return self.set_brightness(hp_monitor["id"], brightness_percent)

def main():
    parser = argparse.ArgumentParser(description="Control monitor brightness using Lunar")
    parser.add_argument("command", choices=["list", "set", "info"], 
                        help="Command to execute: list displays, set brightness, or show info")
    parser.add_argument("brightness", nargs="?", type=int, 
                        help="Brightness percentage (0-100) for 'set' command")
    parser.add_argument("--display", "-d", type=str, 
                        help="Display ID (use 'list' to see available displays)")
    
    args = parser.parse_args()
    controller = LunarBrightnessController()
    
    if args.command == "list":
        displays = controller.list_displays()
        print(displays)
    elif args.command == "info":
        displays = controller.get_display_info()
        if displays:
            print(json.dumps(displays, indent=2))
        else:
            print("No display information available")
    elif args.command == "set":
        if args.brightness is None:
            print("Error: Brightness percentage is required for 'set' command")
            parser.print_help()
            sys.exit(1)
            
        if args.display:
            controller.set_brightness(args.display, args.brightness)
        else:
            # If no specific display is specified, try to find and set the HP monitor
            controller.set_hp_monitor_brightness(args.brightness)
    
if __name__ == "__main__":
    main() 