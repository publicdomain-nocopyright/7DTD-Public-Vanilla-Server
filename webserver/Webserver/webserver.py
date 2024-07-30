# webserver.py          Simple Threading HTTP Server
import sys; sys.dont_write_bytecode = True
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200), self.send_header('Content-type', 'text/html'), self.end_headers()

            from pathlib import Path
            self.wfile.write(open(Path(__file__).parent / 'index.html', 'rb').read())

        if self.path == '/favicon.ico':
            self.send_response(200), self.send_header('Content-type', 'image/x-icon'), self.end_headers()
            favicon_base64 = (
               """AAABAAEAEBAQAAEABAAoAQAAFgAAACgAAAAQAAAAIAAAAAEABAAAAAAAgAAAAAAAAAAAAAAAEAAAAAAAAABXqw4AAAAAAGCuJwBmvSQAtd6YAPHw7ABpvisAccwuAAAAAAAAAAAAAAAAAAAAAA
               AAAAAAAAAAAAAAAAAAAAAAERERERERERERERJndiEREREQd3d3dwERERd3J3d3cRERd3JSd3d3ERF3JVUnd3cRE3dVVVJ3dzEXd1V0VSd3cRd3d3dFUndxF3d3d3RVd3ERd3d3d0d3ERF3d3d3d3cRE
               Rd3d3d3cREREXd3d3cRERERF3d3cRERERERERERERH//wAA+B8AAOAHAADgBwAAwAMAAMADAACAAQAAgAEAAIABAACAAQAAwAMAAMADAADgBwAA8A8AAPgfAAD//wAA
               """)
            import base64        
            self.wfile.write(base64.b64decode(favicon_base64))
            
        if self.path == '/Get_WebServer_Public_IP':
            self.send_response(200), self.send_header('Content-type', 'text/plain'), self.end_headers()
            import urllib.request
            webserver_public_ip = urllib.request.urlopen('https://api.ipify.org').read().decode()
            self.wfile.write(webserver_public_ip.encode('utf-8'))

            



            
def server(server_class=ThreadingHTTPServer, handler_class=RedirectHandler, ip='localhost', port=80):
    from threading import Thread
    
    server_address = (ip, port)

    def serve(httpd = server_class(server_address, handler_class)): 
        httpd.serve_forever()

    return ip, port, Thread(target=serve, daemon=True).start() 

if __name__ == '__main__':
    ip, port, server_thread = server()
    print(f"[Webserver] Server started at {ip}:{port}")
    import webserver_Exit_Threads_Signaling
    import webserver_Main_Thread_Keep_Alive
    