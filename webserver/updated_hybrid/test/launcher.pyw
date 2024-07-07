import subprocess


try:
    script_path = 'main_script.py'
    subprocess.run(['python', script_path, 'child'])
except Exception as e:
    subprocess.run(['cmd', '/c', 'start', 'cmd', '/k', f'echo Syntax error in file {file_path}: {e}'], creationflags=subprocess.CREATE_NEW_CONSOLE)
    input()
    

