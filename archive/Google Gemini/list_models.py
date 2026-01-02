import requests

API_KEY = "AIzaSyCONb4jZcVo_48KT0MEkcHONDeY1iN87WU"

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

response = requests.get(url)

print("Status Code:", response.status_code)
print(response.json())
