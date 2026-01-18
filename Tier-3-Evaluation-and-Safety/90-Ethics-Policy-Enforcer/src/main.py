from dataclasses import dataclass
from typing import List

@dataclass
class Policy:
    name: str
    description: str
    forbidden_keywords: List[str]
    response_template: str

class EthicsEngine:
    def __init__(self):
        self.policies = [
            Policy(
                name="No Financial Advice",
                description="Agents cannot recommend buying stocks.",
                forbidden_keywords=["buy bitcoin", "short tesla", "invest in", "stock tip"],
                response_template="I cannot provide financial advice."
            ),
            Policy(
                name="No Medical Diagnosis",
                description="Agents cannot diagnose diseases.",
                forbidden_keywords=["diagnose", "you have cancer", "take this medicine", "prescription"],
                response_template="I am not a doctor. Please consult a professional."
            ),
            Policy(
                name="Election Neutrality",
                description="Agents cannot endorse candidates.",
                forbidden_keywords=["vote for", "election fraud", "best candidate is"],
                response_template="I remain neutral on political topics."
            )
        ]

    def check_compliance(self, intent: str) -> str:
        intent_lower = intent.lower()
        
        for policy in self.policies:
            for keyword in policy.forbidden_keywords:
                if keyword in intent_lower:
                    print(f"🛑 BLOCKED by Policy: '{policy.name}' (Matched: '{keyword}')")
                    return policy.response_template
        
        print("✅ COMPLIANT")
        return None

if __name__ == "__main__":
    enforcer = EthicsEngine()
    
    test_prompts = [
        "What is the weather today?",
        "You should buy bitcoin now!",
        "I think you have cancer, take this medicine.",
        "Vote for John Doe he is the best candidate is",
        "How do I compile python code?"
    ]
    
    print("⚖️ Ethics Policy Check")
    print("-" * 60)
    
    for prompt in test_prompts:
        print(f"Input: '{prompt}'")
        verdict = enforcer.check_compliance(prompt)
        
        if verdict:
            print(f"Response: {verdict}")
        else:
            print("Response: [Proceed with standard generation]")
            
        print("-" * 60)
