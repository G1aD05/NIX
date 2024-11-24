# Create directory "NIX VHD"
$dirName = "NIX VHD"
New-Item -ItemType Directory -Path $dirName -Force

# Enter the directory
Set-Location -Path $dirName

# Download the file
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/G1aD05/NIX/refs/heads/main/src/kernel.py" -OutFile "kernel.py"

# Run the Python file using Python 3.0
& "python3" "kernel.py"
