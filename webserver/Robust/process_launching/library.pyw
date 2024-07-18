# ProcessLauncher.pyw
# Used for subprocesses to run process under different name on Windows Operating System.
#  newExecutableName parameter - the new .exe executable file name. 
#  targetFolder      parameter - path where the new copy of python executable will be created. 
#  Returns string path to new renamed copy of pythonw.exe or python.exe according to sys.executable. 
# TODO: Permission denied when launching consequential subprocess. Try to reuse subprocess if it's the same.
# TODO: Check if copied custom executable with the name exists. If it already exists, simply reuse it for the next subprocess launch.

# produce_renamed_python_executable to launch Python scripts under different process name.
# Windows determine the process name by executable name. 
# This function produces a new renamed python.exe executable file.
# For later use, to launch scripts under new process name.

#GENERAL NOTE: Always write programs with initial feedback that can be later aligned to make something meaningful.

from os      import path, makedirs; 
from shutil  import copy2;
from pathlib import Path 
from sys     import exec_prefix

def produce_renamed_python_executable(new_executable_path : str): 
    python_executable_installed_ = Path(exec_prefix, 'python.exe') #change to pythonw to create a pythonw executable.
    python_executable_new = Path(new_executable_path)
    makedirs(path.dirname(new_executable_path), exist_ok=True)
    return str(copy2(python_executable_installed_, python_executable_new))  

import tempfile
def produce_renamed_python_executable_in_temp_directory(new_executable_path : str): 
    return produce_renamed_python_executable(Path(tempfile.gettempdir(), new_executable_path))
i = 0
if __name__ == "__main__":


    import sys
    print(sys.argv[1])

    print(len(sys.argv))

    for arg in sys.argv:
        print(i, arg)
        i=i+1

    if len(sys.argv) == 1:
        print("Creating a new executable at Temporary Folder.")
        new_python_exe_path = produce_renamed_python_executable_in_temp_directory('python_custom_processes/python_program.exe')
        print('New Python Executable created at Path: ' + new_python_exe_path)

    if len(sys.argv) >= 2:
        if sys.argv[1] == "Temporary_Directory": 
            if len(sys.argv) < 3: print("Error: Syntax: library.pyw Temporary_Directory Windows: C:/users/yourusername/Desktop/YourFileName.exe or Linux: /home/yourusername/Desktop/YourFileName.exe")
            input()
            sys.exit()
            #else: produce_renamed_python_executable_in_temp_directory(sys.argv[2])
        if sys.argv[1] == "At_Directory": 
            if len(sys.argv) < 3: print("Error: Syntax: library.pyw At_Directory")


    sys.exit()
    #import sys, os
    #if len(sys.argv) == 0:
    #    example_path = os.path.dirname(os.path.abspath(__file__))
    #    example_path = example_path.replace('\\', '/')
    #    exceptioninfo = f"""
    #    Please provide a path to produce a new renamed Python executable. \n  
    #    Example:   python {os.path.basename(__file__)}  \'{example_path}/new_python.exe\'  
    #    Yours:     python {os.path.basename(__file__)}  \'\'
    #    """
    #    raise Exception(exceptioninfo)
    
    #if len(sys.argv) > 1:
    #    print(sys.argv[1])
    #    if sys.argv[1] == "tempdir":
    #        print("custom")
   # print("here")
    #input()

    
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