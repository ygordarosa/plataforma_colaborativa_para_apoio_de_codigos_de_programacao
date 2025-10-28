import json
import numpy as np
from sentence_transformers import SentenceTransformer, util


def listing_get():
    with open("./snippet_list.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["snippets"]

def listing_post(search=None, filter_language=None):
    snippets = listing_get()
    if filter_language and filter_language != "all":
        snippets = [s for s in snippets if s["language"] == filter_language]
    if search:
        # carregar modelo uma única vez
        model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        
        emb_query = model.encode(search.lower())
        embeddings_array = np.array([s["embedding"] for s in snippets], dtype=np.float32)
        scores = util.cos_sim(emb_query, embeddings_array)[0]
        indices = np.argsort(-scores)[:8]
        snippets = [snippets[i] for i in indices]
        
    return snippets
