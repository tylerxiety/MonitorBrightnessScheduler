#!/usr/bin/env python3
import time
import json
import os
import sys
import subprocess
import yaml
from datetime import datetime, timedelta
import logging
import signal

# PID file path (same as in monitor_brightness_control.py)
PID_FILE = "scheduler.pid"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scheduler.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("BrightnessScheduler")

class BrightnessScheduler:
    def __init__(self):
        self.config_file = "config/brightness_schedule.yaml"
        self.schedule = []
        self.running = True
        self.setup_signal_handlers()
        self.write_pid()
        self.load_schedule()
        
    def write_pid(self):
        """Write current process PID to file"""
        try:
            with open(PID_FILE, 'w') as f:
                f.write(str(os.getpid()))
            logger.info(f"PID {os.getpid()} written to {PID_FILE}")
        except Exception as e:
            logger.error(f"Failed to write PID file: {e}")
    
    def setup_signal_handlers(self):
        """Set up handlers for signals"""
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def signal_handler(self, sig, frame):
        """Handle signals to gracefully shutdown"""
        logger.info(f"Received signal {sig}, shutting down...")
        self.running = False
        
        # Clean up PID file on exit
        if os.path.exists(PID_FILE):
            try:
                os.remove(PID_FILE)
                logger.info(f"Removed PID file {PID_FILE}")
            except Exception as e:
                logger.error(f"Failed to remove PID file: {e}")
        
        sys.exit(0)
        
    def load_schedule(self):
        """Load brightness schedule from config file"""
        if not os.path.exists(self.config_file):
            logger.error(f"Config file not found: {self.config_file}")
            return
            
        try:
            with open(self.config_file, 'r') as file:
                config = yaml.safe_load(file)
                self.schedule = config.get('schedule', [])
                logger.info(f"Loaded brightness schedule with {len(self.schedule)} entries")
        except Exception as e:
            logger.error(f"Error loading schedule: {e}")
            
    def get_current_brightness(self):
        """Get the brightness level for the current time"""
        if not self.schedule:
            logger.warning("Schedule is empty, using default brightness of 70%")
            return 70
            
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        # Sort schedule by time
        sorted_schedule = sorted(self.schedule, key=lambda x: x['time'])
        
        # Find the schedule entry that applies now
        for i, entry in enumerate(sorted_schedule):
            entry_time = entry['time']
            if current_time < entry_time:
                # If this is the first entry and current time is before it, 
                # use the last entry from previous day
                if i == 0:
                    return sorted_schedule[-1]['brightness']
                # Otherwise use the previous entry
                return sorted_schedule[i-1]['brightness']
                
        # If we've gone through all entries, use the last one
        return sorted_schedule[-1]['brightness']
        
    def set_brightness(self, brightness):
        """Set the monitor brightness using lunar_brightness.py"""
        try:
            # Call the lunar_brightness.py script
            script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lunar_brightness.py")
            result = subprocess.run(
                [sys.executable, script_path, "set", str(brightness)],
                capture_output=True,
                text=True
            )
            
            if "Successfully set brightness" in result.stdout:
                logger.info(f"Successfully set brightness to {brightness}%")
                return True
            else:
                logger.warning(f"Failed to set brightness: {result.stdout}")
                return False
                
        except Exception as e:
            logger.error(f"Error setting brightness: {e}")
            return False
            
    def run(self):
        """Run the scheduler in a loop"""
        logger.info("Starting brightness scheduler")
        
        last_brightness = None
        check_interval = 60  # Check every minute
        fail_count = 0
        max_consecutive_fails = 5
        
        while self.running:
            try:
                current_brightness = self.get_current_brightness()
                
                # Set brightness if it changed or previous attempts failed
                if current_brightness != last_brightness or fail_count > 0:
                    logger.info(f"Setting brightness to {current_brightness}% (previous: {last_brightness})")
                    if self.set_brightness(current_brightness):
                        last_brightness = current_brightness
                        fail_count = 0  # Reset fail counter on success
                    else:
                        fail_count += 1
                        logger.warning(f"Failed to set brightness (attempt {fail_count}/{max_consecutive_fails})")
                        
                        # If we've had too many consecutive failures, we'll wait longer
                        if fail_count >= max_consecutive_fails:
                            logger.error(f"Too many consecutive failures. Monitor may be disconnected. Waiting longer...")
                            time.sleep(check_interval * 5)  # Wait longer between retries
                            fail_count = max_consecutive_fails // 2  # Reduce fail count to try again soon
                        
                # Sleep until next check
                time.sleep(check_interval)
                
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                time.sleep(check_interval)
                
if __name__ == "__main__":
    scheduler = BrightnessScheduler()
    scheduler.run() 