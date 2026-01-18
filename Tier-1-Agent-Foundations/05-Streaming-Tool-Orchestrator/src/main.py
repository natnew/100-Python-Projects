import time
import random
from typing import Generator, Any
from dataclasses import dataclass

@dataclass
class ToolEvent:
    type: str # 'progress', 'log', 'result', 'error'
    payload: Any

def search_tool(query: str) -> Generator[ToolEvent, None, str]:
    """
    A simulated long-running search tool that yields progress.
    Returns final result string.
    """
    yield ToolEvent("log", f"Starting search for '{query}'...")
    
    # Simulate step 1: Scraping
    for i in range(1, 4):
        time.sleep(0.5) # Simulate work
        yield ToolEvent("progress", {"step": "scraping", "percent": i * 10})
    
    yield ToolEvent("log", "Scraping complete. Analyzing text...")
    
    # Simulate step 2: Analysis
    for i in range(4, 11):
        time.sleep(0.2)
        yield ToolEvent("progress", {"step": "analyzing", "percent": i * 10})
        if random.random() < 0.1:
            yield ToolEvent("log", "Found interesting citation...")

    yield ToolEvent("log", "Analysis complete.")
    
    # Return final value (Generators can return values in Python 3.3+)
    return f"Summary of '{query}': AI agents are optimizing systems."

class StreamingOrchestrator:
    def execute(self, tool_gen: Generator[ToolEvent, None, str]):
        """
        Consumes the tool generator, prints events, and captures return value.
        """
        result = None
        try:
            while True:
                try:
                    event = next(tool_gen)
                    self._handle_event(event)
                except StopIteration as e:
                    # Capture return value
                    result = e.value
                    break
        except Exception as e:
            print(f"❌ Error: {e}")
            raise e
        
        return result

    def _handle_event(self, event: ToolEvent):
        """Render events to UI/Console."""
        if event.type == "progress":
            p = event.payload
            # Simple progress bar
            bar = "█" * (p["percent"] // 10) + "░" * (10 - p["percent"] // 10)
            print(f"\r[{bar}] {p['percent']}% - {p['step']}", end="", flush=True)
        elif event.type == "log":
             # Clear line and print log
            print(f"\n📝 LOG: {event.payload}")

# --- Example Usage ---

if __name__ == "__main__":
    orchestrator = StreamingOrchestrator()
    print("--- Starting Streaming Tool Execution ---")
    
    # Create the generator
    tool = search_tool("Agent Design Patterns")
    
    # Execute
    final_output = orchestrator.execute(tool)
    
    print(f"\n\n✅ Final Result: {final_output}")
