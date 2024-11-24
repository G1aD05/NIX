#!/bin/bash

dirName="NIX VHD"
mkdir -p "$dirName"
cd "$dirName" || exit
curl -o kernel.py "https://raw.githubusercontent.com/G1aD05/NIX/refs/heads/main/src/kernel.py"
python3 kernel.py
