import json

def get_snippet(id):
    with open("./snippet_list.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    for s in data["snippets"]:
        if s["id"] == id:
            return s
    return None