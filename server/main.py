from http.server import BaseHTTPRequestHandler, HTTPServer

import jsonpickle
from mysql.connector import MySQLConnection
import random as rn
from post import Post

hostName = "192.168.6.179"
mysqlhostname = "192.168.6.179"
serverPort = 8080


def connect_to_db():
    conn = MySQLConnection(host="localhost", user="one", password="schillercoin", database="matesuperiority")
    cursor = conn.cursor()

    return cursor, conn


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        params= str(self.path)[1:].strip()
        if params!="":
            params=int(params)
        else:
            params=1
        print(params)
        cursor, conn = connect_to_db()
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        cursor.execute(f"SELECT p.postID, u.userName, p.title, p.text, p.likes FROM users u, posts p WHERE p.userID = u.userID ORDER BY p.postID DESC LIMIT %s", (params,))
        data = cursor.fetchall()
        L=[]
        for i in data:
            p= Post(i[0], i[1], i[2], i[3], i[4], 0)
            L.append(p)
        print(L)
        self.wfile.write(bytes(jsonpickle.encode(L), "utf-8"))

    def do_POST(self):
        cursor, db = connect_to_db()
        content_length = int(self.headers["Content-Length"])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)
        client_post = jsonpickle.decode(post_data)
        if client_post.inputcase == 0:  # Post is being sent
            try:
                cursor.execute(f"SELECT password FROM users WHERE userName=%s", (client_post.userName,))
                password= cursor.fetchall()[0][0]
            except:
                self.send_response(400)
                self.send_header("Content-type", "text/text")
                self.end_headers()
                self.wfile.write(bytes("Falscher User oder Passwort!", "utf-8"))

            if password != client_post.password:
                self.send_response(400)
                self.send_header("Content-type", "text/text")
                self.end_headers()
                self.wfile.write(bytes("Falscher User oder Passwort!", "utf-8"))
            elif client_post.text != "":
                self.send_response(200)
                self.send_header("Content-type", "text/text")
                self.end_headers()
                self.wfile.write(bytes("Post gesendet!", "utf-8"))
                title= client_post.title
                text=client_post.text
                username=client_post.userName
                print(username, ":\n", text)
                cursor.execute(f"SELECT userID FROM users WHERE userName=%s", (client_post.userName,))
                userID = cursor.fetchall()[0][0]
                print(userID)
                likes= rn.randint(1,100) * 10000
                cursor.execute(f"INSERT INTO posts (userID, title, text, likes) VALUES (%s, %s, %s, %s)", (userID, title, text, likes))
                db.commit()
            else:
                self.send_response(400)
                self.send_header("Content-type", "text/text")
                self.end_headers()
                self.wfile.write(bytes("Fehlerhafte Post Syntax!", "utf-8"))

        elif client_post.inputcase == 1:
            newUser= client_post.userName
            newPassword= client_post.password
            cursor.execute(f"SELECT userName FROM users WHERE userName = %s", (newUser,))
            data = cursor.fetchall()
            if len(data) >= 1:
                self.send_response(500)
                self.send_header("Content-type", "text/text")
                self.end_headers()
                self.wfile.write(bytes("User existiert bereits! Anderen Namen wählen!", "utf-8"))
            else:
                cursor.execute(f"INSERT INTO users (userName, password) VALUES (%s, %s)", (newUser, newPassword))
                db.commit()
                self.send_response(200)
                self.send_header("Content-type", "text/text")
                self.end_headers()
                self.wfile.write(bytes("User erstellt.", "utf-8"))

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
