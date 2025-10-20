from sentence_transformers import SentenceTransformer, util
import numpy as np
import json

# carregar modelo e embeddings uma única vez
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

with open("./embeddings.json", "r", encoding="utf-8") as f:
  emb = json.load(f)
# suponha que embeddings_array é uma lista de todos os embeddings do banco
embeddings_array = np.array(emb, dtype=np.float32)  # shape (N, D)
with open("./titles.json", "r", encoding="utf-8") as f:
  titles = json.load(f)
titulos = titles

def buscar_snippets(query, top_k=5):
    emb_query = model.encode(query)
    scores = util.cos_sim(emb_query, embeddings_array)[0]
    indices = np.argsort(-scores)[:top_k]
    return [(titulos[i], float(scores[i])) for i in indices]



print(buscar_snippets("utilizar API"))