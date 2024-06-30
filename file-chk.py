import hashlib
import os

def hash_file(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256.update(byte_block)
    return sha256.hexdigest()

def check_integrity(directory, hashes):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = hash_file(file_path)
            if file_path in hashes:
                if hashes[file_path] != file_hash:
                    print(f"File {file_path} has been modified!")
            else:
                hashes[file_path] = file_hash
    return hashes

if __name__ == "__main__":
    directory = input("Enter the directory to monitor: ")
    hashes = {}
    hashes = check_integrity(directory, hashes)
    print("Initial integrity check completed.")
