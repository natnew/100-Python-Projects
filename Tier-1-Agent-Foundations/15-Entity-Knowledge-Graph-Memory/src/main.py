from typing import List, Tuple, Dict
from dataclasses import dataclass
import networkx as nx

@dataclass
class Triplet:
    source: str
    relation: str
    target: str

class KnowledgeGraph:
    def __init__(self):
        # We use NetworkX for the graph data structure
        self.graph = nx.DiGraph()

    def add_triplet(self, source: str, relation: str, target: str):
        """Adds a fact to the graph."""
        # Add nodes
        self.graph.add_node(source)
        self.graph.add_node(target)
        # Add edge with relation as attribute
        self.graph.add_edge(source, target, relation=relation)
        print(f"DEBUG: Added ({source}) -[{relation}]-> ({target})")

    def query(self, entity: str) -> List[str]:
        """
        Returns all known facts about an entity (outgoing edges).
        """
        if entity not in self.graph:
            return [f"No knowledge about {entity}."]
        
        facts = []
        # Outgoing edges
        for neighbor in self.graph.neighbors(entity):
            relation = self.graph[entity][neighbor]['relation']
            facts.append(f"{entity} {relation} {neighbor}")
        
        return facts

    def find_path(self, start: str, end: str) -> List[str]:
        """Finds connection between two entities."""
        try:
            path = nx.shortest_path(self.graph, source=start, target=end)
            # Reconstruct path with relations
            readable = []
            for i in range(len(path)-1):
                u, v = path[i], path[i+1]
                rel = self.graph[u][v]['relation']
                readable.append(f"{u} {rel} {v}")
            return readable
        except nx.NetworkXNoPath:
            return ["No connection found."]
        except nx.NodeNotFound:
            return ["Entity not found."]

# --- Example Usage ---

# Mock LLM Extractor
def mock_extract(text: str) -> List[Triplet]:
    # In real world: LLM call "Extract triplets from: {text}"
    if "Alice reports to Bob" in text:
        return [Triplet("Alice", "reports_to", "Bob")]
    if "Bob manages Engineering" in text:
        return [Triplet("Bob", "manages", "Engineering")]
    if "Alice lives in Paris" in text:
        return [Triplet("Alice", "lives_in", "Paris")]
    return []

if __name__ == "__main__":
    kg = KnowledgeGraph()
    
    inputs = [
        "Alice reports to Bob.",
        "Bob manages Engineering.",
        "Alice lives in Paris."
    ]
    
    # 1. Ingest
    print("--- Ingesting ---")
    for text in inputs:
        triplets = mock_extract(text)
        for t in triplets:
            kg.add_triplet(t.source, t.relation, t.target)
            
    # 2. Query
    print("\n--- Query: 'Alice' ---")
    print("\n".join(kg.query("Alice")))
    
    # 3. Reasoning (Pathfinding)
    print("\n--- Path: Alice -> Engineering? ---")
    # Does Alice connect to Engineering?
    path = kg.find_path("Alice", "Engineering")
    print(" -> ".join(path))
