import requests
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"
r = requests.get(url)
data = r.json()
token = data["token"]
seconds = data["seconds"]

print(f"Задача создана. Токен: {token}, Время ожидания: {seconds} сек.")

response = requests.get(url, params={"token": token})
data = response.json()

if "error" in data:
    print(data["error"])
else:
    print(f"Статус до ожидания: {data['status']}")

time.sleep(seconds)

response = requests.get(url, params={"token": token})
data = response.json()
if "error" in data:
    print(data["error"])
else:
    print(f"Статус после ожидания: {data['status']}")
    if data["status"] == "Job is ready":
        print(f"Результат: {data['result']}")
