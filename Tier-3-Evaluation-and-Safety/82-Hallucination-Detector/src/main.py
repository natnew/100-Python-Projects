import random
from difflib import SequenceMatcher
from collections import Counter

class StubbornLLM:
    """Simulates an LLM generated answers."""
    
    def complete(self, prompt: str, temperature: float = 0.7) -> str:
        # Scenario 1: Factual Question (High Consistency)
        if "capital of france" in prompt.lower():
            variations = [
                "The capital of France is Paris.",
                "Paris is the capital.",
                "It is Paris.",
                "Paris."
            ]
            return random.choice(variations)
        
        # Scenario 2: Hallucination Question (Low Consistency)
        # "Who invented the Warp Drive in 1850?"
        if "warp drive" in prompt.lower():
            variations = [
                "Dr. Zefram Cochrane invented it in Montana.",
                "It was invented by Isaac Newton in a dream.",
                "Unknown scientists in Germany created it.",
                "The warp drive does not exist."
            ]
            return random.choice(variations)

        return "I do not know."

class ConsistencyChecker:
    def __init__(self, llm: StubbornLLM):
        self.llm = llm

    def check_consistency(self, prompt: str, samples: int = 5):
        print(f"\n🔎 Fact Checking: '{prompt}'")
        
        responses = []
        for i in range(samples):
            resp = self.llm.complete(prompt)
            responses.append(resp)
            # print(f"   Sample {i+1}: {resp}")
            
        # Analyze Similarity
        # Simplified: We treat them as clusters if they share key entity words
        # For this demo, we can just use the exact strings or simple length/content check
        
        # We'll use a Counter to finding the most common "idea"
        # In prod, you'd use Embeddings + Cosine Similarity.
        
        # Creating a simplified 'fingerprint' for grouping
        fingerprints = [resp.split()[-1].strip('.') for resp in responses] # Grab last word as heuristic
        counts = Counter(fingerprints)
        
        most_common_fp, count = counts.most_common(1)[0]
        confidence = count / samples
        
        print(f"   RAW Samples: {responses}")
        print(f"   Confidence Score: {confidence:.2f}")
        
        if confidence < 0.5:
            print("🚨 VERDICT: HALLUCINATION (High Entropy)")
        else:
            print("✅ VERDICT: FACT (High Consistency)")

if __name__ == "__main__":
    llm = StubbornLLM()
    checker = ConsistencyChecker(llm)
    
    checker.check_consistency("What is the capital of France?") # Fact
    checker.check_consistency("Who invented the Warp Drive in 1850?") # Fiction
