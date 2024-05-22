
#__________________Signal_Handler_____________________
import signal
import sys
import time

def signal_handler(signal, frame):
    print("Web Server Shutting Down.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#____________________HTTP_SERVER_______________________
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        response = (
            f"<html><head><title>https://pythonbasics.org</title></head>"
            f"<body><p>Request: {self.path}</p>"
            f"<p>This is an example web server.</p></body></html>"
        ).encode("utf-8")
        self.wfile.write(response)

if __name__ == "__main__":
    address = ('127.0.0.1', 8000)
    print("Web Server Started on: " + address[0] + ":" + str(address[1]))
    ThreadingHTTPServer(address, RedirectHandler).serve_forever()




