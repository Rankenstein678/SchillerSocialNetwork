from http.server import BaseHTTPRequestHandler, HTTPServer

import jsonpickle

from data.post import Post

hostName = "192.168.6.93"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        p = Post(0, 0, "Test", 0)
        self.wfile.write(bytes(jsonpickle.encode(p), "utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)
        client_post = jsonpickle.decode(post_data)
        if client_post.text != '':
            self.send_response(200)
            self.send_header("Content-type", "text/text")
            self.end_headers()
            self.wfile.write(bytes('Post gesendet!', 'utf-8'))
        else:
            self.send_response(400)
            self.send_header("Content-type", "text/text")
            self.end_headers()
            self.wfile.write(bytes('Fehlerhafte Post Syntax!', 'utf-8'))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
