import sys
import inspect
import subprocess
import os

import sys

def set_process_title(title):
    if sys.platform.startswith('win'):
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        try:
            import setproctitle
            setproctitle.setproctitle(title)
        except ImportError:
            print("Error: Unable to set process title. Install the 'setproctitle' package.")


def get_importing_script_name():
    script_name = sys.argv[0]
    calling_script = inspect.stack()[-1].filename
    return script_name, calling_script

if __name__ != "__main__":



    new_process_name = "waffles"
    
    set_process_title(new_process_name)
    script_name, calling_script = get_importing_script_name()
    print(f"Calling script's filename: {calling_script}")

    # Relaunching importer under subprocess.
    # Check if this is already a subprocess execution
    if not os.environ.get('SUBPROCESS_EXECUTION'):
        # Set an environment variable to indicate subprocess execution
        env = os.environ.copy()
        env['SUBPROCESS_EXECUTION'] = '1'


        import sys, tempfile, shutil
        print("THIS IS PYTHON executable")
        print(sys.executable)


        temp_dir = tempfile.gettempdir()
        target_dir = os.path.join(temp_dir, "webserver_python")
        source_executable = sys.executable
        target_executable = os.path.join(target_dir, "webservertest.exe")

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        shutil.copyfile(source_executable, target_executable)
        absolute_path = os.path.abspath(target_executable)

        print(absolute_path)



        #input()
        # Run the calling script as a subprocess with the new environment
        subprocess.Popen(['webserver', calling_script], env=env)

        # Optionally, exit the current process
        sys.exit()

    else:
        print("This is a subprocess execution. Skipping Popen to avoid infinite loop.")
