# A robust standalone function for log file path
def get_path_latest_game_server_log_file(log_directory : str = None) -> str:
    
    from pathlib import Path; 
    DEFAULT_LOG_DIRECTORY = r"C:\Program Files (x86)\Steam\steamapps\common\7 Days To Die\7DaysToDie_Data"
    RELATIVE_LOG_DIRECTORY = Path(r'..\7DaysToDie_Data').resolve()

    if log_directory == "FROM_DEFAULT_LOG_DIRECTORY":
        log_directory = DEFAULT_LOG_DIRECTORY

    if log_directory == "FROM_RELATIVE_LOG_DIRECTORY":
        log_directory = RELATIVE_LOG_DIRECTORY

    import os; 
    if os.path.exists(RELATIVE_LOG_DIRECTORY) and log_directory is None: 
        log_directory = RELATIVE_LOG_DIRECTORY

    if log_directory is None: 
        log_directory = DEFAULT_LOG_DIRECTORY

    # Sorting directories
    # Sort by date and time these directory before printing
    # output_log__2024-08-08__15-05-45.txt
    
    from datetime import datetime
    sorted_files = []
    for filename in os.listdir(log_directory):
        full_path = os.path.abspath(os.path.join(log_directory, filename))
        try:
            date_time_str = filename.split('__')[1] + '__' + filename.split('__')[2].split('.')[0]
            file_datetime = datetime.strptime(date_time_str, '%Y-%m-%d__%H-%M-%S')
            sorted_files.append((file_datetime, full_path))
        except (IndexError, ValueError):
            # If the filename doesn't match the expected format, skip it
            pass

    sorted_files.sort(reverse=True)

    if sorted_files:
        return str(sorted_files[0][1])
    else:
        return None 

def get_latest_game_server_log_filepath_debug():
    print("FROM_DEFAULT_LOG_DIRECTORY", get_path_latest_game_server_log_file("FROM_DEFAULT_LOG_DIRECTORY"))

def previoustest():
     # Monitor log file, polling algorithm, detect if new log file appeared.
    last_file = get_path_latest_game_server_log_file()
    print(f"Starting monitor. Latest file: {last_file}")

    import time
    while True:
        time.sleep(5)
        current_file = get_path_latest_game_server_log_file()
        # Process log file 
        # Parse log line
        # Match log line against pattern
        # Track data and associate with other data
        # Export as JSON file and keep it up to date.

        if current_file != last_file:
            print(f"New log file detected: {current_file}")
            last_file = current_file




if __name__ == "__main__":



    import time, os
    seek_position : int = 0
    previous_log_file = None
    content = None  
    while True:
        latest_log_file = get_path_latest_game_server_log_file()
        if previous_log_file != latest_log_file:
            print("Loading a log file: ", latest_log_file)
            with open(latest_log_file) as file:
                content = file.read()
                seek_position = file.tell()
                print("Seek position: ", seek_position)          
                   
            previous_log_file = latest_log_file
        #if content is not None:


        time.sleep(2)

   


        
        # Process log file 
        # Process a single log file line
        # Pattern matching might require two lines of log file, since log line could be split for convenience of human reading log file
        #with open(current_file, 'r') as file:
        #    file.readline()
        #    pass

        # Parse log line
        # Match log line against pattern
        # Track data and associate with other data
        # Export as JSON file and keep it up to date.

        # Read file, seek file and look for new file while seeking.


        # Future: Read file content without locking it up (Non-blocking reading)

        # If file content is not completely new
        # seek file for updates from last seek position