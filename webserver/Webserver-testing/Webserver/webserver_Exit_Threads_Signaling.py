import signal
import sys

def signal_handler(sig, frame):
    print("\nCtrl+C pressed. Exiting...")
    sys.exit(0)

# Set up the signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)