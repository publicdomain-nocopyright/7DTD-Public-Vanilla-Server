# Continous stream pattern matching.
# Stream_pattern_matching.py

import time

# Open the file in read mode
with open('Stream_pattern_matching.py', 'r') as file:
    time.sleep(10)  # Wait for 10 seconds
    line = file.readline()  # Read a line after the wait
    print(line)