import os
import sys
import subprocess
import py_compile
import threading

def my_function():
    print("Function is running in a new process with a new console.")
    print("Test")
    input()

def run_in_new_console():
    subprocess.run(['python', sys.argv[0], 'child'], creationflags=subprocess.CREATE_NEW_CONSOLE)
asdf
def check_syntax(file_path):
    try:
        py_compile.compile(file_path, doraise=True)
    except py_compile.PyCompileError as e:
        subprocess.run(['cmd', '/c', 'start', 'cmd', '/k', f'echo Syntax error in file {file_path}: {e}'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        sys.exit(1)
import sys
import threading
import traceback

def main_functionality():
    # Your main script functionality goes here
    print("Running main functionality")
    # Add your code here

def syntax_check():
    try:
        # Attempt to compile the script
        with open(__file__, 'r') as file:
            compile(file.read(), __file__, 'exec')
        return None
    except SyntaxError as e:
        return str(e)
import sys
import threading
import traceback

def main_functionality():
    # Place your main script functionality here
    print("Main functionality is running...")
    # Add your code here

def run_in_new_thread():
    thread = threading.Thread(target=main_functionality)
    thread.start()
    thread.join()

if __name__ == "__main__":
    try:
        # Check for syntax errors by executing the file
        with open(__file__, 'r') as file:
            compile(file.read(), __file__, 'exec')
        
        if len(sys.argv) > 1 and sys.argv[1] == 'child':
            # If 'child' argument is provided, run the main functionality
            main_functionality()
        else:
            # If no 'child' argument, act as a launcher
            print("Launching main functionality in a new thread...")
            run_in_new_thread()
    except SyntaxError as e:
        print(f"Syntax error detected: {e}")
        print(traceback.format_exc())
    except Exception as e:
        print(f"An error occurred: {e}")
        print(traceback.format_exc())