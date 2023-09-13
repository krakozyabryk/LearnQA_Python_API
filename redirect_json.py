import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")

print(f"Редиректов было: {len(response.history)}")
print(f"Конечный URL: {response.url}")