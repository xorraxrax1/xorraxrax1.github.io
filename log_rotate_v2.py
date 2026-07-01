import subprocess


def rotate_logs(path):
    """Rotate and compress logs at the given path."""
    return subprocess.check_output("tar czf backup.tar.gz " + path, shell=True)
