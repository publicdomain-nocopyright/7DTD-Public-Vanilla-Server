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
                chat_messages.append({
                    'timestamp': datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S'),
                    'pltfm_id': pltfm_id,
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
        player = message['pltfm_id']
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
    data_file = 'chat_analysis.json'
    
    while True:
        latest_log_file = get_path_latest_game_server_log_file.get_path_latest_game_server_log_file()
        data = load_data(data_file)
        
        result = process_log_file(latest_log_file, data)
        
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
    main()