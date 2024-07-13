# program.pyw - this source file that demonstrates
# Topic: shutil.copyfile corrupts copied file when it's running under Pythonw on Windows 10 Home.
#  shutil.copyfile under .pyw for some reason corrupts the copied file. 
#  Meanwhile: running as .py python.exe shutil.copyfile is producing the file copy correctly. 
#  Workaround: run copyfile operation under python.exe instead of pythonw.exe

# Testcase
# pythonw program.pyw      - not working. (The copied file not working)
# python program.pyw       - working. (The copied file works)


# Used for subprocesses to run process under different name on Windows Operating System.
#  targetFolder argument - path where the new copy of python executable will be created. 
#  Returns string path to new renamed copy of pythonw.exe or python.exe according to sys.executable. 
import os, subprocess, shutil, sys, tempfile
def produce_renamed_python_executable(
        newExecutableName="python_program.exe", 
        targetFolder=os.path.join(tempfile.gettempdir(), "python_custom_processes")
): 
    os.makedirs(targetFolder, exist_ok=True)
    return shutil.copy2(sys.exec_prefix + '\\python.exe', os.path.join(targetFolder, newExecutableName))

renamed_pythonexefilePath = produce_renamed_python_executable()
print(renamed_pythonexefilePath)
subprocess.Popen([renamed_pythonexefilePath, 'C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\process_launching\\Tests\\module.py'])



# variation to copy default executed python executable
import os, subprocess, shutil, sys, tempfile
def produce_renamed_python_executable_auto(
        executableName="python_program.exe", 
        targetFolder=os.path.join(tempfile.gettempdir(), "python_custom_processes")
): 
    os.makedirs(targetFolder, exist_ok=True)
    return shutil.copy2(sys.executable, os.path.join(targetFolder, executableName))










#subprocess.Popen([renamed_pythonexefile, 'C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\process_launching\\module.py'])






env = os.environ.copy()
#C:\Users\Windows10\AppData\Local\Temp\webserver_python\webservertest.exe

#C:\Users\Windows10\Documents\GitHub\7DTD-Public-Vanilla-Server\webserver\Robust\webserver.exe

#subprocess.Popen(['C:\\Users\\Windows10\\AppData\\Local\\Temp\\webserver_python\\webservertest.exe', 'C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\process_launching\\module.py'])
#subprocess.Popen(['C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\webserver.exe', 'C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\process_launching\\module.py'])
#subprocess.Popen(['python', 'C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\process_launching\\module.py'])

print("done")