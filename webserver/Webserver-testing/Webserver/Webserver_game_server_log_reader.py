# A robust standalone function for log file path
def get_latest_game_server_log_file_path(log_directory : str = None) -> str:
    
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
    print("FROM_DEFAULT_LOG_DIRECTORY", get_latest_game_server_log_file_path("FROM_DEFAULT_LOG_DIRECTORY"))



if __name__ == "__main__":

     # Monitor log file, polling algorithm, detect if new log file appeared.
    last_file = get_latest_game_server_log_file_path()
    print(f"Starting monitor. Latest file: {last_file}")

    import time
    while True:
        time.sleep(5)
        current_file = get_latest_game_server_log_file_path()
        # Process log file 
        # Parse log line
        # Match log line against pattern
        # Track data and associate with other data
        # Export as JSON file and keep it up to date.

        if current_file != last_file:
            print(f"New log file detected: {current_file}")
            last_file = current_file


   