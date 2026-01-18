from typing import List, Dict
import random

class Voter:
    def __init__(self, name: str, bias: str = "random"):
        self.name = name
        self.bias = bias # strict, lenient, or random

    def vote(self, proposal: str) -> bool:
        print(f"   🤔 {self.name} considering '{proposal}'...")
        
        # Simulate decision logic
        if self.bias == "strict":
            return False
        if self.bias == "lenient":
            return True
        
        # Random logic for demo
        val = random.random()
        decision = val > 0.5
        return decision

class ConsensusMechanism:
    def __init__(self, voters: List[Voter]):
        self.voters = voters

    def reach_consensus(self, proposal: str) -> bool:
        print(f"🗳️  Starting Vote on: '{proposal}'")
        
        votes_yes = 0
        votes_no = 0
        
        for voter in self.voters:
            decision = voter.vote(proposal)
            if decision:
                votes_yes += 1
                print(f"      ✅ {voter.name} voted YES")
            else:
                votes_no += 1
                print(f"      ❌ {voter.name} voted NO")
                
        total = votes_yes + votes_no
        print(f"📊 Tally: YES={votes_yes}, NO={votes_no}")
        
        # Simple Majority
        if votes_yes > total / 2:
            print(f"🏆 Proposal PASSED.")
            return True
        else:
            print(f"🚫 Proposal REJECTED.")
            return False

# --- Example Usage ---

if __name__ == "__main__":
    # 1. Setup Committee
    committee = [
        Voter("Alice", "lenient"),
        Voter("Bob", "strict"),
        Voter("Charlie", "random"),
        Voter("Dave", "random"),
        Voter("Eve", "lenient")
    ]
    
    consensus = ConsensusMechanism(committee)
    
    # 2. Run Votes
    print("--- Vote 1: Deploy to Production ---")
    consensus.reach_consensus("Deploy v2.0")
    
    print("\n--- Vote 2: Grant Admin Access ---")
    consensus.reach_consensus("Give Admin to User123")
