def get_latest_game_server_log_filepath(log_directory = None):
    
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
    return {"game_server_log_file_path": log_directory}
    pass

def get_latest_game_server_log_filepath_debug():
    print("FROM_DEFAULT_LOG_DIRECTORY", get_latest_game_server_log_filepath("FROM_DEFAULT_LOG_DIRECTORY"))



if __name__ == "__main__":
    get_latest_game_server_log_filepath_debug()