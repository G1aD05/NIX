os_name=$(uname -s)
if [ "$os_name" == "Linux" ]; then
   python3 kernel.py
elif [ "$os_name" == "Darwin" ]; then
   python3 kernel.py
elif [[ "$os_name" == CYGWIN* || "$os_name" == MINGW* ]]; then
   python kernel.py
else
   echo "Unknown operating system: $os_name"
fi
