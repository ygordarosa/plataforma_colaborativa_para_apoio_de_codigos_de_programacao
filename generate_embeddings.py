import json
from sentence_transformers import SentenceTransformer, util


with open("./snippet_list.json", "r", encoding="utf-8") as f:
  jso = f.read()

snippets = json.loads(jso)
snippets = snippets["snippets"]
embeddings = []
titles = []

#transformar o snippet em um texto só para fazer embeddings
for snippet in snippets:
  embeddings.append(f"{snippet["title"]}. {snippet["description"]}. {snippet["code"]}. {snippet["output"]}")
  titles.append(snippet["title"])

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

embeddings_list = []
for snippet in embeddings:
  emb = model.encode(snippet, convert_to_tensor=True)
  embeddings_list.append(emb.tolist())


with open("embeddings.json", "w", encoding="utf-8") as f:
    json.dump(embeddings_list, f, ensure_ascii=False, indent=2)


with open("titles.json", "w", encoding="utf-8") as f:
    json.dump(titles, f, ensure_ascii=False, indent=2)
