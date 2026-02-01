#!/bin/bash
# Party Pool Setup Script for Linux/macOS
# This script sets up the Party Pool chat application on Linux/macOS

echo ""
echo "===================================================="
echo "  Party Pool - Linux/macOS Setup Script"
echo "===================================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.8+ using your package manager:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip python3-venv"
    echo "  macOS: brew install python3"
    exit 1
fi

echo "[1/3] Python 3 found. Installing dependencies..."
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment."
        exit 1
    fi
fi

# Activate virtual environment and install packages
source venv/bin/activate
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install requirements."
    exit 1
fi

echo ""
echo "[2/3] Dependencies installed successfully!"
echo ""
echo "[3/3] Setup complete!"
echo ""
echo "===================================================="
echo "  Setup Complete!"
echo "===================================================="
echo ""
echo "To start Party Pool, run:"
echo "  python3 main.py"
echo ""
echo "To activate the virtual environment in future sessions:"
echo "  source venv/bin/activate"
echo ""
