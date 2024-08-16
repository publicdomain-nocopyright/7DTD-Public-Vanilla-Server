import re
import json
import time
from datetime import datetime
import get_path_latest_game_server_log_file

def process_log_file(file_path):
    players = {}
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

    return {
        "online_count": online_count,
        "players": players
    }

def main():
    while True:
        latest_log_file = get_path_latest_game_server_log_file.get_path_latest_game_server_log_file()
        result = process_log_file(latest_log_file)
        print(json.dumps(result, indent=2))
        with open('Webserver_player_status.json', 'w') as json_file:
                    json.dump(result, json_file, indent=2)
        time.sleep(3)

if __name__ == "__main__":
    main()