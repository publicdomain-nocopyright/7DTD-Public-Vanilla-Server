import json

def process_chat_messages(input_file, output_file):
    # Read the input JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Get the chat messages
    chat_messages = data['chat_messages']

    # Keep only the last 50 messages
    data['chat_messages'] = chat_messages[-50:]

    # Update the analysis
    data['analysis']['total_messages'] = len(data['chat_messages'])
    unique_players = set(msg['player_name'] for msg in data['chat_messages'])
    data['analysis']['unique_players'] = len(unique_players)

    if data['chat_messages']:
        player_counts = {}
        chat_types = set()
        word_counts = {}

        for msg in data['chat_messages']:
            player = msg['player_name']
            player_counts[player] = player_counts.get(player, 0) + 1
            chat_types.add(msg['chat_type'])
            
            words = msg['message'].lower().split()
            for word in words:
                word_counts[word] = word_counts.get(word, 0) + 1

        data['analysis']['most_active_player'] = max(player_counts, key=player_counts.get)
        data['analysis']['chat_types'] = list(chat_types)
        data['analysis']['most_common_words'] = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    # Write the output JSON file
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Processed file saved as {output_file}")

# Usage
input_file = "Webserver_chat_message_processor.json"
output_file = "Webserver_chat_message_processor_last50messages.json"
process_chat_messages(input_file, output_file)
