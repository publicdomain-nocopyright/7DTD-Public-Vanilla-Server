import threading
import code

def start_console():
    console = code.InteractiveConsole()
    console.interact()

console_thread = threading.Thread(target=start_console)
console_thread.start()