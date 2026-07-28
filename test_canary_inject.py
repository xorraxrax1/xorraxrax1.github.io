import subprocess
import sys
import os

def execute_command(user_input):
    cmd = f"echo {user_input}"
    result = subprocess.call(cmd, shell=True)
    return result

def read_file(filename):
    path = os.path.join("/data", filename)
    with open(path, "r") as f:
        return f.read()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        execute_command(sys.argv[1])
