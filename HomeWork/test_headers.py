import requests
import pytest


def test_get_headers():
    url = "https://playground.learnqa.ru/api/homework_header"
    response = requests.get(url)
    header_value = "Some secret value"
    header = "x-secret-homework-header"
    get_header_value = response.headers.get(header)
    print(get_header_value)
    assert get_header_value == header_value, "Некорректное значение header "


