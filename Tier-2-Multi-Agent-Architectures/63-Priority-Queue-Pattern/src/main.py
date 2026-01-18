import heapq
import time
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class Task:
    priority: int
    description: str = field(compare=False)
    
    # Priority: Lower number = Higher priority (Min-Heap behavior)
    # 0 = Critical
    # 10 = High
    # 50 = Normal
    # 100 = Low

class PriorityAgent:
    def __init__(self, name: str):
        self.name = name
        self.queue = [] # Heap

    def add_task(self, priority: int, description: str):
        task = Task(priority, description)
        heapq.heappush(self.queue, task)
        print(f"   📥 [P{priority}] Added: {description}")

    def run(self):
        print("\n--- Starting Execution ---")
        while self.queue:
            task = heapq.heappop(self.queue)
            print(f"   ⚙️ {self.name} executing [P{task.priority}]: {task.description}")
            time.sleep(0.3)
            
        print("   ✅ All tasks complete.")

# --- Example Usage ---

if __name__ == "__main__":
    agent = PriorityAgent("Service-Agent")
    
    # Scene: Random arrival of mixed tasks
    agent.add_task(50, "Update Cache (Normal)")
    agent.add_task(100, "Send Newsletter (Low)")
    agent.add_task(0, "🔥 Fix Server Outage (Critical)")
    agent.add_task(10, "User Password Reset (High)")
    
    # Even though "Update Cache" was first, "Fix Outage" should run first
    agent.run()
