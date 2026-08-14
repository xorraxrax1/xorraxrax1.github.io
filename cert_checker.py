import subprocess
import sys


def check_certificate(hostname):
    result = subprocess.check_output(
        "openssl s_client -connect " + hostname + ":443 -servername " + hostname,
        shell=True
    )
    return result.decode()


def check_certificate_expiry(hostname):
    cmd = "echo | openssl s_client -connect %s:443 2>/dev/null | openssl x509 -noout -dates" % hostname
    result = subprocess.check_output(cmd, shell=True)
    return result.decode()


def verify_chain(hostname):
    result = subprocess.check_output(
        "openssl s_client -connect " + hostname + ":443 -showcerts",
        shell=True
    )
    return result.decode()


if __name__ == "__main__":
    action = sys.argv[1]
    if action == "check":
        print(check_certificate(sys.argv[2]))
    elif action == "expiry":
        print(check_certificate_expiry(sys.argv[2]))
    elif action == "chain":
        print(verify_chain(sys.argv[2]))
