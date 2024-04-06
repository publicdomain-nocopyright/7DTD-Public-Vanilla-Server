#!/bin/bash

# Get the directory of the script
script_dir="$(cd "$(dirname "$0")" && pwd)"
echo "The directory of the current script is: $script_dir"
cd $script_dir
# Run the Python script in the background using nohup
nohup python3 OpenCollective_API_image_server.py > OpenCollective_API_image_server.log 2>&1 &
ps aux | grep 'monitor.py' | grep -v grep | awk '{print $2}'