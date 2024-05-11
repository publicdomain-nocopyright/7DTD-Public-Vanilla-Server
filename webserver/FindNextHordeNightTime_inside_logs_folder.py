import os
import glob
from datetime import datetime

# Directory containing the log files
log_directory = '.'

# Define the pattern to match files
file_pattern = 'output_log__*.txt'

# Get a list of all files matching the pattern
log_files = glob.glob(os.path.join(log_directory, file_pattern))

# Function to extract timestamp from filename
def extract_timestamp(filename):
    timestamp_str = filename.split('__')[1] 
    return datetime.strptime(filename.split('__')[1]+ "__" +filename.split('__')[2], '%Y-%m-%d__%H-%M-%S.txt')

# Sort the files by timestamp (newest first)
log_files.sort(key=lambda x: extract_timestamp(x), reverse=True)

if log_files:
    latest_file = log_files[0]
    print("Latest file:", latest_file)
else:
    print("No log files found.")
