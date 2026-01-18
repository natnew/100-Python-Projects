import time
import queue
import threading
import uuid
from typing import List, Dict, Any, Optional

class Task:
    def __init__(self, name: str, payload: Any):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.payload = payload
        self.result = None

class Worker(threading.Thread):
    def __init__(self, name: str, task_queue: queue.Queue, result_queue: queue.Queue):
        super().__init__()
        self.name = name
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.daemon = True # Die when main dies

    def run(self):
        print(f"   👷 {self.name} ready.")
        while True:
            try:
                task = self.task_queue.get(timeout=3) # Timeout to exit if empty for testing
                print(f"   👷 {self.name} processing task {task.id} ({task.name})...")
                
                # Simulate Work
                time.sleep(0.5)
                task.result = f"Processed {task.payload} by {self.name}"
                
                self.result_queue.put(task)
                self.task_queue.task_done()
            except queue.Empty:
                break # Exit loop for demo purposes

class MasterController:
    def __init__(self, num_workers: int = 3):
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.workers = []
        self.num_workers = num_workers

    def submit_job(self, tasks: List[Task]):
        print(f"🎓 Master: Received Batch Job with {len(tasks)} tasks.")
        
        # 1. Enqueue Tasks
        for t in tasks:
            self.task_queue.put(t)
            
        # 2. Spawn Workers
        for i in range(self.num_workers):
            w = Worker(f"Worker-{i+1}", self.task_queue, self.result_queue)
            w.start()
            self.workers.append(w)
            
        # 3. Wait for Queue to Drain
        self.task_queue.join()
        print("🎓 Master: All tasks completed.")
        
        # 4. Collect results
        results = []
        while not self.result_queue.empty():
            results.append(self.result_queue.get())
            
        return results

# --- Example Usage ---

if __name__ == "__main__":
    master = MasterController(num_workers=2)
    
    # Create Tasks
    tasks = [
        Task("Process Doc 1", "data_1"),
        Task("Process Doc 2", "data_2"),
        Task("Process Doc 3", "data_3"),
        Task("Process Doc 4", "data_4"),
        Task("Process Doc 5", "data_5")
    ]
    
    start_time = time.time()
    results = master.submit_job(tasks)
    duration = time.time() - start_time
    
    print("\n--- Final Report ---")
    print(f"Duration: {duration:.2f}s")
    for r in results:
        print(f"[{r.id}] {r.result}")
