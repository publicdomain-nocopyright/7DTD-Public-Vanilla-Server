from http.server import HTTPServer, BaseHTTPRequestHandler, ThreadingHTTPServer

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/data_test':

            import get_steam_game_server_data
            # TODO: 20 seconds delay requirement 
            # TODO: constant fetch on loop as separate thread, to fetch every 20 seconds the server information.
            game_server = get_steam_game_server_data()

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

            import get_steam_game_server_data
            # TODO: 20 seconds delay requirement 
            # TODO: constant fetch on loop as separate thread, to fetch every 20 seconds the server information.
            game_server = get_steam_game_server_data()
                    
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
    httpd.serve_forever()
    print('Server started at localhost:' + str(port))

if __name__ == '__main__':
    # Run the HTTP server in the main thread
    run()
