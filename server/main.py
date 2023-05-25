from http.server import BaseHTTPRequestHandler, HTTPServer

import jsonpickle
import mysql.connector

from post import Post

hostName = "192.168.6.179"
mysqlhostname = '192.168.6.179'
serverPort = 8080


def connect_to_db():
    return (mysql.connector.connect(
        host='localhost',
        user='one',
        password='schillercoin',
        database='matesuperiority')
    )


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # Verarbeitet die Request Daten
        content_length = int(self.headers['Content-Length'])
        request_data = self.rfile.read(content_length)
        try:
            index = request_data.split()[0]
            amount = request_data.split()[1]
        except:
            self.send_response(400)
            self.send_header("Content-type", "text/text")
            self.end_headers()
            self.wfile.write(bytes('Malformed request','utf-8'))
            return

        db = connect_to_db()
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        p = Post(0, 0, "Test", 0)
        self.wfile.write(bytes(jsonpickle.encode(p), "utf-8"))

    def do_POST(self):
        db = connect_to_db()

        # Verarbeitet die Request Daten
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            client_post = jsonpickle.decode(post_data)
        except:
            self.send_response(400)
            self.send_header("Content-type", "text/text")
            self.end_headers()
            self.wfile.write(bytes('Malformed request','utf-8'))
            return

        try:
            password = db.cursor().execute(f"SELECT password FROM users WHERE userName=%s", (client_post.userName,))
        except mysql.connector.Error:
            self.send_response(400)
            self.send_header("Content-type", "text/text")
            self.end_headers()
            self.wfile.write(bytes('Falscher User oder Passwort!', 'utf-8'))
            return

        if password == client_post.password:
            self.send_response(400)
            self.send_header("Content-type", "text/text")
            self.end_headers()
            self.wfile.write(bytes('Falscher User oder Passwort!', 'utf-8'))

        elif client_post.text != '':
            self.send_response(200)
            self.send_header("Content-type", "text/text")
            self.end_headers()
            self.wfile.write(bytes('Post gesendet!', 'utf-8'))

            text = client_post.text
            username = client_post.userName
            print(username, ":\n", text)
            userID = db.cursor().execute(f"SELECT userID FROM users WHERE userName=%s", (client_post.userName,))
            print(userID)
            db.curser().execute(f"INSERT INTO posts (userID, text, likes) VALUES (%s, %s, 0)", (userID, text))
            db.commit()

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
