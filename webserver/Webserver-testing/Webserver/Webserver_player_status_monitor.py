import re
import json
import time
from datetime import datetime
import os
import get_path_latest_game_server_log_file

def datetime_to_string(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def process_log_file(file_path, data):
    players = data.get('players', {})
    last_processed_position = data.get('last_processed_position', 0)
    last_processed_file = data.get('last_processed_file', '')
    last_timestamp = data.get('last_timestamp')

    patterns = [
        (r"PlayerLogin: (.+?)/V", "Online,Joining"),
        (r"PlayerSpawnedInWorld.*PlayerName='(.+?)'", "Online,Spawned"),
        (r"GMSG: Player '(.+?)' joined the game", "Online,Playing"),
        (r"GMSG: Player '(.+?)' left the game", "Offline"),
        (r"Player disconnected: EntityID=.*PlayerName='(.+?)'", "Offline"),
        (r"\[Auth\].*PlayerName='(.+?)'", None),
        (r"INF.*PlayerName='(.+?)'", None),
    ]

    if last_processed_file != file_path:
        last_processed_position = 0
        print(f"New log file detected. Processing from the beginning: {file_path}")

    with open(file_path, 'r') as file:
        file.seek(last_processed_position)
        new_lines_processed = 0

        for line in file:
            new_lines_processed += 1
            timestamp_match = re.match(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})', line)
            if timestamp_match:
                last_timestamp = datetime.strptime(timestamp_match.group(1), '%Y-%m-%dT%H:%M:%S')

            for pattern, status in patterns:
                match = re.search(pattern, line)
                if match:
                    player_name = match.group(1)
                    if status:
                        if status.startswith("Online"):
                            players[player_name] = players.get(player_name, {})
                            players[player_name]["status"] = status
                        elif status == "Offline":
                            if player_name in players:
                                players[player_name]["status"] = "Offline"
                    
                    pltfm_id_match = re.search(r"PltfmId='(\w+_\d+)'", line)
                    if pltfm_id_match:
                        pltfm_id = pltfm_id_match.group(1)
                        if player_name in players:
                            players[player_name]["pltfm_id"] = pltfm_id
                    
                    break

        last_processed_position = file.tell()

    online_count = sum(1 for player in players.values() if player["status"] != "Offline")

    return {
        "online_count": online_count,
        "players": players,
        "last_processed_position": last_processed_position,
        "last_processed_file": file_path,
        "last_timestamp": last_timestamp,
        "new_lines_processed": new_lines_processed
    }

def load_data(data_file):
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            data = json.load(f)
        if isinstance(data.get('last_timestamp'), str):
            data['last_timestamp'] = datetime.strptime(data['last_timestamp'], '%Y-%m-%dT%H:%M:%S')
        return data
    return {}

def save_data(data_file, data):
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2, default=datetime_to_string)

def main():
    data_file = 'Webserver_player_status.json'
    while True:
        latest_log_file = get_path_latest_game_server_log_file.get_path_latest_game_server_log_file()
        data = load_data(data_file)
        
        result = process_log_file(latest_log_file, data)
        
        if result['new_lines_processed'] > 0:
            print(json.dumps(result, indent=2, default=datetime_to_string))
            
            # Save all data to Webserver_player_status.json
            save_data(data_file, {
                "online_count": result['online_count'],
                "players": result['players'],
                "last_processed_position": result['last_processed_position'],
                "last_processed_file": result['last_processed_file'],
                "last_timestamp": result['last_timestamp']
            })
        else:
            print("No new lines to process.")
        
        time.sleep(3)

if __name__ == "__main__":
    main()