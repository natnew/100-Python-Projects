import queue
import time
import threading
import json
import datetime
from typing import Dict, Any

class LogRecord:
    def __init__(self, service: str, level: str, message: str):
        self.timestamp = datetime.datetime.now().isoformat()
        self.service = service
        self.level = level
        self.message = message

    def to_json(self) -> str:
        return json.dumps(self.__dict__)

class LogAggregator:
    def __init__(self):
        self.queue = queue.Queue()
        self.logs = []
        self.running = True
        self._thread = threading.Thread(target=self._process_queue)
        self._thread.start()

    def submit(self, service: str, level: str, message: str):
        record = LogRecord(service, level, message)
        self.queue.put(record)

    def _process_queue(self):
        print("   📂 Log Aggregator listening...")
        while self.running or not self.queue.empty():
            try:
                record = self.queue.get(timeout=0.5)
                self.logs.append(record)
                # print(f"      [Aggregator] Ingested: {record.message}") 
            except queue.Empty:
                continue

    def stop(self):
        self.running = False
        self._thread.join()

    def query(self, level: str = None, service: str = None):
        print(f"\n--- Query: Level={level or '*'}, Service={service or '*'} ---")
        filtered = [
            l for l in self.logs 
            if (level is None or l.level == level) and 
               (service is None or l.service == service)
        ]
        
        for l in filtered:
            print(f"[{l.timestamp}] {l.level.ljust(5)} | {l.service}: {l.message}")

# --- Example Usage ---

def worker_simulation(aggregator: LogAggregator, name: str):
    aggregator.submit(name, "INFO", "Starting up")
    time.sleep(0.1)
    aggregator.submit(name, "INFO", "Processing data")
    
    if "B" in name:
        aggregator.submit(name, "WARN", "High latency detected")
    if "C" in name:
        aggregator.submit(name, "ERROR", "Connection refused")
        
    aggregator.submit(name, "INFO", "Shutting down")

if __name__ == "__main__":
    agg = LogAggregator()
    
    # Simulate Agents
    threads = []
    for name in ["Service-A", "Service-B", "Service-C"]:
        t = threading.Thread(target=worker_simulation, args=(agg, name))
        t.start()
        threads.append(t)
        
    for t in threads:
        t.join()
        
    agg.stop()
    
    # Run Queries
    agg.query(level="ERROR")
    agg.query(service="Service-B")
