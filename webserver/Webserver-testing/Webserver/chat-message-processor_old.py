import re
import json
import time
from datetime import datetime
import os
import get_path_latest_game_server_log_file
import logging

# Set up logging
logging.basicConfig(filename='chat_processor.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def datetime_to_string(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def process_log_file(file_path, data):
    chat_messages = data.get('chat_messages', [])
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

    chat_pattern = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).*Chat \(from '(.+?)', entity id '(\d+)', to '(.+?)'\): (.+)"
    pltfm_id_pattern = r"PlayerLogin: (.+?)/V"
    player_name_pattern = r"PlayerName='(.+?)'"

    if last_processed_file != file_path:
        last_processed_position = 0
        logging.info(f"New log file detected. Processing from the beginning: {file_path}")

    with open(file_path, 'r') as file:
        file.seek(last_processed_position)
        new_lines_processed = 0
        current_pltfm_id = None

        for line in file:
            new_lines_processed += 1
            timestamp_match = re.match(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})', line)
            if timestamp_match:
                current_timestamp = datetime.strptime(timestamp_match.group(1), '%Y-%m-%dT%H:%M:%S')
                last_timestamp = current_timestamp

            pltfm_id_match = re.search(pltfm_id_pattern, line)
            if pltfm_id_match:
                current_pltfm_id = pltfm_id_match.group(1)

            player_name_match = re.search(player_name_pattern, line)
            if player_name_match and current_pltfm_id:
                player_name = player_name_match.group(1)
                players[current_pltfm_id] = players.get(current_pltfm_id, {})
                players[current_pltfm_id]["pltfm_id"] = current_pltfm_id
                players[current_pltfm_id]["name"] = player_name

            for pattern, status in patterns:
                match = re.search(pattern, line)
                if match:
                    player_name = match.group(1)
                    for pltfm_id, player_data in players.items():
                        if player_data.get("name") == player_name:
                            if status:
                                player_data["status"] = status
                                player_data["last_seen"] = current_timestamp
                            break
                    break

            chat_match = re.search(chat_pattern, line)
            if chat_match:
                timestamp, chat_pltfm_id, entity_id, chat_type, message = chat_match.groups()
                player_name = next((data["name"] for data in players.values() if data["pltfm_id"] == chat_pltfm_id), chat_pltfm_id)
                chat_messages.append({
                    'timestamp': datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S'),
                    'player_name': player_name,
                    'pltfm_id': chat_pltfm_id,
                    'entity_id': entity_id,
                    'chat_type': chat_type,
                    'message': message
                })

        last_processed_position = file.tell()

    return {
        'chat_messages': chat_messages,
        'players': players,
        'last_processed_position': last_processed_position,
        'last_processed_file': file_path,
        'last_timestamp': last_timestamp,
        'new_lines_processed': new_lines_processed
    }

def analyze_data(chat_messages, players):
    player_message_counts = {}
    chat_types = set()
    word_frequency = {}

    for message in chat_messages:
        player = message['player_name']
        player_message_counts[player] = player_message_counts.get(player, 0) + 1
        chat_types.add(message['chat_type'])

        words = message['message'].lower().split()
        for word in words:
            word_frequency[word] = word_frequency.get(word, 0) + 1

    most_active_player = max(player_message_counts, key=player_message_counts.get) if player_message_counts else "No messages yet"
    most_common_words = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)[:5]

    online_players = [data["name"] for data in players.values() if data.get('status', '').startswith('Online')]

    return {
        'total_messages': len(chat_messages),
        'unique_players': len(player_message_counts),
        'most_active_player': most_active_player,
        'chat_types': list(chat_types),
        'most_common_words': most_common_words,
        'online_players': online_players,
        'player_count': len(players),
        'online_count': len(online_players)
    }

def analyze_data(chat_messages, players):
    player_message_counts = {}
    chat_types = set()
    word_frequency = {}

    for message in chat_messages:
        player = message['player_name']
        player_message_counts[player] = player_message_counts.get(player, 0) + 1
        chat_types.add(message['chat_type'])

        words = message['message'].lower().split()
        for word in words:
            word_frequency[word] = word_frequency.get(word, 0) + 1

    most_active_player = max(player_message_counts, key=player_message_counts.get) if player_message_counts else "No messages yet"
    most_common_words = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)[:5]

    online_players = [data["name"] for data in players.values() if data.get('status', '').startswith('Online')]

    return {
        'total_messages': len(chat_messages),
        'unique_players': len(player_message_counts),
        'most_active_player': most_active_player,
        'chat_types': list(chat_types),
        'most_common_words': most_common_words,
        'online_players': online_players,
        'player_count': len(players),
        'online_count': len(online_players)
    }

def load_data(data_file):
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            data = json.load(f)
        for message in data.get('chat_messages', []):
            message['timestamp'] = datetime.strptime(message['timestamp'], '%Y-%m-%dT%H:%M:%S')
        for player in data.get('players', {}).values():
            if 'last_seen' in player:
                player['last_seen'] = datetime.strptime(player['last_seen'], '%Y-%m-%dT%H:%M:%S')
        if isinstance(data.get('last_timestamp'), str):
            data['last_timestamp'] = datetime.strptime(data['last_timestamp'], '%Y-%m-%dT%H:%M:%S')
        return data
    return {}

def save_data(data_file, data):
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2, default=datetime_to_string)

def analyze_data(chat_messages, players):
    player_message_counts = {}
    chat_types = set()
    word_frequency = {}

    for message in chat_messages:
        player = message['player_name']
        player_message_counts[player] = player_message_counts.get(player, 0) + 1
        chat_types.add(message['chat_type'])

        words = message['message'].lower().split()
        for word in words:
            word_frequency[word] = word_frequency.get(word, 0) + 1

    most_active_player = max(player_message_counts, key=player_message_counts.get) if player_message_counts else "No messages yet"
    most_common_words = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)[:5]

    online_players = [data.get("name", pltfm_id) for pltfm_id, data in players.items() if data.get('status', '').startswith('Online')]

    return {
        'total_messages': len(chat_messages),
        'unique_players': len(player_message_counts),
        'most_active_player': most_active_player,
        'chat_types': list(chat_types),
        'most_common_words': most_common_words,
        'online_players': online_players,
        'player_count': len(players),
        'online_count': len(online_players)
    }

def main():
    data_file = 'chat_analysis.json'
    
    while True:
        try:
            latest_log_file = get_path_latest_game_server_log_file.get_path_latest_game_server_log_file()
            data = load_data(data_file)
            
            result = process_log_file(latest_log_file, data)
            
            if result['new_lines_processed'] > 0:
                logging.info(f"Processed {result['new_lines_processed']} new lines.")
                
                analysis = analyze_data(result['chat_messages'], result['players'])
                logging.info("Data Analysis:\n" + json.dumps(analysis, indent=2, default=datetime_to_string))
                
                # Save all data to chat_analysis.json
                save_data(data_file, {
                    'chat_messages': result['chat_messages'],
                    'players': result['players'],
                    'last_processed_position': result['last_processed_position'],
                    'last_processed_file': result['last_processed_file'],
                    'last_timestamp': result['last_timestamp'],
                    'analysis': analysis
                })
            else:
                logging.info("No new lines to process.")
            
            time.sleep(3)  # Check for new messages every 3 seconds
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}", exc_info=True)
            time.sleep(10)  # Wait a bit longer before retrying if there's an error

if __name__ == "__main__":
    main()