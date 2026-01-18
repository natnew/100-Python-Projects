import json
import re
from typing import Type, TypeVar, Any, Callable
from pydantic import BaseModel, ValidationError
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

T = TypeVar("T", bound=BaseModel)

class OutputParserError(Exception):
    """Base error for parsing failures."""
    pass

def extract_json_markdown(text: str) -> str:
    """
    Extracts JSON from a string that might be wrapped in markdown code blocks.
    """
    # Pattern to find ```json ... ``` or just { ... }
    pattern = r"```json\s*(\{.*?\})\s*```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    
    # Fallback: try to find the first { and last }
    text = text.strip()
    if text.startswith("```"):
        # Strip generic code blocks
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
    
    start = text.find("{")
    end = text.rfind("}")
    
    if start != -1 and end != -1:
        return text[start : end + 1]
    
    return text

class StructuredGenerator:
    def __init__(self, llm_func: Callable[[str], str], model: Type[T]):
        self.llm = llm_func
        self.model = model

    def _generate_prompt(self, error: str = "") -> str:
        schema = self.model.model_json_schema()
        base_prompt = f"Return a JSON object matching this schema:\n{json.dumps(schema, indent=2)}"
        if error:
            base_prompt += f"\n\nPrevious attempt failed with error:\n{error}\nTry again and fix the JSON."
        return base_prompt

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1), retry=retry_if_exception_type((ValidationError, OutputParserError)))
    def generate(self, user_prompt: str) -> T:
        """
        Generates structured output. Retries on validation error.
        """
        # This is a simplifed loop. In a real generic agent, we'd pass the conversation history.
        # For this pattern demo, we assume a single-turn structured extraction.
        
        # 1. format prompt
        system_prompt = self._generate_prompt()
        full_prompt = f"{system_prompt}\n\nUser Input: {user_prompt}"
        
        # 2. Call LLM
        raw_output = self.llm(full_prompt)
        print(f"DEBUG: Validating LLM Output: {raw_output[:50]}...")
        
        # 3. Extract JSON
        json_str = extract_json_markdown(raw_output)
        
        # 4. Parse & Validate
        try:
            data = json.loads(json_str)
            return self.model.model_validate(data)
        except json.JSONDecodeError as e:
            # In a more advanced version, we'd retry these too
            raise OutputParserError(f"Invalid JSON: {e}")
        except ValidationError as e:
            # Re-raise to trigger tenacity retry
            print(f"DEBUG: Validation Error: {e}")
            raise e

# --- Example Usage ---

class UserProfile(BaseModel):
    name: str
    age: int
    interests: list[str]

# Mock LLM that simulates a failure first
call_count = 0
def mock_llm(prompt: str) -> str:
    global call_count
    call_count += 1
    if call_count == 1:
        # Failure case: Bad JSON (missing quote)
        return '```json\n{"name": "Alice", "age": 25, "interests": ["AI", "Parsing]}\n```' 
    elif call_count == 2:
        # Failure case: Wrong Schema (age is string)
        return '{"name": "Alice", "age": "twenty", "interests": ["AI"]}'
    else:
        # Success
        return '```json\n{"name": "Alice", "age": 30, "interests": ["Coding", "Agents"]}\n```'

if __name__ == "__main__":
    generator = StructuredGenerator(mock_llm, UserProfile)
    try:
        result = generator.generate("Extract info for Alice")
        print(f"\n✅ SUCCESS:\n{result.model_dump_json(indent=2)}")
    except Exception as e:
        print(f"\n❌ FAILED: {e}")
