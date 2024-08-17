import sys; sys.dont_write_bytecode = True
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

def run(server_class=ThreadingHTTPServer, handler_class=RedirectHandler, ip='localhost', port=80, sslport=443):
    server_address = (ip, port)
    httpd = server_class(server_address, handler_class)
    print(f"[Webserver] Server started at {ip}:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    import threading
    server_thread = threading.Thread(target=run).start() #, daemon = True