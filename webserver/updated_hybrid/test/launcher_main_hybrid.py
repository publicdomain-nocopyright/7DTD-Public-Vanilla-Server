import subprocess

try:
    script_path = 'main_script.py'
    result = subprocess.run(['python', script_path, 'child'], check=True, capture_output=True, text=True, cwd='C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\updated_hybrid\\test')
    print("Subprocess output:")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    # Display error message and context in a new console window and pause
    error_message = f"Subprocess error in file {script_path}:\n{e.stderr}"
    current_directory = subprocess.run(['cmd', '/c', 'cd'], capture_output=True, text=True)
    cmd_command = f'cmd /c start cmd /k "echo {error_message} && echo Current directory: {current_directory.stdout.strip()} && python -c \\"import traceback; traceback.print_exc()\\""'
    subprocess.run(cmd_command, shell=True)
    input("Press Enter to exit...")
except Exception as e:
    print(f"Unexpected error: {e}")
