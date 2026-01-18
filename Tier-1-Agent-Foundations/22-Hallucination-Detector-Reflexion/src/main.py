from typing import Callable, Tuple

class ReflexionAgent:
    def __init__(self, generator: Callable[[str, str], str], critic: Callable[[str], Tuple[bool, str]]):
        self.generator = generator
        self.critic = critic

    def run(self, query: str, max_retries: int = 3) -> str:
        print(f"🏁 Starting Reflexion on: '{query}'")
        
        feedback = ""
        for i in range(max_retries):
            print(f"\n--- Attempt {i+1} ---")
            
            # Generate (with optional feedback from previous turn)
            draft = self.generator(query, feedback)
            print(f"📝 Draft: {draft}")
            
            # Critique
            is_valid, critique = self.critic(draft)
            if is_valid:
                print("✅ Critique passed.")
                return draft
            
            print(f"❌ Critique failed: {critique}")
            feedback = critique
            
        print("⚠️ Max retries reached. Returning last draft.")
        return draft

# --- Example Usage ---

# 1. Generator (simulates a model that hallucinates initially)
def mock_generator(query: str, feedback: str = "") -> str:
    if not feedback:
        # First attempt: Hallucination
        return "The Python programming language was released in 1850."
    else:
        # Second attempt: Fix based on feedback
        return "The Python programming language was released in 1991."

# 2. Critic (simulates a fact checker)
def mock_critic(draft: str) -> Tuple[bool, str]:
    if "1850" in draft:
        return False, "1850 is historically impossible for computers. Check the date."
    return True, "Looks reasonable."

if __name__ == "__main__":
    agent = ReflexionAgent(mock_generator, mock_critic)
    final = agent.run("When was Python released?")
    
    print(f"\n🏆 Final Answer: {final}")
