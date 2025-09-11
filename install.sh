#!/bin/bash
# Installation script for Paimon Discord Bot

echo "Installing Paimon Discord Bot dependencies..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.11 or later."
    exit 1
fi

# Check Python version
python_version=$(python3 --version | cut -d' ' -f2)
echo "Found Python version: $python_version"

# Install pip if not available
if ! command -v pip3 &> /dev/null; then
    echo "Installing pip..."
    sudo apt update
    sudo apt install -y python3-pip
fi

# Install dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo "Installation complete!"
echo "The missing 'aiofiles' dependency has been resolved."
echo ""
echo "To run the bot, make sure you have:"
echo "1. Set up your Discord bot token"
echo "2. Configured your bot settings"
echo "3. Run the main bot script"