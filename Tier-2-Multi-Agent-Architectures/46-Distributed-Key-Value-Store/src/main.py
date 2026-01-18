import time
import threading
import random
from typing import Dict, Any, Optional

class DistributedStore:
    def __init__(self):
        self._store: Dict[str, Any] = {}
        self._lock = threading.Lock()
        
    def get(self, key: str) -> Optional[Any]:
        # Simulate network latency
        time.sleep(random.uniform(0.01, 0.05))
        with self._lock:
            val = self._store.get(key)
        return val

    def set(self, key: str, value: Any):
        time.sleep(random.uniform(0.01, 0.05))
        with self._lock:
            self._store[key] = value
            print(f"   💾 Store: set '{key}' = {value}")

    def transaction(self, key: str, operation: callable):
        """
        Atomic Read-Modify-Write.
        """
        with self._lock:
            current = self._store.get(key, 0) # Assume int for demo
            new_val = operation(current)
            self._store[key] = new_val
            print(f"   🔄 Transaction: '{key}' {current} -> {new_val}")

class Agent(threading.Thread):
    def __init__(self, name: str, store: DistributedStore):
        super().__init__()
        self.name = name
        self.store = store

    def run(self):
        print(f"🤖 {self.name} starting...")
        
        # 1. Check a flag
        if not self.store.get("system_active"):
            print(f"   🛑 {self.name}: System inactive. Waiting...")
            time.sleep(0.5)
            
        # 2. Increment a shared counter (Inventory)
        # Naive way (Race Condition prone if not for GIL/Atomic, but good to show intent)
        # self.store.set("counter", self.store.get("counter") + 1) 
        
        # Correct way: Transaction
        self.store.transaction("counter", lambda x: x + 1)
        
        # 3. Write personal status
        self.store.set(f"status_{self.name}", "Ready")
        print(f"✅ {self.name} finished.")

# --- Example Usage ---

if __name__ == "__main__":
    store = DistributedStore()
    
    # Init State
    store.set("system_active", True)
    store.set("counter", 0)
    
    print("\n--- Starting Agents ---")
    agents = [Agent(f"Agent-{i}", store) for i in range(5)]
    
    for a in agents:
        a.start()
        
    for a in agents:
        a.join()
        
    print("\n--- Final State ---")
    print(f"Counter: {store.get('counter')} (Expected 5)")
    print(f"Agent-0 Status: {store.get('status_Agent-0')}")
