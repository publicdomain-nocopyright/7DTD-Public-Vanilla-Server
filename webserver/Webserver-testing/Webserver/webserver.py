# webserver.py          Simple Threading HTTP Server
import sys; sys.dont_write_bytecode = True
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import Webserver_fix_pythonw_stream_bug

# Define the function to read the log file
def read_server_log(LOG_FILE_PATH):
    try:
        with open(LOG_FILE_PATH, 'r') as file:
            log_content = file.read()
        return log_content
    except FileNotFoundError:
        return "Log file not found."
    except Exception as e:
        return f"An error occurred: {e}"



class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        #html_content = """
        #<head>
        #    <title>Custom Title</title>
        #</head>
        #"""
        #self.wfile.write(html_content.encode('utf-8'))


        if self.path == '/':
            self.send_response(200), self.send_header('Content-type', 'text/html'), self.end_headers()

            from pathlib import Path
            import webserver_Template_Engine

            import Webserver_FindNextHordeNightTime_inside_logs_folder
            bloodmoon_days = Webserver_FindNextHordeNightTime_inside_logs_folder.find_last_bloodmoon_setday()
            Webserver_IP_ADDRESS = Get_WebServer_Public_IP()

            rendered_html = webserver_Template_Engine.render_template('index.html')
            self.wfile.write(bytes(rendered_html, 'utf-8'))

        if self.path == '/favicon.ico':
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
            
        if self.path == '/Get_WebServer_Public_IP':
            self.send_response(200), self.send_header('Content-type', 'text/plain'), self.end_headers()
            self.wfile.write(Get_WebServer_Public_IP().encode('utf-8'))

        if self.path == '/list_paths':
                self.send_response(200), self.send_header('Content-type', 'text/plain'), self.end_headers()
                self.wfile.write(get_self_paths_json(RedirectHandler).encode('utf-8'))

        if self.path == '/server-log':
            
            # Assuming Webserver_Get_Latest_Game_Server_Log_File.get_latest_game_server_log_file_name() returns the log file path
            import Webserver_Get_Latest_Game_Server_Log_File
            log_file_path = Webserver_Get_Latest_Game_Server_Log_File.get_latest_game_server_log_file_name()
            log_content = read_server_log(log_file_path)
            
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
            
            # Send response status code
            self.send_response(200)
            
            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Write the content as UTF-8 data
            self.wfile.write(bytes(formatted_log_content, "utf8"))
            
        if self.path == '/player_status.json':
            import os
            self.send_response(200), self.send_header('Content-type', 'application/json'), self.end_headers()
            import json
            file_path = os.path.join(os.path.dirname(__file__), 'player_status.json')
            with open(file_path, 'r') as file:
                data = json.load(file)
            self.wfile.write(json.dumps(data).encode('utf-8'))

def Get_WebServer_Public_IP():
        import urllib.request
        webserver_public_ip = urllib.request.urlopen('https://api.ipify.org').read().decode()
        return webserver_public_ip

def start_webserver(server_class=ThreadingHTTPServer, handler_class=RedirectHandler, ip='localhost', port=80):
    from threading import Thread
    
    server_address = (ip, port)

    def serve(httpd = server_class(server_address, handler_class)): 
        httpd.serve_forever()

    return ip, port, Thread(target=serve, daemon=True).start() 

def inspect_self_paths(handler_class):
    import inspect
    import re
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
    import inspect
    import re

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
    import player_status_monitor
    Thread(target=player_status_monitor.main, daemon=True).start()

    ip, port, server_thread = start_webserver()
    print(f"[Webserver] Server started at {ip}:{port}")
    import webserver_Exit_Threads_Signaling
    import webserver_Main_Thread_Keep_Alive
    