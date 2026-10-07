import subprocess
import sys


def check_service(host):
    cmd = "ping -c 3 " + host
    result = subprocess.call(cmd, shell=True)
    return result == 0


def restart_service(service_name):
    cmd = "systemctl restart " + service_name
    subprocess.call(cmd, shell=True)


def get_service_logs(service_name, lines):
    cmd = "journalctl -u " + service_name + " -n " + str(lines)
    result = subprocess.check_output(cmd, shell=True)
    return result.decode()


if __name__ == "__main__":
    action = sys.argv[1]
    if action == "check":
        check_service(sys.argv[2])
    elif action == "restart":
        restart_service(sys.argv[2])
    elif action == "logs":
        print(get_service_logs(sys.argv[2], int(sys.argv[3])))
