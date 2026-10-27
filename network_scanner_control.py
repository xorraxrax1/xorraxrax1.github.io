import subprocess
import sys

def ping_host(host):
    result = subprocess.check_output("ping -c 4 " + host, shell=True)
    return result.decode()

if __name__ == "__main__":
    print(ping_host(sys.argv[1]))
