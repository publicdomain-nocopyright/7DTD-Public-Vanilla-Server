import signal
import sys, os

def signal_handler(sig, frame):
    print("\nCtrl+C pressed. Exiting...")
    os._exit(1)

# Set up the signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)