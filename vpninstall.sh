#!/usr/bin/python
# VPN Install (vpninstall.sh)
#   This script installs and configures the Logmein Hamachi VPN service so that
#   the more technical team members are able to remotely run tests and fix issues
#   when away from the lab.
#
# Konstantin Zaremski
# 05 10 2021

echo "    Installing & Configuring Logmein Hamachi VPN"
cd ~

# Download the package from logmein
echo "  Downloading Hamachi package (curl -O https://www.vpn.net/installers/logmein-hamachi_2.1.0.203-1_armhf.deb)"
curl -O https://www.vpn.net/installers/logmein-hamachi_2.1.0.203-1_armhf.deb

# Install package with dpkg
echo "  Installing Hamachi package (sudo dpkg -i logmein-hamachi_2.1.0.203-1_armhf.deb)"
sudo dpkg -i logmein-hamachi_2.1.0.203-1_armhf.deb

# Enable service
echo "  Enabling Hamachi service"
sudo systemctl enable logmein-hamachi.service
sudo systemctl start logmein-hamachi.service

# Login 
echo "  Configuring Hamachi (Push enter for password)"
sudo hamachi login

sudo hamachi do-join 451-709-606

echo "    Installation and configuration complete."
