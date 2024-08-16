import re
import json
import time
from datetime import datetime
import get_path_latest_game_server_log_file

def process_log_file(file_path):
    players = {}
    server_status = "Offline"
    last_timestamp = None

    patterns = [
        (r"PlayerLogin: (.+?)/V", "Online,Joining"),
        (r"PlayerSpawnedInWorld.*PlayerName='(.+?)'", "Online,Spawned"),
        (r"GMSG: Player '(.+?)' joined the game", "Online,Playing"),
        (r"GMSG: Player '(.+?)' left the game", "Offline"),
        (r"Player disconnected: EntityID=.*PlayerName='(.+?)'", "Offline"),
        (r"\[Auth\].*PlayerName='(.+?)'", None),
        (r"INF.*PlayerName='(.+?)'", None),
    ]

    with open(file_path, 'r') as file:
        for line in file:
            timestamp_match = re.match(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})', line)
            if timestamp_match:
                last_timestamp = datetime.strptime(timestamp_match.group(1), '%Y-%m-%dT%H:%M:%S')
                server_status = "Online"

            for pattern, status in patterns:
                match = re.search(pattern, line)
                if match:
                    player_name = match.group(1)
                    if status:
                        if status.startswith("Online"):
                            players[player_name] = {"status": status}
                        elif status == "Offline":
                            players.pop(player_name, None)
                    
                    pltfm_id_match = re.search(r"PltfmId='(\w+_\d+)'", line)
                    if pltfm_id_match:
                        pltfm_id = pltfm_id_match.group(1)
                        if player_name in players:
                            players[player_name]["pltfm_id"] = pltfm_id
                    
                    break

    online_count = len(players)

    # Check if the server is stale (no updates in the last 5 minutes)
    if last_timestamp:
        time_difference = datetime.now() - last_timestamp
        if time_difference.total_seconds() > 300:  # 5 minutes
            server_status = "Offline"
            players = {}
            online_count = 0

    return {
        "online_count": online_count,
        "players": players,
        "server_status": server_status
    }

def main():
    
    
    while True:
        latest_log_file = get_path_latest_game_server_log_file.get_path_latest_game_server_log_file()
        result = process_log_file(latest_log_file)
        print(json.dumps(result, indent=2))
        time.sleep(3)

if __name__ == "__main__":
    main()