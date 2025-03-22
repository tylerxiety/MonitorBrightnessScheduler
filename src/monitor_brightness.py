#!/usr/bin/env python3

import subprocess
import time
import datetime
import os
import signal
import sys
import json
from pathlib import Path

class MonitorBrightnessScheduler:
    def __init__(self, config_path=None):
        self.config_path = config_path or os.path.join(os.path.expanduser("~"), ".config", "monitor_brightness", "config.json")
        self.schedule = []
        self.running = True
        self.load_config()
        self.ensure_monitorcontrol_running()
        
    def load_config(self):
        """Load brightness schedule from config file"""
        try:
            # Make sure config directory exists
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            # Load config if exists, otherwise create default
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    self.schedule = config.get('schedule', self.get_default_schedule())
            else:
                self.schedule = self.get_default_schedule()
                self.save_config()
                
            print(f"Loaded brightness schedule with {len(self.schedule)} entries")
        except Exception as e:
            print(f"Error loading config: {e}")
            self.schedule = self.get_default_schedule()
    
    def save_config(self):
        """Save current schedule to config file"""
        config = {'schedule': self.schedule}
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Config saved to {self.config_path}")
    
    def get_default_schedule(self):
        """Return a default brightness schedule"""
        return [
            {"time": "07:00", "brightness": 70},  # Morning
            {"time": "12:00", "brightness": 80},  # Midday
            {"time": "17:00", "brightness": 70},  # Evening
            {"time": "20:00", "brightness": 50},  # Night
            {"time": "22:00", "brightness": 30}   # Late night
        ]
    
    def ensure_monitorcontrol_running(self):
        """Make sure MonitorControl app is running"""
        try:
            # Check if MonitorControl is running
            result = subprocess.run(
                ["pgrep", "-x", "MonitorControl"],
                capture_output=True,
                text=True
            )
            
            if not result.stdout.strip():
                # Launch MonitorControl if it's not running
                print("Starting MonitorControl app...")
                subprocess.Popen(
                    ["open", "-a", "MonitorControl"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                # Wait for app to fully launch
                time.sleep(5)
        except Exception as e:
            print(f"Error ensuring MonitorControl is running: {e}")
    
    def debug_ui_elements(self):
        """Detailed debug of UI elements"""
        try:
            # This will list all UI elements in the MonitorControl menu
            applescript = '''
            tell application "System Events"
                tell process "MonitorControl"
                    click menu bar item 1 of menu bar 1
                    delay 0.5
                    
                    -- Get detailed info on all UI elements
                    set windowElements to UI elements of window 1
                    set elementDetails to ""
                    
                    repeat with i from 1 to count of windowElements
                        set currentElement to item i of windowElements
                        set elementDetails to elementDetails & "Element " & i & ": " & class of currentElement
                        
                        try
                            set elementDetails to elementDetails & ", Name: " & name of currentElement
                        end try
                        
                        try
                            set elementDetails to elementDetails & ", Description: " & description of currentElement
                        end try
                        
                        -- If it's a group, examine its contents
                        if class of currentElement is group then
                            set groupElements to UI elements of currentElement
                            set elementDetails to elementDetails & ", Contains " & (count of groupElements) & " sub-elements:"
                            
                            repeat with j from 1 to count of groupElements
                                set subElement to item j of groupElements
                                set elementDetails to elementDetails & return & "-- SubElement " & j & ": " & class of subElement
                                
                                try
                                    set elementDetails to elementDetails & ", Name: " & name of subElement
                                end try
                                
                                try
                                    if class of subElement is slider then
                                        set elementDetails to elementDetails & ", Value: " & value of subElement
                                    end if
                                end try
                            end repeat
                        end if
                        
                        set elementDetails to elementDetails & return
                    end repeat
                    
                    -- Close the menu
                    click menu bar item 1 of menu bar 1
                    
                    return elementDetails
                end tell
            end tell
            '''
            
            result = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True, check=False)
            print("UI Element Debug:")
            print(result.stdout)
            return result.stdout
        except Exception as e:
            print(f"Error debugging UI: {e}")
            return ""
    
    def set_brightness_via_monitorcontrol(self, brightness_level):
        """Set the external monitor brightness using MonitorControl menu bar app"""
        try:
            # First debug the UI to understand its structure
            debug_info = self.debug_ui_elements()
            
            # Direct attempt using what we see in the screenshot - looking for HP M24f FHD
            applescript = f'''
            tell application "System Events"
                tell process "MonitorControl"
                    -- Click the menu bar icon
                    click menu bar item 1 of menu bar 1
                    delay 0.5
                    
                    set success to false
                    
                    -- Find all groups in the window
                    set allGroups to groups of window 1
                    
                    -- Look for the group with "HP M24f FHD" text
                    repeat with i from 1 to count of allGroups
                        set currentGroup to item i of allGroups
                        
                        -- Check all static text elements in the group
                        set allTexts to static texts of currentGroup
                        repeat with j from 1 to count of allTexts
                            set currentText to item j of allTexts
                            set textValue to value of currentText
                            
                            -- If this is the HP monitor group
                            if textValue contains "HP M24f FHD" then
                                -- Get all sliders in this group
                                set allSliders to sliders of currentGroup
                                
                                -- The first slider should be the brightness slider
                                if (count of allSliders) > 0 then
                                    set brightnessSlider to item 1 of allSliders
                                    set value of brightnessSlider to {brightness_level / 100.0}
                                    set success to true
                                    exit repeat
                                end if
                            end if
                        end repeat
                        
                        if success then
                            exit repeat
                        end if
                    end repeat
                    
                    -- If we couldn't find the HP text, try just using the first group's first slider
                    if not success and (count of allGroups) > 0 then
                        set firstGroup to item 1 of allGroups
                        set allSliders to sliders of firstGroup
                        
                        if (count of allSliders) > 0 then
                            set brightnessSlider to item 1 of allSliders
                            set value of brightnessSlider to {brightness_level / 100.0}
                            set success to true
                        end if
                    end if
                    
                    -- Close the menu
                    click menu bar item 1 of menu bar 1
                    
                    return success
                end tell
            end tell
            '''
            
            result = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True, check=False)
            success = "true" in result.stdout.strip().lower()
            
            if success:
                print(f"Set HP M24f FHD monitor brightness to {brightness_level}%")
                return True
            else:
                print(f"Failed to find and set HP monitor brightness: {result.stdout}")
                
                # Try a fallback method using simulated manual control
                return self.set_brightness_manually(brightness_level)
                
        except Exception as e:
            print(f"Failed to set HP monitor brightness: {e}")
            return self.set_brightness_manually(brightness_level)
    
    def set_brightness_manually(self, brightness_level):
        """Fallback method to set brightness using clicking and dragging"""
        try:
            # This method will try to manually manipulate the slider by drag actions
            applescript = f'''
            tell application "System Events"
                tell process "MonitorControl"
                    -- Open the menu
                    click menu bar item 1 of menu bar 1
                    delay 0.5
                    
                    -- Get the first group
                    set monitorGroup to group 1 of window 1
                    
                    -- Find the brightness slider (first slider in group)
                    set brightnessSlider to slider 1 of monitorGroup
                    
                    -- Get current position and properties of the slider
                    set sliderPosition to position of brightnessSlider
                    set sliderSize to size of brightnessSlider
                    
                    -- Calculate drag coordinates based on desired brightness
                    set targetX to (item 1 of sliderPosition) + ((item 1 of sliderSize) * {brightness_level / 100.0})
                    set targetY to (item 2 of sliderPosition) + (item 2 of sliderSize) / 2
                    
                    -- Click and drag to set the brightness
                    set currentPosition to position of brightnessSlider
                    set currentX to (item 1 of currentPosition) + ((item 1 of sliderSize) * (value of brightnessSlider))
                    set currentY to (item 2 of currentPosition) + (item 2 of sliderSize) / 2
                    
                    -- Click at current position and drag to target position
                    click at {{currentX, currentY}}
                    drag from {{currentX, currentY}} to {{targetX, currentY}}
                    
                    -- Close the menu
                    click menu bar item 1 of menu bar 1
                    
                    return true
                end tell
            end tell
            '''
            
            result = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True, check=False)
            print(f"Manual brightness control result: {result.stdout}")
            
            print(f"Attempted to manually set HP monitor brightness to {brightness_level}%")
            return "true" in result.stdout.strip().lower()
            
        except Exception as e:
            print(f"Failed to manually set HP monitor brightness: {e}")
            return False

    def set_brightness(self, brightness_level):
        """Set the monitor brightness"""
        # Ensure MonitorControl is running
        self.ensure_monitorcontrol_running()
        
        # Try setting brightness via MonitorControl
        return self.set_brightness_via_monitorcontrol(brightness_level)
    
    def get_current_brightness_setting(self):
        """Get current schedule brightness level based on time"""
        now = datetime.datetime.now().time()
        current_time_str = now.strftime("%H:%M")
        
        # Sort schedule by time
        sorted_schedule = sorted(self.schedule, key=lambda x: x["time"])
        
        # Find the last schedule entry that is before or equal to current time
        for i in range(len(sorted_schedule) - 1, -1, -1):
            if sorted_schedule[i]["time"] <= current_time_str:
                return sorted_schedule[i]["brightness"]
        
        # If current time is before first schedule, use the last entry from previous day
        return sorted_schedule[-1]["brightness"]
    
    def handle_signal(self, signum, frame):
        """Handle termination signals"""
        print("Received termination signal. Exiting...")
        self.running = False
    
    def run(self):
        """Run the brightness scheduler"""
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)
        
        last_brightness = None
        
        try:
            while self.running:
                current_brightness = self.get_current_brightness_setting()
                
                # Only update if brightness has changed
                if current_brightness != last_brightness:
                    self.set_brightness(current_brightness)
                    last_brightness = current_brightness
                
                # Check every minute
                time.sleep(60)
        except Exception as e:
            print(f"Error in scheduler: {e}")
        
        print("Brightness scheduler stopped")

def main():
    scheduler = MonitorBrightnessScheduler()
    scheduler.run()

if __name__ == "__main__":
    main() 