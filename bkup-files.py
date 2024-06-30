import os
import paramiko

def backup_files(local_dir, remote_dir, server, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, username=username, password=password)
    sftp = ssh.open_sftp()
    for root, _, files in os.walk(local_dir):
        for file in files:
            local_path = os.path.join(root, file)
            remote_path = os.path.join(remote_dir, file)
            sftp.put(local_path, remote_path)
            print(f"Backed up {local_path} to {remote_path}")
    sftp.close()
    ssh.close()

if __name__ == "__main__":
    local_dir = input("Enter the local directory path: ")
    remote_dir = input
