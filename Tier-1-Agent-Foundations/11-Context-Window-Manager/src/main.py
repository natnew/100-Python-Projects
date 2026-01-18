import tiktoken
from typing import List, Dict, Literal
from dataclasses import dataclass

@dataclass
class Message:
    role: Literal["system", "user", "assistant", "tool"]
    content: str
    name: str = None

class ContextManager:
    def __init__(self, model: str = "gpt-3.5-turbo", max_tokens: int = 4096):
        self.max_tokens = max_tokens
        self.model = model
        try:
            self.encoder = tiktoken.encoding_for_model(model)
        except KeyError:
            self.encoder = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        return len(self.encoder.encode(text))
    
    def count_message_tokens(self, messages: List[Message]) -> int:
        """
        Approximate token count for a list of messages.
        (Matches OpenAI's calculation roughly).
        """
        count = 0
        for msg in messages:
            count += 4  # Per message overhead (role, etc)
            count += self.count_tokens(msg.content)
            if msg.name:
                count += 1
        count += 2 # Reply prime
        return count

    def trim(self, messages: List[Message], preserve_system: bool = True) -> List[Message]:
        """
        Trims messages from the start (FIFO) until they fit.
        Always tries to preserve the System message if requested.
        """
        if not messages:
            return []

        # Separate system message if needed
        sysem_msg = None
        working_list = list(messages)
        
        if preserve_system and working_list[0].role == "system":
            sysem_msg = working_list.pop(0)

        # Naive approach: Pop from index 0 until fit
        # Optimized: Calculate total, then subtract as we pop
        current_tokens = self.count_message_tokens(working_list)
        if sysem_msg:
             current_tokens += self.count_message_tokens([sysem_msg])
        
        while current_tokens > self.max_tokens and working_list:
            removed = working_list.pop(0) # Remove oldest
            # Recalculate or approximate subtraction (safest to recalc for acc)
            # Optimization: subtract len(removed) - overhead
            current_tokens = self.count_message_tokens(working_list)
            if sysem_msg:
                 current_tokens += self.count_message_tokens([sysem_msg])
        
        if sysem_msg:
            working_list.insert(0, sysem_msg)
            
        return working_list

# --- Example Usage ---

if __name__ == "__main__":
    manager = ContextManager(max_tokens=50) # Very small limit for demo
    
    msgs = [
        Message("system", "You are a helpful assistant."),
        Message("user", "Hello, how are you?"),
        Message("assistant", "I am fine, thank you!"),
        Message("user", "Tell me a very long story about AI."),
        Message("assistant", "Once upon a time there was an AI...")
    ]
    
    print(f"Total Tokens (Original): {manager.count_message_tokens(msgs)}")
    
    trimmed = manager.trim(msgs)
    
    print(f"Total Tokens (Trimmed): {manager.count_message_tokens(trimmed)}")
    print("\n--- Remaining Messages ---")
    for m in trimmed:
        print(f"[{m.role}]: {m.content}")
