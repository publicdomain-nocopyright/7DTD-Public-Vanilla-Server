from http.server import HTTPServer, BaseHTTPRequestHandler, ThreadingHTTPServer
import threading
import time
import json

def lookup():
    import get_steam_game_server_data
    while True:
        try:
            print("[Webserver] [a2s] Synchronizing data with the server.")
            global game_server
            game_server = get_steam_game_server_data()
        except Exception as e:
            print(f"[Error] Exception in lookup thread: {e}")
        time.sleep(5)

class RedirectHandler(BaseHTTPRequestHandler):
    global game_server

    def do_GET(self):
        try:
            if self.path == '/data_test':
                html_content = f"""
                <style>
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
                    async function fetchData() {{
                        try {{
                            const response = await fetch('/data');
                            const data = await response.json();
                            for (const [key, value] of Object.entries(data)) {{
                                let element = document.getElementById(`html${{key}}`);
                                if (element) {{
                                    element.classList.add('fade-in');
                                    setTimeout(() => {{
                                        element.innerText = value;
                                        element.classList.remove('fade-in');
                                    }}, 500);
                                }}
                            }}
                        }} catch (error) {{
                            console.error('Error fetching data:', error);
                        }} finally {{
                            setTimeout(fetchData, 5000);
                        }}
                    }}
                    fetchData();
                </script>
                test
                """
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
            
            elif self.path == '/data':
                data = game_server
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET')
                self.send_header('Access-Control-Allow-Headers', 'Content-type')
                self.end_headers()
                self.wfile.write(json.dumps(data).encode())
        except Exception as e:
            print(f"[Error] Exception in request handler: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'Internal Server Error')

def run(server_class=ThreadingHTTPServer, handler_class=RedirectHandler, port=80, sslport=443, ip=''):
    server_address = (ip, port)
    httpd = server_class(server_address, handler_class)
    print('[Webserver] Server started at localhost:' + str(port))
    httpd.serve_forever()

if __name__ == '__main__':
    try:
        lookup_thread = threading.Thread(target=lookup, daemon=True)
        lookup_thread.start()
        server_thread = threading.Thread(target=run, daemon=True)
        server_thread.start()
        lookup_thread.join()
        server_thread.join()
    except Exception as e:
        print(f"[Error] Exception in main thread: {e}")
    finally:
        print("[Webserver] Main thread exiting.")
