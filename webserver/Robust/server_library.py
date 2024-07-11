import sys
import inspect
import subprocess
import os

def get_importing_script_name():
    script_name = sys.argv[0]
    calling_script = inspect.stack()[-1].filename
    return script_name, calling_script

if __name__ != "__main__":
    script_name, calling_script = get_importing_script_name()
    print(f"Calling script's filename: {calling_script}")

    # Check if this is already a subprocess execution
    if not os.environ.get('SUBPROCESS_EXECUTION'):
        # Set an environment variable to indicate subprocess execution
        env = os.environ.copy()
        env['SUBPROCESS_EXECUTION'] = '1'

        # Run the calling script as a subprocess with the new environment
        subprocess.Popen(['python', calling_script], env=env)
    else:
        print("This is a subprocess execution. Skipping Popen to avoid infinite loop.")