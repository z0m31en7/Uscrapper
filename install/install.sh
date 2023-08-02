#!/bin/bash

# Install required dependencies

pip install requests
pip install beautifulsoup4
pip install termcolor
pip install selenium
pip install webdriver-manager

sudo apt-get update && apt-get install -y firefox

# Make the script executable
chmod +x ../Uscrapper-v2.0.py

echo "Installation complete."
