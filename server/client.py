import jsonpickle
import requests

from post import ClientPost

username = input('Gebe deinen Benuternamen an:\n')
password = input("Passwort: ")
LOGIN_CREDENTIALS = (username, password)  # Security isch stabil Junge, ey

ip = 'http://192.168.6.179:8080'

while True:
    user_in = input("r - Gibt neuesten Post aus; p - sendet einen Post\n")
    match user_in:
        case 'r':  # Password bei Requests nicht benötigt, da der Server eh lokal ist
            response = None
            try:
                response = requests.get(ip)
            except requests.ConnectionError as err:
                print('Server Error:\n' + str(err))
                continue
            if response.status_code == 200:
                post = jsonpickle.decode(response.text)
                print(f'{post.userID}\n{post.text}\nLikes: {post.likes}')
            else:
                print('ErrorStatusCode = ', response.status_code)
        case 'p':
            text = input('Post Inhalt:\n')
            response = None
            data = jsonpickle.encode(ClientPost(LOGIN_CREDENTIALS[0], LOGIN_CREDENTIALS[1], text, 0))
            try:
                response = requests.post(ip, data=data)
            except requests.ConnectionError as err:
                print('Server Error:\n' + str(err))
                continue

            if response.status_code== 200:
                print(response.text)
            elif response.status_code== 400:
                print(response.text)
            else:
                print('ErrorStatusCode = ', response.status_code)
