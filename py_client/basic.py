import requests

# endpoint = "https://httpbin.org/status/200"
# endpoint = "https://httpbin.org/anything"
endpoint = "http://localhost:8000/api/"

get_response = requests.post(endpoint, params={"abc": 123}, 
                            json={"title": "iphone15", "content": "Hello", "price": 123})
# print(get_response.text)
# print(get_response.status_code)
print(get_response.json())