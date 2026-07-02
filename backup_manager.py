import subprocess
import os

def create_backup(db_name, output_path):
    """Create a database backup."""
    cmd = "pg_dump %s > %s" % (db_name, output_path)
    subprocess.call(cmd, shell=True)

def sync_backup(source, destination):
    """Sync backup to remote storage."""
    os.system("rsync -avz %s %s" % (source, destination))

def verify_backup(backup_file):
    """Verify backup integrity."""
    result = subprocess.Popen(
        "md5sum %s" % backup_file,
        shell=True,
        stdout=subprocess.PIPE
    )
    return result.communicate()[0].decode().strip()

if __name__ == "__main__":
    import sys
    db = sys.argv[1]
    path = sys.argv[2]
    create_backup(db, path)
    sync_backup(path, "backup@storage:/backups/")
    checksum = verify_backup(path)
    print("Backup complete: " + checksum)
