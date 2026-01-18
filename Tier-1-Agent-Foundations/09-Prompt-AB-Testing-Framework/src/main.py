import random
from typing import Callable, List, Dict
from dataclasses import dataclass

@dataclass
class ExperimentResult:
    variant_a_score: int
    variant_b_score: int
    details: List[Dict]

class PromptExperimentRunner:
    def __init__(self, judge_func: Callable[[str, str, str], str]):
        """
        judge_func: (input, output_a, output_b) -> 'A' or 'B' (or 'Tie')
        """
        self.judge = judge_func

    def run(self, 
            dataset: List[str], 
            variant_a_func: Callable[[str], str], 
            variant_b_func: Callable[[str], str]
           ) -> ExperimentResult:
        
        score_a = 0
        score_b = 0
        details = []

        print(f"Running experiment on {len(dataset)} items...")
        
        for i, item in enumerate(dataset):
            out_a = variant_a_func(item)
            out_b = variant_b_func(item)
            
            winner = self.judge(item, out_a, out_b)
            
            if winner == 'A': score_a += 1
            elif winner == 'B': score_b += 1
            
            details.append({
                "input": item,
                "output_a": out_a,
                "output_b": out_b,
                "winner": winner
            })
            print(f"[{i+1}/{len(dataset)}] Winner: {winner}")

        return ExperimentResult(score_a, score_b, details)

# --- Example Usage ---

# 1. Define Prompts (Variants)
def prompt_variant_a(topic: str) -> str:
    # Verbose
    return f"Here is a detailed explanation about {topic}. It is very interesting..."

def prompt_variant_b(topic: str) -> str:
    # Concise
    return f"Summary: {topic}."

# 2. Define Judge (Heuristic for demo, commonly another LLM)
def mock_llm_judge(input_text: str, a: str, b: str) -> str:
    # Prefer concise (Variant B)
    if len(b) < len(a):
        return 'B'
    return 'A'

if __name__ == "__main__":
    runner = PromptExperimentRunner(mock_llm_judge)
    
    dataset = [
        "AI Agents",
        "Python",
        "Generative Models"
    ]
    
    result = runner.run(dataset, prompt_variant_a, prompt_variant_b)
    
    print("\n--- Final Results ---")
    print(f"Variant A Score: {result.variant_a_score}")
    print(f"Variant B Score: {result.variant_b_score}")
    
    if result.variant_b_score > result.variant_a_score:
        print("🏆 Variant B Wins!")
    else:
        print("🏆 Variant A Wins!")
