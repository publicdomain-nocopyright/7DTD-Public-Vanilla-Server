# webserver.py          Simple Threading HTTP Server
import sys; sys.dont_write_bytecode = True
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

import Webserver_fix_pythonw_stream_bug

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

        elif self.path == '/server-log':
            
            # Assuming Webserver_Get_Latest_Game_Server_Log_File.get_latest_game_server_log_file_name() returns the log file path
            import get_path_latest_game_server_log_file
            import Webserver_get_latest_game_server_log_file
            log_file_path = latest_log_file = get_path_latest_game_server_log_file.get_path_latest_game_server_log_file()
            log_content = Webserver_get_latest_game_server_log_file.read_server_log(log_file_path)
            
            # Wrap the log content in <pre> tags
            formatted_log_content = f"""
            <pre id="log">{log_content}</pre>
            <script>
                //TODO: This needs more work, pass the txt file content size and check at javascript front side if loaded.
                // if it is fully loaded - scroll to the bottom.
                window.onload = function() {{
                    var logContent = document.getElementById('log')
                    logContent.scrollTop = logContent.scrollHeight;
                    logContent.scrollIntoView(0, logContent.scrollTop)
                }};
            </script>
            """
            
            self.send_response(200); self.send_header('Content-type', 'text/html'); self.end_headers()
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

if __name__ == '__main__':
    list_all_self_paths()

    from threading import Thread
    import Webserver_player_status_monitor
    Thread(target=Webserver_player_status_monitor.main, daemon=True).start()

    #from threading import Thread
    #import Webserver_UPNP_Portforwarding
    #Thread(target=Webserver_UPNP_Portforwarding.main, daemon=True).start()

    ip, port, server_thread = start_webserver()
    print(f"[Webserver] Server started at {ip}:{port}")
    import Webserver_exit_threads_signaling
    import Webserver_main_thread_keep_alive
    