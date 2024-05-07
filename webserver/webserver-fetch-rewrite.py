import a2s
import time
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

start_time = time.time()  # Record the program start time

last_check_time = last_fetch_time = fetched_time = 0
server_info = {}  # Initialize an empty dictionary to store server info
server_return = None  # Initialize server_return globally

# Function to continuously fetch server info
def fetch_server_info():
    global server_info, last_check_time, last_fetch_time, fetched_time, server_return
    while True:
        try:
            current_time = time.time() - start_time  # Calculate current time since program start
            server_return = a2s.rules(("93.49.104.86", 26900))
            fetched = server_return.get("CurrentServerTime")

            if fetched is not None:
                fetched_time = int(fetched)
                if fetched_time > last_fetch_time:
                    time_diff = current_time - last_check_time
                    print(fetched, " Time difference since last trigger:", time_diff)
                    last_check_time = current_time
                    last_fetch_time = fetched_time

            server_info['fetched'] = fetched
            server_info['time_difference'] = current_time - last_check_time
            time.sleep(1.1)
        except TimeoutError:
            print("Error: Connection timed out while fetching server rules.")

# HTTP request handler
class RedirectHandler(BaseHTTPRequestHandler):
    log_file = open("server_log.txt", "a")  # Open the log file in append mode
    def log_message(self, format, *args):
        self.log_file.write("%s - - [%s] %s\n" %
                            (self.address_string(),
                            self.log_date_time_string(),
                            format % args))
        self.log_file.flush()

    def do_GET(self):
        self.log_message("GET %s", self.path)  # Log the incoming request
        if self.path == '/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # Allow requests from any origin
            self.end_headers()
            if server_return is not None:
                self.wfile.write(json.dumps(server_return).encode())  # Encode data as JSON
            else:
                self.wfile.write(json.dumps({"error": "Server info not available"}).encode())
        elif self.path == '/':
            # Serve HTML page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Read and send the contents of your HTML file
            with open('Access.html', 'rb') as f:
                self.wfile.write(f.read())
# Function to run the HTTP server
def run(server_class=HTTPServer, handler_class=RedirectHandler, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Server started at localhost:' + str(port))
    httpd.serve_forever()

if __name__ == '__main__':
    # Start the fetch_server_info function in a separate thread
    fetch_thread = Thread(target=fetch_server_info)
    fetch_thread.start()

    # Run the HTTP server in the main thread
    run()
