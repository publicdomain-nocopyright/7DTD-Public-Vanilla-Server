from http.server import HTTPServer, BaseHTTPRequestHandler, ThreadingHTTPServer

def lookup():
    import time
    import get_steam_game_server_data
    while True:
        print("[Webserver] [a2s] Synchronizing data with the server.")
        global game_server
        game_server = get_steam_game_server_data()        
        time.sleep(5)

class RedirectHandler(BaseHTTPRequestHandler):
    global game_server

    def do_GET(self):
        if self.path == '/data_test':

            # ServerLoginConfirmationText ServerWebsiteURL
            html_content = f"""

            <style>
                /* CSS animation for fading in new data */
                @keyframes fadeIn {{
                    from {{ opacity: 0; }}
                    to {{ opacity: 1; }}
                }}
                .fade-in {{
                    animation: fadeIn 0.5s ease-in-out;
                }}
            </style>
            {game_server["GameHost"]}<br>
            {game_server["ServerDescription"]}<br>
            
            {game_server["IP"]}<br>
            {game_server["Port"]}
            {game_server["ServerVersion"]}<br>
            {game_server["Region"]}<br>
            {game_server["LevelName"]}<br>
            {game_server["WorldSize"]}<br>

            <p id="htmlCurrentPlayers">{game_server["CurrentPlayers"]}</p>
            <p id="htmlCurrentServerTime">{game_server["CurrentServerTime"]}</p>
            
            <script>
            function fetchData() {{
                fetch('/data')
                    .then(response => response.json())
                    .then(data => {{
                        console.log(data)

                    Object.keys(data).forEach(key => {{
                        let id = 'html' + key;
                        let element = document.getElementById(id);
                        
                        if (element) {{
                        // Apply fade-in animation
                        element.classList.add('fade-in');
                        setTimeout(() => {{
                            element.innerText = data[key];
                            element.classList.remove('fade-in');
                        }}, 500); // Adjust delay as needed for animation to complete
                    }}

                    }});

                    }})
                    .catch(error => console.error('Error fetching data:', error))
                    .finally(() => {{
                        setTimeout(fetchData, 5000); // 5000 milliseconds = 5 seconds
                    }});
            }}
            fetchData();
            </script>
            
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
def run(server_class=ThreadingHTTPServer, handler_class=RedirectHandler, port=80, sslport=443, ip='',):
    server_address = (ip, port)
    httpd = server_class(server_address, handler_class)

    #import ssl_verification
    #httpd = ssl_verification.enable_ssl(httpd, server_address)
    
    print('[Webserver] Server started at localhost:' + str(port))
    httpd.serve_forever()

if __name__ == '__main__':
    import threading
    lookup_thread = threading.Thread(target=lookup, daemon = True).start()
    server_thread = threading.Thread(target=run, daemon = True).start()

    import close_threads_signaling    
    import keep_main_thread_alive