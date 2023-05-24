import requests, jsonpickle
json = requests.get("localhost:8080")
print(jsonpickle.decode(json))