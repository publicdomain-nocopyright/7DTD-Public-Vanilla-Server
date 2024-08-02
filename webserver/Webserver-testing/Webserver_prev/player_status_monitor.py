import os
import time
import re
import json
from datetime import datetime
from collections import defaultdict

def get_latest_log_file():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.abspath(os.path.join(script_dir, '..','7DaysToDie_Data'))
    log_files = [f for f in os.listdir(log_dir) if f.startswith("output_log__") and f.endswith(".txt")]
    if not log_files:
        raise FileNotFoundError(f"No log files found in the directory: {log_dir}")
    latest_file = os.path.join(log_dir, max(log_files, key=lambda x: os.path.getmtime(os.path.join(log_dir, x))))
    print(f"Debug: Latest log file found: {latest_file}")
    return latest_file

def parse_log_line(line):
    # Generic pattern to capture PltfmId
    pltfm_id_match = re.search(r"PltfmId='(\w+_\d+)'", line)
    pltfm_id = pltfm_id_match.group(1) if pltfm_id_match else None

    login_match = re.search(r"PlayerLogin: (\w+)/V", line)
    if login_match:
        player = login_match.group(1)
        print(f"Debug: Player '{player}' is logging in")
        return player, "Online,Joining", pltfm_id

    spawn_match = re.search(r"PlayerSpawnedInWorld.*PlayerName='(\w+)'", line)
    if spawn_match:
        player = spawn_match.group(1)
        print(f"Debug: Player '{player}' has spawned in the world")
        return player, "Online,Spawned", pltfm_id

    join_match = re.search(r"GMSG: Player '(\w+)' joined the game", line)
    if join_match:
        player = join_match.group(1)
        print(f"Debug: Player '{player}' has fully joined the game")
        return player, "Online,Playing", pltfm_id

    leave_match = re.search(r"GMSG: Player '(\w+)' left the game", line)
    if leave_match:
        player = leave_match.group(1)
        print(f"Debug: Player '{player}' left the game")
        return player, "Offline", pltfm_id

    disconnect_match = re.search(r"Player disconnected: EntityID=.*PlayerName='(\w+)'", line)
    if disconnect_match:
        player = disconnect_match.group(1)
        print(f"Debug: Player '{player}' disconnected")
        return player, "Offline", pltfm_id

    auth_match = re.search(r"\[Auth\].*PlayerName='(\w+)'", line)
    if auth_match:
        player = auth_match.group(1)
        print(f"Debug: Player '{player}' authentication info found")
        return player, None, pltfm_id

    shutdown_match = re.search(r"Shutdown game from", line)
    if shutdown_match:
        print("Debug: Server is shutting down")
        return "SERVER", "Shutdown", None

    return None, None, pltfm_id

def generate_json(player_status, force_create=False):
    online_players = {player: info for player, info in player_status.items() 
                      if info["status"].startswith("Online") and player != "SERVER"}
    online_count = len(online_players)

    data = {
        "online_count": online_count,
        "players": online_players,
        "server_status": player_status.get("SERVER", {}).get("status", "Online")
    }

    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dir, "player_status.json")

    if force_create or not os.path.exists(json_file):
        print(f"Debug: Creating new player_status.json file")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Debug: New JSON file created: {json_file}")
    else:
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Debug: JSON file updated: {json_file}")

    print(f"Debug: Current player status: {player_status}")
    print(f"Debug: Online count: {online_count}")
    print(f"Debug: JSON data: {json.dumps(data, indent=2)}")

def follow(file_path):
    with open(file_path, "r", encoding="utf-8", errors='ignore') as file:
        file.seek(0, 2)  # Go to the end of the file
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.1)  # Sleep briefly before checking again
                yield None  # Yield None to indicate no new line
            else:
                yield line

def initialize_player_status(log_file):
    player_status = defaultdict(lambda: {"status": "Offline", "pltfm_id": None})
    player_status["SERVER"] = {"status": "Online", "pltfm_id": None}

    print(f"Debug: Initializing player status from log file: {log_file}")
    with open(log_file, "r", encoding="utf-8", errors='ignore') as file:
        for line in file:
            player, status, pltfm_id = parse_log_line(line)
            if player:
                if status:
                    player_status[player]["status"] = status
                if pltfm_id:
                    player_status[player]["pltfm_id"] = pltfm_id

    print(f"Debug: Initial player status: {dict(player_status)}")
    return player_status

def main():
    try:
        current_log_file = get_latest_log_file()
        player_status = initialize_player_status(current_log_file)

        # Check if player_status.json exists, create it if it doesn't
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_file = os.path.join(script_dir, "player_status.json")
        if not os.path.exists(json_file):
            print("Debug: player_status.json not found. Creating new file with refreshed data.")
            generate_json(player_status, force_create=True)
        else:
            print("Debug: player_status.json found. Updating with current data.")
            generate_json(player_status)

        print("Debug: Starting to monitor log file in real-time...")
        last_check_time = time.time()

        for line in follow(current_log_file):
            # Check for new log file every 60 seconds
            if time.time() - last_check_time > 60:
                try:
                    latest_file = get_latest_log_file()
                    if latest_file != current_log_file:
                        print(f"Debug: Switching to newer log file: {latest_file}")
                        current_log_file = latest_file
                        player_status = initialize_player_status(current_log_file)
                        generate_json(player_status)
                except FileNotFoundError as e:
                    print(f"Warning: {e}. Will continue with the current file.")
                last_check_time = time.time()

            if line is None:
                continue

            player, status, pltfm_id = parse_log_line(line)
            if player:
                update_needed = False
                if status:
                    old_status = player_status[player]["status"]
                    player_status[player]["status"] = status
                    if old_status != status:
                        print(f"Debug: Player/Server '{player}' status changed from {old_status} to {status}")
                        update_needed = True
                        if player == "SERVER" and status == "Shutdown":
                            # Set all players to offline when server shuts down
                            for p in player_status:
                                if p != "SERVER":
                                    player_status[p]["status"] = "Offline"
                if pltfm_id and player_status[player]["pltfm_id"] != pltfm_id:
                    player_status[player]["pltfm_id"] = pltfm_id
                    print(f"Debug: Updated PltfmId for player '{player}': {pltfm_id}")
                    update_needed = True
                
                if update_needed:
                    generate_json(player_status)

            if player_status["SERVER"]["status"] == "Shutdown":
                print("Debug: Server has shut down. Stopping monitoring.")
                return

    except KeyboardInterrupt:
        print("Debug: Monitoring stopped by user.")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
    finally:
        print("Debug: Generating final JSON report.")
        generate_json(player_status)

if __name__ == "__main__":
    print("Debug: Script started.")
    main()
    print("Debug: Script ended.")