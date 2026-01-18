import math
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class VectorRecord:
    id: str
    vector: List[float]
    payload: Dict

class VectorDB:
    def __init__(self):
        self.records: List[VectorRecord] = []

    def add(self, id: str, vector: List[float], payload: Dict):
        self.records.append(VectorRecord(id, vector, payload))

    def search(self, query_vector: List[float], limit: int = 3) -> List[Tuple[VectorRecord, float]]:
        """Returns top K records sorted by Cosine Similarity."""
        scored = []
        for rec in self.records:
            score = self.cosine_similarity(query_vector, rec.vector)
            scored.append((rec, score))
            
        # Sort descending score
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:limit]

    @staticmethod
    def cosine_similarity(v1: List[float], v2: List[float]) -> float:
        """
        Similarity = (A . B) / (||A|| * ||B||)
        Range: -1 to 1
        """
        dot = sum(a * b for a, b in zip(v1, v2))
        norm_a = math.sqrt(sum(a * a for a in v1))
        norm_b = math.sqrt(sum(b * b for b in v2))
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
            
        return dot / (norm_a * norm_b)

# --- Mock Embedding Model ---

def mock_embedding(text: str) -> List[float]:
    """
    Simulates embeddings for 2D space (Fruit vs Tech).
    X-axis: Nature/Food
    Y-axis: Technology
    """
    text = text.lower()
    x, y = 0.0, 0.0
    
    # Simple heuristics for demo
    if any(w in text for w in ["apple", "banana", "fruit", "food"]):
        x += 0.9
    if any(w in text for w in ["computer", "code", "ai", "tech"]):
        y += 0.9
        
    # Normalize
    norm = math.sqrt(x*x + y*y)
    if norm > 0:
        return [x/norm, y/norm]
    return [0.0, 0.0]

# --- Example Usage ---

if __name__ == "__main__":
    db = VectorDB()
    
    # 1. Index Documents
    docs = [
        {"id": "1", "text": "Apple is a tasty fruit."},
        {"id": "2", "text": "Banana is yellow."},
        {"id": "3", "text": "Apple Computers makes the Mac."} # Confusing 'Apple'!
    ]
    
    print("--- Indexing ---")
    for d in docs:
        vec = mock_embedding(d["text"])
        db.add(d["id"], vec, d)
        print(f"Indexed {d['id']}: {d['text']} -> {vec}")
        
    # 2. Search
    print("\n--- Searching for 'Food' ---")
    q_vec = mock_embedding("I want some food")
    results = db.search(q_vec)
    for rec, score in results:
        print(f"[{score:.2f}] {rec.payload['text']}")
        
    print("\n--- Searching for 'Tech' ---")
    q_vec = mock_embedding("Computer code")
    results = db.search(q_vec)
    for rec, score in results:
        print(f"[{score:.2f}] {rec.payload['text']}")
