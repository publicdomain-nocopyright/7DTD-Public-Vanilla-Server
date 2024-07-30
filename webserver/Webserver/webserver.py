# webserver.py          Simple Threading HTTP Server
import sys; sys.dont_write_bytecode = True
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

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
    import webserver_Keep_Main_Thread_Alive
    