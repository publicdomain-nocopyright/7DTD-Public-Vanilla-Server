import re
import json
import time
from datetime import datetime
import os
import get_path_latest_game_server_log_file


import logging
import traceback
# Set up logging
logging.basicConfig(filename='chat_processor_errors.log', level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



def datetime_to_string(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def load_player_status():
    while True:
        if os.path.exists('Webserver_player_status.json'):
            with open('Webserver_player_status.json', 'r') as f:
                return json.load(f)
        else:
            print("Waiting for Webserver_player_status.json to be created...")
            time.sleep(5)  # Wait for 5 seconds before checking again

def get_player_name(pltfm_id, player_status):
    for player_name, player_info in player_status['players'].items():
        if player_info['pltfm_id'] == pltfm_id:
            return player_name
    return pltfm_id  # Return pltfm_id if no matching player name is found

def get_machine_timezone_offset():
    from datetime import datetime
    import time

    offset_seconds = time.timezone if time.localtime().tm_isdst == 0 else time.altzone
    offset_hours = offset_seconds / 3600
    current_time_zone_offset = f'{offset_hours:+.0f}:00'
    return current_time_zone_offset

def process_log_file(file_path, data, player_status):
    chat_messages = data.get('chat_messages', [])
    last_processed_position = data.get('last_processed_position', 0)
    last_processed_file = data.get('last_processed_file', '')
    last_timestamp = data.get('last_timestamp')

    chat_pattern = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).*Chat \(from '(.+?)', entity id '(\d+)', to '(.+?)'\): (.+)"

    if last_processed_file != file_path:
        last_processed_position = 0
        print(f"New log file detected. Processing from the beginning: {file_path}")

    with open(file_path, 'r') as file:
        file.seek(last_processed_position)
        new_lines_processed = 0

        for line in file:
            new_lines_processed += 1
            match = re.search(chat_pattern, line)
            if match:
                timestamp, pltfm_id, entity_id, chat_type, message = match.groups()
                player_name = get_player_name(pltfm_id, player_status)
                chat_messages.append({
                    'machine_timezone_offset': get_machine_timezone_offset(),
                    'timestamp': datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S'),
                    'pltfm_id': pltfm_id,
                    'player_name': player_name,
                    'entity_id': entity_id,
                    'chat_type': chat_type,
                    'message': message
                })
                last_timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')

        last_processed_position = file.tell()

    return {
        'chat_messages': chat_messages,
        'last_processed_position': last_processed_position,
        'last_processed_file': file_path,
        'last_timestamp': last_timestamp,
        'new_lines_processed': new_lines_processed
    }

def load_data(data_file):
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            data = json.load(f)
        for message in data.get('chat_messages', []):
            message['timestamp'] = datetime.strptime(message['timestamp'], '%Y-%m-%dT%H:%M:%S')
        if isinstance(data.get('last_timestamp'), str):
            data['last_timestamp'] = datetime.strptime(data['last_timestamp'], '%Y-%m-%dT%H:%M:%S')
        return data
    return {}

def save_data(data_file, data):
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2, default=datetime_to_string)

def analyze_chat(chat_messages):
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

    return {
        'total_messages': len(chat_messages),
        'unique_players': len(player_message_counts),
        'most_active_player': most_active_player,
        'chat_types': list(chat_types),
        'most_common_words': most_common_words
    }

def main():
    data_file = 'Webserver_chat_message_processor.json'
    
    while True:
        latest_log_file = get_path_latest_game_server_log_file.get_path_latest_game_server_log_file()
        data = load_data(data_file)
        player_status = load_player_status()
        
        result = process_log_file(latest_log_file, data, player_status)
        
        if result['new_lines_processed'] > 0:
            print(f"Processed {result['new_lines_processed']} new lines.")
            
            analysis = analyze_chat(result['chat_messages'])
            print("Chat Analysis:")
            print(json.dumps(analysis, indent=2))
            
            # Save all data to chat_analysis.json
            save_data(data_file, {
                'chat_messages': result['chat_messages'],
                'last_processed_position': result['last_processed_position'],
                'last_processed_file': result['last_processed_file'],
                'last_timestamp': result['last_timestamp'],
                'analysis': analysis
            })
        else:
            print("No new lines to process.")
        
        time.sleep(3)  # Check for new messages every 3 seconds

if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        logging.error(f"Fatal error in main script: {str(e)}")
        logging.error(traceback.format_exc())
        print(f"A fatal error occurred. Check the log file for details.")