from typing import List, Dict, Literal
from dataclasses import dataclass, field
from datetime import datetime
import json

@dataclass
class ChatMessage:
    role: Literal["system", "user", "assistant", "function"]
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "role": self.role,
            "content": self.content
        }

class ChatHistory:
    def __init__(self):
        self.messages: List[ChatMessage] = []

    def add_user_message(self, content: str):
        self.messages.append(ChatMessage(role="user", content=content))

    def add_ai_message(self, content: str):
        self.messages.append(ChatMessage(role="assistant", content=content))
    
    def add_system_message(self, content: str):
        self.messages.append(ChatMessage(role="system", content=content))

    def get_messages(self) -> List[Dict]:
        """Return format suitable for LLM APIs (OpenAI)."""
        return [m.to_dict() for m in self.messages]

    def clear(self):
        self.messages = []

    def __str__(self):
        return "\n".join([f"[{m.role.upper()}]: {m.content}" for m in self.messages])

# --- Example Usage ---

if __name__ == "__main__":
    history = ChatHistory()
    
    history.add_system_message("You are a pirate.")
    history.add_user_message("Hello!")
    history.add_ai_message("Ahoy matey!")
    
    print("--- String Repr ---")
    print(history)
    
    print("\n--- JSON Payload ---")
    print(json.dumps(history.get_messages(), indent=2))
