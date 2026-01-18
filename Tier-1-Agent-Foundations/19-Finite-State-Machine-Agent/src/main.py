from enum import Enum, auto
from typing import Dict, Callable

class State(Enum):
    IDLE = auto()
    RESEARCHING = auto()
    WRITING = auto()
    REVIEWING = auto()
    DONE = auto()

class FSMAgent:
    def __init__(self):
        self.state = State.IDLE
        self.context = {}
    
    def transition(self, event: str, payload: str = ""):
        print(f"\n[Event: {event}] | Current State: {self.state.name}")
        
        if self.state == State.IDLE:
            if event == "START_TASK":
                self.context["topic"] = payload
                self.state = State.RESEARCHING
                self._do_research()
                
        elif self.state == State.RESEARCHING:
            if event == "RESEARCH_COMPLETE":
                self.context["notes"] = payload
                self.state = State.WRITING
                self._do_writing()
            elif event == "RESEARCH_FAILED":
                 print("Cannot write without notes. Retrying...")
                 self._do_research()

        elif self.state == State.WRITING:
            if event == "DRAFT_COMPLETE":
                self.context["draft"] = payload
                self.state = State.REVIEWING
                self._do_review()

        elif self.state == State.REVIEWING:
            if event == "APPROVED":
                self.state = State.DONE
                print(f"✅ TASK COMPLETE. Final Output: {self.context['draft']}")
            elif event == "REJECTED":
                print("Draft rejected. Rewriting...")
                self.state = State.WRITING
                self._do_writing()
    
    # --- Actions executed on state entry ---
    
    def _do_research(self):
        print(f"🔍 ACTION: Researching '{self.context['topic']}'...")
        # Simulating work
        notes = f"Facts about {self.context['topic']}"
        self.transition("RESEARCH_COMPLETE", notes)

    def _do_writing(self):
        print("✍️ ACTION: Writing draft...")
        draft = f"Report on {self.context['topic']} based on {self.context.get('notes', '')}"
        self.transition("DRAFT_COMPLETE", draft)

    def _do_review(self):
        print("👀 ACTION: Reviewing draft...")
        # Simulate Review Logic
        if "bad" in self.context["draft"]:
             self.transition("REJECTED")
        else:
             self.transition("APPROVED")

if __name__ == "__main__":
    agent = FSMAgent()
    
    # Initial Trigger
    agent.transition("START_TASK", "AI Agents")
    
    # The rest happens automatically via the state machine logic
