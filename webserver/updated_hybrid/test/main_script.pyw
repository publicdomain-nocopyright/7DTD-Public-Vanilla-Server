import os
import sys
import subprocess

def run_script_in_new_console(script_path):
    subprocess.run(['cmd', '/c', 'start', 'cmd', '/k', f'python {script_path}'], creationflags=subprocess.CREATE_NEW_CONSOLE)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'child':
        # Actual script code goes here
        print("Function is running in a new process with a new console.")
        print("Test")adsf
        input()
    else:
        script_path = __file__
        run_script_in_new_console(script_path)
