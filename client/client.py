import requests, jsonpickle
response = requests.get("http://192.168.6.93:8080")
print(response)
print(jsonpickle.decode(response.text))