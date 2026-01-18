import threading
import time
import random
import uuid
from typing import Dict, Optional

class DistributedLockManager:
    """
    Simulates a centralized lock service like Redis or ZooKeeper.
    """
    def __init__(self):
        self._locks: Dict[str, str] = {} # resource_id -> owner_token
        self._internal_lock = threading.Lock() # Thread-safety for the manager itself

    def acquire(self, resource: str, owner: str, ttl: float = 5.0) -> bool:
        with self._internal_lock:
            current_owner = self._locks.get(resource)
            
            if current_owner is None:
                self._locks[resource] = owner
                print(f"   🔒 {owner} acquired lock on '{resource}'")
                return True
            
            if current_owner == owner:
                 print(f"   🔒 {owner} re-acquired lock on '{resource}'")
                 return True
                 
            return False

    def release(self, resource: str, owner: str):
        with self._internal_lock:
            current_owner = self._locks.get(resource)
            if current_owner == owner:
                del self._locks[resource]
                print(f"   🔓 {owner} released lock on '{resource}'")
            else:
                print(f"   ⚠️ {owner} tried to release lock held by {current_owner}")

class Agent(threading.Thread):
    def __init__(self, name: str, manager: DistributedLockManager, resource: str):
        super().__init__()
        self.name = name
        self.manager = manager
        self.resource = resource

    def run(self):
        print(f"🤖 {self.name} wants '{self.resource}'...")
        
        # Retry Loop
        attempts = 0
        while attempts < 5:
            if self.manager.acquire(self.resource, self.name):
                try:
                    self._critical_section()
                finally:
                    self.manager.release(self.resource, self.name)
                return
            else:
                wait = random.uniform(0.1, 0.5)
                print(f"   ⏳ {self.name} waiting {wait:.2f}s...")
                time.sleep(wait)
                attempts += 1
        
        print(f"❌ {self.name} gave up.")

    def _critical_section(self):
        print(f"      📝 {self.name} writing to shared file...")
        time.sleep(0.3) # Simulate work
        print(f"      ✅ {self.name} done.")

# --- Example Usage ---

if __name__ == "__main__":
    lock_manager = DistributedLockManager()
    target_resource = "database.db"
    
    # Spawn 3 agents fighting for the same resource
    agents = [
        Agent("Agent-A", lock_manager, target_resource),
        Agent("Agent-B", lock_manager, target_resource),
        Agent("Agent-C", lock_manager, target_resource)
    ]
    
    for a in agents:
        a.start()
        
    for a in agents:
        a.join()
