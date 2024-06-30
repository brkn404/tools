import requests

def directory_bruteforce(url, wordlist):
    with open(wordlist, 'r') as file:
        directories = file.read().splitlines()

    found_directories = []
    for directory in directories:
        dir_url = f"{url}/{directory}"
        response = requests.get(dir_url)
        if response.status_code == 200:
            found_directories.append(dir_url)
            print(f"Found directory: {dir_url}")
    return found_directories

if __name__ == "__main__":
    url = input("Enter the target URL: ")
    wordlist = input("Enter the wordlist file path: ")
    found_directories = directory_bruteforce(url, wordlist)
    print(f"Found directories: {found_directories}")
