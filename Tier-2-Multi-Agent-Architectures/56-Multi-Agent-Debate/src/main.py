import time
from typing import List, Optional

class Debater:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role # Affirmative or Negative

    def speak(self, context: List[str]) -> str:
        print(f"   🎤 {self.name} ({self.role}) is thinking...")
        time.sleep(0.5)
        
        last_point = context[-1] if context else "Start"
        
        # Mocking LLM logic for demo
        if self.role == "Affirmative":
            if "Start" in last_point:
                return "The Earth is round because of gravity and satellite imagery."
            if "looks flat" in last_point:
                return "Local observation is limited. Ships disappear hull-first over the horizon."
            
        if self.role == "Negative":
            if "satellite" in last_point:
                return "But from my window, it looks flat. How do you explain that?"
            if "hull-first" in last_point:
                return "I accept the ship evidence. You win."
                
        return "I rest my case."

class Moderator:
    def __init__(self, agent_a: Debater, agent_b: Debater):
        self.agent_a = agent_a
        self.agent_b = agent_b
        self.transcript: List[str] = []

    def run_debate(self, topic: str, max_rounds: int = 3):
        print(f"📢 Debate Topic: '{topic}'\n")
        self.transcript.append(f"Topic: {topic}")
        
        for i in range(max_rounds):
            print(f"--- Round {i+1} ---")
            
            # Agent A speaks
            arg_a = self.agent_a.speak(self.transcript)
            print(f"   🗣️ {self.agent_a.name}: {arg_a}")
            self.transcript.append(arg_a)
            
            if "You win" in arg_a or "rest my case" in arg_a:
                break

            # Agent B speaks
            arg_b = self.agent_b.speak(self.transcript)
            print(f"   🗣️ {self.agent_b.name}: {arg_b}")
            self.transcript.append(arg_b)

            if "You win" in arg_b or "rest my case" in arg_b:
                break
                
        print("\n🔨 Debate Concluded.")
        self._judge()

    def _judge(self):
        print("   ⚖️ Moderator Verdict: The Affirmative side presented stronger evidence regarding ships and horizons.")

# --- Example Usage ---

if __name__ == "__main__":
    alice = Debater("Alice", "Affirmative")
    bob = Debater("Bob", "Negative")
    
    mod = Moderator(alice, bob)
    mod.run_debate("Is the Earth round?")
