import json


json_text = {"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}

key = "messages"
if key in json_text:
        print(json_text[key][1])
else:
    print(f"Ключа {key} нет в json")

