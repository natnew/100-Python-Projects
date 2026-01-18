from dataclasses import dataclass, field
from typing import Dict, Optional, List
from collections import deque

@dataclass
class Envelope:
    sender: str
    recipient: str
    content: str

class Agent:
    def __init__(self, agent_id: str, router: 'MessageRouter'):
        self.id = agent_id
        self.router = router
        self.inbox: deque[Envelope] = deque()

    def send(self, recipient_id: str, content: str):
        print(f"[{self.id}] Sending to {recipient_id}: '{content}'")
        self.router.route(Envelope(self.id, recipient_id, content))

    def receive(self, envelope: Envelope):
        self.inbox.append(envelope)
        print(f"   📬 [{self.id}] Received message from {envelope.sender}")

    def check_inbox(self):
        print(f"\n--- {self.id} Checking Inbox ({len(self.inbox)}) ---")
        while self.inbox:
            msg = self.inbox.popleft()
            print(f"   Reading: '{msg.content}' from {msg.sender}")

class MessageRouter:
    def __init__(self):
        self._directory: Dict[str, Agent] = {}

    def register(self, agent: Agent):
        self._directory[agent.id] = agent
        print(f"📖 Registered {agent.id}")

    def route(self, envelope: Envelope):
        target = self._directory.get(envelope.recipient)
        if target:
            target.receive(envelope)
        else:
            print(f"   ❌ Delivery Failed: Recipient '{envelope.recipient}' not found.")
            # In a real system: Bounce back to sender

# --- Example Usage ---

if __name__ == "__main__":
    router = MessageRouter()
    
    # Setup Agents
    alice = Agent("alice", router)
    bob = Agent("bob", router)
    charlie = Agent("charlie", router)
    
    router.register(alice)
    router.register(bob)
    router.register(charlie)
    
    print("\n--- Interaction ---")
    alice.send("bob", "Hello Bob!")
    bob.send("alice", "Hi Alice, got it.")
    alice.send("charlie", "Secret message.")
    alice.send("dave", "Are you there?") # Dave doesn't exist
    
    # Process
    alice.check_inbox()
    bob.check_inbox()
    charlie.check_inbox()
