#!/bin/bash

# Get the PID of the running Python process
PID=$(ps aux | grep 'OpenCollective_API_image_server.py' | grep -v grep | awk '{print $2}')

# Check if the process is running
if [ -n "$PID" ]; then
    # Kill the process
    kill $PID
    echo "Process stopped."
else
    echo "Process is not running."
fi