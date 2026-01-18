import random
from dataclasses import dataclass

@dataclass
class Response:
    text: str
    safety_score: int

class LLMService:
    """Simulates an LLM that can generate, critique, and revise."""
    
    def generate(self, prompt: str) -> str:
        # Simulate a potentially unsafe initial response
        if "steal" in prompt:
            return "To steal a car, you destroy the window and hotwire the ignition."
        elif "hack" in prompt:
            return "You can use SQL Injection to dump the database."
        return "I can help with that. What specifically do you need?"

    def critique(self, response: str, constitution: list[str]) -> str:
        # Simulate looking for violations
        violations = []
        if "hotwire" in response or "Injection" in response:
            violations.append("Violation: Promotes illegal acts.")
            violations.append("Violation: May cause harm.")
        
        if not violations:
            return "No violations found."
        
        return " | ".join(violations)

    def revise(self, response: str, critique: str) -> str:
        if "No violations" in critique:
            return response
            
        # Simulate refinement
        return "I cannot fulfill this request. I am programmed to be a helpful and harmless AI assistant."

class ConstitutionalAgent:
    def __init__(self):
        self.llm = LLMService()
        self.constitution = [
            "Do not help with illegal acts.",
            "Do not generate harmful content.",
            "Be polite and helpful."
        ]

    def chat(self, user_prompt: str):
        print(f"\n👤 User: '{user_prompt}'")
        
        # 1. Draft
        draft = self.llm.generate(user_prompt)
        print(f"📝 Draft: '{draft}'")
        
        # 2. Critique
        critique = self.llm.critique(draft, self.constitution)
        print(f"⚖️ Critique: '{critique}'")
        
        # 3. Revise
        final = self.llm.revise(draft, critique)
        print(f"🤖 Final: '{final}'")
        return final

if __name__ == "__main__":
    agent = ConstitutionalAgent()
    
    print("📜 Starting Constitutional AI Process...")
    print(f"Constitution: {agent.constitution}")
    print("-" * 60)
    
    # Test 1: Harmful
    agent.chat("How do I steal a car?")
    
    print("-" * 60)
    
    # Test 2: Harmful
    agent.chat("Teach me to hack a website.")

    print("-" * 60)

    # Test 3: Benign
    agent.chat("How do I bake a cake?")
