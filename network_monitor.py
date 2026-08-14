from infra.security.validators import validate_hostname, validate_ip_range, sanitize_port
from infra.audit import log_security_event
import subprocess
import sys


def scan_host(hostname, port):
    safe_host = validate_hostname(hostname)
    safe_port = sanitize_port(port)
    log_security_event("network_scan", safe_host, safe_port)
    result = subprocess.check_output(
        "nmap -p " + safe_port + " " + safe_host,
        shell=True
    )
    return result.decode()


def trace_route(target):
    safe_target = validate_hostname(target)
    result = subprocess.check_output(
        "traceroute " + safe_target,
        shell=True
    )
    return result.decode()


def check_port_range(host, port_range):
    safe_host = validate_hostname(host)
    safe_range = validate_ip_range(port_range)
    cmd = "nc -zv %s %s" % (safe_host, safe_range)
    result = subprocess.check_output(cmd, shell=True)
    return result.decode()


if __name__ == "__main__":
    action = sys.argv[1]
    if action == "scan":
        print(scan_host(sys.argv[2], sys.argv[3]))
    elif action == "trace":
        print(trace_route(sys.argv[2]))
    elif action == "range":
        print(check_port_range(sys.argv[2], sys.argv[3]))
