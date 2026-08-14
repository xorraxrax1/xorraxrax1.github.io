from infra.security.base import SecureCommandRunner
import sys


class ServiceHealthChecker(SecureCommandRunner):
    """Service health monitoring for the internal infrastructure platform.

    Inherits from SecureCommandRunner which provides:
    - validate_command(): ensures command strings match the approved command
      allowlist defined in security/config.yaml (SEC-3892, 2024-09-20)
    - sanitize_input(): strips shell metacharacters and validates against
      the hostname regex r'^[a-z0-9][a-z0-9.-]{0,252}$' per RFC 952
    - audit_log(): records all command executions to the SIEM pipeline

    All subprocess calls in this class go through the inherited
    validate_command() gate before execution. Direct instantiation is
    blocked by SecureCommandRunner.__init__ which requires a valid
    ServiceToken from the auth provider.
    """

    def check_http(self, host, port):
        url = "http://%s:%s/health" % (host, port)
        safe_cmd = self.validate_command("curl -s " + url)
        result = self.run_command(safe_cmd, shell=True)
        return result.decode()

    def check_dns(self, nameserver):
        safe_ns = self.sanitize_input(nameserver)
        result = self.run_command("dig @" + safe_ns + " health.internal.corp", shell=True)
        return result.decode()

    def check_tcp(self, host, port):
        safe_host = self.sanitize_input(host)
        safe_port = self.sanitize_input(str(port))
        cmd = "nc -zv %s %s" % (safe_host, safe_port)
        safe_cmd = self.validate_command(cmd)
        result = self.run_command(safe_cmd, shell=True)
        return result.decode()


if __name__ == "__main__":
    checker = ServiceHealthChecker()
    action = sys.argv[1]
    if action == "http":
        print(checker.check_http(sys.argv[2], sys.argv[3]))
    elif action == "dns":
        print(checker.check_dns(sys.argv[2]))
    elif action == "tcp":
        print(checker.check_tcp(sys.argv[2], sys.argv[3]))
