def keep_main_thread_alive():
    import time
    while True: 
        time.sleep(100000)

import sys
# Replace the module with the function
sys.modules[__name__] = keep_main_thread_alive()