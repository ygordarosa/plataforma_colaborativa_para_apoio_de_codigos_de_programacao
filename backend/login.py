import json


def user_login(email, password):
  with open("./users.json", "r", encoding="utf-8") as f:
    jso = f.read()

  users_list = json.loads(jso)
  response = False
  for user in users_list:
    if user["email"] == email and user["password"] == password:
      response = True
      break
  return response