import json

with open("./snippet_list.json", "r", encoding="utf-8") as f:
        data = json.load(f)


def listing_get():
    return data["snippets"]

def listing_post(search=None, filter_language=None):
    snippets = listing_get()
    if filter_language and filter_language != "all":
        snippets = [s for s in snippets if s["language"] == filter_language]
    if search:
        snippets = [s for s in snippets if search.lower() in s["title"].lower()]
    return snippets
