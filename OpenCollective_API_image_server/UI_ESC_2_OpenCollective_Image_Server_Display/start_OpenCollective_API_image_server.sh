#!/bin/bash

bash ./stop_OpenCollective_API_image_server.sh
# Get the directory of the script
script_dir="$(cd "$(dirname "$0")" && pwd)"
echo "The directory of the current script is: $script_dir"
cd $script_dir
# Run the Python script in the background using nohup
python3 -m venv venv
source ./venv/bin/activate

wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
pip install pillow==9.5.0
pip install requests
pip install --upgrade certifi

nohup python3 OpenCollective_API_image_server.py > OpenCollective_API_image_server.log 2>&1 &
ps aux | grep 'OpenCollective_API_image_server.py' | grep -v grep | awk '{print $2}'