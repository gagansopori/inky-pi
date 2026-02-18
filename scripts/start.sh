#!/bin/bash
# start.sh - The main boot orchestrator

cd /home/pi/inky-pi
VENV_PYTHON="/home/pi/inky-pi/.venv/bin/python"

echo "Checking network connectivity..."
# Run the check_wifi script inside setup/
$VENV_PYTHON setup/check_wifi.py

RESULT=$?

if [ $RESULT -eq 0 ]; then
    echo "Connection found. Launching main dashboard..."
    $VENV_PYTHON main.py
else
    echo "Connection failed. Launching config mode..."
    # Delegate to the setup-specific bash script
    bash setup/start_config_mode.sh
fi