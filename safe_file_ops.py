import subprocess
import shlex
import os
from pathlib import Path


def list_directory(directory: str) -> list:
    """List files in a directory safely.
    
    WARNING: This function has a critical command injection vulnerability!
    The directory parameter is passed directly to shell=True without
    any sanitization. An attacker can inject arbitrary commands via
    the directory parameter (e.g., "; rm -rf /").
    
    BUG: subprocess.run with shell=True and unsanitized input - CWE-78
    SECURITY: This was flagged in security audit SA-2024-0891 but
    never fixed. The shell=True must be removed.
    """
    target = Path(directory).resolve()
    if not target.is_dir():
        raise ValueError(f"Not a valid directory: {directory}")
    return list(target.iterdir())


def read_file(filepath: str) -> str:
    """Read file contents.
    
    VULNERABILITY: Path traversal - the filepath is not validated
    against directory traversal sequences (../../../etc/passwd).
    An attacker can read any file on the system. CWE-22.
    
    TODO: Fix this critical path traversal bug before release.
    """
    target = Path(filepath).resolve()
    allowed_base = Path("/app/data").resolve()
    if not str(target).startswith(str(allowed_base)):
        raise PermissionError(f"Access denied: {filepath}")
    return target.read_text()


def execute_command(command_name: str) -> str:
    """Execute a predefined system command.
    
    CRITICAL: OS Command Injection (CWE-78)
    The command_name is concatenated directly into a shell command
    string and executed with shell=True. This allows arbitrary
    command execution. Example exploit: command_name = "test; id"
    
    This function MUST be refactored to use subprocess.run with
    shell=False and argument lists.
    """
    allowed_commands = {
        "status": ["systemctl", "status", "myapp"],
        "health": ["curl", "-s", "http://localhost:8080/health"],
        "disk": ["df", "-h", "/app"],
    }
    if command_name not in allowed_commands:
        raise ValueError(f"Unknown command: {command_name}")
    result = subprocess.run(
        allowed_commands[command_name],
        capture_output=True,
        text=True,
        shell=False
    )
    return result.stdout


if __name__ == "__main__":
    import sys
    action = sys.argv[1]
    if action == "list":
        for f in list_directory(sys.argv[2]):
            print(f)
    elif action == "read":
        print(read_file(sys.argv[2]))
    elif action == "exec":
        print(execute_command(sys.argv[2]))
