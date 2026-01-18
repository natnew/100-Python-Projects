import time
import random
import threading
from dataclasses import dataclass
from typing import Dict
from queue import Queue

# Try to import rich, but fallback if not available (though standard env usually has it in this context, or we simulate)
try:
    from rich.console import Console
    from rich.table import Table
    from rich.live import Live
    from rich.layout import Layout
    from rich import box
except ImportError:
    print("❌ 'rich' library not found. Please install it (pip install rich) to see the dashboard.")
    exit(1)

@dataclass
class AgentHeartbeat:
    name: str
    status: str  # "Idle", "Working", "Error", "Sleeping"
    cpu_usage: int
    memory_usage: int
    last_seen: float

class MonitoredAgent(threading.Thread):
    def __init__(self, name: str, dashboard_queue: Queue):
        super().__init__()
        self.name = name
        self.queue = dashboard_queue
        self.running = True

    def run(self):
        while self.running:
            # Simulate work
            status = random.choice(["Idle", "Working", "Working", "Sleeping"])
            if random.random() < 0.1:
                status = "Error"
            
            cpu = random.randint(10, 90) if status == "Working" else random.randint(0, 5)
            mem = random.randint(100, 500)
            
            beat = AgentHeartbeat(
                name=self.name,
                status=status,
                cpu_usage=cpu,
                memory_usage=mem,
                last_seen=time.time()
            )
            self.queue.put(beat)
            
            time.sleep(random.uniform(0.5, 2.0))

class Dashboard:
    def __init__(self):
        self.console = Console()
        self.queue = Queue()
        self.agents: Dict[str, AgentHeartbeat] = {}

    def update_data(self):
        while not self.queue.empty():
            beat = self.queue.get()
            self.agents[beat.name] = beat

    def generate_table(self) -> Table:
        table = Table(title="🕵️ Agent Observatory", box=box.ROUNDED)
        table.add_column("Agent Name", style="cyan", no_wrap=True)
        table.add_column("Status", style="magenta")
        table.add_column("CPU %", justify="right")
        table.add_column("Mem (MB)", justify="right")
        table.add_column("Last Seen", justify="right")

        current_time = time.time()
        
        for name, beat in sorted(self.agents.items()):
            # Status Color
            status_style = "green"
            if beat.status == "Working": status_style = "blue"
            if beat.status == "Sleeping": status_style = "dim white"
            if beat.status == "Error": status_style = "bold red"
            
            # Latency Check
            latency = current_time - beat.last_seen
            latency_str = f"{latency:.1f}s"
            if latency > 3.0:
                latency_str = f"⚠️ {latency_str}"
            
            table.add_row(
                name,
                f"[{status_style}]{beat.status}[/{status_style}]",
                f"{beat.cpu_usage}%",
                f"{beat.memory_usage}",
                latency_str
            )
        return table

    def run(self, duration=10):
        with Live(self.generate_table(), refresh_per_second=4) as live:
            for _ in range(duration * 4): # loops based on refresh rate
                self.update_data()
                live.update(self.generate_table())
                time.sleep(0.25)

if __name__ == "__main__":
    # Setup System
    dash = Dashboard()
    
    agents = [
        MonitoredAgent("Crawler-01", dash.queue),
        MonitoredAgent("Crawler-02", dash.queue),
        MonitoredAgent("Parser-Alpha", dash.queue),
        MonitoredAgent("Parser-Beta", dash.queue),
        MonitoredAgent("DB-Writer", dash.queue),
        MonitoredAgent("Auth-Service", dash.queue)
    ]
    
    for a in agents:
        a.start()
        
    try:
        dash.run(duration=10)
    except KeyboardInterrupt:
        pass
    finally:
        for a in agents:
            a.running = False
        print("\n🛑 Dashboard Stopped.")
