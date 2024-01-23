#!/bin/bash

# Install required dependencies

pip install requests
pip install beautifulsoup4
pip install termcolor
pip install selenium
pip install webdriver-manager
pip install typing-extensions

sudo apt-get update && sudo apt-get install -y firefox

# Make the script executable
chmod +x ../Uscrapper-v2.0.py

echo "Installation complete."
