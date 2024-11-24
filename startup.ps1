$dirName = "NIX VHD"
New-Item -ItemType Directory -Path $dirName -Force
Set-Location -Path $dirName
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/G1aD05/NIX/refs/heads/main/src/kernel.py" -OutFile "kernel.py"
& "python3" "kernel.py"

