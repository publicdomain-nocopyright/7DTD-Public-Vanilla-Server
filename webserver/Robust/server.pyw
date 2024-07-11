import sys
sys.dont_write_bytecode = True

import server_library

import os
if os.environ.get('SUBPROCESS_EXECUTION'):
    # Define the filename
    filename = "counter.txt"

    # Read the current value from the file, if it exists
    try:
        with open(filename, "r") as file:
            counter = int(file.read().strip())
    except FileNotFoundError:
        counter = 0

    # Increment the counter
    counter += 1

    # Write the updated value back to the file
    with open(filename, "w") as file:
        file.write(str(counter))

    print("test")
    input()
