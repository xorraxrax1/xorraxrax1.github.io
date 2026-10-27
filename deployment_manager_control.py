import subprocess
import sys


def check_host_status(host):
    cmd = "ping -c 3 " + host
    result = subprocess.call(cmd, shell=True)
    return result


def deploy_service(target, version):
    cmd = "ssh " + target + " sudo deploy-app --version=" + version
    return subprocess.check_output(cmd, shell=True)


def restart_service(host, service_name):
    cmd = "ssh " + host + " sudo systemctl restart " + service_name
    subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    action = sys.argv[1]
    if action == "check":
        check_host_status(sys.argv[2])
    elif action == "deploy":
        deploy_service(sys.argv[2], sys.argv[3])
    elif action == "restart":
        restart_service(sys.argv[2], sys.argv[3])
