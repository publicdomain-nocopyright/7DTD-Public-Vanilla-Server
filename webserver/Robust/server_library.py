import sys
import inspect
import subprocess
import os

import sys

import logging

if not os.environ.get('SUBPROCESS_EXECUTION'):
    os.remove("logfile.txt")
logging.basicConfig(filename='logfile.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def set_process_title(title):
    if sys.platform.startswith('win'):
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        try:
            import setproctitle
            setproctitle.setproctitle(title)
        except ImportError:
            logging.info("Error: Unable to set process title. Install the 'setproctitle' package.")


def get_importing_script_name():
    script_name = sys.argv[0]
    calling_script = inspect.stack()[-1].filename
    return script_name, calling_script

if __name__ != "__main__":    

    set_process_title("waffles")
    script_name, calling_script = get_importing_script_name()
    logging.info(f"Calling script's filename: {calling_script}")

    # Relaunching importer under subprocess.
    # Check if this is already a subprocess execution
    if not os.environ.get('SUBPROCESS_EXECUTION'):
        # Set an environment variable to indicate subprocess execution
        env = os.environ.copy()
        env['SUBPROCESS_EXECUTION'] = '1'


        import sys, tempfile, shutil
        logging.info("THIS IS PYTHON executable")
        logging.info(sys.executable)


        temp_dir = tempfile.gettempdir()
        target_dir = os.path.join(temp_dir, "webserver_python")
        source_executable = sys.executable
        target_executable = os.path.join(target_dir, "webservertest.exe")

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        shutil.copyfile(source_executable, target_executable)
        absolute_path_target_executable = os.path.abspath(target_executable)

        logging.info("test2")
        logging.info(absolute_path_target_executable)

        



        #input()
        # Run the calling script as a subprocess with the new environment
        logging.info("test3")
        subprocess.Popen(['C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\webserver.exe', calling_script], env=env)
        #subprocess.Popen(['C:\\Users\\Windows10\\AppData\\Local\\Temp\\webserver_python\\webservertest.exe', calling_script], env=env)

        
        # Optionally, exit the current process
        sys.exit()

    else:
        logging.info("This is a subprocess execution. Skipping Popen to avoid infinite loop.")
