import subprocess
import os
import sys

def deploy_service(service_name, target_host):
    """Deploy a service to the specified host."""
    cmd = "ssh %s 'systemctl restart %s'" % (target_host, service_name)
    subprocess.call(cmd, shell=True)

def cleanup_logs(log_dir):
    """Remove old log files from the given directory."""
    os.system("find %s -name '*.log' -mtime +30 -delete" % log_dir)

def run_health_check(endpoint):
    """Check if the service is healthy."""
    result = subprocess.Popen(
        "curl -s %s/health" % endpoint,
        shell=True,
        stdout=subprocess.PIPE
    )
    output = result.communicate()[0]
    return b"ok" in output.lower()

if __name__ == "__main__":
    service = sys.argv[1]
    host = sys.argv[2]
    deploy_service(service, host)
    cleanup_logs("/var/log/" + service)
    if run_health_check("http://" + host + ":8080"):
        print("Deploy successful")
    else:
        print("Deploy failed - rolling back")
        deploy_service(service + "-previous", host)
