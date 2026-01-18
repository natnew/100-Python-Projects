from dataclasses import dataclass
from typing import List
import time
import random

@dataclass
class Memory:
    timestamp: int
    desc: str
    importance: int # 1-10

class GenAgent:
    def __init__(self, name: str, bio: str):
        self.name = name
        self.bio = bio
        self.memory_stream: List[Memory] = []
        self.plan: str = "Idle"
        self.location: str = "Home"

    def observe(self, observation: str):
        print(f"   👀 {self.name} saw: '{observation}'")
        # In a real system, LLM rates importance. Mocked here.
        importance = 5
        if "fire" in observation: importance = 10
        if "coffee" in observation: importance = 2
        
        self.memory_stream.append(Memory(int(time.time()), observation, importance))

    def generate_plan(self):
        # Mock LLM Logic based on memories
        last_mem = self.memory_stream[-1].desc if self.memory_stream else ""
        
        print(f"   🧠 {self.name} is planning...")
        if "coffee" in last_mem:
            self.plan = "Go to Cafe"
        elif "work" in last_mem:
            self.plan = "Go to Office"
        else:
            self.plan = "Walk around"
            
        print(f"      👉 New Plan: {self.plan}")

    def act(self):
        print(f"   🏃 {self.name} acting: {self.plan}")
        if "Cafe" in self.plan:
            self.location = "Cafe"
        elif "Office" in self.plan:
            self.location = "Office"

    def chat(self, other: 'GenAgent'):
        print(f"   💬 {self.name} tells {other.name}: 'Did you see the news?'")
        other.observe(f"{self.name} talked about news")

# --- Simulation Engine ---

class TownSimulation:
    def __init__(self):
        self.agents: List[GenAgent] = []

    def add_agent(self, agent: GenAgent):
        self.agents.append(agent)

    def step(self):
        print("\n--- Town Clock Tick ---")
        
        # 1. Observe Environment (Mocked global events)
        event = random.choice(["The sun rises", "A dog barks", "The coffee shop opens"])
        for a in self.agents:
            a.observe(event)
            
        # 2. Plan
        for a in self.agents:
            a.generate_plan()
            
        # 3. Act
        for a in self.agents:
            a.act()
            
        # 4. Interact (If same location)
        locations = {}
        for a in self.agents:
            locations.setdefault(a.location, []).append(a)
            
        for loc, present in locations.items():
            if len(present) > 1:
                print(f"   📍 At {loc}: {present[0].name} meets {present[1].name}")
                present[0].chat(present[1])

# --- Example Usage ---

if __name__ == "__main__":
    town = TownSimulation()
    
    alice = GenAgent("Alice", "Loves coffee")
    bob = GenAgent("Bob", "Workaholic")
    
    town.add_agent(alice)
    town.add_agent(bob)
    
    # Run 2 Steps
    town.step()
    time.sleep(1)
    town.step()
