# vector_database.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class VectorDatabase:
    def __init__(self):
        self.documents = []
        self.vectors = None
        self.vectorizer = TfidfVectorizer()

    def add_document(self, doc: dict):
        self.documents.append(doc)
        self._update_vectors()

    def _update_vectors(self):
        texts = [doc['text'] for doc in self.documents]
        self.vectors = self.vectorizer.fit_transform(texts)

    def search(self, query: str, top_k: int = 10):
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.vectors).flatten()
        top_indices = similarities.argsort()[-top_k:][::-1]
        return [(self.documents[i], similarities[i]) for i in top_indices]