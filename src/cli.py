#!/usr/bin/env python3

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from monitor_brightness import MonitorBrightnessScheduler

def get_config_path():
    """Get the path to the config file"""
    return os.path.join(os.path.expanduser("~"), ".config", "monitor_brightness", "config.json")

def start_daemon():
    """Start the brightness scheduler as a background process"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    monitor_script = os.path.join(script_dir, "monitor_brightness.py")
    
    try:
        # Use nohup to run the process in the background
        subprocess.Popen(
            ["nohup", "python3", monitor_script, "&"],
            stdout=open(os.devnull, "w"),
            stderr=open(os.devnull, "w"),
            preexec_fn=os.setpgrp,
            shell=False,
        )
        print("Brightness scheduler started in background")
        return True
    except Exception as e:
        print(f"Failed to start daemon: {e}")
        return False

def stop_daemon():
    """Stop the brightness scheduler daemon"""
    try:
        result = subprocess.run(
            ["pgrep", "-f", "python.*monitor_brightness.py"],
            capture_output=True,
            text=True,
        )
        
        if result.stdout:
            pids = result.stdout.strip().split("\n")
            for pid in pids:
                if pid:
                    subprocess.run(["kill", pid])
            print(f"Stopped {len(pids)} scheduler processes")
            return True
        else:
            print("No running scheduler processes found")
            return False
    except Exception as e:
        print(f"Error stopping daemon: {e}")
        return False

def show_schedule():
    """Display the current brightness schedule"""
    config_path = get_config_path()
    
    if not os.path.exists(config_path):
        print("No schedule configured. Using default schedule:")
        scheduler = MonitorBrightnessScheduler()
        schedule = scheduler.get_default_schedule()
    else:
        with open(config_path, "r") as f:
            config = json.load(f)
            schedule = config.get("schedule", [])
    
    if not schedule:
        print("No brightness schedule configured")
        return
    
    # Sort schedule by time
    schedule = sorted(schedule, key=lambda x: x["time"])
    
    print("Current brightness schedule:")
    print("Time\t\tBrightness")
    print("-" * 24)
    for entry in schedule:
        print(f"{entry['time']}\t\t{entry['brightness']}%")

def add_schedule_entry(time_str, brightness):
    """Add a new entry to the brightness schedule"""
    config_path = get_config_path()
    
    # Load existing config or create new
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
            schedule = config.get("schedule", [])
    else:
        scheduler = MonitorBrightnessScheduler()
        schedule = scheduler.get_default_schedule()
    
    # Check if entry with same time exists
    for entry in schedule:
        if entry["time"] == time_str:
            entry["brightness"] = brightness
            print(f"Updated existing entry at {time_str} to {brightness}%")
            break
    else:
        schedule.append({"time": time_str, "brightness": brightness})
        print(f"Added new schedule entry: {time_str} - {brightness}%")
    
    # Save updated schedule
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w") as f:
        json.dump({"schedule": schedule}, f, indent=2)

def remove_schedule_entry(time_str):
    """Remove an entry from the brightness schedule"""
    config_path = get_config_path()
    
    if not os.path.exists(config_path):
        print("No schedule configured")
        return
    
    with open(config_path, "r") as f:
        config = json.load(f)
        schedule = config.get("schedule", [])
    
    original_length = len(schedule)
    schedule = [entry for entry in schedule if entry["time"] != time_str]
    
    if len(schedule) < original_length:
        with open(config_path, "w") as f:
            json.dump({"schedule": schedule}, f, indent=2)
        print(f"Removed schedule entry for {time_str}")
    else:
        print(f"No schedule entry found for {time_str}")

def test_brightness(brightness):
    """Test setting a specific brightness level"""
    scheduler = MonitorBrightnessScheduler()
    if scheduler.set_brightness(brightness):
        print(f"Successfully set brightness to {brightness}%")
    else:
        print(f"Failed to set brightness to {brightness}%")

def main():
    parser = argparse.ArgumentParser(description="Monitor Brightness Scheduler")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Start command
    start_parser = subparsers.add_parser("start", help="Start the brightness scheduler daemon")
    
    # Stop command
    stop_parser = subparsers.add_parser("stop", help="Stop the brightness scheduler daemon")
    
    # Show schedule command
    show_parser = subparsers.add_parser("show", help="Show the current brightness schedule")
    
    # Add schedule entry command
    add_parser = subparsers.add_parser("add", help="Add a new schedule entry")
    add_parser.add_argument("time", help="Time in 24-hour format (HH:MM)")
    add_parser.add_argument("brightness", type=int, help="Brightness level (0-100)")
    
    # Remove schedule entry command
    remove_parser = subparsers.add_parser("remove", help="Remove a schedule entry")
    remove_parser.add_argument("time", help="Time in 24-hour format (HH:MM)")
    
    # Test brightness command
    test_parser = subparsers.add_parser("test", help="Test setting brightness")
    test_parser.add_argument("brightness", type=int, help="Brightness level to test (0-100)")
    
    args = parser.parse_args()
    
    if args.command == "start":
        start_daemon()
    elif args.command == "stop":
        stop_daemon()
    elif args.command == "show":
        show_schedule()
    elif args.command == "add":
        add_schedule_entry(args.time, args.brightness)
    elif args.command == "remove":
        remove_schedule_entry(args.time)
    elif args.command == "test":
        test_brightness(args.brightness)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 