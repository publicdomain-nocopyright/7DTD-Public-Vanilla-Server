import subprocess
import py_compile
import sys

def check_syntax(file_path):
    try:
        py_compile.compile(file_path, doraise=True)
    except py_compile.PyCompileError as e:
        subprocess.run(['cmd', '/c', 'start', 'cmd', '/k', f'echo Syntax error in file {file_path}: {e}'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        sys.exit(1)

if __name__ == "__main__":
    script_path = 'main_script.py'  # Path to your main script
    check_syntax(script_path)
    subprocess.run(['python', script_path, 'child'])
