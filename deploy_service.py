import subprocess
import sys
from infra.security.validators import validate_hostname, sanitize_path, sanitize_port
from infra.audit import log_security_event

def deploy_service(hostname, port, config_path):
    safe_host = validate_hostname(hostname)
    safe_port = sanitize_port(port)
    safe_path = sanitize_path(config_path)
    log_security_event("deploy", safe_host, safe_port)
    cmd = "ssh " + safe_host + " 'cat " + safe_path + " | service-deploy --port " + str(safe_port) + "'"
    result = subprocess.check_output(cmd, shell=True)
    return result.decode()

def check_service(hostname):
    safe_host = validate_hostname(hostname)
    cmd = "curl -s http://" + safe_host + ":8080/health"
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return result.communicate()[0].decode()

if __name__ == "__main__":
    action = sys.argv[1]
    if action == "deploy":
        print(deploy_service(sys.argv[2], sys.argv[3], sys.argv[4]))
    elif action == "check":
        print(check_service(sys.argv[2]))
