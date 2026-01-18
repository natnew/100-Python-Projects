import json
import time
import os
import signal
import sys
from typing import Dict, Any

CHECKPOINT_FILE = "agent_state.json"

class CheckpointAgent:
    def __init__(self):
        self.state = {
            "step": 0,
            "data": [],
            "status": "idle"
        }
        self.running = True
        
        # Determine if we should resume
        self._load_state()

        # Handle SigInt
        signal.signal(signal.SIGINT, self._handle_quit)

    def _load_state(self):
        if os.path.exists(CHECKPOINT_FILE):
            try:
                with open(CHECKPOINT_FILE, "r") as f:
                    self.state = json.load(f)
                    print(f"🔄 Resumed from Step {self.state['step']}")
            except Exception as e:
                print(f"⚠️ Corrupt checkpoint: {e}")

    def _save_state(self):
        print(f"💾 Saving checkpoint at Step {self.state['step']}...")
        with open(CHECKPOINT_FILE, "w") as f:
            json.dump(self.state, f, indent=2)

    def _handle_quit(self, signum, frame):
        print("\n🛑 Caught signal. Saving and exiting...")
        self.running = False
        self._save_state()
        sys.exit(0)

    def run_long_process(self):
        print("🚀 Starting Process...")
        
        while self.running and self.state["step"] < 5:
            # Simulate work
            current_step = self.state["step"] + 1
            print(f"   Working on Step {current_step}...")
            time.sleep(1) # Simulate expensive IO
            
            # Update state
            self.state["step"] = current_step
            self.state["data"].append(f"Result of step {current_step}")
            
            # Save
            self._save_state()
            
        print("✅ Process Complete.")
        # Cleanup
        if os.path.exists(CHECKPOINT_FILE):
            os.remove(CHECKPOINT_FILE)

# --- Example Usage ---

if __name__ == "__main__":
    # To test resumption: Run this script, Ctrl+C halfway, then run again.
    # Since I cannot Ctrl+C in this environment easily, I will simulate a "Mock Crash"
    
    # 1. Start fresh
    if os.path.exists(CHECKPOINT_FILE):
        os.remove(CHECKPOINT_FILE)

    print("--- Run 1 (Simulating Crash at Step 3) ---")
    agent = CheckpointAgent()
    
    # Monkeypatch to crash at step 3
    original_save = agent._save_state
    def save_and_crash():
        original_save()
        if agent.state["step"] == 3:
            print("💥 CRASHING PROCESS!")
            sys.exit(1) # Unclean exit
    
    agent._save_state = save_and_crash
    
    try:
        agent.run_long_process()
    except SystemExit:
        pass # Expected crash
        
    print("\n--- Run 2 (Resuming) ---")
    # Should pick up at Step 3 and finish 4, 5
    agent_resume = CheckpointAgent()
    agent_resume.run_long_process()
