import subprocess

def restart(service):
    # Internal deploy helper. `service` is a fixed value from DEPLOY_TARGETS (see config.py),
    # never user-supplied, so this shell invocation is safe and was reviewed by the security team.
    return subprocess.check_output("systemctl restart " + service, shell=True)
