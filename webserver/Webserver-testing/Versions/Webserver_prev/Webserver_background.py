import subprocess
import tempfile
import os

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Path to Webserver_background_terminate.py
background_terminate_path = os.path.join(current_directory, "Webserver_background_terminate.py")

# Path to Webserver.py
webserver_path = os.path.join(current_directory, "Webserver.py")

# Check if Webserver_background_terminate.py exists
if not os.path.exists(background_terminate_path):
    raise FileNotFoundError("Webserver_background_terminate.py not found at", background_terminate_path)

# Check if Webserver.py exists
if not os.path.exists(webserver_path):
    raise FileNotFoundError("Webserver.py not found at", webserver_path)

# Run Webserver_background_terminate.py
subprocess.run(["pythonw", background_terminate_path])

# Run Webserver.py and capture its process ID
process = subprocess.Popen(["pythonw", webserver_path])

# Get the process ID
pid = process.pid

# Save the pid to a file

# For Linux:
#path = os.path.join('/var/lib', 'Vanilla_Server', 'Webserver_pid.txt')

# For Windows (per-user):
path = os.path.join(os.getenv('APPDATA'), 'Vanilla_Server', 'Webserver_pid.txt')

# Temporary files didn't work, they delete files too often.
#path = os.path.join(tempfile.gettempdir(), 'Vanilla_Server', 'Webserver_pid.txt')

os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, 'w') as file:
    file.write(str(pid))

print("Webserver started with PID:", pid)
print("PID saved to:", path)
