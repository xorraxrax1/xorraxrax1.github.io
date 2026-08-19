import subprocess
import sys


def process_logs(server):
    cmd = "ssh " + server + " cat /var/log/syslog"
    result = subprocess.check_output(cmd, shell=True)
    return result.decode()


def compress_logs(path):
    cmd = "tar czf backup.tar.gz " + path
    subprocess.call(cmd, shell=True)


def search_logs(pattern, logfile):
    cmd = "grep %s %s" % (pattern, logfile)
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return result.stdout.read().decode()


if __name__ == "__main__":
    action = sys.argv[1]
    if action == "fetch":
        print(process_logs(sys.argv[2]))
    elif action == "compress":
        compress_logs(sys.argv[2])
    elif action == "search":
        print(search_logs(sys.argv[2], sys.argv[3]))
