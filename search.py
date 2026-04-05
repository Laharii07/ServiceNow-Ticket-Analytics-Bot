from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sops import SOPS

# Build corpus from title + content + tags
corpus = [f"{s['title']} {s['content']} {' '.join(s['tags'])}" for s in SOPS]
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(corpus)

def search_kb(query: str, top_n: int = 3) -> list:
    query_vec = vectorizer.transform([query])
    scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = np.argsort(scores)[::-1][:top_n]
    
    results = []
    for idx in top_indices:
        if scores[idx] > 0.01:  # threshold — ignore totally irrelevant results
            results.append({
                "title": SOPS[idx]["title"],
                "content": SOPS[idx]["content"],
                "score": round(float(scores[idx]), 3)
            })
    return results
