#!/bin/bash
# Script to build a single-file executable using PyInstaller.
# Usage: ./build.sh

set -e
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "Installing PyInstaller (if missing)..."
python3 -m pip install pyinstaller

echo "Running PyInstaller (onefile) and including DB directory..."
python3 -m PyInstaller --onefile --add-data "DB:DB" --name parcial2 main.py

echo "Build finished. Result: $SCRIPT_DIR/dist/parcial2"
