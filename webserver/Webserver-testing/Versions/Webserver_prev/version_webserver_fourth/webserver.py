# webserver.py          Simple Threading HTTP Server
import sys; sys.dont_write_bytecode = True
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

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
            self.wfile.write(open(Path(__file__).parent / 'index.html', 'rb').read())

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
            import urllib.request
            webserver_public_ip = urllib.request.urlopen('https://api.ipify.org').read().decode()
            self.wfile.write(webserver_public_ip.encode('utf-8'))

        if self.path == '/list_paths':
                self.send_response(200), self.send_header('Content-type', 'text/plain'), self.end_headers()
                self.wfile.write(get_self_paths_json(RedirectHandler).encode('utf-8'))
           
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

    ip, port, server_thread = start_webserver()
    print(f"[Webserver] Server started at {ip}:{port}")
    import webserver_Exit_Threads_Signaling
    import webserver_Main_Thread_Keep_Alive
    