import json


def get_user(email):
    with open("./users.json", "r", encoding="utf-8") as f:
        jso = f.read()

    users_list = json.loads(jso)
    response = False
    for user in users_list:
        if user["email"] == email:
            response = user
            return user