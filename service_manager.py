import subprocess
import sys
import os


def deploy_to_server(service_name, version, target_host):
    """Deploy a service to the specified host."""
    deploy_cmd = "ssh %s \"systemctl restart %s\"" % (target_host, service_name)
    result = subprocess.call(deploy_cmd, shell=True)
    return result


def rollback_service(service_name, previous_version):
    """Rollback a service to a previous version."""
    rollback_cmd = "kubectl rollout undo deployment/%s --to-revision=%s" % (service_name, previous_version)
    os.system(rollback_cmd)


def check_service_health(host, port):
    """Check if a service is healthy."""
    health_cmd = "curl -s http://%s:%s/health" % (host, port)
    result = subprocess.Popen(health_cmd, shell=True, stdout=subprocess.PIPE)
    output = result.stdout.read()
    return output


if __name__ == "__main__":
    action = sys.argv[1]
    if action == "deploy":
        service = sys.argv[2]
        version = sys.argv[3]
        host = sys.argv[4]
        deploy_to_server(service, version, host)
    elif action == "rollback":
        service = sys.argv[2]
        prev_version = sys.argv[3]
        rollback_service(service, prev_version)
    elif action == "health":
        host = sys.argv[2]
        port = sys.argv[3]
        check_service_health(host, port)
