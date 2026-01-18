import time
from typing import Dict, Any

class MockFile:
    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content

class Sandbox:
    def __init__(self):
        self.files: Dict[str, MockFile] = {}

    def write_file(self, filename: str, content: str):
        print(f"   💾 Saved '{filename}'")
        self.files[filename] = MockFile(filename, content)

    def run_file(self, filename: str) -> str:
        print(f"   🚀 Executing '{filename}'...")
        if filename not in self.files:
            return "Error: File not found"
        
        content = self.files[filename].content
        
        # Simulate Execution Logic
        if "syntax error" in content.lower():
            return "SyntaxError: invalid syntax on line 1"
        if "division by zero" in content.lower():
            return "ZeroDivisionError: division by zero"
        if "print('hello')" in content:
            return "Hello"
            
        return "Success (No Output)"

class CodingAgent:
    def __init__(self):
        self.sandbox = Sandbox()
        self.max_retries = 3

    def solve(self, problem: str) -> str:
        print(f"👨‍💻 Coder received: '{problem}'")
        
        # 1. Initial Attempt
        code = self._generate_code(problem, attempt=0)
        filename = "solution.py"
        
        for i in range(self.max_retries):
            print(f"\n--- Attempt {i+1} ---")
            self.sandbox.write_file(filename, code)
            
            output = self.sandbox.run_file(filename)
            print(f"   Output: {output}")
            
            if "Error" not in output:
                return f"✅ Solved: {output}"
            
            print("   ❌ Bug detected. Fixing...")
            code = self._fix_code(code, output)
            
        return "❌ Failed to solve after retries."

    def _generate_code(self, problem: str, attempt: int) -> str:
        # Mock LLM generation
        if attempt == 0:
            return "# This has a syntax error"
        return "print('hello')"

    def _fix_code(self, code: str, error: str) -> str:
        # Mock LLM fix
        time.sleep(0.5)
        return "print('hello') # Fixed"

# --- Example Usage ---

if __name__ == "__main__":
    agent = CodingAgent()
    
    # Scene: User wants a Hello World, but the agent fails the first time
    result = agent.solve("Write a hello world script")
    print("\n" + result)
