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

def process_log_file(file_path, checkpoint):
    players = checkpoint.get('players', {})
    last_processed_position = checkpoint.get('last_processed_position', 0)
    last_processed_file = checkpoint.get('last_processed_file', '')
    last_timestamp = checkpoint.get('last_timestamp')

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
                            players[player_name] = players.get(player_name, {"name": player_name})
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

def load_checkpoint(checkpoint_file):
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            checkpoint = json.load(f)
        if isinstance(checkpoint.get('last_timestamp'), str):
            checkpoint['last_timestamp'] = datetime.strptime(checkpoint['last_timestamp'], '%Y-%m-%dT%H:%M:%S')
        return checkpoint
    return {}

def save_checkpoint(checkpoint_file, checkpoint):
    with open(checkpoint_file, 'w') as f:
        json.dump(checkpoint, f, indent=2, default=datetime_to_string)

def main():
    checkpoint_file = 'log_processing_checkpoint.json'
    while True:
        latest_log_file = get_path_latest_game_server_log_file.get_path_latest_game_server_log_file()
        checkpoint = load_checkpoint(checkpoint_file)
        
        result = process_log_file(latest_log_file, checkpoint)
        
        if result['new_lines_processed'] > 0:
            print(json.dumps(result, indent=2, default=datetime_to_string))
            with open('Webserver_player_status.json', 'w') as json_file:
                json.dump(result['players'], json_file, indent=2, default=datetime_to_string)
            
            save_checkpoint(checkpoint_file, {
                'players': result['players'],
                'last_processed_position': result['last_processed_position'],
                'last_processed_file': result['last_processed_file'],
                'last_timestamp': result['last_timestamp']
            })
        else:
            print("No new lines to process.")
        
        time.sleep(3)

if __name__ == "__main__":
    main()