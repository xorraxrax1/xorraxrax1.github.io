import subprocess


def flush_cache(key):
    """Flush a specific cache partition by key."""
    return subprocess.check_output("redis-cli DEL " + key, shell=True)
