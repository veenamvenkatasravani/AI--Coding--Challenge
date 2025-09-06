import json
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TinyRAG:
    def __init__(self, kb_path: str = "knowledge_base.json"):
        with open(kb_path, 'r', encoding='utf-8') as f:
            self.docs = json.load(f)
        self.texts = [d["content"] for d in self.docs]
        self.ids = [d["id"] for d in self.docs]
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.mat = self.vectorizer.fit_transform(self.texts)

    def retrieve(self, query: str, k: int = 2) -> List[Dict]:
        qv = self.vectorizer.transform([query])
        sims = cosine_similarity(qv, self.mat)[0]
        top = sims.argsort()[::-1][:k]
        return [{"id": self.ids[i], "content": self.texts[i], "score": float(sims[i])} for i in top]
