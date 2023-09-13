import requests


url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
methods = ["GET", "POST", "PUT", "DELETE"]


response = requests.get(url)
print("1. Ответ на запрос без параметра method:")
print(response.status_code, response.text)
print()

method = "HEAD"
response = requests.request(method, url, params={"method": method})
print(f"2. Ответ на запрос с неверным типом ({method}):")
print(response.status_code, response.text)
print()

method = "GET"
response = requests.request(method, url, params={"method": method})
print(f"3. Ответ на запрос с правильным значением method ({method}):")
print(response.status_code, response.text)
print()


for method in methods:
    for param_method in methods:
        if method == "GET":
            response = requests.get(url, params={"method": param_method})
        else:
            response = requests.request(method, url, data={"method": param_method})
        is_match = response.text == f"Method is {param_method}"
        print(
            f"Method: {param_method}, Результат: {'Совпадает' if is_match else 'Не совпадает'}, Код ответа:{response.status_code}")
