
import os
import glob
from datetime import datetime
import re

def get_latest_game_server_log_file_name():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_directory = os.path.join(script_dir, '../7DaysToDie_Data')

    # Temporary | Optional | Remove this later
    # Override log directory with default 7DTD Path on Windows.
    #log_directory = "C:/Program Files (x86)/Steam/steamapps/common/7 Days To Die/7DaysToDie_Data"

    file_pattern = 'output_log__*.txt'
    log_files = glob.glob(os.path.join(log_directory, file_pattern))

    # Function to extract timestamp from filename
    def extract_timestamp(filename):
        timestamp_str = filename.split('__')[1]  
        return datetime.strptime(filename.split('__')[1]+ "__" +filename.split('__')[2], '%Y-%m-%d__%H-%M-%S.txt')
    log_files.sort(key=lambda x: extract_timestamp(x), reverse=True)
    if log_files:
        latest_file = log_files[0]
        print("Latest file:", latest_file)
        return latest_file
        


# Define the function to read the log file
def read_server_log(LOG_FILE_PATH):
    try:
        with open(LOG_FILE_PATH, 'r') as file:
            log_content = file.read()
        return log_content
    except FileNotFoundError:
        return "Log file not found."
    except Exception as e:
        return f"An error occurred: {e}"
    

import os
import glob
from datetime import datetime

def list_game_server_log_files():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_directory = os.path.join(script_dir, '../7DaysToDie_Data')

    # Temporary | Optional | Remove this later
    # Override log directory with default 7DTD Path on Windows.
    #log_directory = "C:/Program Files (x86)/Steam/steamapps/common/7 Days To Die/7DaysToDie_Data"

    file_pattern = 'output_log__*.txt'
    log_files = glob.glob(os.path.join(log_directory, file_pattern))

    # Function to extract timestamp from filename
    def extract_timestamp(filename):
        timestamp_str = os.path.basename(filename).split('__')[1] + "__" + os.path.basename(filename).split('__')[2]
        return datetime.strptime(timestamp_str, '%Y-%m-%d__%H-%M-%S.txt')

    # Sort log files by timestamp
    sorted_log_files = sorted(log_files, key=extract_timestamp, reverse=True)

    # Print sorted log files
    print("Log files sorted by timestamp (most recent first):")
    for file in sorted_log_files:
        timestamp = extract_timestamp(file)
        print(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {file}")

    return sorted_log_files



if __name__ == "__main__":
    get_latest_game_server_log_file_name()
    print(list_game_server_log_files())