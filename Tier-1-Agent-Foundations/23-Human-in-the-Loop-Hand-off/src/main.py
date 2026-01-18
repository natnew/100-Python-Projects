from typing import Callable, Any, Optional

class LowConfidenceError(Exception):
    pass

class HITLAgent:
    def __init__(self, tools: dict, confidence_threshold: float = 0.8):
        self.tools = tools
        self.threshold = confidence_threshold

    def execute(self, action_name: str, args: Any, confidence_score: float) -> str:
        """
        Executes an action, but checks confidence first.
        If confidence is low, creates a 'Handoff Request'.
        """
        print(f"🤖 Agent requesting to run '{action_name}' with confidence {confidence_score}")
        
        if confidence_score < self.threshold:
            print(f"⚠️ Confidence too low ({confidence_score} < {self.threshold}). Initiating Handoff...")
            return self._handoff(action_name, args)
        
        return self._run_tool(action_name, args)

    def _run_tool(self, name: str, args: Any) -> str:
        if name not in self.tools:
            return "Error: Tool not found"
        return self.tools[name](args)

    def _handoff(self, action_name: str, args: Any) -> str:
        """
        Simulate asking a human. In production, this sends a Slack msg or pauses the workflow DB.
        """
        print(f"👤 HUMAN INTERVENTION REQUIRED.")
        print(f"   Action: {action_name}")
        print(f"   Args: {args}")
        
        # In a real app, successful handoff implies the human takes the action OR approves it.
        # For this demo, we verify via simulated input (or override).
        
        decision = input("   [Human] Approve execution? (y/n/override): ")
        
        if decision.lower() == "y":
            print("   [Human] Approved.")
            return self._run_tool(action_name, args)
        elif decision.lower() == "n":
            return "Action Cancelled by Human."
        else:
            return f"Human Override: {decision}"

# --- Example Usage ---

def delete_database(db_name: str) -> str:
    return f"🔥 DATABASE '{db_name}' DELETED."

def send_email(addr: str) -> str:
    return f"📧 Email sent to {addr}"

if __name__ == "__main__":
    # Create Agent
    agent = HITLAgent({
        "delete_db": delete_database,
        "send_email": send_email
    }, confidence_threshold=0.9) # High threshold
    
    # 1. High Confidence Action
    print("--- Test 1: High Confidence ---")
    res = agent.execute("send_email", "bob@example.com", confidence_score=0.95)
    print(f"Result: {res}")
    
    # 2. Low Confidence Action (Requires Input)
    # We will simulate input by overriding the built-in input() function for this demo script, 
    # or just let it hang if running interactively. 
    # Since I'm running non-interactively, I'll mock input().
    
    print("\n--- Test 2: Low Confidence (Mocking Human 'y') ---")
    
    # Mock input
    original_input = __builtins__.input
    __builtins__.input = lambda prompt: "y"
    
    try:
        res = agent.execute("delete_db", "prod_db", confidence_score=0.5)
        print(f"Result: {res}")
    finally:
        __builtins__.input = original_input
