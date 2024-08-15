import re
import json
import time

# Define patterns and associated statuses
patterns = [
    (r"PlayerLogin: (.+?)/V", "Online,Joining"),
    (r"PlayerSpawnedInWorld.*PlayerName='(.+?)'", "Online,Spawned"),
    (r"GMSG: Player '(.+?)' joined the game", "Online,Playing"),
    (r"GMSG: Player '(.+?)' left the game", "Offline"),
    (r"Player disconnected: EntityID=.*PlayerName='(.+?)'", "Offline"),
    (r"\[Auth\].*PlayerName='(.+?)'", None),
    (r"INF.*PlayerName='(.+?)'", None),
]

# Infinite loop to continually process the log file
while True:
    # Read the entire log file content

    import get_path_latest_game_server_log_file
    latest_log_file = get_path_latest_game_server_log_file.get_path_latest_game_server_log_file()
    print(latest_log_file)
    with open(latest_log_file) as logfile:
        logfile_content = logfile.read()

    # Initialize dictionary to store player statuses
    player_status = {}

    # Process the entire log file content
    for pattern, status in patterns:
        matches = re.findall(pattern, logfile_content)
        for player_name in matches:
            if status:
                player_status[player_name] = status

    # Write latest player statuses to JSON file
    with open("latest_status.json", "w") as json_file:
        json.dump(player_status, json_file, indent=4)

    # Wait for 3 seconds before the next iteration
    time.sleep(3)
