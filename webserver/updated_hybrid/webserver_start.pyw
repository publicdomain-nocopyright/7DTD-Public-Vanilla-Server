# webserver_start.pyw | Process and threads manager.
import os
import sys
import multiprocessing
import subprocess

def my_function():
    print("Function is running in a new process with a new console.")
    print("Test")
    input()

def run_in_new_console():
    script_path = sys.argv[0]  # Current script
    subprocess.run(['python', script_path, 'child'], creationflags=subprocess.CREATE_NEW_CONSOLE)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'child':
        my_function()
        
    else:
        p = multiprocessing.Process(target=run_in_new_console)
        p.start()
        p.join()



