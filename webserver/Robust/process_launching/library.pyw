# ProcessLauncher.pyw
# Used for subprocesses to run process under different name on Windows Operating System.
#  newExecutableName parameter - the new .exe executable file name. 
#  targetFolder      parameter - path where the new copy of python executable will be created. 
#  Returns string path to new renamed copy of pythonw.exe or python.exe according to sys.executable. 
# TODO: Permission denied when launching consequential subprocess. Try to reuse subprocess if it's the same.
# TODO: Check if copied custom executable with the name exists. If it already exists, simply reuse it for the next subprocess launch.
import os, shutil, sys, tempfile
def produce_renamed_python_executable(
        newExecutableName="python_program.exe", 
        targetFolder=os.path.join(tempfile.gettempdir(), "python_custom_processes")
    ): 
    os.makedirs(targetFolder, exist_ok=True)
    return shutil.copy2(os.path.join(sys.exec_prefix, 'python.exe'),  #change to pythonw to create a pythonw executable.
                        os.path.join(targetFolder, newExecutableName))
import subprocess
def launch_script_under_different_process_name(
        process_name = "python_new_program.exe",
        scriptToLaunch = 'C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\process_launching\\Tests\\module.py'
     ):
    
    if os.path.isfile(tempfile.gettempdir() + "\\python_custom_processes\\" + process_name):
        print("File exists.")
        return subprocess.Popen([tempfile.gettempdir() + "\\python_custom_processes\\" + process_name , scriptToLaunch])
    else:
        path_to_renamed_python_exe = produce_renamed_python_executable(newExecutableName=process_name)
        print("File does not exist.")
        return subprocess.Popen([path_to_renamed_python_exe, scriptToLaunch])


    

launch_script_under_different_process_name(process_name="test.exe", scriptToLaunch='C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\process_launching\\Tests\\module.py')