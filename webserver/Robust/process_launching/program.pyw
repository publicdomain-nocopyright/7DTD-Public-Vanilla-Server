# copyfile under .pyw for some reason corrupts the copied file. While running as .py python.exe is working correctly. Workaround: run copy operation as a seprate python.exe instead of pythonw.exe

# Testcase
# pythonw program.pyw      - not working. (The copied file not working)
# python program.pyw       - working. (The copied file works)

import os, subprocess, shutil, sys, tempfile
os.makedirs(os.path.join(tempfile.gettempdir(), "webserver_python"), exist_ok=True)
renamed_pythonexefile = shutil.copyfile(sys.executable, os.path.join(tempfile.gettempdir(), "webserver_python\\webservertest.exe"))

#subprocess.Popen([renamed_pythonexefile, 'C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\process_launching\\module.py'])

env = os.environ.copy()
#C:\Users\Windows10\AppData\Local\Temp\webserver_python\webservertest.exe

#C:\Users\Windows10\Documents\GitHub\7DTD-Public-Vanilla-Server\webserver\Robust\webserver.exe

#subprocess.Popen(['C:\\Users\\Windows10\\AppData\\Local\\Temp\\webserver_python\\webservertest.exe', 'C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\process_launching\\module.py'])
#subprocess.Popen(['C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\webserver.exe', 'C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\process_launching\\module.py'])
#subprocess.Popen(['python', 'C:\\Users\\Windows10\\Documents\\GitHub\\7DTD-Public-Vanilla-Server\\webserver\\Robust\\process_launching\\module.py'])

print("done")