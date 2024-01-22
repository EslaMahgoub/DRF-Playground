import requests

endpoint = "http://localhost:8000/api/products/1/update/"

data = {
  "title": "OPPO 10",
  "price": 7025.0
}

get_response = requests.put(endpoint, json=data)


print(get_response.json())