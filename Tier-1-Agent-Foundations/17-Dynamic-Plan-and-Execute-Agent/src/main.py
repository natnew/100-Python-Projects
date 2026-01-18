from typing import List, Any
from dataclasses import dataclass

@dataclass
class PlanStep:
    id: int
    description: str

class Planner:
    def create_plan(self, goal: str) -> List[PlanStep]:
        """
        Mock Planner. In production, this uses an LLM.
        System Prompt: "Break the user's goal into a numbered list of steps."
        """
        print(f"🧠 PLANNING for goal: '{goal}'")
        
        # Simulated Plan for "Research and Write Report"
        if "research" in goal.lower():
            return [
                PlanStep(1, "Search for information about topic."),
                PlanStep(2, "Summarize the search results."),
                PlanStep(3, "Write the final report.")
            ]
        return [PlanStep(1, f"Solve: {goal}")]

class Executor:
    def __init__(self, tools: dict):
        self.tools = tools

    def execute_plan(self, plan: List[PlanStep]):
        print("⚙️ EXECUTING Plan...")
        context = ""
        
        for step in plan:
            print(f"  👉 Step {step.id}: {step.description}")
            # In a real agent, the "Solver" sees the step + context and chooses a tool.
            # Here, we mock the solver logic based on keywords.
            
            output = ""
            if "Search" in step.description:
                output = self.tools["search"]("Python Agents")
            elif "Summarize" in step.description:
                output = self.tools["summarize"](context)
            elif "Write" in step.description:
                output = self.tools["write"](context)
            
            print(f"     ✅ Result: {output[:40]}...")
            context += f"\nStep {step.id} Result: {output}"
        
        return context

# --- Example Tools ---
def mock_search(query: str) -> str:
    return "Search Result: Python agents are autonomous useful systems."

def mock_summarize(text: str) -> str:
    return "Summary: Agents are useful systems."

def mock_write(text: str) -> str:
    return "Final Report: Agents are useful systems. They can plan and execute."

# --- Example Usage ---

if __name__ == "__main__":
    planner = Planner()
    executor = Executor({
        "search": mock_search,
        "summarize": mock_summarize,
        "write": mock_write
    })
    
    user_goal = "Research Python Agents and write a report."
    
    # 1. Plan
    plan = planner.create_plan(user_goal)
    for s in plan:
        print(f"  [Plan]: {s.id}. {s.description}")
        
    print("-" * 20)
    
    # 2. Execute
    final_output = executor.execute_plan(plan)
    
    print("-" * 20)
    print(f"Final Output:\n{final_output}")
