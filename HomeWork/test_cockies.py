import requests
import pytest



def test_get_cookie():
    url ="https://playground.learnqa.ru/api/homework_cookie"
    response = requests.get(url)
    cookie_value = response.cookies.get('HomeWork')
    assert cookie_value is not None, "Cookie не найдено в ответе"
    print(f"Значение cookie: {cookie_value}")
    cookie_value2 = "hw_value"
    assert cookie_value == cookie_value2, "Некорректное значение coockie"
