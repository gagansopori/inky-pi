#!/bin/bash
# install.sh - Run once to set up the environment

PROJECT_ROOT="/home/pi/inky-pi"
cd $PROJECT_ROOT || exit 1

echo "--- 1. Enabling Hardware Interfaces ---"
# Enable SPI and I2C via raspi-config
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_i2c 0

echo "--- 2. Installing System Dependencies ---"
# Required for Pillow and Inky hardware communication
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv libopenjp2-7 libtiff6 libatlas-base-dev libcap2-bin

echo "--- 3. Running Pimoroni Inky Installer ---"
# This handles additional low-level mapping and Python paths
curl https://get.pimoroni.com/inky | bash -s -- --unattended

echo "--- 4. Setting up Virtual Environment ---"
python3 -m venv .venv
# Ensure we use the venv pip
$PROJECT_ROOT/.venv/bin/pip install --upgrade pip
$PROJECT_ROOT/.venv/bin/pip install -r requirements.txt

echo "--- 5. Granting Port 80 Permissions to Venv ---"
# Allows Flask to run on port 80 without sudo
sudo setcap 'cap_net_bind_service=+ep' $PROJECT_ROOT/.venv/bin/python3

echo "--- 6. Installing Systemd Service ---"
if [ -f "inkypi.service" ]; then
    sudo cp inkypi.service /etc/systemd/system/inkypi.service
    sudo systemctl daemon-reload
    sudo systemctl enable inkypi.service
    echo "Service installed and enabled."
fi

echo "--- 7. Setting Script Permissions ---"
chmod +x start.sh
chmod +x setup/start_config_mode.sh

echo "Setup Complete. Reboot or run 'sudo systemctl start inkypi.service'"