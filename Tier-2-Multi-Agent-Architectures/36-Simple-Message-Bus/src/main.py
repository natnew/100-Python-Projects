from dataclasses import dataclass
from typing import Dict, List, Callable, Any
from collections import defaultdict
import datetime

@dataclass
class Message:
    topic: str
    payload: Any
    sender: str
    timestamp: float = 0.0

    def __post_init__(self):
        self.timestamp = datetime.datetime.now().timestamp()

class MessageBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Message], None]]] = defaultdict(list)
        self.history: List[Message] = []

    def subscribe(self, topic: str, handler: Callable[[Message], None]):
        """Register a handler for a specific topic."""
        self._subscribers[topic].append(handler)
        print(f"👂 New subscriber for '{topic}'")

    def publish(self, topic: str, payload: Any, sender: str = "System"):
        """Send a message to all subscribers of the topic."""
        msg = Message(topic, payload, sender)
        self.history.append(msg)
        
        print(f"📣 [{topic}] from {sender}: {str(payload)[:50]}")
        
        if topic in self._subscribers:
            for handler in self._subscribers[topic]:
                try:
                    handler(msg)
                except Exception as e:
                    print(f"   ❌ Error in handler {handler.__name__}: {e}")
        else:
            print(f"   ⚠️ No subscribers for '{topic}'")

# --- Example Usage ---

class Agent:
    def __init__(self, name: str, bus: MessageBus):
        self.name = name
        self.bus = bus

    def listen(self, topic: str):
        self.bus.subscribe(topic, self.handle_message)

    def handle_message(self, msg: Message):
        print(f"   🤖 {self.name} received: {msg.payload}")
        
        # React to specific messages
        if msg.topic == "task_assigned":
            self.bus.publish("task_status", f"{self.name} started working on {msg.payload}", self.name)

if __name__ == "__main__":
    bus = MessageBus()
    
    # 1. Setup Agents
    agent_a = Agent("Agent A", bus)
    agent_b = Agent("Agent B", bus)
    logger = Agent("Logger", bus)
    
    # 2. Subscribe
    agent_a.listen("global_alert")
    agent_b.listen("task_assigned")
    
    # Wildcard or multi-topic subscription handling depends on implementation complexity.
    # Here we keep it simple 1:1 map.
    bus.subscribe("task_status", lambda m: print(f"   📝 Log: Task update from {m.sender}"))
    
    # 3. Publish Events
    print("\n--- Event 1: Global Alert ---")
    bus.publish("global_alert", "Server restarting!", "Admin")
    
    print("\n--- Event 2: Task Assignment ---")
    bus.publish("task_assigned", "Clean Data", "Manager")
