import json

def register_user(email, name, password):
  with open("./users.json", "r", encoding="utf-8") as f:
    jso = f.read()

  users_list = json.loads(jso)
  response = True
  max_id = 0
  for user in users_list:
    if user["id"] > max_id:
      max_id = user["id"]
    if user["email"] == email:
      response = False

  if response:
    users_list.append({
      "id": max_id + 1,
      "email":email,
      "name":name,
      "password":password
    })

  with open("./users.json", "w", encoding="utf-8" ) as f:
    json.dump(users_list, f, ensure_ascii=False, indent=2)

  return response