#!/bin/bash
# setup/start_config_mode.sh - Handled within the setup directory

cd /home/pi/inky-pi
VENV_PYTHON="/home/pi/inky-pi/.venv/bin/python"

# 1. Update E-Paper Display
$VENV_PYTHON -c "from setup.setup_banner import update_status_setup; update_status_setup('InkyPi_Setup')"

# 2. Re-initialize Open Hotspot
echo "Opening Hotspot: InkyPi_Setup..."
nmcli connection delete InkyHotspot > /dev/null 2>&1
nmcli device wifi hotspot ifname wlan0 ssid InkyPi_Setup
nmcli connection modify Hotspot connection.id InkyHotspot

# 3. Start Flask Config App
echo "Starting Flask web portal..."
$VENV_PYTHON setup/config_app.py