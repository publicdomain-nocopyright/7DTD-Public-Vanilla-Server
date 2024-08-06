# Webserver_FindNextHordeNightTime_inside_logs_folder.py

import os
import glob
from datetime import datetime
import re

def find_last_bloodmoon_setday():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Directory containing the log files relative to the script's directory
    log_directory = os.path.join(script_dir, '../7DaysToDie_Data')

    # Temporary | Optional | Remove this later
    # Override log directory with default 7DTD Path on Windows.
    #log_directory = "C:/Program Files (x86)/Steam/steamapps/common/7 Days To Die/7DaysToDie_Data"

    # Define the pattern to match files
    file_pattern = 'output_log__*.txt'

    # Get a list of all files matching the pattern
    log_files = glob.glob(os.path.join(log_directory, file_pattern))

    # Function to extract timestamp from filename
    def extract_timestamp(filename):
        timestamp_str = filename.split('__')[1]  
        return datetime.strptime(filename.split('__')[1]+ "__" +filename.split('__')[2], '%Y-%m-%d__%H-%M-%S.txt')

    # Function to extract day number from line
    def extract_day_number(line):
        match = re.search(r'day (\d+)', line)
        if match:
            return int(match.group(1))
        return None

    # Sort the files by timestamp (newest first)
    log_files.sort(key=lambda x: extract_timestamp(x), reverse=True)

    if log_files:
        latest_file = log_files[0]
        print("Latest file:", latest_file)

        # Open the latest log file
        with open(latest_file, 'r') as file:
            # Read the lines of the file in reverse order
            lines = reversed(file.readlines())
            # Search for the last occurrence of the line containing the information
            for line in lines:
                if "BloodMoon SetDay" in line:
                    day_number = extract_day_number(line)
                    if day_number:
                        return day_number
                    else:
                        print("Day number not found in the line.")
                    break
    else:
        print("No log files found.")
        return None
