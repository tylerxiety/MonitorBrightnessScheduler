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
        self.lunar_cli = "/Applications/Lunar.app/Contents/MacOS/Lunar"
        # Check if Lunar is installed
        if not os.path.exists(self.lunar_app):
            print("Error: Lunar is not installed in the default location.")
            print("Please install Lunar from https://lunar.fyi/ or via Homebrew: brew install --cask lunar")
            sys.exit(1)
        
        # Ensure Lunar is running
        self._ensure_lunar_running()
        
        # Install CLI if not already installed
        self._ensure_cli_installed()

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
            
    def _ensure_cli_installed(self):
        """Make sure the Lunar CLI is installed"""
        try:
            # Check if lunar command is available in the path
            result = subprocess.run(
                ["which", "lunar"],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                # CLI not installed, install it
                print("Installing Lunar CLI...")
                install_result = subprocess.run(
                    [self.lunar_cli, "install-cli"], 
                    capture_output=True,
                    text=True
                )
                if install_result.returncode != 0:
                    print(f"Error installing Lunar CLI: {install_result.stderr}")
                    print("You may need to run the Lunar app manually and set up the CLI from the app settings.")
                else:
                    print("Lunar CLI installed successfully")
                    # Wait a moment for installation to complete
                    time.sleep(1)
        except Exception as e:
            print(f"Error installing Lunar CLI: {e}")
            print("Please make sure Lunar app is installed and running before using this script.")

    def list_displays(self):
        """List all connected displays using Lunar CLI"""
        try:
            result = subprocess.run(
                ["lunar", "displays"],
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except Exception as e:
            print(f"Error listing displays: {e}")
            return None

    def get_display_info(self):
        """Get information about connected displays using Lunar CLI"""
        try:
            result = subprocess.run(
                ["lunar", "displays", "--json"],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"Error getting display info: {result.stderr}")
                return None
                
            # Parse JSON output
            try:
                displays_data = json.loads(result.stdout)
                displays = {}
                
                # Format the display data for our use
                # The JSON returns an object with serial numbers as keys
                for i, (serial, display) in enumerate(displays_data.items()):
                    display_id = str(i+1)
                    displays[display_id] = {
                        "name": display.get("name", "Unknown Display"),
                        "id": display_id,
                        "serial": serial,
                        "model": display.get("edidName", ""),
                        "brightness": display.get("brightness", 50),
                        "lunar_id": display.get("id", i+1)  # Lunar's internal ID
                    }
                
                return displays
            except json.JSONDecodeError as e:
                print(f"Error parsing display info JSON: {e}")
                print(f"Raw output: {result.stdout[:200]}...")  # Print first 200 chars for debugging
                return None
                
        except Exception as e:
            print(f"Error getting display info: {e}")
            return None

    def set_brightness(self, display_id, brightness_percent):
        """Set brightness for a specific display using Lunar CLI"""
        brightness = int(brightness_percent)
        if brightness < 0 or brightness > 100:
            print("Error: Brightness must be between 0 and 100")
            return False
        
        # Get display info to find the name or serial
        displays = self.get_display_info()
        if not displays or display_id not in displays:
            print(f"Error: Display ID {display_id} not found")
            return False
            
        display_name = displays[display_id]["name"]
        display_serial = displays[display_id]["serial"]
        
        try:
            # Use the lunar CLI to set brightness by serial
            # Note: Lunar CLI needs the serial number, not the display ID
            
            result = subprocess.run(
                ["lunar", "displays", display_serial, "brightness", str(brightness)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"Successfully set brightness to {brightness}% for display {display_name}")
                return True
            else:
                print(f"Failed to set brightness: {result.stderr}")
                # Try fallback method using index
                lunar_id = displays[display_id].get("lunar_id", int(display_id))
                print(f"Trying fallback method with ID: {lunar_id}")
                
                result = subprocess.run(
                    ["lunar", "displays", str(lunar_id-1), "brightness", str(brightness)],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    print(f"Successfully set brightness to {brightness}% using fallback method")
                    return True
                else:
                    print(f"Fallback method also failed: {result.stderr}")
                    return False
                
        except Exception as e:
            print(f"Error setting brightness: {e}")
            return False

    def set_hp_monitor_brightness(self, brightness_percent):
        """Set brightness specifically for HP monitor"""
        displays = self.get_display_info()
        if not displays:
            return False
            
        hp_monitor = None
        for display_id, display_info in displays.items():
            # Look for an HP monitor in the connected displays
            display_name = display_info.get("name", "")
            display_model = display_info.get("model", "")
            
            # Check both name and model fields for "HP"
            if "HP" in display_name or "HP" in display_model:
                # Check if it's specifically the M24f model
                if "M24f" in display_name or "M24f" in display_model:
                    hp_monitor = {
                        "id": display_id,
                        "name": display_name,
                        "model": display_model
                    }
                    break
                # Otherwise keep the first HP monitor found
                elif not hp_monitor:
                    hp_monitor = {
                        "id": display_id,
                        "name": display_name,
                        "model": display_model
                    }
                
        if not hp_monitor:
            print("No HP monitor found among connected displays")
            print("Connected displays:")
            for display_id, display_info in displays.items():
                print(f"  {display_id}: {display_info['name']} ({display_info['model']})")
            return False
            
        print(f"Found HP monitor: {hp_monitor['name']} ({hp_monitor['model']})")
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