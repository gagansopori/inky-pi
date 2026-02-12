#!/bin/bash

# Navigate to the project folder
cd /home/pi/inky-pi/setup

echo "Verifying Python environment..."
# --break-system-packages is necessary on Pi OS Bookworm
# --no-cache-dir saves RAM and SD card wear on the Pi Zero
pip3 install -r requirements.txt --break-system-packages --quiet --no-cache-dir

# Run the network check
echo "Starting network check (60s timeout)..."

# Run the network check
python3 check_wifi.py

# Capture the exit code of the python script
RESULT=$?

if [ $RESULT -eq 0 ]; then
    echo "Network found! Starting Dashboard..."
    # Replace this with your actual project launch command
    python3 main.py
else
    echo "Network NOT found. Entering Config Mode..."
    # 1. Stop normal networking to free the radio
    # 2. Start the Hotspot
    # 3. Start the Flask Config App
    /home/pi/inky-pi/setup/start_config_mode.sh
fi