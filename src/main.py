from kernel import log, username
import kernel
import os
import re
import platform
import functools


def panic(msg, error_type=Exception):
    raise error_type(msg)


def attempt(func=None, retry_on_error=True, panic_code=Exception):
    if func is None:
        return lambda func: attempt(func, retry_on_error=retry_on_error)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            if retry_on_error:
                log(f"Error: {str(e)}")
                return wrapper(*args, **kwargs)
            else:
                panic(f"attempt decorator mode was set to \"retry_on_error=False\"", panic_code)

    return wrapper


class Main:
    def __init__(self):
        print("""
|---------------------------------------------|
|                    NIX                      |
|                                             |
|               Welcome back                  |
|---------------------------------------------|
""")
        self._ARGS = []
        self._USER = username()
        self._COMMAND = None
        self._MAX_PATH = "NIX VHD"
        self.path = None
        self._CURRENT_PATH = os.getcwd().split("\\" if platform.system() == "Windows" else "/")[1:]
        self._TRUE_PATH = os.getcwd().split("\\" if platform.system() == "Windows" else "/")[1:]
        self.sys_interactor()

    @attempt
    def sys_interactor(self, ):
        self._TRUE_PATH = os.getcwd().split("\\" if platform.system() == "Windows" else "/")[1:]
        self._check_path()
        self._COMMAND = input(f"NIX::{os.getcwd()} : ")
        self._ARGS.clear()
        self._CURRENT_PATH = os.getcwd().split("\\" if platform.system() == "Windows" else "/")[1:]
        print(self._CURRENT_PATH)
        for match in re.findall(r'"(.*?)"|(\S+)', self._COMMAND):
            if match[0]:
                self._ARGS.append(match[0])
            elif match[1]:
                self._ARGS.append(match[1])

        match self._ARGS[0]:
            case "exit":
                exit()
            case "cd":
                os.chdir(self._ARGS[1])
            case "gen-app":
                kernel.generate_app(self._ARGS[1], self._ARGS[2], None if self._ARGS[3] is None else self._ARGS[3])
            case _:
                print("ERR: COMMAND NOT FOUND")
                log("Error: Command not found")

        self.sys_interactor()

    @attempt(retry_on_error=False)
    def _check_path(self):
        if self._MAX_PATH not in self._TRUE_PATH:
            self.path = ""
            sep = "\\" if platform.system() == 'Windows' else "/"
            for segment in self._CURRENT_PATH:
                self.path = self.path + segment + sep
            self.path = "C:\\" if platform.system() == 'Windows' else "/" + self.path
            os.chdir(self.path)


Main()

