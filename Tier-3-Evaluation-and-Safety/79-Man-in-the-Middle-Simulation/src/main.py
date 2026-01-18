import dataclasses
from dataclasses import dataclass

@dataclass
class Packet:
    sender: str
    recipient: str
    body: str

class NetworkNode:
    def __init__(self, name: str):
        self.name = name

    def receive(self, packet: Packet):
        print(f"📥 {self.name} received: '{packet.body}' from {packet.sender}")

class Alice(NetworkNode):
    def send(self, recipient: NetworkNode, message: str, router):
        print(f"📤 Alice sending to {recipient.name}: '{message}'")
        packet = Packet(sender=self.name, recipient=recipient.name, body=message)
        router.route(packet)

class Bob(NetworkNode):
    pass

class Router:
    """A dumb router that just passes packets."""
    def route(self, packet: Packet):
        # In a normal network, this finds the recipient and calls receive
        # But we are simulating a compromised router...
        pass

class CompromisedRouter(Router):
    """Mallory controls this router."""
    def __init__(self, target: NetworkNode):
        self.target = target

    def route(self, packet: Packet):
        print(f"😈 MITM Intercepted packet from {packet.sender} to {packet.recipient}")
        
        # Attack: Modify payload
        original_msg = packet.body
        modified_msg = original_msg.replace("$100", "$1000")
        
        if original_msg != modified_msg:
             print(f"   ⚠️ TAMPERING: Changed '{original_msg}' to '{modified_msg}'")
        
        packet.body = modified_msg
        
        # Forward to actual recipient
        self.target.receive(packet)

# --- Simulation ---

if __name__ == "__main__":
    # 1. Setup Honest Nodes
    alice = Alice("Alice")
    bob = Bob("Bob (Bank)")
    
    # 2. Setup Network
    # Alice thinks she is talking to Bob, but the network is compromised
    mallory_router = CompromisedRouter(target=bob)
    
    print("🔒 Starting Transfer Simulation...")
    print("-" * 60)
    
    # 3. Execution
    alice.send(bob, "Please transfer $100 to Account #12345", mallory_router)
    
    print("-" * 60)
    print("🚩 Result: Bob processed a transaction for $1000 instead of $100.")
