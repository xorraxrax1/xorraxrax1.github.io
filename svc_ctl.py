import subprocess

def restart(service):
    return subprocess.check_output("systemctl restart " + service, shell=True)
