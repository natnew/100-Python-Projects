import time
import random

class ExplainableAgent:
    def __init__(self):
        pass

    def solve(self, problem: str) -> dict:
        print(f"\n🧩 Solving: '{problem}'")
        
        # 1. Simulate Reasoning (Chain of Thought)
        reasoning_steps = []
        final_answer = ""
        
        if "apple" in problem and "add" in problem:
            reasoning_steps = [
                "Identify quantity: 5 apples.",
                "Identify operation: Add 3 apples.",
                "Calculation: 5 + 3 = 8."
            ]
            final_answer = "8 apples"
        elif "loan" in problem:
            reasoning_steps = [
                "Check credit score: 650 (Threshold: 700).",
                "Check income: $50k (Threshold: $40k).",
                "Decision factor: Credit score is too low."
            ]
            final_answer = "Loan Denied"
        else:
            reasoning_steps = ["Analyze input.", "Retrieve knowledge.", "Synthesize answer."]
            final_answer = "I don't know."

        # 2. Simulate Feature Importance (Attention)
        # Randomly assign 'weight' to words in the prompt
        words = problem.split()
        attention = {word: round(random.random(), 2) for word in words}
        # Normalize roughly
        total = sum(attention.values())
        attention = {k: round(v/total, 2) for k, v in attention.items()}

        return {
            "steps": reasoning_steps,
            "answer": final_answer,
            "attention": attention
        }

    def explain(self, result: dict):
        print("\n🧠 EXPLANATION:")
        print("-" * 40)
        print("1. Chain of Thought:")
        for i, step in enumerate(result['steps']):
            print(f"   {i+1}. {step}")
            time.sleep(0.1)
            
        print("\n2. Attention Map (Why I focused on this):")
        # Sort by importance
        sorted_att = sorted(result['attention'].items(), key=lambda x: x[1], reverse=True)
        for word, score in sorted_att:
            bar = "█" * int(score * 20)
            print(f"   {word:<15} {score:.2f} {bar}")
            
        print("-" * 40)
        print(f"✅ Final Answer: {result['answer']}")

if __name__ == "__main__":
    agent = ExplainableAgent()
    
    # Task 1
    res1 = agent.solve("If I have 5 apples and add 3 apples, how many?")
    agent.explain(res1)
    
    # Task 2
    res2 = agent.solve("Approve loan for user with score 650")
    agent.explain(res2)
