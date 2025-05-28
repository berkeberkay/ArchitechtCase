from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingUtil:
    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    
    def get_embedding(self, text: str) -> list:
        return self.model.encode(text).tolist()
    
    def calculate_similarity(self, vec1: list, vec2: list) -> float:
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def find_most_similar(self, query_vec: list, doc_vecs: list) -> tuple:
        similarities = [self.calculate_similarity(query_vec, doc) for doc in doc_vecs]
        max_idx = np.argmax(similarities)
        return max_idx, similarities[max_idx]
