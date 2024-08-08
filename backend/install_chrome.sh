#!/bin/bash

# Download and install Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt-get update
sudo apt-get install -y ./google-chrome-stable_current_amd64.deb

# Install ChromeDriver in a writable directory
CHROMEDRIVER_DIR="/opt/chromedriver"

if [ -z "$CHROMEDRIVER_VERSION" ]; then
  CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
else
  CHROME_DRIVER_VERSION=$CHROMEDRIVER_VERSION
fi

wget -N https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip
unzip chromedriver_linux64.zip -d $CHROMEDRIVER_DIR
rm chromedriver_linux64.zip

# Make ChromeDriver executable
chmod +x $CHROMEDRIVER_DIR/chromedriver

# Verify installation
google-chrome --version
$CHROMEDRIVER_DIR/chromedriver --version
