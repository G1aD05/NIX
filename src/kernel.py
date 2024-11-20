import os
import platform
import subprocess
from urllib.request import urlretrieve as get
import getpass
import hashlib
import datetime


def log(message):
    os.chdir(f"{find_base_dir("NIX VHD")}")
    with open("log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()}: {message}\n")
        f.close()


def find_base_dir(base_dir: str):
    parts = os.getcwd().split(os.sep)
    parts.reverse()
    for i, part in enumerate(parts):
        if part == base_dir:
            return os.sep.join(parts[i:][::-1])
    return None


def user_setup():
    hashObject = hashlib.sha256()
    os.chdir(f"{find_base_dir("NIX VHD")}/Users")
    username = input("Username: ")
    os.mkdir(username)
    os.chdir(username)
    password = getpass.getpass("Password: ")
    hashObject.update(password.encode('utf-8'))
    with open(".password") as f:
        f.write(hashObject.hexdigest())
        f.close()


def run_app(name: str):
    os.chdir(f"{find_base_dir("NIX VHD")}/var")
    try:
        with open(f"{name.lower()}.dat", 'r') as f:
            path = f.read()[6:]
            if not platform.system() == "Windows":
                subprocess.run(f"python3 {path}", shell=True)
            else:
                subprocess.run(f"python {path}", shell=True)

    except OSError:
        log(f"Path::NIX VHD/var/{name.lower()}.dat not found; failed to run app")


def login():
    tries = 5
    os.chdir(f"{find_base_dir('NIX VHD')}/Users")

    def getPassword():
        with open(".password") as f:
            password = f.read()
            f.close()
            hashObject.update(getpass.getpass("Password: ").encode('utf-8'))
            if password == hashObject.hexdigest():
                return True
            else:
                if tries < 1:
                    print(f"You have attempted to login too many times.")
                    return
                print("Incorrect password")
                getPassword()

    username = input("Username: ")
    try:
        os.chdir(username)
        getPassword()
    except OSError:
        print(f"User '{username}' does not exist")
        tries -= 1
        login()
    hashObject = hashlib.sha256()


def generate_app(name: str, url: str, dependencies: str = None):
    """
    This function helps you generate apps that are compatible with the kernel

    Separate dependencies by ' '
    :param name:
    :param url:
    :param dependencies:
    :return:
    """
    os.mkdir(f"{name}.nix")
    os.chdir(f"{name}.nix")
    os.mkdir("Contents")
    os.chdir("Contents")
    os.mkdir("src")
    os.chdir("src")
    path = os.getcwd()
    if dependencies is not None:
        if platform.system() == "Darwin":
            subprocess.run("python3 -m pip install --upgrade pip", shell=True)
            subprocess.run(f"python3 -m pip install {dependencies}", shell=True)
        elif platform.system() == "Windows":
            subprocess.run("python -m pip install  --upgrade pip", shell=True)
            subprocess.run(f"python -m pip install {dependencies}", shell=True)
        elif platform.system() == "Linux":
            subprocess.run("pip3 install --upgrade pip", shell=True)
            subprocess.run(f"pip3 install {dependencies}", shell=True)
    get(url, 'exec.py')
    os.chdir(f"{find_base_dir("NIX VHD")}/var")
    with open(f"{name.lower()}.dat", 'w') as f:
        f.write(f"PATH::{path.replace(' ', '\\ ')}/exec.py")


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
        subprocess.run("python3 -m pip install --upgrade pip", shell=True, capture_output=True)
        subprocess.run("python3 -m pip install requests", shell=True, capture_output=True)
    elif platform.system() == "Windows":
        subprocess.run("python -m pip install  --upgrade pip", shell=True, capture_output=True)
        subprocess.run("python -m pip install requests", shell=True, capture_output=True)
    elif platform.system() == "Linux":
        subprocess.run("pip3 install --upgrade pip", shell=True, capture_output=True)
        subprocess.run("pip3 install requests", shell=True, capture_output=True)
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
    os.mkdir("system")
    os.chdir("Applications")

    print("Successfully generated the directories!")
    print("Downloading files...")

    generate_app("Terminal", "https://raw.githubusercontent.com/G1aD05/terminal/refs/heads/main/src/main.py", "ping3 tzlocal psutil pyfiglet colorama pillow")


if __name__ == "__main__":
    if len(os.listdir('.')) == 1:
        log("Kernel has booted into \"setup mode\"")
        setup()
    else:
        log("Kernel has booted into \"normal mode\"")
        run_app("Terminal")
        print("Hi")
