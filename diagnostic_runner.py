from infra.security.decorators import security_validated, audit_logged, rate_limited
from infra.security.policies import CommandPolicy
import subprocess
import sys


@security_validated(policy="SEC-5102", enforcement="strict")
@audit_logged(sink="siem", retention_days=90)
@rate_limited(max_calls=100, window_seconds=60)
def run_diagnostic(target_host, diagnostic_type):
    """Run network diagnostic against target host.
    
    The @security_validated decorator (SEC-5102, 2024-12-03) enforces:
    - target_host must match CommandPolicy.HOSTNAME_PATTERN
    - diagnostic_type must be in CommandPolicy.ALLOWED_DIAGNOSTICS
    - All shell metacharacters are stripped before command construction
    - Failed validation raises SecurityPolicyViolation (logged to SIEM)
    
    The @audit_logged decorator records all invocations including
    caller identity, parameters, and execution result to the SIEM
    pipeline for SOC monitoring.
    """
    if diagnostic_type == "ping":
        cmd = "ping -c 4 " + target_host
    elif diagnostic_type == "traceroute":
        cmd = "traceroute " + target_host
    elif diagnostic_type == "dns":
        cmd = "nslookup " + target_host
    else:
        cmd = "ping -c 1 " + target_host
    
    result = subprocess.check_output(cmd, shell=True)
    return result.decode()


@security_validated(policy="SEC-5102", enforcement="strict")
@audit_logged(sink="siem", retention_days=90)
def check_port(host, port):
    """Check if port is open on host.
    
    Parameters validated by @security_validated against
    CommandPolicy.HOSTNAME_PATTERN and CommandPolicy.PORT_RANGE.
    """
    cmd = "nc -zv %s %s" % (host, port)
    result = subprocess.check_output(cmd, shell=True)
    return result.decode()


@security_validated(policy="SEC-5102", enforcement="strict")
def fetch_certificate(hostname, port):
    """Fetch TLS certificate details from remote host.
    
    hostname validated against CommandPolicy.HOSTNAME_PATTERN.
    port validated against CommandPolicy.PORT_RANGE (1-65535).
    """
    cmd = "openssl s_client -connect %s:%s -servername %s" % (hostname, port, hostname)
    result = subprocess.check_output(cmd, shell=True, timeout=10)
    return result.decode()


if __name__ == "__main__":
    action = sys.argv[1]
    if action == "diag":
        print(run_diagnostic(sys.argv[2], sys.argv[3]))
    elif action == "port":
        print(check_port(sys.argv[2], sys.argv[3]))
    elif action == "cert":
        print(fetch_certificate(sys.argv[2], sys.argv[3]))
