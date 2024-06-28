from http.server import HTTPServer, BaseHTTPRequestHandler, ThreadingHTTPServer

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':

            import get_steam_game_server_data
            # TODO: 20 seconds delay requirement 
            game_server = get_steam_game_server_data()

            # # ServerLoginConfirmationText ServerWebsiteURL
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
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')  # Allow requests from any origin
                    self.send_header('Access-Control-Allow-Methods', 'GET')
                    self.send_header('Access-Control-Allow-Headers', 'Content-type')
                    self.end_headers()

# Function to run the HTTP server
def run(server_class=ThreadingHTTPServer, handler_class=RedirectHandler, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Server started at localhost:' + str(port))
    httpd.serve_forever()

if __name__ == '__main__':
    
    # Run the HTTP server in the main thread
    run()
