import subprocess

def run_backup(target):
    return subprocess.check_output("tar czf /backups/" + target + ".tgz /data", shell=True)
