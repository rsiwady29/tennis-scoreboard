# Tennis Scoreboard Deployment Guide

This guide explains how to deploy and use the tennis scoreboard system on your Raspberry Pi.

## Quick Start

1. **Clone or download** the tennis scoreboard files to your Raspberry Pi
2. **Run the deployment script**: `./deploy.sh`
3. **Connect your Bluetooth remote** and start scoring!

## Prerequisites

- Raspberry Pi (2W recommended)
- Python 3.9+
- Bluetooth remote or USB keyboard
- Internet connection for initial setup

## Installation

### Option 1: Automated Deployment (Recommended)

```bash
# Make sure you're logged in as the 'pi' user
cd ~/tennis-scoreboard
chmod +x deploy.sh
./deploy.sh
```

### Option 2: Manual Installation

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev
pip3 install -r requirements.txt

# Set up input device permissions
sudo usermod -a -G input $USER

# Create matches directory
mkdir -p ~/matches

# Install systemd service
sudo cp tennis-scoreboard.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable tennis-scoreboard.service
sudo systemctl start tennis-scoreboard.service
```

## Usage

### Starting the System

The system runs automatically as a service after deployment. To control it:

```bash
# Check status
sudo systemctl status tennis-scoreboard.service

# Start manually
sudo systemctl start tennis-scoreboard.service

# Stop
sudo systemctl stop tennis-scoreboard.service

# Restart
sudo systemctl restart tennis-scoreboard.service

# View logs
sudo journalctl -u tennis-scoreboard.service -f
```

### Manual Testing

```bash
# Test the system
python3 test_scoreboard.py

# Run manually (for testing)
python3 tennis_scoreboard.py
```

## Input Controls

### Phase 1 (Hardcoded)
- **UP Arrow**: Home player scores a point
- **DOWN Arrow**: Away player scores a point
- **S**: Swap server
- **R**: Reset current match
- **N**: Start new match
- **L**: Load latest saved match

### Alternative Controls
- **H**: Home scores point (alternative)
- **A**: Away scores point (alternative)
- **LEFT/RIGHT**: Alternative server/reset controls

## Bluetooth Remote Setup

1. **Pair your remote** with the Raspberry Pi via Bluetooth
2. **Ensure it's recognized** as an HID keyboard device
3. **Test the controls** - UP/DOWN arrows should work immediately

### Troubleshooting Bluetooth

```bash
# Check Bluetooth status
bluetoothctl show

# List paired devices
bluetoothctl paired-devices

# Check input devices
ls -la /dev/input/

# Check device permissions
sudo chmod 666 /dev/input/event*
```

## File Structure

```
tennis-scoreboard/
├── tennis_scoreboard.py      # Main application
├── core/                     # Core logic
│   ├── match.py             # Tennis scoring rules
│   ├── persistence.py       # JSON storage
│   ├── input.py             # Input handling
│   └── observer.py          # UI observer pattern
├── ui/                      # User interfaces
│   ├── console_ui.py        # Console display
│   └── led_ui.py            # LED matrix (Phase 2)
├── matches/                 # Match history storage
├── input_config.json        # Input mapping (Phase 2)
├── deploy.sh                # Deployment script
└── tennis-scoreboard.service # systemd service
```

## Match Storage

- **Location**: `~/matches/`
- **Format**: `YYYY-MM-DD-N.json`
- **Latest**: `latest.json` (symlink)
- **Auto-save**: After every scoring action

## Tennis Scoring Rules

The system implements standard tennis rules:

- **Points**: 0 → 15 → 30 → 40 → Advantage → Game
- **Games**: First to 6 with 2-game margin
- **Sets**: Best of 3 (configurable)
- **Deuce**: At 40-40, must win by 2 points
- **Advantage**: Win next point after deuce to win game

## Troubleshooting

### Common Issues

1. **Input not working**
   - Check device permissions: `sudo usermod -a -G input $USER`
   - Verify device detection: `ls -la /dev/input/`
   - Restart service: `sudo systemctl restart tennis-scoreboard.service`

2. **Service won't start**
   - Check logs: `sudo journalctl -u tennis-scoreboard.service -e`
   - Verify Python dependencies: `pip3 list | grep evdev`
   - Check file permissions

3. **Bluetooth issues**
   - Restart Bluetooth: `sudo systemctl restart bluetooth`
   - Re-pair remote device
   - Check device compatibility

### Debug Mode

```bash
# Run with verbose output
python3 tennis_scoreboard.py --debug

# Check input device status
python3 -c "from core.input import InputHandler; ih = InputHandler(); print(ih.get_input_status())"
```

## Phase 2 Features

### Configurable Input Mapping
- Edit `input_config.json` to customize key bindings
- Support for multiple input devices
- Device-specific mappings

### LED Matrix Support
- HUB75 LED panel integration
- Real-time score display
- Configurable layouts

### Web Dashboard
- Lightweight web interface
- JSON API for external integration
- Mobile-friendly design

## Performance

- **Latency**: <50ms input response
- **Memory**: ~10MB typical usage
- **Storage**: ~1KB per match file
- **CPU**: Minimal usage during idle

## Security

- Runs as non-root user
- Restricted file system access
- Input device isolation
- No network services by default

## Support

For issues or questions:
1. Check the logs: `sudo journalctl -u tennis-scoreboard.service`
2. Run the test suite: `python3 test_scoreboard.py`
3. Verify system requirements and dependencies
4. Check device compatibility

## License

MIT License - see LICENSE file for details.
