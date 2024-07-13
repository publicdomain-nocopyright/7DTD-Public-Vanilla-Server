# Used for subprocesses to run process under different name on Windows Operating System.
#  targetFolder argument - path where the new copy of python executable will be created. 
#  Returns string path to new renamed copy of pythonw.exe or python.exe according to sys.executable. 
import os, subprocess, shutil, sys, tempfile
def produce_renamed_python_executable(
        newExecutableName="python_program.exe", 
        targetFolder=os.path.join(tempfile.gettempdir(), "python_custom_processes")
    ): 
    os.makedirs(targetFolder, exist_ok=True)
    return {'renamed_pythonexefilePath': 
            shutil.copy2(os.path.join(sys.exec_prefix, 'python.exe'), 
                        os.path.join(targetFolder, newExecutableName))}


renamed_pythonexefilePath = produce_renamed_python_executable()
print(renamed_pythonexefilePath)
subprocess.Popen([renamed_pythonexefilePath["renamed_pythonexefilePath"], 'C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\process_launching\\Tests\\module.py'])
