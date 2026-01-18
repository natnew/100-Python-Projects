import random
from typing import List, Callable, Any

class ModelError(Exception):
    pass

class ModelCascade:
    def __init__(self, models: List[Callable[[str], str]]):
        self.models = models

    def generate(self, prompt: str) -> str:
        errors = []
        for i, model in enumerate(self.models):
            try:
                print(f"🔄 Attempting Model {i+1} ({model.__name__})...")
                result = model(prompt)
                print(f"   ✅ Success with Model {i+1}")
                return result
            except Exception as e:
                print(f"   ❌ Model {i+1} Failed: {e}")
                errors.append(str(e))
        
        raise ModelError(f"All models failed. Errors: {errors}")

# --- Example Usage ---

def mock_gpt4(prompt: str) -> str:
    # 80% chance of failure (simulating outage)
    if random.random() < 0.8:
        raise ConnectionError("503 Service Unavailable")
    return f"[GPT-4] Response to: {prompt}"

def mock_gpt35(prompt: str) -> str:
    # 50% chance of failure
    if random.random() < 0.5:
        raise TimeoutError("Request Timed Out")
    return f"[GPT-3.5] Response to: {prompt}"

def mock_claude(prompt: str) -> str:
    # Reliable backup
    return f"[Claude] Response to: {prompt}"

if __name__ == "__main__":
    cascade = ModelCascade([mock_gpt4, mock_gpt35, mock_claude])
    
    print("--- Request 1 ---")
    try:
        res = cascade.generate("Hello world")
        print(f"Final Result: {res}")
    except ModelError as e:
        print(f"System Crash: {e}")
        
    print("\n--- Request 2 ---")
    try:
        res = cascade.generate("Complex Query")
        print(f"Final Result: {res}")
    except ModelError as e:
        print(f"System Crash: {e}")
