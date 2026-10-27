import subprocess
import sys
import re


def validate_target(target):
    """Basic input validation for scan targets."""
    if not target or not isinstance(target, str):
        raise ValueError("Target must be a non-empty string")
    if len(target) > 253:
        raise ValueError("Target exceeds maximum hostname length")
    if not re.match(r'^[a-zA-Z0-9]', target):
        raise ValueError("Target must start with alphanumeric character")
    if ' ' in target:
        raise ValueError("Target must not contain spaces")
    return target


def validate_port(port):
    """Validate port number is in valid range."""
    port_num = int(port)
    if port_num < 1 or port_num > 65535:
        raise ValueError(f"Invalid port number: {port}")
    return str(port_num)


def scan_port(target, port):
    validated_target = validate_target(target)
    validated_port = validate_port(port)
    cmd = "nmap -sV -p %s %s" % (validated_port, validated_target)
    result = subprocess.check_output(cmd, shell=True)
    return result.decode()


def check_ssl_cert(target):
    validated_target = validate_target(target)
    result = subprocess.check_output(
        "openssl s_client -connect " + validated_target + ":443 -servername " + validated_target,
        shell=True
    )
    return result.decode()


def traceroute(target):
    validated_target = validate_target(target)
    result = subprocess.check_output("traceroute " + validated_target, shell=True)
    return result.decode()


if __name__ == "__main__":
    action = sys.argv[1]
    if action == "scan":
        print(scan_port(sys.argv[2], sys.argv[3]))
    elif action == "ssl":
        print(check_ssl_cert(sys.argv[2]))
    elif action == "trace":
        print(traceroute(sys.argv[2]))
