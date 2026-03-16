#!/usr/bin/python3
import socket, ssl, http.server

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory = ".", **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        http.server.SimpleHTTPRequestHandler.end_headers(self)

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain("domain.crt", "domain.key")
ctx.check_hostname = False
httpd = http.server.HTTPServer(("0.0.0.0", 443), Handler)
httpd.socket = ctx.wrap_socket(httpd.socket, server_hostname = "localhost")
print("navigate to https://127.0.0.1 in a web browser")
httpd.serve_forever()
