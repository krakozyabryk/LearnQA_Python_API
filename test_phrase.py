import requests
import pytest

class TestPhrase:
    def test_phrases(self):
        phrase = input("Set a phrase: ")
        count = len(phrase)
        assert count < 15, "phrase is more then 15 symbol"