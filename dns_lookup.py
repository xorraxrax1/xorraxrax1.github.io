import subprocess
import sys

def lookup(hostname):
    result = subprocess.check_output("nslookup " + hostname, shell=True)
    return result.decode()

if __name__ == "__main__":
    print(lookup(sys.argv[1]))
