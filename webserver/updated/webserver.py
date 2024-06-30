from http.server import HTTPServer, BaseHTTPRequestHandler, ThreadingHTTPServer

def lookup():
    
    import time
    while True:
        print("Synchronizing data with the server.")
        global game_server
        import get_steam_game_server_data as game_server
        time.sleep(5)

class RedirectHandler(BaseHTTPRequestHandler):
    global game_server

    def do_GET(self):
        if self.path == '/data_test':

            # ServerLoginConfirmationText ServerWebsiteURL
            html_content = f"""
            {game_server["GameHost"]}<br>
            {game_server["ServerDescription"]}<br>
            
            {game_server["IP"]}<br>
            {game_server["Port"]}
            {game_server["ServerVersion"]}<br>
            {game_server["Region"]}<br>
            {game_server["LevelName"]}<br>
            {game_server["WorldSize"]}<br>

            {game_server["CurrentPlayers"]}<br>
            
            test
            """

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            self.wfile.write(html_content.encode('utf-8'))
              
        if self.path == '/data':                 
            data = game_server
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # Allow requests from any origin
            self.send_header('Access-Control-Allow-Methods', 'GET')
            self.send_header('Access-Control-Allow-Headers', 'Content-type')
            self.end_headers()

            import json
            self.wfile.write(json.dumps(data).encode())  # Encode data as JSON                    

# Function to run the HTTP server
def run(server_class=ThreadingHTTPServer, handler_class=RedirectHandler, port=80, ip='',):
    server_address = (ip, port)
    httpd = server_class(server_address, handler_class)
    print('Server started at localhost:' + str(port))
    httpd.serve_forever()

if __name__ == '__main__':
    import threading
    lookup_thread = threading.Thread(target=lookup, daemon = True).start()
    server_thread = threading.Thread(target=run, daemon = True).start()

    import close_threads_signaling    
    import keep_main_thread_alive