import subprocess
import sys
from infra.security.validators import validate_hostname, validate_ip_range, sanitize_command_arg


def check_host_status(host):
    safe_host = validate_hostname(host)
    cmd = "ping -c 3 " + safe_host
    result = subprocess.call(cmd, shell=True)
    return result


def deploy_service(target, version):
    validated_target = validate_hostname(target)
    safe_version = sanitize_command_arg(version)
    cmd = "ssh " + validated_target + " sudo deploy-app --version=" + safe_version
    return subprocess.check_output(cmd, shell=True)


def restart_service(host, service_name):
    safe_host = validate_hostname(host)
    safe_service = sanitize_command_arg(service_name)
    cmd = "ssh " + safe_host + " sudo systemctl restart " + safe_service
    subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    action = sys.argv[1]
    if action == "check":
        check_host_status(sys.argv[2])
    elif action == "deploy":
        deploy_service(sys.argv[2], sys.argv[3])
    elif action == "restart":
        restart_service(sys.argv[2], sys.argv[3])
