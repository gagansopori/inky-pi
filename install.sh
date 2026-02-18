#!/bin/bash

# =================================================================
# InkyPi System Installer
# Purpose: One-time environment provisioning and hardware setup.
# =================================================================

# Exit immediately if a command exits with a non-zero status
set -e

# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (use sudo)"
  exit 1
fi

# Determine the directory where the script is located to allow for relative paths
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
cd "$PROJECT_ROOT"

echo "--- 1. Enabling Hardware Interfaces ---"
# Enable SPI and I2C via raspi-config (Non-interactive)
raspi-config nonint do_spi 0
raspi-config nonint do_i2c 0

echo "--- 2. Installing System Dependencies ---"
# Install binary headers and system-optimized python libs
apt-get update
apt-get install -y \
    libopenjp2-7 \
    libtiff6 \
    libatlas-base-dev \
    libcap2-bin \
    python3-numpy \
    python3-pil \
    python3-rpi.gpio \
    fontconfig

echo "--- 3. Installing System-Wide Fonts ---"
FONT_DIR="/usr/local/share/fonts/inky-pi"
ASSET_FONTS="./assets/fonts"

mkdir -p "$FONT_DIR"
if [ -d "$ASSET_FONTS" ]; then
    echo "Registering fonts from $ASSET_FONTS..."
    cp "$ASSET_FONTS"/*.ttf "$FONT_DIR/" 2>/dev/null || true
    cp "$ASSET_FONTS"/*.otf "$FONT_DIR/" 2>/dev/null || true
    fc-cache -f -v
else
    echo "Notice: No assets/fonts directory found. Skipping."
fi

echo "--- 4. Setting up Hybrid Virtual Environment ---"
# Create venv with access to system-optimized numpy/PIL
if [ ! -d ".venv" ]; then
    python3 -m venv --system-site-packages .venv
fi
# Use the venv pip for application-specific libraries
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

echo "--- 5. Granting Port 80 Permissions to Venv ---"
# Allows the Flask server to run on port 80 without root privileges
setcap 'cap_net_bind_service=+ep' .venv/bin/python3

echo "--- 6. Installing Systemd Service ---"
if [ -f "inkypi.service" ]; then
    cp inkypi.service /etc/systemd/system/inkypi.service
    systemctl daemon-reload
    systemctl enable inkypi.service
    echo "Service registered and enabled."
fi

echo "--- 7. Setting Script Permissions ---"
chmod +x scripts/start.sh
chmod +x scripts/update.sh

# Create the hidden installation flag
touch .installed

echo ""
echo "-------------------------------------------------------"
echo "System Setup Complete."
echo "Handoff: Running application-level setup (installer.py)"
echo "-------------------------------------------------------"

# Final step: Run the Python-based installer for DB and asset checks
.venv/bin/python3 -m lifecycle.installer