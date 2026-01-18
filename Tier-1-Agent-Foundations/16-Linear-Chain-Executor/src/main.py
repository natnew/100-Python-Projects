from typing import Callable, Any, List
from dataclasses import dataclass

@dataclass
class ChainStep:
    name: str
    func: Callable[[Any], Any]

class LinearChain:
    def __init__(self, steps: List[ChainStep]):
        self.steps = steps

    def invoke(self, input_data: Any) -> Any:
        current_data = input_data
        print(f"🔗 Starting Chain with input: {current_data}")
        
        for step in self.steps:
            print(f"  ⬇️ Running Step: {step.name}")
            try:
                current_data = step.func(current_data)
                print(f"     ✅ Output: {str(current_data)[:50]}...")
            except Exception as e:
                print(f"     ❌ Step Failed: {e}")
                raise e
                
        print("🏁 Chain Complete.")
        return current_data

# --- Example Usage ---

# Step 1: Sanitize
def sanitize(text: str) -> str:
    return text.strip().lower()

# Step 2: Simulate Translation (Mock LLM)
def translate_to_french(text: str) -> str:
    # Quick dirty mock
    translations = {
        "hello world": "bonjour le monde",
        "i love python": "j'aime python"
    }
    return translations.get(text, f"[Translated: {text}]")

# Step 3: Format as JSON
def wrap_json(text: str) -> dict:
    return {"message": text, "lang": "fr"}

if __name__ == "__main__":
    # Define the pipeline
    pipeline = LinearChain([
        ChainStep("Sanitize", sanitize),
        ChainStep("Translate", translate_to_french),
        ChainStep("Format", wrap_json)
    ])
    
    # Run it
    input_str = "  Hello World  "
    result = pipeline.invoke(input_str)
    
    print(f"\nFinal Result: {result}")
