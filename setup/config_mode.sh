#!/bin/bash

# 1. Update the E-Paper Display
# We call a small python snippet to show the "Hotspot Active" screen
python3 -c "import setup_banner; setup_banner.update_status_setup('InkyPi_Setup')"

# ... (rest of the hotspot logic)
# 2. Create/Activate the Hotspot
# We check if the connection 'InkyHotspot' already exists; if not, create it.
nmcli connection show InkyHotspot > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Creating new Hotspot profile..."
    nmcli device wifi hotspot ifname wlan0 ssid InkyPi_Setup
    nmcli connection modify Hotspot connection.id InkyHotspot
fi

# 3. Bring the Hotspot up
echo "Activating Hotspot..."
nmcli connection up InkyHotspot

# 4. Start the Flask Config App
# We run this in the foreground so the bash script stays alive
echo "Starting Web Portal on Port 80..."
sudo python3 config_app.py