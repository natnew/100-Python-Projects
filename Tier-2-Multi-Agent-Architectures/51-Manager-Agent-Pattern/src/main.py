import time
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    description: str
    assigned_to: str
    status: str = "pending"
    result: str = ""

class Agent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    def do_work(self, task: Task):
        print(f"   👷 {self.name} ({self.role}) starting: '{task.description}'...")
        time.sleep(0.5)
        task.result = f"Completed ({task.description}) by {self.name}"
        task.status = "done"

class ManagerAgent:
    def __init__(self, name: str, workers: List[Agent]):
        self.name = name
        self.workers = workers

    def run_mission(self, mission: str):
        print(f"🎓 {self.name} received mission: '{mission}'")
        
        # 1. Decompose (Simulated Planning)
        tasks = self._plan_mission(mission)
        print(f"   📋 Plan created with {len(tasks)} steps.")
        
        # 2. Delegate & Execute
        context = []
        for task in tasks:
            worker = self._select_worker(task)
            if worker:
                worker.do_work(task)
                context.append(task.result)
            else:
                print(f"   ❌ No worker found for: {task.description}")
        
        # 3. Aggregate
        self._summarize(context)

    def _plan_mission(self, mission: str) -> List[Task]:
        """
        In a real LLM system, this would call GPT-4 to generate a JSON plan.
        Here we mock the logic.
        """
        if "website" in mission.lower():
            return [
                Task(1, "Design Homepage Layout", "Designer"),
                Task(2, "Write HTML/CSS", "Coder"),
                Task(3, "Test Responsiveness", "QA")
            ]
        return [Task(1, "Generic Task", "Generalist")]

    def _select_worker(self, task: Task) -> Agent:
        """Find the best worker for the job."""
        for w in self.workers:
            if w.role == task.assigned_to:
                return w
        # Fallback
        return self.workers[0]

    def _summarize(self, results: List[str]):
        print("\n--- Final Output ---")
        print(f"Mission Accomplished. {len(results)} steps completed.")
        for r in results:
            print(f" - {r}")

# --- Example Usage ---

if __name__ == "__main__":
    # Setup Team
    team = [
        Agent("Alice", "Designer"),
        Agent("Bob", "Coder"),
        Agent("Charlie", "QA")
    ]
    
    manager = ManagerAgent("Eve", team)
    
    # Run
    manager.run_mission("Build a new personal website")
