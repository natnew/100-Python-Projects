import time
import random
from typing import Generator

# Try importing rich, commonly available. If not, we'd fall back (omitted for brevity).
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.prompt import Prompt
    from rich.live import Live
    from rich.spinner import Spinner
except ImportError:
    print("Please install rich: `pip install rich`")
    exit(1)

class AgentCLI:
    def __init__(self, name: str = "Assistant"):
        self.console = Console()
        self.name = name

    def start_session(self):
        self.console.print(Panel(f"Welcome to {self.name} CLI", style="bold blue"))
        self.console.print("[dim]Type 'exit' to quit.[/dim]\n")

        while True:
            user_input = Prompt.ask("[bold green]You[/bold green]")
            
            if user_input.lower() in ["exit", "quit"]:
                self.console.print("\n[yellow]Goodbye![/yellow]")
                break
            
            self._handle_interaction(user_input)

    def _handle_interaction(self, user_input: str):
        # 1. Show Spinner while "thinking"
        with self.console.status("[bold cyan]Thinking...[/bold cyan]", spinner="dots"):
            # Simulate latency
            time.sleep(random.uniform(0.5, 1.5))
        
        # 2. Simulate Streaming Response
        self.console.print(f"[bold purple]{self.name}[/bold purple]: ", end="")
        
        response_text = self._mock_llm_response(user_input)
        
        # We use a Live display to simulate streaming tokens
        # For simplicity here, we just print chunk by chunk
        # In a real app, you'd use Live(Panel(...)) to update content in place
        
        delay = 0.02
        for char in response_text:
            self.console.print(char, end="", style="white")
            time.sleep(delay)
        self.console.print("\n")

    def _mock_llm_response(self, query: str) -> str:
        """Generates a mock markdown response."""
        if "code" in query.lower():
            return (
                "Here is a Python example:\n\n"
                "```python\n"
                "def hello():\n"
                "    print('Hello World')\n"
                "```\n\n"
                "Hope that helps!"
            )
        return f"I received your query: '{query}'. This is a **bold** response with some `inline code`."

if __name__ == "__main__":
    cli = AgentCLI("DevBot")
    cli.start_session()
