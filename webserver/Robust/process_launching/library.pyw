# ProcessLauncher.pyw
# Used for subprocesses to run process under different name on Windows Operating System.
#  newExecutableName parameter - the new .exe executable file name. 
#  targetFolder      parameter - path where the new copy of python executable will be created. 
#  Returns string path to new renamed copy of pythonw.exe or python.exe according to sys.executable. 
# TODO: Permission denied when launching consequential subprocess. Try to reuse subprocess if it's the same.
# TODO: Check if copied custom executable with the name exists. If it already exists, simply reuse it for the next subprocess launch.
from os import path, makedirs; 
from shutil import copy2; 
import sys, tempfile
def produce_renamed_python_executable(new_executable_name = None, target_folder = None): 
    if new_executable_name is None: new_executable_name = "python_program.exe"
    if target_folder       is None:    target_folder    = path.join(tempfile.gettempdir(), "python_custom_processes")

    makedirs(target_folder, exist_ok=True)
    return copy2(path.join(sys.exec_prefix, 'python.exe'),  #change to pythonw to create a pythonw executable.
                 path.join(target_folder, new_executable_name))
produce_renamed_python_executable()
input()

import subprocess
def launch_script_under_different_process_name(
        process_name = "python_new_program.exe",
        script_to_launch = 'C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\process_launching\\Tests\\module.py'
     ):
    
    if path.isfile(tempfile.gettempdir() + "\\python_custom_processes\\" + process_name):
        return subprocess.Popen([tempfile.gettempdir() + "\\python_custom_processes\\" + process_name , script_to_launch])
    else:
        path_to_renamed_python_exe = produce_renamed_python_executable(new_executable_name=process_name)
        return subprocess.Popen([path_to_renamed_python_exe, script_to_launch])


    

launch_script_under_different_process_name(process_name="test.exe", script_to_launch='C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\process_launching\\Tests\\module.py')