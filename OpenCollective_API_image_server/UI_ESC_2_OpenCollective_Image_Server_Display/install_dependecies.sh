#!/bin/bash
 
# Need to be ran as root.
sudo apt install python3-pip
sudo apt install python3.11-venv

# Create new environment and activate it
python3 -m venv venv
source venv/bin/activate

# Install dependecies.
pip install Pillow
pip install requests