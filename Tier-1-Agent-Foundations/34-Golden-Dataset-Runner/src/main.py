from dataclasses import dataclass
from typing import List, Callable, Any

@dataclass
class EvalCase:
    id: str
    query: str
    expected: str

@dataclass
class EvalResult:
    case_id: str
    passed: bool
    actual: str
    score: float

class EvalRunner:
    def __init__(self, agent_func: Callable[[str], str]):
        self.agent = agent_func

    def run_dataset(self, dataset: List[EvalCase]) -> List[EvalResult]:
        print(f"🧪 Starting Evaluation on {len(dataset)} cases...")
        results = []
        
        for case in dataset:
            print(f"   Running Case {case.id}...")
            actual = self.agent(case.query)
            
            # Simple Grader: "Contains" check
            # In production, use embeddings or LLM-as-a-Judge
            passed = case.expected.lower() in actual.lower()
            score = 1.0 if passed else 0.0
            
            res = EvalResult(case.id, passed, actual, score)
            results.append(res)
            
            icon = "✅" if passed else "❌"
            print(f"   {icon} Result: {score}")

        return results

# --- Example Usage ---

# 1. Mock Agent
def my_agent(query: str) -> str:
    if "capital of france" in query.lower():
        return "The capital of France is Paris."
    if "2 + 2" in query:
        return "The answer is 4."
    return "I don't know."

if __name__ == "__main__":
    # 2. Define Golden Dataset
    dataset = [
        EvalCase("1", "What is the capital of France?", "Paris"),
        EvalCase("2", "What is 2 + 2?", "4"),
        EvalCase("3", "Who is the president of Mars?", "Elon") # Intentionally failing
    ]
    
    # 3. Run Eval
    runner = EvalRunner(my_agent)
    results = runner.run_dataset(dataset)
    
    # 4. Summarize
    total_score = sum(r.score for r in results)
    accuracy = total_score / len(results) * 100
    
    print("\n--- Summary ---")
    print(f"Accuracy: {accuracy:.1f}%")
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        print(f"[{r.case_id}] {status} | Expected: ... | Actual: {r.actual}")
