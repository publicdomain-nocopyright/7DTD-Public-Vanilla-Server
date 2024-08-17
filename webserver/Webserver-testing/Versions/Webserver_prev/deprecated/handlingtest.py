import signal
import os
import time

import ctypes

def terminate_process(pid):
    try:
        # Run the taskkill command
        import subprocess
        subprocess.run(["taskkill", "/F", "/PID", str(pid)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to terminate process {pid}: {e}")

        
def signal_handler(sig, frame):
    print("Interrupt received. Exiting...")
    current_pid = os.getpid()
    
    # Terminate the current process
    terminate_process(current_pid)

signal.signal(signal.SIGINT, signal_handler)

print("Running. Press CTRL+C to exit.")
while True:
    time.sleep(1)
