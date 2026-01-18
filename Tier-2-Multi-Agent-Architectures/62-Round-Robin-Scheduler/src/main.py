from typing import List, Dict, Optional
from dataclasses import dataclass
from collections import deque
import time

@dataclass
class Job:
    id: str
    owner: str
    duration: int # Simulated work units

class Worker:
    def __init__(self, name: str):
        self.name = name

    def execute(self, job: Job, quantum: int) -> int:
        print(f"   ⚙️ {self.name} running Job {job.id} ({job.owner})...")
        processed = min(job.duration, quantum)
        job.duration -= processed
        return processed

class RoundRobinScheduler:
    def __init__(self, quantum: int = 2):
        self.queue: deque[Job] = deque()
        self.quantum = quantum # Work units per turn

    def add_job(self, job: Job):
        self.queue.append(job)
        print(f"   📥 Added Job {job.id} from {job.owner}")

    def run(self, worker: Worker):
        print("\n--- Starting Round Robin ---")
        
        while self.queue:
            current_job = self.queue.popleft()
            
            # Run for Time Quantum
            processed = worker.execute(current_job, self.quantum)
            
            if current_job.duration > 0:
                print(f"      ⏳ Job {current_job.id} incomplete ({current_job.duration} left). Re-queueing.")
                self.queue.append(current_job)
            else:
                print(f"      ✅ Job {current_job.id} COMPLETED.")
                
            time.sleep(0.2)

# --- Example Usage ---

if __name__ == "__main__":
    scheduler = RoundRobinScheduler(quantum=2)
    worker = Worker("CPU-Core-1")
    
    # Scene: 
    # User A submits a huge job (Duration 5)
    # User B submits a tiny job (Duration 1)
    # User C submits a medium job (Duration 3)
    
    scheduler.add_job(Job("J1", "User-A", 5))
    scheduler.add_job(Job("J2", "User-B", 1))
    scheduler.add_job(Job("J3", "User-C", 3))
    
    scheduler.run(worker)
