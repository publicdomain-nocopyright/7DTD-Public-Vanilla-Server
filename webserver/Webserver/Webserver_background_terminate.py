import os
import tempfile

# For Linux:
#path = os.path.join('/var/lib', 'Vanilla_Server', 'Webserver_pid.txt')

# For Windows (per-user):
path = os.path.join(os.getenv('APPDATA'), 'Vanilla_Server', 'Webserver_pid.txt')

# Temporary files didn't work, they delete files too often.
#path = os.path.join(tempfile.gettempdir(), 'Vanilla_Server', 'Webserver_pid.txt')

# Read the pid from the file
if os.path.exists(path):
    with open(path, 'r') as file:
        pid = int(file.read().strip())

    # Terminate the process using the pid
    try:
        os.kill(pid, 9)  # Sends SIGKILL signal
        os.remove(path)
        print("Process with PID", pid, "terminated successfully.")
    except OSError:
        print("Failed to terminate process with PID", pid)
