#!/bin/bash

# Install required dependencies

pip install requests
pip install beautifulsoup4
pip install termcolor
pip install selenium
pip install webdriver-manager
pip install stem
pip install tbselenium stem
pip install pyvirtualdisplay

sudo apt-get update && apt-get install -y firefox
sudo apt get install -y tor

# Make the script executable
chmod +x ../Uscrapper-vanta.py

echo "Installation complete."
