from typing import List, Optional
import time

class Agent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    def execute(self, task: str) -> str:
        raise NotImplementedError

class Specialist(Agent):
    def execute(self, task: str) -> str:
        print(f"      👷 {self.name} ({self.role}) working on: '{task}'")
        time.sleep(0.2)
        return f"[Done: {task}]"

class TeamLead(Agent):
    def __init__(self, name: str, role: str, subordinates: List[Agent]):
        super().__init__(name, role)
        self.subordinates = subordinates

    def execute(self, task: str) -> str:
        print(f"   👨‍💼 {self.name} received: '{task}'. Delegating...")
        
        # Simple delegation strategy: Splitting task or assigning to first avail
        # Here we mock splitting a complex task
        sub_tasks = [f"{task} (Part {i+1})" for i in range(len(self.subordinates))]
        
        results = []
        for i, sub in enumerate(self.subordinates):
            res = sub.execute(sub_tasks[i])
            results.append(res)
            
        return f"Report({', '.join(results)})"

class Director(Agent):
    def __init__(self, name: str, leads: List[TeamLead]):
        super().__init__(name, "Director")
        self.leads = leads

    def assign_goal(self, goal: str) -> str:
        print(f"🎓 {self.name} set goal: '{goal}'")
        
        final_report = []
        for lead in self.leads:
            # Route based on role (mocked logic)
            if "Backend" in goal and lead.role == "Dev Lead":
                final_report.append(lead.execute(goal))
            elif "Research" in goal and lead.role == "Research Lead":
                 final_report.append(lead.execute(goal))
            elif "Full" in goal:
                final_report.append(lead.execute(goal))
                
        return "\n".join(final_report)

# --- Example Usage ---

if __name__ == "__main__":
    # 1. Build Research Team
    r_lead = TeamLead("Alice", "Research Lead", [
        Specialist("R1", "Scraper"),
        Specialist("R2", "Analyst")
    ])
    
    # 2. Build Dev Team
    d_lead = TeamLead("Bob", "Dev Lead", [
        Specialist("D1", "Python Dev"),
        Specialist("D2", "Tester")
    ])
    
    # 3. Director
    director = Director("Eve", [r_lead, d_lead])
    
    # Run
    print("--- Project 1: Market Research ---")
    res1 = director.assign_goal("Full Market Research Phase 1")
    print(f"Output: {res1}\n")
    
    print("--- Project 2: Backend API ---")
    res2 = director.assign_goal("Build Backend API")
    print(f"Output: {res2}")
