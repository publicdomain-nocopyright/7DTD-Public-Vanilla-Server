# program.pyw - this source file that demonstrates
# Topic: shutil.copyfile corrupts copied file when it's running under Pythonw on Windows 10 Home.
#  shutil.copyfile under .pyw for some reason corrupts the copied file. 
#  Meanwhile: running as .py python.exe shutil.copyfile is producing the file copy correctly. 
#  Workaround: run copyfile operation under python.exe instead of pythonw.exe

# Testcase
# pythonw program.pyw      - not working. (The copied file not working)
# python program.pyw       - working. (The copied file works)


# Used for subprocesses to run process under different name on Windows Operating System.
def produce_renamed_python_executable(): 
    import os, subprocess, shutil, sys, tempfile
    os.makedirs(os.path.join(tempfile.gettempdir(), "modifield_python"), exist_ok=True)
    renamed_pythonexefile = shutil.copy2(sys.executable, os.path.join(tempfile.gettempdir(), "modifield_python\\modified_python.exe"))


#subprocess.Popen([renamed_pythonexefile, 'C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\process_launching\\module.py'])

env = os.environ.copy()
#C:\Users\Windows10\AppData\Local\Temp\webserver_python\webservertest.exe

#C:\Users\Windows10\Documents\GitHub\7DTD-Public-Vanilla-Server\webserver\Robust\webserver.exe

#subprocess.Popen(['C:\\Users\\Windows10\\AppData\\Local\\Temp\\webserver_python\\webservertest.exe', 'C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\process_launching\\module.py'])
#subprocess.Popen(['C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\webserver.exe', 'C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\process_launching\\module.py'])
#subprocess.Popen(['python', 'C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\process_launching\\module.py'])

print("done")