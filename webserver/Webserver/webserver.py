# webserver.py          Simple Threading HTTP Server
import sys; sys.dont_write_bytecode = True
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

def run(server_class=ThreadingHTTPServer, handler_class=RedirectHandler, ip='localhost', port=80):
    server_address = (ip, port)
    httpd = server_class(server_address, handler_class)

    from threading import Thread

    def serve():
        httpd.serve_forever()

    server_thread = Thread(target=serve).start() #, daemon = True

    return ip, port, server_thread

if __name__ == '__main__':
    ip, port, server_thread = run()
    print(f"[Webserver] Server started at {ip}:{port}")
    