import json
import math
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class MemoryItem:
    text: str
    metadata: Dict

class VectorStore:
    def __init__(self):
        self.documents: List[MemoryItem] = []

    def add(self, text: str, metadata: Dict = None):
        self.documents.append(MemoryItem(text, metadata or {}))

    def search(self, query: str, k: int = 3) -> List[MemoryItem]:
        """
        Simulated semantic search using token overlap (Jaccard) for demo.
        In production, replace with:
        `embedding = model.encode(query)`
        `results = chroma.query(embedding)`
        """
        query_tokens = set(query.lower().split())
        
        scored = []
        for doc in self.documents:
            doc_tokens = set(doc.text.lower().split())
            if not query_tokens or not doc_tokens:
                score = 0.0
            else:
                intersection = len(query_tokens.intersection(doc_tokens))
                union = len(query_tokens.union(doc_tokens))
                score = intersection / union
            scored.append((score, doc))
            
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:k]]

class SemanticMemory:
    def __init__(self):
        self.store = VectorStore()

    def remember(self, text: str, meta: Dict = None):
        print(f"DEBUG: Storing '{text}'")
        self.store.add(text, meta)

    def recall(self, query: str) -> str:
        results = self.store.search(query, k=1)
        if not results:
            return "No relevant memories found."
        
        # Format the retrieved memory
        best = results[0]
        return f"Memory: {best.text}"

# --- Example Usage ---

if __name__ == "__main__":
    memory = SemanticMemory()
    
    # Simulate past conversations
    memory.remember("My favorite color is blue.", {"date": "2023-01-01"})
    memory.remember("I have a dog named Rex.", {"date": "2023-01-05"})
    memory.remember("I work as a software engineer.", {"date": "2023-01-10"})
    
    print("\n--- Recall Test 1 ---")
    q1 = "What is my job?"
    print(f"Query: {q1}")
    print(memory.recall(q1))
    
    print("\n--- Recall Test 2 ---")
    q2 = "Do I have any pets?"
    print(f"Query: {q2}")
    print(memory.recall(q2))
