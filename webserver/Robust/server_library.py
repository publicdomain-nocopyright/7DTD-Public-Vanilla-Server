import sys, inspect

def get_importing_script_name():
    script_name = sys.argv[0]
    calling_script = inspect.stack()[-1].filename
    return script_name, calling_script



if __name__ != "__main__":
    script_name, calling_script = get_importing_script_name()
    print(f"Script name of the importing program: {script_name}")
    print(f"Calling script's filename: {calling_script}")
    import subprocess
    subprocess.Popen(['cmd.exe', '/k', 'python', calling_script])
