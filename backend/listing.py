snip = [
        {"id": 1, "title": "Loop em Python", "description": "Exemplo de loop for", "language": "python", "likes": 50, "dislikes": 2},
        {"id": 2, "title": "Função em JS", "description": "Função arrow simples", "language": "javascript", "likes": 30, "dislikes": 1},
        {"id": 3, "title": "Classe em Java", "description": "Exemplo básico de classe", "language": "java", "likes": 10, "dislikes": 0},
    ]


def listing_get():
    return snip

def listing_post(search=None, filter_language=None):
    snippets = listing_get()
    if filter_language and filter_language != "all":
        snippets = [s for s in snippets if s["language"] == filter_language]
    if search:
        snippets = [s for s in snippets if search.lower() in s["title"].lower()]
    return snippets
