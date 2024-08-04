import collections, sys; sys.dont_write_bytecode = True
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

def run(server_class=ThreadingHTTPServer, handler_class=RedirectHandler, port=80, sslport=443, ip='localhost',):
        server_address = (ip, port)
        httpd = server_class(server_address, handler_class)
        print('[Webserver] Server started at ' + str(server_address))
        httpd.serve_forever()

if __name__ == '__main__':
    import threading
    server_thread = threading.Thread(target=run).start() #, daemon = True
