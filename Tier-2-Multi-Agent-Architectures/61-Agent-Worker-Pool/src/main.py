import queue
import time
import threading
import uuid
from typing import Optional

class Agent:
    def __init__(self, id: int):
        self.id = id
        self.memory = []

    def process(self, task: str):
        print(f"   🤖 Agent-{self.id} processing: {task}")
        self.memory.append(task) # Accumulate garbage state
        time.sleep(0.5)

    def reset(self):
        """Sanitize state before reuse."""
        print(f"      🧹 Agent-{self.id} wiping memory...")
        self.memory = []

class AgentPool:
    def __init__(self, size: int):
        self.pool = queue.Queue(maxsize=size)
        self.size = size
        
        print(f"🏊 Initializing Pool with {size} agents...")
        for i in range(size):
            self.pool.put(Agent(i))

    def acquire(self, timeout: float = 3.0) -> Optional[Agent]:
        try:
            agent = self.pool.get(timeout=timeout)
            print(f"   ✅ Acquired Agent-{agent.id}")
            return agent
        except queue.Empty:
            print("   ⏳ Pool exhausted! Waiting...")
            return None

    def release(self, agent: Agent):
        agent.reset()
        self.pool.put(agent)
        print(f"   🔙 Released Agent-{agent.id}")

# --- Worker Thread ---

def client_worker(pool: AgentPool, task_id: str):
    agent = pool.acquire()
    if agent:
        try:
            agent.process(f"Task-{task_id}")
        finally:
            pool.release(agent)
    else:
        print(f"   ❌ Task-{task_id} failed: No agents available.")

# --- Example Usage ---

if __name__ == "__main__":
    # Create a small pool of 2 agents
    pool = AgentPool(size=2)
    
    # Simulate 5 concurrent requests
    threads = []
    print("\n--- Burst of Activity ---")
    for i in range(5):
        t = threading.Thread(target=client_worker, args=(pool, str(i)))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
