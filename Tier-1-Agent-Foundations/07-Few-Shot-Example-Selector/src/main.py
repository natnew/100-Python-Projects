import json
import math
from typing import List, Dict, Callable
from dataclasses import dataclass

@dataclass
class Example:
    input: str
    output: str
    metadata: Dict = None

class ExampleSelector:
    def __init__(self, examples: List[Example]):
        self.examples = examples

    def select(self, query: str, k: int = 3) -> List[Example]:
        """
        Selects top k examples based on similarity.
        For this pattern demo, we implement a simple Jaccard/Keyword similarity 
        to avoid heavy dependencies (torch/transformers) in the base project.
        In production, use `sentence-transformers` and a proper vector store.
        """
        # Simple similarity: token overlap
        query_tokens = set(query.lower().split())
        
        scored = []
        for ex in self.examples:
            ex_tokens = set(ex.input.lower().split())
            if not query_tokens or not ex_tokens:
                score = 0.0
            else:
                intersection = len(query_tokens.intersection(ex_tokens))
                union = len(query_tokens.union(ex_tokens))
                score = intersection / union
            scored.append((score, ex))
            
        # Sort desc
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:k]]

class FewShotPrompt:
    def __init__(self, selector: ExampleSelector, prefix: str, suffix: str):
        self.selector = selector
        self.prefix = prefix
        self.suffix = suffix

    def format(self, query: str) -> str:
        selected = self.selector.select(query)
        prompt_parts = [self.prefix]
        
        for i, ex in enumerate(selected):
            prompt_parts.append(f"Example {i+1}:\nInput: {ex.input}\nOutput: {ex.output}\n")
            
        prompt_parts.append(self.suffix.replace("{query}", query))
        return "\n".join(prompt_parts)

# --- Example Usage ---

if __name__ == "__main__":
    # Dataset: SQL generation examples
    dataset = [
        Example("Get all users", "SELECT * FROM users;"),
        Example("Count active subscriptions", "SELECT count(*) FROM subs WHERE status = 'active';"),
        Example("Find users in London", "SELECT * FROM users WHERE city = 'London';"),
        Example("Delete bad data", "DELETE FROM data WHERE quality = 'bad';"),
    ]
    
    selector = ExampleSelector(dataset)
    prompt_builder = FewShotPrompt(
        selector=selector,
        prefix="Convert natural language to SQL. Use these examples:",
        suffix="Now convert this:\nInput: {query}\nOutput:"
    )
    
    queries = [
        "Show me the users inside Paris", 
        "Count the subscriptions"
    ]
    
    for q in queries:
        print(f"--- Query: '{q}' ---")
        print(prompt_builder.format(q))
        print("\n")
