# program.pyw - this source file that demonstrates
# Topic: shutil.copyfile corrupts copied file when it's running under Pythonw on Windows 10 Home.
#  shutil.copyfile under .pyw for some reason corrupts the copied file. 
#  Meanwhile: running as .py python.exe shutil.copyfile is producing the file copy correctly. 
#  Workaround: run copyfile operation under python.exe instead of pythonw.exe

# Testcase
# pythonw program.pyw      - not working. (The copied file not working)
# python program.pyw       - working. (The copied file works)


# Used for subprocesses to run process under different name on Windows Operating System.
# Returns string path to new renamed copy of pythonw.exe or python.exe according to sys.executable. 
import os, subprocess, shutil, sys, tempfile
def produce_renamed_python_executable(targetFolder=os.path.join(tempfile.gettempdir(), "modifield_python")): 
    os.makedirs(targetFolder, exist_ok=True)
    return shutil.copy2(sys.executable, os.path.join(targetFolder, "modified_python.exe"))

produce_renamed_python_executable()
#subprocess.Popen([renamed_pythonexefile, 'C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\process_launching\\module.py'])

env = os.environ.copy()
#C:\Users\Windows10\AppData\Local\Temp\webserver_python\webservertest.exe

#C:\Users\Windows10\Documents\GitHub\7DTD-Public-Vanilla-Server\webserver\Robust\webserver.exe

#subprocess.Popen(['C:\\Users\\Windows10\\AppData\\Local\\Temp\\webserver_python\\webservertest.exe', 'C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\process_launching\\module.py'])
#subprocess.Popen(['C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\webserver.exe', 'C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\process_launching\\module.py'])
#subprocess.Popen(['python', 'C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\process_launching\\module.py'])

print("done")