from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
         if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
            self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":
    address = ('127.0.0.1', 8000)
    print("Web Server Started on:", ":".join(map(str, address)))
    ThreadingHTTPServer(address, RedirectHandler).serve_forever()