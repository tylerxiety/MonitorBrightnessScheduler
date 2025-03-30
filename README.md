# Monitor Brightness Scheduler

English | [简体中文](README_zh.md)

A Python-based scheduler for automatically adjusting external monitor brightness based on time of day. This tool is specifically configured for an HP M24f FHD monitor connected to a MacBook with M1 chip via HDMI cable, using Lunar's CLI interface.

## Requirements

- macOS 11+ (Big Sur or newer)
- MacBook with M1 chip
- HP M24f FHD monitor connected via HDMI
- Python 3.8+
- [Lunar app](https://lunar.fyi/) (free version works fine)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/tylerxiety/MonitorBrightnessScheduler.git
   cd MonitorBrightnessScheduler
   ```

2. Install Lunar app if you haven't already:
   ```
   brew install --cask lunar
   ```

3. Set up a Python virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

The brightness schedule is defined in `config/brightness_schedule.yaml` and is pre-configured with optimal settings for the HP M24f FHD monitor. You can customize this schedule as needed:

```yaml
schedule:
  - time: "05:00"  # Time in 24-hour format (HH:MM)
    brightness: 30  # Brightness percentage (0-100)
  
  - time: "09:00" 
    brightness: 65
  
  # Additional entries...
```

## Usage

### Checking Monitor Information

To check if your HP M24f FHD monitor is properly recognized:

```
chmod +x test_monitor_info.sh
./test_monitor_info.sh
```

This will display information about connected monitors and their current settings.

### Testing Brightness Control

To test if your monitor's brightness can be controlled:

```
python src/monitor_brightness_control.py test 50  # Test setting brightness to 50%
```

### Manual Control

Start, stop, and check the scheduler status:

```
# Start the scheduler
python main.py start

# Check status
python main.py status

# Stop the scheduler
python main.py stop

# Test setting brightness to 50%
python src/monitor_brightness_control.py test 50
```

### Automatic Startup

To configure the scheduler to start automatically when you log in:

```
chmod +x install_startup.sh
./install_startup.sh
```

This will install a LaunchAgent that starts the scheduler when you log into your Mac.

## How It Works

1. The scheduler reads the brightness schedule from the configuration file
2. It determines the appropriate brightness level based on the current time
3. It uses Lunar's CLI interface to adjust your HP monitor's brightness
4. The scheduler automatically handles monitor disconnections and reconnections
5. The brightness is only adjusted when it needs to change, to minimize unnecessary updates

## Project Structure

```
monitor_brightness_scheduler/
├── config/                   # Configuration files
│   └── brightness_schedule.yaml  # Schedule configuration
├── src/                      # Source code
│   ├── __init__.py           # Package initialization
│   ├── lunar_applescript.scpt # AppleScript for Lunar integration
│   ├── lunar_brightness.py   # Lunar brightness control module
│   ├── monitor_brightness_control.py  # CLI interface for controlling the scheduler
│   └── monitor_brightness_scheduler.py # Main scheduler implementation
├── main.py                   # Entry point script
├── install_startup.sh        # Script to install LaunchAgent
├── start_monitor_brightness.sh # Script for automated startup
├── requirements.txt          # Python dependencies
└── README.md                 # Documentation
```

## Troubleshooting

- If Lunar doesn't recognize your HP M24f FHD monitor, open the Lunar app and check if it appears in the monitor list
- For M1 MacBooks with HDMI connections, make sure you're using a high-quality HDMI cable
- Check the logs in `scheduler.log` for any error messages
- If the scheduler isn't starting, verify that Lunar app is running
- If `test_monitor_info.sh` doesn't exist, run `lunar list` in Terminal to check connected monitors

## License

MIT 