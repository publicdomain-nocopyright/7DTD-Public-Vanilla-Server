import os
import time
import re
import json
import logging
from datetime import datetime
from collections import defaultdict

# Set up logging
logging.basicConfig(filename='log_parser.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

#def get_latest_log_file():
#    script_dir = os.path.dirname(os.path.abspath(__file__))
#    log_dir = os.path.abspath(os.path.join(script_dir, '..', '7DaysToDie_Data'))
#    log_files = [f for f in os.listdir(log_dir) if f.startswith("output_log__") and f.endswith(".txt")]
#    
#    if not log_files:
#        logger.error(f"No log files found in the directory: {log_dir}")
#        raise FileNotFoundError(f"No log files found in the directory: {log_dir}")
#    
#    sorted_log_files = sorted(log_files, key=lambda x: x.split('__')[1], reverse=True)
#    latest_file = os.path.join(log_dir, sorted_log_files[0])
#    
#    logger.debug(f"Latest log file found: {latest_file}")
#    return latest_file

def get_latest_log_file():
    import Webserver_Get_Latest_Game_Server_Log_File
    log_file_path = Webserver_Get_Latest_Game_Server_Log_File.get_latest_game_server_log_file_name()
    return log_file_path

def parse_log_line(line):
    pltfm_id_match = re.search(r"PltfmId='(\w+_\d+)'", line)
    pltfm_id = pltfm_id_match.group(1) if pltfm_id_match else None

    patterns = [
        (r"PlayerLogin: (.+?)/V", "Online,Joining"),
        (r"PlayerSpawnedInWorld.*PlayerName='(.+?)'", "Online,Spawned"),
        (r"GMSG: Player '(.+?)' joined the game", "Online,Playing"),
        (r"GMSG: Player '(.+?)' left the game", "Offline"),
        (r"Player disconnected: EntityID=.*PlayerName='(.+?)'", "Offline"),
        (r"\[Auth\].*PlayerName='(.+?)'", None),
        (r"INF.*PlayerName='(.+?)'", None),
    ]

    for pattern, status in patterns:
        match = re.search(pattern, line)
        if match:
            player = match.group(1)
            logger.debug(f"Player '{player}' detected with status: {status}")
            return player, status, pltfm_id

    if "Shutdown game from" in line:
        logger.info("Server is shutting down")
        return "SERVER", "Shutdown", None

    return None, None, pltfm_id

def generate_json(player_status, force_create=False):
    if player_status["SERVER"]["status"] == "Shutdown":
        data = {
            "online_count": 0,
            "players": {},
            "server_status": "Offline"
        }
    else:
        online_players = {player: info for player, info in player_status.items() 
                          if info["status"].startswith("Online") and player != "SERVER"}
        online_count = len(online_players)

        data = {
            "online_count": online_count,
            "players": online_players,
            "server_status": player_status.get("SERVER", {}).get("status", "Online")
        }

    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dir, "Webserver_player_status.json")

    if force_create or not os.path.exists(json_file):
        logger.info(f"Creating new player_status.json file")
    else:
        logger.info(f"Updating player_status.json file")
    
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    
    logger.debug(f"Current player status: {dict(player_status)}")
    logger.debug(f"Online count: {data['online_count']}")
    logger.debug(f"JSON data: {json.dumps(data, indent=2)}")

def follow(file_path):
    with open(file_path, "r", encoding="utf-8", errors='ignore') as file:
        file.seek(0, 2)
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.1)
                yield None
            else:
                yield line

def initialize_player_status(log_file):
    player_status = defaultdict(lambda: {"status": "Offline", "pltfm_id": None})
    player_status["SERVER"] = {"status": "Online", "pltfm_id": None}

    logger.info(f"Initializing player status from log file: {log_file}")
    with open(log_file, "r", encoding="utf-8", errors='ignore') as file:
        for line in file:
            player, status, pltfm_id = parse_log_line(line)
            if player:
                if status:
                    player_status[player]["status"] = status
                if pltfm_id:
                    player_status[player]["pltfm_id"] = pltfm_id

    logger.debug(f"Initial player status: {dict(player_status)}")
    return player_status

def print_full_status(player_status):
    status_report = "\nFull Player Status Report:"
    for player, info in player_status.items():
        status_report += f"\n  {player}: {info['status']} (PltfmId: {info['pltfm_id']})"
    logger.info(status_report)

def main():
    try:
        import Webserver_Get_Latest_Game_Server_Log_File
        log_file_path = Webserver_Get_Latest_Game_Server_Log_File.get_latest_game_server_log_file_name()
        current_log_file = log_file_path
        player_status = initialize_player_status(current_log_file)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_file = os.path.join(script_dir, "Webserver_player_status.json")
        if not os.path.exists(json_file):
            logger.info("player_status.json not found. Creating new file with refreshed data.")
            generate_json(player_status, force_create=True)
        else:
            logger.info("player_status.json found. Updating with current data.")
            generate_json(player_status)

        logger.info("Starting to monitor log file in real-time...")
        last_check_time = time.time()
        line_count = 0

        for line in follow(current_log_file):
            line_count += 1
            if line_count % 1000 == 0:
                logger.info(f"Processed {line_count} lines")
                print_full_status(player_status)

            if time.time() - last_check_time > 60:
                try:
                    latest_file = get_latest_log_file()
                    if latest_file != current_log_file:
                        logger.info(f"Switching to newer log file: {latest_file}")
                        current_log_file = latest_file
                        player_status = initialize_player_status(current_log_file)
                        generate_json(player_status)
                except FileNotFoundError as e:
                    logger.warning(f"{e}. Will continue with the current file.")
                last_check_time = time.time()

            if line is None:
                continue

            player, status, pltfm_id = parse_log_line(line)
            if player:
                update_needed = False
                if player not in player_status:
                    logger.info(f"New player '{player}' added to tracking")
                    update_needed = True
                if status:
                    old_status = player_status[player]["status"]
                    player_status[player]["status"] = status
                    if old_status != status:
                        logger.info(f"Player/Server '{player}' status changed from {old_status} to {status}")
                        update_needed = True
                        if player == "SERVER" and status == "Shutdown":
                            for p in player_status:
                                if p != "SERVER":
                                    player_status[p]["status"] = "Offline"
                if pltfm_id and player_status[player]["pltfm_id"] != pltfm_id:
                    player_status[player]["pltfm_id"] = pltfm_id
                    logger.info(f"Updated PltfmId for player '{player}': {pltfm_id}")
                    update_needed = True
                
                if update_needed:
                    generate_json(player_status)

            if player_status["SERVER"]["status"] == "Shutdown":
                logger.info("Server has shut down. Stopping monitoring.")
                generate_json(player_status)  # Generate empty JSON on shutdown
                return

    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user.")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
    finally:
        logger.info("Generating final JSON report.")
        generate_json(player_status)

if __name__ == "__main__":
    logger.info("Script started.")
    main()
    logger.info("Script ended.")