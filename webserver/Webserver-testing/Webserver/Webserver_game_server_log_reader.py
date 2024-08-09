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
    for file in os.listdir(log_directory):
        try:
            date_time_str = file.split('__')[1] + '__' + file.split('__')[2].split('.')[0]
            file_datetime = datetime.strptime(date_time_str, '%Y-%m-%d__%H-%M-%S')
            sorted_files.append((file_datetime, file))
        except (IndexError, ValueError):
            # If the filename doesn't match the expected format, use a minimum date
            #sorted_files.append((datetime.min, file))
            pass

    # Sort the list of tuples and extract just the filenames
    sorted_files.sort(reverse=True)
    sorted_filenames = [file for _, file in sorted_files]

    # Print the sorted list of files
    #for file in sorted_filenames:
    #    print(file)

    # Return latest log file
   
    return str(sorted_filenames[0])

   # if relative_path:
        
    #if not relative_path:
    #    DEFAULT_LOG_DIRECTORY = r"C:\Program Files (x86)\Steam\steamapps\common\7 Days To Die\7DaysToDie_Data"
    #    
    #import os 
    #if log_directory is standard:
    #    print("yes")
    #    log_directory = os.path.abspath(__file__)
    #
    #

    #return {"game_server_log_file_path": log_directory}
    pass

def get_latest_game_server_log_filepath_debug():
    print("FROM_DEFAULT_LOG_DIRECTORY", get_latest_game_server_log_file_path("FROM_DEFAULT_LOG_DIRECTORY"))



if __name__ == "__main__":
    print(get_latest_game_server_log_file_path())