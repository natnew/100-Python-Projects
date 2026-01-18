from typing import Dict, Any, List, Callable
import time

class Blackboard:
    def __init__(self):
        self._data: Dict[str, Any] = {}

    def read(self, key: str) -> Any:
        return self._data.get(key)

    def write(self, key: str, value: Any):
        print(f"   📝 Blackboard Update: {key} = {value}")
        self._data[key] = value

    def exists(self, key: str) -> bool:
        return key in self._data

class KnowledgeSource:
    def __init__(self, name: str):
        self.name = name

    def can_contribute(self, blackboard: Blackboard) -> bool:
        """Check preconditions."""
        return False

    def execute(self, blackboard: Blackboard):
        """Write new knowledge."""
        pass

# --- Example Experts ---

class SentenceStarter(KnowledgeSource):
    def can_contribute(self, bb: Blackboard) -> bool:
        return not bb.exists("sentence")

    def execute(self, bb: Blackboard):
        bb.write("sentence", ["The"])
        print(f"      {self.name} started the sentence.")

class NounAdder(KnowledgeSource):
    def can_contribute(self, bb: Blackboard) -> bool:
        s = bb.read("sentence")
        return s and s[-1] == "The"

    def execute(self, bb: Blackboard):
        s = bb.read("sentence")
        s.append("cat")
        bb.write("sentence", s) # Update
        print(f"      {self.name} added a noun.")

class VerbAdder(KnowledgeSource):
    def can_contribute(self, bb: Blackboard) -> bool:
        s = bb.read("sentence")
        return s and s[-1] == "cat"

    def execute(self, bb: Blackboard):
        s = bb.read("sentence")
        s.append("sits")
        bb.write("sentence", s)
        print(f"      {self.name} added a verb.")

class Controller:
    def __init__(self, blackboard: Blackboard, experts: List[KnowledgeSource]):
        self.bb = blackboard
        self.experts = experts

    def run_loop(self, max_steps: int = 5):
        print(f"🏫 Blackboard Session Started.")
        
        for i in range(max_steps):
            print(f"\n--- Step {i+1} ---")
            active_expert = None
            
            # Find first expert who can contribute
            for expert in self.experts:
                if expert.can_contribute(self.bb):
                    active_expert = expert
                    break
            
            if active_expert:
                active_expert.execute(self.bb)
            else:
                print("   💤 No expert can contribute. Stalled.")
                break
                
            time.sleep(0.2)
            
        print(f"\n✅ Final Blackboard: {self.bb._data}")

# --- Example Usage ---

if __name__ == "__main__":
    bb = Blackboard()
    
    # Experts unordered
    experts = [
        VerbAdder("Expert-Verb"),
        SentenceStarter("Expert-Start"),
        NounAdder("Expert-Noun")
    ]
    
    controller = Controller(bb, experts)
    controller.run_loop()
