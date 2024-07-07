# webserver_start.pyw | Process and threads manager.
# First proccess should be responsible for launcher, reporting syntax errors in the launcher.
# Second process should be responsible for launching, reporting syntax errors of the functions and launching functions
# Thrid and all others processes should be the executed functions for application.

# Launcher Process should be responsible for reporting its own syntax errors and launch other functions as separate processes.

import os
import sys
import multiprocessing
import subprocess
import py_compile

def my_function():
    print("Function is running in a new process with a new console.")
    print("Test")
    input()

def run_in_new_console():
    subprocess.run(['python', sys.argv[0], 'child'], creationflags=subprocess.CREATE_NEW_CONSOLE)

def check_syntax(file_path):
    try:
        py_compile.compile(file_path, doraise=True)
    except py_compile.PyCompileError as e:
        print(f"Syntax error in file {file_path}: {e}")
        subprocess.run(['cmd', '/k', 'echo', f"Syntax error in file {file_path}: {e}"], creationflags=subprocess.CREATE_NEW_CONSOLE)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'child':
        my_function()
    else:
        check_syntax(sys.argv[0])
        p = multiprocessing.Process(target=run_in_new_console)
        p.start()
        p.join()
