# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import jsonpickle

from data.post import Post
import json

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        p = Post(0, 0, "Test", 0)
        self.wfile.write(bytes(jsonpickle.encode(p), "utf-8"))


if __name__ == "__main__":
    p = Post(0, 0, "Test", 0)
    print(jsonpickle.encode(p))
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
