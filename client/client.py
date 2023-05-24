import jsonpickle
import requests

from data.post import ClientPost

USERID = -1
while True:
    user_in = input("r - Gibt neuesten Post aus; p - sendet einen Post\n")
    match user_in:
        case 'r':
            response = None
            try:
                response = requests.get("http://192.168.6.93:8080")
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
            try:
                response = requests.post('http://192.168.6.93:8080', data=jsonpickle.encode(ClientPost(USERID, text)))
            except requests.ConnectionError as err:
                print('Server Error:\n' + str(err))
                continue

            if response.status_code == 200:
                print(response.text)
            elif response.status_code==400:
                print(response.text)
            else:
                print('ErrorStatusCode = ', response.status_code)
