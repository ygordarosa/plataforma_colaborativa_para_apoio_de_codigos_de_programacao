import json

def register_user(email, name, password):
  with open("./users.json", "r", encoding="utf-8") as f:
    jso = f.read()

  users_list = json.loads(jso)
  response = True
  for user in users_list:
    if user["email"] == email:
      response = False
      break

  if response:
    users_list.append({
      "email":email,
      "name":name,
      "password":password
    })

  with open("./users.json", "w", encoding="utf-8" ) as f:
    json.dump(users_list, f, ensure_ascii=False, indent=2)

  return response