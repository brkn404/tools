import subprocess

def scan_wifi():
    networks = subprocess.check_output(['nmcli', 'dev', 'wifi'], universal_newlines=True)
    print(networks)

if __name__ == "__main__":
    scan_wifi()

