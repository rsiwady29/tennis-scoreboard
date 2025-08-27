#!/bin/bash
# Deployment script for Tennis Scoreboard on Raspberry Pi

set -e

echo "Tennis Scoreboard Deployment Script"
echo "=================================="
echo

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "This script should not be run as root. Please run as pi user."
   exit 1
fi

# Check if we're on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
    echo "Warning: This doesn't appear to be a Raspberry Pi system."
    echo "Some features may not work correctly."
    echo
fi

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev python3-venv

# Install Python packages
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Create matches directory
echo "Creating matches directory..."
mkdir -p ~/matches

# Set up input device permissions
echo "Setting up input device permissions..."
sudo usermod -a -G input $USER

# Create systemd service
echo "Installing systemd service..."
sudo cp tennis-scoreboard.service /etc/systemd/system/
sudo systemctl daemon-reload

# Enable and start service
echo "Enabling and starting service..."
sudo systemctl enable tennis-scoreboard.service
sudo systemctl start tennis-scoreboard.service

# Check service status
echo "Checking service status..."
sudo systemctl status tennis-scoreboard.service --no-pager

echo
echo "Deployment complete!"
echo
echo "The tennis scoreboard service is now running."
echo "To check status: sudo systemctl status tennis-scoreboard.service"
echo "To stop: sudo systemctl stop tennis-scoreboard.service"
echo "To restart: sudo systemctl restart tennis-scoreboard.service"
echo "To view logs: sudo journalctl -u tennis-scoreboard.service -f"
echo
echo "Match files will be saved to: ~/matches/"
echo "Connect your Bluetooth remote and start scoring!"
echo
echo "Note: You may need to log out and back in for input device permissions to take effect."
