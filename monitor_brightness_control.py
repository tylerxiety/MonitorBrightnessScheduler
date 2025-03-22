#!/usr/bin/env python3
import sys
import os
import subprocess
import time
from datetime import datetime

def print_usage():
    print("Usage:")
    print("  monitor_brightness_control.py start - Start the brightness scheduler")
    print("  monitor_brightness_control.py stop - Stop the brightness scheduler")
    print("  monitor_brightness_control.py status - Check if the scheduler is running")
    print("  monitor_brightness_control.py test <brightness> - Test setting brightness to the specified level (0-100)")

def is_process_running(process_name):
    try:
        # Check if the process is running
        result = subprocess.run(
            ["pgrep", "-f", process_name],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error checking process status: {e}")
        return False

def start_scheduler():
    if is_process_running("python.*monitor_brightness_scheduler.py"):
        print("Scheduler is already running")
        return
    
    # Start the scheduler in the background
    try:
        # Use nohup to keep the process running after terminal closes
        subprocess.Popen(
            ["nohup", "python3", "src/monitor_brightness_scheduler.py", "&"],
            stdout=open("scheduler.log", "a"),
            stderr=subprocess.STDOUT,
            preexec_fn=os.setpgrp
        )
        print("Brightness scheduler started")
    except Exception as e:
        print(f"Error starting scheduler: {e}")

def stop_scheduler():
    try:
        # Find and kill the scheduler process
        subprocess.run(["pkill", "-f", "python.*monitor_brightness_scheduler.py"])
        print("Brightness scheduler stopped")
    except Exception as e:
        print(f"Error stopping scheduler: {e}")

def check_status():
    if is_process_running("python.*monitor_brightness_scheduler.py"):
        print("Brightness scheduler is running")
    else:
        print("Brightness scheduler is not running")

def test_brightness(brightness):
    # Convert brightness to int and validate
    try:
        brightness_level = int(brightness)
        if brightness_level < 0 or brightness_level > 100:
            print("Brightness must be between 0 and 100")
            return
    except ValueError:
        print("Brightness must be a number between 0 and 100")
        return
    
    print(f"Testing brightness control with level: {brightness_level}%")
    
    # Use the new Lunar-based script to control brightness
    try:
        result = subprocess.run(
            ["python3", "src/lunar_brightness.py", "set", str(brightness_level)],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"Error testing brightness control: {e}")

def main():
    if len(sys.argv) < 2:
        print_usage()
        return
    
    command = sys.argv[1].lower()
    
    if command == "start":
        start_scheduler()
    elif command == "stop":
        stop_scheduler()
    elif command == "status":
        check_status()
    elif command == "test":
        if len(sys.argv) < 3:
            print("Please specify a brightness level (0-100)")
            return
        test_brightness(sys.argv[2])
    else:
        print_usage()

if __name__ == "__main__":
    main() 