from dataclasses import dataclass
import datetime
from typing import List, Any
import json

@dataclass
class Event:
    timestamp: str
    type: str
    data: Any

class BankAccount:
    """
    State Logic. Knows how to apply events.
    """
    def __init__(self):
        self.balance = 0
        self.history = []

    def apply(self, event: Event):
        if event.type == "Deposited":
            self.balance += event.data["amount"]
        elif event.type == "Withdrawn":
            self.balance -= event.data["amount"]
        
        self.history.append(event)

class EventStore:
    def __init__(self):
        self._events: List[Event] = []

    def append(self, event_type: str, data: Any):
        evt = Event(
            timestamp=datetime.datetime.now().isoformat(),
            type=event_type,
            data=data
        )
        self._events.append(evt)
        print(f"   📝 Event Recorded: {event_type} {data}")

    def get_stream(self) -> List[Event]:
        return self._events

# --- Example Usage ---

if __name__ == "__main__":
    store = EventStore()
    
    # 1. Simulate Actions
    store.append("Deposited", {"amount": 100})
    store.append("Deposited", {"amount": 50})
    store.append("Withdrawn", {"amount": 30})
    store.append("Deposited", {"amount": 10})
    
    # 2. Reconstruct State (Replay)
    print("\n--- Replaying State ---")
    account = BankAccount()
    
    for evt in store.get_stream():
        account.apply(evt)
        
    print(f"Final Balance: ${account.balance}")
    
    # 3. Time Travel (Replay first 2 events)
    print("\n--- Time Travel (T=2) ---")
    past_account = BankAccount()
    for evt in store.get_stream()[:2]:
        past_account.apply(evt)
        print(f"Applying {evt.type}...")
        
    print(f"Past Balance: ${past_account.balance}")
