import time
import uuid
from typing import Dict, List, Set

class Agent:
    def __init__(self, name: str):
        self.name = name

    def receive_broadcast(self, message: str, correlation_id: str) -> str:
        print(f"   🤖 {self.name} heard: '{message}'")
        # Simulate processing time
        time.sleep(0.1)
        return "ACK"

class BroadcastController:
    def __init__(self):
        self.registry: List[Agent] = []

    def register_agent(self, agent: Agent):
        self.registry.append(agent)

    def broadcast(self, message: str, timeout: float = 2.0):
        correlation_id = str(uuid.uuid4())[:8]
        print(f"📢 BROADCAST [{correlation_id}]: {message}")
        print(f"   Targeting {len(self.registry)} agents...")

        acks: Set[str] = set()
        
        # In a real distributed system, this would be async/parallel.
        # Here we simulate the tracking logic.
        start_time = time.time()
        
        for agent in self.registry:
            if time.time() - start_time > timeout:
                print("   ⚠️ Broadcast Timeout!")
                break
                
            try:
                response = agent.receive_broadcast(message, correlation_id)
                if response == "ACK":
                    acks.add(agent.name)
                    print(f"      ✅ Ack from {agent.name}")
            except Exception as e:
                print(f"      ❌ Failed to reach {agent.name}")

        self._report(acks)

    def _report(self, acks: Set[str]):
        total = len(self.registry)
        received = len(acks)
        success_rate = (received / total) * 100 if total > 0 else 0
        
        print("\n--- Broadcast Report ---")
        print(f"Success: {received}/{total} ({success_rate:.0f}%)")
        
        missing = [a.name for a in self.registry if a.name not in acks]
        if missing:
            print(f"Missing ACKs: {missing}")
        else:
            print("All agents acknowledged.")

# --- Example Usage ---

if __name__ == "__main__":
    controller = BroadcastController()
    
    # 1. Register Fleet
    names = ["Alpha", "Beta", "Gamma", "Delta"]
    for n in names:
        controller.register_agent(Agent(n))
        
    # 2. Send Broadcast
    controller.broadcast("SYSTEM_SHUTDOWN_IN_5_MIN")
    
    # 3. Simulate Failure (Unregistered/Offline agent simulation not shown in simple loop, 
    # but covered by logic if register_agent wasn't called)
