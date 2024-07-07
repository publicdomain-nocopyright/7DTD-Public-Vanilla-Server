# webserver_start.pyw | Process and threads manager.
# First proccess should be responsible for launcher
# Second process should be responsible for launching
# Thrid process should be the program.

try: 
    import os, sys
    import multiprocessing
    import subprocess

    def my_function():
        print("Function is running in a new process with a new console.")
        print("Test")
        input()

    def run_in_new_console():
        subprocess.run(['python', sys.argv[0], 'child'], creationflags=subprocess.CREATE_NEW_CONSOLE)

    if __name__ == "__main__":
        if len(sys.argv) > 1 and sys.argv[1] == 'child':
            my_function()
            
        else:
            p = multiprocessing.Process(target=run_in_new_console)
            p.start()
            p.join()



except Exception:
    p = multiprocessing.Process(target=run_in_new_console)
    
