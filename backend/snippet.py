import json

def get_snippet(id):
    with open("./snippet_list.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    for s in data["snippets"]:
        if s["id"] == id:
            return s
    return None



def create_snippett(snippet, user):
    with open("./snippet_list.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    snippets_list = data["snippets"]
    max_id = 0
    for snippetf in snippets_list:
        if snippetf["id"] >= max_id:
            max_id = snippetf["id"] + 1
    
    new_snippet = {
        "id": max_id,
        "user_id": user["id"],
        "version": snippet["version"],
        "language": snippet["language"],
        "linkedin": None,
        "x": None,
        "github": None,
        "like": 0,
        "dislike": 0,
        "title": snippet["title"],
        "description": snippet["description"],
        "code": snippet["code"],
        "output": snippet["output"]
    }
    snippets_list.append(new_snippet)
    response = {
        "snippets" : snippets_list
    }
    with open("./snippet_list.json", "w", encoding="utf-8" ) as f:
        json.dump(response, f, ensure_ascii=False, indent=2)
    print(f"snippet com id {max_id} criado.")
    return True


def get_snippets_with_more_likes():
    with open("./snippet_list.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    snippets = data.get("snippets", [])

    # ordena pela chave "like" em ordem decrescente
    sorted_snippets = sorted(snippets, key=lambda s: s.get("like", 0), reverse=True)

    # pega apenas os 3 primeiros
    top_3 = sorted_snippets[:3]
    
    return top_3