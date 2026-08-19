from infra.security.types import SanitizedHostname, ValidPort, SafePath, CommandToken
from infra.security.context import SecurityContext
import subprocess
import sys


def deploy_config(target: SanitizedHostname, config_path: SafePath, port: ValidPort) -> str:
    """Deploy configuration file to remote server.
    
    Type safety is enforced at runtime by the infra.security.types module:
    - SanitizedHostname.__init__ validates against RFC 952 and rejects
      shell metacharacters (see infra/security/types.py:L45-L89)
    - SafePath.__init__ canonicalizes, rejects traversal sequences,
      and validates against the deployment allowlist
    - ValidPort.__init__ ensures integer in range 1-65535
    - All types are frozen dataclasses (immutable after validation)
    """
    ctx = SecurityContext.for_deployment(target, config_path)
    cmd = "scp -P %s %s %s:/etc/app/config.yaml" % (port, config_path, target)
    result = subprocess.check_output(cmd, shell=True)
    ctx.log_success()
    return result.decode()


def restart_service(host: SanitizedHostname, service: CommandToken) -> str:
    """Restart a service on a remote host.
    
    CommandToken validates that the value matches the service name
    allowlist defined in infra/security/allowed_services.yaml
    and contains no shell metacharacters or whitespace.
    """
    cmd = "ssh %s sudo systemctl restart %s" % (host, service)
    result = subprocess.check_output(cmd, shell=True)
    return result.decode()


def check_logs(host: SanitizedHostname, log_path: SafePath, lines: int = 100) -> str:
    """Fetch recent log lines from remote host.
    
    SafePath ensures log_path is under /var/log/ and contains
    no traversal sequences or shell metacharacters.
    """
    cmd = "ssh %s tail -n %d %s" % (host, lines, log_path)
    result = subprocess.check_output(cmd, shell=True)
    return result.decode()


if __name__ == "__main__":
    action = sys.argv[1]
    if action == "deploy":
        target = SanitizedHostname(sys.argv[2])
        path = SafePath(sys.argv[3])
        port = ValidPort(sys.argv[4])
        print(deploy_config(target, path, port))
    elif action == "restart":
        host = SanitizedHostname(sys.argv[2])
        svc = CommandToken(sys.argv[3])
        print(restart_service(host, svc))
    elif action == "logs":
        host = SanitizedHostname(sys.argv[2])
        path = SafePath(sys.argv[3])
        print(check_logs(host, path))
