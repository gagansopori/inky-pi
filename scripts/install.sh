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
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    python3-numpy \
    python3-pil \
    python3-smbus \
    python3-rpi.gpio \
    python3-spidev \
    libopenjp2-7 \
    libtiff6 \
    libatlas-base-dev \
    libcap2-bin \
    libopenblas-dev \
    libgpiod-dev

#echo "--- 3. Running Pimoroni Inky Installer ---"
## This handles additional low-level mapping and Python paths
#curl https://get.pimoroni.com/inky | bash -s -- --unattended

echo "--- 3. Setting up Virtual Environment ---"
python3 -m venv --system-site-packages .venv

# Ensure we use the venv pip
$PROJECT_ROOT/.venv/bin/pip install --upgrade pip
$PROJECT_ROOT/.venv/bin/pip install -r requirements.txt

echo "--- 4. Granting Port 80 Permissions to Venv ---"
# Allows Flask to run on port 80 without sudo
sudo setcap 'cap_net_bind_service=+ep' $PROJECT_ROOT/.venv/bin/python3

echo "--- 5. Installing Systemd Service ---"
if [ -f "inkypi.service" ]; then
    sudo cp inkypi.service /etc/systemd/system/inkypi.service
    sudo systemctl daemon-reload
    sudo systemctl enable inkypi.service
    echo "Service installed and enabled."
fi

echo "--- 6. Setting Script Permissions ---"
chmod +x scripts/start.sh
chmod +x setup/start_config_mode.sh

echo "--- 7. Marking Installation Complete ---"
touch "$PROJECT_ROOT/.installed"

echo "Setup Complete. Reboot or run 'sudo systemctl start inkypi.service'"