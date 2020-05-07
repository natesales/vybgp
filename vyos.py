# VyOS Agent

import os
from urllib.parse import unquote
from http.server import HTTPServer, BaseHTTPRequestHandler

LOG = False
HOST = "10.0.10.2"
PORT = 8000

class RequestHandler(BaseHTTPRequestHandler):
    def send_response(self, code):
        if LOG:
            self.log_request(code)
        self.send_response_only(code)
        self.send_header("Server", "python3 http.server Development Server")
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        output = os.popen("/opt/vyatta/bin/vyatta-op-cmd-wrapper " + unquote(self.path[1:])).read()
        self.wfile.write(output.encode())

server_address = (HOST, PORT)
httpd = HTTPServer(server_address, RequestHandler)
httpd.serve_forever()
