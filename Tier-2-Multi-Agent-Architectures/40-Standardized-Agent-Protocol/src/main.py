from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict
import json

class Performative(Enum):
    REQUEST = "REQUEST"         # User asks for an action
    INFORM = "INFORM"           # Agent provides information
    REFUSE = "REFUSE"           # Agent declines action
    AGREE = "AGREE"             # Agent accepts action
    NOT_UNDERSTOOD = "NOT_UNDERSTOOD" # Parsing error

@dataclass
class ACLMessage:
    performative: Performative
    sender: str
    receiver: str
    content: Any
    language: str = "json"
    ontology: str = "general"
    
    def to_json(self) -> str:
        return json.dumps({
            "performative": self.performative.value,
            "sender": self.sender,
            "receiver": self.receiver,
            "content": self.content,
            "language": self.language,
            "ontology": self.ontology
        }, indent=2)

    @staticmethod
    def from_json(json_str: str) -> 'ACLMessage':
        data = json.loads(json_str)
        return ACLMessage(
            performative=Performative(data["performative"]),
            sender=data["sender"],
            receiver=data["receiver"],
            content=data["content"],
            language=data.get("language", "json"),
            ontology=data.get("ontology", "general")
        )

class Agent:
    def __init__(self, name: str):
        self.name = name

    def process_message(self, msg: ACLMessage) -> ACLMessage:
        print(f"[{self.name}] Processing {msg.performative.name} from {msg.sender}")
        
        # 1. Check if I understand the language
        if msg.language != "json":
             return self._reply(msg, Performative.NOT_UNDERSTOOD, "I only speak JSON")

        # 2. Check Intent
        if msg.performative == Performative.REQUEST:
            if msg.content == "delete_db":
                return self._reply(msg, Performative.REFUSE, "Permission Denied")
            return self._reply(msg, Performative.AGREE, "Will do.")
        
        return self._reply(msg, Performative.NOT_UNDERSTOOD, "Unknown performative")

    def _reply(self, original: ACLMessage, performative: Performative, content: Any) -> ACLMessage:
        return ACLMessage(
            performative=performative,
            sender=self.name,
            receiver=original.sender,
            content=content,
            ontology=original.ontology
        )

# --- Example Usage ---

if __name__ == "__main__":
    server = Agent("Server")
    
    # Test 1: Valid Request
    msg1 = ACLMessage(
        performative=Performative.REQUEST,
        sender="Client",
        receiver="Server",
        content="ping"
    )
    
    print("--- Message 1 ---")
    print(f"Sent: {msg1.to_json()}")
    reply1 = server.process_message(msg1)
    print(f"Replied: {reply1.performative.name} -> {reply1.content}")
    
    # Test 2: Dangerous Request (Refusal)
    msg2 = ACLMessage(
        performative=Performative.REQUEST,
        sender="Hacker",
        receiver="Server",
        content="delete_db"
    )
    
    print("\n--- Message 2 ---")
    reply2 = server.process_message(msg2)
    print(f"Replied: {reply2.performative.name} -> {reply2.content}")
