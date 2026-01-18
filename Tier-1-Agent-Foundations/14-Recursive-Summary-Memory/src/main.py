from typing import List
from dataclasses import dataclass

@dataclass
class Message:
    role: str
    content: str

class SummaryMemory:
    def __init__(self, max_messages: int = 4):
        self.max_messages = max_messages
        self.summary = ""
        self.buffer = []

    def add_message(self, role: str, content: str):
        self.buffer.append(Message(role, content))
        if len(self.buffer) > self.max_messages:
            self._condense()

    def _condense(self):
        """
        Takes the oldest messages and updates the running summary.
        """
        # Pop oldest 2 messages (usually a user-ai pair)
        to_summarize = self.buffer[:2]
        self.buffer = self.buffer[2:]

        conversation_text = "\n".join([f"{m.role}: {m.content}" for m in to_summarize])
        
        # Simulate LLM Call: "Update this summary with these new lines"
        new_summary = self.mock_llm_summarize(self.summary, conversation_text)
        
        print(f"DEBUG: Summarizing {len(to_summarize)} msgs -> Updated Summary")
        self.summary = new_summary

    def mock_llm_summarize(self, current_summary: str, new_lines: str) -> str:
        """
        In production, this calls OpenAI:
        Prompt: 'Update the summary based on the new lines.'
        """
        # Simple heuristic for demo: Append extraction
        # Real logic would be: return llm.predict(prompt)
        
        # Taking the last few words as a "summary" of the new text
        mini_update = new_lines.split()[-3:] if new_lines else []
        mini_update_str = " ".join(mini_update)
        
        if not current_summary:
            return f"User discussed {mini_update_str}."
        return f"{current_summary} Then discussed {mini_update_str}."

    def get_context(self) -> str:
        """Returns the context to inject into prompt."""
        recent = "\n".join([f"{m.role}: {m.content}" for m in self.buffer])
        return f"PREVIOUS SUMMARY:\n{self.summary}\n\nRECENT MESSAGES:\n{recent}"

# --- Example Usage ---

if __name__ == "__main__":
    mem = SummaryMemory(max_messages=2)
    
    # Turn 1
    print("--- Turn 1 ---")
    mem.add_message("user", "Hi, my name is Alice.")
    mem.add_message("ai", "Hello Alice!")
    print(mem.get_context())
    
    # Turn 2 (Should trigger summarization of Turn 1)
    print("\n--- Turn 2 (Trigger Summary) ---")
    mem.add_message("user", "I like coding Python.")
    mem.add_message("ai", "Python is great.")
    print(mem.get_context())
    
    # Turn 3 (Should trigger summarization of Turn 2)
    print("\n--- Turn 3 (Trigger Summary) ---")
    mem.add_message("user", "I'm building an agent.")
    print(mem.get_context())
