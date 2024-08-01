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
    login_match = re.search(r"PlayerLogin: (\w+)/V", line)
    if login_match:
        player = login_match.group(1)
        print(f"Debug: Player '{player}' is logging in")
        return player, "Online,Joining"
    
    spawn_match = re.search(r"PlayerSpawnedInWorld.*PlayerName='(\w+)'", line)
    if spawn_match:
        player = spawn_match.group(1)
        print(f"Debug: Player '{player}' has spawned in the world")
        return player, "Online,Spawned"
    
    join_match = re.search(r"GMSG: Player '(\w+)' joined the game", line)
    if join_match:
        player = join_match.group(1)
        print(f"Debug: Player '{player}' has fully joined the game")
        return player, "Online,Playing"
    
    leave_match = re.search(r"GMSG: Player '(\w+)' left the game", line)
    if leave_match:
        player = leave_match.group(1)
        print(f"Debug: Player '{player}' left the game")
        return player, "Offline"
    
    disconnect_match = re.search(r"Player disconnected: EntityID=.*PlayerName='(\w+)'", line)
    if disconnect_match:
        player = disconnect_match.group(1)
        print(f"Debug: Player '{player}' disconnected")
        return player, "Offline"
    
    shutdown_match = re.search(r"Shutdown game from", line)
    if shutdown_match:
        print("Debug: Server is shutting down")
        return "SERVER", "Shutdown"
    
    return None, None

def generate_json(player_status):
    online_players = {player: status for player, status in player_status.items() 
                      if status.startswith("Online") and player != "SERVER"}
    online_count = len(online_players)
    
    data = {
        "online_count": online_count,
        "players": online_players,
        "server_status": player_status.get("SERVER", "Online")
    }
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dir, "player_status.json")
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

def main():
    player_status = defaultdict(lambda: "Offline")
    player_status["SERVER"] = "Online"
    print("Debug: Starting to monitor log file...")
    
    try:
        current_log_file = get_latest_log_file()
        last_check_time = time.time()
        
        while True:
            for line in follow(current_log_file):
                # Check for new log file every 60 seconds
                if time.time() - last_check_time > 60:
                    try:
                        latest_file = get_latest_log_file()
                        if latest_file != current_log_file:
                            print(f"Debug: Switching to newer log file: {latest_file}")
                            current_log_file = latest_file
                            break  # Exit the for loop to start following the new file
                    except FileNotFoundError as e:
                        print(f"Warning: {e}. Will continue with the current file.")
                    last_check_time = time.time()
                
                if line is None:
                    continue
                
                player, status = parse_log_line(line)
                if player:
                    old_status = player_status[player]
                    player_status[player] = status
                    if old_status != status:
                        print(f"Debug: Player/Server '{player}' status changed from {old_status} to {status}")
                        if player == "SERVER" and status == "Shutdown":
                            # Set all players to offline when server shuts down
                            for p in player_status:
                                if p != "SERVER":
                                    player_status[p] = "Offline"
                        generate_json(player_status)
                    else:
                        print(f"Debug: Player/Server '{player}' status unchanged ({status})")
                
                if player_status["SERVER"] == "Shutdown":
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