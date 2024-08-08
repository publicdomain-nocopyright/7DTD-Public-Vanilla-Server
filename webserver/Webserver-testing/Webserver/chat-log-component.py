import os
import glob
from datetime import datetime
import time
import re
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

def get_latest_game_server_log_file_name():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_directory = os.path.join(script_dir, '../7DaysToDie_Data')
    file_pattern = 'output_log__*.txt'
    log_files = glob.glob(os.path.join(log_directory, file_pattern))

    print(f"Looking for log files in: {log_directory}")  # Debug print
    print(f"Found {len(log_files)} log files")  # Debug print

    if not log_files:
        print("No log files found. Check the log directory path.")
        return None

    def extract_timestamp(filename):
        timestamp_str = filename.split('__')[1] + "__" + filename.split('__')[2]
        return datetime.strptime(timestamp_str, '%Y-%m-%d__%H-%M-%S.txt')

    log_files.sort(key=extract_timestamp, reverse=True)
    latest_file = log_files[0] if log_files else None
    print(f"Latest log file: {latest_file}")  # Debug print
    return latest_file

def parse_chat_messages(log_file):
    chat_messages = []
    chat_pattern = re.compile(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).*Chat \(from \'.*\', entity id \'.*\', to \'.*\'\): (.*?): (.*)')

    try:
        with open(log_file, 'r', encoding='utf-8') as file:
            for line in file:
                match = chat_pattern.search(line)
                if match:
                    timestamp, username, message = match.groups()
                    chat_messages.append({
                        'timestamp': timestamp,
                        'username': username,
                        'message': message
                    })
    except Exception as e:
        print(f"Error reading log file: {e}")
        return []

    print(f"Found {len(chat_messages)} chat messages in the log file")  # Debug print
    return chat_messages

class ChatLogHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html_content = self.get_html_content()
            self.wfile.write(html_content.encode())
        elif self.path == '/get_chat_messages':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            latest_log_file = get_latest_game_server_log_file_name()
            if latest_log_file:
                chat_messages = parse_chat_messages(latest_log_file)
                self.wfile.write(json.dumps(chat_messages).encode())
            else:
                self.wfile.write(json.dumps([]).encode())
        else:
            super().do_GET()

    def get_html_content(self):
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>7 Days to Die Chat Log</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
        #chat-container { width: 300px; height: 400px; border: 1px solid #ccc; overflow-y: auto; padding: 10px; }
        .chat-message { margin-bottom: 10px; }
        .username { font-weight: bold; }
        .timestamp { font-size: 0.8em; color: #888; }
    </style>
</head>
<body>
    <div id="chat-container"></div>
    <div id="debug-info"></div>

    <script>
        // ... (rest of the JavaScript code remains the same)
    </script>
</body>
</html>
        """

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, ChatLogHandler)
    print('Server running on port 8000...')
    httpd.serve_forever()