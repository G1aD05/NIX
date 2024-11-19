import os
import platform
import subprocess
from urllib.request import urlretrieve as get


def generate_app(name: str, url: str, cur_dir: str = None):
    os.mkdir(f"{name}.nix")
    os.chdir(f"{name}.nix")
    os.mkdir("Contents")
    os.chdir("Contents")
    os.mkdir("src")
    os.chdir("src")
    get(url, 'exec.py')
    os.chdir("../../../var")
    with open(f"{name.lower}.dat", 'w') as f:
        f.write(f"PATH::/Applications/{name}.nix/Contents/src/exec.py")
        f.close()
    os.chdir("")


def setup():

    print("""
|---------------------------------------------|
|                    NIX                      |
|                                             |
| Welcome to NIX, we will now begin the setup |
|---------------------------------------------|
""")
    print("Downloading dependencies...\n")
    if platform.system() == "Darwin":
        subprocess.run("python3 -m pip install --upgrade pip", shell=True)
        subprocess.run("python3 -m pip install requests", shell=True)
    elif platform.system() == "Windows":
        subprocess.run("python -m pip install  --upgrade pip", shell=True)
        subprocess.run("python -m pip install requests", shell=True)
    elif platform.system() == "Linux":
        subprocess.run("pip3 install --upgrade pip", shell=True)
        subprocess.run("pip3 install requests", shell=True)
    else:
        print("Unsupported operating system")
        return

    print("Dependencies installed!")
    print("Generating Directories...")

    os.mkdir("Users")
    os.mkdir("Applications")
    os.mkdir("pub")
    os.mkdir("tmp")
    os.mkdir("var")
    os.chdir("Applications")

    print("Successfully generated the directories!")
    print("Downloading files...")

    generate_app("Terminal", "https://raw.githubusercontent.com/G1aD05/terminal/refs/heads/main/src/main.py")
    os.chdir("")


if __name__ == "__main__":
    if not os.path.isdir("NIX VHD"):
        setup()
    else:
        pass
