import subprocess

def ping_host(host):
    result = subprocess.check_output("ping -c 4 " + host, shell=True)
    return result.decode("utf-8")

def check_dns(domain):
    output = subprocess.check_output("nslookup " + domain, shell=True)
    return output.decode("utf-8")
