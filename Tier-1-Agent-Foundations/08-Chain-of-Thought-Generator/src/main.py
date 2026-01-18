import re
from typing import Dict
from dataclasses import dataclass

@dataclass
class CoTResult:
    reasoning: str
    answer: str

class ChainOfThoughtParser:
    """
    Parses output where reasoning is separated from the answer.
    Supports standard XML-like tags <thought> and <answer>.
    """
    def parse(self, text: str) -> CoTResult:
        # Try finding tags
        thought_match = re.search(r"<thought>(.*?)</thought>", text, re.DOTALL)
        answer_match = re.search(r"<answer>(.*?)</answer>", text, re.DOTALL)
        
        if thought_match and answer_match:
            return CoTResult(
                reasoning=thought_match.group(1).strip(), 
                answer=answer_match.group(1).strip()
            )
            
        # Fallback: Look for "Answer:" keyword if no tags
        # "Reasoning... \nAnswer: ..."
        if "Answer:" in text:
            parts = text.split("Answer:", 1)
            return CoTResult(reasoning=parts[0].strip(), answer=parts[1].strip())
            
        # Fallback: Treat whole text as reasoning if explicit failure
        return CoTResult(reasoning=text, answer="[Parser: No explicit answer found]")

def apply_cot_template(query: str, method: str = "zero_shot") -> str:
    if method == "zero_shot":
        return f"{query}\n\nLet's think step by step."
    elif method == "structured":
        return (
            f"Question: {query}\n\n"
            "Respond in this format:\n"
            "<thought>\nYour step-by-step reasoning here.\n</thought>\n"
            "<answer>\nThe final concise answer here.\n</answer>"
        )
    return query

# --- Example Usage ---

if __name__ == "__main__":
    parser = ChainOfThoughtParser()
    
    # Simulate LLM outputs
    responses = [
        # Structured Success
        """<thought>
        1. The user asks for 15% of 200.
        2. 10% of 200 is 20.
        3. 5% is half of 10%, so 10.
        4. 20 + 10 = 30.
        </thought>
        <answer>30</answer>""",
        
        # Keyword Fallback
        """First calculate the radius. Radius is 5.
        Area is pi*r^2 = 25pi.
        Answer: 25pi""",
        
        # Failure
        """Just 42."""
    ]
    
    for i, raw in enumerate(responses):
        print(f"--- Response {i+1} ---")
        result = parser.parse(raw)
        print(f"Reasoning: {result.reasoning[:50]}...")
        print(f"Answer:    {result.answer}")
