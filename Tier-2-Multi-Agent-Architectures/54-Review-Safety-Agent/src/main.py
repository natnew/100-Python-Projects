from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class ReviewResult:
    approved: bool
    feedback: str

class SafetyPolicy:
    def check(self, content: str) -> ReviewResult:
        raise NotImplementedError

class PIIPolicy(SafetyPolicy):
    def check(self, content: str) -> ReviewResult:
        if "@example.com" in content or "555-0199" in content:
            return ReviewResult(False, "Contains PII (Email/Phone)")
        return ReviewResult(True, "No PII found")

class ToxicityPolicy(SafetyPolicy):
    def check(self, content: str) -> ReviewResult:
        blocklist = ["hate", "violence", "kill"]
        if any(word in content.lower() for word in blocklist):
            return ReviewResult(False, "Contains Toxic Content")
        return ReviewResult(True, "Content is civil")

class ReviewAgent:
    def __init__(self, name: str = "SafetyBot"):
        self.name = name
        self.policies: List[SafetyPolicy] = [
            PIIPolicy(),
            ToxicityPolicy()
        ]

    def review(self, content: str) -> ReviewResult:
        print(f"👮 {self.name} reviewing: '{content[:30]}...'")
        
        for policy in self.policies:
            res = policy.check(content)
            if not res.approved:
                print(f"   ❌ Blocked by {policy.__class__.__name__}: {res.feedback}")
                return res
        
        print("   ✅ Approved.")
        return ReviewResult(True, "LGTM")

# --- Example Usage ---

if __name__ == "__main__":
    reviewer = ReviewAgent()
    
    # Test 1: Safe Content
    print("--- Case 1 ---")
    res1 = reviewer.review("Hello! How can I help you today?")
    
    # Test 2: Unsafe (Toxicity)
    print("\n--- Case 2 ---")
    res2 = reviewer.review("I hate you and I want to kill the process.")
    
    # Test 3: Unsafe (PII)
    print("\n--- Case 3 ---")
    res3 = reviewer.review("My email is bob@example.com, please contact me.")
