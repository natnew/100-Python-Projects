import json
import uuid
import datetime
import os
from typing import Any, Dict

class TraceLogger:
    def __init__(self, log_file: str = "traces.jsonl"):
        self.log_file = log_file
        self.run_id = str(uuid.uuid4())
        self.session_start = datetime.datetime.utcnow().isoformat()
        
        # Init log entry for this run
        self._log({
            "event": "run_start",
            "run_id": self.run_id,
            "timestamp": self.session_start
        })
        print(f"📝 Logging run {self.run_id} to {log_file}")

    def log_step(self, step_name: str, input_data: Any, output_data: Any, metadata: Dict = None):
        entry = {
            "event": "step",
            "run_id": self.run_id,
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "step": step_name,
            "input": input_data,
            "output": output_data,
            "metadata": metadata or {}
        }
        self._log(entry)

    def log_error(self, step_name: str, error_msg: str):
        entry = {
            "event": "error",
            "run_id": self.run_id,
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "step": step_name,
            "error": error_msg
        }
        self._log(entry)

    def _log(self, data: Dict):
        # JSON Lines format: One JSON object per line
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")

# --- Example Usage ---

if __name__ == "__main__":
    # 1. Start Logger
    tracer = TraceLogger()
    
    # 2. Simulate Agent Steps
    tracer.log_step("search_tool", 
                   input_data={"query": "Weather in NY"}, 
                   output_data="25C, Sunny",
                   metadata={"latency_ms": 120})
    
    tracer.log_step("llm_reasoning", 
                   input_data="Context: 25C...", 
                   output_data="It is warm in NY.")
    
    # 3. Simulate Error
    try:
        raise ValueError("API Connection Failed")
    except Exception as e:
        tracer.log_error("api_call", str(e))
        
    print("\n--- Log File Content ---")
    with open("traces.jsonl", "r") as f:
        print(f.read())
