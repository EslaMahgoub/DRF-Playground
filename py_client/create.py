import requests

endpoint = "http://localhost:8000/api/products/"

data = {
  "title": "OPPO 11",
  "price": "7000.0"
}

get_response = requests.post(endpoint, json=data)

print(get_response.json())