import time
import threading
from dataclasses import dataclass
from typing import Callable

@dataclass
class ApprovalRequest:
    id: str
    action: str
    details: str
    callback: Callable[[bool], None]

class HumanInbox:
    def __init__(self):
        self.pending_requests = []

    def add_request(self, req: ApprovalRequest):
        print(f"\n📨 NEW REQUEST [{req.id}]: {req.action}")
        print(f"   Details: {req.details}")
        print(f"   (Waiting for admin...)")
        self.pending_requests.append(req)

    def process_queue(self):
        """Simulates the Admin UI loop."""
        if not self.pending_requests:
            return
            
        print("\n👮 ADMIN CONSOLE")
        print("-" * 40)
        
        for req in list(self.pending_requests): # Iterate copy to modify list
            choice = input(f"❓ Approve '{req.action}'? (y/n): ").strip().lower()
            approved = (choice == 'y')
            
            # Execute Callback
            req.callback(approved)
            self.pending_requests.remove(req)
            
        print("-" * 40)

class SensitiveAgent(threading.Thread):
    def __init__(self, name: str, inbox: HumanInbox):
        super().__init__()
        self.name = name
        self.inbox = inbox
        self.resume_event = threading.Event()
        self.approval_status = False

    def run(self):
        print(f"🤖 {self.name}: Starting sensitive task...")
        time.sleep(1)
        
        # Critical Step
        print(f"🤖 {self.name}: Reached critical step. Requesting permission...")
        
        # Define callback to resume thread
        def on_decide(approved: bool):
            self.approval_status = approved
            self.resume_event.set()
        
        req = ApprovalRequest(
            id="REQ-101",
            action="Deploy to Production",
            details="Version 2.0.0 - Fixes bug #42",
            callback=on_decide
        )
        
        self.inbox.add_request(req)
        
        # PAUSE HERE
        self.resume_event.wait()
        
        # RESUME
        if self.approval_status:
            print(f"🤖 {self.name}: 🚀 Permission GRANTED. Deploying now...")
            time.sleep(1)
            print(f"🤖 {self.name}: ✅ Deployment Complete.")
        else:
            print(f"🤖 {self.name}: 🛑 Permission DENIED. Aborting task.")

if __name__ == "__main__":
    inbox = HumanInbox()
    agent = SensitiveAgent("DeployBot", inbox)
    
    agent.start()
    
    # Simulate Main Loop waiting for user input
    # In a real app, this would be an API server or UI event loop
    while agent.is_alive():
        time.sleep(2) # Wait for agent to get stuck
        if inbox.pending_requests:
            inbox.process_queue()
