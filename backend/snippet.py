import json
from sentence_transformers import SentenceTransformer, util

def get_snippet(id):
    with open("./snippet_list.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    with open("./comments.json", "r", encoding="utf-8") as f:
        dataComment = json.load(f)
    for s in data["snippets"]:
        if s["id"] == id:
            comments = [s for s in dataComment if s["snippet_id"] == id]
            return s, comments
    return None



def create_snippett(snippet, user):
    with open("./snippet_list.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    snippets_list = data["snippets"]
    max_id = 0
    for snippetf in snippets_list:
        if snippetf["id"] >= max_id:
            max_id = snippetf["id"] + 1
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    pre_embedding = f"{snippet["title"]}. {snippet["description"]}. {snippet["code"]}. {snippet["output"]}"
    pre_embedding = pre_embedding.lower()
    emb = model.encode(pre_embedding, convert_to_tensor=True)
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
        "output": snippet["output"],
        "embedding": emb.tolist()
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



def post_comment(snippet_id, user, comment):
    with open("./comments.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    data.append(
        {
            "snippet_id": snippet_id,
            "user_id": user["id"],
            "user_name": user["name"],
            "user_pfp": None,
            "comment": comment
        }
    )
    with open("./comments.json", "w", encoding="utf-8" ) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True



def post_like_or_deslike(type, snippet_id):
    with open("./snippet_list.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    snippets_list = data["snippets"]
    for snippet in snippets_list:
         if snippet["id"] == snippet_id:
            if type == 0:
                snippet["like"] += 1
            else:
                snippet["dislike"] += 1
            break
    response = {
        "snippets" : snippets_list
    }
    with open("./snippet_list.json", "w", encoding="utf-8" ) as f:
        json.dump(response, f, ensure_ascii=False, indent=2)
    return True