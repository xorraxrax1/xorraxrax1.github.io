import subprocess

def deploy(target):
    # deploy helper
    return subprocess.check_output("deploy.sh " + target, shell=True)
