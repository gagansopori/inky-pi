#!/bin/bash
# install.sh - Run once to set up the environment

PROJECT_ROOT="/home/pi/inky-pi"
cd $PROJECT_ROOT || exit 1

echo "--- 1. Running Pimoroni Inky Installer ---"
# This enables SPI/I2C and installs system-level dependencies
curl https://get.pimoroni.com/inky | bash -s -- --unattended

echo "--- 2. Setting up Virtual Environment ---"
python3 -m venv .venv
# Ensure we use the venv pip
$PROJECT_ROOT/.venv/bin/pip install --upgrade pip
$PROJECT_ROOT/.venv/bin/pip install -r requirements.txt

echo "--- 3. Granting Port 80 Permissions to Venv ---"
# Allows Flask to run on port 80 without sudo
sudo setcap 'cap_net_bind_service=+ep' $PROJECT_ROOT/.venv/bin/python3

echo "--- 4. Installing Systemd Service ---"
if [ -f "inkypi.service" ]; then
    sudo cp inkypi.service /etc/systemd/system/inkypi.service
    sudo systemctl daemon-reload
    sudo systemctl enable inkypi.service
    echo "Service installed and enabled."
fi

echo "--- 5. Setting Script Permissions ---"
chmod +x start.sh
chmod +x setup/start_config_mode.sh

echo "Setup Complete. Reboot or run 'sudo systemctl start inkypi.service'"