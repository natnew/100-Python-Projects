import threading
import time
from dataclasses import dataclass
from typing import List

@dataclass
class Operation:
    type: str # 'INSERT' or 'DELETE'
    position: int
    content: str = "" # For insert
    by: str = "Unknown"

class CollaborativeDocument:
    def __init__(self, initial_text: str = ""):
        self.text_buffer = list(initial_text)
        self.history: List[Operation] = []
        self.lock = threading.Lock()

    def apply_op(self, op: Operation):
        with self.lock:
            # Simple Operational logic (Not full OT, but thread-safe atomic apply)
            if op.type == 'INSERT':
                self.text_buffer.insert(op.position, op.content)
            elif op.type == 'DELETE':
                if 0 <= op.position < len(self.text_buffer):
                    del self.text_buffer[op.position]
            
            self.history.append(op)
            print(f"✏️  [{op.by}] {op.type} '{op.content}' at {op.position}")

    def get_text(self) -> str:
        with self.lock:
            return "".join(self.text_buffer)

class WriterAgent(threading.Thread):
    def __init__(self, name: str, doc: CollaborativeDocument, text_to_write: str, start_pos: int):
        super().__init__()
        self.name = name
        self.doc = doc
        self.text = text_to_write
        self.pos = start_pos

    def run(self):
        # Simulate typing character by character
        for i, char in enumerate(self.text):
            time.sleep(0.1)
            op = Operation(
                type='INSERT',
                position=self.pos + i, # NOTE: In real OT, this pos needs checking against other inserts
                content=char,
                by=self.name
            )
            self.doc.apply_op(op)

if __name__ == "__main__":
    doc = CollaborativeDocument("")
    
    print("🎨 Starting Collaborative Editing...")
    
    # Two agents writing simultaneously
    # Agent 1 writes "Hello " at 0
    a1 = WriterAgent("Alice", doc, "Hello ", 0)
    
    # Agent 2 writes "World" at 6 (Assuming Alice finishes, calculating offsets is hard in pure threading without OT)
    # For this simple demo, we rely on the buffer simply growing.
    # However, if they type interlaced, positions shift.
    # Let's verify what happens if they just append.
    
    a1.start()
    time.sleep(0.05) # Slight offset
    a2 = WriterAgent("Bob", doc, "World!", 0) # Bob tries to write at start too! Chaos!
    a2.start()
    
    a1.join()
    a2.join()
    
    print("-" * 60)
    print(f"📄 Final Document: '{doc.get_text()}'")
    print("-" * 60)
    print("Note: Without real OT/CRDT, Bob writing at 0 while Alice writes means mixed text.")
    print("This demonstrates the NEED for complex algorithms (Project 97 Scope is revealing this).")
