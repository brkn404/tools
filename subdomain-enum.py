import requests

def subdomain_enum(domain, wordlist):
    with open(wordlist, 'r') as file:
        subdomains = file.read().splitlines()
    
    found_subdomains = []
    for subdomain in subdomains:
        url = f"http://{subdomain}.{domain}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                found_subdomains.append(url)
                print(f"Found subdomain: {url}")
        except requests.ConnectionError:
            continue
    return found_subdomains

if __name__ == "__main__":
    domain = input("Enter the target domain: ")
    wordlist = input("Enter the wordlist file path: ")
    found_subdomains = subdomain_enum(domain, wordlist)
    print(f"Found subdomains: {found_subdomains}")
