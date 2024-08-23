# webserver.py          Simple Threading HTTP Server
import sys; sys.dont_write_bytecode = True
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

import Webserver_fix_pythonw_stream_bug
def read_server_log(LOG_FILE_PATH):
    import html
    try:
        with open(LOG_FILE_PATH, 'r', encoding='utf-8') as file:
            log_content = file.read()
        
        # Escape XML content
        log_content = html.escape(log_content)
        
        print(f"Read {len(log_content)} characters from log file")
        return log_content
    except FileNotFoundError:
        print("Log file not found")
        return "Log file not found."
    except Exception as e:
        print(f"Error reading log file: {e}")
        return f"An error occurred: {e}"
class RedirectHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        #html_content = """
        #<head>
        #    <title>Custom Title</title>
        #</head>
        #"""
        #self.wfile.write(html_content.encode('utf-8'))


        if self.path == '/':
            self.send_response(200), self.send_header('Content-type', 'text/html'), self.end_headers()

            #from pathlib import Path
            import Webserver_template_engine

            import Webserver_findNextHordeNightTime_inside_logs_folder
            bloodmoon_days = Webserver_findNextHordeNightTime_inside_logs_folder.find_last_bloodmoon_setday()
            Webserver_IP_ADDRESS = Get_WebServer_Public_IP()
            simple_player_status_component_loaded = Webserver_template_engine.render_template('Page_component_simple_player_status.html')
            chat_log_interface = Webserver_template_engine.render_template('chat-log-interface.html')

            self.wfile.write(bytes(Webserver_template_engine.render_template('Page_index.html'), 'utf-8'))

        elif self.path == '/favicon.ico':
            self.send_response(200), self.send_header('Content-type', 'image/x-icon'), self.end_headers()
            favicon_base64 = (
               """AAABAAEAEBAQAAEABAAoAQAAFgAAACgAAAAQAAAAIAAAAAEABAAAAAAA
               gAAAAAAAAAAAAAAAEAAAAAAAAABXqw4AAAAAAGCuJwBmvSQAtd6YAPHw7ABp
               visAccwuAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAERERERER
               ERERERJndiEREREQd3d3dwERERd3J3d3cRERd3JSd3d3ERF3JVUnd3cRE3dV
               VVJ3dzEXd1V0VSd3cRd3d3dFUndxF3d3d3RVd3ERd3d3d0d3ERF3d3d3d3cR
               ERd3d3d3cREREXd3d3cRERERF3d3cRERERERERERERH//wAA+B8AAOAHAADg
               BwAAwAMAAMADAACAAQAAgAEAAIABAACAAQAAwAMAAMADAADgBwAA8A8AAPgf
               AAD//wAA
               """)
            import base64        
            self.wfile.write(base64.b64decode(favicon_base64))
            
        elif self.path == '/Get_WebServer_Public_IP':
            self.send_response(200), self.send_header('Content-type', 'text/plain'), self.end_headers()
            self.wfile.write(Get_WebServer_Public_IP().encode('utf-8'))

        elif self.path == '/list_paths':
                self.send_response(200), self.send_header('Content-type', 'text/plain'), self.end_headers()
                self.wfile.write(get_self_paths_json(RedirectHandler).encode('utf-8'))




        # In the main handler
        elif self.path == '/server-log':
            import get_path_latest_game_server_log_file
            log_file_path = get_path_latest_game_server_log_file.get_path_latest_game_server_log_file()
            log_content = read_server_log(log_file_path)
            
            formatted_log_content = f"""
            <pre id="log">{log_content}</pre>
            <script>
                window.addEventListener('load', function() {{
                    var logContent = document.getElementById('log');
                    console.log("Log content size in browser:", logContent.textContent.length, "characters");
                    console.log("Last 200 characters:", logContent.textContent.slice(-200));
                    logContent.scrollTop = logContent.scrollHeight;
                }});
            </script>
            """
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-Length', str(len(formatted_log_content)))
            self.end_headers()
            self.wfile.write(bytes(formatted_log_content, "utf8"))            
        elif self.path == '/player_status.json':
            self.send_response(200), self.send_header('Content-type', 'application/json'), self.end_headers()
            import os, json
            file_path = os.path.join(os.path.dirname(__file__), 'Webserver_player_status.json')
            with open(file_path, 'r') as file:
                data = json.load(file)
            self.wfile.write(json.dumps(data).encode('utf-8'))

        elif self.path == '/Page_component_simple-player-status.html':
            import os
            self.send_response(200), self.send_header('Content-type', 'text/html'), self.end_headers()
            file_path = os.path.join(os.path.dirname(__file__), 'Page_component_simple-player-status.html')
            with open(file_path, 'r') as file:
                data = file.read()
            self.wfile.write(data.encode('utf-8'))

        elif self.path == '/Public_IP_Accessibilty':
            import json
            # Webserver Status: Online Offline
            webserver_portforwarding_status = {
                "webserver_status": verify_external_port("78.63.42.224", 80)
            }
            # Convert JSON object to a string
            json_response = json.dumps(webserver_portforwarding_status)
            
            # Set response headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Write the JSON response
            self.wfile.write(json_response.encode('utf-8'))
            pass
        elif self.path == '/current_game_time.json':
                import os
                file_path = os.path.join(os.path.dirname(__file__), '..', 'UserDataFolder', 'Mods', 'World_GameTime', 'current_game_time.json')

                try:
                    with open(file_path, 'r') as file:
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(file.read().encode('utf-8'))
                except FileNotFoundError:
                    self.send_response(404)
                    self.end_headers()

        elif self.path == '/join_game_server':
            self.send_response(302)
            self.send_header('Location', 'steam://connect/' + Webserver_Public_IP + ':26900')
            self.end_headers()
            

        # Enables SimpleHTTPRequestHandler to serve files from current directory
        else:
                # Serve files from the current directory for all other paths
                # Serve only .html files from the current directory for all other paths
            if self.path.endswith('.html') or self.path.endswith('.json'):
                super().do_GET()
            else:
                self.send_error(404, "File not found")



def verify_external_port(external_ip, port, timeout=10):
            
    import socket
    import requests
    """
    Verify if a port is open externally using multiple methods.

    :param external_ip: The external IP address to test
    :param port: The port number to test
    :param timeout: Timeout for connection attempts (default 10 seconds)
    :return: True if the port is open, False otherwise
    """
    if not external_ip:
        print("External IP not available. Provide a valid IP address.")
        return False

    print(f"Verifying if port {port} is open on {external_ip}...")

    # Method 1: Direct socket connection
    try:
        with socket.create_connection((external_ip, port), timeout=timeout) as sock:
            print(f"Successfully connected to {external_ip}:{port}")
            return True
    except (socket.timeout, ConnectionRefusedError):
        print(f"Could not connect directly to {external_ip}:{port}")
    # Method: Using an external port checking service
    import http.client
    import socket

    def check_port(port, external_ip, timeout=10):
        conn = None
        try:
            conn = http.client.HTTPConnection(external_ip, timeout=timeout)
            conn.request("GET", f"/tools/open-ports/check/?port={port}&host={external_ip}")
            response = conn.getresponse()
            body = response.read().decode()

            if "open" in body.lower():
                print(f"External service reports {external_ip}:{port} is open")
                return True
            else:
                print(f"External service reports {external_ip}:{port} is closed")
        except (http.client.HTTPException, socket.error) as e:
            print(f"Error checking port using external service: {e}")
        finally:
            if conn:
                conn.close()

        # If the method fails, consider the port closed
        print(f"Port {port} appears to be closed on {external_ip}")
        return False


# Example usage
#is_open = verify_external_port("8.8.8.8", 80)
#print(f"Port 80 open: {is_open}")

def Get_WebServer_Public_IP():     
        import urllib.request
        webserver_public_ip = urllib.request.urlopen('https://api.ipify.org').read().decode()
        return webserver_public_ip



# Note: ip='localhost' or ip='127.0.0.1' will disallow local network and internet access to the HTTP server.
def start_webserver(server_class=ThreadingHTTPServer, handler_class=RedirectHandler, ip='0.0.0.0', port=80):
    from threading import Thread
    
    server_address = (ip, port)

    def serve(httpd = server_class(server_address, handler_class)): 
        httpd.serve_forever()

    return ip, port, Thread(target=serve, daemon=True).start() 

def inspect_self_paths(handler_class):
    import inspect, re
    paths = []
    for method_name in dir(handler_class):
        if method_name.startswith('do_'):
            method = getattr(handler_class, method_name)
            if callable(method):
                method_source = inspect.getsource(method)
                self_path_matches = re.findall(r'self\.path\s*==\s*[\'"]([^\'"]+)[\'"]', method_source)
                paths.extend(self_path_matches)
    return sorted(set(paths)) 

def list_all_self_paths():
    import inspect, re

    paths = inspect_self_paths(RedirectHandler)
    print("All self.path values:")
    for path in paths:
        print(path)


def get_self_paths_json(handler_class):
    import json
    paths = inspect_self_paths(handler_class)
    return json.dumps({"paths": paths})


def check_port_connectable(host='localhost', port=26900, check_interval=4):
    import socket, time, os
    def check():
        while True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)  # Set a timeout for the connection attempt
            result = sock.connect_ex((host, port))
            if result == 0:
                print(f"Server on port {port} is online.")
            else:
                print(f"Server on port {port} is offline.")
                # Define the full path to the JSON file
                script_dir = os.path.dirname(os.path.abspath(__file__))
                json_file_path = os.path.join(script_dir, 'Webserver_player_status.json')
                # Check if the file exists and remove it if it does
                if os.path.exists(json_file_path):
                    os.remove(json_file_path)
                    print("Webserver_player_status.json has been deleted.")
            sock.close()
            time.sleep(check_interval)
    
    # Start the check function in a separate thread
    Thread(target=check, daemon=True).start()

if __name__ == '__main__':
    global Webserver_Public_IP
    Webserver_Public_IP = Get_WebServer_Public_IP()

    list_all_self_paths()

    from threading import Thread
    import Webserver_player_status_monitor
    Thread(target=Webserver_player_status_monitor.main, daemon=True).start()

    import Webserver_chat_message_processor
    Thread(target=Webserver_chat_message_processor.main, daemon=True).start()

    import portforwarderchecker
    Thread(target=portforwarderchecker.main, daemon=True).start()

    # Start the port connectivity check in a separate thread
    check_port_connectable()

    #from threading import Thread
    #import Webserver_UPNP_Portforwarding
    #Thread(target=Webserver_UPNP_Portforwarding.main, daemon=True).start()

    ip, port, server_thread = start_webserver()
    print(f"[Webserver] Server started at {ip}:{port}")
    import Webserver_exit_threads_signaling
    import Webserver_main_thread_keep_alive
    