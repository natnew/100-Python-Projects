from pydantic import BaseModel
from typing import Optional

class InputSchema(BaseModel):
    query: str
    context: Optional[dict] = None

class OutputSchema(BaseModel):
    result: str
    confidence: float

def run_pattern(data: InputSchema) -> OutputSchema:
    """
    Main entry point for the pattern.
    
    Args:
        data: Validated input data
        
    Returns:
        OutputSchema: Validated output
    """
    # TODO: Implement pattern logic
    return OutputSchema(result="Hello World", confidence=0.0)

if __name__ == "__main__":
    # Simple smoke test
    print(run_pattern(InputSchema(query="test")))
