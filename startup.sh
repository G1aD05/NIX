#!/bin/bash

# Create directory "NIX VHD"
dirName="NIX VHD"
mkdir -p "$dirName"

# Enter the directory
cd "$dirName" || exit

# Download the file
curl -o kernel.py "https://raw.githubusercontent.com/G1aD05/NIX/refs/heads/main/src/kernel.py"

# Run the Python file using Python 3.0
python3 kernel.py
