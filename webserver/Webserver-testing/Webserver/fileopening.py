import re
import json
import time

patterns = [
    (r"PlayerLogin:\s*(.+?)/V", "Online,Joining"),
    (r"PlayerSpawnedInWorld.*PlayerName='(.+?)'", "Online,Spawned"),
    (r"GMSG: Player '(.+?)' joined the game", "Online,Playing"),
    (r"GMSG: Player '(.+?)' left the game", "Offline"),
    (r"Player disconnected: EntityID=.*PlayerName='(.+?)'", "Offline"),
    (r"\[Auth\].*PlayerName='(.+?)'", "Authenticating"),
    (r"INF.*PlayerName='(.+?)'", "Info"),
]

def process_log():
    results = {}
    try:


        import get_path_latest_game_server_log_file
        latest_log_file = get_path_latest_game_server_log_file.get_path_latest_game_server_log_file()
        logfile_content = open(latest_log_file).read()
        print(latest_log_file)
        
        with open(latest_log_file) as log_file:
            logfile_content = log_file.read()
        
        for line in logfile_content.splitlines():
            pltfm_id_match = re.search(r"PltfmId='(\w+_\d+)'", line)
            pltfm_id = pltfm_id_match.group(1) if pltfm_id_match else None

            for pattern, status in patterns:
                match = re.search(pattern, line)
                if match:
                    player_name = match.group(1).strip()
                    if player_name and not player_name.startswith("'"):  # Avoid invalid names
                        key = f"{player_name}_{pltfm_id}" if pltfm_id else player_name
                        if key not in results or status != "Info":  # Prioritize non-Info statuses
                            results[key] = {"name": player_name, "status": status, "pltfm_id": pltfm_id}
        
        # Merge entries for the same player
        final_results = {}
        for key, value in results.items():
            player_name = value['name']
            if player_name in final_results:
                if value['pltfm_id']:
                    final_results[player_name]['pltfm_id'] = value['pltfm_id']
                if value['status'] != "Info":
                    final_results[player_name]['status'] = value['status']
            else:
                final_results[player_name] = value

        with open("player_status.json", "w") as json_file:
            json.dump(final_results, json_file, indent=2)
        print("Updated player_status.json")
    except FileNotFoundError:
        print("Log file not found. Waiting for the next cycle.")
    except Exception as e:
        print(f"An error occurred: {e}")

print("Starting log monitoring. Press Ctrl+C to stop.")
try:
    while True:
        process_log()
        time.sleep(3)
except KeyboardInterrupt:
    print("\nMonitoring stopped.")